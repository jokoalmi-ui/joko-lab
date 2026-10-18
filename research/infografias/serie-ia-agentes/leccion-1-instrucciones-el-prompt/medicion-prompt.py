#!/usr/bin/env python3
"""Medicion de la Leccion 1 (serie IA y agentes): el formato exigido en la instruccion.

Misma tanda de resenas a un modelo local, temperatura 0, dos condiciones:
  A) "Clasifica estas resenas" sin mas                -> se espera texto libre
  B) la misma peticion + formato JSON exigido         -> se espera JSON parseable
  C) control de temperatura: B con temperatura alta, para ver si el formato aguanta

Metrica: % de salidas parseables con json.loads (crudo y tras quitar vallas markdown).
Guarda JSON crudo con las respuestas LITERALES, fecha y modelo.

Uso:
  python3 medicion-prompt.py --modelo ibm/granite4.2:8b-q4_K_M --backend ollama --json
  python3 medicion-prompt.py --modelo granite-4.2-8b --backend lmstudio
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

RESENAS = [
    "Pedido llegado en dos dias y bien embalado.",
    "El producto vino rayado y nadie contesta al correo.",
    "Funciona como se describe, repetire.",
    "Me cobraron dos veces y sigo esperando el reembolso.",
    "Buena relacion calidad precio, aunque tardo una semana.",
    "El manual esta en un idioma que no entiendo.",
]

PETICION_A = ("Clasifica estas resenas como POSITIVA o NEGATIVA.\n\n"
              + "\n".join(f"{i+1}. {r}" for i, r in enumerate(RESENAS)))

PETICION_B = (PETICION_A + "\n\nResponde SOLO con JSON valido: una lista de objetos con las "
              "claves \"id\" (numero) y \"sentimiento\" (\"positiva\" o \"negativa\"). "
              "Sin texto antes ni despues.")


def post_json(url, payload, timeout=300):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def llamar(backend, host, modelo, prompt, temperature):
    if backend == "ollama":
        payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
                   "stream": False,
                   "options": {"temperature": temperature, "seed": 42, "num_ctx": 8192}}
        t0 = time.time()
        resp = post_json(host + "/api/chat", payload)
        return (resp.get("message", {}).get("content") or ""), time.time() - t0
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "temperature": temperature, "seed": 42, "stream": False}
    t0 = time.time()
    resp = post_json(host + "/v1/chat/completions", payload)
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    return (msg.get("content") or ""), time.time() - t0


def quitar_vallas(txt):
    t = txt.strip()
    t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def parseable(txt):
    """(crudo_ok, tras_quitar_vallas_ok)"""
    crudo = False
    limpio = False
    try:
        json.loads(txt)
        crudo = True
    except Exception:
        pass
    try:
        json.loads(quitar_vallas(txt))
        limpio = True
    except Exception:
        pass
    return crudo, limpio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--backend", choices=["ollama", "lmstudio"], default="ollama")
    ap.add_argument("--host", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()

    host = args.host or ("http://127.0.0.1:11434" if args.backend == "ollama" else "http://127.0.0.1:1234")
    condiciones = [("A_sin_formato", PETICION_A, 0.0), ("B_formato", PETICION_B, 0.0),
                   ("C_formato_temp_alta", PETICION_B, 0.8)]
    filas = []
    for nombre, prompt, temp in condiciones:
        try:
            texto, seg = llamar(args.backend, host, args.modelo, prompt, temp)
            crudo, limpio = parseable(texto)
            fila = {"condicion": nombre, "temperature": temp, "segundos": round(seg, 1),
                    "json_valido_crudo": crudo, "json_valido_sin_vallas": limpio,
                    "chars": len(texto), "respuesta_literal": texto}
        except urllib.error.URLError as e:
            fila = {"condicion": nombre, "temperature": temp, "error": str(e)}
        filas.append(fila)
        print(f"{nombre}: json_crudo={fila.get('json_valido_crudo')} "
              f"json_sin_vallas={fila.get('json_valido_sin_vallas')} "
              f"{fila.get('segundos', '')}s chars={fila.get('chars', '')}")

    n = len([f for f in filas if "respuesta_literal" in f])
    ok = len([f for f in filas if f.get("json_valido_sin_vallas")])
    salida = {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
              "modelo": args.modelo, "backend": args.backend, "host": host,
              "num_resenas": len(RESENAS), "condiciones_ejecutadas": n,
              "parseables": ok, "filas": filas}
    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, ensure_ascii=False, indent=2)
        print("escrito:", args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
