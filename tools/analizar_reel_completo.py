#!/usr/bin/env python3
"""analizar_reel_completo.py — Análisis COMPLETO de un reel/vídeo local.

MEJORA 13-ago-2026 (integra el flujo que antes era manual):
1. Extrae frames INTELIGENTES (scdet — cambios de escena)
2. Transcribe el AUDIO (faster-whisper GPU)
3. Analiza los frames con GLM (como analizar_carrusel_rapido.py)
4. Une transcripción + análisis visual en una salida única

USO:
    python3 analizar_reel_completo.py <video.mp4> [idioma] [--max-px 512]

Salida: imprime análisis visual + transcripción. Guarda transcripción al lado.
"""
import sys
import os
import subprocess
import tempfile
import shutil

# LD_LIBRARY_PATH para libcublas (mismo fix que transcribir_reel.sh)
_NVIDIA_LIB = os.path.expanduser(
    "~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib"
)
if os.path.isdir(_NVIDIA_LIB) and _NVIDIA_LIB not in os.environ.get("LD_LIBRARY_PATH", ""):
    _actual = os.environ.get("LD_LIBRARY_PATH", "")
    os.environ["LD_LIBRARY_PATH"] = _NVIDIA_LIB + (os.pathsep + _actual if _actual else "")

TOOLS = "/home/jokoalmi/joko-lab/tools"


def frames_inteligentes(video: str, dir_salida: str, max_frames: int = 12):
    """Reutiliza extraer_frames_escenas.py."""
    subprocess.run(
        [sys.executable, os.path.join(TOOLS, "extraer_frames_escenas.py"),
         video, dir_salida, str(max_frames)],
        check=True, capture_output=True,
    )


def tiene_audio(video: str) -> bool:
    """Comprueba si el vídeo tiene pista de audio (ffprobe). Fix 19-ago-2026:
    los reels de infografía animada son solo h264 sin audio → ffmpeg fallaba
    con exit 234 y el pipeline moría ANTES de analizar los frames."""
    try:
        proc = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", video],
            capture_output=True, text=True,
        )
        return bool(proc.stdout.strip())
    except Exception:
        return True  # ante la duda, intentar transcribir


def transcribir(video: str, idioma: str | None) -> str:
    """Reutiliza la lógica de transcripción (faster-whisper GPU, CPU si no cabe)."""
    from faster_whisper import WhisperModel

    wav = tempfile.mktemp(suffix=".wav", prefix="whisper_")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav],
            check=True, capture_output=True,
        )
        # Detectar VRAM libre: si GLM u otro modelo grande está cargado, usar CPU
        import urllib.request, json
        vram_libre = 0
        try:
            with urllib.request.urlopen("http://localhost:1234/api/v0/models", timeout=3) as r:
                d = json.loads(r.read())
            cargados = [m for m in d.get("data", []) if m.get("state") == "loaded"]
            # Si hay cualquier modelo grande cargado, usar CPU (whisper small no cabe)
            usar_gpu = len(cargados) == 0
        except Exception:
            usar_gpu = True

        if usar_gpu:
            print("⏳ Whisper small en GPU...", flush=True)
            model = WhisperModel("small", device="cuda", compute_type="float16")
        else:
            print("⏳ Whisper small en CPU (GLM cargado — no cabe en VRAM)...", flush=True)
            model = WhisperModel("small", device="cpu", compute_type="int8")

        kwargs = {"language": idioma} if idioma else {}
        segments, _ = model.transcribe(wav, beam_size=5, **kwargs)
        return " ".join(s.text.strip() for s in segments)
    finally:
        if os.path.exists(wav):
            os.remove(wav)


def analizar_frames(dir_frames: str, max_px: int) -> str:
    """Reutiliza analizar_carrusel_rapido.py (GLM sobre los frames)."""
    proc = subprocess.run(
        [sys.executable, os.path.join(TOOLS, "analizar_carrusel_rapido.py"),
         dir_frames, "--max_px", str(max_px)],
        capture_output=True, text=True,
    )
    return proc.stdout


def main():
    if len(sys.argv) < 2:
        print("Uso: analizar_reel_completo.py <video.mp4> [idioma] [--max-px 512]")
        sys.exit(1)

    video = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    max_px = 512
    for i, a in enumerate(sys.argv):
        if a == "--max-px" and i + 1 < len(sys.argv):
            max_px = int(sys.argv[i + 1])

    if not os.path.exists(video):
        print(f"❌ No existe: {video}")
        sys.exit(1)

    tmp = tempfile.mkdtemp(prefix="reel_analisis_")
    try:
        print(f"📼 Analizando completo: {video}")
        print(f"   1/3 Frames inteligentes...")
        frames_inteligentes(video, os.path.join(tmp, "frames"))
        if tiene_audio(video):
            print(f"   2/3 Transcribiendo audio...")
            texto = transcribir(video, idioma)
            print(f"      → {len(texto)} chars")
        else:
            print(f"   2/3 ⚠️ Sin pista de audio — salto transcripción (fix 19-ago-2026)")
            texto = ""
        print(f"   3/3 Analizando frames con GLM...")
        analisis = analizar_frames(os.path.join(tmp, "frames"), max_px)

        # Salida combinada
        print("\n" + "=" * 60)
        print("🎬 ANÁLISIS VISUAL (GLM sobre frames)")
        print("=" * 60)
        print(analisis)
        print("\n" + "=" * 60)
        print("🎧 TRANSCRIPCIÓN DEL AUDIO")
        print("=" * 60)
        print(texto if texto.strip() else "(sin voz detectable)")

        # Guardar transcripción al lado del vídeo
        salida = video.rsplit(".", 1)[0] + "_transcripcion.txt"
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"\n✅ Transcripción guardada: {salida}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
