#!/usr/bin/env python3
# Verifica que la base hoja-cuaderno-base.png NO se tocó en los renders narr-*.png
# Compara 4 zonas SIN contenido superpuesto entre cada render y el original.
# Esperado: 0.00% de píxeles distintos (umbral 8 por canal) en todas las zonas.
# Uso: python3 verificar_base.py  (PIL puro, sin numpy)
import os
from PIL import Image

SLIDES = "/home/jokoalmi/joko-lab/tfm/slides"
ORIG = os.path.join(SLIDES, "hoja-cuaderno-base.png")
UMBRAL = 8

# Zonas sin contenido superpuesto (medidas del original 1824x2310)
ZONAS = {
    "espiral_sup_izq": (0, 0, 190, 320),
    "borde_derecho": (1760, 0, 1823, 2310),
    "margen_inferior": (0, 2280, 1823, 2309),
    "esquina_inf_der": (1760, 2280, 1823, 2309),
}

def diff_pct(a_img, b_img, box):
    x1, y1, x2, y2 = box
    a = a_img.crop(box).convert("RGB").load()
    b = b_img.crop(box).convert("RGB").load()
    w, h = x2 - x1, y2 - y1
    total = w * h
    distintos = 0
    for yy in range(h):
        for xx in range(w):
            pa = a[xx, yy]
            pb = b[xx, yy]
            if (abs(pa[0]-pb[0]) > UMBRAL or abs(pa[1]-pb[1]) > UMBRAL or abs(pa[2]-pb[2]) > UMBRAL):
                distintos += 1
    return 100.0 * distintos / total

orig = Image.open(ORIG)

narr = sorted(f for f in os.listdir(SLIDES) if f.startswith("narr-") and f.endswith(".png"))
for f in narr:
    path = os.path.join(SLIDES, f)
    try:
        r = Image.open(path)
    except Exception as e:
        print(f"{f}: ERROR abriendo ({e})")
        continue
    if r.size != orig.size:
        print(f"{f}: TAMAÑO {r.size} != {orig.size}  <-- REVISAR")
        continue
    partes = []
    ok = True
    for nombre, box in ZONAS.items():
        pct = diff_pct(orig, r, box)
        estado = "OK" if pct == 0.0 else ("<-- REVISAR" if pct > 0.05 else "~ok")
        if pct > 0.05:
            ok = False
        partes.append(f"{nombre}={pct:.2f}%{estado}")
    print(f"{f}: {'BASE INTACTA' if ok else 'POSIBLE CONTACTO'} | " + " | ".join(partes))
