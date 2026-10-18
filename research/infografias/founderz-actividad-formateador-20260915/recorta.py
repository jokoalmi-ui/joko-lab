#!/usr/bin/env python3
"""Recorta el blanco/crema sobrante del render PNG (determinista, sin juicios visuales)."""
import sys
from PIL import Image

ruta = sys.argv[1]
im = Image.open(ruta).convert("RGB")
w, h = im.size
fondo = im.getpixel((3, 3))


def fila_es_fondo(y):
    for x in range(0, w, 7):
        p = im.getpixel((x, y))
        if abs(p[0] - fondo[0]) + abs(p[1] - fondo[1]) + abs(p[2] - fondo[2]) > 18:
            return False
    return True


arriba, abajo = None, None
for y in range(h):
    if not fila_es_fondo(y):
        arriba = y
        break
for y in range(h - 1, -1, -1):
    if not fila_es_fondo(y):
        abajo = y
        break

if arriba is None or abajo is None:
    print("PNG vacío: no hay contenido (¿render fallido?)")
    sys.exit(1)

margen = 18
arriba = max(0, arriba - margen)
abajo = min(h - 1, abajo + margen)
recorte = im.crop((0, 0, w, abajo + 1))
recorte.save(ruta)
print(f"fondo={fondo} alto_original={h} alto_recortado={recorte.size[1]} nuevas_esquinas={recorte.getpixel((2, 2))},{recorte.getpixel((w - 3, recorte.size[1] - 3))}")
