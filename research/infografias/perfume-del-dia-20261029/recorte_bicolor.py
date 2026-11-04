#!/usr/bin/env python3
"""Recorte GEOMETRICO del frasco bicolor de OIKB (packshot trasero oficial, sb_1.jpg).

Motivo (medido 29-oct-2026): el packshot trasero tiene el 30 % derecho del cuerpo
en blanco sobre fondo blanco y el borde derecho desaparece en varias filas
(y=2600: ultimo pixel no-blanco en x=1935) -> el flood-fill se cuela DENTRO del
frasco y deja transparente el lateral derecho (medido: 37,8 % de alfa 0 y el VLM
vio "hueco transparente a la derecha de la banda azul").

Fix: mascara por geometria medida fila a fila (cuerpo de lados verticales
x~688..2629, base redondeada y 2995-3070, corcho/cuello/hombro por contraste),
feather 0,6 px. Se escribe un PNG nuevo; no toca nada publicado.
"""
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC = "/home/jokoalmi/.hermes/cache/scratch/sb_1.jpg"
OUT = "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20261029/santi_oikb_figura_b.png"
# gain: el packshot trasero sale mas claro que el frontal (L media 190,6 vs 179,2)
# y eso hunde el contraste del tapon sobre el fondo de la ficha (medido: 75,2 -> 1,69:1)
GAIN = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
CORK_GAIN = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
if len(sys.argv) > 2:
    OUT = sys.argv[2]

im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(int)
H, W = a.shape[:2]
nw = a.min(axis=2) < 250

# limpieza: el JPEG deja motas no-blancas sueltas en los bordes del lienzo
# (medido: 1 px en y=0 y y=3306 -> el recorte se iba a 3307 px de alto)
from scipy import ndimage as ndi
lab, nlab = ndi.label(nw)
tam = ndi.sum(nw, lab, range(1, nlab + 1))
keep = np.isin(lab, np.nonzero(tam > 2000)[0] + 1)
print("componentes %d, conservados %d (%.1f%% de px)"
      % (nlab, int((tam > 2000).sum()), keep.mean() * 100))
nw = keep

# limites medidos del cuerpo (lados verticales)
Y_BODY_TOP, Y_BODY_BOT = 1500, 2995
X_RIGHT_BODY = 2629

left = np.zeros(H, dtype=int)
right = np.zeros(H, dtype=int)
rows_nw = nw.any(axis=1)
y_first, y_last = int(np.argmax(rows_nw)), int(H - np.argmax(rows_nw[::-1]) - 1)
last = None
for y in range(y_first, y_last + 1):
    xs = np.nonzero(nw[y])[0]
    if len(xs) == 0:
        if last is None:            # hueco antes del primer objeto: no rellenar
            left[y] = right[y] = -1
            continue
        left[y], right[y] = last    # hueco INTERNO: se puentea
        continue
    l, r = int(xs.min()), int(xs.max())
    if Y_BODY_TOP <= y <= Y_BODY_BOT:
        l = min(max(l, 680), 700)          # lado izquierdo: 688-693 medidos
        r = X_RIGHT_BODY                    # lado derecho: borde fino, con huecos
    left[y], right[y] = l, r
    last = (l, r)

mask = np.zeros((H, W), dtype=np.uint8)
for y in range(H):
    if left[y] < 0:
        continue
    mask[y, left[y]:right[y] + 1] = 255

# limpia filas-testigo (motas de JPEG que sobreviven al filtro de componentes)
anchos = (mask > 0).sum(axis=1)
mask[anchos < 50] = 0
print("filas utiles %d de %d" % (int((anchos >= 50).sum()), H))

alpha = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(0.6))
fig = im.convert("RGBA")
if GAIN != 1.0:
    rgb = np.array(fig.convert("RGB")).astype(float) * GAIN
    fig = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
fig.putalpha(alpha)
bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
pad = 6
box = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
       min(bbox[2] + pad, W), min(bbox[3] + pad, H))
fig = fig.crop(box)

# oscurece SOLO el corcho, con rampa hasta el aro dorado (medido en el original:
# corcho hasta y=1300, aro 1310-1390). Asi el cuerpo blanco queda intacto.
if CORK_GAIN != 1.0:
    arr = np.array(fig).astype(float)
    hh = arr.shape[0]
    y0 = 1300 - box[1]
    y1 = 1400 - box[1]
    fac = np.full(hh, 1.0)
    fac[:max(y0, 0)] = CORK_GAIN
    ramp = slice(max(y0, 0), max(min(y1, hh), 0))
    n = fac[ramp].size
    if n > 0:
        fac[ramp] = np.linspace(CORK_GAIN, 1.0, n)
    arr[..., :3] *= fac[:, None, None]
    fig = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

fig.save(OUT)

al = np.array(fig.getchannel("A"))
print("OK ->", OUT, fig.size, "| alfa0 %.1f%% | alfa>=250 %.1f%%"
      % ((al == 0).mean() * 100, (al >= 250).mean() * 100))
