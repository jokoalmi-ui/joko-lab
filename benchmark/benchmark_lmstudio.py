#!/usr/bin/env python3
"""Benchmark comparativo de modelos LM Studio.
Mide: tiempo, tokens, calidad de respuesta.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

MODELS = [
    "glm-4.6v-flash",
    "google/gemma-4-12b-qat",
    "qwen/qwen3.5-9b",
]

TESTS = [
    {
        "name": "Razonamiento",
        "prompt": "Tengo 5 archivos en una carpeta. Borro 2. Luego creo 3 nuevos. ¿Cuántos archivos hay ahora? Explica paso a paso.",
        "max_tokens": 300,
        "eval": lambda r: "6" in r or "seis" in r or "5-2+3" in r
    },
    {
        "name": "Código",
        "prompt": "Escribe un script Python que lea un archivo JSON, filtre los elementos donde 'activo' sea true, y los guarde en otro archivo. Solo el código, sin explicación.",
        "max_tokens": 400,
        "eval": lambda r: "json" in r.lower() and ("open" in r or "load" in r) and "filter" in r or "if" in r
    },
    {
        "name": "Extracción",
        "prompt": "Extrae SOLO los nombres de persona de este texto, separados por comas: 'Juan fue a la tienda con María y Pedro, mientras Carlos esperaba en casa. Luego llegó Ana.'",
        "max_tokens": 100,
        "eval": lambda r: "Juan" in r and "María" in r and "Pedro" in r
    },
]

LMS = "/home/jokoalmi/.lmstudio/bin/lms"
API = "http://localhost:1234/v1/chat/completions"
LOG = Path("/mnt/ssd_ia_datos/lab-state/logs/benchmark.log")


def log(msg):
    print(msg)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def run_cmd(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return str(e), -1


def load_model(model_id):
    log(f"  Cargando {model_id}...")
    out, rc = run_cmd([LMS, "load", model_id, "--identifier", model_id], timeout=120)
    if not out and rc != 0:
        log(f"  Error carga: rc={rc}")
        return False
    # Si ya está cargado o se cargó ok, continuamos
    if "loaded" in out.lower() or "successfully" in out.lower() or rc == 0:
        time.sleep(5)
        return True
    log(f"  Posible error: {out[:200]}")
    time.sleep(5)
    return True  # intentamos igual


def unload_all():
    run_cmd([LMS, "unload", "--all"], timeout=10)
    time.sleep(2)


def query_model(model_id, prompt, max_tokens, timeout=120):
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0
    }
    t0 = time.time()
    out, rc = run_cmd([
        "curl", "-s", "--max-time", str(timeout), API,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data)
    ], timeout=timeout + 10)
    elapsed = time.time() - t0

    if rc != 0 or not out:
        return {"error": f"curl fail (rc={rc})", "time_s": round(elapsed, 1), "content": "", "tokens": 0}

    try:
        d = json.loads(out)
        if "error" in d:
            return {"error": d["error"]["message"], "time_s": round(elapsed, 1), "content": "", "tokens": 0}
        msg = d.get("choices", [{}])[0].get("message", {})
        content = (msg.get("content", "") or "") + (msg.get("reasoning_content", "") or "")
        tokens = d.get("usage", {}).get("total_tokens", 0)
        return {
            "content": content,
            "time_s": round(elapsed, 1),
            "tokens": tokens,
            "tok_s": round(tokens / elapsed, 1) if elapsed > 0 else 0,
            "error": None
        }
    except Exception as e:
        return {"error": str(e), "time_s": round(elapsed, 1), "content": out[:200], "tokens": 0}


print("╔══════════════════════════════════════════════════════╗")
print("║         BENCHMARK LM STUDIO — 3 modelos              ║")
print("╚══════════════════════════════════════════════════════╝\n")

results = {}

for model in MODELS:
    print(f"\n{'='*55}")
    print(f"  MODELO: {model}")
    print(f"{'='*55}")

    ok = load_model(model)
    if not ok:
        print(f"  ❌ No se pudo cargar. Saltando.")
        results[model] = [{"test": t["name"], "error": "carga fallida"} for t in TESTS]
        continue

    model_results = []
    for test in TESTS:
        print(f"\n  ── Test: {test['name']} ──")
        print(f"  Prompt: {test['prompt'][:60]}...")
        r = query_model(model, test["prompt"], test["max_tokens"])

        if r["error"]:
            print(f"  ❌ Error: {r['error']}")
            model_results.append({"test": test["name"], "error": r["error"]})
            continue

        passed = test["eval"](r["content"]) if r["content"] else False
        status = "✅" if passed else "⚠️"
        print(f"  {status} Tiempo: {r['time_s']}s | Tokens: {r['tokens']} | Vel: {r['tok_s']} tok/s")
        print(f"  Respuesta: {r['content'][:100]}")
        model_results.append({
            "test": test["name"],
            "passed": passed,
            "time_s": r["time_s"],
            "tokens": r["tokens"],
            "tok_s": r["tok_s"],
        })

    results[model] = model_results
    unload_all()

# ─── Tabla comparativa ────────────────────────────────────
print(f"\n\n{'═'*75}")
print("  TABLA COMPARATIVA")
print(f"{'═'*75}")
print(f"{'Modelo':<28} {'Test':<16} {'Tiempo':<9} {'Tokens':<9} {'tok/s':<9} {'Resultado':<10}")
print(f"{'─'*28} {'─'*16} {'─'*9} {'─'*9} {'─'*9} {'─'*10}")

for model in MODELS:
    first = True
    for r in results.get(model, []):
        if "error" in r:
            print(f"{model if first else '':<28} {r['test']:<16} {'❌ '+r['error']:<37}")
        else:
            ok = "✅" if r["passed"] else "⚠️"
            print(f"{model if first else '':<28} {r['test']:<16} {r['time_s']:<9} {r['tokens']:<9} {r['tok_s']:<9} {ok:<10}")
        first = False

print(f"\n{'═'*75}")
print(f"  VRAM FINAL: ", end="")
out, _ = run_cmd(["nvidia-smi", "--query-gpu=memory.used,memory.free", "--format=csv,noheader,nounits"])
print(out if out else "N/A")
print(f"{'═'*75}")
