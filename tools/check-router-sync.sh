#!/bin/bash
# check-router-sync.sh — Hook formal: consulta el DE y compara con la config real.
# Solo lectura. NO modifica config.yaml (la decisión la toma el usuario o el cron).
# Uso: bash check-router-sync.sh [hint]
set -euo pipefail
HINT="${1:-}"

# 1. Decisión del Runtime (9 campos del contrato)
DECISION=$(python3 /home/jokoalmi/hermes-lab/runtime/api.py --json 2>/dev/null || echo "{}")
DE_PROVIDER=$(echo "$DECISION" | python3 -c "import sys,json; print(json.load(sys.stdin).get('provider','?'))" 2>/dev/null || echo "?")
DE_MODEL=$(echo "$DECISION" | python3 -c "import sys,json; print(json.load(sys.stdin).get('model','?'))" 2>/dev/null || echo "?")

# 2. Config real de Hermes
CFG_PROVIDER=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep provider | awk '{print $2}' | head -1)
CFG_MODEL=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep default | awk '{print $2}' | head -1)

# 3. Comparar
echo "=== SINCRO ROUTER ==="
echo "  DE sugiere:  $DE_PROVIDER / $DE_MODEL"
echo "  Hermes usa:  $CFG_PROVIDER / $CFG_MODEL"

if [ "$DE_PROVIDER" = "$CFG_PROVIDER" ] && [ "$DE_MODEL" = "$CFG_MODEL" ]; then
    echo "  ✅ SINCRONIZADO — el Router y Hermes coinciden"
else
    echo "  ⚠️  DESINCRONIZADO — el Router recomienda distinto de lo que usa Hermes"
    echo ""
    echo "  La sesión actual seguirá con $CFG_PROVIDER/$CFG_MODEL"
    echo "  Para aplicar la recomendación del Router (si la validación pre-pasa):"
    echo "    bash /home/jokoalmi/hermes-lab/decision-engine/apply-decision.sh"
    echo "  O cambiar manualmente en la sesión: /model"
fi
