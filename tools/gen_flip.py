#!/usr/bin/env python3
"""gen_flip.py — Genera un clip de paso de pagina 3D (page flip) como MP4.
Uso: python3 gen_flip.py <A.png> <B.png> <outdir> <prefix> [n_frames]
A = pagina que se levanta (ultimo frame del grupo anterior)
B = pagina revelada (primera variante del grupo actual)
Genera outdir/prefix.mp4 (solo video, 25fps, 1080x1350, libx264).
"""
import os, subprocess, sys, math

A, B = sys.argv[1], sys.argv[2]
OUT = sys.argv[3]
PREFIX = sys.argv[4]
N_FRAMES = int(sys.argv[5]) if len(sys.argv) > 5 else 30  # 30 @ 25fps = 1.2s

os.makedirs(OUT, exist_ok=True)
FRAMES = f"{OUT}/{PREFIX}_fr"
os.makedirs(FRAMES, exist_ok=True)

def ease(t):
    return t * t * (3 - 2 * t)

def frame_html(i, t):
    ang = -180.0 * ease(t)
    sombra = 0.30 * math.sin(math.pi * t)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  html, body {{ margin:0; padding:0; width:1080px; height:1350px; background:#141414; overflow:hidden; }}
  .escena {{ position:relative; width:1080px; height:1350px; perspective:2200px; }}
  .pag2 {{ position:absolute; left:0; top:0; width:1080px; height:1350px; }}
  .pag1 {{ position:absolute; left:0; top:0; width:1080px; height:1350px;
           transform-origin:left center; transform-style:preserve-3d;
           transform: rotateY({ang:.4f}deg); }}
  .pag1 .front {{ position:absolute; left:0; top:0; width:1080px; height:1350px; backface-visibility:hidden; }}
  .pag1 .back {{ position:absolute; left:0; top:0; width:1080px; height:1350px;
                 transform: rotateY(180deg); backface-visibility:hidden; }}
  .sombra {{ position:absolute; left:0; top:0; width:1080px; height:1350px;
             background:#000; opacity:{sombra:.3f}; pointer-events:none; }}
</style></head>
<body>
  <div class="escena">
    <img class="pag2" src="file://{B}">
    <div class="pag1">
      <img class="front" src="file://{A}">
      <img class="back" src="file://{os.path.dirname(A)}/hoja-cuaderno-base.png">
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
         f"--screenshot={FRAMES}/frame_{i:02d}.png", "--window-size=1080,1350",
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
