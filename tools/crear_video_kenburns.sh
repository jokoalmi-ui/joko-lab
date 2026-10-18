#!/bin/bash
# crear_video_kenburns.sh — Vídeo dinámico estilo "Memorias de Pez" (Ken Burns + aparición progresiva)
#
# Uso:
#   bash crear_video_kenburns.sh <dir_slides> <dir_salida> [voz]
#
# Convención de slides (una carpeta):
#   slide_05.txt        -> narración del GRUPO 05
#   slide_05a.png/.html -> variante 1 del grupo (aparece primero)
#   slide_05b.png/.html -> variante 2 del grupo (aparece después: efecto "se va dibujando")
#   slide_06.png/.html  -> grupo sin variantes (una sola imagen)
#
# El audio de cada grupo se reparte a partes iguales entre sus variantes.
# Cada variante recibe un movimiento de cámara (zoom-in / zoom-out / paneo) alternado.
set -euo pipefail

# ── Codec de vídeo: NVENC si hay VRAM libre (≥4 GB), si no libx264 (CPU) ──
# NVENC necesita crear un contexto CUDA: con GLM cargado (~9.7 GB de 12 GB) FALLA
# con CUDA_ERROR_OUT_OF_MEMORY (validado 17-ago-2026). La detección por VRAM
# libre evita reintentar NVENC inútilmente cuando el montaje va a fallar.
elegir_codec() {
  local vram_mb
  vram_mb=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1 || echo 0)
  if [ -n "$vram_mb" ] && [ "$vram_mb" -ge 4000 ] 2>/dev/null; then
    echo "-c:v h264_nvenc -preset p4 -cq 20"
  else
    echo "-c:v libx264 -preset medium -crf 20"
  fi
}
CODEC_VIDEO=$(elegir_codec)
echo "🎬 Codec vídeo: $CODEC_VIDEO"

DIR_SLIDES="${1:-}"
DIR_SALIDA="${2:-}"
VOZ="${3:-es-ES-ElviraNeural}"

if [ -z "$DIR_SLIDES" ] || [ -z "$DIR_SALIDA" ]; then
  echo "Uso: bash crear_video_kenburns.sh <dir_slides> <dir_salida> [voz]"
  exit 1
fi

mkdir -p "$DIR_SALIDA"
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

EDGE_TTS="$HOME/.hermes/hermes-agent/venv/bin/edge-tts"
if [ ! -x "$EDGE_TTS" ]; then EDGE_TTS="$(which edge-tts 2>/dev/null || echo '')"; fi
[ -z "$EDGE_TTS" ] && { echo "ERROR: edge-tts no encontrado"; exit 1; }

# 1. Grupos = slide_XX.txt ordenados
mapfile -t TXTS < <(ls "$DIR_SLIDES"/slide_*.txt 2>/dev/null | sort -V)
if [ ${#TXTS[@]} -eq 0 ]; then echo "ERROR: no hay slide_*.txt en $DIR_SLIDES"; exit 1; fi

CONCAT_VIDEO="$WORKDIR/concat_video.txt"
CONCAT_AUDIO="$WORKDIR/concat_audio.txt"
: > "$CONCAT_VIDEO"
: > "$CONCAT_AUDIO"
PREV_LAST_PNG=""

echo "=== 1. TTS + Ken Burns por grupo ==="
IDX=0
for txt in "${TXTS[@]}"; do
  base=$(basename "$txt" .txt)        # slide_05
  num=${base#slide_}                  # 05
  audio="$WORKDIR/$base.mp3"
  echo "  🎙 $base.txt → $base.mp3"
  "$EDGE_TTS" --voice "$VOZ" --text "$(cat "$txt")" --write-media "$audio" 2>/dev/null || true
  if [ ! -s "$audio" ]; then
    echo "  ⚠️ $base: sin narración → silencio 3s"
    ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 3 -q:a 9 "$audio" 2>/dev/null
  fi
  DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio" 2>/dev/null || echo 3)
  DUR=$(python3 -c "import sys; print(f'{max(float(sys.argv[1]),2.0):.2f}')" "$DUR")

  mapfile -t PNGS < <(ls "$DIR_SLIDES"/slide_${num}*.png 2>/dev/null | sort -V)
  if [ ${#PNGS[@]} -eq 0 ]; then
    echo "  ⚠️ $base: sin PNG → se renderiza desde HTML (Chrome)"
    for h in "$DIR_SLIDES"/slide_${num}*.html; do
      [ -f "$h" ] || continue
      hb=$(basename "$h" .html)
      google-chrome --headless --disable-gpu --virtual-time-budget=10000 \
        --screenshot="$DIR_SLIDES/$hb.png" \
        --window-size=1824,2310 --hide-scrollbars "file://$(realpath "$h")" 2>/dev/null || true
    done
    mapfile -t PNGS < <(ls "$DIR_SLIDES"/slide_${num}*.png 2>/dev/null | sort -V)
  fi
  [ ${#PNGS[@]} -eq 0 ] && { echo "ERROR: grupo $num sin imágenes"; exit 1; }

  N=${#PNGS[@]}
  DI=$(python3 -c "import sys; print(f'{float(sys.argv[1])/int(sys.argv[2]):.3f}')" "$DUR" "$N")
  echo "  grupo $num: $N variante(s) × ${DI}s"
  # --- PASO DE PÁGINA (page flip) entre grupos ---
  if [ "$IDX" -gt 0 ]; then
    FLIP_MP4="$WORKDIR/flip_${num}.mp4"
    SIL="$WORKDIR/silencio_${num}.mp3"
    # 1.2s de silencio que acompañan al flip (vídeo extra = audio extra)
    ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 1.2 -q:a 9 "$SIL" 2>/dev/null
    echo "file '$(realpath "$SIL")'" >> "$CONCAT_AUDIO"
    # generador: A=última variante del grupo anterior, B=primera variante de este
    python3 "$HOME/joko-lab/tools/gen_flip.py" "$PREV_LAST_PNG" "${PNGS[0]}" "$WORKDIR" "flip_${num}" >/dev/null 2>&1
    if [ -s "$FLIP_MP4" ]; then
      echo "  🔄 flip ${num}: ${PREV_LAST_PNG##*/} -> ${PNGS[0]##*/}"
      echo "file '$(realpath "$FLIP_MP4")'" >> "$CONCAT_VIDEO"
    else
      echo "  ⚠️ flip ${num}: no generado (continúa sin transición)"
    fi
  fi
  echo "file '$(realpath "$audio")'" >> "$CONCAT_AUDIO"

  # --- Clip del grupo: Manim si existe, si no Ken Burns sobre las variantes ---
  if [ -f "$DIR_SLIDES/manim_${num}.mp4" ]; then
    MANIM_SRC="$DIR_SLIDES/manim_${num}.mp4"
    clip_manim="$WORKDIR/clip_${num}_manim.mp4"
    MANIM_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$MANIM_SRC" 2>/dev/null || echo 0)
    AJUSTE=$(python3 -c "import sys; print(f'{max(float(sys.argv[1])-float(sys.argv[2]),0.0):.2f}')" "$DUR" "$MANIM_DUR")
    echo "  🎬 grupo $num: clip Manim (${MANIM_DUR}s + ${AJUSTE}s de cola)"
    ffmpeg -y -i "$MANIM_SRC" -vf "fps=25,scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,tpad=stop_mode=clone:stop_duration=$AJUSTE" \
      -t "$DUR" $CODEC_VIDEO -pix_fmt yuv420p "$clip_manim" 2>/dev/null || exit 1
    echo "file '$(realpath "$clip_manim")'" >> "$CONCAT_VIDEO"
    PREV_LAST_PNG="${PNGS[0]}"
  else
  k=0
  for png in "${PNGS[@]}"; do
    FRAMES=$(python3 -c "import sys; print(max(int(round(float(sys.argv[1])*25)),25))" "$DI")
    case $((k % 3)) in
      0) ZF="z='min(zoom+0.0005,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'" ;;
      1) ZF="z='if(eq(on,1),1.07,max(zoom-0.0005,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'" ;;
      2) ZF="z='min(zoom+0.0004,1.06)':x='(iw-iw/zoom)*on/${FRAMES}':y='ih/2-(ih/zoom/2)'" ;;
    esac
    clip="$WORKDIR/clip_${num}_${k}.mp4"
    # Sin zoompan (feedback 17-ago: el "zoom tembloroso" no gusta): clip estático,
    # solo scale+crop cover para que la hoja 1824x2310 entre en 1080x1350.
    ffmpeg -y -loop 1 -i "$png" \
      -vf "scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,fps=25" \
      -t "$DUR" $CODEC_VIDEO -pix_fmt yuv420p "$clip" 2>/dev/null || exit 1
    echo "file '$(realpath "$clip")'" >> "$CONCAT_VIDEO"
    k=$((k+1)); IDX=$((IDX+1))
  done
  PREV_LAST_PNG="${PNGS[-1]}"
  fi
  done

echo ""
echo "=== 2. Concat + MUX ==="
VIDEO="$WORKDIR/video_sin_audio.mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_VIDEO" -c copy "$VIDEO" 2>/dev/null || exit 1
AUDIO_TOTAL="$WORKDIR/audio_total.mp3"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_AUDIO" -c copy "$AUDIO_TOTAL" 2>/dev/null || exit 1
OUT="$DIR_SALIDA/video_kenburns_$(date +%Y%m%d_%H%M).mp4"
ffmpeg -y -i "$VIDEO" -i "$AUDIO_TOTAL" -c:v copy -c:a aac -shortest "$OUT" 2>/dev/null || exit 1

if [ -f "$OUT" ] && [ -s "$OUT" ]; then
  echo ""
  echo "✅ VÍDEO KEN BURNS CREADO: $OUT"
  echo "   Duración: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT" 2>/dev/null)s"
  ls -lh "$OUT"
else
  echo "❌ Fallo al crear el vídeo"
  exit 1
fi
