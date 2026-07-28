#!/bin/bash
# fin — Cierre de sesión de Joko Lab
# 1. Smoke test rápido de servicios
# 2. Backup rápido de n8n y ollama (si no se ha hecho hoy)
# 3. Git commit de cambios del día
# 4. Informe ejecutivo de cierre con datos reales
# Uso: fin

set +e

LAB_DIR="$HOME/hermes-lab"
INFORMES_DIR="$HOME/informes-joko-lab"
STACK="$HOME/automation-stack"
FECHA=$(date +%Y-%m-%d)
HORA=$(date +%H:%M)
HOY=$(date +%Y%m%d)

echo "═══════════════════════════════════════════════════════════════"
echo "  FIN — Cierre de sesión de Joko Lab ($FECHA $HORA)"
echo "═══════════════════════════════════════════════════════════════"

# ─── 1. Smoke test ────────────────────────────────────────────
echo ""
echo "[1/4] Smoke test de servicios..."

SMOKE_OUTPUT=$(bash "$LAB_DIR/scripts/smoke-test.sh" --quiet 2>&1)
PASS_COUNT=$(echo "$SMOKE_OUTPUT" | grep -c "PASS")
FAIL_COUNT=$(echo "$SMOKE_OUTPUT" | grep -c "FAIL")
echo "$SMOKE_OUTPUT" | while IFS= read -r line; do echo "  $line"; done

# ─── 2. Backup rápido (solo si no hay backup de hoy) ──────────
echo ""
echo "[2/4] Backup de volúmenes..."

BACKUP_SCRIPT="$LAB_DIR/skills/docker-admin/scripts/backup-volumen.sh"
BACKUP_DIR="/mnt/ssd_ia_datos/backups"

for VOL in n8n ollama; do
    if ls "$BACKUP_DIR/$VOL-$HOY"* >/dev/null 2>&1; then
        echo "  ℹ️  Backup $VOL: ya existe de hoy, saltando."
    elif [ -x "$BACKUP_SCRIPT" ]; then
        echo "  🔄 Ejecutando backup de $VOL..."
        bash "$BACKUP_SCRIPT" "$VOL" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "  ✅ Backup $VOL completado."
        else
            echo "  ⚠️  Backup $VOL falló."
        fi
    else
        echo "  ⚠️  Script de backup no encontrado."
    fi
done

# ─── 3. Git commit ────────────────────────────────────────────
echo ""
echo "[3/4] Verificando cambios en hermes-lab..."

(
    cd "$LAB_DIR" || exit 1

    if ! git status --short 2>/dev/null | grep -q .; then
        echo "  ℹ️  Sin cambios nuevos que commitar."
        exit 0
    fi

    git add -A 2>/dev/null
    git reset HEAD -- loop-engineering/ 2>/dev/null

    if ! git status --short 2>/dev/null | grep -q .; then
        echo "  ℹ️  Sin cambios para commit (solo loop-engineering)."
        exit 0
    fi

    MSG="sesion $FECHA"
    if git commit -m "$MSG" 2>/dev/null; then
        echo "  ✅ Commit hecho: $MSG"
    else
        echo "  ℹ️  No se pudo hacer commit (posiblemente sin cambios)."
    fi
)

# ─── 4. Informe de cierre ─────────────────────────────────────
echo ""
echo "[4/4] Generando informe de cierre..."

# Datos reales del sistema
NVIDIA=$(nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null || echo "N/A")
RAM=$(free -h 2>/dev/null | grep "^Mem:" | awk '{print $3 " / "$2}' || echo "N/A")
DISCO_ROOT=$(df -h / 2>/dev/null | awk 'NR==2 {print $3 " / "$2 " ("$5")"}' || echo "N/A")
DISCO_SSD=$(df -h /mnt/ssd_ia_datos 2>/dev/null | awk 'NR==2 {print $3 " / "$2 " ("$5")"}' || echo "N/A")
LOAD=$(uptime 2>/dev/null | awk -F'load average:' '{print $2}' | xargs || echo "N/A")
COMMITS=$(cd "$LAB_DIR" 2>/dev/null && git log --oneline --after="$FECHA" 2>/dev/null | wc -l || echo "0")

# Docker stack
DOCKER_PS=$(docker compose -f "$STACK/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null || echo "docker compose no disponible")

# Modelos Ollama
OLLAMA_MODELS=$(docker compose -f "$STACK/docker-compose.yml" exec ollama ollama list 2>/dev/null | tail -n +2 | awk '{print $1}' | tr '\n' ', ' | sed 's/,$//')

# Pendientes
PENDIENTES=""
if [ -f "$LAB_DIR/docs/pendientes.txt" ]; then
    PENDIENTES=$(grep -v '^#' "$LAB_DIR/docs/pendientes.txt" | grep -v '^$' || echo "(sin pendientes registrados)")
else
    PENDIENTES="(archivo de pendientes no encontrado)"
fi

# Backup de hoy
BKP_N8N=$(ls "$BACKUP_DIR/n8n-$HOY"* 2>/dev/null | head -1 | xargs -I{} basename {} || echo "no")
BKP_OLLAMA=$(ls "$BACKUP_DIR/ollama-$HOY"* 2>/dev/null | head -1 | xargs -I{} basename {} || echo "no")

mkdir -p "$INFORMES_DIR"

cat > "$INFORMES_DIR/$FECHA-cierre-joko-lab.txt" << EOF
INFORME DE CIERRE — JOKO LAB
=============================
Fecha: $FECHA
Hora: $HORA

SMOKE TEST
  PASS: $PASS_COUNT  FAIL: $FAIL_COUNT
  $SMOKE_OUTPUT

HARDWARE
  GPU:    $NVIDIA
  RAM:    $RAM
  Disco /: $DISCO_ROOT
  Disco SSD: $DISCO_SSD
  Load:   $LOAD

STACK DOCKER
$DOCKER_PS

OLLAMA
  Modelos: $OLLAMA_MODELS

BACKUPS DE HOY
  n8n:    $BKP_N8N
  ollama: $BKP_OLLAMA

COMMITS HOY EN HERMES-LAB
  Total: $COMMITS

PENDIENTES ABIERTOS
$PENDIENTES
EOF

echo "  ✅ Informe guardado: $INFORMES_DIR/$FECHA-cierre-joko-lab.txt"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Sesión cerrada. Nos vemos, Joseba."
echo "═══════════════════════════════════════════════════════════════"
