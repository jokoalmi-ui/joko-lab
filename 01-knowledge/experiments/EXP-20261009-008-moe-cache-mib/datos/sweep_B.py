#!/usr/bin/env python3
"""EXP-20261009-008 - Fase B (ronda 2 intercalada + prosa + control CPU puro).

Diseño: pares intercalados C=1024 / C=0 para separar la deriva temporal del
efecto del flag; repeticion de C=512 (la celda contaminada de la fase A);
clase E2 (prosa) en 0 y 1024; y control de direccion conocida con -ngl 0.
"""
import json, subprocess, time

PY = "/usr/bin/python3"
RC = "/tmp/exp008/run_cell.py"
E1 = "/tmp/exp008/prompt-E1-estructurada.txt"
E2 = "/tmp/exp008/prompt-E2-prosa.txt"
BASE = ["--ncmoe", "28", "--ngl", "99", "--ctx", "2048", "--ubatch", "128"]

CELLS = [
    ("E1_C1024_R2", 1024, E1, 128, 99),
    ("E1_C0000_R2", 0, E1, 128, 99),
    ("E1_C0512_R2", 512, E1, 128, 99),
    ("E1_C1024_R2b", 1024, E1, 128, 99),
    ("E1_C0000_R2b", 0, E1, 128, 99),
    ("E2_C0000", 0, E2, 128, 99),
    ("E2_C1024", 1024, E2, 128, 99),
    ("CTL_ngl0_CPU", 0, E1, 16, 0),
]


def log(m):
    with open("/tmp/exp008/sweep_B.log", "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%F %T')} {m}\n"); fh.flush()


def cells():
    try:
        return [json.loads(l) for l in open("/tmp/exp008/cells.jsonl", encoding="utf-8") if l.strip()]
    except Exception:
        return []


log("=== sweep B inicio ===")
done = {c["label"] for c in cells()}
for label, c, prompt, npred, ngl in CELLS:
    if label in done:
        log(f"SKIP {label}"); continue
    cmd = [PY, RC, "--label", label, "--moe-cache-mib", str(c),
           "--npredict", str(npred), "--ngl", str(ngl), "--prompt", prompt]
    if ngl > 0:
        cmd += BASE
    t0 = time.time()
    log(f"START {label} (C={c} ngl={ngl} npred={npred})")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=1500)
        out = [l for l in (p.stdout or "").strip().splitlines() if l.strip()]
        last = out[-1] if out else ("ERR:" + (p.stderr or "")[-200:])
    except subprocess.TimeoutExpired:
        last = '{"error":"timeout 1500s"}'
    log(f"END {label} ok={'\"healthy\": true' in last} {int(time.time()-t0)}s {last[:200]}")
    time.sleep(5)
log("=== sweep B fin ===")
