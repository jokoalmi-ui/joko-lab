#!/usr/bin/env python3
"""
reranker_daemon.py - Daemon persistente del reranker (fix cuello de botella 2-ago-2026)

Problema: search.py se ejecuta como subprocess en cada consulta y paga ~11s
por importar sentence_transformers + inicializar CUDA + cargar 2.27GB del
CrossEncoder a VRAM. Este daemon carga el modelo UNA vez y sirve peticiones
por HTTP local, reduciendo la busqueda de ~15s a ~2-3s.

Endpoints:
  GET  /health   -> {"status":"ok","model":...,"device":...}
  POST /rerank   -> {"query": str, "texts": [str,...]} -> {"scores":[float,...]}

Uso:
  python3 reranker_daemon.py [--port 8765] [--model BAAI/bge-reranker-v2-m3]

Servicio systemd: ~/.config/systemd/user/joko-reranker.service
"""
import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from sentence_transformers.cross_encoder import CrossEncoder

DEFAULT_MODEL = "BAAI/bge-reranker-v2-m3"
FALLBACK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DEFAULT_PORT = 8765
# Fix 05-ago-2026 (cuello de botella): los fragmentos del indexer (~1000 chars =
# ~800 tokens) escalaban la latencia linealmente porque el modelo acepta hasta
# 8192 tokens y procesaba TODO. 256 tokens bastan para puntuar relevancia de un
# fragmento; el texto completo se conserva en los resultados (search.py devuelve
# el fragmento entero, solo el rerank usa el prefijo).
DEFAULT_MAX_SEQ = 256

_model = None
_model_name = None
_device = None
_max_seq = DEFAULT_MAX_SEQ


def cargar_modelo(nombre: str, forzar_cpu: bool = False, max_seq: int = DEFAULT_MAX_SEQ):
    """Carga el CrossEncoder intentando GPU primero; cae a CPU si CUDA falla.
    Con forzar_cpu=True, va directo a CPU (libera VRAM para otros modelos).
    max_seq limita los tokens por fragmento en el rerank (fix latencia 05-ago)."""
    global _model_name, _device, _max_seq
    _max_seq = max_seq
    import torch
    if not forzar_cpu and torch.cuda.is_available():
        try:
            print(f"[daemon] Cargando {nombre} en CUDA (max_seq={max_seq})...", flush=True)
            m = CrossEncoder(nombre, device="cuda", max_length=max_seq)
            _device = "cuda"
            return m
        except Exception as e:
            print(f"[daemon] CUDA fallo ({e}), cayo a CPU...", flush=True)
    print(f"[daemon] Cargando {nombre} en CPU (max_seq={max_seq})...", flush=True)
    _device = "cpu"
    return CrossEncoder(nombre, device="cpu", max_length=max_seq)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write(f"[daemon] {fmt % args}\n")

    def _send_json(self, code: int, obj: dict):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            self._send_json(200, {
                "status": "ok",
                "model": _model_name,
                "device": _device,
            })
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        global _model, _model_name
        if urlparse(self.path).path != "/rerank":
            self._send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            query = payload.get("query", "")
            texts = payload.get("texts", [])
            if not query or not texts:
                self._send_json(400, {"error": "query y texts son obligatorios"})
                return
            pairs = [[query, t] for t in texts]
            scores = _model.predict(pairs).tolist()
            self._send_json(200, {"scores": scores})
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def main():
    global _model, _model_name
    parser = argparse.ArgumentParser(description="Daemon persistente del reranker")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--cpu", action="store_true",
                        help="Forzar CPU (libera VRAM para otros modelos en LM Studio)")
    parser.add_argument("--max-seq", type=int, default=DEFAULT_MAX_SEQ,
                        help="Max tokens por fragmento en el rerank (fix latencia, default 256)")
    args = parser.parse_args()

    try:
        _model = cargar_modelo(args.model, forzar_cpu=args.cpu, max_seq=args.max_seq)
        _model_name = args.model
    except Exception as e:
        print(f"[daemon] No se pudo cargar {args.model}: {e}", flush=True)
        print(f"[daemon] Usando fallback {FALLBACK_MODEL}...", flush=True)
        _model = cargar_modelo(FALLBACK_MODEL, forzar_cpu=args.cpu, max_seq=args.max_seq)
        _model_name = FALLBACK_MODEL

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"[daemon] Listo en http://127.0.0.1:{args.port} (modelo: {_model_name}, device: {_device})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[daemon] Detenido.", flush=True)
        server.shutdown()


if __name__ == "__main__":
    main()
