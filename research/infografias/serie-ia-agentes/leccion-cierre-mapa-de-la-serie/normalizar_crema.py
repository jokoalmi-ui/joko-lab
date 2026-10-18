#!/usr/bin/env python3
"""normalizar_crema.py — deja el fondo del arte en el crema EXACTO de la serie.

Por que existe
--------------
Las slides del carrusel tienen fondo #F5EFE6 y el arte (SDXL) se pega dentro.
Si el fondo del PNG no coincide, se ve un rectangulo alrededor del objeto.
El primer intento (umbral global de saturacion/brillo) no sirvio: el beige que
genera SDXL es mas oscuro de lo previsto y solo pillo 1 de 4 fondos.

Como lo hace ahora
------------------
Relleno (flood fill) desde 8 puntos del borde: pinta la region de fondo
CONECTADA al borde y la sustituye por el crema exacto. Umbral adaptativo de una
escalera fija (30, 45, 60) y se queda con el PRIMER valor que deja el anillo de
borde en crema (tolerancia 12). Los trazos negros y el acento naranja no son
contiguos al fondo con color parecido, asi que no se tocan.

No borra ni sobrescribe el original: escribe <nombre>-crema.png (el que usa
build_slides.py). Imprime, por fichero, el umbral usado, el % de pixeles
cambiados y el color medio del borde antes/despues (verificacion, no fe).
"""
import pathlib
import sys

from PIL import Image, ImageChops, ImageDraw

CREMA = (245, 239, 230)  # #F5EFE6
SENTINELA = (255, 0, 255)
UMBRALES = (30, 45, 60)
TOL = 12


def borde_medio(im, px=12):
    """Color medio del anillo de borde de la imagen."""
    w, h = im.size
    zonas = [(0, 0, w, px), (0, h - px, w, h), (0, 0, px, h), (w - px, 0, w, h)]
    tot = [0, 0, 0]
    n = 0
    for z in zonas:
        for p in im.crop(z).getdata():
            tot[0] += p[0]
            tot[1] += p[1]
            tot[2] += p[2]
            n += 1
    return tuple(round(t / n) for t in tot)


def dif(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def semillas(w, h):
    return [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
            (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]


def normalizar(f, destino):
    im = Image.open(f).convert("RGB")
    antes = borde_medio(im)
    for t in UMBRALES:
        work = im.copy()
        for s in semillas(*im.size):
            ImageDraw.floodfill(work, s, SENTINELA, thresh=t)
        r, g, b = work.split()
        m_r = r.point(lambda p: 255 if p == 255 else 0).convert("1")
        m_g = g.point(lambda p: 255 if p == 0 else 0).convert("1")
        m_b = b.point(lambda p: 255 if p == 255 else 0).convert("1")
        m = ImageChops.logical_and(ImageChops.logical_and(m_r, m_g), m_b)
        crema_img = Image.new("RGB", im.size, CREMA)
        out = Image.composite(crema_img, im, m)
        despues = borde_medio(out)
        if dif(despues, CREMA) <= TOL:
            n = m.convert("L").histogram()[255]
            out.save(destino)
            print(f"{f.name} -> {destino.name}: umbral {t} | {n}/{im.size[0]*im.size[1]} px "
                  f"({100*n/(im.size[0]*im.size[1]):.1f}%) | borde {antes} -> {despues} | OK")
            return True
    print(f"{f.name}: FALLO — ningun umbral de {UMBRALES} deja el borde en crema "
          f"(quedo en {despues}, objetivo {CREMA}, tol {TOL})")
    return False


def main():
    d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    ficheros = sorted(p for p in d.glob("*.png") if not p.stem.endswith("-crema"))
    if not ficheros:
        print(f"no hay PNG en {d}")
        return 1
    ok = 0
    for f in ficheros:
        dest = f.with_name(f.stem + "-crema.png")
        if normalizar(f, dest):
            ok += 1
    print(f"\nnormalizados {ok}/{len(ficheros)}; borde en crema (tol {TOL}): {ok}/{len(ficheros)}")
    return 0 if ok == len(ficheros) else 1


if __name__ == "__main__":
    sys.exit(main())
