#!/usr/bin/env python3
"""Bateria v2 (01-oct-2026) — extiende la bateria de 7 dimensiones a los modelos
que NO estaban probados (los 8 del 06-ago siguen en bateria_modelos.jsonl).

DIFERENCIAS con bateria_modelos.py (v1), y por que:
  1. Reutiliza EXACTAMENTE las mismas pruebas y los mismos evaluadores (import de
     PRUEBAS) para que los resultados sean comparables con el historico.
  2. `fecha` se calcula con datetime (v1 la tenia fijada a "2026-08-06").
  3. Timeout configurable (default 1200 s). v1 usaba 300 s fijos: un modelo de
     razonamiento a 7 tok/s con max_tokens=2000 tarda ~260 s y podia dar FAIL falso.
  4. Warm-up previo (no medido): fuerza la carga JIT del modelo para que el tiempo
     del test A1 no incluya la carga (v1 si la incluia -> latencia sesgada a la baja).
  5. Escribe en un fichero NUEVO (bateria_modelos_v2.jsonl). Nunca toca el historico.
  6. Reanudable: salta los modelos ya presentes en el fichero de salida.
  7. Guarda finish_reason, uso de tokens y VRAM (nvidia-smi) por prueba.

Uso:
  # solo listar los pendientes, sin llamar a ningun modelo (lectura pura)
  python3 bateria_modelos_v2.py --dry-run

  # lanzar la bateria completa a los pendientes (reanudable)
  python3 bateria_modelos_v2.py --run-pendientes

  # un modelo concreto
  python3 bateria_modelos_v2.py --model "granite-4.0-h-tiny"
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import date

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from bateria_modelos import PRUEBAS, normalizar_texto  # noqa: E402  (pruebas identicas a v1)

METRICS = os.path.expanduser("~/joko-lab/04-operations/metrics")
HISTORICOS = [os.path.join(METRICS, f) for f in
              ("bateria_modelos.jsonl", "bateria_modelos_gptoss.jsonl")]
SALIDA_DEF = os.path.join(METRICS, "bateria_modelos_v2.jsonl")


def norm_id(m):
    """normaliza ids para comparar (qwen/qwen3-14b == qwen3-14b)."""
    return m.strip().lower().split("/")[-1]


def leidos(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for l in f:
            if l.strip():
                try:
                    out.append(json.loads(l))
                except json.JSONDecodeError:
                    pass
    return out


def ya_probados(salida):
    s = set()
    for p in HISTORICOS + [salida]:
        for d in leidos(p):
            if d.get("model"):
                s.add(norm_id(d["model"]))
    return s


def vram_mib():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used",
                            "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10)
        return int(r.stdout.strip().splitlines()[0])
    except Exception:
        return None


def llamar(endpoint, model, prompt, max_tokens, timeout):
    t0 = time.time()
    r = requests.post(endpoint, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }, timeout=timeout)
    dt = time.time() - t0
    r.raise_for_status()
    data = r.json()
    ch = data["choices"][0]
    msg = ch.get("message", {})
    content = (msg.get("content") or "") + (msg.get("reasoning_content") or "")
    return content.strip(), dt, data.get("usage", {}), ch.get("finish_reason")


def bateria_modelo(model, args):
    resultados, tiempos, tokens_gen, fins = [], {}, 0, []
    if not args.no_warmup:
        try:
            llamar(args.endpoint, model, "ok", 1, args.timeout)
        except Exception as e:
            print(f"  ! warm-up fallo: {type(e).__name__}: {str(e)[:120]}")

    for nombre, (prompt, evaluar, max_tokens) in PRUEBAS.items():
        content = dt = None
        usage, fin = {}, None
        for intento in (1, 2):
            try:
                content, dt, usage, fin = llamar(args.endpoint, model, prompt,
                                                 max_tokens, args.timeout)
                break
            except Exception as e:
                if intento == 2:
                    resultados.append({"prueba": nombre, "pass": False,
                                       "error": f"{type(e).__name__}: {str(e)[:200]}"})
                    print(f"  [ERROR] {nombre}: {type(e).__name__}")
                    content = None
                else:
                    time.sleep(5)
        if content is None:
            continue

        tiempos[nombre] = round(dt, 2)
        tokens_gen += usage.get("completion_tokens", 0) or 0
        fins.append(f"{nombre}:{fin}")

        if nombre == "E1_consistencia":
            try:
                c2, dt2, _, _ = llamar(args.endpoint, model, prompt, max_tokens, args.timeout)
                tiempos["E1_segunda"] = round(dt2, 2)
                n1, n2 = normalizar_texto(content), normalizar_texto(c2)
                eq = n1 == n2 or n1[:40] == n2[:40]
                resultados.append({"prueba": nombre, "pass": bool(eq),
                                   "respuesta1": content[:150], "respuesta2": c2[:150]})
            except Exception as e:
                resultados.append({"prueba": nombre, "pass": False, "error": str(e)[:200]})
        elif evaluar is not None:
            try:
                ok = bool(evaluar(content))
            except Exception as e:
                ok = False
                print(f"  ! evaluador {nombre}: {type(e).__name__}")
            resultados.append({"prueba": nombre, "pass": ok, "respuesta": content[:400]})

        marca = "PASS" if resultados[-1].get("pass") else "FAIL"
        print(f"  [{marca}] {nombre:28} {round(dt,1):>7} s")

    total_s = round(sum(tiempos.values()), 2)
    fila = {
        "fecha": date.today().isoformat(),
        "run": "bateria_v2",
        "model": model,
        "endpoint": args.endpoint,
        "resultados": resultados,
        "puntuacion": sum(1 for r in resultados if r.get("pass")),
        "total": len(PRUEBAS),
        "tiempos_s": tiempos,
        "tiempo_total_s": total_s,
        "tokens_generados": tokens_gen,
        "latencia_tok_s": round(tokens_gen / max(total_s, 0.01), 1),
        "finish_reasons": fins,
        "vram_mib_fin": vram_mib(),
    }
    return fila


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", action="append", default=[])
    p.add_argument("--run-pendientes", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--salida", default=SALIDA_DEF)
    p.add_argument("--endpoint", default="http://localhost:1234/v1/chat/completions")
    p.add_argument("--api-modelos", default="http://localhost:1234/api/v0/models")
    p.add_argument("--timeout", type=int, default=1200)
    p.add_argument("--no-warmup", action="store_true")
    args = p.parse_args()

    probados = ya_probados(args.salida)
    try:
        data = json.loads(requests.get(args.api_modelos, timeout=15).text)["data"]
    except Exception as e:
        print(f"ERROR: no puedo leer la lista de modelos ({e}).")
        print("Comprueba que LM Studio esta abierto y su API Server en :1234.")
        sys.exit(1)

    servidos = [(m["id"], m.get("type", "?"), m.get("state"))
                for m in sorted(data, key=lambda x: x["id"])]
    pendientes = [i for i, t, s in servidos if t != "embeddings" and norm_id(i) not in probados]

    if args.dry_run:
        print(f"=== Modelos servidos por la API ({len(servidos)}) ===")
        for i, t, s in servidos:
            marca = "probado " if norm_id(i) in probados else "PENDIENTE"
            print(f"  [{marca:9}] {i[:58]:58} {t:10} {s}")
        print(f"\n=== PENDIENTES ({len(pendientes)}) ===")
        for i in pendientes:
            print(f"  - {i}")
        print(f"\nSalida: {args.salida}")
        return

    cola = args.model if args.model else (pendientes if args.run_pendientes else [])
    if not cola:
        print("Nada que hacer: usa --dry-run, --run-pendientes o --model <id>.")
        sys.exit(0)

    cola = [m for m in cola if norm_id(m) not in probados]
    print(f"=== Bateria v2 · {len(cola)} modelos · salida {args.salida} ===")
    os.makedirs(os.path.dirname(args.salida), exist_ok=True)

    for k, model in enumerate(cola, 1):
        print(f"\n--- [{k}/{len(cola)}] {model} ---")
        t0 = time.time()
        try:
            fila = bateria_modelo(model, args)
        except Exception as e:
            print(f"  !! modelo abortado: {type(e).__name__}: {str(e)[:200]}")
            continue
        with open(args.salida, "a", encoding="utf-8") as f:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
        print(f"  >>> {fila['puntuacion']}/{fila['total']} | "
              f"{fila['latencia_tok_s']} tok/s | {round(time.time() - t0)} s de reloj | guardado")

    print("\n=== Resumen de esta corrida ===")
    for d in leidos(args.salida):
        print(f"  {d['fecha']}  {d['model'][:46]:46} {d['puntuacion']}/{d['total']}  "
              f"{d.get('latencia_tok_s')} tok/s")


if __name__ == "__main__":
    main()
