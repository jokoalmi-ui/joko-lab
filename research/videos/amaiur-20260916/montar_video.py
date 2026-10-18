#!/usr/bin/env python3
"""Monta el video AMAIUR: 29 fotogramas, fundido cruzado, 1080x1920.

D = 2.5 s por foto, F = 0.5 s de fundido cruzado.
Duracion total = 29*2.5 - 28*0.5 = 58.5 s
offset del fundido i-esimo (i=1..28) = i * (D - F) = i * 2.0
"""
import os
import subprocess
import sys
import time

BASE = "/home/jokoalmi/joko-lab/research/videos/amaiur-20260916"
FRAMES = os.path.join(BASE, "frames")
SALIDA = os.path.join(BASE, "album-amaiur-1080x1920.mp4")

D = 2.5
F = 0.5
FPS = 30
N = 29


def run(cmd, **kw):
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, time.time() - t0, p.stdout[-1500:], p.stderr[-2500:]


# --- 1) probar NVENC ---
prueba = os.path.join(BASE, "test_nvenc.mp4")
rc, dt, out, err = run([
    "ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS),
    "-i", os.path.join(FRAMES, "frame_01.png"), "-t", "0.5",
    "-c:v", "h264_nvenc", "-preset", "p4", "-rc", "constqp", "-qp", "20",
    "-pix_fmt", "yuv420p", prueba,
])
if rc == 0:
    ENC = ["-c:v", "h264_nvenc", "-preset", "p4", "-rc", "constqp", "-qp", "20"]
    print(f"[encoder] NVENC disponible ({dt:.1f}s la prueba)")
else:
    ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19"]
    print(f"[encoder] NVENC NO disponible -> CPU libx264. Motivo: {err.strip().splitlines()[-1] if err.strip() else 'desconocido'}")
os.path.exists(prueba) and os.remove(prueba)

# --- 2) construir el filtro ---
entradas = []
for i in range(1, N + 1):
    entradas += ["-loop", "1", "-framerate", str(FPS),
                 "-t", str(D), "-i", os.path.join(FRAMES, f"frame_{i:02d}.png")]

partes = []
for i in range(N):
    partes.append(f"[{i}:v]fps={FPS},format=yuv420p,settb=AVTB[v{i}]")

etiqueta = "v0"
for i in range(1, N):
    offset = round(i * (D - F), 3)
    siguiente = f"x{i}"
    partes.append(f"[{etiqueta}][v{i}]xfade=transition=fade:duration={F}:offset={offset}[{siguiente}]")
    etiqueta = siguiente

filtro = ";".join(partes)
cmd = (["ffmpeg", "-y"] + entradas +
       ["-filter_complex", filtro, "-map", f"[{etiqueta}]",
        "-an", "-r", str(FPS)] + ENC + ["-pix_fmt", "yuv420p", "-movflags", "+faststart", SALIDA])

print(f"[montaje] {N} entradas, {N-1} fundidos, duracion prevista {N*D - (N-1)*F:.1f}s")
rc, dt, out, err = run(cmd)
print(f"[montaje] exit={rc}  tiempo={dt:.1f}s")
if rc != 0:
    print("STDERR (ultimas lineas):")
    print(err)
    sys.exit(1)

print(f"[salida] {SALIDA}  {os.path.getsize(SALIDA)/1048576:.1f} MB")
