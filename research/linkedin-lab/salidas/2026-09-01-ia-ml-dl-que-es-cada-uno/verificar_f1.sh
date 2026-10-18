#!/bin/bash
# Verificación visual de la ficha F1 — "IA, ML y DL: qué es cada uno"
# Usa GLM local (glm-4.6v-flash) con el script validado de la skill infografia-html.
# Uso: bash verificar_f1.sh
GLM=/home/jokoalmi/.hermes/skills/creative/infografia-html/scripts/glm_vision.py
DIR=/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-01-ia-ml-dl-que-es-cada-uno

CHECK="Verifica esta slide de carrusel LinkedIn (1080x1350). Checklist: 1) fondo crema claro correcto 2) titulo visible y sin cortes 3) logo JL y marca Joko Lab visibles arriba 4) grafico central o listas visibles y sin solapamientos 5) sin texto cortado ni desbordado 6) pie de slide visible. Responde SOLO si/no por punto, sin razonar."

for i in 01 02 03 04 05 06; do
  echo "===== slide-$i ====="
  python3 "$GLM" "$DIR/slide-$i.png" "$CHECK"
  echo ""
done
