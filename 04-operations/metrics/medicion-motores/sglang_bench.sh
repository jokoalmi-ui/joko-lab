#!/usr/bin/env bash
# Lanzador AISLADO de SGLang para el banco de medida (Joko Lab).
# NO toca automation-stack, ni n8n, ni compose. Contenedor suelto con nombre propio.
set -u
GGUF="/mnt/ssd_ia_datos/LM STUDIO/GT-Edge-AI/Dolphin3.0-Llama3.1-8B-Cyber-LoRA-Test-v0.2/Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf"
NAME=sglang-bench
IMG=lmsysorg/sglang:v0.5.21-cu130-runtime
PORT=30000

case "${1:-}" in
  start)
    docker rm -f "$NAME" >/dev/null 2>&1 || true
    docker run -d --name "$NAME" --gpus all --net=host --shm-size 8g \
      -v "$GGUF:/models/model.gguf:ro" \
      -e SGLANG_ENABLE_JIT_DEEPGEMM=0 \
      "$IMG" \
      python3 -m sglang.launch_server \
        --model-path /models/model.gguf \
        --load-format gguf \
        --host 127.0.0.1 --port $PORT \
        --context-length 8192 \
        --attention-backend triton \
        --sampling-backend pytorch \
        --mem-fraction-static 0.85
    echo "lanzado (docker run rc=$?)";;
  logs)   docker logs --tail "${2:-40}" "$NAME";;
  wait)
    for i in $(seq 1 90); do
      if curl -s -m 3 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
        echo "SGLang LISTO tras ~$((i*5))s"; exit 0; fi
      if ! docker ps --format '{{.Names}}' | grep -qx "$NAME"; then
        echo "contenedor NO esta corriendo; ultimas lineas:"; docker logs --tail 30 "$NAME"; exit 1; fi
      sleep 5
    done
    echo "timeout esperando a SGLang"; docker logs --tail 30 "$NAME"; exit 1;;
  gpu)    docker exec "$NAME" nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader 2>/dev/null; nvidia-smi --query-gpu=memory.used,utilization.gpu,temperature.gpu --format=csv,noheader;;
  stop)   docker stop "$NAME" >/dev/null 2>&1; echo "parado (el contenedor sigue existiendo)";;
  *) echo "uso: $0 {start|wait|logs [n]|gpu|stop}";;
esac
