#!/usr/bin/env python3
"""Contraste EFECTIVO medido sobre el PNG final, no sobre el CSS.

Por que existe: los medidores anteriores comparan el color declarado del texto
contra el fondo dominante. Cuando la legibilidad se gana con HALO (text-shadow)
o con degradados, ese calculo no ve nada y da un falso NO CUMPLE. Este mide lo
que el ojo ve: dentro de la caja del nodo, el pixel oscuro (letra) contra el
claro (fondo inmediato ya afectado por el halo).

Metodo: luminancia relativa WCAG sobre sRGB; letra = percentil 5 de la caja,
fondo = percentil 95 de la misma caja. Ratio = (Lf+0.05)/(Ll+0.05).
LIMITE DECLARADO: es un percentil, no un color plano. En textos de 12-13 px el
antialiasing mezcla letra y fondo y el ratio sale algo optimista. Sirve para
comparar variantes entre si con el mismo metodo, no como certificado WCAG.

Uso: contraste_efectivo.py <inventario.json> <render.png> [--json salida]
"""
import json, sys
import numpy as np
from PIL import Image

def lum(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]

inv = json.load(open(sys.argv[1]))
img = np.asarray(Image.open(sys.argv[2]).convert('RGB'))
H, W = img.shape[:2]
nodos = inv['nodos'] if isinstance(inv, dict) and 'nodos' in inv else inv

filas = []
for n in nodos:
    try:
        x, y, w, h = int(n['x']), int(n['y']), int(n['w']), int(n['h'])
    except Exception:
        continue
    if w < 2 or h < 2:
        continue
    pad = 2
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
    box = img[y0:y1, x0:x1]
    if box.size == 0:
        continue
    L = lum(box).ravel()
    Ll = float(np.percentile(L, 5))
    Lf = float(np.percentile(L, 95))
    if Lf < Ll:
        Ll, Lf = Lf, Ll
    ratio = (Lf + 0.05) / (Ll + 0.05)
    px = float(n.get('px') or 0)
    need = 3.0 if (px >= 24 or 'f' in str(n.get('cls', '')) and px >= 12 and False) else 4.5
    if px >= 24:
        need = 3.0
    filas.append({'t': (n.get('t') or '')[:28], 'cls': n.get('cls', ''), 'px': px,
                  'ratio': round(ratio, 2), 'need': need})

mal = [f for f in filas if f['ratio'] < f['need']]
mal.sort(key=lambda f: f['ratio'])
peor = min(filas, key=lambda f: f['ratio'])
print(f'nodos medidos        {len(filas)}')
print(f'R1 px < 12           {sum(1 for f in filas if f["px"] < 12)}')
print(f'bajo umbral          {len(mal)}')
for f in mal[:8]:
    print(f'   {f["ratio"]:5.2f}:1  {f["px"]:5.1f}px  {f["t"]!r}  [{f["cls"]}] (min {f["need"]})')
print(f'peor nodo            {peor["ratio"]:.2f}:1  {peor["px"]}px  {peor["t"]}')
print('VEREDICTO ' + ('CUMPLE' if not mal else 'NO CUMPLE'))
if '--json' in sys.argv:
    p = sys.argv[sys.argv.index('--json') + 1]
    json.dump({'nodos': filas, 'mal': mal, 'peor': peor}, open(p, 'w'), ensure_ascii=False, indent=1)
sys.exit(0 if not mal else 2)
