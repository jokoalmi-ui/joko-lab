#!/usr/bin/env python3
"""recortar_silueta.py — aísla la FIGURA del frasco por FLOOD-FILL del fondo exterior.

Método exigido por la skill perfume-del-dia desde 08-oct-2026 (el recorte por umbral de
distancia a un color de fondo deja el VIDRIO CLARO semitransparente; medido: alfa medio
del cuerpo 48,3 y 0,9 % de píxeles opacos -> frasco fantasma).

Aquí la transparencia va SOLO fuera de la silueta:
  1) modelo del fondo = superficie lineal ajustada por mínimos cuadrados sobre el MARCO
     de la imagen (bandas laterales y superior/inferior), que absorbe el degradado y el
     viñeteado del estudio (medido: residual del marco media 5,6 / p95 13,3)
  2) bg_like = distancia al modelo < T
  3) flood-fill geodésico desde el BORDE de la imagen sobre bg_like -> "fuera"
     (todo lo NO alcanzado desde el borde = botella; los huecos internos quedan llenos)
  4) alpha = 0 fuera / 255 dentro (+ blur 1,2 px), recorte al bbox robusto de la figura

Uso: python3 recortar_silueta.py <entrada.jpg|png> <salida.png> [T]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def dilatar(m):
    out = m.copy()
    out[1:, :] |= m[:-1, :]
    out[:-1, :] |= m[1:, :]
    out[:, 1:] |= m[:, :-1]
    out[:, :-1] |= m[:, 1:]
    return out


def recortar(src, dst, T=40, marco=80, min_px=20):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    m = (xx < marco) | (xx >= w - marco) | (yy < marco) | (yy >= h - marco)
    X = np.stack([np.ones_like(xx), xx, yy], -1)
    pred = np.zeros_like(a)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(X[m], a[m][:, c], rcond=None)
        pred[:, :, c] = X @ coef
    d = np.abs(a - pred).sum(2)

    fig = d >= T
    filas = np.where(fig.sum(1) > min_px)[0]
    cols = np.where(fig.sum(0) > min_px)[0]
    y0, y1, x0, x1 = filas[0], filas[-1] + 1, cols[0], cols[-1] + 1
    print(f"bbox robusto: x {x0}-{x1} y {y0}-{y1}  ({x1-x0}x{y1-y0})")

    # fuera = flood-fill geodésico desde el borde sobre bg_like; el resto es botella
    # (los huecos internos de la botella NO son alcanzables desde el borde -> quedan llenos)
    bg = d < T
    fuera = np.zeros((h, w), bool)
    fuera[0, :] = bg[0, :]
    fuera[-1, :] = bg[-1, :]
    fuera[:, 0] = bg[:, 0]
    fuera[:, -1] = bg[:, -1]
    it = 0
    for it in range(20000):
        nuevo = dilatar(fuera) & bg
        if nuevo.sum() == fuera.sum():
            break
        fuera = nuevo

    # quedarse con la componente conexa de la BOTELLA (semilla = píxel más distinto del
    # fondo) para descartar motas de viñeteado fuera del frasco
    cand = ~fuera
    sy, sx = np.unravel_index(np.argmax(d * cand), d.shape)
    main = np.zeros((h, w), bool)
    main[sy, sx] = True
    it2 = 0
    for it2 in range(20000):
        nuevo = dilatar(main) & cand
        if nuevo.sum() == main.sum():
            break
        main = nuevo

    filas = np.where(main.sum(1) > min_px)[0]
    cols = np.where(main.sum(0) > min_px)[0]
    y0, y1, x0, x1 = filas[0], filas[-1] + 1, cols[0], cols[-1] + 1
    print(f"semilla botella ({sx},{sy}) | bbox final: x {x0}-{x1} y {y0}-{y1}  ({x1-x0}x{y1-y0})")

    alpha_sub = main[y0:y1, x0:x1]
    alpha = np.where(alpha_sub, 255, 0).astype(np.uint8)
    rgb = a[y0:y1, x0:x1].astype(np.uint8)
    img = Image.fromarray(np.dstack([rgb, alpha]), "RGBA")
    img.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(1.2)))
    img.save(dst)

    al = np.asarray(img.getchannel("A"))
    print(f"figura OK: {dst} | tamaño {img.size} | iteraciones fuera={it} main={it2}")
    print(f"  alfa medio {al.mean():.1f} | % opacos(>=250) {100*(al>=250).mean():.1f} | % transparentes(<=5) {100*(al<=5).mean():.1f}")
    return img


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    t = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    recortar(sys.argv[1], sys.argv[2], t)
