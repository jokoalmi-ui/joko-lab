#!/bin/bash
# apply-decision.sh
# Aplica la decisión del Runtime a Hermes Agent.
# Consume Runtime.resolve() via runtime/api.py.
#
# Ya no llama al DE directamente. El DE es puro (solo decide).
# El Runtime (runtime/api.py) gestiona logs y archivos de estado.
#
# Responsabilidades de este script:
# 1. Llamar a Runtime.resolve() (vía runtime/api.py --json)
# 2. Aplicar el resultado mediante hermes config set
# 3. Informar del resultado

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="/mnt/ssd_ia_datos/lab-state/logs/apply-decision.log"
RUNTIME_API="$PROJECT_ROOT/runtime/api.py"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $*" >> "$LOG_FILE"
}

# Obtener decisión del Runtime
DECISION=$(python3 "$RUNTIME_API" --json 2>/dev/null)

if [ -z "$DECISION" ]; then
    log "ERROR: No se pudo obtener decisión del Runtime"
    exit 1
fi

PROVIDER=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['provider'])")
MODEL=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['model'])")
REASON=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['reason'])")

log "Decisión: $PROVIDER / $MODEL — $REASON"

# Estado actual antes del cambio
OLD_PROVIDER=$(hermes config show 2>/dev/null | grep "provider:" | head -1 | awk '{print $2}')
OLD_MODEL=$(hermes config show 2>/dev/null | grep "default:" | head -1 | awk '{print $2}')

if [ "$OLD_PROVIDER" = "$PROVIDER" ] && [ "$OLD_MODEL" = "$MODEL" ]; then
    log "Sin cambios: ya está en $PROVIDER/$MODEL"
    exit 0
fi

# Aplicar nuevo proveedor y modelo
log "Cambiando: $OLD_PROVIDER/$OLD_MODEL → $PROVIDER/$MODEL"

hermes config set model.provider "$PROVIDER" 2>/dev/null
hermes config set model.default "$MODEL" 2>/dev/null

# Verificar
NEW_PROVIDER=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "provider:" | awk '{print $2}')
NEW_MODEL=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "default:" | awk '{print $2}')

if [ "$NEW_PROVIDER" = "$PROVIDER" ] && [ "$NEW_MODEL" = "$MODEL" ]; then
    log "✅ Cambio aplicado correctamente: $PROVIDER/$MODEL"
else
    log "❌ Fallo al aplicar: esperado $PROVIDER/$MODEL, obtenido $NEW_PROVIDER/$NEW_MODEL"
fi
