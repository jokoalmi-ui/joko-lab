#!/usr/bin/env python3
"""transcribir_youtube_fallback.py — Transcripción de vídeo de YouTube con fallback local.

MEJORA 13-ago-2026: cuando YouTube bloquea el transcript oficial (rate-limit
429, problema recurrente del lab), en vez de esperar 24h se descarga el audio
con yt-dlp y se transcribe LOCALMENTE con faster-whisper. 100% independiente
del rate-limit de YouTube.

USO:
    python3 transcribir_youtube_fallback.py <video_id_o_url> [idioma]
    python3 transcribir_youtube_fallback.py FMuUEe-QWXg es
"""
import sys
import os
import subprocess
import tempfile

# LD_LIBRARY_PATH para libcublas (mismo fix)
_NVIDIA_LIB = os.path.expanduser(
    "~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib"
)
if os.path.isdir(_NVIDIA_LIB) and _NVIDIA_LIB not in os.environ.get("LD_LIBRARY_PATH", ""):
    _actual = os.environ.get("LD_LIBRARY_PATH", "")
    os.environ["LD_LIBRARY_PATH"] = _NVIDIA_LIB + (os.pathsep + _actual if _actual else "")

VENV_PY = "/home/jokoalmi/.hermes/hermes-agent/venv/bin/python3"


def descargar_audio(url: str, dir_tmp: str) -> str:
    """Descarga el audio (m4a) del vídeo con yt-dlp."""
    cmd = [
        os.path.join(os.path.dirname(VENV_PY), "yt-dlp"),
        "-x", "--audio-format", "wav", "--audio-quality", "0",
        "-o", os.path.join(dir_tmp, "audio.%(ext)s"),
        url,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # yt-dlp puede fallar por rate-limit/geo; buscar si ya hay un wav
        existing = [f for f in os.listdir(dir_tmp) if f.endswith(".wav")]
        if not existing:
            raise RuntimeError(f"yt-dlp falló y no hay audio previo: {e.stderr[-300:]}")
    # Buscar el wav generado
    for f in os.listdir(dir_tmp):
        if f.endswith(".wav"):
            return os.path.join(dir_tmp, f)
    raise RuntimeError("No se generó el wav")


def transcribir(wav: str, idioma: str | None) -> str:
    """Transcribe con faster-whisper en GPU."""
    from faster_whisper import WhisperModel

    print("⏳ Whisper base en GPU...", flush=True)
    model = WhisperModel("small", device="cuda", compute_type="float16")
    kwargs = {"language": idioma} if idioma else {}
    segments, info = model.transcribe(wav, beam_size=5, **kwargs)
    return " ".join(s.text.strip() for s in segments)


def main():
    if len(sys.argv) < 2:
        print("Uso: transcribir_youtube_fallback.py <video_id_o_url> [idioma]")
        sys.exit(1)

    url = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else None

    # Normalizar: si es solo el ID, montar la URL
    if not url.startswith("http"):
        url = f"https://www.youtube.com/watch?v={url}"

    tmp = tempfile.mkdtemp(prefix="yt_fallback_")
    try:
        print(f"📥 Descargando audio de {url} (yt-dlp)...")
        wav = descargar_audio(url, tmp)
        print(f"   → {wav}")

        texto = transcribir(wav, idioma)
        print(f"\n=== TRANSCRIPCIÓN LOCAL ({len(texto)} chars) ===")
        print(texto[:4000])
        if len(texto) > 4000:
            print(f"\n... ({len(texto) - 4000} chars más)")

        # Guardar
        salida = os.path.join(os.path.dirname(os.path.abspath(url)) if False else os.getcwd(),
                              f"transcripcion_fallback_{sys.argv[1][:11]}.txt")
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"\n✅ Guardada: {salida}")
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
