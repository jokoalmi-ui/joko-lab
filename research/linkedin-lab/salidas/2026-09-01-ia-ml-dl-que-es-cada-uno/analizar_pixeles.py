#!/usr/bin/env python3
"""Comparar slides nuevas vs ejemplo validado (20-ago): colores únicos y variación.
Determina si el render tiene contenido real (texto/gráficos) SIN depender de GLM."""
import os
from PIL import Image

NUEVAS = "/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-01-ia-ml-dl-que-es-cada-uno"
REF = "/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-08-20-lancedb-de-26-gb-a-320-mb-sin-tocar-una-sola-fila"

def analizar(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # Muestrear 1 de cada 4 píxeles (rápido) y contar colores únicos
    small = im.resize((w // 4, h // 4))
    colores = small.getcolors(maxcolors=1_000_000)
    n_colores = len(colores) if colores else ">1M"
    # Variación por filas (texto/gráficos generan filas con mucho contraste)
    g = im.convert("L")
    px = g.load()
    filas_contraste = 0
    for y in range(0, h, 8):
        fila = [px[x, y] for x in range(0, w, 8)]
        if max(fila) - min(fila) > 40:
            filas_contraste += 1
    return f"{os.path.basename(path):>12}  {w}x{h}  colores={n_colores:>8}  filas_contraste={filas_contraste}/{h//8}"

print("=== NUEVAS (01-sep) ===")
for i in range(1, 7):
    p = os.path.join(NUEVAS, f"slide-{i:02d}.png")
    print(analizar(p) if os.path.exists(p) else f"falta {p}")

print("\n=== REFERENCIA VALIDADA (20-ago) ===")
for i in range(1, 7):
    p = os.path.join(REF, f"slide-{i:02d}.png")
    print(analizar(p) if os.path.exists(p) else f"falta {p}")
