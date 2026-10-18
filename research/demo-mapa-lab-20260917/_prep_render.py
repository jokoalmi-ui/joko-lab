#!/usr/bin/env python3
"""Prepara 2 copias de la demo (mapa con nodo elegido / vista huecos), renderiza PNG y verifica."""
import re, shutil, subprocess, sys
from pathlib import Path

SRC = Path("/home/jokoalmi/joko-lab/research/demo-mapa-lab-20260917/ejemplo-mapa-lab-interactivo.html")
OUT = SRC.parent
TMP = Path("/tmp/demo_render"); TMP.mkdir(parents=True, exist_ok=True)

RENDER = "/home/jokoalmi/joko-lab/tools/render_html.sh"   # helper unico HTML->PNG del lab
if not shutil.which("google-chrome-stable") and not shutil.which("google-chrome"):
    sys.exit("no hay chrome")
print("render:", RENDER)

html = SRC.read_text(encoding="utf-8")

# --- copia 1: mapa por capas con el nodo P0 'git' seleccionado
inyect = """<script>window.addEventListener('load',()=>{try{document.querySelector('.node[data-id="git"]').click();}catch(e){}});</script>
</body>"""
c1 = TMP / "demo_mapa.html"
c1.write_text(html.replace("</body>", inyect), encoding="utf-8")

# --- copia 2: vista "qué falta" activa
c2 = TMP / "demo_falt.html"
h2 = html.replace('<section class="view on" id="v-map">', '<section class="view" id="v-map">')
h2 = h2.replace('<section class="view" id="v-falt">', '<section class="view on" id="v-falt">')
assert h2 != html and h2.count('class="view on"') == 1, "swap de vista falló"
c2.write_text(h2, encoding="utf-8")

jobs = [
    (c1, OUT / "demo-mapa-lab.png", 1600, 1500),
    (c2, OUT / "demo-que-falta.png", 1600, 1130),
]
for src, dst, w, h in jobs:
    cmd = ["bash", RENDER, "--espera=12000", str(src), str(dst), str(w), str(h)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if p.stdout.strip():
        print("   ", p.stdout.strip())
    print(f"\n{dst.name}: rc={p.returncode}")
    if p.stderr.strip():
        print("  stderr:", p.stderr.strip()[:300])

# verificación de los PNG
try:
    from PIL import Image, ImageStat
    for _, dst, w, h in jobs:
        im = Image.open(dst).convert("RGB")
        st = ImageStat.Stat(im)
        # zona no vacía: varianza global (una imagen en blanco/negro plano da ~0)
        print(f"{dst.name}: {im.size[0]}x{im.size[1]} · brillo medio {[round(x) for x in st.mean]} · std {[round(x) for x in st.stddev]}")
except Exception as e:
    print("PIL no disponible:", e)

print("\ntemporales:", c1, c2)
