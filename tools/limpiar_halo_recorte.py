#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""limpiar_halo_recorte.py — quita el HALO claro del filo de una figura con alfa.

PROBLEMA (medido 27-oct-2026, Basso): el recorte por flood-fill deja en el filo
de la silueta los píxeles de ANTIALIASING del packshot original — mezcla del
color del frasco con el BLANCO del estudio. Son opacos (alfa 255), así que el
alfa está bien, pero al componer sobre un fondo oscuro se ven como un halo
blanco/grisáceo pegado al contorno. El blur del alfa de `recorte_silueta.py`
lo empeora: los píxeles semitransparentes conservan el RGB del fondo original.

SOLUCIÓN: descontaminación de color del filo. El color de cada píxel del borde
se sustituye por la media de los píxeles OPACOS interiores vecinos (sin tocar
el alfa), en N capas hacia dentro. Opcionalmente se erode 1-2 px el alfa para
cortar el filo contaminado.

MIDE ANTES Y DESPUÉS con la misma métrica, para no fiarse de la impresión:
  L media del borde opaco y % de píxeles casi-blancos (L>230 y sat<0.10).

USO:
  python3 limpiar_halo_recorte.py <figura.png> <salida.png> [--capas N] [--erode N]
Salida: métricas antes/después por stdout. No sobrescribe la entrada salvo que
se indique la misma ruta (no recomendado: RULE-018, sufijo nuevo).
"""
import sys
from PIL import Image
import numpy as np


def _dilatar(m, radio):
    out = np.zeros_like(m)
    for dy in range(-radio, radio + 1):
        for dx in range(-radio, radio + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def metricas(rgba):
    """L media del borde opaco y % casi-blanco en el borde."""
    alfa = rgba[..., 3]
    rgb = rgba[..., :3].astype(float)
    L = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    mx, mn = rgb.max(2), rgb.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    borde = (alfa > 250) & _dilatar(alfa < 10, 2)
    n = int(borde.sum())
    if not n:
        return 0, 0.0, 0.0, 0.0
    blancos = int(((L > 230) & (sat < 0.10))[borde].sum())
    return n, float(L[borde].mean()), 100.0 * blancos / n, float(np.percentile(L[borde], 95))


def limpiar(rgba, capas=3, erode=1):
    a = rgba.copy()
    alfa = a[..., 3]
    # 1) erosión opcional del alfa: corta el filo contaminado
    if erode:
        for _ in range(erode):
            alfa = np.where(_dilatar(alfa < 128, 1), 0, alfa).astype(np.uint8)
        a[..., 3] = alfa
    rgb = a[..., :3].astype(float)
    opaco = alfa > 250
    # 2) descontaminación por capas, de fuera hacia dentro
    actual = opaco & _dilatar(alfa < 10, 2)
    for _ in range(capas):
        if not actual.any():
            break
        valido = opaco & ~actual
        acc = np.zeros_like(rgb)
        cnt = np.zeros(alfa.shape, dtype=float)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dy == 0 and dx == 0:
                    continue
                m = np.roll(np.roll(valido.astype(float), dy, 0), dx, 1)
                acc += np.roll(np.roll(rgb, dy, 0), dx, 1) * m[..., None]
                cnt += m
        hay = cnt > 0
        nuevo = acc / np.maximum(cnt, 1)[..., None]
        rgb[hay] = nuevo[hay]
        # la siguiente capa es el anillo interior contiguo
        actual = _dilatar(actual, 1) & opaco
    a[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return a


def limpiar_color(rgba, pasadas=8):
    """Descontamina el COLOR del filo SIN tocar el alfa (conserva el suavizado).

    Corrige tanto los opacos del borde como los SEMITRANSPARENTES: en un recorte
    por flood-fill el semitransparente conserva el color del fondo original
    (blanco), que es justo lo que se ve como halo. El alfa se queda intacto.
    """
    a = rgba.copy()
    alfa = a[..., 3]
    rgb = a[..., :3].astype(float)
    transparente = alfa < 10
    opaco = alfa > 250
    # zona a corregir: todo pixel visible a <=4 px de la transparencia
    objetivo = (alfa > 12) & _dilatar(transparente, 4)
    valido = opaco & ~objetivo          # núcleo opaco limpio: fuente de color
    if not valido.any():
        return a
    for _ in range(pasadas):
        pend = objetivo & ~valido
        if not pend.any():
            break
        acc = np.zeros_like(rgb)
        cnt = np.zeros(alfa.shape, dtype=float)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy == 0 and dx == 0:
                    continue
                m = np.roll(np.roll(valido.astype(float), dy, 0), dx, 1)
                acc += np.roll(np.roll(rgb, dy, 0), dx, 1) * m[..., None]
                cnt += m
        rell = pend & (cnt > 0)
        nuevo = acc / np.maximum(cnt, 1)[..., None]
        rgb[rell] = nuevo[rell]
        valido = valido | rell
    a[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return a


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    capas, erode = 3, 1
    for arg in sys.argv[3:]:
        if arg.startswith("--capas="):
            capas = int(arg.split("=")[1])
        elif arg.startswith("--erode="):
            erode = int(arg.split("=")[1])
    im = Image.open(src)
    if im.mode != "RGBA":
        print(f"ERROR: {src} no tiene alfa (mode={im.mode}); no es una figura recortada")
        sys.exit(3)
    a0 = np.array(im.convert("RGBA"))
    n0, l0, w0, p0 = metricas(a0)
    a1 = limpiar(a0, capas, erode)
    n1, l1, w1, p1 = metricas(a1)
    Image.fromarray(a1, "RGBA").save(dst)
    print(f"entrada : {src}  {im.size}")
    print(f"ANTES   : borde {n0} px | L media {l0:.1f} | p95 {p0:.1f} | casi-blanco {w0:.1f} %")
    print(f"DESPUES : borde {n1} px | L media {l1:.1f} | p95 {p1:.1f} | casi-blanco {w1:.1f} %")
    print(f"salida  : {dst}  (capas={capas}, erode={erode})")
