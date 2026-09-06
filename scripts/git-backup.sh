#!/usr/bin/env bash
# git-backup.sh — Backup del repositorio Joko Lab a Google Drive via rclone
# Genera un bundle git (.bundle) y lo sube a gdrive:hermes-lab-backups/
# Uso: ./git-backup.sh [--quiet]
#
# v2 (03-sep-2026): los fallos registran TIMESTAMP + error real de rclone
# (antes: 2>/dev/null ocultaba el motivo; sin fecha no se podía diagnosticar
#  qué días falló — ver bundles perdidos 27-30 ago 2026).
# Contrato watchdog preservado: con --quiet, en EXITO no escribe nada.
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

LAB_DIR="/home/jokoalmi/hermes-lab"
BUNDLE="/tmp/hermes-lab-bundle-$(date +%Y%m%d).bundle"
REMOTE="gdrive:hermes-lab-backups/"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

cd "$LAB_DIR" || exit 1

# Crear bundle del repo completo (todas las ramas y tags)
BUNDLE_ERR=$(git bundle create "$BUNDLE" --all 2>&1)
GIT_EXIT=$?
if [[ $GIT_EXIT -ne 0 ]]; then
    echo "[$TS] ✗ Error creando bundle (exit code: $GIT_EXIT)"
    echo "[$TS] detalle: $(echo "$BUNDLE_ERR" | head -5 | tr '\n' ' ')"
    exit 1
fi
SIZE=$(du -h "$BUNDLE" | cut -f1)

# Subir a Google Drive (capturar stderr para diagnosticar fallos reales)
RCLONE_ERR=$(rclone copy "$BUNDLE" "$REMOTE" 2>&1)
RCLONE_EXIT=$?

# Limpiar
rm -f "$BUNDLE"

if [[ $RCLONE_EXIT -eq 0 ]]; then
    $QUIET || echo "✔ Backup subido a Google Drive ($SIZE)"
    exit 0
else
    echo "[$TS] ✗ Error al subir backup (exit code: $RCLONE_EXIT)"
    echo "[$TS] detalle: $(echo "$RCLONE_ERR" | head -5 | tr '\n' ' ')"
    exit 1
fi
