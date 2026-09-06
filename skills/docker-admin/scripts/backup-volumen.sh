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

# Política ollama (decidido 05-sep-2026): backup SOLO los domingos.
# Los models pesan ~22G y son re-descargables; un backup diario satura el SSD.
if [ "$SERVICE" = "ollama" ] && [ "$(date +%u)" != "7" ]; then
    echo "Omitido: backup de ollama solo los domingos (hoy: $(date +%A))."
    exit 0
fi

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
else
    echo "✗  Error en backup de $SERVICE (rsync code $RC)"
    echo "    Destino: $DEST"
    exit $RC
fi

# Rotación: conservar solo los $KEEP backups MÁS RECIENTES de este servicio.
# Los nombres usan YYYYMMDD_HHMMSS → orden alfabético = orden cronológico.
KEEP=7
[ "$SERVICE" = "ollama" ] && KEEP=3   # ollama es semanal (domingos): 3 copias = ~3 semanas
ANTIGUOS=$(ls -1d "$BACKUP_BASE/${SERVICE}-"* 2>/dev/null | sort | head -n -${KEEP})
if [ -n "$ANTIGUOS" ]; then
    echo "Rotación de $SERVICE: eliminando $(echo "$ANTIGUOS" | wc -l) backup(s) antiguo(s), conservando los $KEEP más recientes"
    echo "$ANTIGUOS" | while IFS= read -r d; do
        echo "  rm -rf $d"
        rm -rf "$d"
    done
fi
exit 0
