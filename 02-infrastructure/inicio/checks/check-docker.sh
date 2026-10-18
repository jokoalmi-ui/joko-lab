#!/bin/bash
# check-docker.sh — Verifica que Docker esta corriendo
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

# 1. Docker daemon responde
if ! docker info >/dev/null 2>&1; then
    echo "ERROR: docker daemon no responde"
    exit 2
fi

# 2. Contenedores del stack
STACK_DIR="/home/jokoalmi/automation-stack"
if [ -f "$STACK_DIR/docker-compose.yml" ]; then
    RUNNING=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --status running -q 2>/dev/null | wc -l)
    TOTAL=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps -q 2>/dev/null | wc -l)
    if [ "$RUNNING" -lt "$TOTAL" ]; then
        echo "WARNING: $RUNNING/$TOTAL contenedores activos"
        exit 1
    fi
    echo "OK: $RUNNING/$TOTAL contenedores activos"
    exit 0
fi

echo "OK: docker daemon responde"
exit 0
