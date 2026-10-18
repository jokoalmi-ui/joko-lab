#!/usr/bin/env python3
"""analizar_youtube_completo.py — Análisis COMPLETO de un vídeo de YouTube.

MEJORA 13-ago-2026: el análisis de YouTube era SOLO texto. Los tutoriales de
código muestran comandos/flags en la PANTALLA que el audio no captura.
Flujo:
1. Intentar transcript oficial (fetch_transcript.py)
2. Si falla (429): descargar audio con yt-dlp + whisper local (fallback)
3. Descargar el VÍDEO (baja calidad) y extraer frames inteligentes
4. Salida: transcripción (texto) + frames (para análisis visual)

USO:
    python3 analizar_youtube_completo.py <video_id> [idioma] [dir_salida]
    python3 analizar_youtube_completo.py FMuUEe-QWXg es /tmp/yt_analisis
"""
import sys
import os
import subprocess
import tempfile
import shutil

VENV_PY = "/home/jokoalmi/.hermes/hermes-agent/venv/bin/python3"
TOOLS = "/home/jokoalmi/joko-lab/tools"
SKILL_SCRIPT = "/home/jokoalmi/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py"
NVIDIA_LIB = os.path.expanduser(
    "~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib"
)


def transcript_oficial(url: str, idioma: str) -> str | None:
    """Intenta el transcript oficial. None si falla (429)."""
    try:
        proc = subprocess.run(
            [VENV_PY, SKILL_SCRIPT, url, "--text-only", "--timestamps", "--language", idioma],
            capture_output=True, text=True, timeout=90,
        )
        out = proc.stdout.strip()
        if out and "error" not in out.lower() and "No transcript" not in out:
            return out
    except Exception:
        pass
    return None


def descargar(video_id: str, dir_tmp: str) -> tuple[str | None, str | None]:
    """Descarga audio (wav) y vídeo (mp4 baja calidad). Devuelve (mp4, wav)."""
    ytdlp = os.path.join(os.path.dirname(VENV_PY), "yt-dlp")
    url = f"https://www.youtube.com/watch?v={video_id}"
    mp4, wav = None, None

    # Audio
    try:
        subprocess.run(
            [ytdlp, "-x", "--audio-format", "wav", "--audio-quality", "0",
             "-o", os.path.join(dir_tmp, "audio.%(ext)s"), url],
            check=True, capture_output=True, text=True, timeout=300,
        )
        wav = next((os.path.join(dir_tmp, f) for f in os.listdir(dir_tmp) if f.endswith(".wav")), None)
    except Exception:
        pass

    # Vídeo (baja calidad para frames)
    try:
        subprocess.run(
            [ytdlp, "-f", "worst[ext=mp4]/worst", "-o", os.path.join(dir_tmp, "video.%(ext)s"), url],
            check=True, capture_output=True, text=True, timeout=300,
        )
        mp4 = next((os.path.join(dir_tmp, f) for f in os.listdir(dir_tmp)
                    if f.startswith("video") and f.endswith((".mp4", ".webm"))), None)
    except Exception:
        pass

    return mp4, wav


def transcribir_local(wav: str, idioma: str) -> str:
    """Transcribe el wav con whisper small (GPU) via el wrapper."""
    # Usar el wrapper (que exporta LD_LIBRARY_PATH correctamente)
    proc = subprocess.run(
        [os.path.join(TOOLS, "transcribir_reel.sh"), wav, idioma],
        capture_output=True, text=True, timeout=600,
    )
    txt = wav.rsplit(".", 1)[0] + "_transcripcion.txt"
    if os.path.exists(txt):
        return open(txt, encoding="utf-8").read()
    return proc.stdout


def main():
    if len(sys.argv) < 2:
        print("Uso: analizar_youtube_completo.py <video_id> [idioma] [dir_salida]")
        sys.exit(1)

    video_id = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else "es"
    dir_salida = sys.argv[3] if len(sys.argv) > 3 else f"/tmp/yt_{video_id[:8]}"
    os.makedirs(dir_salida, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"

    tmp = tempfile.mkdtemp(prefix="yt_completo_")
    try:
        print(f"📺 Analizando completo: {url}")
        print(f"   1/3 Transcript oficial...", flush=True)
        texto = transcript_oficial(url, idioma)
        fuente = "oficial"
        if texto:
            print(f"      → OK ({len(texto)} chars)")
        else:
            print(f"      → falló. Descargando + whisper local...", flush=True)
            mp4, wav = descargar(video_id, tmp)
            if wav:
                texto = transcribir_local(wav, idioma)
                fuente = "whisper local"
                print(f"      → OK ({len(texto)} chars)")
            else:
                print(f"      → sin audio descargable")
                mp4 = None

        # Descargar vídeo para frames (si no se descargó ya)
        mp4_ya = next((os.path.join(tmp, f) for f in os.listdir(tmp)
                       if f.startswith("video") and f.endswith((".mp4", ".webm"))), None)
        if not mp4_ya:
            mp4_ya, _ = descargar(video_id, tmp)

        print(f"   2/3 Frames inteligentes...", flush=True)
        if mp4_ya:
            subprocess.run(
                [VENV_PY, os.path.join(TOOLS, "extraer_frames_escenas.py"),
                 mp4_ya, dir_salida, "10"],
                capture_output=True, text=True, timeout=180,
            )
            print(f"      → frames en {dir_salida}")
        else:
            print(f"      → vídeo no disponible")

        print(f"   3/3 Guardando transcripción...")
        if texto:
            with open(os.path.join(dir_salida, "transcripcion.txt"), "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"      → {os.path.join(dir_salida, 'transcripcion.txt')} ({fuente})")

        print(f"\n=== TRANSCRIPCIÓN ({fuente}) — {len(texto or '')} chars ===")
        print((texto or "NO DISPONIBLE")[:1500])
        if texto and len(texto) > 1500:
            print(f"\n... ({len(texto) - 1500} chars más en el archivo)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
