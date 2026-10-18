#!/usr/bin/env python3
"""Anade la musica CC0 al video mudo y produce el entregable final.

Video : album-amaiur-1080x1920.mp4  (58,5 s, sin audio)
Musica: audio/musica-cc0-gymnopedie-no1.ogg (Satie, CC0, 204,8 s)
Final : AMAIUR-1080x1920.mp4  (video + AAC, con fundido de entrada y salida)
"""
import json
import os
import subprocess
import sys

BASE = "/home/jokoalmi/joko-lab/research/videos/amaiur-20260916"
VIDEO = os.path.join(BASE, "album-amaiur-1080x1920.mp4")
MUSICA = os.path.join(BASE, "audio", "musica-cc0-gymnopedie-no1.ogg")
SALIDA = os.path.join(BASE, "AMAIUR-1080x1920.mp4")
SALTO_INICIAL = 6.0   # empezar la pieza 6 s dentro (evita el arranque en silencio)
FADE = 1.5


def duracion(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", p], capture_output=True, text=True)
    return float(json.loads(out.stdout)["format"]["duration"])


if not os.path.exists(VIDEO):
    sys.exit(f"FALTA el video mudo: {VIDEO}")

dur = duracion(VIDEO)
t_fade_out = max(0.5, dur - FADE)
print(f"video mudo: {dur:.2f} s | musica desde {SALTO_INICIAL}s | fade in {FADE}s, fade out en {t_fade_out:.2f}s")

filtro = (f"[1:a]aresample=48000,afade=t=in:st=0:d={FADE},"
          f"afade=t=out:st={t_fade_out:.2f}:d={FADE}[a]")

cmd = ["ffmpeg", "-y", "-i", VIDEO, "-ss", str(SALTO_INICIAL), "-i", MUSICA,
       "-filter_complex", filtro, "-map", "0:v", "-map", "[a]",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
       "-movflags", "+faststart", "-shortest", SALIDA]

p = subprocess.run(cmd, capture_output=True, text=True)
print(f"exit={p.returncode}")
if p.returncode != 0:
    print(p.stderr[-2500:])
    sys.exit(1)
print(f"[entregable] {SALIDA}  {os.path.getsize(SALIDA)/1048576:.1f} MB")
