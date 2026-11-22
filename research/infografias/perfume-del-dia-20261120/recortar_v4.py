#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte v4 (18-11-2026, Vibrato/Sospiro): v3 generalizado a FONDO GRIS.

El packshot del fabricante (Shopify sospirointernational.com, 1000x1500) trae
fondo L=236 uniforme, NO blanco puro 255. Por eso:
  - free  = L >= BG-8  (fondo gris conectado a los bordes)
  - banda = 4 px, alpha gradual segun (BG - L)/(BG-190)
  - descontaminacion del fondo con BG=236, no con 255
Sin MinFilter/MaxFilter (fabricaban el dentado).

Uso: python3 recortar_v4.py <packshot> <salida.png> [BG]
"""
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

BANDA = 4
BLUR = 1.8


def main(src, dst, BG):
    a = np.array(Image.open(src).convert("RGB")).astype(float)
    h, w, _ = a.shape
    L = a.mean(axis=2)

    free = L >= (BG - 8.0)
    ext = np.zeros((h, w), bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if free[y, x] and not ext[y, x]:
                ext[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if free[y, x] and not ext[y, x]:
                ext[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not ext[ny, nx]:
                ext[ny, nx] = True
                dq.append((ny, nx))

    obj = ~ext
    dist = np.full((h, w), 1e9, float)
    dist[ext] = 0
    frente = ext.copy()
    for k in range(1, BANDA + 2):
        nuevo = np.zeros((h, w), bool)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.zeros((h, w), bool)
            sh[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)] = \
                frente[max(0, dy):h - max(0, -dy), max(0, dx):w - max(0, -dx)]
            nuevo |= sh
        nuevo &= ~frente
        dist[nuevo] = k
        frente |= nuevo

    alpha = np.where(obj, 255.0, 0.0)
    borde = obj & (dist <= BANDA)
    frac = np.clip((BG - L) / (BG - 190.0), 0.0, 1.0)
    alpha[borde] = 255.0 * frac[borde]
    alpha[obj & (dist > BANDA)] = 255.0

    al = np.clip(alpha / 255.0, 0.0, 1.0)
    safe = np.clip(al, 1e-3, 1.0)[..., None]
    col = np.clip((a - (1.0 - safe) * BG) / safe, 0.0, 255.0)
    col[alpha <= 0] = 0

    am = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(BLUR))
    alpha = np.array(am).astype(float)
    alpha[~obj] = np.minimum(alpha[~obj], 40.0)
    alpha[alpha < 3] = 0

    img = Image.fromarray(np.dstack([col.astype(np.uint8), alpha.astype(np.uint8)]), "RGBA")
    img = img.crop(img.getbbox())
    PAD = 16
    cv = Image.new("RGBA", (img.width + 2 * PAD, img.height + 2 * PAD), (0, 0, 0, 0))
    cv.alpha_composite(img, (PAD, PAD))
    cv.save(dst)

    al2 = np.array(cv)[:, :, 3]
    print("OK %s %s (BG=%.0f)" % (dst, cv.size, BG))
    print("margenes opacos top=%d bottom=%d left=%d right=%d" % (
        (al2[:PAD] > 8).sum(), (al2[-PAD:] > 8).sum(),
        (al2[:, :PAD] > 8).sum(), (al2[:, -PAD:] > 8).sum()))


if __name__ == "__main__":
    bg = float(sys.argv[3]) if len(sys.argv) > 3 else 236.0
    main(sys.argv[1], sys.argv[2], bg)
