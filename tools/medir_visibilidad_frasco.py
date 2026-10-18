#!/usr/bin/env python3
"""medir_visibilidad_frasco.py — ¿SE VE el frasco dentro de la ficha? Medido, no preguntado.

Origen (07-oct-2026): la ficha v5 de Bois Impérial se envió con el frasco invisible
sobre el fondo, y la verificación del flujo decía "packshot y fondo verificados por
visión: sin problemas". La visión NO sirve para contraste: medido con la misma
batería, GLM-4.6V-flash acertó 0/4 casos de contraste y gemma-4-12b-qat falló 0/3
al repetir la tarjeta real (1/4 acumulado). El contraste se MIDE.

Mide, sobre el PNG final de la ficha:
  - L mediana del TAPÓN y del CUERPO del frasco (máscaras sacadas de la propia
    figura RGBA: alpha>200; tapón L<90, cuerpo L>200)
  - L mediana del FONDO CONTIGUO (anillo alrededor del rect del frasco)
  - ratio de contraste WCAG de cada uno contra ese fondo
  - % de píxeles CLAROS (L>225) dentro del rect del frasco

Referencias de la medición que originó el instrumento (misma definición de máscaras
y mismo anillo), ficha 1080x1350 del 07-oct-2026:
    v5 (enviada, frasco invisible)  cuerpo 1,08:1   tapón  6,37:1   4,0 % claros
    v6 (fondo claro)                cuerpo 1,53:1   tapón 11,74:1  63,2 % claros
    v7 (fondo profundo)             cuerpo 2,26:1   tapón  7,95:1  63,0 % claros
    v8 (fondo mixto, la buena)      cuerpo 2,25:1   tapón  7,97:1  63,0 % claros

Medición, no juicio: los umbrales NO van fijados a priori (RULE-015). Sin --min-claros
/ --min-contraste el script solo imprime las cifras y sale con 0. Con umbrales
explícitos imprime OK/NO CUMPLE y sale con 1 si no se cumple (para uso fail-closed).

Geometría: no se escribe a mano. Con --html se lee del DOM la caja real del frasco
(`.frasco-figura`, o lo que diga --sel) y el src de su <img> (o se pasa --figura).
Así el instrumento sigue valiendo cuando la plantilla cambia el tamaño del frasco
(el 27-sep-2026 pasó de 350 a 450 px de alto, un rect hardcodeado habría seguido
midiendo donde ya no había frasco).

Uso:
  python3 tools/medir_visibilidad_frasco.py <ficha.png> --html <ficha.html> \
      [--figura <figura.png>] [--sel .frasco-figura] [--ancho 1080] \
      [--min-claros 40] [--min-contraste <ratio>] [--json salida.json]

Sin dependencias nuevas: PIL + google-chrome (los del lab).
"""
import argparse, base64, json, os, re, subprocess, sys, tempfile

from PIL import Image

JS = r"""
(function(){
  var sel=%s;
  var el=document.querySelector(sel);
  var d={sel:sel};
  if(!el){ d.error='no existe el selector'; }
  else{
    var b=el.getBoundingClientRect();
    d.rect={x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)};
    var img=el.tagName.toLowerCase()==='img'?el:el.querySelector('img');
    d.src=img?(img.getAttribute('src')||''):'';
    d.naturalW=img?img.naturalWidth:null; d.naturalH=img?img.naturalHeight:null;
    var cs=getComputedStyle(el); d.transform=cs.transform; d.overflow=cs.overflow;
  }
  var p=document.createElement('pre'); p.id='geomfrasco';
  p.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(d))));
  document.body.appendChild(p);
})();
"""


def _absolutizar(src, html):
    """Rutas relativas -> file:// absolutas (la copia vive en /tmp). Mismo patrón
    que inventario_legibilidad.py: sin esto el fondo no carga y se mide un falso
    fondo blanco."""
    base = os.path.dirname(os.path.abspath(html))

    def rep(m):
        u = m.group(2)
        if u.startswith(('http', 'data:', '#', 'file:', '/', 'about:')):
            return m.group(0)
        return m.group(1) + 'file://' + os.path.join(base, u) + m.group(3)

    src = re.sub(r"""(url\(\s*['"]?)([^'")]+)(['"]?\s*\))""", rep, src)
    src = re.sub(r"""(src\s*=\s*['"])([^'"]+)(['"])""", rep, src)
    return src


def _geom_dom(html_path, sel):
    src = _absolutizar(open(html_path, encoding='utf-8').read(), html_path)
    js = JS % json.dumps(sel)
    envoltorio = ("<script>(function(){function corre(){"
                  "document.body.getBoundingClientRect();%s}"
                  "var fs=[];if(document.fonts&&document.fonts.forEach){"
                  "document.fonts.forEach(function(ff){fs.push(ff.load('ESPANAaeiou0123456789'))});"
                  "}else{corre();return;}"
                  "Promise.all(fs).then(corre).catch(corre);})();</script>")
    inj = src.replace('</body>', (envoltorio % js) + '</body>')
    if inj == src:
        inj = src + '<script>%s</script>' % js
    tmp = os.path.join(tempfile.mkdtemp(prefix='geomfrasco_'), 'ficha.html')
    open(tmp, 'w', encoding='utf-8').write(inj)
    last = ''
    for flags in (['--headless=new'], ['--headless'], ['--headless=old']):
        cmd = ['google-chrome'] + flags + ['--disable-gpu', '--no-sandbox',
               '--virtual-time-budget=8000', '--dump-dom', 'file://' + tmp]
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = pr.stdout or ''
        last = out[:300] + ' | ' + (pr.stderr or '')[-200:]
        m = re.search(r'<pre id="geomfrasco">([A-Za-z0-9+/=]+)</pre>', out)
        if m:
            return json.loads(base64.b64decode(m.group(1)).decode('utf-8'))
    raise SystemExit('chrome no devolvio la geometria. Ultimo: ' + last)


def _lum(p):
    r, g, b = p[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ratio(l1, l2):
    """Contraste WCAG entre dos luminancias 0-255 (referencia publicada, no umbral)."""
    def f(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    a, b = f(max(l1, l2)) + 0.05, f(min(l1, l2)) + 0.05
    return a / b


def _mediana(v):
    v = sorted(v)
    return v[len(v) // 2] if v else float('nan')


def medir(png, figura, rect, json_out=None, min_claros=None, min_contraste=None):
    im = Image.open(png).convert('RGB')
    px = im.load()
    W, H = im.size
    x0, y0, rw, rh = [int(round(v)) for v in rect]

    fig = Image.open(figura).convert('RGBA')
    fw, fh = fig.size
    fpx = fig.load()
    cap, body = [], []
    for x in range(fw):
        for y in range(fh):
            r, g, b, a = fpx[x, y]
            if a <= 200:
                continue
            L = _lum((r, g, b))
            if L < 90:
                cap.append((x, y))
            elif L > 200:
                body.append((x, y))
    if not cap or not body:
        raise SystemExit('la figura no da mascaras utilizables: tapon %d px, cuerpo %d px'
                         % (len(cap), len(body)))

    def en_tarjeta(src):
        return [_lum(px[x0 + int(x * rw / fw), y0 + int(y * rh / fh)]) for x, y in src]

    # fondo contiguo: MISMO anillo que la medicion de referencia (offsets relativos)
    fondo = []
    for x in list(range(x0 - 55, x0 - 5, 2)) + list(range(x0 + rw + 5, x0 + rw + 55, 2)):
        for y in range(y0, y0 + rh, 2):
            if 0 <= x < W and 0 <= y < H:
                fondo.append(_lum(px[x, y]))
    for x in range(x0, x0 + rw, 2):
        for y in list(range(y0 - 44, y0 - 2, 2)) + list(range(y0 + rh + 2, y0 + rh + 46, 2)):
            if 0 <= x < W and 0 <= y < H:
                fondo.append(_lum(px[x, y]))
    if not fondo:
        raise SystemExit('el rect del frasco cae fuera del PNG: %s (PNG %dx%d)' % (rect, W, H))
    fondo_med = _mediana(fondo)

    tapon = _mediana(en_tarjeta(cap))
    cuerpo = _mediana(en_tarjeta(body))
    claros = sum(1 for x in range(x0, x0 + rw) for y in range(y0, y0 + rh)
                 if 0 <= x < W and 0 <= y < H and _lum(px[x, y]) > 225)
    pct = 100.0 * claros / (rw * rh)
    c_tapon, c_cuerpo = _ratio(tapon, fondo_med), _ratio(cuerpo, fondo_med)

    print('=== VISIBILIDAD DEL FRASCO (medido) ===')
    print('ficha              : %s  (%dx%d)' % (os.path.basename(png), W, H))
    print('figura             : %s  (%dx%d)  [%d px tapon / %d px cuerpo]'
          % (os.path.basename(figura), fw, fh, len(cap), len(body)))
    print('rect del frasco    : x %d-%d  y %d-%d  (%dx%d)'
          % (x0, x0 + rw, y0, y0 + rh, rw, rh))
    print('fondo contiguo     : L mediana %.1f' % fondo_med)
    print('tapon              : L %.1f  -> contraste %.2f:1' % (tapon, c_tapon))
    print('cuerpo             : L %.1f  -> contraste %.2f:1' % (cuerpo, c_cuerpo))
    print('pixeles claros     : %d de %d  -> %.1f %%  (L>225 dentro del rect)'
          % (claros, rw * rh, pct))

    fallos = []
    if min_claros is not None:
        fallos.append(('%% claros >= %g' % min_claros, pct >= min_claros, '%.1f %%' % pct))
    if min_contraste is not None:
        fallos.append(('contraste cuerpo >= %g:1' % min_contraste,
                       c_cuerpo >= min_contraste, '%.2f:1' % c_cuerpo))
    if fallos:
        print('')
        for nombre, ok, valor in fallos:
            print('  [%s] %s -> %s' % ('OK' if ok else 'NO CUMPLE', nombre, valor))
    else:
        print('\n(sin umbrales: esto es medicion, no veredicto; usa --min-claros / --min-contraste)')

    if json_out:
        json.dump({'png': png, 'figura': figura, 'rect': [x0, y0, rw, rh],
                   'fondo_L': fondo_med, 'tapon_L': tapon, 'cuerpo_L': cuerpo,
                   'contraste_tapon': c_tapon, 'contraste_cuerpo': c_cuerpo,
                   'pct_claros': pct, 'min_claros': min_claros,
                   'min_contraste': min_contraste},
                  open(json_out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print('json -> %s' % json_out)
    return all(ok for _, ok, _ in fallos) if fallos else True


def main():
    ap = argparse.ArgumentParser(description='Mide si el frasco se ve dentro de la ficha.')
    ap.add_argument('png')
    ap.add_argument('--html', help='ficha HTML de la que leer la geometria real del frasco')
    ap.add_argument('--figura', help='PNG RGBA de la figura (si no, el src del <img>)')
    ap.add_argument('--sel', default='.frasco-figura')
    ap.add_argument('--rect', help='x0,y0,w,h en px del PNG (sustituye a --html)')
    ap.add_argument('--ancho', type=int, default=1080, help='ancho CSS usado al renderizar')
    ap.add_argument('--min-claros', type=float)
    ap.add_argument('--min-contraste', type=float)
    ap.add_argument('--json')
    a = ap.parse_args()

    png = os.path.abspath(a.png)
    figura = os.path.abspath(a.figura) if a.figura else None
    rect = None
    if a.rect:
        rect = [float(v) for v in a.rect.split(',')]
        if len(rect) != 4:
            raise SystemExit('--rect necesita x0,y0,w,h')
    else:
        if not a.html:
            raise SystemExit('hace falta --html (geometria real) o --rect x0,y0,w,h')
        g = _geom_dom(os.path.abspath(a.html), a.sel)
        if 'rect' not in g:
            raise SystemExit('no pude leer la geometria: %s' % g)
        # escala CSS -> px del PNG
        im = Image.open(png)
        esc = im.size[0] / float(a.ancho)
        r = g['rect']
        rect = [r['x'] * esc, r['y'] * esc, r['w'] * esc, r['h'] * esc]
        if not figura and g.get('src'):
            s = g['src']
            figura = s if s.startswith('/') else os.path.join(
                os.path.dirname(os.path.abspath(a.html)), s.replace('file://', '').split('?')[0])
        print('geometria del DOM  : %s -> x %d y %d w %d h %d (CSS)  x%.2f = %s px del PNG'
              % (a.sel, r['x'], r['y'], r['w'], r['h'], esc,
                 ','.join('%d' % v for v in rect)))
    if not figura or not os.path.exists(figura):
        raise SystemExit('no encuentro la figura: %s' % figura)

    ok = medir(png, figura, rect, a.json, a.min_claros, a.min_contraste)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
