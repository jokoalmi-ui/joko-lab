#!/usr/bin/env python3
"""Batería JSON estricto + tool calling — CORRECTOR v2 (Joko Lab, 2026-09-25).

Por qué existe el v2 (fichero NUEVO; el v1 no se toca):
  1. El v1 solo puntúa la PRIMERA llamada (`tc = tool_calls[0]`): no puede
     comprobar que el modelo emita DOS tool_calls en un mismo turno (caso E).
  2. El v1 da por fallo la ausencia de `tool_calls`, así que no puede puntuar el
     caso en que NO hay ninguna herramienta útil y lo correcto es no llamar (caso F).
  3. FALLO DE INSTRUMENTO corregido aquí: `llamar_ollama` del v1 solo añade la
     clave `think` al payload cuando vale exactamente `False`; `low`/`medium`/
     `high`/`True` NUNCA llegaban al modelo. En el v2 `think` se transmite tal
     cual viene, y se registra `think_payload` para que no pueda repetirse en
     silencio.
  4. Registra por llamada: `thinking_chars` (discriminador directo de si el
     modelo razona), `n_tool_calls` y `nombres`, para no volver a confundir
     razonamiento con nivel.

VE el vocabulario JSON del v1 tal cual: importa su módulo congelado (sha256
verificado) y usa SU `validar_json` y SU `post_json`. Si el v1 cambia, ABORTA.

Uso:
  python3 tools/evaluar_json_tool_calling_v2.py --bateria <banco.json> \
      --modelo ibm/granite4.2:8b-q4_K_M --think omit|false|true|low|medium|high --json
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_V1 = os.path.join(SCRIPT_DIR, "evaluar_json_tool_calling.py")
SHA_V1 = "849c12fe093420bae89971566e190653c5ca50d3322b7e404e144d9f012e6121"

NIVELES = {"omit": None, "false": False, "true": True, "low": "low", "medium": "medium", "high": "high"}


def cargar_v1():
    """Importa el corrector v1 congelado (vocabulario JSON de referencia)."""
    with open(RUTA_V1, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    if h != SHA_V1:
        raise SystemExit(f"[ABORT] El corrector v1 ha cambiado (sha {h[:16]}… != {SHA_V1[:16]}…). "
                         f"El vocabulario JSON del v2 debe seguir siendo el suyo.")
    spec = importlib.util.spec_from_file_location("jtc_v1", RUTA_V1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V1 = cargar_v1()
validar_json = V1.validar_json      # vocabulario JSON idéntico al v1
post_json = V1.post_json


def payload_think(think):
    """Lo que viaja DE VERDAD en el payload (evita el fallo del v1)."""
    return "<AUSENTE>" if think is None else think


def llamar_ollama(modelo, prompt, tools, host, timeout=180, num_ctx=8192, think=None):
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "stream": False,
               "options": {"temperature": 0.0, "seed": 42, "num_ctx": num_ctx}}
    if think is not None:           # <<< el arreglo: se transmite tal cual
        payload["think"] = think
    if tools:
        payload["tools"] = tools
    t0 = time.time()
    resp = post_json(host + "/api/chat", payload, timeout)
    return resp, time.time() - t0


def llamar_lmstudio(modelo, prompt, tools, host, timeout=180, num_ctx=None, think=None):
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.0, "seed": 42, "stream": False}
    if tools:
        payload["tools"] = tools
    t0 = time.time()
    resp = post_json(host + "/v1/chat/completions", payload, timeout)
    return resp, time.time() - t0


def extraer(resp, backend):
    """Devuelve (texto, tool_calls, thinking) — el v1 no exponía el thinking."""
    if backend == "ollama":
        msg = resp.get("message", {}) or {}
    else:
        msg = ((resp.get("choices") or [{}])[0] or {}).get("message", {}) or {}
    return (msg.get("content") or "", msg.get("tool_calls") or [], msg.get("thinking") or "")


def nombres_args(tool_calls):
    """[(nombre, args_dict), ...] tolerando argumentos como texto JSON."""
    out = []
    for tc in tool_calls or []:
        fn = tc.get("function", tc)
        args = fn.get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {"__raw__": args}
        out.append((fn.get("name"), args if isinstance(args, dict) else {}))
    return out


def validar_tool_v2(caso, tool_calls):
    """Sustituye a validar_tool del v1: N llamadas, orden, y ausencia correcta."""
    comp = caso["comprueba"]
    pares = nombres_args(tool_calls)
    nombres = [n for n, _ in pares]
    fallos = []

    if comp.get("sin_tool_calls"):
        if pares:
            fallos.append(f"devolvió {len(pares)} tool_calls sin herramienta útil: {nombres}")
        return fallos

    if not pares:
        pedido = comp.get("secuencia_herramientas") or comp.get("herramienta")
        return [f"no devolvió tool_calls (esperaba {pedido})"]

    seq = comp.get("secuencia_herramientas")
    if seq:
        i = 0
        for n in nombres:
            if i < len(seq) and n == seq[i]:
                i += 1
        if i < len(seq):
            fallos.append(f"secuencia incompleta: esperaba {seq}, obtuvo {nombres} (faltan {seq[i:]})")
        sobrantes = [n for n in nombres if n not in seq]
        if sobrantes:
            fallos.append(f"herramienta(s) no pedida(s): {sobrantes}")
        if comp.get("exactamente_n") and len(pares) != comp["exactamente_n"]:
            fallos.append(f"nº de llamadas esperado {comp['exactamente_n']}, obtenido {len(pares)}")

    if comp.get("herramienta"):
        if comp["herramienta"] not in nombres:
            fallos.append(f"herramienta elegida {nombres}, esperada {comp['herramienta']!r}")
        else:
            args = pares[nombres.index(comp["herramienta"])][1]
            for k, v in (comp.get("args_iguales") or {}).items():
                if str(args.get(k, "")).strip() != v:
                    fallos.append(f"arg {k}: esperado {v!r}, obtenido {args.get(k)!r}")
            for k, v in (comp.get("args_contiene") or {}).items():
                if v.lower() not in str(args.get(k, "")).lower():
                    fallos.append(f"arg {k}: {v!r} no aparece en {args.get(k)!r}")
    return fallos


def puntuar(caso, texto, tool_calls):
    if caso["tipo"] == "tool_calling":
        return validar_tool_v2(caso, tool_calls)
    return validar_json(caso, texto)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bateria", required=True, help="banco de casos (JSON con 'casos')")
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--backend", choices=["ollama", "lmstudio"], default="ollama")
    ap.add_argument("--host-ollama", default="http://localhost:11434")
    ap.add_argument("--host-lm", default="http://localhost:1234")
    ap.add_argument("--think", choices=sorted(NIVELES), default="omit",
                    help="valor que se envía en 'think' (por defecto 'omit' = no enviar la clave)")
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--solo-casos", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    think_val = NIVELES[args.think]

    bateria = json.load(open(args.bateria, encoding="utf-8"))
    casos = bateria["casos"]
    if args.solo_casos:
        ids = {x.strip() for x in args.solo_casos.split(",")}
        casos = [c for c in casos if c["id"] in ids]
    host = args.host_ollama if args.backend == "ollama" else args.host_lm
    llamar = llamar_ollama if args.backend == "ollama" else llamar_lmstudio

    filas, t_total = [], 0.0
    for caso in casos:
        try:
            resp, dt = llamar(args.modelo, caso["prompt"], caso.get("herramientas"), host,
                              num_ctx=args.num_ctx, think=think_val)
        except urllib.error.URLError as e:
            print(f"ERROR de conexión con {host}: {e}", file=sys.stderr)
            sys.exit(2)
        texto, tcs, think_txt = extraer(resp, args.backend)
        fallos = puntuar(caso, texto, tcs)
        pares = nombres_args(tcs)
        t_total += dt
        fila = {"id": caso["id"], "tipo": caso["tipo"], "pasa": not fallos, "fallos": fallos,
                "segundos": round(dt, 2), "think_pedido": args.think,
                "think_payload": payload_think(think_val), "thinking_chars": len(think_txt),
                "n_tool_calls": len(pares), "nombres": [n for n, _ in pares],
                "args": [a for _, a in pares],
                "respuesta": (texto or json.dumps(tcs, ensure_ascii=False))[:400]}
        filas.append(fila)
        if not args.json:
            marca = "PASA" if not fallos else "FALLA"
            print(f"[{marca}] {caso['id']} ({dt:.1f}s) {caso['tipo']} calls={fila['n_tool_calls']} "
                  f"thinking={fila['thinking_chars']}ch")
            for f in fallos:
                print(f"    - {f}")

    pasan = sum(1 for f in filas if f["pasa"])
    resumen = {"corrector": "v2", "modelo": args.modelo, "backend": args.backend,
               "bateria": os.path.abspath(args.bateria),
               "sha_bateria": hashlib.sha256(open(args.bateria, "rb").read()).hexdigest(),
               "think_pedido": args.think, "think_payload": payload_think(think_val),
               "num_ctx": args.num_ctx if args.backend == "ollama" else None,
               "pasan": pasan, "total": len(filas), "segundos_total": round(t_total, 1),
               "casos": filas}
    if args.json:
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
    else:
        media = t_total / len(filas) if filas else 0.0
        print(f"\nRESUMEN v2 {args.modelo}: {pasan}/{len(filas)} — {t_total:.1f}s total "
              f"({media:.1f}s/llamada) — think payload={payload_think(think_val)!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
