#!/usr/bin/env bash
# n8n-admin: Healthcheck específico para n8n
# Uso: bash healthcheck-n8n.sh              (modo interactivo)
#       bash healthcheck-n8n.sh --quiet     (modo silencioso, solo salida simple, exit 0/1)
set -uo pipefail

N8N_URL="http://localhost:5678"
COMPOSE_FILE="/home/jokoalmi/automation-stack/docker-compose.yml"
OK=0
FAIL=0
MODE="${1:-interactive}"

if [ "$MODE" = "interactive" ]; then
    echo "╔══════════════════════════════════════╗"
    echo "║  Healthcheck n8n                     ║"
    echo "╚══════════════════════════════════════╝"
    echo ""
fi

# 1. Estado del contenedor
if [ "$MODE" = "interactive" ]; then echo "── Contenedor ──"; fi
STATUS=$(docker compose -f "$COMPOSE_FILE" ps --format "{{.Status}}" n8n 2>/dev/null)
if echo "$STATUS" | grep -q "Up"; then
    [ "$MODE" = "interactive" ] && echo "  ✔  Contenedor: $STATUS"
    OK=$((OK + 1))
else
    [ "$MODE" = "interactive" ] && echo "  ✘  Contenedor: $STATUS"
    FAIL=$((FAIL + 1))
fi

# 2. Endpoint healthz
if [ "$MODE" = "interactive" ]; then echo ""; echo "── Health HTTP ──"; fi
HEALTH=$(wget -q -O - "${N8N_URL}/healthz" 2>/dev/null)
if echo "$HEALTH" | grep -q '"ok"'; then
    [ "$MODE" = "interactive" ] && echo "  ✔  /healthz → OK"
    OK=$((OK + 1))
else
    [ "$MODE" = "interactive" ] && echo "  ✘  /healthz → $HEALTH"
    FAIL=$((FAIL + 1))
fi

# 3. Puerto abierto
PORT_CHECK=$(ss -ltnp | grep 5678 | head -1)
if [ -n "$PORT_CHECK" ]; then
    [ "$MODE" = "interactive" ] && echo "  ✔  Puerto 5678 → abierto"
    OK=$((OK + 1))
else
    [ "$MODE" = "interactive" ] && echo "  ✘  Puerto 5678 → no escucha"
    FAIL=$((FAIL + 1))
fi

# 4. Logs sin errores recientes
if [ "$MODE" = "interactive" ]; then echo ""; echo "── Logs recientes ──"; fi
ERRORS=$(docker compose -f "$COMPOSE_FILE" logs --since=5m --tail=50 n8n 2>/dev/null | grep -i "error\\|fail\\|exception\\|traceback\\|crash" | grep -v "Failed to start Python task runner" || true)
ERROR_COUNT=$(echo "$ERRORS" | grep -c . || true)
if [ "$ERROR_COUNT" -eq 0 ]; then
    [ "$MODE" = "interactive" ] && echo "  ✔  Sin errores en últimos 5 minutos"
    OK=$((OK + 1))
else
    [ "$MODE" = "interactive" ] && echo "  ⚠️  $ERRORS errores en últimos 5 minutos"
    FAIL=$((FAIL + 1))
fi

# 5. Workflows activos
if [ "$MODE" = "interactive" ]; then echo ""; echo "── Workflows activos ──"; fi
ACTIVE=$(docker compose -f "$COMPOSE_FILE" logs --tail=100 n8n 2>/dev/null | grep "Activated workflow" | tail -5)
if [ -n "$ACTIVE" ]; then
    [ "$MODE" = "interactive" ] && echo "$ACTIVE" | while IFS= read -r line; do
        echo "  ✔  $line"
    done
    OK=$((OK + 1))
else
    [ "$MODE" = "interactive" ] && echo "  ⚠️  No se detectaron workflows activos en logs"
    FAIL=$((FAIL + 1))
fi

TOTAL=$((OK + FAIL))

if [ "$MODE" = "interactive" ]; then
    echo ""
    echo "── Recursos ──"
    docker stats n8n --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" 2>/dev/null | tail -1
    echo ""
    echo "── Resumen ──"
    echo "  OK:   $OK/$TOTAL"
    echo "  FAIL: $FAIL/$TOTAL"
    echo ""
fi

if [ "$FAIL" -gt 0 ]; then
    [ "$MODE" = "interactive" ] && echo "  ⚠️  Hay problemas con n8n. Revisar logs completos:"
    [ "$MODE" = "interactive" ] && echo "  docker compose -f $COMPOSE_FILE logs --tail=80 n8n"
    exit 1
else
    [ "$MODE" = "interactive" ] && echo "  ✔  n8n funcionando correctamente."
    exit 0
fi
