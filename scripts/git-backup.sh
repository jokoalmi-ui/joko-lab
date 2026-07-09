#!/usr/bin/env bash
# git-backup.sh — Backup del repositorio Joko Lab a Google Drive via rclone
# Genera un bundle git (.bundle) y lo sube a gdrive:hermes-lab-backups/
# Uso: ./git-backup.sh [--quiet]
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

LAB_DIR="/home/jokoalmi/hermes-lab"
BUNDLE="/tmp/hermes-lab-bundle-$(date +%Y%m%d).bundle"
REMOTE="gdrive:hermes-lab-backups/"

cd "$LAB_DIR" || exit 1

# Crear bundle del repo completo (todas las ramas y tags)
git bundle create "$BUNDLE" --all 2>/dev/null
SIZE=$(du -h "$BUNDLE" | cut -f1)

# Subir a Google Drive
rclone copy "$BUNDLE" "$REMOTE" 2>/dev/null
RCLONE_EXIT=$?

# Limpiar
rm -f "$BUNDLE"

if [[ $RCLONE_EXIT -eq 0 ]]; then
    $QUIET || echo "✔ Backup subido a Google Drive ($SIZE)"
    exit 0
else
    echo "✗ Error al subir backup (exit code: $RCLONE_EXIT)"
    exit 1
fi
