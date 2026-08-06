#!/usr/bin/env python3
"""pipeline_proxy.py — Observabilidad del pipeline LLM (Fase A, t2-t4).

Proxy HTTP OpenAI-compatible de medicion. Se coloca entre Hermes y el
proveedor (model.base_url -> http://127.0.0.1:9911/v1) y registra una OBS
por consulta en el ledger de observabilidad.

Mide (fases t2-t4 de la spec observabilidad-pipeline-diseno.md):
  ttfb_ms   : desde el envio de la peticion hasta el primer byte del upstream
  total_ms  : duracion completa de la llamada LLM
  tokens    : prompt/completion si el upstream los devuelve (usage)

NO mide (limite honesto del proxy): t1 contexto, t5 postproceso, t6 entrega,
canal — requieren instrumentacion dentro de Hermes.

Garantias:
  - Reenvio transparente: headers y body del cliente se pasan al upstream
    (excepto Host). La API key viaja en Authorization y NO se registra.
  - Nunca rompe: si el registro falla, la llamada continua.
  - Solo escucha en 127.0.0.1.

Uso:
  python3 pipeline_proxy.py [--port 9911] [--upstream https://api.deepseek.com/v1]
"""
import argparse
import json
import os
import sys
import threading
import time
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LEDGER_DEFAULT = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
_lock = threading.Lock()


def registrar_obs(entry: dict, ledger: str):
    """Append JSONL. Nunca rompe la llamada."""
    try:
        Path(ledger).parent.mkdir(parents=True, exist_ok=True)
        with _lock:
            with open(ledger, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[pipeline_proxy] error registrando OBS: {e}", file=sys.stderr)


def parse_usage(body: bytes, stream: bool):
    """Extrae usage del cuerpo (no-stream) o del ultimo chunk (stream)."""
    if stream:
        # DeepSeek/OpenAI solo incluyen usage en stream con stream_options.
        # Buscamos en el ultimo chunk SSE "[DONE]" y capturamos un usage si viene.
        text = body.decode("utf-8", errors="ignore")
        for line in reversed(text.splitlines()):
            if line.startswith("data:") and line != "data: [DONE]":
                try:
                    d = json.loads(line[5:].strip())
                    if "usage" in d:
                        return d["usage"]
                except Exception:
                    continue
        return None
    try:
        d = json.loads(body.decode("utf-8", errors="ignore"))
        return d.get("usage")
    except Exception:
        return None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    upstream = None      # establecido en main
    ledger = None

    def log_message(self, *args):
        pass  # silenciar el log por defecto

    def _do_proxy(self):
        t_start = time.monotonic()
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        model = None
        stream = False
        try:
            payload = json.loads(body.decode("utf-8", errors="ignore"))
            model = payload.get("model")
            stream = bool(payload.get("stream"))
        except Exception:
            pass

        # Reenvio al upstream: mismo host, path del cliente tal cual
        # (el cliente ya envia el prefijo correcto, p.ej. /v1/chat/completions)
        host = self.upstream.netloc
        path = self.path
        headers = {}
        for k, v in self.headers.items():
            if k.lower() not in ("host", "content-length", "connection", "accept-encoding"):
                headers[k] = v
        headers["Content-Length"] = str(len(body))
        if stream:
            headers.pop("Accept-Encoding", None)  # sin compresion para medir bien

        conn = http.client.HTTPSConnection(host, timeout=900)
        status = 0
        error = None
        usage = None
        ttfb_ms = None
        try:
            conn.request("POST", path, body=body, headers=headers)
            r = conn.getresponse()
            ttfb_ms = round((time.monotonic() - t_start) * 1000, 1)
            status = r.status
            resp_headers = [(k, v) for k, v in r.getheaders()
                            if k.lower() not in ("transfer-encoding", "connection")]
            if stream:
                self.send_response(status)
                for k, v in resp_headers:
                    self.send_header(k, v)
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                chunks = []
                while True:
                    chunk = r.read(8192)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    self.wfile.write(f"{len(chunk):x}\r\n".encode() + chunk + b"\r\n")
                    self.wfile.flush()
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
                usage = parse_usage(b"".join(chunks), stream=True)
            else:
                data = r.read()
                self.send_response(status)
                for k, v in resp_headers:
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
                self.wfile.flush()
                usage = parse_usage(data, stream=False)
        except Exception as e:
            error = str(e)[:200]
            if not status:
                try:
                    msg = f"pipeline_proxy: upstream error: {error}".encode()
                    self.send_response(502)
                    self.send_header("Content-Type", "text/plain")
                    self.send_header("Content-Length", str(len(msg)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(msg)
                    self.wfile.flush()
                except Exception:
                    pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

        total_ms = round((time.monotonic() - t_start) * 1000, 1)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "path": self.path,
            "model": model,
            "provider": "deepseek",
            "stream": stream,
            "ttfb_ms": ttfb_ms,
            "total_ms": total_ms,
            "status": status,
            "prompt_tokens": usage.get("prompt_tokens") if usage else None,
            "completion_tokens": usage.get("completion_tokens") if usage else None,
            "error": error,
        }
        registrar_obs(entry, self.ledger)

    def do_POST(self):
        try:
            self._do_proxy()
        except Exception as e:
            print(f"[pipeline_proxy] handler error: {e}", file=sys.stderr)
            try:
                self.send_response(500)
                self.end_headers()
            except Exception:
                pass

    def do_GET(self):
        # Health check basico
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok","proxy":"pipeline_proxy"}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9911)
    ap.add_argument("--upstream", default="https://api.deepseek.com/v1")
    ap.add_argument("--ledger", default=LEDGER_DEFAULT)
    args = ap.parse_args()

    from urllib.parse import urlparse
    Handler.upstream = urlparse(args.upstream)
    Handler.ledger = args.ledger
    if Handler.upstream.scheme != "https":
        print("El upstream debe ser https", file=sys.stderr)
        sys.exit(1)

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"[pipeline_proxy] escuchando en 127.0.0.1:{args.port} -> {args.upstream}")
    print(f"[pipeline_proxy] ledger OBS: {args.ledger}")
    server.serve_forever()


if __name__ == "__main__":
    main()
