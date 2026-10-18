#!/usr/bin/env python3
"""extraer_audio_y_transcribir.py — Transcribe el audio de un vídeo/reel con faster-whisper.

SALTO DE CALIDAD 13-ago-2026: los reels de IG tienen AUDIO (voz explicando)
que el analizador de carruseles NO capturaba (solo frames visuales). Este
script extrae el audio (ffmpeg) y lo transcribe con faster-whisper (GPU,
modelo base ~142MB ya instalado en el sistema).

USO:
    python3 extraer_audio_y_transcribir.py <video.mp4> [idioma]
    python3 extraer_audio_y_transcribir.py /tmp/reel_tools/reel.mp4 es

Salida: imprime la transcripción + guarda en <video>.txt al lado.
"""
import sys
import os
import subprocess
import tempfile

# ⚠️ CUDA 12 wheels (nvidia-cublas-cu12) no se auto-cargan en CTranslate2:
# hay que añadir el directorio de la lib al LD_LIBRARY_PATH. Se usa os.environ
# DIRECTAMENTE (no setdefault) porque CTranslate2 lee el path al importar
# faster_whisper (que ocurre dentro de transcribir(), después de esto).
_NVIDIA_LIB = os.path.expanduser(
    "~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib"
)
if os.path.isdir(_NVIDIA_LIB):
    _actual = os.environ.get("LD_LIBRARY_PATH", "")
    if _NVIDIA_LIB not in _actual:
        os.environ["LD_LIBRARY_PATH"] = _NVIDIA_LIB + (os.pathsep + _actual if _actual else "")


def extraer_audio(video: str) -> str:
    """Extrae el audio a WAV mono 16kHz (lo que espera whisper)."""
    wav = tempfile.mktemp(suffix=".wav", prefix="whisper_")
    # 16kHz mono = óptimo para whisper (rápido, suficiente)
    subprocess.run(
        ["ffmpeg", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav],
        check=True,
        capture_output=True,
    )
    return wav


def transcribir(wav: str, idioma: str | None = None, device: str = "auto") -> str:
    """Transcribe con faster-whisper (modelo small).

    device: "auto" (detecta VRAM libre → GPU o CPU), "cuda" (fuerza GPU) o "cpu".
    - Si hay ≥3 GB de VRAM libre → GPU (float16, rápido)
    - Si no → CPU (int8, más lento pero NUNCA falla con CUDA OOM)
    """
    from faster_whisper import WhisperModel

    if device == "auto":
        try:
            import subprocess
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5,
            ).stdout.strip()
            vram_mb = int(out.splitlines()[0]) if out else 0
            device = "cuda" if vram_mb >= 3000 else "cpu"
        except Exception:
            device = "cpu"

    if device == "cuda":
        print("⏳ Cargando modelo Whisper small en GPU...", flush=True)
        model = WhisperModel("small", device="cuda", compute_type="float16")
    else:
        print("⏳ Cargando modelo Whisper small en CPU (VRAM insuficiente)...", flush=True)
        model = WhisperModel("small", device="cpu", compute_type="int8")

    kwargs = {}
    if idioma:
        kwargs["language"] = idioma

    print("🎧 Transcribiendo...", flush=True)
    segments, info = model.transcribe(wav, beam_size=5, **kwargs)

    partes = []
    for seg in segments:
        partes.append(seg.text.strip())

    texto = " ".join(partes)
    return texto


def main():
    if len(sys.argv) < 2:
        print("Uso: extraer_audio_y_transcribir.py <video.mp4> [idioma] [auto|cuda|cpu]")
        sys.exit(1)

    video = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else None
    device = sys.argv[3] if len(sys.argv) > 3 else "auto"

    if not os.path.exists(video):
        print(f"❌ No existe: {video}")
        sys.exit(1)

    print(f"📼 Vídeo: {video}")

    wav = extraer_audio(video)
    try:
        texto = transcribir(wav, idioma, device)
        # Guardar junto al vídeo
        salida = video.rsplit(".", 1)[0] + "_transcripcion.txt"
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"\n✅ Transcripción guardada: {salida}")
        print(f"📝 Longitud: {len(texto)} chars")
        print(f"\n=== TRANSCRIPCIÓN ===")
        print(texto[:3000])
        if len(texto) > 3000:
            print(f"\n... ({len(texto) - 3000} chars más en el archivo)")
    finally:
        # Limpiar WAV temporal
        if os.path.exists(wav):
            os.remove(wav)


if __name__ == "__main__":
    main()
