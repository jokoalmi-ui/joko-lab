#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte del frasco de Jubilation XXV Man (Amouage) desde el packshot de isolee (800x800, fondo blanco puro).
Sin banda: flood-fill del blanco exterior desde los bordes + corte de la reflexion de la base si existe.
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

THR = 243.0
free = L >= THR
vis = np.zeros((h, w), bool)
dq = deque()
for x in range(w):
    for y in (0, h - 1):
        if free[y, x] and not vis[y, x]:
            vis[y, x] = True
            dq.append((y, x))
for y in range(h):
    for x in (0, w - 1):
        if free[y, x] and not vis[y, x]:
            vis[y, x] = True
            dq.append((y, x))
while dq:
    y, x = dq.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not vis[ny, nx]:
            vis[ny, nx] = True
            dq.append((ny, nx))

obj = ~vis
rows = obj.sum(axis=1)
ys = np.where(rows > 0)[0]
print("objeto filas: y=%d..%d  alto=%d" % (ys.min(), ys.max(), ys.max() - ys.min() + 1))
print("ultimas 8 filas con pixeles:", [(int(y), int(rows[y])) for y in ys[-8:]])
cols = obj.sum(axis=0)
xs = np.where(cols > 0)[0]
print("objeto cols: x=%d..%d  ancho=%d" % (xs.min(), xs.max(), xs.max() - xs.min() + 1))

# corte de reflexion: si el objeto se estrecha mucho en las filas finales
keep_bottom = ys.max()
for y in range(ys.min(), ys.max() + 1):
    pass
cand = obj.copy()
cand[:, :] = cand
m = (Image.fromarray((cand * 255).astype(np.uint8))
     .filter(ImageFilter.MinFilter(3))
     .filter(ImageFilter.MaxFilter(3))
     .filter(ImageFilter.GaussianBlur(0.6)))
alpha = np.array(m)
al = alpha.astype(float) / 255
safe = np.clip(al, 1e-3, 1)[..., None]
col = np.clip((a - (1 - safe) * 255) / safe, 0, 255)
img = Image.fromarray(np.dstack([col.astype(np.uint8), alpha]).astype(np.uint8), "RGBA")
bbox = img.getbbox()
img = img.crop(bbox)
print("bbox recorte:", bbox, "->", img.size)

PAD = 16
cv = Image.new("RGBA", (img.width + 2 * PAD, img.height + 2 * PAD), (0, 0, 0, 0))
cv.alpha_composite(img, (PAD, PAD))
cv.save(dst)
al2 = np.array(cv)[:, :, 3]
print("OK %s %s" % (dst, cv.size))
print("margenes opacos: top=%d bottom=%d left=%d right=%d" % (
    (al2[:PAD] > 8).sum(), (al2[-PAD:] > 8).sum(),
    (al2[:, :PAD] > 8).sum(), (al2[:, -PAD:] > 8).sum()))
