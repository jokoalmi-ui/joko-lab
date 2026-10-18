#!/usr/bin/env bash
# lab-panel.sh — lanzador del panel de estado del Joko Lab (equivalente al .bat de Windows).
#
#   doble clic / ./lab-panel.sh        arranca el panel y abre el navegador
#   ./lab-panel.sh stop                para SOLO el panel del lab (no toca Docker, ni n8n, ni nada más)
#   ./lab-panel.sh estado              dice si está corriendo y muestra las últimas líneas del log
#
# Variables opcionales:  LABPANEL_PORT (def 8099) · LABPANEL_REFRESH (def 5 minutos)

set -u
LAB="/home/jokoalmi/joko-lab"
DIR="$LAB/research/lab-panel"
PIDFILE="$DIR/panel.pid"
LOG="$DIR/panel.log"
PUERTO="${LABPANEL_PORT:-8099}"
REFRESH="${LABPANEL_REFRESH:-5}"
URL="http://localhost:${PUERTO}/"

responde() { curl -s -o /dev/null -m 2 "$URL"; }

case "${1:-arrancar}" in
  arrancar)
    mkdir -p "$DIR"
    if responde; then
      echo "El panel ya está corriendo en $URL — solo abro el navegador."
      xdg-open "$URL" >/dev/null 2>&1 &
      notify-send "Joko Lab — panel" "Ya estaba corriendo. Abriendo $URL" 2>/dev/null
      exit 0
    fi
    echo "Arrancando el panel del lab (puerto $PUERTO, autorefresco cada $REFRESH min)…"
    cd "$LAB" || { echo "No encuentro $LAB"; exit 1; }
    # PATH fijo y python3 del sistema: un .desktop no hereda el entorno del shell,
    # y si al lanzar desde el escritorio falta entorno, el panel se queda a medias.
    export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    PY="$(command -v /usr/bin/python3 || command -v python3)"
    [ -n "$PY" ] || { echo "No encuentro python3."; exit 1; }
    nohup "$PY" tools/lab_panel.py --serve --open --refresh "$REFRESH" --port "$PUERTO" >>"$LOG" 2>&1 &
    echo $! > "$PIDFILE"
    for _ in $(seq 1 30); do
      responde && break
      sleep 1
    done
    if responde; then
      echo "Panel listo: $URL   (pid $(cat "$PIDFILE"), log $LOG)"
      echo "Para pararlo:  $0 stop"
      notify-send "Joko Lab — panel listo" "Instantánea real del lab en $URL" 2>/dev/null
      exit 0
    fi
    echo "El panel no ha respondido en 30 s. Últimas líneas del log:"
    tail -12 "$LOG"
    exit 1
    ;;
  stop)
    if [ ! -f "$PIDFILE" ]; then echo "No hay PID guardado ($PIDFILE)."; exit 1; fi
    PID="$(cat "$PIDFILE")"
    if ! kill -0 "$PID" 2>/dev/null; then
      echo "El proceso $PID ya no existe. Limpio el PID guardado."
      rm -f "$PIDFILE"
      exit 0
    fi
    echo "Parando SOLO el panel del lab (pid $PID, puerto $PUERTO)…"
    kill -TERM "$PID" 2>/dev/null
    for _ in $(seq 1 10); do kill -0 "$PID" 2>/dev/null || break; sleep 1; done
    if kill -0 "$PID" 2>/dev/null; then
      echo "El proceso $PID sigue vivo. No lo fuerzo: míralo tú con: ps -p $PID -o pid,cmd"
      exit 1
    fi
    rm -f "$PIDFILE"
    echo "Parado."
    ;;
  estado)
    if responde; then echo "CORRIENDO · $URL"; else echo "PARADO · no responde en $URL"; fi
    [ -f "$PIDFILE" ] && echo "pid guardado: $(cat "$PIDFILE")"
    echo "--- últimas líneas del log ---"
    tail -6 "$LOG" 2>/dev/null || echo "(todavía no hay log)"
    ;;
  *)
    echo "Uso: $0 [arrancar|stop|estado]"; exit 1;;
esac
