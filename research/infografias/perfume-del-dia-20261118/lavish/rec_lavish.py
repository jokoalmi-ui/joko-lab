#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorte del frasco de Lavish (ficha 18-11-2026, sustituto de Vibrato).

El packshot de partida (pack_parf.png, CDN de Parfinity) NO es blanco: es un
frasco metalico plateado sobre **fondo negro liso** (L media 56,7; esquinas
(0,0,0)). Por eso no vale el metodo de rec_v5.py, que supone fondo blanco.

Metodo:
  1. exterior = negro (L <= NEGRO) conectado a los bordes de la imagen
  2. objeto = complemento; solo la componente principal, con huecos rellenos
     (los reflejos oscuros internos del metal NO se vacian)
  3. alpha gradual en la banda de borde segun luminancia: sobre negro, el
     pixel es opaco en proporcion a su brillo (L/UMBRAL), sin MinFilter/MaxFilter
  4. descontaminacion del negro en los semitransparentes + blur del alpha
  5. metricas de control: asimetria de silueta, huecos y perfil de anchura

Uso: python3 rec_lavish.py <packshot> <salida.png> [NEGRO]
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

NEGRO = 20.0
BANDA = 5
BLUR = 1.4


def main(src, dst, negro=NEGRO):
    a = np.array(Image.open(src).convert("RGB")).astype(float)
    L = a.mean(axis=2)

    free = L <= negro
    lab, _ = ndimage.label(free)
    bordes = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    ext = np.isin(lab, [b for b in bordes if b])
    obj = ~ext

    lab2, n2 = ndimage.label(obj)
    if n2 == 0:
        raise SystemExit("sin objeto")
    sz = ndimage.sum(obj, lab2, range(1, n2 + 1))
    obj = ndimage.binary_fill_holes(lab2 == (int(np.argmax(sz)) + 1))

    dist = ndimage.distance_transform_cdt(~ext, metric="taxicab")
    alpha = np.where(obj, 255.0, 0.0)
    borde = obj & (dist <= BANDA)
    frac = np.clip(L / 55.0, 0.0, 1.0)
    alpha[borde] = 255.0 * frac[borde]
    alpha[obj & (dist > BANDA)] = 255.0

    al = np.clip(alpha / 255.0, 0.0, 1.0)
    safe = np.clip(al, 1e-3, 1.0)[..., None]
    col = np.clip((a - (1.0 - safe) * 0.0) / safe, 0.0, 255.0)
    col[alpha <= 0] = 0

    am = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(BLUR))
    alpha = np.array(am).astype(float)
    alpha[~obj] = np.minimum(alpha[~obj], 30.0)
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

    print("OK %s %s" % (dst, cv.size))
    print("silueta %dx%d | eje %.0f | izq %.0f der %.0f | asimetria %+.1f%%"
          % (x1 - x0 + 1, y1 - y0 + 1, cx, izq, der, 100 * (der - izq) / max(izq, 1)))
    # perfil de anchura por filas (cada 8%)
    print("perfil anchura por filas:")
    for f in range(0, 101, 8):
        yy2 = y0 + int((y1 - y0) * f / 100.0)
        rr = np.where(op[yy2])[0]
        print("  y=%4d (%3d%%) ancho %4d  x %4d..%4d"
              % (yy2, f, len(rr) and rr.max() - rr.min() + 1, rr.min() if len(rr) else -1,
                 rr.max() if len(rr) else -1))
    # huecos internos
    holes = ndimage.binary_fill_holes(op) & ~op
    hl, nh = ndimage.label(holes)
    sizes = sorted(ndimage.sum(holes, hl, range(1, nh + 1)), reverse=True)[:5]
    print("huecos alpha>128: %d | mayores %s" % (nh, [int(s) for s in sizes]))
    print("opacos %d px | bbox imagen %s" % (op.sum(), cv.size))


if __name__ == "__main__":
    f = float(sys.argv[3]) if len(sys.argv) > 3 else NEGRO
    main(sys.argv[1], sys.argv[2], f)
