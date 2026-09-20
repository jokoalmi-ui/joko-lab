#!/bin/bash
# backup-joko-lab.sh — Backup TOTAL automatizado de joko-lab
# Creado 2-ago-2026 (analisis exhaustivo, mejora M: el backup de joko-lab
# era manual y fin.sh solo hace commit de hermes-lab, NO de joko-lab).
#
# - Copia completa con rsync (incremental entre ejecuciones)
# - Excluye .venv, __pycache__, .lancedb y .git (regenerables/versionables)
#   → backup de ~500M en vez de 1.5G
# - Rotacion: conserva los ultimos 7 backups
# - Destino: /home/jokoalmi/joko-lab.BACKUP.<YYYYMMDD>/
#
# Uso: ./backup-joko-lab.sh [--quiet]
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

SRC="/home/jokoalmi/joko-lab/"
FECHA=$(date +%Y%m%d)
DEST="/home/jokoalmi/joko-lab.BACKUP.${FECHA}/"
LOG="/tmp/backup-joko-lab-${FECHA}.log"

# Copia previa mas reciente, para --link-dest (misma fecha del nombre, nunca
# $DEST). Si no existe, se copia todo desde cero (sin hardlinks).
PREV=$(ls -1d /home/jokoalmi/joko-lab.BACKUP.*/ 2>/dev/null \
  | grep -E '^/home/jokoalmi/joko-lab\.BACKUP\.[0-9]{8}/$' \
  | grep -vxF "$DEST" | sort | tail -1)

$QUIET || echo "=== Backup joko-lab → ${DEST} ==="
if [ -n "$PREV" ]; then
    $QUIET || echo "    Base para hardlinks (--link-dest): $PREV"
    LINK=(--link-dest="$PREV")
else
    LINK=()
fi

# Copia completa con exclusiones
# --delete-excluded: elimina del destino lo que esta excluido (ej: .venv
# que quedo en un backup manual previo). Verificado 2-ago-2026: sin esta
# flag, rsync copia pero NO limpia lo excluido ya presente en el destino.
# --link-dest (18-sep-2026): el registro de sesiones del lab
# (04-operations/metrics/sesiones/*.jsonl) ocupa 9,7G y el consolidador
# re-exporta el historico completo cada noche; sin hardlinks, 7 copias
# diarias serian ~77G sobre 95G libres. Con --link-dest las copias siguen
# siendo completas pero los ficheros sin cambios se enlazan: ~11G + ~0,6G
# por dia. rsync escribe temp+rename (no --inplace), asi que nunca modifica
# el inodo compartido con la copia anterior.
rsync -a --delete --delete-excluded "${LINK[@]}" \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.lancedb' \
    --exclude='.git' \
    --exclude='.BACKUP' \
    --exclude='*.BACKUP.*' \
    --exclude='~/tmp' \
    "$SRC" "$DEST" > "$LOG" 2>&1
RSYNC_EXIT=$?

# Chequeo de existencia (18-sep-2026): el job NO debe devolver ok si la copia
# no ha quedado en disco. El 17-sep (y la noche anterior) el cron devolvio ok
# con 0 copias, porque solo se miraba el exit de rsync.
if [ ! -d "$DEST" ]; then
    echo "✗ El backup no existe tras rsync: $DEST (log: $LOG)"
    exit 1
fi

# Tamano resultante
SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
[ -n "$PREV" ] && MODO="hardlinks sobre $(basename "$PREV")" || MODO="copia completa"

if [ $RSYNC_EXIT -eq 0 ]; then
    $QUIET || echo "✔ Backup completado: $DEST ($SIZE)"
    # Rotacion por FECHA DEL NOMBRE (no por mtime). Motivo (bug confirmado
    # 18-sep-2026: 0 copias de joko-lab en disco): rsync -a hereda al directorio
    # destino el mtime de la raiz de joko-lab, asi que si esa raiz lleva >7 dias
    # sin cambios el antiguo 'find -mtime +7' borraba en la misma pasada el
    # backup recien escrito. Se conservan los 7 mas recientes y $DEST nunca
    # entra en la lista. Sin coincidencias -> no borra nada (xargs -r).
    ls -1d /home/jokoalmi/joko-lab.BACKUP.*/ 2>/dev/null \
      | grep -E '^/home/jokoalmi/joko-lab\.BACKUP\.[0-9]{8}/$' \
      | grep -vxF "$DEST" \
      | sort | head -n -7 | xargs -r rm -rf
    $QUIET || echo "✔ Rotacion: conservados los 7 backups mas recientes (por fecha del nombre)"

    # --- Capa de perfume-ia (18-sep-2026) ---
    # La BD de perfume-ia (/home/jokoalmi/perfume-ia/data) vive fuera de
    # ~/joko-lab y fuera de ~/.hermes: ninguna de las 4 capas la cubria y no
    # existia copia automatica. Se llama desde aqui para NO crear un segundo
    # scheduler. Un fallo de perfume-ia no deshace el backup ya hecho de
    # joko-lab, pero SI hace que el job del cron devuelva error (no mas fallos
    # silenciosos). Detalle del script: backup-perfume-ia.sh
    PERF_ARGS=()
    $QUIET && PERF_ARGS+=(--quiet)
    if ! bash /home/jokoalmi/hermes-lab/scripts/backup-perfume-ia.sh "${PERF_ARGS[@]}"; then
        echo "✗ Backup de perfume-ia FALLO (log: /tmp/backup-perfume-ia-$(date +%Y%m%d).log)"
        exit 1
    fi

    # --- Capa de cafe-ia (20-sep-2026) ---
    # La BD de cafe-ia (/home/jokoalmi/cafe-ia/data/cafes.db) vivia fuera de las
    # capas 1, 1b, 2 y perfume-ia, y su unico respaldo era un .bak dentro del
    # MISMO directorio (un fallo del disco se llevaba original y copia a la vez).
    # Detectado por tools/auditar_cobertura_backups.py (informe 14-sep-2026).
    # Mismo patron que perfume-ia: se llama desde aqui para NO crear un segundo
    # scheduler. Un fallo de cafe-ia no deshace el backup ya hecho de joko-lab,
    # pero SI hace que el job del cron devuelva error (no mas fallos silenciosos).
    # Detalle del script: backup-cafe-ia.sh
    CAFE_ARGS=()
    $QUIET && CAFE_ARGS+=(--quiet)
    if ! bash /home/jokoalmi/hermes-lab/scripts/backup-cafe-ia.sh "${CAFE_ARGS[@]}"; then
        echo "✗ Backup de cafe-ia FALLO (log: /tmp/backup-cafe-ia-$(date +%Y%m%d).log)"
        exit 1
    fi
    exit 0
else
    echo "✗ Error en rsync (exit $RSYNC_EXIT). Log: $LOG"
    exit 1
fi
