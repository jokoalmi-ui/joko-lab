#!/bin/bash
# crear_video_explicativo.sh — Genera un vídeo MP4 a partir de slides (PNG) + narración TTS
#
# Pipeline: slides HTML → PNG (Chrome headless, opcional) → audio por slide (edge-tts) → MP4 (ffmpeg)
#
# Uso:
#   bash crear_video_explicativo.sh <dir_slides> <dir_salida> [voz]
#
#   <dir_slides> : carpeta con slide_01.html / slide_01.png + slide_01.txt (narración)
#   <dir_salida> : donde se guarda el MP4 final
#   [voz]        : voz edge-tts (default: es-ES-ElviraNeural)
#
# Requisitos: google-chrome/chromium (solo si hay HTML), edge-tts (venv Hermes), ffmpeg, ffprobe
set -euo pipefail

# ── Codec de vídeo: NVENC si hay VRAM libre (≥4 GB), si no libx264 (CPU) ──
# NVENC necesita crear un contexto CUDA: con GLM cargado (~9.7 GB de 12 GB) FALLA
# con CUDA_ERROR_OUT_OF_MEMORY (validado 17-ago-2026). Detección por VRAM libre.
elegir_codec() {
  local vram_mb
  vram_mb=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1 || echo 0)
  if [ -n "$vram_mb" ] && [ "$vram_mb" -ge 4000 ] 2>/dev/null; then
    echo "-c:v h264_nvenc -preset p4 -cq 20"
  else
    echo "-c:v libx264 -preset medium -crf 23"
  fi
}
CODEC_VIDEO=$(elegir_codec)
echo "🎬 Codec vídeo: $CODEC_VIDEO"

DIR_SLIDES="${1:-}"
DIR_SALIDA="${2:-}"
VOZ="${3:-es-ES-ElviraNeural}"

if [ -z "$DIR_SLIDES" ] || [ -z "$DIR_SALIDA" ]; then
  echo "Uso: bash crear_video_explicativo.sh <dir_slides> <dir_salida> [voz]"
  exit 1
fi

mkdir -p "$DIR_SALIDA"
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

EDGE_TTS="$HOME/.hermes/hermes-agent/venv/bin/edge-tts"
CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null || echo "")

echo "=== 1. DETECTAR/RENDERIZAR SLIDES ==="
PNGS=()
# PNG directos
if ls "$DIR_SLIDES"/slide_*.png >/dev/null 2>&1; then
  echo "Usando PNG existentes"
  for f in "$DIR_SLIDES"/slide_*.png; do PNGS+=("$f"); done
else
  # HTML → PNG
  if [ -z "$CHROME" ]; then
    echo "ERROR: no hay PNG ni Chrome para renderizar HTML"
    exit 1
  fi
  echo "Renderizando HTML → PNG (Chrome headless)"
  for h in "$DIR_SLIDES"/slide_*.html; do
    [ -f "$h" ] || continue
    base=$(basename "$h" .html)
    "$CHROME" --headless --disable-gpu --virtual-time-budget=10000 \
      --screenshot="$WORKDIR/$base.png" \
      --window-size=1000,1260 --hide-scrollbars \
      "file://$(realpath "$h")" 2>/dev/null || true
    [ -f "$WORKDIR/$base.png" ] && PNGS+=("$WORKDIR/$base.png")
  done
fi

if [ ${#PNGS[@]} -eq 0 ]; then
  echo "ERROR: no se encontraron slides (slide_*.png o slide_*.html en $DIR_SLIDES)"
  exit 1
fi

mapfile -t PNGS < <(printf '%s\n' "${PNGS[@]}" | sort -V)
echo "Slides: ${#PNGS[@]}"

echo ""
echo "=== 2. AUDIO POR SLIDE (edge-tts) ==="
CONCAT_AUDIO="$WORKDIR/concat_audio.txt"
CONCAT_VIDEO="$WORKDIR/concat_video.txt"
: > "$CONCAT_AUDIO"
: > "$CONCAT_VIDEO"

for png in "${PNGS[@]}"; do
  base=$(basename "$png" .png)
  txt="$DIR_SLIDES/$base.txt"
  audio="$WORKDIR/$base.mp3"

  if [ -f "$txt" ] && [ -s "$txt" ]; then
    echo "  🎙 $base.txt → $base.mp3"
    "$EDGE_TTS" --voice "$VOZ" --text "$(cat "$txt")" --write-media "$audio" 2>/dev/null || true
  fi

  # Si no hay audio válido → silencio 3s
  if [ ! -f "$audio" ] || [ ! -s "$audio" ]; then
    echo "  ⚠️ $base: sin narración → silencio 3s"
    ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 3 -q:a 9 "$audio" 2>/dev/null
  fi

  DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio" 2>/dev/null || echo 3)
  DUR=$(python3 -c "import sys; d=max(float(sys.argv[1]),2.0)+0.8; print(f'{d:.2f}')" "$DUR")

  echo "file '$(realpath "$audio")'" >> "$CONCAT_AUDIO"
  echo "file '$(realpath "$png")'" >> "$CONCAT_VIDEO"
  echo "duration $DUR" >> "$CONCAT_VIDEO"
done
# El concat demuxer de vídeo necesita una última línea duplicada
echo "file '$(realpath "${PNGS[-1]}")'" >> "$CONCAT_VIDEO"

echo ""
echo "=== 3. AUDIO TOTAL ==="
AUDIO_FINAL="$WORKDIR/audio_total.mp3"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_AUDIO" -c copy "$AUDIO_FINAL" 2>/dev/null
echo "Audio: $AUDIO_FINAL ($(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FINAL" 2>/dev/null)s)"

echo ""
echo "=== 4. VÍDEO (PNG secuenciales con duración por slide) ==="
VIDEO_FINAL="$WORKDIR/video_sin_audio.mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_VIDEO" \
  -vf "scale=1080:1350:force_original_aspect_ratio=decrease,pad=1080:1350:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25,format=yuv420p" \
  $CODEC_VIDEO "$VIDEO_FINAL" 2>/dev/null || {
    echo "❌ ffmpeg vídeo falló (¿PNG con tamaños distintos o codec?) — reintento sin escala fija con libx264"
    ffmpeg -y -f concat -safe 0 -i "$CONCAT_VIDEO" -vf "fps=25,format=yuv420p" -c:v libx264 -preset medium -crf 23 "$VIDEO_FINAL" 2>/dev/null || exit 1
  }
echo "Vídeo: $VIDEO_FINAL"

echo ""
echo "=== 5. MUX FINAL ==="
OUT="$DIR_SALIDA/video_explicativo_$(date +%Y%m%d_%H%M).mp4"
ffmpeg -y -i "$VIDEO_FINAL" -i "$AUDIO_FINAL" -c:v copy -c:a aac -shortest "$OUT" 2>/dev/null

if [ -f "$OUT" ] && [ -s "$OUT" ]; then
  echo ""
  echo "✅ VÍDEO CREADO: $OUT"
  echo "   Duración: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT" 2>/dev/null)s"
  ls -lh "$OUT"
else
  echo "❌ Fallo al crear el vídeo"
  exit 1
fi
