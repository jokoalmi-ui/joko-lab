#!/usr/bin/env bash
# docker-admin: Backup de volúmenes de un servicio
# Uso: bash scripts/backup-volumen.sh <servicio>
# Servicios: n8n, ollama, exports
set -uo pipefail

BACKUP_BASE="/mnt/ssd_ia_datos/backups"
COMPOSE_FILE="/home/jokoalmi/automation-stack/docker-compose.yml"

if [ $# -lt 1 ]; then
    echo "Uso: bash scripts/backup-volumen.sh <servicio>"
    echo "Servicios: n8n, ollama, exports"
    exit 1
fi

SERVICE=$1
DATE=$(date +%Y%m%d_%H%M%S)
EXCLUDE=()

case "$SERVICE" in
    n8n)
        SRC="/mnt/ssd_ia_datos/n8n"
        DEST="$BACKUP_BASE/n8n-$DATE"
        ;;
    ollama)
        SRC="/mnt/ssd_ia_datos/ollama"
        DEST="$BACKUP_BASE/ollama-$DATE"
        # Archivos root:root del contenedor no legibles por jokoalmi: se excluyen del rsync
        EXCLUDE=(--exclude='/history' --exclude='/id_ed25519' --exclude='/cache/model-recommendations.json')
        ;;
    exports)
        SRC="/mnt/ssd_ia_datos/exports"
        DEST="$BACKUP_BASE/exports-$DATE"
        ;;
    *)
        echo "Servicio no soportado: $SERVICE"
        echo "Servicios con datos: n8n, ollama, exports"
        exit 1
        ;;
esac

echo "Backup de $SERVICE..."
echo "  Desde: $SRC"
echo "  Hacia: $DEST"
mkdir -p "$DEST"
rsync -av --delete "${EXCLUDE[@]}" "$SRC/" "$DEST/"
RC=$?

if [ $RC -eq 0 ]; then
    echo "✔  Backup de $SERVICE completado: $DEST"
elif [ $RC -eq 23 ]; then
    echo "⚠  Backup de $SERVICE con errores parciales (rsync code 23): algunos archivos no se copiaron"
    echo "    Destino: $DEST"
    exit 0
else
    echo "✗  Error en backup de $SERVICE (rsync code $RC)"
    echo "    Destino: $DEST"
    exit $RC
fi
