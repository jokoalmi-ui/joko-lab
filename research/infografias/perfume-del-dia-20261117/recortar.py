#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte de la figura del frasco (Tuttle, Tiziana Terenzi) por banda.
Packshot: perfumerialaura 7328 (800x800, fondo blanco puro, frasco aislado + reflejo tenue en la base).
Corta la reflexion de la base (L>135 por debajo de y=708) para que no aparezca 'segunda botella'.
"""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
a = np.array(im).astype(float)
h, w, _ = a.shape
L = a.mean(axis=2)
mx = a.max(axis=2); mn = a.min(axis=2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1) * 255, 0)

# 1. base real del frasco: ultima fila con L media baja (el reflejo sube a L>140)
base = 0
for y in range(h):
    xs = np.where(L[y] < 237)[0]
    if len(xs) > 40 and L[y][xs].mean() < 135:
        base = y
print("base real del frasco: y=%d" % base)

# 2. banda del frasco: liquido/cuerpo saturado U tapon dorado, +-14 px
gold = (sat > 55) & (L > 60) & (L < 252)
ys, xs = np.where(gold)
gx0, gx1 = xs.min(), xs.max()
dark = (L < 110) & (np.abs(a[:, :, 0] - a[:, :, 2]) < 40)
dy, dx = np.where(dark)
bx0, bx1 = max(0, min(gx0, dx.min()) - 14), min(w - 1, max(gx1, dx.max()) + 14)
print("banda x: %d-%d | gold x: %d-%d | dark x: %d-%d" % (bx0, bx1, gx0, gx1, dx.min(), dx.max()))
band = np.zeros((h, w), bool)
band[:, bx0:bx1 + 1] = True
band[base + 2:, :] = False          # fuera la reflexion de la base

# 3. flood fill del fondo exterior DENTRO de la banda
obj = (L < 237) & band
free = ~obj
vis = np.zeros((h, w), bool)
dq = deque()
for x in range(w):
    for y in (0, h - 1):
        if free[y, x]:
            vis[y, x] = True; dq.append((y, x))
for y in range(h):
    for x in (0, w - 1):
        if free[y, x]:
            vis[y, x] = True; dq.append((y, x))
while dq:
    y, x = dq.popleft()
    for dyy, dxx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dyy, x + dxx
        if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not vis[ny, nx]:
            vis[ny, nx] = True; dq.append((ny, nx))
solid = (~vis) & band

# 4. erosion 2 px + descontaminacion del blanco
m = (Image.fromarray((solid * 255).astype(np.uint8))
     .filter(ImageFilter.MinFilter(5))
     .filter(ImageFilter.MaxFilter(3))
     .filter(ImageFilter.GaussianBlur(0.7)))
alpha = np.array(m)
al = alpha.astype(float) / 255
safe = np.clip(al, 1e-3, 1)[..., None]
col = np.clip((a - (1 - safe) * 255) / safe, 0, 255)
img = Image.fromarray(np.dstack([col.astype(np.uint8), alpha]).astype(np.uint8), "RGBA").crop()

img = img.crop(img.getbbox())
PAD = 16
cv = Image.new("RGBA", (img.width + 2 * PAD, img.height + 2 * PAD), (0, 0, 0, 0))
cv.alpha_composite(img, (PAD, PAD))
cv.save(dst)
print("OK %s %s" % (dst, cv.size))

# 5. puertas: 0 opacos en margenes de 16 px
al = np.array(cv)[:, :, 3]
print("margenes opacos: top=%d bottom=%d left=%d right=%d" % (
    (al[:PAD] > 8).sum(), (al[-PAD:] > 8).sum(),
    (al[:, :PAD] > 8).sum(), (al[:, -PAD:] > 8).sum()))
