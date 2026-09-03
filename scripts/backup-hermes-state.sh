#!/usr/bin/env bash
# backup-hermes-state.sh — Backup diario del estado critico de ~/.hermes
# Cubre el hueco detectado 03-sep-2026: NADIE respaldaba ~/.hermes entre
# actualizaciones (los pre-update de `hermes update` eran lo unico).
# Contenido: config.yaml, memories/, skills/, scripts/, cron/jobs.json
#            + state.db con copia CONSISTENTE (sqlite .backup, seguro con WAL).
# Destino: /mnt/ssd_ia_datos/backups-hermes/ (disco distinto al de ~ — protege
#          contra fallo del disco de sistema). Rotacion: 7 dias.
# Cron: backup-hermes-diario (22:20, no_agent) → wrapper ~/.hermes/scripts/.
# Rutas ABSOLUTAS: el cron corre con PATH limpio (pitfall hermes-cron-jobs 9).
# Creado 03-sep-2026 tras el incidente de corrupcion de state.db (v0.21.0).

set -uo pipefail

HERMES="$HOME/.hermes"
DEST="/mnt/ssd_ia_datos/backups-hermes"
STAMP="$(/usr/bin/date +%Y%m%d-%H%M)"
TMPDIR="/tmp/hermes-state-backup-$STAMP"
OUT="$DEST/hermes-state-$STAMP.tar.gz"
KEEP=7

mkdir -p "$DEST" "$TMPDIR/.hermes/cron" || exit 1

# 1. Copia consistente de state.db (sqlite .backup — NUNCA cp de BD viva en WAL)
/usr/bin/sqlite3 "$HERMES/state.db" ".backup '$TMPDIR/.hermes/state.db'" 2>/dev/null
if [ ! -s "$TMPDIR/.hermes/state.db" ]; then
    echo "ERROR: sqlite .backup de state.db fallo"
    /usr/bin/rm -rf "$TMPDIR"
    exit 1
fi

# 2. Estado critico (config, memorias, skills, scripts, jobs de cron)
/usr/bin/cp "$HERMES/config.yaml" "$TMPDIR/.hermes/" 2>/dev/null || true
/usr/bin/cp -r "$HERMES/memories" "$TMPDIR/.hermes/" 2>/dev/null || true
/usr/bin/cp -r "$HERMES/skills" "$TMPDIR/.hermes/" 2>/dev/null || true
/usr/bin/cp -r "$HERMES/scripts" "$TMPDIR/.hermes/" 2>/dev/null || true
/usr/bin/cp "$HERMES/cron/jobs.json" "$TMPDIR/.hermes/cron/" 2>/dev/null || true

# 3. Empaquetar (gzip; si tardara demasiado para el timeout del cron, ver
#    cron.script_timeout_seconds en config.yaml — configurable globalmente)
/usr/bin/tar czf "$OUT" -C "$TMPDIR" .hermes 2>/dev/null
CODE=$?
/usr/bin/rm -rf "$TMPDIR"
if [ $CODE -ne 0 ] || [ ! -s "$OUT" ]; then
    echo "ERROR: tar fallo (code $CODE)"
    exit 1
fi

# 4. Verificar integridad del tar
FILES=$(/usr/bin/tar tzf "$OUT" 2>/dev/null | /usr/bin/wc -l)
if ! /usr/bin/tar tzf "$OUT" .hermes/config.yaml >/dev/null 2>&1; then
    echo "ERROR: verificacion de integridad fallo"
    exit 1
fi
if ! /usr/bin/tar tzf "$OUT" .hermes/state.db >/dev/null 2>&1; then
    echo "ERROR: state.db no esta dentro del backup"
    exit 1
fi

# 5. Rotacion: conservar los ultimos K dias
/usr/bin/find "$DEST" -maxdepth 1 -name "hermes-state-*.tar.gz" -mtime +"$KEEP" -delete 2>/dev/null

SIZE=$(/usr/bin/du -h "$OUT" | /usr/bin/cut -f1)
echo "OK: $OUT ($SIZE, $FILES archivos). Rotacion conserva $KEEP dias."
exit 0
