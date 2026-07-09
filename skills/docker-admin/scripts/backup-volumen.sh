#!/usr/bin/env bash
# docker-admin: Backup de volúmenes de un servicio
# Uso: bash scripts/backup-volumen.sh <servicio>
set -uo pipefail

BACKUP_BASE="/mnt/ssd_ia_datos/backups"
COMPOSE_FILE="/home/jokoalmi/automation-stack/docker-compose.yml"

if [ $# -lt 1 ]; then
    echo "Uso: bash scripts/backup-volumen.sh <servicio>"
    echo "Servicios: n8n, ollama"
    exit 1
fi

SERVICE=$1
DATE=$(date +%Y%m%d_%H%M%S)

case "$SERVICE" in
    n8n)
        SRC="/mnt/ssd_ia_datos/n8n"
        DEST="$BACKUP_BASE/n8n-$DATE"
        echo "Backup de n8n..."
        echo "  Desde: $SRC"
        echo "  Hacia: $DEST"
        mkdir -p "$DEST"
        rsync -av --delete "$SRC/" "$DEST/"
        echo "✔  Backup de n8n completado: $DEST"
        ;;
    ollama)
        SRC="/mnt/ssd_ia_datos/ollama"
        DEST="$BACKUP_BASE/ollama-$DATE"
        echo "Backup de ollama..."
        echo "  Desde: $SRC"
        echo "  Hacia: $DEST"
        mkdir -p "$DEST"
        rsync -av --delete "$SRC/" "$DEST/"
        echo "✔  Backup de ollama completado: $DEST"
        ;;
    exports)
        SRC="/mnt/ssd_ia_datos/exports"
        DEST="$BACKUP_BASE/exports-$DATE"
        echo "Backup de exports..."
        echo "  Desde: $SRC"
        echo "  Hacia: $DEST"
        mkdir -p "$DEST"
        rsync -av --delete "$SRC/" "$DEST/"
        echo "✔  Backup de exports completado: $DEST"
        ;;
    *)
        echo "Servicio no soportado: $SERVICE"
        echo "Servicios con datos: n8n, ollama, exports"
        exit 1
        ;;
esac
