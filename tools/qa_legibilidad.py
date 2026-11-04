#!/usr/bin/env python3
"""qa_legibilidad.py — norma ciclica de legibilidad de la ficha del dia (Joko Lab, 04-11-2026).

Mide, no opina:
  * alto real del documento vs lienzo (desbordamiento)
  * suelo tipografico (px minimo)
  * contraste WCAG nodo a nodo, estimando el fondo desde el propio PNG

Uso:
  /usr/bin/python3 tools/qa_legibilidad.py --html <ficha.html> [--png <png>] [--json <out>]
  exit 0 = pasa la puerta | 2 = falla

Reglas (norma v6):
  cuerpo (px>=13)          -> >= 4,5:1
  texto grande (>=24px)    -> >= 3,0:1
  nota legal / credito     -> >= 3,0:1
  ningun nodo < 12px
  alto <= lienzo
"""
import argparse, json, math, os, re, subprocess, sys, tempfile, pathlib, shutil
from html.parser import HTMLParser

CHROME = '/usr/bin/google-chrome-stable'
MEASURE = """
<script>
window.addEventListener('load', () => setTimeout(() => {
  const items = [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect();
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
    return own && r.width > 2 && r.height > 2;
  }).map(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    return { t: [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').slice(0,120),
             x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
             px: parseFloat(cs.fontSize), color: cs.color, fill: cs.fill, weight: cs.fontWeight,
             tag: e.tagName, cls: (e.className||'').toString().slice(0,40) };
  });
  document.documentElement.setAttribute('data-inv', JSON.stringify({alto: document.body.scrollHeight, ancho: document.body.scrollWidth, items}));
}, 400));
</script>
"""

LEGAL = ('fuente-line', 'nota-fondo', 'sello', 'pl', 'donde')
DECO = ('sep',)  # separadores tipograficos: no son texto de lectura


class InvParser(HTMLParser):
    inv = None

    def handle_starttag(self, tag, attrs):
        if tag == 'html':
            for k, v in attrs:
                if k == 'data-inv':
                    InvParser.inv = v


def _lum(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def parse_color(css):
    m = re.findall(r'[\d.]+', css)
    if len(m) >= 3:
        return tuple(int(float(x)) for x in m[:3])
    return (0, 0, 0)


def measure(html_path, png_path=None, W=1080, H=1440, budget=8000):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='qa_leg_'))
    src = html_path.read_text()
    meas = tmp / 'measure.html'
    meas.write_text(src.replace('</body>', MEASURE + '</body>'))
    dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                          '--force-device-scale-factor=1', f'--virtual-time-budget={budget}',
                          f'--window-size={W},{H}', '--dump-dom', f'file://{meas}'],
                         capture_output=True, text=True).stdout
    p = InvParser()
    p.feed(dom)
    if not InvParser.inv:
        raise SystemExit('ERROR: no se pudo leer el inventario del DOM')
    inv = json.loads(InvParser.inv)
    shot = png_path
    if shot is None:
        shot = tmp / 'shot.png'
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=1', f'--virtual-time-budget={budget}',
                        f'--window-size={W},{H}', f'--screenshot={shot}', f'file://{html_path}'],
                       capture_output=True)
        shot = pathlib.Path(shot)
    return inv, pathlib.Path(shot), tmp


def analyze(inv, png, min_px=13, target=4.5):
    from PIL import Image
    im = Image.open(png).convert('RGB')
    W, H = im.size
    px = im.load()
    rows = []
    for it in inv['items']:
        x, y, w, h = it['x'], it['y'], it['w'], it['h']
        x0, y0 = max(0, x - 3), max(0, y - 3)
        x1, y1 = min(W, x + w + 3), min(H, y + h + 3)
        is_svg_text = it.get('tag', '').lower() in ('text', 'tspan')
        fg_src = it.get('fill') if (is_svg_text and it.get('fill') not in (None, 'none', '')) else it['color']
        fg = parse_color(fg_src)
        bins = {}
        for yy in range(y0, y1, 2):
            for xx in range(x0, x1, 2):
                c = px[xx, yy]
                if c is None:
                    continue
                c = tuple(c)[:3]
                if math.dist(c, fg) <= 90:
                    continue
                k = (c[0] // 16, c[1] // 16, c[2] // 16)
                bins.setdefault(k, []).append(c)
        if not bins:
            continue
        # el fondo es el color DOMINANTE de la caja (el texto ocupa menos area);
        # la mediana se contaminaba con el antialiasing en textos grandes y gruesos.
        grp = max(bins.values(), key=len)
        bg = tuple(sum(ch[i] for ch in grp) // len(grp) for i in range(3))
        share = len(grp) / sum(len(v) for v in bins.values())
        r = ratio(fg, bg)
        cls = it.get('cls') or ''
        if any(k in cls for k in DECO) and len((it.get('t') or '').strip()) <= 2:
            continue
        legal = any(k in cls for k in LEGAL)
        need = 3.0 if (it['px'] >= 24 or legal) else target
        rows.append({**it, 'ratio': round(r, 2), 'bg': bg, 'share': round(share, 2),
                    'need': need, 'pass': r + 1e-9 >= need})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', required=True)
    ap.add_argument('--png')
    ap.add_argument('--json')
    ap.add_argument('--target', type=float, default=4.5)
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()

    hp = pathlib.Path(a.html).expanduser().resolve()
    inv, png, tmp = measure(hp, pathlib.Path(a.png).expanduser().resolve() if a.png else None)
    rows = analyze(inv, png, target=a.target)
    if not a.keep:
        shutil.rmtree(tmp, ignore_errors=True)

    fails = [r for r in rows if not r['pass']]
    sub35 = [r for r in rows if r['ratio'] < 3.0]
    sub45 = [r for r in rows if r['ratio'] < 4.5]
    small = [r for r in rows if r['px'] < 12]
    over = inv['alto'] > 1440

    print(f'fichero   {hp.name}')
    print(f'png       {png.name}  {inv["ancho"]}x{inv["alto"]}  (lienzo 1080x1440)')
    print(f'nodos     {len(rows)}')
    print(f'<3:1      {len(sub35)}   <4,5:1 {len(sub45)}   fallan-umbral {len(fails)}')
    print(f'<12px     {len(small)}   desborda {over}')
    for r in sorted(rows, key=lambda z: z['ratio'])[:8]:
        print(f'  {r["ratio"]:5.2f}:1  {r["px"]:5.1f}px  {r["cls"][:14]:14}  {r["t"][:44]}')
    ok = not fails and not small and not over
    print('VEREDICTO', 'PASA' if ok else 'FALLA')
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({'alto': inv['alto'], 'rows': rows}, ensure_ascii=False, indent=1))
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()
