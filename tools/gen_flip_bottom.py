#!/usr/bin/env python3
"""gen_flip_bottom.py — Paso de página BOTTOM-UP (bloc apaisado, espiral arriba).
La página se levanta desde el borde INFERIOR girando hacia arriba (rotateX).
Uso: python3 gen_flip_bottom.py <A.png> <B.png> <outdir> <prefix> [n_frames]
A = página que se levanta (último frame del grupo anterior)
B = página revelada (primera variante del grupo actual)
Genera outdir/prefix.mp4 (solo video, 25fps, 1920x1080, libx264).
"""
import os, subprocess, sys, math

A, B = sys.argv[1], sys.argv[2]
OUT = sys.argv[3]
PREFIX = sys.argv[4]
N_FRAMES = int(sys.argv[5]) if len(sys.argv) > 5 else 28  # 28 @ 25fps = 1.12s

os.makedirs(OUT, exist_ok=True)
FRAMES = f"{OUT}/{PREFIX}_fr"
os.makedirs(FRAMES, exist_ok=True)

# hoja de cuaderno apaisada (el reverso de la hoja)
HOJA = os.path.join(os.path.dirname(A), "hoja-cuaderno-apaisada.png")
if not os.path.exists(HOJA):
    HOJA = "/tmp/fusion_apaisado/slides/hoja-cuaderno-apaisada.png"

def ease(t):
    return t * t * (3 - 2 * t)

def frame_html(i, t):
    # rotación alrededor del eje X con origen en el borde INFERIOR: la hoja se levanta hacia arriba
    ang = -168.0 * ease(t)
    sombra = 0.30 * math.sin(math.pi * t)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  html, body {{ margin:0; padding:0; width:1920px; height:1080px; background:#141414; overflow:hidden; }}
  .escena {{ position:relative; width:1920px; height:1080px; perspective:2600px; }}
  .pag2 {{ position:absolute; left:0; top:0; width:1920px; height:1080px; }}
  .pag1 {{ position:absolute; left:0; top:0; width:1920px; height:1080px;
           transform-origin:bottom center; transform-style:preserve-3d;
           transform: rotateX({ang:.4f}deg); }}
  .pag1 .front {{ position:absolute; left:0; top:0; width:1920px; height:1080px; backface-visibility:hidden; }}
  .pag1 .back {{ position:absolute; left:0; top:0; width:1920px; height:1080px;
                 transform: rotateX(180deg); backface-visibility:hidden; }}
  .sombra {{ position:absolute; left:0; top:0; width:1920px; height:1080px;
             background:#000; opacity:{sombra:.3f}; pointer-events:none; }}
</style></head>
<body>
  <div class="escena">
    <img class="pag2" src="file://{B}">
    <div class="pag1">
      <img class="front" src="file://{A}">
      <img class="back" src="file://{HOJA}">
    </div>
    <div class="sombra"></div>
  </div>
</body></html>"""

for i in range(N_FRAMES):
    t = i / (N_FRAMES - 1)
    with open(f"{FRAMES}/frame_{i:02d}.html", "w", encoding="utf-8") as f:
        f.write(frame_html(i, t))
    r = subprocess.run(
        ["google-chrome", "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={FRAMES}/frame_{i:02d}.png", "--window-size=1920,1080",
         f"file://{FRAMES}/frame_{i:02d}.html"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"chrome frame {i}: {r.stderr[-300:]}")

mp4 = f"{OUT}/{PREFIX}.mp4"
r = subprocess.run(
    ["ffmpeg", "-y", "-framerate", "25", "-i", f"{FRAMES}/frame_%02d.png",
     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", mp4],
    capture_output=True, text=True)
if r.returncode != 0:
    sys.exit(f"ffmpeg: {r.stderr[-300:]}")
print(mp4)
