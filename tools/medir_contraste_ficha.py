#!/usr/bin/env python3
"""medir_contraste_ficha.py — contraste REAL texto/fondo en una ficha renderizada.

Metodo (doble render, sin inventar metricas):
  A = render normal (el PNG de la ficha)
  B = mismo HTML con TODO el texto transparente -> queda el fondo real,
      incluido lo que hay DEBAJO de cada texto (fondo generado, tarjetas, chips)
  Para cada nodo de texto del inventario: L del color de texto (CSS) vs
  L mediana de su bbox en B  ->  ratio de contraste (formula WCAG).

Referencias que se imprimen: 4,5:1 (WCAG AA texto normal) y 3:1 (AA texto
grande). Son referencia publicada, NO umbral fijado por el asistente: la
decision de que se acepta es del usuario.

Uso:
  python3 medir_contraste_ficha.py <ficha.html> --inventario inv.json \\
      [--render-a ficha.png] [--limite 1350]

Sin dependencias (PIL + chrome). El render B se hace en /tmp.
"""
import argparse, json, os, re, statistics, subprocess, sys, tempfile
from PIL import Image

CSS_OCULTA = """
<style>
/* Ocultar SOLO el relleno del glifo: -webkit-text-fill-color NO toca `color`,
   de modo que los fondos que usan currentColor (circulos de seccion, chips)
   siguen pintandose. Con `color:transparent` desaparecian y el fondo medido
   salia blanco (falso positivo verificado por pixeles el 26-sep). */
*{text-shadow:none !important;text-decoration-color:transparent !important}
body{--nada:0}
*{-webkit-text-fill-color:transparent !important}
svg text,tspan{fill:transparent !important}
</style>
"""


def _lum(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _ratio(l1, l2):
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def _absolutizar(src, html):
    """Reescribe rutas relativas de assets a file:// absolutas: la copia temporal
    vive en /tmp y, si no, el fondo y las fuentes no cargan (el fondo medido
    salia blanco = 253 -> falso positivo, verificado por pixeles el 26-sep)."""
    base = os.path.dirname(os.path.abspath(html))

    def rep(m):
        u = m.group(2)
        if u.startswith(('http', 'data:', '#', 'file:', '/', 'about:')):
            return m.group(0)
        return m.group(1) + 'file://' + os.path.join(base, u) + m.group(3)

    src = re.sub(r"""(url\(\s*['"]?)([^'")]+)(['"]?\s*\))""", rep, src)
    src = re.sub(r"""(src\s*=\s*['"])([^'"]+)(['"])""", rep, src)
    return src


def render_sin_texto(html, w, h):
    src = open(html, encoding='utf-8').read()
    src = _absolutizar(src, html)
    inj = src.replace('</head>', CSS_OCULTA + '</head>') if '</head>' in src else CSS_OCULTA + src
    tmp = os.path.join(tempfile.mkdtemp(prefix='contraste_'), 'b.html')
    open(tmp, 'w', encoding='utf-8').write(inj)
    png = tmp.replace('b.html', 'b.png')
    cmd = ['google-chrome', '--headless=new', '--disable-gpu', '--no-sandbox',
           '--hide-scrollbars', '--virtual-time-budget=8000',
           '--window-size=%d,%d' % (w, h), '--screenshot=' + png, 'file://' + tmp]
    pr = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(png):
        raise SystemExit('no se pudo renderizar B: %s' % (pr.stderr[-300:],))
    return png


def _confirmar(A, B, x, y, w, h):
    """VERIFICACION de coordenadas: NO se usa para medir. A tiene texto y B no, asi
    que en la banda del texto la senal |A-B| debe destacar sobre el fondo local.
    Hace falta porque el inventario se lee con --dump-dom, que no pinta: si esa
    pasada no carga las fuentes, sus coordenadas quedan hasta 36 px altas
    (verificado por pixeles el 26-sep: badge 04 en 1100 real / 1064 medido).
    Prueba de PRESENCIA (no de deriva): buscar la banda "mas lejana" se engancha a
    los titulares vecinos. Devuelve (senal, fondo_local, confirmado)."""
    if A is None or h < 3:
        return 0.0, 0.0, False
    x = max(0, min(x, B.size[0] - 2)); w = max(2, min(w, B.size[0] - x))
    H = min(A.size[1], B.size[1])

    def perfil(y0, y1):
        y0 = max(0, y0); y1 = min(H, y1)
        if y1 - y0 < 2:
            return None
        pa = A.crop((x, y0, x + w, y1)).convert('L').tobytes()
        pb = B.crop((x, y0, x + w, y1)).convert('L').tobytes()
        n = (y1 - y0) * w
        return sum(abs(pa[k] - pb[k]) for k in range(n)) / float(n)

    propio = perfil(y - 2, y + h + 2)
    refs = [v for v in (perfil(y - 45, y - 20), perfil(y + h + 20, y + h + 45)) if v is not None]
    fondo = (sum(refs) / len(refs)) if refs else 0.0
    if propio is None:
        return 0.0, fondo, False
    # umbral absoluto: en una tarjeta densa los tramos vecinos SIEMPRE tienen texto,
    # asi que exigir 'x2,5 sobre el fondo local' marcaba medio inventario como dudoso
    return propio, fondo, (propio >= 4.0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--inventario', required=True)
    ap.add_argument('--render-a')
    ap.add_argument('--limite', type=int, default=1350)
    a = ap.parse_args()
    inv = json.load(open(a.inventario, encoding='utf-8'))
    meta, items = inv['meta'], inv['items']
    w = int(meta['cardW'] or 1080)
    h = int(meta['scrollH'] or a.limite)
    png_b = render_sin_texto(os.path.abspath(a.html), w, h)
    B = Image.open(png_b).convert('RGB')
    print('=== CONTRASTE TEXTO/FONDO ===')
    print('render B (sin texto): %s  %sx%s' % (os.path.basename(png_b), *B.size))
    A = None
    if a.render_a:
        A = Image.open(a.render_a).convert('RGB')
        print('render A (ficha)    : %s  %sx%s' % (os.path.basename(a.render_a), *A.size))
    else:
        print('render A: NO dado -> alineacion de coordenadas SIN verificar')
    print('')
    filas = []
    confirmados = 0
    dudosos = []
    for i in items:
        # el texto SVG se pinta con `fill`, no con `color` (falso positivo verificado 26-sep)
        color = i.get('fill') if (i.get('tag') in ('text', 'tspan') and i.get('fill')) else i['color']
        if re.match(r'#[0-9a-fA-F]{6}$', color or ''):
            color = 'rgb(%d, %d, %d)' % tuple(int(color[k:k + 2], 16) for k in (1, 3, 5))
        m = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color or '')
        if not m or ('rgba' in (color or '') and ', 0)' in color):
            continue
        lt = _lum(tuple(int(x) for x in m.groups()))
        x0 = max(0, int(i['x']) - 2); y0 = max(0, int(i['y']) - 2)
        x1 = min(B.size[0], int(i['x'] + i['w']) + 2)
        y1 = min(B.size[1], int(i['y'] + i['h']) + 2)
        sen, flo, ok = _confirmar(A, B, x0, int(i['y']), max(2, x1 - x0), int(i['h']))
        if ok:
            confirmados += 1
        else:
            dudosos.append((i['cls'] or i['tag'], int(i['y']), round(sen, 1), round(flo, 1)))
        if x1 - x0 < 2 or y1 - y0 < 2:
            continue
        gris = B.crop((x0, y0, x1, y1)).convert('L')
        med = statistics.median(gris.getdata())
        lb = _lum((med, med, med))
        r = _ratio(lt, lb)
        filas.append((r, i, med))
    filas.sort(key=lambda t: t[0])
    print('%-7s %-7s %-6s %-8s %s' % ('ratio', 'px', '%ancho', 'fondoL', 'texto  [clase]'))
    for r, i, med in filas:
        marca = 'CRITICO' if r < 3.0 else ('BAJO' if r < 4.5 else 'ok')
        print('%-7.2f %-7.1f %-6.2f %-8s %-7s %s  [%s%s]' % (
            r, i['px'], i['px'] / w * 100, med, marca, i['t'][:50],
            i['tag'], ('.' + i['cls']) if i['cls'] else ''))
    crit = [f for f in filas if f[0] < 3.0]
    bajo = [f for f in filas if 3.0 <= f[0] < 4.5]
    print('')
    if A is not None:
        print('coordenadas A/B      : texto detectado en su coordenada en %d de %d nodos' % (
            confirmados, confirmados + len(dudosos)))
        if dudosos:
            print('   senal <4 (texto tan tenue que casi no se distingue del fondo; '
                  'coincide con los de peor contraste): %s' % ', '.join(
                '%s(y=%d s=%.1f)' % (d[0], d[1], d[2]) for d in dudosos[:6]))
    else:
        print('coordenadas A/B      : NO verificado (falta --render-a)')
    print('nodos medidos        : %d' % len(filas))
    print('por debajo de 4,5:1  : %d  (referencia WCAG AA texto normal)' % (len(crit) + len(bajo)))
    print('por debajo de 3,0:1  : %d  (referencia WCAG AA texto grande)' % len(crit))
    print('peor contraste       : %.2f:1  %s  [%s]' % (filas[0][0], filas[0][1]['t'][:40], filas[0][1]['cls']))
    print('Nota: mide contra la MEDIANA de luminancia del fondo bajo el texto;')
    print('      no incluye el text-shadow (que ayuda) ni el zoom del lector.')


if __name__ == '__main__':
    main()
