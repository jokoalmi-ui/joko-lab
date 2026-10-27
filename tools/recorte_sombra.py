"""Re-recorta un packshot descartando la SOMBRA y el fondo claro.

Motivo (27-oct-2026, BASSO): `recorte_silueta.py` (flood-fill desde el borde)
metio dentro de la silueta la sombra difusa del packshot. Resultado: 35,7 % de
los pixeles opacos eran gris claro (L>140, sat<0,12) y la banda crecia de 71 px
(y=250) a 158 px (y=500) sobre una figura de 514 px. Eso es lo que el ojo ve
como "forma blanca pegada al frasco"; no es antialiasing.

Criterio: el frasco es VERDE OSCURO SATURADO + DORADO SATURADO; la sombra y el
fondo son GRIS NEUTRO. Asi que se segmenta por saturacion/luminancia, se rellenan
huecos (brillos especulares), se erosiona el filo mezclado y se descontamina el
color del borde con el interior (limpiar_color).

Uso:
  python recorte_sombra.py <pack.png> <salida.png> [--sat 0.15] [--lum 110]
                           [--erode 2] [--feather 1]
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from limpiar_halo_recorte import limpiar_color  # noqa: E402


def _dil(m, n=1):
    for _ in range(n):
        out = m.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
        m = out
    return m


def _ero(m, n=1):
    for _ in range(n):
        out = m.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                out &= np.roll(np.roll(m, dy, 0), dx, 1)
        m = out
    return m


def mascara_frasco(rgb, sat_min=0.15, lum_max=110):
    a = rgb.astype(float)
    mx = a.max(2)
    mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0.0)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    m = (sat > sat_min) | (lum < lum_max)          # frasco: color o muy oscuro
    m = _dil(m, 2)
    m = _ero(m, 1)                                  # cierre: une zonas fragmentadas
    # rellenar huecos: el fondo (sin frasco) inundado desde el borde exterior
    fondo = _ero(~m, 1)
    for _ in range(400):
        crece = _dil(fondo, 1) & ~m
        if (crece == fondo).all():
            break
        fondo = crece
    return m | ~fondo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pack')
    ap.add_argument('salida')
    ap.add_argument('--sat', type=float, default=0.15)
    ap.add_argument('--lum', type=float, default=110)
    ap.add_argument('--erode', type=int, default=2)
    ap.add_argument('--feather', type=float, default=1.0)
    ap.add_argument('--capas-color', type=int, default=8)
    o = ap.parse_args()

    with Image.open(o.pack) as im0:
        im = im0.convert('RGB')
    rgb = np.array(im)
    m = mascara_frasco(rgb, o.sat, o.lum)
    print('mascara: %d px = %.1f %% de la imagen' % (m.sum(), 100 * m.sum() / m.size))
    if o.erode:
        m = _ero(m, o.erode)
    # borde suave (antialiasing) a partir de la mascara dura erosionada
    al = Image.fromarray((m * 255).astype(np.uint8), 'L')
    if o.feather:
        al = al.filter(ImageFilter.GaussianBlur(o.feather))
    rgba = np.dstack([rgb, np.array(al)]).astype(np.uint8)
    antes = int(((rgba[..., 3] > 12) & (rgba[..., 3] < 250)).sum())
    rgba = limpiar_color(rgba, pasadas=o.capas_color)
    out = Image.fromarray(rgba, 'RGBA')
    out.save(o.salida)
    al_f = rgba[..., 3].astype(float)
    r, g, b = (rgba[..., i].astype(float) for i in range(3))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    mx = np.maximum.reduce([r, g, b])
    mn = np.minimum.reduce([r, g, b])
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0.0)
    op = al_f > 250
    gris = op & (lum > 140) & (sat < 0.12)
    print('opacos %d | gris claro %d = %.1f %%  (antes del recorte: 35,7 %%)'
          % (op.sum(), gris.sum(), 100 * gris.sum() / max(op.sum(), 1)))
    print('semitransparentes %d (antes %d)' % (int(((al_f > 12) & (al_f < 250)).sum()), antes))
    print('OK -> %s  %s' % (o.salida, out.size))


if __name__ == '__main__':
    main()
