#!/usr/bin/env python3
"""inventario_legibilidad.py — inventario REAL del texto de una ficha HTML.

Medición, no juicio: NO marca PASS/FAIL. El tamaño mínimo legible lo decide el
usuario sobre los datos (RULE-015: el umbral no se fija a priori).

Uso:
  python3 inventario_legibilidad.py <ficha.html> [--ancho 1080] [--json salida.json]

Metodo (patron ya validado en el lab): copiar el HTML a /tmp con un <script>
inyectado, recorrer los nodos de texto con getComputedStyle + getBoundingClientRect,
serializar en base64 dentro de un <pre>, y leerlo con chrome --headless --dump-dom.
Sin dependencias (solo stdlib + google-chrome).
"""
import argparse, base64, json, os, re, subprocess, sys, tempfile

JS = r"""
(function(){
  var out=[];
  var walk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null);
  var n;
  while(n=walk.nextNode()){
    var t=(n.nodeValue||'').replace(/\s+/g,' ').trim();
    if(t.length<2) continue;
    var e=n.parentElement; if(!e) continue;
    var cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
    var r=document.createRange(); r.selectNodeContents(n);
    var b=r.getBoundingClientRect();
    if(b.width<1||b.height<1) continue;
    out.push({t:t.slice(0,80),px:parseFloat(cs.fontSize),w:Math.round(b.width),
      h:Math.round(b.height),x:Math.round(b.x),y:Math.round(b.y),color:cs.color,
      fill:(e.getAttribute&&e.getAttribute('fill'))||cs.fill||'',
      weight:cs.fontWeight,tag:e.tagName.toLowerCase(),
      cls:(e.className||'').toString().replace(/\s+/g,'.').slice(0,44)});
  }
  var card=document.querySelector('.ficha')||document.body;
  var pie=document.querySelector('.pie');
  var meta={scrollH:document.body.scrollHeight,scrollW:document.documentElement.scrollWidth,
    cardW:Math.round(card.getBoundingClientRect().width),
    pieBottom:pie?Math.round(pie.getBoundingClientRect().bottom):null,
    n:out.length};
  var payload=btoa(unescape(encodeURIComponent(JSON.stringify({meta:meta,items:out}))));
  var p=document.createElement('pre'); p.id='inventario'; p.textContent=payload;
  document.body.appendChild(p);
})();
"""


def _absolutizar(src, html):
    """Reescribe rutas relativas de assets a file:// absolutas: la copia temporal
    vive en /tmp y, si no, el fondo y las fuentes no cargan (falso positivo
    'fondo blanco' verificado por pixeles el 26-sep)."""
    base = os.path.dirname(os.path.abspath(html))

    def rep(m):
        u = m.group(2)
        if u.startswith(('http', 'data:', '#', 'file:', '/', 'about:')):
            return m.group(0)
        return m.group(1) + 'file://' + os.path.join(base, u) + m.group(3)

    src = re.sub(r"""(url\(\s*['"]?)([^'")]+)(['"]?\s*\))""", rep, src)
    src = re.sub(r"""(src\s*=\s*['"])([^'"]+)(['"])""", rep, src)
    return src


def _dump(html_path):
    src = open(html_path, encoding='utf-8').read()
    src = _absolutizar(src, html_path)
    # Con --dump-dom Chrome no pinta, asi que las fuentes NO se piden y el texto se
    # mide con metricas de reserva: el inventario quedaba 19-36 px desplazado
    # respecto al render real (verificado por pixeles 26-sep). Cargamos las fuentes
    # a mano y forzamos layout antes de serializar.
    envoltorio = ("<script>(function(){function corre(){"
                  "document.body.getBoundingClientRect();%s}"
                  "var fs=[];if(document.fonts&&document.fonts.forEach){"
                  "document.fonts.forEach(function(ff){fs.push(ff.load('ESPA\u00d1Aaeiou0123456789'))});"
                  "}else{corre();return;}"
                  "Promise.all(fs).then(corre).catch(corre);})();</script>")
    inj = src.replace('</body>', (envoltorio % JS) + '</body>')
    if inj == src:
        inj = src + '<script>%s</script>' % JS
    tmp = os.path.join(tempfile.mkdtemp(prefix='inventario_'), 'ficha.html')
    open(tmp, 'w', encoding='utf-8').write(inj)
    last = ''
    for flags in (['--headless=new'], ['--headless'], ['--headless=old']):
        cmd = ['google-chrome'] + flags + ['--disable-gpu', '--no-sandbox',
               '--virtual-time-budget=8000', '--dump-dom', 'file://' + tmp]
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = pr.stdout
        last = (out or '')[:400] + ' | ' + (pr.stderr or '')[-200:]
        m = re.search(r'<pre id="inventario">([A-Za-z0-9+/=]+)</pre>', out)
        if m:
            return json.loads(base64.b64decode(m.group(1)).decode('utf-8'))
    raise SystemExit('chrome no devolvio el inventario. Ultimo: ' + last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--ancho', type=int, default=1080)
    ap.add_argument('--json')
    a = ap.parse_args()
    d = _dump(os.path.abspath(a.html))
    meta, items = d['meta'], d['items']
    items.sort(key=lambda i: (i['px'], i['y']))
    print('=== INVENTARIO DE LEGIBILIDAD ===')
    print('fichero            : %s' % os.path.basename(a.html))
    print('tamano tarjeta     : %s x %s px  (scrollHeight %s)' % (meta['cardW'], meta['scrollH'], meta['scrollH']))
    print('pie (bottom)       : %s px   [limite 1350]  -> %s' % (meta['pieBottom'],
          'OK' if (meta.get('pieBottom') or 0) <= 1350 else 'SE SALE'))
    print('nodos de texto     : %s' % meta['n'])
    print('')
    print('%-7s %-7s %-6s %-9s %s' % ('px', '%ancho', 'peso', 'color', 'texto  [clase]'))
    for i in items:
        print('%-7.1f %-7.2f %-6s %-9s %s  [%s%s]' % (
            i['px'], i['px'] / a.ancho * 100, i['weight'], i['color'],
            i['t'][:58], i['tag'], ('.' + i['cls']) if i['cls'] else ''))
    print('')
    tramos = [(0, 10), (10, 11.5), (11.5, 13), (13, 15), (15, 20), (20, 999)]
    print('=== resumen por tramos (son datos, no veredicto) ===')
    for lo, hi in tramos:
        n = [i for i in items if lo <= i['px'] < hi]
        if n:
            print('%5s-%-5s px : %3d textos   min %.1f' % (lo, hi, len(n), min(i['px'] for i in n)))
    print('Criterio: el minimo legible lo fija el usuario sobre esta tabla.')
    if a.json:
        json.dump({'meta': meta, 'items': items}, open(a.json, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('json -> %s' % a.json)


if __name__ == '__main__':
    main()
