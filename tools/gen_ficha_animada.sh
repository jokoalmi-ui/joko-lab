#!/usr/bin/env bash
# =============================================================================
# gen_ficha_animada.sh — Convierte la ficha del perfume del día en vídeo animado
# (21-ago-2026, validado con POC v6: figura del frasco recortada → despegue → crece → desaparece)
#
# FLUJO: HTML de la ficha (sin frasco) → base PNG · recorte figura frasco (PIL)
#        → 180 frames (despegue) → ffmpeg → edge-tts → MP4 vertical
# TODO LOCAL, 0 €, sin instalar nada.
#
# USO:
#   bash gen_ficha_animada.sh \
#     --html /ruta/ficha.html \
#     --frasco /ruta/frasco_original.png \
#     --narracion "Adonis Awakens. La figura del frasco." \
#     --out /tmp/ficha_animada
#
# REQUISITOS: Chrome headless (render), ffmpeg, edge-tts, PIL, GLM opcional (verificar)
# PITFALLS validados:
#   - putalpha(255) global → opaca TODO el canvas del frasco (borde negro) → usar
#     multiplicación del alpha original por el factor
#   - colorkey deja cuadro → recorte por distancia al blanco (PIL, rampa suave)
#   - posición del frasco en la ficha (hero): verificar con browser_console
#     getBoundingClientRect (por defecto x=44 y=265 w=240 en formato v4)
# =============================================================================
set -euo pipefail

HTML=""
FRASCO=""
NARRACION=""
OUT="/tmp/ficha_animada"
VOZ="es-ES-ElviraNeural"
# Posición del frasco en la ficha (lienzo 3:4 1080x1440, plantilla v5;
# medido con getBoundingClientRect el 17-oct-2026: x54 y121 w296)
FX=54; FY=121; FW_ORIG=296
# Animación
FPS=30; DUR=6.0
FINAL_H=950

while [[ $# -gt 0 ]]; do
  case "$1" in
    --html)      HTML="$2"; shift 2 ;;
    --frasco)    FRASCO="$2"; shift 2 ;;
    --narracion) NARRACION="$2"; shift 2 ;;
    --out)       OUT="$2"; shift 2 ;;
    --voz)       VOZ="$2"; shift 2 ;;
    --fx)        FX="$2"; shift 2 ;;
    --fy)        FY="$2"; shift 2 ;;
    *) echo "❌ Argumento desconocido: $1"; exit 1 ;;
  esac
done

if [[ -z "$HTML" || -z "$FRASCO" || -z "$NARRACION" ]]; then
  echo "❌ Faltan: --html, --frasco y --narracion son obligatorios"
  exit 1
fi

mkdir -p "$OUT"
echo "==========================================================="
echo " 🎬 gen_ficha_animada.sh"
echo " HTML:    $HTML"
echo " Frasco:  $FRASCO"
echo " Salida:  $OUT"
echo "==========================================================="

# --- 0. Comprobar herramientas ------------------------------------------------
echo "[0/6] Comprobando herramientas..."
# RULE-021: el PATH no interactivo no trae el venv de edge-tts; resolverlo aquí.
if ! command -v edge-tts >/dev/null 2>&1 && [ -x "$HOME/edge-tts-env/bin/edge-tts" ]; then
  export PATH="$HOME/edge-tts-env/bin:$PATH"
fi
command -v ffmpeg >/dev/null || { echo "❌ ffmpeg no está"; exit 1; }
command -v edge-tts >/dev/null || { echo "❌ edge-tts no está"; exit 1; }
# RULE-021: el `python3` del PATH puede ser el de Hermes (sin PIL) → usar uno con PIL.
if /usr/bin/python3 -c "import PIL" 2>/dev/null; then
  PY=/usr/bin/python3
elif python3 -c "import PIL" 2>/dev/null; then
  PY=python3
else
  echo "❌ PIL no está"; exit 1
fi
echo "      OK"

# --- 1. Base de la ficha SIN el frasco ----------------------------------------
echo "[1/6] Renderizando ficha sin frasco..."
sed 's/class="frasco"/class="frasco" style="display:none"/' "$HTML" > "$OUT/ficha_sin_frasco.html"
google-chrome --headless --disable-gpu --virtual-time-budget=10000 \
  --screenshot="$OUT/base_sin_frasco.png" --window-size=1080,1440 --hide-scrollbars \
  "file://$OUT/ficha_sin_frasco.html" >/dev/null 2>&1
"$PY" -c "
from PIL import Image
im = Image.open('$OUT/base_sin_frasco.png')
assert im.size == (1080, 1440), f'tamaño inesperado: {im.size}'
print('      base OK (1080x1440)')
"

# --- 2. Recortar la FIGURA del frasco (PIL, distancia al blanco) --------------
echo "[2/6] Recortando figura del frasco..."
"$PY" - "$FRASCO" "$OUT/frasco_figura.png" << 'PYEOF'
import sys, math
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
w, h = im.size
px = im.load()
out = Image.new("RGBA", (w, h))
opx = out.load()
UMB_OP = 40   # distancia < 40 → transparente
UMB_FULL = 110  # distancia > 110 → opaco
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        d = math.sqrt((r-255)**2 + (g-255)**2 + (b-255)**2)
        if d <= UMB_OP:
            a = 0
        elif d >= UMB_FULL:
            a = 255
        else:
            a = int(255 * (d - UMB_OP) / (UMB_FULL - UMB_OP))
        opx[x, y] = (r, g, b, a)
bbox = out.getchannel('A').getbbox()
out = out.crop(bbox)
out.putalpha(out.getchannel('A').filter(ImageFilter.GaussianBlur(1.2)))
out.save(dst)
print(f"      figura OK ({dst}, bbox {bbox})")
PYEOF

# --- 3. Generar frames (despegue: sitio → crece → desaparece) -----------------
echo "[3/6] Generando frames..."
"$PY" - "$OUT" "$FX" "$FY" "$FW_ORIG" "$FINAL_H" "$FPS" "$DUR" << 'PYEOF'
import sys, os
from PIL import Image

outdir, fx, fy, fw_orig, final_h, fps, dur = sys.argv[1:8]
fx, fy, fw_orig = int(fx), int(fy), int(fw_orig)
final_h = int(final_h); fps = int(fps); dur = float(dur)

ficha = Image.open(f"{outdir}/base_sin_frasco.png").convert("RGBA")
fig = Image.open(f"{outdir}/frasco_figura.png").convert("RGBA")
FW, FH = fig.size
W, H = ficha.size
N = int(fps * dur)
FR = f"{outdir}/frames"
os.makedirs(FR, exist_ok=True)

ORIG_W = int(fw_orig * 0.62)   # figura estrecha → ancho ~62% del hueco cuadrado
ORIG_X = fx + fw_orig // 2
ORIG_Y = fy
FINAL_W = int(final_h * FW / FH)
FINAL_X = W // 2
FINAL_Y = 150

for i in range(N):
    t = i / fps
    frame = ficha.copy()
    if t < 1.2:
        alpha_f = t / 1.2
        w = ORIG_W
        x = ORIG_X - w // 2
        y = ORIG_Y
    elif t < 4.5:
        k = (t - 1.2) / 3.3
        k = k * k * (3 - 2 * k)
        w = ORIG_W + (FINAL_W - ORIG_W) * k
        x = (ORIG_X - w // 2) + (FINAL_X - w // 2 - (ORIG_X - w // 2)) * k
        y = ORIG_Y + (FINAL_Y - ORIG_Y) * k
        alpha_f = 1.0
    elif t < 5.0:
        w = FINAL_W
        x = FINAL_X - w // 2
        y = FINAL_Y
        alpha_f = 1.0
    else:
        alpha_f = max(0.0, 1.0 - (t - 5.0))
        w = FINAL_W
        x = FINAL_X - w // 2
        y = FINAL_Y

    fr = fig.resize((int(w), int(w * FH / FW)), Image.LANCZOS)
    if alpha_f < 1.0:
        fr.putalpha(fr.getchannel('A').point(lambda p, af=alpha_f: int(p * af)))
    frame.paste(fr, (int(x), int(y)), fr)
    frame.convert("RGB").save(f"{FR}/f_{i:04d}.png", quality=92)
print(f"      frames OK ({N})")
PYEOF

# --- 4. Vídeo sin audio -------------------------------------------------------
echo "[4/6] Creando vídeo..."
ffmpeg -y -v quiet -framerate "$FPS" -i "$OUT/frames/f_%04d.png" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p "$OUT/video_sin_audio.mp4"

# --- 5. Voz + mux ---------------------------------------------------------------
echo "[5/6] Generando voz y mezclando..."
edge-tts --voice "$VOZ" --text "$NARRACION" --write-media "$OUT/narracion.mp3" >/dev/null 2>&1
ffmpeg -y -v quiet -i "$OUT/video_sin_audio.mp4" -i "$OUT/narracion.mp3" \
  -filter_complex "[1:a]adelay=1500|1500,afade=t=in:st=1.5:d=0.3,afade=t=out:st=4.8:d=0.5[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 128k "$OUT/ficha_animada_final.mp4"

# --- 6. Verificación ------------------------------------------------------------
echo "[6/6] Verificando..."
ffmpeg -y -v quiet -i "$OUT/ficha_animada_final.mp4" -vf "fps=1" "$OUT/check_%02d.jpg"
NEGROS=0
for f in "$OUT"/check_*.jpg; do
  BRILLO=$("$PY" -c "from PIL import Image, ImageStat; print(round(ImageStat.Stat(Image.open('$f').convert('L')).mean[0],1))" 2>/dev/null || echo "0")
  if "$PY" -c "exit(0 if float('$BRILLO') < 20 else 1)" 2>/dev/null; then NEGROS=$((NEGROS+1)); fi
done
rm -f "$OUT"/check_*.jpg
DUR_FINAL=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT/ficha_animada_final.mp4")
SIZE=$(du -h "$OUT/ficha_animada_final.mp4" | cut -f1)
echo "==========================================================="
echo " ✅ LISTO: $OUT/ficha_animada_final.mp4"
echo "    ${DUR_FINAL}s · ${SIZE} · 1080x1440"
if [ "$NEGROS" -gt 0 ]; then echo " ⚠️  $NEGROS frames oscuros"; else echo "    Frames verificados ✅"; fi
echo "==========================================================="
