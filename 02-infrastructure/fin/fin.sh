#!/bin/bash
# fin.sh — Protocolo de cierre de sesion de Joko Lab
# Version: 1.0.0
#
# Uso: ./fin.sh                    (no apaga el stack)
#      FIN_STOP_STACK=1 ./fin.sh   (apaga el stack al cerrar: docker compose down)
#
# Captura el estado final, compara con el inicial,
# hace backup si hay cambios, guarda estado-final.json.

# Flock: evitar ejecucion paralela (corrupcion de JSON)
FLOCK_FILE="$HOME/.joko-lab.lock"
exec 200>"$FLOCK_FILE"
flock -n 200 || { echo "ERROR: Ya hay una sesion de Joko Lab en ejecucion (lock en $FLOCK_FILE)"; exit 1; }

set -e

JOKO_LAB="$HOME/joko-lab"
INICIAL_JSON="$JOKO_LAB/02-infrastructure/inicio/estado-inicial.json"
FINAL_JSON="$JOKO_LAB/02-infrastructure/fin/estado-final.json"
REPORTS_DIR="$JOKO_LAB/04-operations/reports"
STACK_DIR="$HOME/automation-stack"
HERMES_LAB="$HOME/hermes-lab"
# Push automatico al cierre: remotos de hermes-lab que se empujan tras el checkpoint.
# Por defecto SOLO el bare local del SSD (el backup real). GitHub va a proposito:
#   FIN_PUSH_REMOTES="origin github" ~/joko-lab/02-infrastructure/fin/fin.sh
FIN_PUSH_REMOTES="${FIN_PUSH_REMOTES:-origin}"
FIN_PUSH_TIMEOUT="${FIN_PUSH_TIMEOUT:-60}"

# Colores
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
AZUL='\033[0;34m'
NC='\033[0m'

echo -e "${AZUL}========================================${NC}"
echo -e "${AZUL}  FIN: Joko Lab${NC}"
echo -e "${AZUL}  $(date '+%Y-%m-%d %H:%M:%S %Z')${NC}"
echo -e "${AZUL}========================================${NC}"
echo ""

# --- 1. SNAPSHOT DEL ESTADO ACTUAL ---
TIMESTAMP=$(date --iso-8601=seconds)
FECHA=$(date '+%Y-%m-%d')
HORA=$(date '+%H:%M:%S %Z')

# Git
GIT_BRANCH=""
GIT_COMMIT=""
GIT_DIRTY=0
if [ -d "$HERMES_LAB/.git" ]; then
    GIT_BRANCH=$(cd "$HERMES_LAB" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    GIT_COMMIT=$(cd "$HERMES_LAB" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    GIT_DIRTY=$(cd "$HERMES_LAB" && git status --porcelain 2>/dev/null | wc -l)
fi
# Estado de git del repo del lab (joko-lab) — anadido 2026-10-17: antes solo se media hermes-lab
JOKO_BRANCH=""
JOKO_COMMIT=""
JOKO_DIRTY=0
if [ -d "$JOKO_LAB/.git" ]; then
    JOKO_BRANCH=$(cd "$JOKO_LAB" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    JOKO_COMMIT=$(cd "$JOKO_LAB" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    JOKO_DIRTY=$(cd "$JOKO_LAB" && git status --porcelain 2>/dev/null | grep -vE '^\.\. (02-infrastructure/(inicio/estado-inicial|fin/estado-final)\.json|04-operations/reports/)' | wc -l)
fi

# Docker
DOCKER_RUNNING=0
DOCKER_TOTAL=0
if docker info >/dev/null 2>&1 && [ -f "$STACK_DIR/docker-compose.yml" ]; then
    DOCKER_RUNNING=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --status running -q 2>/dev/null | wc -l)
    DOCKER_TOTAL=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps -q 2>/dev/null | wc -l)
fi

# Herramientas
UV_INSTALLED=0
command -v uv >/dev/null 2>&1 && UV_INSTALLED=1
CARGO_INSTALLED=0
command -v cargo >/dev/null 2>&1 && CARGO_INSTALLED=1
NODE_INSTALLED=0
command -v node >/dev/null 2>&1 && NODE_INSTALLED=1
PYTHON_VER=$(python3 --version 2>/dev/null || echo "desconocido")

echo -e "${AZUL}--- ESTADO ACTUAL ---${NC}"
echo -e "  Git:    ${AZUL}$GIT_BRANCH${NC} @ ${AZUL}$GIT_COMMIT${NC} ($GIT_DIRTY pendientes)"
echo -e "  Docker: ${AZUL}$DOCKER_RUNNING/$DOCKER_TOTAL${NC} contenedores"
echo -e "  uv:     $([ "$UV_INSTALLED" = 1 ] && echo "${VERDE}OK${NC}" || echo "${ROJO}NO${NC}")"
echo -e "  cargo:  $([ "$CARGO_INSTALLED" = 1 ] && echo "${VERDE}OK${NC}" || echo "${AMARILLO}NO${NC}")"
echo -e "  node:   $([ "$NODE_INSTALLED" = 1 ] && echo "${VERDE}OK${NC}" || echo "${AMARILLO}NO${NC}")"
echo -e "  kernel: ${AZUL}$(uname -r)${NC}"
echo ""

# Sistema
KERNEL=$(uname -r 2>/dev/null || echo "desconocido")
NVIDIA_DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1 || echo "desconocido")

# Docker containers (nombres)
DOCKER_CONTAINERS="[]"
STACK_DIR="$HOME/automation-stack"
if docker info >/dev/null 2>&1 && [ -f "$STACK_DIR/docker-compose.yml" ]; then
    DOCKER_CONTAINERS=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --format json 2>/dev/null | python3 -c "
import sys, json
containers = []
for line in sys.stdin:
    try:
        c = json.loads(line)
        containers.append({'name': c.get('Name','?'), 'state': c.get('State','?')})
    except:
        pass
print(json.dumps(containers))
" 2>/dev/null || echo "[]")
fi

# --- 2. DIFF CONTRA ESTADO INICIAL ---
CAMBIOS=""
DETECTED=0

if [ -f "$INICIAL_JSON" ]; then
    echo -e "${AZUL}--- DIFF contra inicio de sesion ---${NC}"

    INICIO_FECHA=$(python3 -c "import json; d=json.load(open('$INICIAL_JSON')); print(d.get('fecha','?'), d.get('hora','?'))" 2>/dev/null || echo "desconocido")
    echo -e "  Inicio: ${AZUL}$INICIO_FECHA${NC}"

    INICIO_DOCKER=$(python3 -c "import json; d=json.load(open('$INICIAL_JSON')); print(d.get('docker',{}).get('running',0))" 2>/dev/null || echo "0")
    if [ "$DOCKER_RUNNING" != "$INICIO_DOCKER" ]; then
        echo -e "  ${AMARILLO}Docker: $INICIO_DOCKER -> $DOCKER_RUNNING contenedores${NC}"
        CAMBIOS="$CAMBIOS
  [INFRA] Docker: $INICIO_DOCKER -> $DOCKER_RUNNING contenedores"
        DETECTED=1
    else
        echo -e "  ${VERDE}Docker: sin cambios${NC}"
    fi

    INICIO_UV=$(python3 -c "import json; d=json.load(open('$INICIAL_JSON')); print(d.get('tools',{}).get('uv_installed',0))" 2>/dev/null || echo "0")
    if [ "$UV_INSTALLED" != "$INICIO_UV" ]; then
        echo -e "  ${ROJO}uv: CAMBIO DETECTADO${NC}"
        CAMBIOS="$CAMBIOS
  [INFRA] uv: $([ "$INICIO_UV" = 1 ] && echo 'instalado' || echo 'no instalado') -> $([ "$UV_INSTALLED" = 1 ] && echo 'instalado' || echo 'no instalado')"
        DETECTED=1
    else
        echo -e "  ${VERDE}uv: sin cambios${NC}"
    fi

    if [ "$GIT_DIRTY" -gt 0 ]; then
        echo -e "  ${AMARILLO}Git: $GIT_DIRTY archivos sin commit${NC}"
        CAMBIOS="$CAMBIOS
  [CODIGO] Git: $GIT_DIRTY archivos sin commit"
        DETECTED=1
    else
        echo -e "  ${VERDE}Git: limpio${NC}"
    fi
else
    echo -e "  ${AMARILLO}No hay estado-inicial.json (sesion no inicio con protocolo)${NC}"
fi
echo ""

# --- 3. BACKUP SI HAY CAMBIOS ---
if [ "$DETECTED" -gt 0 ] || [ "$GIT_DIRTY" -gt 0 ]; then
    echo -e "${AZUL}--- BACKUP ---${NC}"

    # Commit automatico si hay cambios
    if [ "$GIT_DIRTY" -gt 0 ]; then
        cd "$HERMES_LAB"
        git add -A 2>/dev/null || true
        JOKO_RDD_DISABLE=1 git commit -m "checkpoint: $FECHA $HORA" || true
        echo -e "  ${VERDE}Commit: OK${NC}"
        NEW_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        GIT_COMMIT="$NEW_COMMIT"
    else
        echo -e "  ${AMARILLO}Commit: sin cambios nuevos${NC}"
    fi

    echo -e "  Backup automatico completado."
else
    echo -e "${VERDE}Sin cambios detectados. Backup no necesario.${NC}"
fi
echo ""

# --- 3b. PUSH AUTOMATICO ---
# Empuja el checkpoint a los remotos indicados. Un fallo se AVISA (rc + salida) y NO
# aborta el cierre: el cierre local manda. Un remoto inexistente se omite con aviso.
echo -e "${AZUL}--- PUSH AUTOMATICO ---${NC}"
PUSH_RESUMEN=""
if [ -d "$HERMES_LAB/.git" ] && [ "$GIT_BRANCH" != "unknown" ]; then
    cd "$HERMES_LAB"
    for REMOTE in $FIN_PUSH_REMOTES; do
        if git remote | grep -qx "$REMOTE"; then
            if PUSH_OUT=$(timeout "$FIN_PUSH_TIMEOUT" git push "$REMOTE" "$GIT_BRANCH" 2>&1); then
                echo -e "  ${VERDE}Push $REMOTE: OK${NC} $(echo "$PUSH_OUT" | tail -1)"
                PUSH_RESUMEN="$PUSH_RESUMEN $REMOTE=OK"
            else
                PUSH_RC=$?
                echo -e "  ${ROJO}Push $REMOTE: FALLO (rc=$PUSH_RC)${NC}"
                echo "$PUSH_OUT" | while read -r PLINE; do
                    echo -e "    ${ROJO}$PLINE${NC}"
                done
                PUSH_RESUMEN="$PUSH_RESUMEN $REMOTE=FALLO(rc=$PUSH_RC)"
            fi
        else
            echo -e "  ${AMARILLO}Push $REMOTE: remoto inexistente, se omite${NC}"
            PUSH_RESUMEN="$PUSH_RESUMEN $REMOTE=OMITIDO"
        fi
    done
else
    echo -e "  ${AMARILLO}hermes-lab no es repo git o rama desconocida: push omitido${NC}"
    PUSH_RESUMEN=" no ejecutado"
fi
echo ""

# --- 4. GUARDAR ESTADO-FINAL.JSON (escritura atomica) ---
FINAL_TMP="${FINAL_JSON}.tmp"
cat > "$FINAL_TMP" << EOF
{
  "timestamp": "$TIMESTAMP",
  "fecha": "$FECHA",
  "hora": "$HORA",
  "sesion": {
    "inicio": $( [ -f "$INICIAL_JSON" ] && python3 -c "import json; print(json.dumps(open('$INICIAL_JSON').read()))" 2>/dev/null || echo '"no registrado"' )
  },
  "git": {
    "branch": "$GIT_BRANCH",
    "commit": "$GIT_COMMIT",
    "dirty_files": $GIT_DIRTY
  },
  "git_joko": {
    "branch": "$JOKO_BRANCH",
    "commit": "$JOKO_COMMIT",
    "dirty_files": $JOKO_DIRTY
  },
  "docker": {
    "running": $DOCKER_RUNNING,
    "total": $DOCKER_TOTAL,
    "containers": $DOCKER_CONTAINERS
  },
  "tools": {
    "uv_installed": $UV_INSTALLED,
    "cargo_installed": $CARGO_INSTALLED,
    "node_installed": $NODE_INSTALLED,
    "python_version": "$PYTHON_VER"
  },
  "system": {
    "kernel": "$KERNEL",
    "nvidia_driver": "$NVIDIA_DRIVER"
  },
  "cambios_detectados": $DETECTED
}
EOF
mv "$FINAL_TMP" "$FINAL_JSON"

echo -e "  ${VERDE}Estado guardado:${NC} $FINAL_JSON"

# --- 5. INFORME DE CIERRE ---
REPORT_FILE="$REPORTS_DIR/$FECHA-cierre-joko-lab.txt"
mkdir -p "$REPORTS_DIR"

{
    echo "CIERRE JOKO LAB — $FECHA $HORA"
    echo "========================================"
    echo ""
    echo "Git: $GIT_BRANCH @ $GIT_COMMIT"
    echo "Git joko-lab: $JOKO_BRANCH @ $JOKO_COMMIT ($JOKO_DIRTY sin commit)"
    echo "Push backup:$PUSH_RESUMEN"
    echo "Docker: $DOCKER_RUNNING/$DOCKER_TOTAL contenedores"
    echo "uv: $([ "$UV_INSTALLED" = 1 ] && echo 'OK' || echo 'NO')"
    echo "cargo: $([ "$CARGO_INSTALLED" = 1 ] && echo 'OK' || echo 'NO')"
    echo ""
    echo "Cambios detectados: $([ "$DETECTED" -gt 0 ] && echo 'SI' || echo 'NO')"
    if [ -n "$CAMBIOS" ]; then
        echo "$CAMBIOS"
    fi
    echo ""
    echo "--- Fin del informe ---"
} > "$REPORT_FILE"

echo -e "  ${VERDE}Informe:${NC} $REPORT_FILE"
echo ""

# --- 6. PARAR STACK DOCKER (opt-in: FIN_STOP_STACK=1) ---
echo -e "${AZUL}--- STACK DOCKER ---${NC}"
if [ "${FIN_STOP_STACK:-0}" != "1" ]; then
    echo -e "  ${VERDE}Stack intacto (el apagado es opt-in: FIN_STOP_STACK=1 $0)${NC}"
elif docker info >/dev/null 2>&1 && [ -f "$STACK_DIR/docker-compose.yml" ]; then
    echo -e "  ${AMARILLO}Parando $DOCKER_RUNNING contenedores...${NC}"
    DOWN_OUTPUT=$(docker compose -f "$STACK_DIR/docker-compose.yml" down 2>&1) || DOWN_OUTPUT="ERROR: docker compose down falló"
    echo -e "$DOWN_OUTPUT" | while read -r line; do
        echo -e "  ${AZUL}$line${NC}"
    done
    {
        echo ""
        echo "--- Salida del cierre Docker ($(date '+%H:%M:%S %Z')) ---"
        echo "$DOWN_OUTPUT"
        echo "--- Fin del cierre Docker ---"
    } >> "$REPORT_FILE"
    echo -e "  ${VERDE}Stack Docker detenido${NC}"
else
    echo -e "  ${AMARILLO}Docker no disponible o no hay stack definido${NC}"
fi
echo ""

# --- 7. CIERRE ---
echo -e "${VERDE}=== SESION CERRADA ===${NC}"
echo -e "  Fecha: $FECHA $HORA"
echo -e "  Estado: $FINAL_JSON"
echo ""

exit 0
