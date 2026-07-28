#!/bin/bash
# fin — Cierre controlado de sesión de Joko Lab
# 1. Ejecuta checkpoint (punto de recuperación completo)
# 2. Muestra resumen y prepara para cierre
# Uso: fin

set +e

LAB_DIR="$HOME/hermes-lab"
CHECKPOINT="$LAB_DIR/scripts/checkpoint.sh"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                     FIN — CIERRE DE SESIÓN                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ─── 1. Ejecutar checkpoint ────────────────────────────────
if [ -x "$CHECKPOINT" ]; then
    bash "$CHECKPOINT"
    CHECKPOINT_EXIT=$?
else
    echo "  ✗ checkpoint.sh no encontrado en $CHECKPOINT"
    exit 1
fi

# ─── 2. Buscar el último punto de recuperación ─────────────
RECOVERY_DIR="$LAB_DIR/recovery"
LATEST=$(ls -1t "$RECOVERY_DIR" 2>/dev/null | head -1)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SESIÓN LISTA PARA CERRAR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ -n "$LATEST" ]; then
    echo "  Último checkpoint:  $RECOVERY_DIR/$LATEST"
    echo "  Recuperación:       $RECOVERY_DIR/$LATEST/recovery.md"
fi
echo ""
echo "  Escribe Ctrl+C para salir de Hermes."
echo ""
