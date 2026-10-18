#!/usr/bin/env bash
# Servidor llama.cpp aislado con Gemma 4 12B QAT + speculative decoding MTP.
# Medido en A2000 12 GB (2026-10-18): +80% a +88% tok/s frente a sin MTP,
# texto identico a temperatura 0. LM Studio 0.4.20 NO puede usar este MTP
# (exige cabeza MTP embebida en el GGUF); esta ventana es la via operativa.
#
# Uso:
#   gemma-mtp-server.sh start [--ctx N] [--nmax N] [--port P]
#   gemma-mtp-server.sh status
#   gemma-mtp-server.sh stop
set -uo pipefail

MODELO="/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/gemma-4-12B-it-QAT-GGUF/gemma-4-12B-it-QAT-Q4_0.gguf"
DRAFT="$HOME/joko-lab/05-inference/models/gemma-4-12B-it-qat-assistant-MTP-Q8_0.gguf"
BACKEND="$HOME/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.60.0"
VENDOR="$HOME/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1"
PIDFILE="$HOME/.cache/gemma-mtp.pid"
LOGFILE="$HOME/.cache/gemma-mtp.log"
PORT=8099
CTX=32768
NMAX=4

prevarg=""
for arg in "$@"; do
  case "$prevarg" in
    --ctx)  CTX="$arg" ;;
    --nmax) NMAX="$arg" ;;
    --port) PORT="$arg" ;;
  esac
  prevarg="$arg"
done
CMD="${1:-status}"

vram() { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1; }

salud() { curl -s -m 3 -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/health"; }

case "$CMD" in
  start)
    if ss -ltn 2>/dev/null | grep -q ":$PORT "; then
      echo "ABORTO: puerto $PORT ya ocupado. Usa: ss -ltnp | grep $PORT"; exit 1
    fi
    for f in "$MODELO" "$DRAFT" "$BACKEND/llama-server"; do
      [ -e "$f" ] || { echo "FALTA: $f"; exit 1; }
    done
    export LD_LIBRARY_PATH="$VENDOR:$BACKEND"
    nohup "$BACKEND/llama-server" -m "$MODELO" -md "$DRAFT" \
      --spec-type draft-mtp --spec-draft-n-max "$NMAX" \
      -c "$CTX" -ngl 99 -t 6 --flash-attn on --jinja \
      --host 127.0.0.1 --port "$PORT" >"$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    for _ in $(seq 1 90); do
      [ "$(salud)" = "200" ] && {
        echo "OK pid=$(cat "$PIDFILE") puerto=$PORT ctx=$CTX nmax=$NMAX vram=$(vram) MiB"
        echo "log: $LOGFILE   stop: $0 stop"; exit 0; }
      kill -0 "$(cat "$PIDFILE")" 2>/dev/null || { echo "MURIO al cargar. Ultimas lineas:"; tail -15 "$LOGFILE"; exit 1; }
      sleep 2
    done
    echo "TIMEOUT esperando /health. Revisa $LOGFILE"; exit 1
    ;;
  status)
    echo "health=$([[ "$(salud)" = "200" ]] && echo up || echo down) puerto=$PORT vram=$(vram) MiB"
    [ -f "$PIDFILE" ] && echo "pid=$(cat "$PIDFILE") $(kill -0 "$(cat "$PIDFILE")" 2>/dev/null && echo vivo || echo muerto)"
    curl -s -m 3 "http://127.0.0.1:$PORT/props" 2>/dev/null | head -c 300; echo
    ;;
  stop)
    [ -f "$PIDFILE" ] || { echo "Sin pidfile: nada que parar"; exit 0; }
    P=$(cat "$PIDFILE")
    if kill -0 "$P" 2>/dev/null; then
      kill "$P"; for _ in $(seq 1 15); do kill -0 "$P" 2>/dev/null || break; sleep 1; done
      kill -0 "$P" 2>/dev/null && kill -9 "$P"
      echo "parado pid=$P vram=$(vram) MiB"
    else
      echo "pid $P ya no existia"
    fi
    rm -f "$PIDFILE"
    ;;
  *) echo "uso: $0 start|status|stop [--ctx N] [--nmax N] [--port P]"; exit 2 ;;
esac
