#!/usr/bin/env python3
"""F2 · Instrumento C — composición de un request_dump real, por rol y por herramienta.

Solo lectura sobre ~/.hermes/sessions/request_dump_*.json (modo 0600).
NO imprime el header Authorization (contiene la clave de API EN CLARO).

Uso:
    python3 analizar_dumps.py                 # inventario de los 27 dumps
    python3 analizar_dumps.py <ruta_dump>     # composición detallada de uno
"""
import collections
import glob
import json
import os
import sys

DUMPS = "/home/jokoalmi/.hermes/sessions/request_dump_*.json"


def inventario():
    dumps = sorted(glob.glob(DUMPS))
    print(f"dumps: {len(dumps)}")
    dentro = 0
    for p in dumps:
        d = json.load(open(p))
        ts = d.get("timestamp", "")
        body = d["request"]["body"]
        msgs = body.get("messages", [])
        tools = body.get("tools", [])
        mb = len(json.dumps(msgs, ensure_ascii=False))
        tb = len(json.dumps(tools, ensure_ascii=False))
        host = d["request"]["url"].split("/")[2]
        inled = "LEDGER" if ts >= "2026-08-06" else "  -   "
        dentro += inled.strip() == "LEDGER"
        print(f"{ts[:19]} {inled} {host:>32} msgs={len(msgs):>5} ({mb:>8} B) "
              f"tools={len(tools):>3} ({tb:>6} B) reason={d.get('reason')} "
              f"err={(d.get('error') or {}).get('type')}")
    print(f"dentro del rango del ledger: {dentro}/{len(dumps)}")


def composicion(ruta):
    d = json.load(open(ruta))
    assert "Authorization" in d["request"]["headers"], "no parece un request_dump"
    msgs = d["request"]["body"]["messages"]
    tot = len(json.dumps(msgs, ensure_ascii=False))
    print(f"dump: {os.path.basename(ruta)}")
    print(f"timestamp: {d.get('timestamp')} | host: {d['request']['url'].split('/')[2]}")
    print(f"total messages JSON = {tot} B ({len(msgs)} mensajes)")

    by = collections.defaultdict(lambda: [0, 0])
    for m in msgs:
        r = m.get("role")
        by[r][0] += 1
        by[r][1] += len(json.dumps(m, ensure_ascii=False))
    for r, (n, b) in sorted(by.items(), key=lambda x: -x[1][1]):
        print(f"  {r:>10}: {n:>4} msgs {b:>9} B {100*b/tot:5.1f}%")

    # salidas de tool: en el dump el mensaje tool NO lleva 'name' -> se empareja por orden
    # con el tool_calls emitido por el assistant inmediatamente anterior.
    pendientes = []
    salidas = collections.Counter()
    llamadas = collections.Counter()
    for m in msgs:
        for t in (m.get("tool_calls") or []):
            fn = (t.get("function") or {}).get("name", "?")
            pendientes.append(fn)
            llamadas[fn] += 1
        if m.get("role") == "tool":
            nombre = m.get("name") or (pendientes.pop(0) if pendientes else "?")
            salidas[nombre] += len(json.dumps(m, ensure_ascii=False))
    print("  --- salidas de tool (bytes) ---")
    for nme, b in salidas.most_common(15):
        print(f"    {nme:>20}: {b:>9} B  ({llamadas.get(nme, 0)} llamadas)")
    comp = [m for m in msgs
            if isinstance(m.get("content"), str) and m["content"].startswith("[CONTEXT COMPACTION")]
    print(f"  compactaciones: {len(comp)} -> {sum(len(m['content']) for m in comp)} B")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        composicion(sys.argv[1])
    else:
        inventario()
