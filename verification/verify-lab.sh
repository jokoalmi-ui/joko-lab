#!/bin/bash
# verify-lab.sh — Verificación determinista de capitalización Joko Lab
# Mide si el conocimiento del laboratorio se aplica correctamente.
# Ejecuta las preguntas del banco contra el pipeline completo.
#
# Uso: ./verify-lab.sh

set -e

VERIFY_DIR="$HOME/joko-lab/verification"
MODEL="${1:-granite-4.1-8b}"
ENDPOINT="${2:-http://localhost:1234}"

echo "🔬 Joko Lab — Verificación determinista"
echo "   Modelo: $MODEL"
echo "   Endpoint: $ENDPOINT"
echo ""

cd "$VERIFY_DIR"
source .venv/bin/activate

python3 run_eval.py \
    --model "$MODEL" \
    --endpoint "$ENDPOINT" \
    --use-lab \
    --fail-under 0.25
