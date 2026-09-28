#!/usr/bin/env bash
# git-backup.sh — Backup de los repos git del Joko Lab a Google Drive via rclone
# Genera un bundle git (.bundle) por repo y lo sube a gdrive:hermes-lab-backups/
# Uso: ./git-backup.sh [--quiet]
#
# v2 (03-sep-2026): los fallos registran TIMESTAMP + error real de rclone
# (antes: 2>/dev/null ocultaba el motivo; sin fecha no se podía diagnosticar
#  qué días falló — ver bundles perdidos 27-30 ago 2026).
#
# v3 (24-sep-2026): SEGUNDO REPO — joko-lab. joko-lab pasó a ser repo git el
# 24-sep-2026 y su .git entra ahora en la capa 1 (22:46, rsync); antes de esto
# su historial no lo cubría ninguna capa. Se añade aquí para tenerlo TAMBIÉN
# fuera del PC (una caída del disco se llevaría el repo y su copia local).
# Contrato watchdog preservado: con --quiet, en EXITO no escribe nada; si
# falla CUALQUIERA de los dos repos, imprime el error real y sale != 0.
set +e

QUIET=false
[[ "$1" == "--quiet" ]] && QUIET=true

REMOTE="gdrive:hermes-lab-backups/"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
FECHA="$(date +%Y%m%d)"

# backup_repo <ruta-repo> <nombre>: bundle completo (todas las ramas y tags) + subida
backup_repo() {
    local DIR="$1"
    local NOMBRE="$2"
    local BUNDLE="/tmp/${NOMBRE}-bundle-${FECHA}.bundle"
    local ERR RC SIZE

    ERR=$(git -C "$DIR" bundle create "$BUNDLE" --all 2>&1)
    RC=$?
    if [[ $RC -ne 0 ]]; then
        echo "[$TS] ✗ Error creando bundle de $NOMBRE ($DIR, exit $RC)"
        echo "[$TS] detalle: $(echo "$ERR" | head -5 | tr '\n' ' ')"
        return 1
    fi
    SIZE=$(du -h "$BUNDLE" | cut -f1)

    ERR=$(rclone copy "$BUNDLE" "$REMOTE" 2>&1)
    RC=$?
    rm -f "$BUNDLE"

    if [[ $RC -ne 0 ]]; then
        echo "[$TS] ✗ Error al subir backup de $NOMBRE (exit code: $RC)"
        echo "[$TS] detalle: $(echo "$ERR" | head -5 | tr '\n' ' ')"
        return 1
    fi
    $QUIET || echo "✔ $NOMBRE → Google Drive ($SIZE)"
    return 0
}

backup_repo "/home/jokoalmi/hermes-lab" "hermes-lab"
HL=$?
backup_repo "/home/jokoalmi/joko-lab" "joko-lab"
JL=$?

if [[ $HL -eq 0 && $JL -eq 0 ]]; then
    exit 0
fi
exit 1
