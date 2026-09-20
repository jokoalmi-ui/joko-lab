#!/bin/bash
# backup-cafe-ia.sh — Copia diaria de la BD de cafe-ia (Joko Lab)
# Creado 20-sep-2026. Motivo: /home/jokoalmi/cafe-ia/data quedaba FUERA de la
# cadena de backups (vive fuera de ~/joko-lab, ~/.hermes y ~/perfume-ia) y su
# unico respaldo era cafes.db.bak-20260813 DENTRO del mismo directorio, asi que
# un fallo del disco se llevaba original y copia a la vez. Detectado por
# tools/auditar_cobertura_backups.py (pendiente desde el informe del 14-sep).
#
# Patron clonado de backup-perfume-ia.sh (validado 18-sep-2026):
# - BD SQLite con `sqlite3 .backup` (copia coherente; NUNCA cp de BD viva con WAL)
#   y `PRAGMA integrity_check` sobre la copia antes de dar el OK.
# - Resto de data/ con rsync, excluyendo los *.db (ya copiados arriba) y las
#   copias manuales (*.bak-*), que multiplicarian el mismo dato.
# - Cierre: si la copia no existe o queda vacia -> exit 1 (nada de fallo mudo).
# - Rotacion por FECHA DEL NOMBRE, nunca por mtime (rsync -a hereda el mtime de
#   la fuente y la rotacion por mtime se autodestruye).
# - Se invoca desde backup-joko-lab.sh (22:15, cron "backup-joko-lab-diario"),
#   para no crear un segundo scheduler ni duplicar disparos.
#
# Uso: backup-cafe-ia.sh [--quiet]
# Variables pensadas para pruebas en sandbox: CAFE_SRC, CAFE_BASE, CAFE_KEEP
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

# Rutas LITERALES primero: el auditor tools/auditar_cobertura_backups.py deriva las
# raices cubiertas leyendo lineas `CLAVE="valor"` de los scripts de backup. Con la
# forma ${VAR:-default} no puede leerlas y reportaria un FALSO hueco (medido 18-sep).
# Los overrides por entorno (para pruebas en sandbox) van despues, aparte.
SRC="/home/jokoalmi/cafe-ia/data"
BASE="/mnt/ssd_ia_datos/backups"
KEEP=14
[ -n "${CAFE_SRC:-}" ] && SRC="$CAFE_SRC"
[ -n "${CAFE_BASE:-}" ] && BASE="$CAFE_BASE"
[ -n "${CAFE_KEEP:-}" ] && KEEP="$CAFE_KEEP"
FECHA=$(date +%Y%m%d)
DEST="${BASE}/cafe-ia-${FECHA}"
LOG="/tmp/backup-cafe-ia-${FECHA}.log"

: > "$LOG" 2>/dev/null

if [ ! -d "$SRC" ]; then
    echo "✗ Origen inexistente: $SRC"
    exit 1
fi

mkdir -p "$BASE" || { echo "✗ No se pudo crear el directorio base: $BASE"; exit 1; }
mkdir -p "$DEST" || { echo "✗ No se pudo crear el destino: $DEST"; exit 1; }

$QUIET || echo "=== Backup cafe-ia → ${DEST} ==="

# --- BDs SQLite: copia coherente + verificacion de integridad ---
OK_DBS=0
while IFS= read -r -d '' db; do
    n=$(basename "$db")
    if sqlite3 "$db" ".backup '$DEST/$n'" >>"$LOG" 2>&1; then
        INTEG=$(sqlite3 "$DEST/$n" 'PRAGMA integrity_check;' 2>>"$LOG")
        if [ "$INTEG" = "ok" ] && [ -s "$DEST/$n" ]; then
            OK_DBS=$((OK_DBS+1))
            $QUIET || echo "    ✔ BD copiada y verificada: $n ($(du -h "$DEST/$n" 2>/dev/null | cut -f1))"
        else
            echo "✗ Copia de $n corrupta o vacia (integrity_check: ${INTEG:-sin salida})"
            exit 1
        fi
    else
        echo "✗ Fallo copiando $n (log: $LOG)"
        exit 1
    fi
done < <(find "$SRC" -maxdepth 1 -type f -name '*.db' -print0 | sort -z)

if [ "$OK_DBS" -eq 0 ]; then
    echo "✗ No se copio NINGUNA BD (*.db) desde $SRC"
    exit 1
fi

# --- Resto de ficheros (sin BDs, sin copias manuales) ---
rsync -a --delete \
    --exclude='*.db' \
    --exclude='*.db-wal' \
    --exclude='*.db-shm' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.bak-*' \
    --exclude='*.BACKUP.*' \
    --exclude='*.backup-*' \
    "$SRC/" "$DEST/" >>"$LOG" 2>&1
RSYNC_EXIT=$?

# --- Cierre: la copia debe existir y llevar contenido ---
if [ ! -d "$DEST" ]; then
    echo "✗ La copia no existe tras la ejecucion: $DEST"
    exit 1
fi
N_FICH=$(find "$DEST" -type f 2>/dev/null | wc -l)
if [ "$N_FICH" -eq 0 ]; then
    echo "✗ Copia vacia: $DEST"
    exit 1
fi
SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)

if [ "$RSYNC_EXIT" -ne 0 ]; then
    echo "✗ rsync devolvio exit $RSYNC_EXIT (log: $LOG)"
    exit 1
fi

$QUIET || echo "✔ Backup cafe-ia completado: $DEST ($SIZE, $N_FICH ficheros, $OK_DBS BD)"

# --- Rotacion por FECHA DEL NOMBRE. KEEP = total de copias en disco, INCLUIDA
# la de hoy: la lista que se filtra excluye $DEST, asi que hay que conservar
# KEEP-1 de las anteriores (con head -n -KEEP quedaban KEEP+1 en disco: medido
# en sandbox el 18-sep-2026) ---
ls -1d "$BASE"/cafe-ia-*/ 2>/dev/null \
  | grep -E "^${BASE}/cafe-ia-[0-9]{8}/$" \
  | grep -vxF "${DEST}/" \
  | sort | head -n -"$((KEEP-1))" | xargs -r rm -rf
$QUIET || echo "✔ Rotacion: conservadas las $KEEP copias mas recientes en disco (por fecha del nombre)"
exit 0
