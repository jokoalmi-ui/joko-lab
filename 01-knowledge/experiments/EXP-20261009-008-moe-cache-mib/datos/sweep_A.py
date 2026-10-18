#!/usr/bin/env python3
"""EXP-20261009-008 - Fase A: barrido de --moe-cache-mib en la clase E1
(estructurada) + linea base E2 (prosa). Secuencial, un parametro por celda.
Escribe progreso en /tmp/exp008/sweep_A.log y celdas en cells.jsonl.
"""
import json, subprocess, sys, time

PY = "/usr/bin/python3"
RC = "/tmp/exp008/run_cell.py"
E1 = "/tmp/exp008/prompt-E1-estructurada.txt"
E2 = "/tmp/exp008/prompt-E2-prosa.txt"
BASE = ["--ncmoe", "28", "--ngl", "99", "--ctx", "2048", "--ubatch", "128"]

CELLS = [
    ("E1_C0000", 0, E1),
    ("E1_C0256", 256, E1),
    ("E1_C0512", 512, E1),
    ("E1_C1024", 1024, E1),
    ("E1_C2048", 2048, E1),
    ("E2_C0000", 0, E2),
]


def log(msg):
    with open("/tmp/exp008/sweep_A.log", "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%F %T')} {msg}\n")
        fh.flush()


def cells():
    try:
        with open("/tmp/exp008/cells.jsonl", encoding="utf-8") as fh:
            return [json.loads(l) for l in fh if l.strip()]
    except Exception:
        return []


log("=== sweep A inicio ===")
done = {c["label"] for c in cells()}
for label, c, prompt in CELLS:
    if label in done:
        log(f"SKIP {label} (ya existe)")
        continue
    cmd = [PY, RC, "--label", label, "--moe-cache-mib", str(c),
           "--npredict", "128", "--prompt", prompt] + BASE
    t0 = time.time()
    log(f"START {label} (C={c})")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        out = (p.stdout or "").strip().splitlines()
        last = out[-1] if out else ""
    except subprocess.TimeoutExpired:
        last = '{"error":"timeout 900s"}'
    ok = '"healthy": true' in last
    log(f"END {label} ok={ok} {int(time.time()-t0)}s {last[:260]}")
    if not ok and prompt == E1 and c > 0:
        log("OOM/fallo en la escalera -> corto la escalada de C (segun diseno)")
        break
    time.sleep(5)
log("=== sweep A fin ===")
