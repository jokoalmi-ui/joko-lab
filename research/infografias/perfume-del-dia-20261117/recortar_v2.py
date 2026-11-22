#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte v2 del frasco: borde limpio, sin halo blanco dentado.

Problema que corrige (ficha Jubilation XXV 17-11-2026): el recorte v1
(recortar2.py) usaba THR=243 + MinFilter(3)/MaxFilter(3) + blur 0.6, asi que
los pixeles del canto del cristal (L 246-252) quedaban OPACOS y con su color
casi blanco -> linea blanca dentada alrededor del frasco.

Metodo v2:
  1. flood-fill del blanco exterior (L >= 246) desde los bordes -> exterior
  2. alpha 255 en el objeto; en la banda de borde (<=3 px del exterior) el
     alpha baja segun lo cerca que este el pixel del blanco puro
  3. descontaminacion del blanco en esos pixeles (deshacer la mezcla con 255)
  4. suavizado del alpha con blur 1.2 (sin MinFilter/MaxFilter: son los que
     producen el dentado)

Uso: python3 recortar_v2.py <packshot> <salida.png>
"""
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

FONDO = 246.0     # L a partir de la cual el pixel es fondo
BANDA = 3         # px de borde que se descontaminan
BLUR = 1.2


def main(src, dst):
    a = np.array(Image.open(src).convert("RGB")).astype(float)
    h, w, _ = a.shape
    L = a.mean(axis=2)

    # 1. exterior = blanco conectado a los bordes de la imagen
    free = L >= FONDO
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
    # 2. distancia al exterior (pasos de 4-vecindad)
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
    # 3. banda de borde: alpha gradual segun luminancia (blanco puro -> 0)
    borde = obj & (dist <= BANDA)
    frac = np.clip((255.0 - L) / (255.0 - 200.0), 0.0, 1.0)  # 255->0, 200->1
    alpha[borde] = 255.0 * frac[borde]
    # el nucleo se queda opaco
    alpha[obj & (dist > BANDA)] = 255.0

    # 4. descontaminacion del blanco en todos los semitransparentes
    al = np.clip(alpha / 255.0, 0.0, 1.0)
    safe = np.clip(al, 1e-3, 1.0)[..., None]
    col = np.clip((a - (1.0 - safe) * 255.0) / safe, 0.0, 255.0)
    col[alpha <= 0] = 0

    am = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(BLUR))
    alpha = np.array(am).astype(float)
    alpha[~obj] = np.minimum(alpha[~obj], 40.0)  # el exterior no se infla
    alpha[alpha < 3] = 0

    img = Image.fromarray(
        np.dstack([col.astype(np.uint8), alpha.astype(np.uint8)]), "RGBA"
    )
    img = img.crop(img.getbbox())
    PAD = 16
    cv = Image.new("RGBA", (img.width + 2 * PAD, img.height + 2 * PAD), (0, 0, 0, 0))
    cv.alpha_composite(img, (PAD, PAD))
    cv.save(dst)

    al2 = np.array(cv)[:, :, 3]
    print("OK %s %s" % (dst, cv.size))
    print("margenes opacos top=%d bottom=%d left=%d right=%d" % (
        (al2[:PAD] > 8).sum(), (al2[-PAD:] > 8).sum(),
        (al2[:, :PAD] > 8).sum(), (al2[:, -PAD:] > 8).sum()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
