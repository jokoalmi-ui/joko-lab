#!/bin/bash
# Render ficha F1 — "IA, ML y DL: qué es cada uno" (serie La IA que yo uso)
# Uso: bash render_f1.sh
cd /home/jokoalmi/joko-lab/research/linkedin-lab
python3 generar_carrusel_linkedin.py \
  --guion salidas/2026-09-01-ia-ml-dl-que-es-cada-uno/guion.json \
  --outdir salidas/2026-09-01-ia-ml-dl-que-es-cada-uno
