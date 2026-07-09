#!/usr/bin/env bash
# docker-admin: Healthcheck rápido de todos los servicios del stack
# Uso: bash scripts/healthcheck.sh              (modo interactivo)
#       bash scripts/healthcheck.sh --cron       (modo silencioso para cron, notifica si falla)
set -uo pipefail

COMPOSE_FILE="/home/jokoalmi/automation-stack/docker-compose.yml"
LOG_FILE="/tmp/docker-healthcheck.log"
OK=0
FAIL=0
MODE="${1:-interactive}"

check_port() {
    local service=$1 url=$2 expected=$3
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    if [ "$code" = "$expected" ]; then
        [ "$MODE" = "interactive" ] && echo "  ✔  $service  →  $code (esperado $expected)"
        OK=$((OK + 1))
    else
        [ "$MODE" = "interactive" ] && echo "  ✘  $service  →  $code (esperado $expected)"
        FAIL=$((FAIL + 1))
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL: $service → HTTP $code (esperado $expected)" >> "$LOG_FILE"
    fi
}

if [ "$MODE" = "interactive" ]; then
    echo "╔══════════════════════════════════════╗"
    echo "║  Healthcheck del stack Docker        ║"
    echo "╚══════════════════════════════════════╝"
    echo ""

    echo "── Contenedores ──"
    docker compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null
    echo ""

    echo "── Healthcheck HTTP ──"
fi

check_port "n8n"          "http://localhost:5678/"        "200"
check_port "ollama"       "http://localhost:11434/api/tags" "200"
check_port "stirling-pdf" "http://localhost:8081/"        "200"
check_port "pdf-cleaner"  "http://localhost:8000/"        "404"

if [ "$MODE" = "interactive" ]; then
    echo ""
    echo "── GPU ──"
    if command -v nvidia-smi &>/dev/null; then
        nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null || echo "  nvidia-smi disponible pero no devuelve datos"
    else
        echo "  nvidia-smi no disponible"
    fi
    echo ""

    TOTAL=$((OK + FAIL))
    echo "── Resumen ──"
    echo "  OK:   $OK/$TOTAL"
    echo "  FAIL: $FAIL/$TOTAL"
    echo ""
fi

if [ "$FAIL" -gt 0 ]; then
    [ "$MODE" = "interactive" ] && echo "  ⚠️  Hay servicios que no responden como se espera."
    exit 1
else
    [ "$MODE" = "interactive" ] && echo "  ✔  Todo correcto."
    exit 0
fi
