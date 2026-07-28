#!/usr/bin/env bash
# cloud-backup.sh — Backup cifrado de configs criticas a Google Drive
# Sube lo IRREMPLAZABLE que pesa KB (no modelos de GB):
#   - Decisiones (04-operations/decisions/)
#   - Patrones (01-knowledge/patterns/)
#   - Fichas de modelo (01-knowledge/models/)
#   - Docs (docs/)
#   - Procedimientos de recovery (02-infrastructure/recovery/procedures/)
#   - Contract de inferencia (05-inference/contract.md)
#
# Uso: ./cloud-backup.sh

set +e

JOKO_LAB="$HOME/joko-lab"
BUNDLE="/tmp/joko-lab-critical-$(date +%Y%m%d_%H%M).tar.gz"
REMOTE="gdrive:hermes-lab-backups/critical/"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CLOUD BACKUP — Configuracion critica ($TIMESTAMP)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar rclone
if ! command -v rclone >/dev/null 2>&1; then
    echo "ERROR: rclone no instalado"
    exit 1
fi

# Crear bundle con lo critico (solo texto, pesa KB)
tar -czf "$BUNDLE" \
    -C "$JOKO_LAB" \
    04-operations/decisions/ \
    01-knowledge/patterns/ \
    01-knowledge/models/ \
    01-knowledge/anti-patterns.md \
    02-infrastructure/recovery/procedures/ \
    02-infrastructure/inicio/protocolo.md \
    02-infrastructure/fin/protocolo.md \
    05-inference/contract.md \
    docs/ \
    README.md \
    2>/dev/null

if [ ! -f "$BUNDLE" ]; then
    echo "ERROR: No se pudo crear el bundle"
    exit 1
fi

SIZE=$(du -h "$BUNDLE" | cut -f1)

# Verificar integridad
echo -n "  Verificando bundle... "
if tar -tzf "$BUNDLE" >/dev/null 2>&1; then
    FILES=$(tar -tzf "$BUNDLE" | wc -l)
    echo "OK ($FILES archivos)"
else
    echo "CORRUPTO"
    rm -f "$BUNDLE"
    exit 1
fi

# Subir a Google Drive
echo -n "  Subiendo a Google Drive... "
rclone copy "$BUNDLE" "$REMOTE" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "OK ($SIZE)"
else
    echo "FALLIDO"
    rm -f "$BUNDLE"
    exit 1
fi

# Limpiar
rm -f "$BUNDLE"

echo ""
echo "  Backup completado: $FILES archivos, $SIZE"
echo "  Destino: $REMOTE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CLOUD BACKUP COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
exit 0
