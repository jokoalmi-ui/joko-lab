#!/bin/bash
# fin — Cierre de sesión diario de Joko Lab
# 1. Git commit de los cambios del día (no bloquea el informe si falla)
# 2. Informe ejecutivo de cierre
# Uso: ./fin.sh

LAB_DIR="$HOME/hermes-lab"
INFORMES_DIR="$HOME/informes-joko-lab"
FECHA=$(date +%Y-%m-%d)
HORA=$(date +%H:%M)

echo "═══════════════════════════════════════════════════════════════"
echo "  FIN — Cierre de sesion de Joko Lab ($FECHA $HORA)"
echo "═══════════════════════════════════════════════════════════════"

# ─── 1. Git commit (no critico — no bloquea el informe) ────────
echo ""
echo "[1/2] Verificando cambios en hermes-lab..."

# Desactivar set -e para que un fallo aqui no mate el script
set +e
(
    cd "$LAB_DIR" || exit 1

    if ! git status --short | grep -q .; then
        echo "  ℹ️  Sin cambios nuevos que commitar."
        exit 0
    fi

    git add -A 2>/dev/null
    # Deshacer loop-engineering si se anadio
    git reset HEAD -- loop-engineering/ 2>/dev/null

    if ! git status --short | grep -q .; then
        echo "  ℹ️  Sin cambios para commit (solo loop-engineering)."
        exit 0
    fi

    MSG="sesion $FECHA"
    if git commit -m "$MSG" 2>/dev/null; then
        echo "  ✅ Commit hecho: $MSG"
    else
        echo "  ℹ️  No se pudo hacer commit."
    fi
)
set -e

# ─── 2. Informe ejecutivo de cierre (siempre se ejecuta) ────────
echo ""
echo "[2/2] Generando informe de cierre..."

# Recoger datos del sistema
NVIDIA=$(nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null || echo "N/A")
RAM=$(free -h | grep "^Mem:" | awk '{print $3 " / "$2}')
DOCKER=$(docker compose -f "$HOME/automation-stack/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null || echo "docker compose no disponible")
COMMITS=$(cd "$LAB_DIR" 2>/dev/null && git log --oneline --after="$FECHA" 2>/dev/null | wc -l || echo "0")

# CPU load
LOAD=$(uptime | awk -F'load average:' '{print $2}' | xargs)

# Guardar informe
mkdir -p "$INFORMES_DIR"

cat > "$INFORMES_DIR/$FECHA-cierre-joko-lab.txt" << EOF
INFORME DE CIERRE — JOKO LAB
Fecha: $FECHA
Hora: $HORA

RESUMEN DEL DIA
Commits hoy en hermes-lab: $COMMITS
Load del sistema: $LOAD

HARDWARE
  GPU: $NVIDIA
  RAM: $RAM

STACK DOCKER
$DOCKER

PENDIENTES ABIERTOS
- Loop Engineering: pendiente de evaluar
- LM Studio + monitor Flask: probados, parados a proposito
- Eliminar acoplamiento apply-decision.sh a config.yaml
- docs/joko-lab-principles.md: vacio
- Skills betterbird, perfumes: sin poblar
EOF

echo "  ✅ Informe guardado: $INFORMES_DIR/$FECHA-cierre-joko-lab.txt"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Sesion cerrada. Nos vemos."
echo "═══════════════════════════════════════════════════════════════"
