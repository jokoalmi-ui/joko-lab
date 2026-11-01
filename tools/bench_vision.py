#!/usr/bin/env python3
"""Batería de medición de modelos locales de visión del LAB (instrumento versionado).

Arranca cada GGUF con `llama-server` del backend CUDA de LM Studio, lanza las
pruebas con material REAL del laboratorio y mide VRAM pico, TTFT, tokens/s y
acierto. Nació como `bateria.py` en el scratch el 01-nov-2026 y se versiona para
no perder el instrumento (el scratch se poda a las 24 h).

Tres defectos ya medidos y aquí blindados (sin ellos las cifras son falsas):
  1. Otro `llama-server` vivo en el puerto → los modelos dan tiempos idénticos.
     Se comprueba el puerto libre antes de arrancar y se aborta.
  2. GLM y gemma emiten `reasoning_content` antes de `content` (respuestas
     vacías si solo se lee `delta.content`). Se acumula aparte y también cuenta
     como primer token.
  3. `tool_calls` llega en deltas parciales: se indexan por `index` y se
     concatenan, o los argumentos salen truncados.

Uso:
    python3 tools/bench_vision.py --listar
    python3 tools/bench_vision.py --modelo gemma --repeticiones 3
    python3 tools/bench_vision.py --puntuar ~/.hermes/cache/scratch/bench-vision/resultados.json

`--repeticiones N` repite cada prueba N veces y guarda métricas por repetición
(la mediana va en el campo principal; RULE-015: una sola medida no se publica).
Solo lectura sobre el lab: escribe únicamente en --dir (scratch por defecto).
"""
import argparse
import base64
import json
import os
import re
import socket
import statistics
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.request

SRV = os.path.expanduser(
    "~/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.61.0/llama-server")
VENDOR = os.path.expanduser(
    "~/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1")
ENV = dict(os.environ, LD_LIBRARY_PATH=VENDOR + ":" + os.path.dirname(SRV))

DEF_DIR = os.path.expanduser("~/.hermes/cache/scratch/bench-vision")
DEF_FICHA = ("/home/jokoalmi/joko-lab/research/infografias/"
             "perfume-del-dia-20261101/perfume_del_dia_v5_indigo_suede_corr.png")
DEF_DOC = os.path.expanduser(
    "~/joko-lab/research/material-bench-vision/docp6-006.png")  # página 6 del PDF de empleo, 110 dpi

M = "/mnt/ssd_ia_datos/LM STUDIO"
MODELOS = [
    ("GLM-4.6V-Flash", f"{M}/lmstudio-community/GLM-4.6V-Flash-GGUF/GLM-4.6V-Flash-Q4_K_M.gguf",
     f"{M}/lmstudio-community/GLM-4.6V-Flash-GGUF/mmproj-GLM-4.6V-Flash-F16.gguf"),
    ("LFM2.5-VL-3B", f"{M}/lmstudio-community/LFM2.5-VL-3B-GGUF/LFM2.5-VL-3B-Q4_K_M.gguf",
     f"{M}/lmstudio-community/LFM2.5-VL-3B-GGUF/mmproj-LFM2.5-VL-3B-Q8_0.gguf"),
    ("gemma-4-12B-it", f"{M}/lmstudio-community/gemma-4-12B-it-QAT-GGUF/gemma-4-12B-it-QAT-Q4_0.gguf",
     f"{M}/lmstudio-community/gemma-4-12B-it-QAT-GGUF/mmproj-gemma-4-12B-it-QAT-BF16.gguf"),
    ("granite-4.1-8B", f"{M}/unsloth/granite-4.1-8b-GGUF/granite-4.1-8b-Q4_K_S.gguf", None),
]

TOOLS = [{"type": "function", "function": {
    "name": "buscar_precio",
    "description": "Devuelve el precio de un perfume de la colección",
    "parameters": {"type": "object", "properties": {
        "perfume": {"type": "string"}, "ml": {"type": "integer"}},
        "required": ["perfume", "ml"]}}}]

# Verdad conocida del material de prueba (ficha publicada y página 6 del PDF).
FICHA_OK = {"nombre": ["indigo suede", "indigo"], "casa": ["lunio"],
            "precio": ["120"], "tamano": ["100 ml", "100ml"]}
DOC_OK = {1943: ["mcculloch", "pitts", "neurona"], 1950: ["turing"],
          1956: ["mccarthy"], 1958: ["lisp"], 1966: ["eliza"],
          1986: ["retropropag", "perceptr", "rumelhart"],
          1997: ["deep blue", "ajedrez", "kasparov"],
          2022: ["chatgpt", "openai"]}


# ---------------------------------------------------------------- utilidades
def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def vram_mib():
    try:
        o = subprocess.run(["nvidia-smi", "--query-gpu=memory.used",
                            "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10).stdout
        return int(o.strip().split("\n")[0])
    except Exception:
        return -1


def port_free(port):
    s = socket.socket()
    try:
        s.settimeout(1)
        s.connect(("127.0.0.1", port))
        return False
    except Exception:
        return True
    finally:
        s.close()


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def score_ficha(t):
    t = norm(t)
    hits = [k for k, vs in FICHA_OK.items() if any(v in t for v in vs)]
    return len(hits), ",".join(hits)


def score_doc(t):
    t = norm(t)
    hits = []
    for year, keys in DOC_OK.items():
        m = re.search(rf"\b{year}\b.{{0,90}}", t, re.S)
        if m and any(k in m.group(0) for k in keys):
            hits.append(year)
    return len(hits), ",".join(map(str, hits))


def tool_ok(tc):
    if not tc:
        return "no"
    t = tc.lower()
    name = "buscar_precio" in t
    args = ("indigo" in t or "perfume" in t) and "100" in t
    return "si" if (name and args) else ("parcial" if name else "no")


# ------------------------------------------------------------------ medición
class Sampler(threading.Thread):
    """Muestrea VRAM en paralelo a la petición; el pico es el máximo visto."""

    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0
        self.stop = False

    def run(self):
        while not self.stop:
            self.peak = max(self.peak, vram_mib())
            time.sleep(0.3)


def chat(base, payload, timeout=300):
    payload = dict(payload, stream=True, stream_options={"include_usage": True},
                   temperature=0.0)
    req = urllib.request.Request(base + "/v1/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    s = Sampler()
    s.start()
    t0 = time.time()
    ttft = None
    chunks, think, tcs, usage, fin = [], [], [], None, None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    j = json.loads(data)
                except Exception:
                    continue
                if j.get("usage"):
                    usage = j["usage"]
                for ch in j.get("choices", []):
                    d = ch.get("delta") or {}
                    if ch.get("finish_reason"):
                        fin = ch["finish_reason"]
                    if d.get("reasoning_content"):
                        if ttft is None:
                            ttft = time.time() - t0
                        think.append(d["reasoning_content"])
                    if d.get("content"):
                        if ttft is None:
                            ttft = time.time() - t0
                        chunks.append(d["content"])
                    for tc in (d.get("tool_calls") or []):
                        i = tc.get("index", 0)
                        while len(tcs) <= i:
                            tcs.append({"id": None, "name": None, "arguments": ""})
                        if tc.get("id"):
                            tcs[i]["id"] = tc["id"]
                        fn = tc.get("function") or {}
                        if fn.get("name"):
                            tcs[i]["name"] = (tcs[i]["name"] or "") + fn["name"]
                        if fn.get("arguments"):
                            tcs[i]["arguments"] += fn["arguments"]
    finally:
        s.stop = True
        s.join(timeout=2)
    total = time.time() - t0
    text = "".join(chunks)
    ct = (usage or {}).get("completion_tokens") or max(1, len(text) // 3)
    gen = total - (ttft or 0)
    return {"seg": round(total, 2), "ttft": round(ttft, 3) if ttft else None,
            "tok_s": round(ct / gen, 1) if gen > 0.2 else None, "tokens": ct,
            "vram_pico": s.peak, "texto": text[:1500], "fin": fin,
            "razonamiento_len": len("".join(think)),
            "tool_calls": json.dumps(tcs, ensure_ascii=False)[:800] if tcs else None}


def start(mm_path, mproj, d, port, ctx=8192):
    if not port_free(port):
        return None, 0.0, "PUERTO %d OCUPADO: hay otro llama-server vivo; no se mide" % port
    cmd = [SRV, "-m", mm_path, "-ngl", "99", "-c", str(ctx), "--port", str(port),
           "--host", "127.0.0.1", "-fa", "auto", "--jinja", "-t", "6", "--no-webui"]
    if mproj:
        cmd += ["--mmproj", mproj]
    logp = os.path.join(d, "server.log")
    log = open(logp, "w")
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                         cwd=os.path.dirname(SRV), env=ENV)
    base = "http://127.0.0.1:%d" % port
    t0 = time.time()
    while time.time() - t0 < 240:
        if p.poll() is not None:
            return None, round(time.time() - t0, 1), open(logp).read()[-800:]
        try:
            with urllib.request.urlopen(base + "/health", timeout=3) as r:
                if json.loads(r.read()).get("status") in ("ok", "no slot available"):
                    return p, round(time.time() - t0, 1), None
        except Exception:
            time.sleep(1)
    p.terminate()
    return None, round(time.time() - t0, 1), "timeout"


def stop(p):
    try:
        p.terminate()
        p.wait(timeout=20)
    except Exception:
        try:
            p.kill()
        except Exception:
            pass
    time.sleep(3)


def mediana(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(statistics.median(vals), 2) if vals else None


def resumen(reps):
    """Métricas de N repeticiones: mediana principal, min/max explícitos."""
    return {"n": len(reps),
            "seg": mediana([r.get("seg") for r in reps]),
            "seg_min": min([r["seg"] for r in reps]) if reps else None,
            "seg_max": max([r["seg"] for r in reps]) if reps else None,
            "ttft": mediana([r.get("ttft") for r in reps]),
            "tok_s": mediana([r.get("tok_s") for r in reps]),
            "tok_s_min": min([r["tok_s"] for r in reps if r.get("tok_s")] or [0]) or None,
            "tok_s_max": max([r["tok_s"] for r in reps if r.get("tok_s")] or [0]) or None,
            "vram_pico": max([r.get("vram_pico") or 0 for r in reps]) if reps else None,
            "razonamiento_len": mediana([r.get("razonamiento_len") for r in reps]),
            "reps": reps}


def run_model(name, pesos, mproj, d, port, ctx, reps_n, ficha, doc):
    base = "http://127.0.0.1:%d" % port
    res = {"modelo": name, "ctx": ctx, "repeticiones": reps_n, "pruebas": {}}
    p, tload, err = start(pesos, mproj, d, port, ctx)
    res["carga_seg"] = tload
    if not p:
        res["error"] = err
        return res

    def varias(payload, n):
        out = []
        for _ in range(n):
            out.append(chat(base, payload))
        return resumen(out)

    try:
        if mproj:
            res["pruebas"]["ficha"] = varias({"max_tokens": 800, "model": name, "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": "Mira esta ficha. Responde SOLO con una línea: "
                                             "NOMBRE | CASA | PRECIO | TAMAÑO"},
                    {"type": "image_url",
                     "image_url": {"url": "data:image/png;base64," + b64(ficha)}}]}]}, reps_n)
            if doc:
                res["pruebas"]["documento"] = varias({"max_tokens": 900, "model": name, "messages": [
                    {"role": "user", "content": [
                        {"type": "text", "text": "Extrae los años y el evento de esta línea de "
                                                 "tiempo, una línea por año con formato AÑO: evento."},
                        {"type": "image_url",
                         "image_url": {"url": "data:image/png;base64," + b64(doc)}}]}]}, reps_n)
            res["pruebas"]["tool_imagen"] = varias({"max_tokens": 600, "model": name, "tools": TOOLS,
                                                    "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": "Usa la herramienta buscar_precio para saber cuánto "
                                             "cuesta el perfume que aparece en la imagen, en 100 ml."},
                    {"type": "image_url",
                     "image_url": {"url": "data:image/png;base64," + b64(ficha)}}]}]}, reps_n)
        res["pruebas"]["tool_texto"] = varias({"max_tokens": 600, "model": name, "tools": TOOLS,
                                               "messages": [{"role": "user", "content":
                    "¿Cuánto cuesta Indigo Suede de Lunio en 100 ml? Usa la herramienta buscar_precio."}]}, reps_n)
        res["pruebas"]["texto_es"] = varias({"max_tokens": 500, "model": name, "messages": [
            {"role": "user", "content": "Explica en tres frases qué es el tool calling en un LLM."}]}, reps_n)
    except Exception as e:
        res["error"] = repr(e)[:400]
    finally:
        stop(p)
    return res


# ------------------------------------------------------------------- puntuar
def puntuar(path):
    res = json.load(open(path))
    for r in res:
        pr = r.get("pruebas", {})
        vram = [v.get("vram_pico") for v in pr.values() if v.get("vram_pico")]
        print(f"\n=== {r.get('modelo')}  carga {r.get('carga_seg')}s  "
              f"VRAM pico {max(vram) if vram else None} MiB"
              + (f"  ERROR: {r['error'][:160]}" if r.get("error") else ""))
        for k in ("ficha", "documento", "tool_imagen", "tool_texto", "texto_es"):
            v = pr.get(k)
            if not v:
                continue
            reps = v.get("reps") or [v]
            base = f"  {k:11s}: {v.get('seg')}s (n={v.get('n', len(reps))}) ttft {v.get('ttft')} " \
                   f"{v.get('tok_s')} t/s"
            if k == "ficha":
                sc = [score_ficha(x.get("texto")) for x in reps]
                base += f"  acierto {max(s[0] for s in sc)}/4 en {sum(1 for s in sc if s[0] == max(x[0] for x in sc))}/{len(sc)} reps"
            elif k == "documento":
                sc = [score_doc(x.get("texto")) for x in reps]
                base += f"  acierto {max(s[0] for s in sc)}/8 en {sum(1 for s in sc if s[0] == max(x[0] for x in sc))}/{len(sc)} reps"
            elif k.startswith("tool"):
                base += "  tool " + ",".join(tool_ok(x.get("tool_calls")) for x in reps)
            print(base)


# --------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="Batería de visión local del LAB")
    ap.add_argument("--dir", default=DEF_DIR, help="directorio de trabajo (logs y JSON)")
    ap.add_argument("--out", default=None, help="JSON de resultados (por defecto <dir>/resultados.json)")
    ap.add_argument("--port", type=int, default=12345)
    ap.add_argument("--ctx", type=int, default=8192)
    ap.add_argument("--repeticiones", type=int, default=1)
    ap.add_argument("--modelo", default=None, help="filtro por nombre (subcadena)")
    ap.add_argument("--ficha", default=DEF_FICHA)
    ap.add_argument("--doc", default=DEF_DOC, help="PNG de la página del PDF para la prueba de línea de tiempo")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--puntuar", default=None, metavar="JSON")
    a = ap.parse_args(argv)

    if a.listar:
        for n, m, mm in MODELOS:
            print(f"{n:16s} mmproj={'si' if mm else 'no ':3s} {m}")
        return 0
    if a.puntuar:
        puntuar(a.puntuar)
        return 0

    os.makedirs(a.dir, exist_ok=True)
    out = a.out or os.path.join(a.dir, "resultados.json")
    try:
        allres = json.load(open(out))
    except Exception:
        allres = []
    for name, pesos, mproj in MODELOS:
        if a.modelo and a.modelo.lower() not in name.lower():
            continue
        print(f"### {name} (n={a.repeticiones})", flush=True)
        r = run_model(name, pesos, mproj, a.dir, a.port, a.ctx, a.repeticiones, a.ficha, a.doc)
        allres = [x for x in allres if x.get("modelo") != name] + [r]
        json.dump(allres, open(out, "w"), ensure_ascii=False, indent=1)
        print(json.dumps({k: v for k, v in r.items() if k != "pruebas"}, ensure_ascii=False), flush=True)
        for k, v in r.get("pruebas", {}).items():
            print(f"  {k}: {v.get('seg')}s [{v.get('seg_min')}-{v.get('seg_max')}] "
                  f"ttft={v.get('ttft')} tok/s={v.get('tok_s')} vram={v.get('vram_pico')}", flush=True)
    print("FIN", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
