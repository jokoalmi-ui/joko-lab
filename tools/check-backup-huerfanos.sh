#!/usr/bin/env bash
# check-backup-huerfanos.sh — SOLO LECTURA
# Detecta backups ".bak-*" fuera del arbol respaldado (en ~/ home) y
# referencias de backup documentadas que ya no existen en el arbol.
# Regla RULE-008: un backup fuera del arbol no lo cubre ninguna copia
# automatica (backup-joko-lab.sh rsync de joko-lab/, tar de cierre).
#
# Uso: bash check-backup-huerfanos.sh
# Exit: 0 = sin hallazgos | 1 = hay backups fuera del arbol o refs rotas
set +e

HOME_DIR="$HOME"
ARBOL_LAB="/home/jokoalmi/joko-lab"
ARBOL_HERMES="/home/jokoalmi/hermes-lab"
HALLAZGOS=0

echo "=== check-backup-huerfanos (RULE-008) — $(date '+%Y-%m-%d %H:%M') ==="

# 1. Backups sueltos en home (fuera del arbol)
HUERFANOS=$(find "$HOME_DIR" -maxdepth 1 \( -name '.bak-*' -o -name '*.bak-2026*' \) 2>/dev/null)
if [ -n "$HUERFANOS" ]; then
    echo "⚠️  Backups FUERA del arbol respaldado en ~/ (RULE-008):"
    echo "$HUERFANOS" | sed 's/^/    /'
    HALLAZGOS=$((HALLAZGOS + 1))
else
    echo "✓ Sin .bak-* en ~/ (home)"
fi

# 2. Referencias de backup documentadas vs disco (solo las conocidas)
if [ ! -d "$ARBOL_LAB/01-knowledge/objects/.bak-wikilinks-20260802" ]; then
    echo "⚠️  GUIA 6.11 referencia .bak-wikilinks-20260802/ pero no existe en el arbol"
    echo "    (se conserva dentro de joko-lab.BACKUP.20260803-noche.tar.gz)"
    HALLAZGOS=$((HALLAZGOS + 1))
else
    echo "✓ .bak-wikilinks-20260802 presente en 01-knowledge/objects/"
fi

echo ""
if [ "$HALLAZGOS" -gt 0 ]; then
    echo "RESULTADO: $HALLAZGOS hallazgo(s) — revisar (ver RULE-008 y GUIA 6.11)"
    exit 1
else
    echo "RESULTADO: OK — sin backups huerfanos ni referencias rotas"
    exit 0
fi
