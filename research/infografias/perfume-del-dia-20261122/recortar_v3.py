#!/usr/bin/env python3
"""Recorte v3 para frasco Lalique ENCRE NOIRE A L'EXTREME (packshot Amazon 1000x1000, fondo blanco).
Fondo 252, banda 4 px alfa gradual, descontaminacion del blanco, GaussianBlur 1.8 del alfa.
Sin MinFilter/MaxFilter (fabrican dentado)."""
import sys
from PIL import Image, ImageDraw, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
w, h = im.size

# 1. flood fill del fondo exterior desde las 4 esquinas sobre una copia
mark = im.copy()
d = ImageDraw.Draw(mark)
for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    if mark.getpixel(pt) != (255, 0, 255):
        ImageDraw.floodfill(mark, pt, (255, 0, 255), thresh=10)

px = im.load()
mk = mark.load()
alpha = Image.new("L", (w, h), 255)
ap = alpha.load()

for y in range(h):
    for x in range(w):
        if mk[x, y] == (255, 0, 255):
            ap[x, y] = 0
        else:
            L = (px[x, y][0] * 299 + px[x, y][1] * 587 + px[x, y][2] * 114) // 1000
            if L > 200:
                a = int(max(0, min(255, (255 - L) * 255 / 55)))
                ap[x, y] = a
            else:
                ap[x, y] = 255

# 2. descontaminacion del blanco en cada pixel semitransparente
rgb = im.load()
outim = im.copy()
op = outim.load()
for y in range(h):
    for x in range(w):
        a = ap[x, y]
        if 0 < a < 255:
            f = a / 255.0
            r, g, b = rgb[x, y]
            op[x, y] = (
                int(max(0, min(255, (r - 255 * (1 - f)) / f))),
                int(max(0, min(255, (g - 255 * (1 - f)) / f))),
                int(max(0, min(255, (b - 255 * (1 - f)) / f))),
            )

# 3. suavizado del alfa
alpha = alpha.filter(ImageFilter.GaussianBlur(1.8))
outim.putalpha(alpha)

# 4. recorte con aire
bb = alpha.point(lambda p: 255 if p > 8 else 0).getbbox()
mx, my = 26, 26
box = (max(0, bb[0] - mx), max(0, bb[1] - my), min(w, bb[2] + mx), min(h, bb[3] + my))
outim = outim.crop(box)
outim.save(out)
print("bbox origen", bb, "-> guardado", out, outim.size)

# 5. metricas: filo semitransparente (halo) y cristal conservado
a2 = outim.split()[3]
hist = a2.histogram()
semis = sum(hist[1:250])
tot = sum(hist[1:])
print("alfa semitransparente %.1f%% del objeto" % (100 * semis / max(1, tot)))
