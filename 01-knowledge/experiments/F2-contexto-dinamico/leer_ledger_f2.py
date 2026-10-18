#!/usr/bin/env python3
"""F2 · Instrumento D — distribución de prompt_tokens del ledger del pipeline.

Solo lectura. El ledger NO tiene campo de sesión ni de cliente: esto es una
DISTRIBUCIÓN de referencia, nunca un patrón oro (skill skill-compaction §5).
Las sondas del proxy (<1.000 tok) se separan a propósito.

Uso: python3 leer_ledger_f2.py [--umbral-sonda 1000]
"""
import argparse
import json
import statistics
import sys

LEDGER = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--umbral-sonda", type=int, default=1000,
                    help="por debajo de esto la fila se considera sonda del proxy")
    ap.add_argument("--ruta", default=LEDGER)
    args = ap.parse_args()

    filas, validas, sondas, ts = [], [], 0, []
    with open(args.ruta) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            filas.append(r)
            if r.get("timestamp"):
                ts.append(r["timestamp"])
            pt = r.get("prompt_tokens")
            if not isinstance(pt, (int, float)):
                continue
            if pt < args.umbral_sonda:
                sondas += 1
                continue
            validas.append(pt)

    validas.sort()
    print(f"filas: {len(filas)} | con prompt_tokens y >= {args.umbral_sonda} tok: {len(validas)}")
    print(f"sondas del proxy descartadas (< {args.umbral_sonda}): {sondas}")
    if ts:
        print(f"rango: {min(ts)} -> {max(ts)}")
    if validas:
        n = len(validas)
        print(f"min {validas[0]} | p50 {statistics.median(validas):.0f} | "
              f"p90 {validas[int(n*0.9)-1]} | max {validas[-1]} | "
              f"media {statistics.mean(validas):.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
