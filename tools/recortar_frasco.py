#!/usr/bin/env python3
"""
recortar_frasco.py — Aísla la FIGURA del frasco de perfume de su fondo (packshot).

Validado 02-sep-2026 (Acqua di Sale, ficha v5): la botella recortada se ve GRANDE,
con transparencia real (se ve el fondo de la ficha a través del vidrio claro) y sin
marco blanco — método de distancia al blanco con rampa suave (el mismo que se usó
el 21-ago en gen_ficha_animada.sh).

USO:
  python3 recortar_frasco.py <packshot.png|webp> <salida.png> [umbral_opaco] [umbral_full]

  umbral_opaco (default 42): distancia RGB al blanco <= valor -> transparente
  umbral_full  (default 115): distancia >= valor -> opaco
  Entre ambos: rampa lineal (alpha suave, sin halo).

Reglas:
- El fondo del packshot debe ser BLANCO o casi blanco.
- NO usar en frascos con fondo de estudio oscuro/color (la distancia al blanco no aplica).
- El resultado es RGBA recortado al contenido (bbox del canal alpha) + blur 1.2px en bordes.
"""
import math
import sys
from PIL import Image, ImageFilter


def recortar(src: str, dst: str, umb_op: int = 42, umb_full: int = 115) -> tuple:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    out = Image.new("RGBA", (w, h))
    opx = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = math.sqrt((r - 255) ** 2 + (g - 255) ** 2 + (b - 255) ** 2)
            if d <= umb_op:
                a = 0
            elif d >= umb_full:
                a = 255
            else:
                a = int(255 * (d - umb_op) / (umb_full - umb_op))
            opx[x, y] = (r, g, b, a)
    bbox = out.getchannel("A").getbbox()
    out = out.crop(bbox)
    out.putalpha(out.getchannel("A").filter(ImageFilter.GaussianBlur(1.2)))
    out.save(dst)
    return bbox, out.size


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    op = int(sys.argv[3]) if len(sys.argv) > 3 else 42
    full = int(sys.argv[4]) if len(sys.argv) > 4 else 115
    bbox, size = recortar(src, dst, op, full)
    print(f"figura OK: {dst} | bbox original {bbox} | tamaño final {size}")
