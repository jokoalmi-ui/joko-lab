#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recorte_silueta.py — FIGURA del frasco por FLOOD-FILL del fondo exterior.

Método exigido por la lección del 08-oct-2026 (Naxos): en frascos de VIDRIO CLARO
sobre blanco, el recorte por distancia al blanco (recortar_frasco.py) vuelve
semitransparente el propio vidrio y el frasco queda fantasma. Aquí la
transparencia va SOLO fuera de la botella: se inunda el fondo desde los bordes
(píxeles casi blancos) y todo lo no alcanzado es frasco OPACO (alfa 255).

USO: python3 recorte_silueta.py <packshot> <salida.png> [thr_suma_abs] [blur]
     thr_suma_abs (def. 60): |r-255|+|g-255|+|b-255| para considerar "fondo"
"""
import sys
from collections import deque
from PIL import Image, ImageFilter


def silueta(src, dst, thr=60, blur=0.8):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (abs(r - 255) + abs(g - 255) + abs(b - 255)) <= thr:
                bg[y * w + x] = 1
    ext = bytearray(w * h)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if bg[i] and not ext[i]:
                ext[i] = 1
                dq.append(i)
    for y in range(h):
        for x in (0, w - 1):
            i = y * w + x
            if bg[i] and not ext[i]:
                ext[i] = 1
                dq.append(i)
    while dq:
        i = dq.popleft()
        x = i % w
        y = i // w
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                j = ny * w + nx
                if bg[j] and not ext[j]:
                    ext[j] = 1
                    dq.append(j)
    out = Image.new("RGBA", (w, h))
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            op[x, y] = (r, g, b, 0 if ext[y * w + x] else 255)
    bbox = out.getchannel("A").getbbox()
    out = out.crop(bbox)
    if blur > 0:
        out.putalpha(out.getchannel("A").filter(ImageFilter.GaussianBlur(blur)))
    out.save(dst)
    n_sil = sum(1 for i in range(w * h) if not ext[i])
    return bbox, out.size, 100.0 * n_sil / (w * h)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    thr = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    blur = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
    bbox, size, pct = silueta(src, dst, thr, blur)
    print("silueta OK: %s | bbox %s | tamano %s | silueta %.1f%% del lienzo" % (dst, bbox, size, pct))
