#!/bin/bash
# fin.sh — Cierre controlado de sesion de Joko Lab
# 
# ATENCION: Esta version queda como wrapper para compatibilidad.
# La implementacion real esta en:
#   ~/joko-lab/02-infrastructure/fin/fin.sh
#
# Para actualizar el alias, ejecuta:
#   alias fin='~/joko-lab/02-infrastructure/fin/fin.sh'
#
# Uso: fin

NEW_FIN="$HOME/joko-lab/02-infrastructure/fin/fin.sh"

if [ -x "$NEW_FIN" ]; then
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║           FIN — CIERRE DE SESION (joko-lab)                  ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    bash "$NEW_FIN"
else
    echo "ERROR: ~/joko-lab/02-infrastructure/fin/fin.sh no encontrado"
    echo "Usando fallback: checkpoint clasico"
    bash "$HOME/hermes-lab/scripts/checkpoint.sh"
fi
