#!/bin/bash
# backup-hermes-lab.sh — Copia diaria de ~/hermes-lab (Joko Lab, capa 1b)
# Creado 21-sep-2026. Motivo: ~/hermes-lab (803 M: scripts de backup, skills del
# lab, herramientas y su repo git) entraba en las copias SOLO por git; todo lo que
# no estuviera commiteado (y el propio .git) no lo cubria NINGUNA capa. Medido
# antes de escribir este script: 0 copias en disco, 0 ficheros sin commitear.
#
# - rsync -a con --link-dest a la copia anterior (mismo patron que joko-lab):
#   las copias son completas pero los ficheros sin cambios se enlazan, asi que
#   ~800 M iniciales y unos pocos M por dia.
# - SI se copia .git (20 M): asi la copia es autosuficiente (restaurable sin
#   depender del bare del SSD ni de GitHub).
# - Excluye solo regenerables: __pycache__, *.pyc, .venv, venv, node_modules,
#   .lancedb y *.BACKUP.* (para no copiar una copia dentro de la copia).
# - Rotacion por FECHA DEL NOMBRE, nunca por mtime (rsync -a hereda el mtime de
#   la fuente: la rotacion por mtime se autodestruye; bug confirmado 18-sep-2026
#   en la capa de joko-lab). KEEP = total de copias EN DISCO, incluida la de hoy:
#   por eso la lista excluye $DEST y conserva KEEP-1 de las anteriores.
# - Cierre: si la copia no existe, esta vacia o no lleva el fichero esperado ->
#   exit 1 (nada de fallo mudo: el job del cron debe devolver error).
# - Se invoca desde backup-joko-lab.sh (22:15, cron "backup-joko-lab-diario"),
#   para no crear un segundo scheduler.
#
# Uso: backup-hermes-lab.sh [--quiet]
# Variables pensadas para pruebas en sandbox: HERMESLAB_SRC, HERMESLAB_BASE, HERMESLAB_KEEP
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

# Rutas LITERALES primero: el auditor tools/auditar_cobertura_backups.py deriva
# las raices cubiertas leyendo lineas `CLAVE="valor"` de los scripts de backup.
SRC="/home/jokoalmi/hermes-lab"
BASE="/home/jokoalmi"
KEEP=7
[ -n "${HERMESLAB_SRC:-}" ] && SRC="$HERMESLAB_SRC"
[ -n "${HERMESLAB_BASE:-}" ] && BASE="$HERMESLAB_BASE"
[ -n "${HERMESLAB_KEEP:-}" ] && KEEP="$HERMESLAB_KEEP"
FECHA=$(date +%Y%m%d)
DEST="${BASE}/hermes-lab.BACKUP.${FECHA}/"
LOG="/tmp/backup-hermes-lab-${FECHA}.log"

: > "$LOG" 2>/dev/null

if [ ! -d "$SRC" ]; then
    echo "✗ Origen inexistente: $SRC"
    exit 1
fi

# Copia previa mas reciente para --link-dest (por fecha del nombre, nunca $DEST)
PREV=$(ls -1d "${BASE}"/hermes-lab.BACKUP.*/ 2>/dev/null \
  | grep -E "^${BASE}/hermes-lab\\.BACKUP\\.[0-9]{8}/$" \
  | grep -vxF "$DEST" | sort | tail -1)

$QUIET || echo "=== Backup hermes-lab → ${DEST} ==="
if [ -n "$PREV" ]; then
    $QUIET || echo "    Base para hardlinks (--link-dest): $PREV"
    LINK=(--link-dest="$PREV")
else
    LINK=()
fi

mkdir -p "$DEST" || { echo "✗ No se pudo crear el destino: $DEST"; exit 1; }

rsync -a --delete "${LINK[@]}" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='node_modules' \
    --exclude='.lancedb' \
    --exclude='*.BACKUP.*' \
    "$SRC/" "$DEST" > "$LOG" 2>&1
RSYNC_EXIT=$?

# --- Cierre: la copia debe existir, llevar contenido y el fichero esperado ---
if [ ! -d "$DEST" ]; then
    echo "✗ La copia no existe tras rsync: $DEST (log: $LOG)"
    exit 1
fi
N_FICH=$(find "$DEST" -type f 2>/dev/null | wc -l)
if [ "$N_FICH" -eq 0 ]; then
    echo "✗ Copia vacia: $DEST"
    exit 1
fi
if [ ! -s "${DEST}scripts/backup-joko-lab.sh" ]; then
    echo "✗ La copia no lleva el fichero esperado scripts/backup-joko-lab.sh: $DEST"
    exit 1
fi
if [ "$RSYNC_EXIT" -ne 0 ]; then
    echo "✗ rsync devolvio exit $RSYNC_EXIT (log: $LOG)"
    exit 1
fi

SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
[ -n "$PREV" ] && MODO="hardlinks sobre $(basename "$PREV")" || MODO="copia completa"
$QUIET || echo "✔ Backup hermes-lab completado: $DEST ($SIZE, $N_FICH ficheros, $MODO)"

# --- Rotacion por FECHA DEL NOMBRE (KEEP total en disco, incluida la de hoy) ---
ls -1d "${BASE}"/hermes-lab.BACKUP.*/ 2>/dev/null \
  | grep -E "^${BASE}/hermes-lab\\.BACKUP\\.[0-9]{8}/$" \
  | grep -vxF "$DEST" \
  | sort | head -n -"$((KEEP-1))" | xargs -r rm -rf
$QUIET || echo "✔ Rotacion: conservadas las $KEEP copias mas recientes en disco (por fecha del nombre)"
exit 0
