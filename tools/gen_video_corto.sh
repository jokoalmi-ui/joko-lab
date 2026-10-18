#!/usr/bin/env bash
# =============================================================================
# gen_video_corto.sh — Genera vídeos cortos tipo reel con tecnología del lab
# (21-ago-2026, validado con POC: 4 escenas SDXL + zoompan + crossfade + edge-tts)
#
# FLUJO: ComfyUI (SDXL) → imágenes → ffmpeg (zoompan/xfade) → edge-tts → MP4
# TODO LOCAL, 0 €, sin instalar nada nuevo.
#
# USO:
#   bash gen_video_corto.sh \
#     --tema "IA local en tu escritorio" \
#     --narracion "Tu IA local, en tu escritorio. Sin nube, sin límites." \
#     --escenas 4 \
#     --out /tmp/mi_video
#
# REQUISITOS: ComfyUI activo (:8188) con sd_xl_base_1.0.safetensors, ffmpeg, edge-tts
# NOTA: este script NO gestiona la VRAM — si LM Studio ocupa la GPU, descargar
# el modelo primero (lms unload) o el render puede fallar por falta de memoria.
# =============================================================================
set -euo pipefail

# --- Parámetros por defecto -------------------------------------------------
TEMA="IA local en tu escritorio"
NARRACION="Tu IA local, en tu escritorio. Sin nube, sin límites. Datos tuyos, modelos tuyos, decisiones tuyas."
ESCENAS=4
OUT="/tmp/video_corto"
VOZ="es-ES-ElviraNeural"
SERVER="http://127.0.0.1:8188"
CHECKPOINT="sd_xl_base_1.0.safetensors"
DUR_ESCENA=3
FPS=30
RES="1920x1080"
SEED=42

# --- Parseo de argumentos ----------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tema)      TEMA="$2"; shift 2 ;;
    --narracion) NARRACION="$2"; shift 2 ;;
    --escenas)   ESCENAS="$2"; shift 2 ;;
    --out)       OUT="$2"; shift 2 ;;
    --voz)       VOZ="$2"; shift 2 ;;
    --seed)      SEED="$2"; shift 2 ;;
    *) echo "❌ Argumento desconocido: $1"; exit 1 ;;
  esac
done

IMG_DIR="$OUT/img"
mkdir -p "$IMG_DIR"

echo "==========================================================="
echo " 🎬 gen_video_corto.sh"
echo " Tema:      $TEMA"
echo " Escenas:   $ESCENAS"
echo " Narración: ${NARRACION:0:60}..."
echo " Salida:    $OUT"
echo "==========================================================="

# --- 0. Comprobar ComfyUI ----------------------------------------------------
echo "[0/5] Comprobando ComfyUI..."
if ! curl -s -m 5 "$SERVER/system_stats" >/dev/null 2>&1; then
  echo "❌ ComfyUI no responde en $SERVER. Arranca: systemctl --user start comfyui"
  exit 1
fi
echo "      ComfyUI OK"

# --- 1. Generar escenas con SDXL ---------------------------------------------
echo "[1/5] Generando $ESCENAS escenas SDXL..."
BASE="soft 3d render, cozy workspace at dusk, warm amber and deep blue palette, clean minimal composition, no text, no words, cinematic lighting, high detail, 16:9"
python3 - "$SERVER" "$CHECKPOINT" "$IMG_DIR" "$BASE" "$TEMA" "$ESCENAS" "$SEED" << 'PYEOF'
import json, urllib.request, time, os, sys, random

server, checkpoint, outdir, base, tema, n, seed = sys.argv[1:8]
n = int(n); seed = int(seed)

VARIACIONES = [
    "a sleek desktop computer with a glowing brain hologram floating above it, neural network connections",
    "a cozy desk with a coffee cup and a small robot assistant, warm lamp light",
    "a glass bookshelf with glowing blue data cubes and a tiny plant, soft bokeh",
    "a wide shot of a peaceful home office at night, city lights through window, holographic charts",
    "a laptop with code glowing on screen and floating particles of light, deep blue ambiance",
    "a hand holding a glowing orb with circuit patterns, amber light, dark background",
]

def queue(prompt):
    req = urllib.request.Request(f"{server}/prompt", data=json.dumps({"prompt": prompt}).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())

def history(pid):
    req = urllib.request.Request(f"{server}/history/{pid}")
    return json.loads(urllib.request.urlopen(req).read())

def workflow(text, s):
    return {
        "3": {"class_type": "KSampler", "inputs": {
            "seed": s, "steps": 22, "cfg": 7.0, "sampler_name": "dpmpp_2m",
            "scheduler": "karras", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
            "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 576, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": text, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "blurry, low quality, text, watermark, jpeg artifacts", "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "vdc_escena", "images": ["8", 0]}},
    }

for i in range(n):
    var = VARIACIONES[i % len(VARIACIONES)]
    text = f"{base}, {var}, {tema}"
    pid = queue(workflow(text, seed + i))["prompt_id"]
    ok = False
    for _ in range(150):
        time.sleep(2)
        hist = history(pid)
        if pid in hist:
            for node_id in hist[pid]["outputs"]:
                for img in hist[pid]["outputs"][node_id].get("images", []):
                    src = f"{server}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
                    dest = f"{outdir}/escena_{i+1:02d}.png"
                    urllib.request.urlretrieve(src, dest)
                    print(f"      escena {i+1}: OK ({os.path.getsize(dest)//1024} KB)")
                    ok = True
            break
    if not ok:
        print(f"⚠️  timeout en escena {i+1}")
print("      Imágenes listas")
PYEOF

# --- 2. Animación (zoompan variado) ------------------------------------------
echo "[2/5] Animando escenas (zoom/pan)..."
D_FRAMES=$((DUR_ESCENA * FPS))
for i in $(seq 1 "$ESCENAS"); do
  case $((i % 4)) in
    1) ZF="zoompan=z='min(zoom+0.0012,1.15)':d=${D_FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${RES}:fps=${FPS}" ;;
    2) ZF="zoompan=z='1.12':d=${D_FRAMES}:x='(iw-iw/zoom)*on/${D_FRAMES}':y='ih/2-(ih/zoom/2)':s=${RES}:fps=${FPS}" ;;
    3) ZF="zoompan=z='max(1.15-0.0012*on,1.0)':d=${D_FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${RES}:fps=${FPS}" ;;
    0) ZF="zoompan=z='1.10':d=${D_FRAMES}:x='iw-(iw/zoom)-(iw-iw/zoom)*on/${D_FRAMES}':y='ih/2-(ih/zoom/2)':s=${RES}:fps=${FPS}" ;;
  esac
  ffmpeg -y -v quiet -loop 1 -i "$IMG_DIR/escena_$(printf '%02d' "$i").png" -vf "$ZF" -t "$DUR_ESCENA" -r "$FPS" "$OUT/escena_$i.mp4"
done
echo "      Animación OK"

# --- 3. Concatenar con crossfade ----------------------------------------------
echo "[3/5] Uniendo escenas (crossfade)..."
DUR_TOTAL=$(echo "$ESCENAS * $DUR_ESCENA - ($ESCENAS - 1) * 0.5" | bc)
FILTER=""
PREV="0:v"
for i in $(seq 2 "$ESCENAS"); do
  IDX=$((i - 1))
  OFFSET=$(echo "$IDX * ($DUR_ESCENA - 0.5)" | bc)
  if [ "$i" -lt "$ESCENAS" ]; then
    FILTER="${FILTER}[${PREV}][$((i-1)):v]xfade=transition=fade:duration=0.5:offset=${OFFSET}[v${IDX}];"
    PREV="v${IDX}"
  else
    FILTER="${FILTER}[${PREV}][$((i-1)):v]xfade=transition=fade:duration=0.5:offset=${OFFSET}[vout]"
  fi
done
INPUTS=""
for i in $(seq 1 "$ESCENAS"); do INPUTS="$INPUTS -i $OUT/escena_$i.mp4"; done
ffmpeg -y -v quiet $INPUTS -filter_complex "$FILTER" -map "[vout]" -r "$FPS" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p "$OUT/video_sin_audio.mp4"
echo "      Conexión OK (${DUR_TOTAL}s)"

# --- 4. Narración edge-tts ----------------------------------------------------
echo "[4/5] Generando voz (edge-tts: $VOZ)..."
edge-tts --voice "$VOZ" --text "$NARRACION" --write-media "$OUT/narracion.mp3" >/dev/null 2>&1
AUD_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT/narracion.mp3")
echo "      Narración OK (${AUD_DUR}s)"

# --- 5. Mezclar audio + verificar ---------------------------------------------
echo "[5/5] Mezclando audio y verificando..."
ffmpeg -y -v quiet -i "$OUT/video_sin_audio.mp4" -i "$OUT/narracion.mp3" \
  -filter_complex "[1:a]afade=t=out:st=$(echo "$AUD_DUR - 0.5" | bc):d=0.5[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 128k -shortest \
  "$OUT/video_final.mp4"

# Verificación: frames no negros
ffmpeg -y -v quiet -i "$OUT/video_final.mp4" -vf "fps=1" "$OUT/check_%02d.jpg"
NEGROS=0
for f in "$OUT"/check_*.jpg; do
  BRILLO=$(python3 -c "from PIL import Image, ImageStat; print(round(ImageStat.Stat(Image.open('$f').convert('L')).mean[0],1))" 2>/dev/null || echo "0")
  if python3 -c "exit(0 if float('$BRILLO') < 20 else 1)"; then NEGROS=$((NEGROS+1)); fi
done
rm -f "$OUT"/check_*.jpg

DUR_FINAL=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT/video_final.mp4")
SIZE=$(du -h "$OUT/video_final.mp4" | cut -f1)

echo "==========================================================="
echo " ✅ VÍDEO LISTO: $OUT/video_final.mp4"
echo "    Duración: ${DUR_FINAL}s · Tamaño: ${SIZE} · ${RES}"
if [ "$NEGROS" -gt 0 ]; then
  echo " ⚠️  $NEGROS frames con brillo <20 (posible negro)"
else
  echo "    Frames verificados: sin negros ✅"
fi
echo "==========================================================="
