#!/usr/bin/env bash
# n8n-admin: Exportar workflows de n8n via API
# Uso: bash export-workflows.sh [--output DIR] [--format json]
set -uo pipefail

N8N_URL="http://localhost:5678"
OUTPUT_DIR="${2:-/mnt/ssd_ia_datos/exports}"
FORMAT="${3:-json}"
DATE=$(date +%Y%m%d_%H%M%S)
EXPORT_DIR="${OUTPUT_DIR}/workflows-export-${DATE}"

# n8n no tiene autenticación configurada (sin N8N_BASIC_AUTH_ACTIVE, sin N8N_ENCRYPTION_KEY visible)
# Se puede acceder a la API REST directamente

echo "=== Exportación de workflows n8n ==="
echo "Fecha: $DATE"
echo "Destino: $EXPORT_DIR"
echo ""

mkdir -p "$EXPORT_DIR"

# Obtener lista de workflows
echo "Obteniendo lista de workflows..."
WORKFLOWS=$(curl -s "${N8N_URL}/rest/workflows" 2>&1)

if echo "$WORKFLOWS" | grep -q "401\|Unauthorized\|error"; then
    echo "✗ Error de autenticación. La API requiere login."
    echo "  Solución: exportar manualmente desde la UI de n8n en http://localhost:5678"
    echo "  Workflow individual → 'Download'"
    exit 1
fi

if echo "$WORKFLOWS" | grep -q "\[\]"; then
    echo "No hay workflows publicados para exportar."
    exit 0
fi

# Extraer IDs de workflows (intento con jq si está disponible)
if command -v jq &>/dev/null; then
    echo "$WORKFLOWS" | jq -c '.data[] | {id: .id, name: .name}' | while read -r wf; do
        ID=$(echo "$wf" | jq -r '.id')
        NAME=$(echo "$wf" | jq -r '.name' | sed 's/[^a-zA-Z0-9_-]/_/g')
        echo "  Exportando: $NAME (ID: $ID)"
        curl -s "${N8N_URL}/rest/workflows/${ID}" > "${EXPORT_DIR}/${NAME}-${ID}.json"
        echo "    → ${EXPORT_DIR}/${NAME}-${ID}.json ($(wc -c < "${EXPORT_DIR}/${NAME}-${ID}.json") bytes)"
    done
else
    echo "jq no disponible. Exportando respuesta completa..."
    echo "$WORKFLOWS" > "${EXPORT_DIR}/workflows-list-${DATE}.json"
    echo "  → ${EXPORT_DIR}/workflows-list-${DATE}.json"
fi

echo ""
echo "✔ Exportación completada: $EXPORT_DIR"
echo "Total: $(find "$EXPORT_DIR" -type f | wc -l) archivos"
