#!/bin/bash
# inicio.sh — Protocolo de apertura de sesion de Joko Lab
# Version: 1.0.0
#
# Uso: ./inicio.sh
#
# Ejecuta todos los checks, genera estado-inicial.json,
# compara con el ultimo estado-final.json y reporta anomalias.

# Flock: evitar ejecucion paralela (corrupcion de JSON)
FLOCK_FILE="$HOME/.joko-lab.lock"
exec 200>"$FLOCK_FILE"
flock -n 200 || { echo "ERROR: Ya hay una sesion de Joko Lab en ejecucion (lock en $FLOCK_FILE)"; exit 1; }

set -e

JOKO_LAB="$HOME/joko-lab"
CHECKS_DIR="$JOKO_LAB/02-infrastructure/inicio/checks"
INICIAL_JSON="$JOKO_LAB/02-infrastructure/inicio/estado-inicial.json"
FINAL_JSON="$JOKO_LAB/02-infrastructure/fin/estado-final.json"
REPORTS_DIR="$JOKO_LAB/04-operations/reports"
STACK_DIR="$HOME/automation-stack"

# Colores
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
AZUL='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${AZUL}========================================${NC}"
echo -e "${AZUL}  INICIO: Joko Lab${NC}"
echo -e "${AZUL}  $(date '+%Y-%m-%d %H:%M:%S %Z')${NC}"
echo -e "${AZUL}========================================${NC}"
echo ""

# --- LEVANTAR STACK DOCKER (si no esta completo) ---
# El stack baja con `docker compose down` en fin.sh (los contenedores se
# eliminan, los datos en /mnt/ssd_ia_datos persisten). Al abrir sesion se
# levanta de nuevo. Esto incluye n8n (zona protegida): ejecutar inicio.sh
# implica confirmar el arranque del stack completo.
echo -e "${AZUL}--- STACK DOCKER ---${NC}"
if docker info >/dev/null 2>&1 && [ -f "$STACK_DIR/docker-compose.yml" ]; then
    EXPECTED=$(docker compose -f "$STACK_DIR/docker-compose.yml" config --services 2>/dev/null | wc -l)
    STACK_UP=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --status running -q 2>/dev/null | wc -l)
    if [ "$STACK_UP" -lt "$EXPECTED" ]; then
        echo -e "  ${AMARILLO}Stack incompleto ($STACK_UP/$EXPECTED corriendo). Levantando...${NC}"
        UP_OUTPUT=$(docker compose -f "$STACK_DIR/docker-compose.yml" up -d 2>&1) || { echo -e "  ${ROJO}ERROR: fallo al levantar el stack${NC}"; exit 1; }
        echo -e "$UP_OUTPUT" | while read -r line; do
            echo -e "  ${AZUL}$line${NC}"
        done
        sleep 5
        STACK_UP=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --status running -q 2>/dev/null | wc -l)
        if [ "$STACK_UP" -lt "$EXPECTED" ]; then
            echo -e "  ${AMARILLO}Verificacion: $STACK_UP/$EXPECTED corriendo (revisar logs)${NC}"
        else
            echo -e "  ${VERDE}Stack levantado: $STACK_UP/$EXPECTED corriendo${NC}"
        fi
    else
        echo -e "  ${VERDE}Stack ya estaba arriba ($STACK_UP/$EXPECTED)${NC}"
    fi
else
    echo -e "  ${AMARILLO}Docker no disponible o no hay stack definido${NC}"
fi
echo ""

# --- EJECUTAR CHECKS ---
TOTAL=0
PASS=0
WARN=0
FAIL=0
ANOMALIAS=""

echo -e "${AZUL}--- CHECKS ---${NC}"

for check in "$CHECKS_DIR"/check-*.sh; do
    [ -f "$check" ] || continue
    NAME=$(basename "$check" .sh | sed 's/check-//')
    TOTAL=$((TOTAL + 1))

    set +e
    OUTPUT=$("$check" 2>&1)
    EXIT_CODE=$?
    set -e

    LINE="${NAME} "
    # Pad to 20 chars
    while [ ${#LINE} -lt 18 ]; do LINE="${LINE}."; done

    if [ "$EXIT_CODE" -eq 0 ]; then
        echo -e "  ${LINE} ${VERDE}OK${NC}  $(echo "$OUTPUT" | head -1)"
        PASS=$((PASS + 1))
    elif [ "$EXIT_CODE" -eq 1 ]; then
        echo -e "  ${LINE} ${AMARILLO}WARN${NC} $(echo "$OUTPUT" | head -1)"
        WARN=$((WARN + 1))
        ANOMALIAS="$ANOMALIAS
  [MEDIA] $NAME — $(echo "$OUTPUT" | head -1)"
    else
        echo -e "  ${LINE} ${ROJO}FAIL${NC} $(echo "$OUTPUT" | head -1)"
        FAIL=$((FAIL + 1))
        ANOMALIAS="$ANOMALIAS
  [ALTA] $NAME — $(echo "$OUTPUT" | head -1)"
    fi
done

echo ""

# --- GENERAR ESTADO-INICIAL.JSON ---
TIMESTAMP=$(date --iso-8601=seconds)

# Estado de git
GIT_BRANCH=""
GIT_COMMIT=""
GIT_DIRTY=""
if [ -d "$HOME/hermes-lab/.git" ]; then
    GIT_BRANCH=$(cd "$HOME/hermes-lab" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    GIT_COMMIT=$(cd "$HOME/hermes-lab" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    GIT_DIRTY=$(cd "$HOME/hermes-lab" && git status --porcelain 2>/dev/null | wc -l)
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

# Estado de docker
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

# PATH
PATH_HAS_LOCAL_BIN=0
echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.local/bin" && PATH_HAS_LOCAL_BIN=1
PATH_HAS_CARGO_BIN=0
echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.cargo/bin" && PATH_HAS_CARGO_BIN=1
PATH_FULL="$PATH"

# Sistema
KERNEL=$(uname -r 2>/dev/null || echo "desconocido")
NVIDIA_DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1 || echo "desconocido")
CUDA_VER=$(nvcc --version 2>/dev/null | grep "release" | awk '{print $6}' | sed 's/,//' || echo "desconocido")

# Docker containers (nombres, no solo count)
DOCKER_CONTAINERS="[]"
if docker info >/dev/null 2>&1 && [ -f "$STACK_DIR/docker-compose.yml" ]; then
    DOCKER_CONTAINERS=$(docker compose -f "$STACK_DIR/docker-compose.yml" ps --format json 2>/dev/null | python3 -c "
import sys, json
containers = []
for line in sys.stdin:
    try:
        c = json.loads(line)
        containers.append({'name': c.get('Name','?'), 'state': c.get('State','?'), 'status': c.get('Status','?')})
    except:
        pass
print(json.dumps(containers))
" 2>/dev/null || echo "[]")
fi
# LM Studio modelos (si el API no responde, no abortar: set -e activo)
LMS_MODELS="[]"
LMS=$(curl -s --max-time 3 http://localhost:1234/api/v0/models 2>/dev/null || echo "")
if [ -n "$LMS" ]; then
    LMS_MODELS=$(echo "$LMS" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    models = [m.get('id','?') for m in d.get('data',[])]
    print(json.dumps(models))
except:
    print('[]')
" 2>/dev/null || echo "[]")
fi

# Escritura atomica: .tmp + mv (evita JSON truncado por interrupcion)
INICIAL_TMP="${INICIAL_JSON}.tmp"
cat > "$INICIAL_TMP" << EOF
{
  "timestamp": "$TIMESTAMP",
  "fecha": "$(date '+%Y-%m-%d')",
  "hora": "$(date '+%H:%M:%S %Z')",
  "checks": {
    "total": $TOTAL,
    "pass": $PASS,
    "warn": $WARN,
    "fail": $FAIL
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
  "path": {
    "has_local_bin": $PATH_HAS_LOCAL_BIN,
    "has_cargo_bin": $PATH_HAS_CARGO_BIN,
    "full": "$PATH_FULL"
  },
  "system": {
    "kernel": "$KERNEL",
    "nvidia_driver": "$NVIDIA_DRIVER",
    "cuda_version": "$CUDA_VER"
  },
  "lm_studio_models": $LMS_MODELS
}
EOF
mv "$INICIAL_TMP" "$INICIAL_JSON"

echo -e "${AZUL}--- ESTADO INICIAL ---${NC}"
echo -e "  Git:    ${AZUL}$GIT_BRANCH${NC} @ ${AZUL}$GIT_COMMIT${NC}"
if [ "$GIT_DIRTY" -gt 0 ]; then
    echo -e "  Git:    ${AMARILLO}$GIT_DIRTY archivo(s) sin commit${NC}"
fi
echo -e "  Docker: ${AZUL}$DOCKER_RUNNING/$DOCKER_TOTAL${NC} contenedores"
echo -e "  Checks: ${VERDE}$PASS pass${NC}, ${AMARILLO}$WARN warn${NC}, ${ROJO}$FAIL fail${NC}"
echo ""

# --- DIFF CONTRA ULTIMO ESTADO FINAL ---
if [ -f "$FINAL_JSON" ]; then
    echo -e "${AZUL}--- DIFF contra ultimo cierre ---${NC}"

    LAST_FECHA=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('fecha','?'), d.get('hora','?'))" 2>/dev/null || echo "desconocido")
    echo -e "  Ultimo cierre: ${AZUL}$LAST_FECHA${NC}"

    # Comparaciones basicas
    DIFFS=""

    LAST_DOCKER=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('docker',{}).get('running',0))" 2>/dev/null || echo "0")
    if [ "$DOCKER_RUNNING" != "$LAST_DOCKER" ]; then
        DIFFS="$DIFFS
  ${AMARILLO}Docker: $LAST_DOCKER contenedores -> $DOCKER_RUNNING${NC}"
    fi

    LAST_UV=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('tools',{}).get('uv_installed',0))" 2>/dev/null || echo "0")
    if [ "$UV_INSTALLED" != "$LAST_UV" ]; then
        DIFFS="$DIFFS
  ${ROJO}uv: $([ "$LAST_UV" = 1 ] && echo 'instalado' || echo 'no instalado') -> $([ "$UV_INSTALLED" = 1 ] && echo 'instalado' || echo 'NO INSTALADO')${NC}"
    fi

    LAST_GIT_COMMIT=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('git',{}).get('commit',''))" 2>/dev/null || echo "")
    if [ "$GIT_COMMIT" != "$LAST_GIT_COMMIT" ] && [ -n "$LAST_GIT_COMMIT" ]; then
        DIFFS="$DIFFS
  ${AZUL}Git commit: $LAST_GIT_COMMIT -> $GIT_COMMIT${NC}"
    fi

    LAST_JOKO_COMMIT=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('git_joko',{}).get('commit',''))" 2>/dev/null || echo "")
    if [ -n "$LAST_JOKO_COMMIT" ] && [ "$JOKO_COMMIT" != "$LAST_JOKO_COMMIT" ]; then
        DIFFS="$DIFFS
  ${AZUL}joko-lab commit: $LAST_JOKO_COMMIT -> $JOKO_COMMIT${NC}"
    fi
    LAST_JOKO_DIRTY=$(python3 -c "import json; d=json.load(open('$FINAL_JSON')); print(d.get('git_joko',{}).get('dirty_files',-1))" 2>/dev/null || echo "-1")
    if [ "$LAST_JOKO_DIRTY" != "-1" ] && [ "$JOKO_DIRTY" != "$LAST_JOKO_DIRTY" ]; then
        DIFFS="$DIFFS
  ${AMARILLO}joko-lab sin commit: $LAST_JOKO_DIRTY -> $JOKO_DIRTY${NC}"
    fi

    if [ -z "$DIFFS" ]; then
        echo -e "  ${VERDE}Sin diferencias detectadas.${NC}"
    else
        echo -e "  ${AMARILLO}Diferencias encontradas:${NC}$DIFFS"
        ANOMALIAS="$ANOMALIAS
$DIFFS"
    fi
else
    echo -e "  ${AMARILLO}No hay estado-final.json previo (primera ejecucion)${NC}"
fi
echo ""

# --- REPORTAR ANOMALIAS ---
if [ -n "$ANOMALIAS" ]; then
    echo -e "${AMARILLO}--- ANOMALIAS DETECTADAS ---${NC}$ANOMALIAS"
    echo ""
fi

# --- RESUMEN ---
echo -e "${AZUL}--- RESUMEN ---${NC}"
if [ "$FAIL" -gt 0 ]; then
    echo -e "  ${ROJO}$FAIL check(s) criticos fallaron${NC}"
    echo -e "  Revisa antes de empezar a trabajar."
elif [ "$WARN" -gt 0 ]; then
    echo -e "  ${AMARILLO}$WARN check(s) con advertencias${NC}"
    echo -e "  Puedes trabajar pero revisa las advertencias."
else
    echo -e "  ${VERDE}Todo correcto.${NC}"
fi

echo ""
echo -e "${VERDE}=== LABORATORIO LISTO ===${NC}"

exit $FAIL
