#!/bin/bash
# check-gateway.sh — Verifica que Hermes Gateway responde
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

# 1. Fuente de verdad: servicio systemd (el gateway es servicio de mensajeria,
#    no expone /health HTTP en esta instalacion)
if systemctl --user is-active hermes-gateway.service >/dev/null 2>&1; then
    # Comprobacion secundaria: si algun dia expone HTTP, confirmar tambien
    for PORT in 8080 9090; do
        if curl -s --max-time 2 http://localhost:$PORT/health >/dev/null 2>&1; then
            echo "OK: gateway activo (systemd) y responde en puerto $PORT"
            exit 0
        fi
    done
    echo "OK: gateway activo (systemd hermes-gateway.service)"
    exit 0
fi

# 2. Si no hay servicio activo pero el proceso existe
if pgrep -f "hermes.*gateway" >/dev/null 2>&1; then
    echo "WARNING: gateway procesado pero servicio systemd no activo"
    exit 1
fi

echo "ERROR: gateway no detectado"
exit 2
