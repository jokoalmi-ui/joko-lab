#!/usr/bin/env python3
"""plata_silver.py - Recorta el packshot del frasco 7 Plata y lo deja PLATA BRILLANTE OPACA.

Motivo (28-sep-2026, orden del usuario): la figura salia transparente porque
recortar_frasco.py (distancia al blanco, umbral 42) volvia semitransparente la
plata clara del frasco (la plata clara esta cerca del blanco). Aqui:
  1) fondo por FLOOD FILL desde las esquinas (el fondo es blanco 255 conectado)
     -> dentro del frasco todo OPACO, se conservan los brillos.
  2) material metalico: niveles + bandas verticales de brillo + tinte frio,
     respetando los negros (texto LOEWE 7, cantos) que no se tocan.

USO: python3 plata_silver.py <pack.png> <salida.png> [amplitud_bandas]
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PACK, OUT = sys.argv[1], sys.argv[2]
AMP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.32

im = Image.open(PACK).convert("RGB")
w, h = im.size
ff = im.copy()
d = ImageDraw.Draw(ff)
for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1)):
    try:
        ImageDraw.floodfill(ff, seed, (255, 0, 255), thresh=12)
    except Exception as e:
        print("floodfill seed", seed, "->", e)
arr = np.asarray(ff)
bg = (arr[:, :, 0] == 255) & (arr[:, :, 1] == 0) & (arr[:, :, 2] == 255)
alpha = np.where(bg, 0, 255).astype(np.uint8)

rgb = np.asarray(im).astype(np.float32)
# 1) niveles: estirar el metal (0.16-0.94 del rango util)
L = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
L = np.clip(L, 0, 255)
Ls = np.clip((L - 40.0) * 255.0 / (236.0 - 40.0), 0, 255)
Ls = np.where(L < 70, L, Ls)  # los negros (texto/cantos) intactos

# 2) bandas verticales de brillo (metal pulido), segun la posicion en cada fila
ys, xs = np.nonzero(alpha > 0)
yy = np.arange(h)
band = np.ones((h, w), dtype=np.float32)
for y in range(h):
    cols = np.nonzero(alpha[y] > 0)[0]
    if cols.size < 4:
        continue
    x0, x1 = cols.min(), cols.max()
    t = (np.arange(x0, x1 + 1) - x0) / max(1.0, (x1 - x0))
    p = (0.80
         + AMP * np.exp(-(((t - 0.17) / 0.13) ** 2))
         + (AMP * 0.85) * np.exp(-(((t - 0.52) / 0.10) ** 2))
         + (AMP * 0.55) * np.exp(-(((t - 0.81) / 0.16) ** 2))
         - 0.14 * np.exp(-((t / 0.06) ** 2))
         - 0.14 * np.exp(-(((t - 1.0) / 0.06) ** 2)))
    band[y, x0:x1 + 1] = p
Lm = np.clip(Ls * band, 0, 255)
Lm = np.where(L < 70, L, Lm)

# 3) plata: tinte ligeramente frio
out = np.zeros((h, w, 3), dtype=np.uint8)
out[:, :, 0] = np.clip(Lm * 0.97, 0, 255).astype(np.uint8)
out[:, :, 1] = np.clip(Lm * 1.00, 0, 255).astype(np.uint8)
out[:, :, 2] = np.clip(Lm * 1.045, 0, 255).astype(np.uint8)

rgba = np.dstack([out, alpha])
img = Image.fromarray(rgba, "RGBA")
# borde suave (1 px) y recorte al contenido
img.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(0.7)))
bbox = img.getchannel("A").getbbox()
img = img.crop(bbox)
img.save(OUT)

body = alpha > 0
n_body = int(body.sum())
negro = int(((L < 70) & body).sum())
print(f"pack {w}x{h} | fondo {int(bg.sum())} | cuerpo {n_body} px")
print(f"figura {OUT} {img.size} | opacos>=250: {int((np.asarray(img)[:,:,3]>=250).sum())} "
      f"({100.0*(np.asarray(img)[:,:,3]>=250).sum()/img.size[0]/img.size[1]:.1f}%)")
print(f"px oscuros conservados (texto/cantos): {negro}")
