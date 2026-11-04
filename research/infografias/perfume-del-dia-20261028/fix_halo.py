#!/usr/bin/env python3
"""Decontamina el feather de la figura recortada: los píxeles de borde conservaban el color
del fondo del packshot (246,246,246 medido en las 3 esquinas) y fabricaban un halo claro
(A5 delta L +41,1 · feather L 220,0 vs interior-borde 175,7 · confirmado por visión).
Deshace la mezcla con el color REAL del fondo: fg = (rgb - (1-a)*bg)/a, y recorta el feather
para que el borde opaco empiece en alfa>=0,30 (evita el borde translúcido blanquecino).
No sobreescribe la figura original: escribe <slug>_figura_corr.png.
"""
from PIL import Image
import sys

src, dst = sys.argv[1], sys.argv[2]
BG = (246, 246, 246)
im = Image.open(src).convert("RGBA")
w, h = im.size
px = im.load()
cambiados = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a == 0 or a == 255:
            continue
        af = a / 255.0
        rgb = []
        for c, bg in zip((r, g, b), BG):
            v = (c - (1 - af) * bg) / af
            rgb.append(int(max(0, min(255, round(v)))))
        # recorte del feather: por debajo de 0,30 de cobertura el píxel es casi fondo
        a2 = int(max(0.0, min(1.0, (af - 0.30) / 0.70)) * 255)
        px[x, y] = (rgb[0], rgb[1], rgb[2], a2)
        cambiados += 1
im.save(dst)
print(f"OK {dst} · píxeles de borde corregidos {cambiados}")


def L(t):
    return 0.299 * t[0] + 0.587 * t[1] + 0.114 * t[2]


for f in (src, dst):
    im2 = Image.open(f).convert("RGBA")
    p2 = im2.load()
    e, i = [], []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            a = p2[x, y][3]
            if 5 < a < 250:
                e.append(L(p2[x, y]))
            elif a == 255 and any(p2[x + dx, y + dy][3] < 250 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                i.append(L(p2[x, y]))
    if e and i:
        me, mi = sum(e) / len(e), sum(i) / len(i)
        print(f"{f}: feather {len(e)} px L {me:.1f} · interior-borde {len(i)} px L {mi:.1f} · delta {me - mi:+.1f}")
