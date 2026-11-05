#!/usr/bin/env python3
"""norma_legibilidad.py — verificador de la NORMA DE LEGIBILIDAD v8 «SIN CAJAS» (Joko Lab, 04-11-2026).

Cambio de fondo respecto a la v6: la legibilidad ya NO se gana con un panel
blanco detrás del texto (el usuario lo ha vetado: «nada de cajas o recuadros»),
sino con un HALO DE LUZ (text-shadow) y tinta oscura sobre la foto real.
Eso obliga a cambiar la medida: comparar el color declarado contra el fondo
dominante no ve el halo y daría un falso NO CUMPLE. Aquí se mide lo que el ojo
ve, sobre el PNG final: dentro de la caja del nodo, la letra (percentil 5 de
luminancia) contra el fondo inmediato (percentil 95).

Reglas
  R1 suelo      ningún texto de lectura < 12 px
  R2 duro       ningún nodo por debajo de 3,0:1
  R3 objetivo   texto normal -> 4,5:1. Entre 3,0 y 4,5 se admite solo si es
                texto grande (>=24 px), nota legal, o etiqueta SVG sobre forma
                opaca; se reporta como AVISO. En SVG el percentil 5/95 mezcla
                la losa con el fondo exterior y no es fiable, por eso no bloquea.
  R4 lienzo     nada desborda el alto (1440 px por defecto)

Uso:
  /usr/bin/python3 tools/norma_legibilidad.py <ficha.html> --png <ficha.png> [--json out]
  exit 0 = CUMPLE | 2 = NO CUMPLE

LIMITE DECLARADO del método: percentiles, no color plano WCAG. En 12-13 px el
antialiasing mezcla letra y fondo y el ratio sale algo optimista. Sirve para
comparar variantes con el mismo método y para detectar el texto ilegible real.
"""
import argparse, json, pathlib, re, subprocess, sys, tempfile
from PIL import Image

TOOLS = pathlib.Path(__file__).resolve().parent
PY = '/usr/bin/python3'
LEGAL = ('fuente-line', 'nota-fondo', 'sello', 'donde', 'caveat', 'span.f', 'div.f')
DECO = ('·', '-', '—', '|', '/')


def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def ratio_de(box):
    raw = box.tobytes()          # sin getdata(): Pillow 11 lo marca obsoleto y ensucia la salida
    L = sorted(0.2126 * lin(raw[k]) + 0.7152 * lin(raw[k + 1]) + 0.0722 * lin(raw[k + 2])
               for k in range(0, len(raw), 3))
    n = len(L)
    lo = L[max(0, int(0.05 * n) - 1)]
    hi = L[min(n - 1, int(0.95 * n))]
    if hi < lo:
        lo, hi = hi, lo
    return (hi + 0.05) / (lo + 0.05)


def _rgb(s):
    """'rgb(255, 255, 255)' / 'rgba(0,0,0,0.5)' -> (r,g,b) o None si hay alfa."""
    m = re.match(r'rgba?\(([^)]+)\)', (s or '').strip())
    if not m:
        return None
    p = [x for x in re.split(r'[,\s/]+', m.group(1)) if x.strip()]
    if len(p) < 3:
        return None
    try:
        v = [float(x) for x in p[:4]]
    except ValueError:
        return None
    if len(v) > 3 and v[3] < 0.99:
        return None
    return v[:3]


def ratio_css(fg, bg):
    """Ratio WCAG del par DECLARADO en el CSS (color de texto vs fondo efectivo).
    Es el que manda: el percentil sobre el PNG mezcla antialiasing y sale optimista."""
    a, b = _rgb(fg), _rgb(bg)
    if not a or not b:
        return None
    la = 0.2126 * lin(a[0]) + 0.7152 * lin(a[1]) + 0.0722 * lin(a[2])
    lb = 0.2126 * lin(b[0]) + 0.7152 * lin(b[1]) + 0.0722 * lin(b[2])
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--png', required=True)
    ap.add_argument('--alto', type=int, default=1440)
    ap.add_argument('--json')
    a = ap.parse_args()

    html = pathlib.Path(a.html).expanduser().resolve()
    png = pathlib.Path(a.png).expanduser().resolve()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='norma_leg_'))
    inv_path = tmp / 'inv.json'

    r = subprocess.run([PY, str(TOOLS / 'inventario_legibilidad.py'), str(html), '--json', str(inv_path)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not inv_path.exists():
        print('ERROR: el inventario falló\n' + (r.stdout + r.stderr)[-800:])
        return 2
    inv = json.loads(inv_path.read_text())
    items = inv['items']
    alto = (inv.get('meta') or {}).get('alto') or (inv.get('meta') or {}).get('scrollHeight')

    img = Image.open(png).convert('RGB')
    W, H = img.size
    filas = []
    for i in items:
        x, y, w, h = [int(i.get(k) or 0) for k in ('x', 'y', 'w', 'h')]
        if w < 2 or h < 2:
            continue
        x0, y0 = max(0, x - 2), max(0, y - 2)
        x1, y1 = min(W, x + w + 2), min(H, y + h + 2)
        if x1 <= x0 or y1 <= y0:
            continue          # nodo fuera del PNG renderizado
        box = img.crop((x0, y0, x1, y1))
        if box.size[0] < 2 or box.size[1] < 2:
            continue
        r_px = ratio_de(box)
        r_css = ratio_css(i.get('color'), i.get('bg'))
        r = r_px if r_css is None else min(r_px, r_css)
        filas.append({'ratio': round(r, 2), 'ratio_px': round(r_px, 2),
                      'ratio_css': None if r_css is None else round(r_css, 2),
                      'px': float(i.get('px') or 0),
                      't': (i.get('t') or '')[:40], 'cls': str(i.get('cls', ''))})
    if not filas:
        print('ERROR: no se pudo medir ningún nodo sobre el PNG')
        return 2

    chicos = [i for i in items if i['px'] < 12 and (i['t'] or '').strip() not in DECO]
    duros, avisos = [], []
    for f in filas:
        if (f['t'] or '').strip() in DECO:
            continue
        legal = any(k in f['cls'] for k in LEGAL)
        es_svg = 'SVG' in f['cls'] or 'svg' in f['cls']
        objetivo = 3.0 if (f['px'] >= 24 or legal) else 4.5
        if f['ratio'] < 3.0:
            duros.append(f)
        elif f['ratio'] + 1e-9 < objetivo and not (es_svg or legal):
            avisos.append(f)
    desborda = bool(alto and alto > a.alto)
    ok = not chicos and not duros and not desborda

    print(f'NORMA LEGIBILIDAD v8 (sin cajas) — {html.name}')
    print(f'  nodos medidos       {len(filas)}   (inventario {len(items)})')
    print(f'  R1 px < 12          {len(chicos)}' + ('' if not chicos else '  ' + str([(c['t'][:18], c['px']) for c in chicos[:5]])))
    print(f'  R2 bajo 3,0:1       {len(duros)}' + ('' if not duros else '  ' + str([(d['ratio'], d['px'], d['t'][:18], d['cls']) for d in duros[:5]])))
    print(f'  R3 avisos 3-4,5:1   {len(avisos)}' + ('' if not avisos else '  ' + str([(v['ratio'], v['px'], v['t'][:16], v['cls']) for v in avisos[:5]])))
    if alto:
        print(f'  R4 alto             {alto} / {a.alto}  {"DESBORDA" if desborda else "cabe"}')
    else:
        print('  R4 alto             NO MEDIDO aqui -> lo comprueba validar_ficha_preenvio.py')
    peor = min(filas, key=lambda f: f['ratio'])
    print(f'  peor nodo           {peor["ratio"]:.2f}:1  {peor["px"]}px  {peor["t"][:40]}  [{peor["cls"]}]')
    if avisos:
        linea_av = '; '.join(f'{v["t"][:18].strip()} [{v["cls"]}] {v["ratio"]:.2f}:1 {v["px"]:.0f}px'
                             for v in avisos)
    else:
        linea_av = 'ninguno'
    print(f'  AVISOS 3-4,5:1      {linea_av}')
    print(f'VEREDICTO NORMA {"CUMPLE" if ok else "NO CUMPLE"}')
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {'ok': ok, 'nodos': len(filas), 'chicos': chicos, 'duros': duros, 'avisos': avisos,
             'resumen_avisos': linea_av,
             'alto': alto, 'desborda': desborda, 'rows': filas}, ensure_ascii=False, indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
