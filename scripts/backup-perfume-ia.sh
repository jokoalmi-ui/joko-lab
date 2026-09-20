#!/bin/bash
# backup-perfume-ia.sh — Copia diaria de la BD de perfume-ia (Joko Lab)
# Creado 18-sep-2026. Motivo: /home/jokoalmi/perfume-ia/data quedaba FUERA de
# las 4 capas de backup (vive fuera de ~/joko-lab y fuera de ~/.hermes); en disco
# no existia NINGUNA copia automatica, solo .bak manuales sueltos de agosto.
#
# - BDs SQLite con `sqlite3 .backup` (copia coherente; NUNCA cp de BD viva con WAL)
#   y `PRAGMA integrity_check` sobre la copia antes de dar el OK.
# - Resto de data/ con rsync (schema.sql, seed, imports, photos, logs, json),
#   excluyendo .lancedb (regenerable), los *.db (ya copiados arriba),
#   *.bak-* / *.BACKUP.* (copias manuales: copiarlas dentro de la copia
#   diaria multiplicaria el mismo dato) y __pycache__.
# - Cierre: si la copia no existe o queda vacia -> exit 1 (nada de fallo mudo).
# - Rotacion por FECHA DEL NOMBRE, nunca por mtime (leccion de la capa 1:
#   rsync -a hereda el mtime de la fuente y la rotacion por mtime se autodestruye).
#   KEEP=14 (~500 KB/dia) mientras la capa 1 conserva 7: la BD es el dato que no
#   se puede regenerar, asi que se le da el doble de historico por casi cero coste.
# - Se invoca desde backup-joko-lab.sh (22:15, cron "backup-joko-lab-diario"),
#   para no crear un segundo scheduler ni duplicar disparos.
#
# Uso: backup-perfume-ia.sh [--quiet]
# Variables pensadas para pruebas en sandbox: PERFUME_SRC, PERFUME_BASE, PERFUME_KEEP
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

# Rutas LITERALES primero: el auditor tools/auditar_cobertura_backups.py deriva las
# raices cubiertas leyendo lineas `CLAVE="valor"` de los scripts de backup. Con la
# forma ${VAR:-default} no puede leerlas y reportaria un FALSO hueco (medido 18-sep).
# Los overrides por entorno (para pruebas en sandbox) van despues, aparte.
SRC="/home/jokoalmi/perfume-ia/data"
BASE="/mnt/ssd_ia_datos/backups"
KEEP=14
[ -n "${PERFUME_SRC:-}" ] && SRC="$PERFUME_SRC"
[ -n "${PERFUME_BASE:-}" ] && BASE="$PERFUME_BASE"
[ -n "${PERFUME_KEEP:-}" ] && KEEP="$PERFUME_KEEP"
FECHA=$(date +%Y%m%d)
DEST="${BASE}/perfume-ia-${FECHA}"
LOG="/tmp/backup-perfume-ia-${FECHA}.log"

: > "$LOG" 2>/dev/null

if [ ! -d "$SRC" ]; then
    echo "✗ Origen inexistente: $SRC"
    exit 1
fi

mkdir -p "$BASE" || { echo "✗ No se pudo crear el directorio base: $BASE"; exit 1; }
mkdir -p "$DEST" || { echo "✗ No se pudo crear el destino: $DEST"; exit 1; }

$QUIET || echo "=== Backup perfume-ia → ${DEST} ==="

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
    --exclude='.lancedb' \
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

$QUIET || echo "✔ Backup perfume-ia completado: $DEST ($SIZE, $N_FICH ficheros, $OK_DBS BD)"

# --- Rotacion por FECHA DEL NOMBRE. KEEP = total de copias en disco, INCLUIDA
# la de hoy: la lista que se filtra excluye $DEST, asi que hay que conservar
# KEEP-1 de las anteriores (con head -n -KEEP quedaban KEEP+1 en disco: medido
# en sandbox el 18-sep-2026, 17 carpetas -> 15 en vez de 14) ---
ls -1d "$BASE"/perfume-ia-*/ 2>/dev/null \
  | grep -E "^${BASE}/perfume-ia-[0-9]{8}/$" \
  | grep -vxF "${DEST}/" \
  | sort | head -n -"$((KEEP-1))" | xargs -r rm -rf
$QUIET || echo "✔ Rotacion: conservadas las $KEEP copias mas recientes en disco (por fecha del nombre)"
exit 0
