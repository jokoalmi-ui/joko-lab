#!/usr/bin/env bash
# Servidor llama.cpp aislado para MoE con cache de expertos en VRAM
# (--moe-cache-mib, llama.cpp PR #29887, mergeado 2026-10-13).
#
# Medido en A2000 12 GB + i5-9500 (2026-10-18), gpt-oss-20b MXFP4 12,11 GB,
# -cmoe (expertos en RAM), ctx 4096, temp 0, 128-220 tokens:
#   cache   0 MiB -> 13,2 tok/s   VRAM 4.082 MiB
#   cache1024 MiB ->  5,4 tok/s   (thrashing: peor que sin cache)
#   cache2048 MiB ->  8,5 tok/s
#   cache4096 MiB -> 16,8 tok/s
#   cache6144 MiB -> 30,1 tok/s   VRAM 10.225 MiB  (+128%)
# OJO: por debajo de ~3 GiB la cache EMPEORA el rendimiento. No es "mas es mejor".
# La salida no es bit-identica frente a sin cache (orden de acumulacion FP
# distinto GPU/CPU): misma calidad, redaccion distinta.
#
# Uso:
#   moe-cache-server.sh start [--mib N] [--ctx N] [--port P] [--modelo RUTA]
#   moe-cache-server.sh status
#   moe-cache-server.sh stop
set -uo pipefail

MODELO="/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/gpt-oss-20b-GGUF/gpt-oss-20b-MXFP4.gguf"
BACKEND="$HOME/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.60.0"
VENDOR="$HOME/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1"
PIDFILE="$HOME/.cache/moe-cache.pid"
LOGFILE="$HOME/.cache/moe-cache.log"
PORT=8098
CTX=4096
MIB=6144

prevarg=""
for arg in "$@"; do
  case "$prevarg" in
    --mib)    MIB="$arg" ;;
    --ctx)    CTX="$arg" ;;
    --port)   PORT="$arg" ;;
    --modelo) MODELO="$arg" ;;
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
    for f in "$MODELO" "$BACKEND/llama-server"; do
      [ -e "$f" ] || { echo "FALTA: $f"; exit 1; }
    done
    # aviso si la RAM libre no cubre el modelo
    libre_mib=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
    tam_mib=$(( $(stat -c %s "$MODELO") / 1048576 ))
    if [ "$libre_mib" -lt "$tam_mib" ]; then
      echo "AVISO: RAM disponible ${libre_mib} MiB < modelo ${tam_mib} MiB. Puede ir a swap."
    fi
    export LD_LIBRARY_PATH="$VENDOR:$BACKEND"
    nohup "$BACKEND/llama-server" -m "$MODELO" -cmoe \
      --moe-cache-mib "$MIB" -c "$CTX" -ngl 99 -t 6 --flash-attn on --jinja \
      --host 127.0.0.1 --port "$PORT" >"$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    for _ in $(seq 1 120); do
      [ "$(salud)" = "200" ] && {
        echo "OK pid=$(cat "$PIDFILE") puerto=$PORT ctx=$CTX mib=$MIB modelo=$(basename "$MODELO") vram=$(vram) MiB"
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
  *) echo "uso: $0 start|status|stop [--mib N] [--ctx N] [--port P] [--modelo RUTA]"; exit 2 ;;
esac
