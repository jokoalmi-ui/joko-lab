#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte v5 del frasco (ficha Vibrato 18-11-2026).

Que corrige respecto a v4:
  v4 recorto desde pack_B.png, que NO es un packshot limpio: tiene una masa
  gris clara (L ~200-230) pegada al lado derecho del frasco que el umbral
  incluyo como objeto. En la ficha se ve como un bloque gris de 46.415 px
  (13,9 % de la figura) junto al frasco y deja la silueta asimetrica (+23 %).
  pack_A.png es el packshot limpio: silueta a -6 % de asimetria.

Metodo:
  1. exterior = fondo (L >= FONDO) conectado a los bordes de la imagen
  2. se descarta toda componente de objeto que no sea la principal
     (asi caen reflejos y marcas sueltas)
  3. alpha gradual en la banda de borde segun luminancia (sin MinFilter/MaxFilter)
  4. descontaminacion del fondo en los semitransparentes + blur del alpha
  5. metrica de control: asimetria de la silueta respecto al eje del cuello

Uso: python3 rec_v5.py <packshot> <salida.png> [FONDO]
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

FONDO = 236.0
BANDA = 4
BLUR = 1.8


def main(src, dst, fondo=FONDO):
    a = np.array(Image.open(src).convert("RGB")).astype(float)
    h, w, _ = a.shape
    L = a.mean(axis=2)

    # 1. exterior: fondo conectado a los bordes
    free = L >= fondo - 1.0
    lab, n = ndimage.label(free)
    bordes = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    ext = np.isin(lab, [b for b in bordes if b])
    obj = ~ext

    # 2. solo la componente principal (frasco), y relleno de huecos internos
    lab2, n2 = ndimage.label(obj)
    if n2 == 0:
        raise SystemExit("sin objeto")
    sz = ndimage.sum(obj, lab2, range(1, n2 + 1))
    obj = ndimage.binary_fill_holes(lab2 == (int(np.argmax(sz)) + 1))

    # distancia al exterior
    dist = ndimage.distance_transform_cdt(~ext, metric="taxicab")
    alpha = np.where(obj, 255.0, 0.0)
    borde = obj & (dist <= BANDA)
    frac = np.clip((255.0 - L) / (255.0 - 200.0), 0.0, 1.0)
    alpha[borde] = 255.0 * frac[borde]
    alpha[obj & (dist > BANDA)] = 255.0

    # 3. descontaminacion del fondo
    al = np.clip(alpha / 255.0, 0.0, 1.0)
    safe = np.clip(al, 1e-3, 1.0)[..., None]
    col = np.clip((a - (1.0 - safe) * fondo) / safe, 0.0, 255.0)
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
    op = al2 > 128
    ys, xs = np.where(op)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    yy = y0 + int((y1 - y0) * 0.22)
    r = np.where(op[yy])[0]
    cx = (r.min() + r.max()) / 2.0
    izq, der = cx - x0, x1 - cx
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    Lr = np.array(cv.convert("RGB")).astype(float)
    Lr = 0.2126 * Lr[:, :, 0] + 0.7152 * Lr[:, :, 1] + 0.0722 * Lr[:, :, 2]
    Ar = np.array(cv)[:, :, 3] > 128
    gris = Ar & (Lr > 195) & (Lr < 234) & (mx.mean() >= 0)
    print("OK %s %s" % (dst, cv.size))
    print("silueta %dx%d | eje %.0f | izq %.0f der %.0f | asimetria %+.1f%%"
          % (x1 - x0 + 1, y1 - y0 + 1, cx, izq, der, 100 * (der - izq) / max(izq, 1)))
    print("gris claro (L 195-234) dentro: %.2f%%" % (100 * gris.sum() / max(1, Ar.sum())))


if __name__ == "__main__":
    f = float(sys.argv[3]) if len(sys.argv) > 3 else FONDO
    main(sys.argv[1], sys.argv[2], f)
