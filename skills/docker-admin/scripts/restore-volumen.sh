#!/usr/bin/env bash
# docker-admin: Restaurar backup de un servicio
# Uso: bash scripts/restore-volumen.sh <servicio> <fecha>
# Ejemplo: bash scripts/restore-volumen.sh n8n 20260706_153000
set -uo pipefail

BACKUP_BASE="/mnt/ssd_ia_datos/backups"

if [ $# -lt 2 ]; then
    echo "Uso: bash scripts/restore-volumen.sh <servicio> <fecha>"
    echo "  Ejemplo: bash scripts/restore-volumen.sh n8n 20260706_153000"
    echo ""
    echo "Backups disponibles:"
    ls "$BACKUP_BASE/" 2>/dev/null || echo "  No hay backups en $BACKUP_BASE"
    exit 1
fi

SERVICE=$1
DATE=$2
SRC="$BACKUP_BASE/$SERVICE-$DATE"

case "$SERVICE" in
    n8n)
        DEST="/mnt/ssd_ia_datos/n8n"
        ;;
    ollama)
        DEST="/mnt/ssd_ia_datos/ollama"
        ;;
    exports)
        DEST="/mnt/ssd_ia_datos/exports"
        ;;
    *)
        echo "Servicio no soportado: $SERVICE"
        echo "Servicios: n8n, ollama, exports"
        exit 1
        ;;
esac

if [ ! -d "$SRC" ]; then
    echo "No existe el backup: $SRC"
    echo "Backups disponibles para $SERVICE:"
    ls "$BACKUP_BASE/" | grep "^$SERVICE-" || echo "  Ninguno"
    exit 1
fi

echo "⚠️  VAS A RESTAURAR un backup encima del volumen actual."
echo "  Origen:  $SRC"
echo "  Destino: $DEST"
echo "  El contenido actual de $DEST será REEMPLAZADO."
echo ""
echo "Escribe 'yes' para confirmar:"
read -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restauración cancelada."
    exit 1
fi

rsync -av --delete "$SRC/" "$DEST/"
echo "✔  Restauración completada: $SRC → $DEST"
