#!/bin/bash
# fin — Cierre de sesión diario de Joko Lab
# 1. Git commit de los cambios del día
# 2. Informe ejecutivo de cierre
# Uso: ./fin.sh

LAB_DIR="$HOME/hermes-lab"
INFORMES_DIR="$HOME/informes-joko-lab"
FECHA=$(date +%Y-%m-%d)
HORA=$(date +%H:%M)

echo "═══════════════════════════════════════════════════════════════"
echo "  FIN — Cierre de sesión de Joko Lab ($FECHA $HORA)"
echo "═══════════════════════════════════════════════════════════════"

# ─── 1. Git commit ────────────────────────────────────────────────
echo ""
echo "[1/2] Verificando cambios en hermes-lab..."
cd "$LAB_DIR"

if git status --short | grep -q .; then
    # Generar mensaje descriptivo: archivos modificados clave
    MOD=$(git status --short | grep "^[M ]" | wc -l)
    NEW=$(git status --short | grep "^??" | wc -l)
    MSG="sesion $FECHA: $MOD modificados, $NEW nuevos"
    
    # Añadir todo excepto loop-engineering/
    git add -A 2>/dev/null || true
    # Deshacer loop-engineering si se añadió
    git reset HEAD loop-engineering/ 2>/dev/null || true
    
    if git status --short | grep -q .; then
        git commit -m "$MSG" 2>/dev/null && echo "  ✅ Commit hecho: $MSG" || echo "  ℹ️  Sin cambios para commit."
    else
        echo "  ℹ️  Sin cambios nuevos que commitar."
    fi
else
    echo "  ℹ️  Sin cambios nuevos que commitar."
fi

# ─── 2. Informe ejecutivo de cierre ──────────────────────────────
echo ""
echo "[2/2] Generando informe de cierre..."

# Recoger datos del sistema
NVIDIA=$(nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null || echo "N/A")
RAM=$(free -h | grep "^Mem:" | awk '{print $3 " / " $2}')
DOCKER=$(docker compose -f "$HOME/automation-stack/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null || echo "docker compose no disponible")
COMMITS=$(cd "$LAB_DIR" && git log --oneline --after="$FECHA" 2>/dev/null | wc -l)

# Guardar informe
mkdir -p "$INFORMES_DIR"

cat > "$INFORMES_DIR/$FECHA-cierre-joko-lab.txt" << EOF
INFORME DE CIERRE — JOKO LAB
Fecha: $FECHA
Hora: $HORA

RESUMEN DEL DIA

Commits hoy en hermes-lab: $COMMITS

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
