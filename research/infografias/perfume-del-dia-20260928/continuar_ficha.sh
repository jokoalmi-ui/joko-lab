#!/bin/bash
# Continuación automática de la ficha del día 28-09-2026 — Loewe 7 Plata
# Motivo: GPU colgada (nvidia-smi sin responder) → se reinicia el PC y este script
# retoma la tarea sin intervención: espera la GPU, genera el fondo SDXL, renderiza,
# pasa la puerta de calidad y envía la ficha al canal.
# Idempotente: si ya existe ficha_enviada.ok no hace nada.
# Prueba en seco (sin GPU, sin enviar, todo en /tmp): FICHA_DRY=1 bash continuar_ficha.sh
set -u
D=/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20260928
LOG="$D/post_reboot.log"
MARK="$D/ficha_enviada.ok"
CANAL="telegram:-1003968087263"
DM="telegram:1052590045"
HTML="$D/perfume_del_dia_v5_7plata.html"
FONDO="$D/7plata_fondo.png"
R1="$D/render_7plata_1.png"; R2="$D/render_7plata_2.png"
PNG="$D/ficha_perfume_del_dia_20260928_7plata.png"
DRY="${FICHA_DRY:-0}"

cd "$D" || exit 1
exec >> "$LOG" 2>&1

avisar() { /home/jokoalmi/.local/bin/hermes send --to "$DM" "$1" >/dev/null 2>&1 || true; }

echo "=== $(date '+%F %T') inicio (DRY=$DRY) ==="
if [ -f "$MARK" ]; then echo "ya enviada el $(cat "$MARK") — nada que hacer"; exit 0; fi

if [ "$DRY" = "1" ]; then
  TD=/tmp/ficha_dry; mkdir -p "$TD"
  cp "$D/7plata_figura.png" "$D/qr_fragrantica.png" "$TD/" 2>/dev/null
  python3 -c "
from PIL import Image, ImageDraw
im = Image.new('RGB',(1024,1024),(238,242,244)); d = ImageDraw.Draw(im)
for y in range(1024): d.line([(0,y),(1024,y)], fill=(238-y//24, 242-y//28, 244-y//32))
im.save('$TD/fondo.png')
s = open('$HTML', encoding='utf-8').read().replace(\"url('7plata_fondo.png')\", \"url('fondo.png')\")
open('$TD/ficha.html','w',encoding='utf-8').write(s)
print('[dry] fondo y html de prueba en', '$TD')
"
  HTML="$TD/ficha.html"; FONDO="$TD/fondo.png"; R1="$TD/r1.png"; R2="$TD/r2.png"; PNG="$TD/ficha_dry.png"
fi

# 1) esperar a que la GPU responda
if [ "$DRY" = "1" ]; then
  echo "[dry] salto la espera de GPU y ComfyUI"
else
  ok=0
  for i in $(seq 1 45); do
    if timeout 15 nvidia-smi --query-gpu=name --format=csv,noheader >/dev/null 2>&1; then ok=1; break; fi
    echo "$(date '+%T') GPU sin responder (intento $i/45)"; sleep 20
  done
  if [ "$ok" != "1" ]; then
    echo "GPU NO responde tras ~15 min: se deja pendiente, sin enviar nada"
    avisar "Ficha del día: la GPU sigue colgada tras el reinicio, no he podido generar el fondo. Queda pendiente."
    exit 1
  fi
  echo "GPU OK: $(timeout 15 nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader)"

  # 2) ComfyUI + fondo SDXL
  systemctl --user start comfyui
  listo=0
  for i in $(seq 1 30); do
    if curl -s --max-time 5 http://127.0.0.1:8188/system_stats >/dev/null; then listo=1; break; fi
    sleep 5
  done
  if [ "$listo" != "1" ]; then
    echo "ComfyUI no abre el puerto 8188"
    avisar "Ficha del día: la GPU responde pero ComfyUI no arranca (8188 cerrado). Queda pendiente."
    exit 1
  fi
  echo "ComfyUI listo"
  cd /home/jokoalmi/ComfyUI || exit 1
  TMPDIR=/home/jokoalmi/tmp_comfy ./venv/bin/python gen_comfy.py \
    "editorial still-life background photograph, pale marble table beside a large window, fresh mint sprigs and curls of mandarin peel on a small silver tray, soft morning sunlight and long gentle shadows, blurred modern office interior with glass and green plants, airy minimal composition with lots of empty space, palette of cool silver blue, soft cream and warm amber, shallow depth of field, high detail, no text" \
    "$FONDO" --seed 42 --steps 20 --size 1024
  echo "gen_comfy rc=$?"
  cd "$D" || exit 1
  systemctl --user stop comfyui
  echo "ComfyUI parado (VRAM liberada)"
fi

if [ ! -s "$FONDO" ]; then
  echo "el fondo no existe o está vacío"
  avisar "Ficha del día: el fondo SDXL no se generó. Queda pendiente."
  exit 1
fi
python3 -c "
from PIL import Image, ImageStat
im = Image.open('$FONDO'); print('fondo', im.size, im.mode)
print('brillo medio', round(ImageStat.Stat(im.convert('L')).mean[0],1))
"

# 3) render final: dos pasadas, deben dar el mismo sha256
google-chrome --headless --disable-gpu --virtual-time-budget=10000 --screenshot="$R1" --window-size=1080,1350 --hide-scrollbars "file://$HTML" >/dev/null 2>&1
google-chrome --headless --disable-gpu --virtual-time-budget=10000 --screenshot="$R2" --window-size=1080,1350 --hide-scrollbars "file://$HTML" >/dev/null 2>&1
sha256sum "$R1" "$R2"
if [ "$(sha256sum "$R1" | cut -d' ' -f1)" != "$(sha256sum "$R2" | cut -d' ' -f1)" ]; then
  echo "AVISO: los dos renders no coinciden (fuentes); se usa el segundo"
  cp "$R2" "$PNG"
else
  cp "$R1" "$PNG"
fi
ls -la "$PNG"

# 4) puerta de calidad
GATE="$(python3 /home/jokoalmi/joko-lab/tools/validar_ficha_preenvio.py "$HTML" 2>&1)"
echo "$GATE" | tail -14
if echo "$GATE" | grep -q "\[FALTA\]"; then
  echo "PUERTA NO PASA: no se envía"
  avisar "Ficha del día: la puerta de calidad no pasa, no la he enviado. Lo reviso contigo."
  exit 2
fi
python3 -c "
from PIL import Image
print('render final', Image.open('$PNG').size)
"

# 5) envío al canal
SALUDO="$(python3 /home/jokoalmi/joko-lab/tools/saludo_perfume.py --perfume '7 Plata' --nota 'menta Nanah y mandarina' --clima 26)"
echo "saludo: $SALUDO"
if [ "$DRY" = "1" ]; then
  echo "[dry] no se envía nada (el resto del flujo ha funcionado)"
  exit 0
fi
/home/jokoalmi/.local/bin/hermes send --to "$CANAL" "$SALUDO MEDIA:$PNG"
rc=$?
echo "/home/jokoalmi/.local/bin/hermes send rc=$rc"
if [ $rc -eq 0 ]; then
  date '+%F %T' > "$MARK"
  echo "ENVIADA"
else
  avisar "Ficha del día: el render está listo pero el envío al canal falló (rc=$rc)."
fi
echo "=== $(date '+%F %T') fin ==="
