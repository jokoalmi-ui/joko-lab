#!/bin/bash
# =============================================================================
# lock-backlog.sh — Protocolo de lock para el backlog del lab
# =============================================================================
# Resuelve: colisiones de escritura entre sesiones paralelas (CLI + Telegram)
# en 04-operations/backlogs/2026-07-31-backlog.md (subagente hermano vs TG).
#
# Uso:
#   lock-backlog.sh acquire [nota]   # Tomar el lock (falla si ya está tomado)
#   lock-backlog.sh release          # Liberar el lock
#   lock-backlog.sh status           # Ver quién lo tiene
#   lock-backlog.sh force-release    # Liberar un lock obsoleto (stale)
#
# Regla del protocolo (RULE-009):
#   1. ANTES de editar el backlog  → acquire
#   2. Editar (con backup .bak-* previo SIEMPRE)
#   3. DESPUÉS de editar           → release
#   4. Si acquire falla → otra sesión está editando: ESPERAR y reintentar,
#      nunca editar sin lock.
#
# Stale lock: si el PID del lock ya no existe, se considera obsoleto y
# force-release lo limpia (el proceso murió sin liberar).
# =============================================================================

LOCK_DIR="/home/jokoalmi/joko-lab/04-operations/backlogs"
LOCK_FILE="${LOCK_DIR}/.backlog.lock"
LOCK_TIMEOUT_STALE=3600  # 1h: un lock con PID vivo pero más viejo que esto se reporta

# -----------------------------------------------------------------------------
# Encuentra el PID del proceso Hermes que invoca este script (el ancestro de
# larga vida, no el subshell del script que muere al instante). Sube por la
# cadena de PPIDs hasta encontrar un proceso hermes/python del agente.
find_hermes_pid() {
    local pid=$$
    local name=""
    for _ in $(seq 1 15); do
        name=$(ps -p "$pid" -o comm= 2>/dev/null)
        # ¿Es un proceso Hermes? (python3 .../hermes o hermes)
        if echo "$name" | grep -qE "^(python3?|hermes)$"; then
            local full
            full=$(ps -p "$pid" -o args= 2>/dev/null)
            if echo "$full" | grep -qE "hermes"; then
                echo "$pid"
                return 0
            fi
        fi
        local ppid
        ppid=$(ps -p "$pid" -o ppid= 2>/dev/null | tr -d ' ')
        [ -z "$ppid" ] || [ "$ppid" = "0" ] || [ "$ppid" = "$pid" ] && break
        pid=$ppid
    done
    # Fallback: el PPID directo del script
    ps -p $$ -o ppid= 2>/dev/null | tr -d ' '
}

# -----------------------------------------------------------------------------
# ¿El PID está vivo?
pid_alive() {
    [ -n "$1" ] && kill -0 "$1" 2>/dev/null
}

# -----------------------------------------------------------------------------
acquire() {
    local nota="${1:-sin nota}"
    local my_pid
    my_pid=$(find_hermes_pid)
    if [ -f "$LOCK_FILE" ]; then
        # ¿El PID que lo tiene sigue vivo?
        local pid_holder
        pid_holder=$(grep -oP '^PID:\s*\K[0-9]+' "$LOCK_FILE" 2>/dev/null)
        if pid_alive "$pid_holder"; then
            echo "❌ LOCK TOMADO por PID $pid_holder:"
            cat "$LOCK_FILE"
            echo "→ Espera a que libere (release) o usa force-release si es stale."
            exit 1
        else
            echo "⚠️ Lock obsoleto (PID $pid_holder muerto). Liberando automáticamente..."
            rm -f "$LOCK_FILE"
        fi
    fi
    # Adquirir (guardamos el PID de Hermes de larga vida, no el del subshell)
    {
        echo "PID: $my_pid"
        echo "Proceso: $(ps -p "$my_pid" -o args= 2>/dev/null | cut -c1-80)"
        echo "Hora: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "Sesión: ${HERMES_SESSION:-desconocida}"
        echo "Nota: $nota"
    } > "$LOCK_FILE"
    echo "✅ Lock adquirido (PID Hermes $my_pid) — edita el backlog y luego:"
    echo "   lock-backlog.sh release"
}

# -----------------------------------------------------------------------------
release() {
    if [ ! -f "$LOCK_FILE" ]; then
        echo "ℹ️ No hay lock que liberar."
        exit 0
    fi
    local pid_holder my_pid
    pid_holder=$(grep -oP '^PID:\s*\K[0-9]+' "$LOCK_FILE" 2>/dev/null)
    my_pid=$(find_hermes_pid)
    if [ -n "$pid_holder" ] && [ "$pid_holder" != "$my_pid" ]; then
        echo "⚠️ El lock pertenece a PID $pid_holder, no a ti ($my_pid)."
        echo "   ¿Seguro? Forzar con: lock-backlog.sh force-release"
        exit 1
    fi
    rm -f "$LOCK_FILE"
    echo "✅ Lock liberado."
}

# -----------------------------------------------------------------------------
status() {
    if [ ! -f "$LOCK_FILE" ]; then
        echo "🔓 Sin lock — el backlog está libre."
        exit 0
    fi
    echo "🔒 Lock presente:"
    cat "$LOCK_FILE"
    local pid_holder
    pid_holder=$(grep -oP '^PID:\s*\K[0-9]+' "$LOCK_FILE" 2>/dev/null)
    if pid_alive "$pid_holder"; then
        echo "→ PID $pid_holder VIVO (sesión activa editando)."
    else
        echo "→ PID $pid_holder MUERTO → lock STALE, usar force-release."
    fi
}

# -----------------------------------------------------------------------------
force_release() {
    if [ ! -f "$LOCK_FILE" ]; then
        echo "ℹ️ No hay lock que liberar."
        exit 0
    fi
    echo "⚠️ Forzando liberación:"
    cat "$LOCK_FILE"
    rm -f "$LOCK_FILE"
    echo "✅ Lock eliminado por fuerza."
}

# -----------------------------------------------------------------------------
case "${1:-status}" in
    acquire)       acquire "$2" ;;
    release)       release ;;
    status)        status ;;
    force-release) force_release ;;
    *) echo "Uso: $0 {acquire|release|status|force-release} [nota]"; exit 2 ;;
esac
