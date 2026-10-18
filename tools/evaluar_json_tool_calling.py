#!/usr/bin/env python3
"""Batería JSON estricto + tool calling para modelos locales (Joko Lab).

Instrumento NUEVO creado 2026-09-14 (no existía batería de este tipo en el lab).
Complementa a evaluar_alucinaciones.py: aquel mide invención/honestidad, este
mide formato (JSON válido sin fugas de markdown) y uso de herramientas.

Uso:
  python3 tools/evaluar_json_tool_calling.py --modelo ibm/granite4.2:8b-q4_K_M --backend ollama
  python3 tools/evaluar_json_tool_calling.py --modelo granite-4.2-8b --backend lmstudio --json
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BATERIA = os.path.join(SCRIPT_DIR, "bateria_json_tool_calling.json")


def post_json(url, payload, timeout=180):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def llamar_ollama(modelo, prompt, tools, host, timeout=180, num_ctx=8192, think=None):
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "stream": False,
               "options": {"temperature": 0.0, "seed": 42, "num_ctx": num_ctx}}
    if think is False:
        payload["think"] = False
    if tools:
        payload["tools"] = tools
    t0 = time.time()
    resp = post_json(host + "/api/chat", payload, timeout)
    return resp, time.time() - t0


def llamar_lmstudio(modelo, prompt, tools, host, timeout=180):
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.0, "seed": 42, "stream": False}
    if tools:
        payload["tools"] = tools
    t0 = time.time()
    resp = post_json(host + "/v1/chat/completions", payload, timeout)
    return resp, time.time() - t0


def extraer_texto(resp, backend):
    if backend == "ollama":
        msg = resp.get("message", {})
        return msg.get("content", "") or "", msg.get("tool_calls") or []
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    return msg.get("content", "") or "", msg.get("tool_calls") or []


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def validar_json(caso, texto):
    fallos = []
    comp = caso["comprueba"]
    plano = texto.strip()
    if comp.get("sin_fences") and "```" in plano:
        fallos.append("contiene fences markdown (```)")
    if comp.get("sin_texto_extra") and not (plano.startswith("{") and plano.endswith("}")):
        fallos.append("texto extra fuera del JSON")
    obj = None
    try:
        obj = json.loads(plano)
    except Exception:
        m = re.search(r"\{.*\}", plano, re.S)
        if m:
            try:
                obj = json.loads(m.group(0))
                fallos.append("JSON embebido en texto, no es la respuesta completa")
            except Exception:
                pass
    if not isinstance(obj, dict):
        fallos.append("no es un objeto JSON parseable")
        return fallos
    for k in comp.get("claves", []):
        if k not in obj:
            fallos.append(f"falta la clave '{k}'")
    for k, esperado in (comp.get("iguales") or {}).items():
        if k not in obj:
            continue
        got = obj[k]
        if isinstance(esperado, (int, float)) and not isinstance(esperado, bool):
            if _num(got) is None or abs(_num(got) - esperado) > 0.01:
                fallos.append(f"{k}: esperado {esperado}, obtenido {got!r}")
        elif got != esperado:
            fallos.append(f"{k}: esperado {esperado!r}, obtenido {got!r}")
    for k, tipo in (comp.get("tipos") or {}).items():
        if k in obj:
            mapa = {"array": list, "object": dict, "string": str, "number": (int, float)}
            exp = mapa.get(tipo)
            if exp and (not isinstance(obj[k], exp) or isinstance(obj[k], bool)):
                fallos.append(f"{k}: tipo esperado {tipo}, obtenido {type(obj[k]).__name__}")
    for k, n in (comp.get("longitud") or {}).items():
        if k in obj and isinstance(obj[k], (list, str)) and len(obj[k]) != n:
            fallos.append(f"{k}: longitud esperada {n}, obtenida {len(obj[k])}")
    for k, regla in (comp.get("valor_en") or {}).items():
        if isinstance(regla, dict):
            permitidos, esperado = regla.get("valores") or regla.get("permitidos") or [], regla.get("esperado")
        else:
            permitidos, esperado = regla, None
        if k in obj and permitidos and obj[k] not in permitidos:
            fallos.append(f"{k}: valor {obj[k]!r} fuera de {permitidos}")
        elif esperado and obj.get(k) != esperado:
            fallos.append(f"{k}: esperado {esperado!r}, obtenido {obj.get(k)!r}")
    for k, tipo in (comp.get("tipo_claves") or {}).items():
        if k in obj and tipo == "string" and not isinstance(obj[k], str):
            fallos.append(f"{k}: se esperaba string")
    return fallos


def validar_tool(caso, tool_calls):
    comp = caso["comprueba"]
    if not tool_calls:
        return ["no devolvió tool_calls (debería llamar a una herramienta)"]
    fallos = []
    tc = tool_calls[0]
    fn = tc.get("function", tc)
    nombre = fn.get("name")
    args = fn.get("arguments")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except Exception:
            fallos.append(f"argumentos no parseables: {args!r}")
            args = {}
    if comp.get("herramienta") and nombre != comp["herramienta"]:
        fallos.append(f"herramienta elegida {nombre!r}, esperada {comp['herramienta']!r}")
    for k, v in (comp.get("args_iguales") or {}).items():
        if str(args.get(k, "")).strip() != v:
            fallos.append(f"arg {k}: esperado {v!r}, obtenido {args.get(k)!r}")
    for k, v in (comp.get("args_contiene") or {}).items():
        if v.lower() not in str(args.get(k, "")).lower():
            fallos.append(f"arg {k}: {v!r} no aparece en {args.get(k)!r}")
    return fallos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bateria", default=DEFAULT_BATERIA)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--backend", choices=["ollama", "lmstudio"], default="ollama")
    ap.add_argument("--host-ollama", default="http://localhost:11434")
    ap.add_argument("--host-lm", default="http://localhost:1234")
    ap.add_argument("--no-think", action="store_true",
                    help="Ollama: desactivar razonamiento largo (think=false)")
    ap.add_argument("--num-ctx", type=int, default=8192,
                    help="contexto a fijar en Ollama (8192 por defecto; con 131072 el modelo pasa a CPU)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    bateria = json.load(open(args.bateria, encoding="utf-8"))
    host = args.host_ollama if args.backend == "ollama" else args.host_lm
    if args.backend == "ollama":
        llamar = lambda m, p, t, h: llamar_ollama(
            m, p, t, h, num_ctx=args.num_ctx, think=False if args.no_think else None)
    else:
        llamar = llamar_lmstudio

    filas, t_total = [], 0.0
    for caso in bateria["casos"]:
        try:
            resp, dt = llamar(args.modelo, caso["prompt"], caso.get("herramientas"), host)
        except urllib.error.URLError as e:
            print(f"ERROR de conexión con {host}: {e}", file=sys.stderr)
            sys.exit(2)
        texto, tcs = extraer_texto(resp, args.backend)
        fallos = validar_tool(caso, tcs) if caso["tipo"] == "tool_calling" else validar_json(caso, texto)
        t_total += dt
        filas.append({"id": caso["id"], "tipo": caso["tipo"], "pasa": not fallos,
                      "fallos": fallos, "segundos": round(dt, 2),
                      "respuesta": (texto or json.dumps(tcs, ensure_ascii=False))[:400]})
        if not args.json:
            marca = "PASA" if not fallos else "FALLA"
            print(f"[{marca}] {caso['id']} ({dt:.1f}s) {caso['tipo']}")
            for f in fallos:
                print(f"    - {f}")
            if fallos:
                print(f"    respuesta: {filas[-1]['respuesta'][:200]!r}")
    pasan = sum(1 for f in filas if f["pasa"])
    resumen = {"modelo": args.modelo, "backend": args.backend,
               "num_ctx": args.num_ctx if args.backend == "ollama" else None,
               "think": (False if args.no_think else None) if args.backend == "ollama" else None,
               "pasan": pasan, "total": len(filas), "segundos_total": round(t_total, 1),
               "casos": filas}
    if args.json:
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
    else:
        print(f"\nRESUMEN {args.modelo} [{args.backend}]: {pasan}/{len(filas)} — {t_total:.1f}s total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
