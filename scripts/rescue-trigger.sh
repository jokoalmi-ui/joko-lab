#!/bin/bash
# rescue-trigger.sh — Activado por udev cuando el USB de rescate se conecta
# Espera a que el mount esté listo y lanza rescue.sh como usuario jokoalmi

LOGFILE="/tmp/joko-rescue-trigger.log"
echo "$(date): USB detectado, esperando mount..." >> "$LOGFILE"

# Esperar hasta 30s a que aparezca el mount
for i in $(seq 1 30); do
    if [ -d "/run/media/jokoalmi/New Volume" ]; then
        echo "$(date): Mount detectado en iteración $i, lanzando rescue.sh..." >> "$LOGFILE"
        sudo -u jokoalmi bash /home/jokoalmi/hermes-lab/scripts/rescue.sh >> "$LOGFILE" 2>&1
        echo "$(date): rescue.sh completado (exit=$?)" >> "$LOGFILE"
        exit 0
    fi
    sleep 1
done

echo "$(date): Timeout — mount no apareció en 30s" >> "$LOGFILE"
exit 1
