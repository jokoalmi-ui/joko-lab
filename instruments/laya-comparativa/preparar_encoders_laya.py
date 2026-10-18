#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baja a la cache HF los ENCODERS que necesitan los checkpoints de Laya.

  router / typed-decisions -> answerdotai/ModernBERT-large
  multilingual            -> jhu-clsp/mmBERT-base

Motivo: los checkpoints del repo convaiinnovations/laya solo traen las
cabezas (model.safetensors); el encoder lo referencia rl_agent_config.json
y se resuelve contra el Hub en tiempo de carga. Si no esta cacheado, la
medicion dependeria de la red en el momento de ejecutarse.

Solo escribe en la cache estandar (~/.cache/huggingface). No toca el rig.
"""
import json
import os
import sys
import time

from huggingface_hub import snapshot_download

REPOS = ["answerdotai/ModernBERT-large", "jhu-clsp/mmBERT-base"]

AQUI = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(AQUI, "prep_laya_encoders.log")


def log(msg=""):
    linea = str(msg)
    print(linea, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(linea + "\n")


def main():
    log(f"=== ENCODERS: INICIO {time.strftime('%Y-%m-%d %H:%M:%S %Z')} ===")
    fallos = []
    for repo in REPOS:
        t0 = time.time()
        log(f"\n--- {repo} ---")
        try:
            ruta = snapshot_download(repo)
            log(f"OK  {ruta}")
        except Exception as exc:  # noqa: BLE001
            log(f"FALLO {repo}: {type(exc).__name__}: {exc}")
            fallos.append(repo)
            continue
        total = 0
        for raiz, _dirs, ficheros in os.walk(ruta):
            for f in ficheros:
                p = os.path.join(raiz, f)
                if os.path.isfile(p) and not os.path.islink(p):
                    total += os.path.getsize(p)
                elif os.path.islink(p):
                    try:
                        total += os.path.getsize(os.path.realpath(p))
                    except OSError:
                        pass
        log(f"    peso en disco: {total / 1048576:.1f} MB   ({time.time() - t0:.1f} s)")
        ficheros_reales = [f for f in os.listdir(ruta) if not f.startswith(".")]
        log(f"    ficheros: {sorted(ficheros_reales)}")

    log(f"\n=== ENCODERS: FIN {time.strftime('%Y-%m-%d %H:%M:%S %Z')} "
        f"— fallos={len(fallos)} ===")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
