#!/usr/bin/env python3
"""Compone los 29 fotogramas 1080x1920 del album AMAIUR.

Patron: fondo = la misma foto a pantalla completa, desenfocada (pero reconocible)
y algo oscurecida; frente = la foto INTEGRA encajada sin recortar, centrada, con
sombra suave y un borde blanco fino que la separa limpiamente del fondo.
Ninguna foto pierde un pixel. Solo lectura sobre los originales.

v2: blur 45->30 y brillo 0.45->0.62 (el fondo se leia como banda negra) y borde
    blanco de 3 px (el corte foto/fondo no quedaba limpio).
"""
import os
import glob
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw

ORIGEN = "/mnt/ssd_ia_datos/exports/AMAIUR"
DESTINO = "/home/jokoalmi/joko-lab/research/videos/amaiur-20260916/frames"
W, H = 1080, 1920
MARGEN = 40
RADIO_BLUR = 30
BRILLO_FONDO = 0.62
SOMBRA_BLUR = 22
SOMBRA_ALPHA = 130
BORDE = 3

os.makedirs(DESTINO, exist_ok=True)


def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im2 = im.resize((max(1, int(im.width * r + 0.5)), max(1, int(im.height * r + 0.5))), Image.LANCZOS)
    x = (im2.width - w) // 2
    y = (im2.height - h) // 2
    return im2.crop((x, y, x + w, y + h))


def contain(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * r + 0.5)), max(1, int(im.height * r + 0.5))), Image.LANCZOS)


ficheros = sorted(glob.glob(os.path.join(ORIGEN, "*.jpeg")),
                  key=lambda p: int(os.path.splitext(os.path.basename(p))[0]))
print(f"originales encontrados: {len(ficheros)}")

for i, f in enumerate(ficheros, 1):
    base = os.path.splitext(os.path.basename(f))[0]
    im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")

    fondo = cover(im, W, H).filter(ImageFilter.GaussianBlur(RADIO_BLUR))
    fondo = ImageEnhance.Brightness(fondo).enhance(BRILLO_FONDO)
    fondo = ImageEnhance.Color(fondo).enhance(0.9)

    caja_w, caja_h = W - 2 * MARGEN, H - 2 * MARGEN
    frente = contain(im, caja_w, caja_h)
    px, py = (W - frente.width) // 2, (H - frente.height) // 2

    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).rectangle(
        [px + 8, py + 10, px + frente.width + 8, py + frente.height + 10], fill=SOMBRA_ALPHA)
    sombra = sombra.filter(ImageFilter.GaussianBlur(SOMBRA_BLUR))

    lienzo = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), fondo, sombra)
    lienzo.paste(frente, (px, py))
    ImageDraw.Draw(lienzo).rectangle(
        [px - BORDE, py - BORDE, px + frente.width + BORDE - 1, py + frente.height + BORDE - 1],
        outline=(255, 255, 255), width=BORDE)

    salida = os.path.join(DESTINO, f"frame_{i:02d}.png")
    lienzo.save(salida, "PNG")
    print(f"  [{i:02d}/29] {base:>4s}.jpeg -> frente {frente.width}x{frente.height}  {os.path.getsize(salida)//1024} KB")

print(f"\ncompuestos: {len(ficheros)} PNG en {DESTINO}")
