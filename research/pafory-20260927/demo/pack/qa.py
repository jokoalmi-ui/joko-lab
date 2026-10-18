#!/usr/bin/env python3
"""QA visual medible: brillo, tinta, huecos verticales, margen inferior y contraste WCAG.
No sustituye al ojo humano: detecta piezas vacías, apelotonadas o con texto ilegible."""
import pathlib
from PIL import Image, ImageStat
import numpy as np

OUT = pathlib.Path(__file__).parent / "out"
BG = (12, 14, 17)

# contraste WCAG de la paleta sobre el fondo
PAL = {"ink": "#F4F5F7", "muted": "#A7AEBB", "dim": "#8E96A5", "gold": "#E7CB84",
       "gold2": "#D8B45C", "blue": "#7FA8FF", "legal": "#828A99", "micro": "#8A91A0",
       "faint": "#7B828F", "u2": "#78808F"}

def lum(rgb):
    c = [x / 255 for x in rgb]
    c = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def hexs(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def ratio(a, b):
    la, lb = lum(hexs(a)), lum(hexs(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

print("== contraste sobre el fondo #0C0E12 (WCAG AA: 4,5 normal · 3,0 texto grande) ==")
for n, c in PAL.items():
    r = ratio(c, "#0C0E12")
    print(f"   {'OK  ' if r >= 4.5 else ('aviso' if r >= 3 else 'BAJO')} {n:6s} {c} {r:5.2f}:1")

print("\n== piezas ==")
print(f"   {'pieza':22s} {'px':>11s} {'brillo':>6s} {'sd':>5s} {'tinta':>6s} {'hueco máx':>9s} {'margen inf':>10s} {'colores':>7s}")
for p in sorted(OUT.glob("*.png")):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(int)
    st = ImageStat.Stat(im)
    gray = a.mean(axis=2)
    ink = float((gray > 55).mean() * 100)
    rows = (np.abs(a - np.array(BG)).max(axis=2) > 12).mean(axis=1)   # filas con algo distinto del fondo
    # mayor hueco interior (filas seguidas casi vacías)
    vacio = rows < 0.005
    mejor = cur = 0
    for v in vacio:
        cur = cur + 1 if v else 0
        mejor = max(mejor, cur)
    inf = 0
    for v in vacio[::-1]:
        if v: inf += 1
        else: break
    col = len(set(map(tuple, a[::17, ::17].reshape(-1, 3))))
    print(f"   {p.stem:22s} {im.size[0]:5d}x{im.size[1]:<5d} {st.mean[0]:6.1f} {st.stddev[0]:5.1f} "
          f"{ink:5.1f}% {mejor:8d}p {inf:9d}p {col:7d}")
