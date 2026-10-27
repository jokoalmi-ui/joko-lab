#!/usr/bin/env python3
"""validar_ficha_preenvio.py — gate pre-envio de la ficha del dia.

Comprueba, sobre el HTML FINAL que se va a enviar:
  - los 17 campos del checklist canonico (skill perfume-del-dia, linea 134),
    cada uno por su selector/patron, no por un contenedor padre
  - estructura: scrollHeight y el borde inferior del pie dentro del limite
  - ANTIFALLOS: assets locales que existan, que no se envia un resto
    .PRUEBA/.PROVISIONAL, factor de ampliacion del fondo, y que el precio
    lleve fecha de consulta

Uso:
  python3 validar_ficha_preenvio.py <ficha.html> [--limite 1440] [--json out.json]
Salida: [OK]/[FALTA]/[AVISO] por linea + resumen. Exit 0 si no hay FALTA, 1 si hay.
"""
import argparse, base64, datetime, json, os, re, subprocess, sys, tempfile
from PIL import Image

CLASSES = ['.casa', '.dh', '.sello', '.r-num', '.r-meta', '.alt-n', '.alt-casa',
           '.alt-motivo', '.lab', '.clima', '.pie', '.caveat-pie', '.sub',
           '.fuente-line', '.nota-fondo', '.sec-title', '.sec-num', '.f', 'h1',
           'blockquote', '.precio', '.p']
JS = r"""
(function(){
  var norm=function(s){return (s||'').replace(/\s+/g,' ').trim();};
  function medir(){
    if(document.getElementById('valficha')) return;
    var cls={};
    %s.forEach(function(sel){
      try{cls[sel]=[...document.querySelectorAll(sel)].map(function(e){return norm(e.innerText);}).filter(function(t){return t;});}
      catch(e){cls[sel]=[];}
    });
    var imgs=[...document.querySelectorAll('img')].map(function(i){return {src:i.getAttribute('src')||'',alt:i.getAttribute('alt')||''};});
    var svg=[...document.querySelectorAll('svg text')].map(function(t){return norm(t.textContent);}).filter(Boolean);
    var pie=document.querySelector('.pie');
    // borde inferior real del contenido: se ignoran capas decorativas (velo/fondo)
    var maxB=0, debiles=[];
    [...document.querySelectorAll('body *')].forEach(function(e){
      var cs=getComputedStyle(e); if(cs.position==='fixed') return;
      if(/(^|\s)(velo|fondo)(\s|$)/.test(typeof e.className==='string'?e.className:'')) return;
      var r=e.getBoundingClientRect();
      if(r.height>2 && r.bottom>maxB) maxB=r.bottom;
      var op=parseFloat(cs.opacity); if(!isNaN(op) && op<0.5 && r.height>2) debiles.push(Math.round(r.bottom));
    });
    var data={cls:cls,imgs:imgs,svg:svg,txt:norm(document.body.innerText),
      scrollH:document.body.scrollHeight,scrollW:document.documentElement.scrollWidth,
      contentBottom:Math.round(maxB),
      pieBottom:pie?Math.round(pie.getBoundingClientRect().bottom):null,
      fontsOk:document.fonts?document.fonts.status:'n/a',
      imgsOk:[...document.images].filter(function(i){return i.naturalWidth>0;}).length,
      imgsTot:document.images.length};
    var p=document.createElement('pre');p.id='valficha';
    p.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(data))));
    document.body.appendChild(p);
  }
  // medir SOLO con fuentes e imagenes cargadas: sin esto la altura sale corta (falso OK)
  var ps=[document.fonts?document.fonts.ready:Promise.resolve()];
  [...document.images].forEach(function(i){
    if(i.complete) return;
    ps.push(new Promise(function(res){i.addEventListener('load',res);i.addEventListener('error',res);}));
  });
  Promise.all(ps).then(function(){requestAnimationFrame(function(){requestAnimationFrame(medir);});});
  setTimeout(medir,10000);
})();
"""


def dump(html):
    src = open(html, encoding='utf-8').read()
    js = JS % json.dumps(CLASSES)
    inj = src.replace('</body>', '<script>%s</script></body>' % js)
    # La sonda va EN LA MISMA CARPETA que el HTML: en un tmp las rutas relativas
    # del fondo y las <img> no cargan y la altura medida sale corta (falso OK).
    probe = os.path.join(os.path.dirname(html), '.valficha_probe_%d.html' % os.getpid())
    open(probe, 'w', encoding='utf-8').write(inj)
    out = ''
    try:
        for flags in (['--headless=new'], ['--headless']):
            pr = subprocess.run(['google-chrome'] + flags + ['--disable-gpu', '--no-sandbox',
                                 '--virtual-time-budget=20000', '--dump-dom', 'file://' + probe],
                                capture_output=True, text=True, timeout=180)
            out = pr.stdout or ''
            m = re.search(r'<pre id="valficha">([A-Za-z0-9+/=]+)</pre>', out)
            if m:
                return json.loads(base64.b64decode(m.group(1)).decode('utf-8')), src
    finally:
        try:
            os.unlink(probe)
        except OSError:
            pass
    raise SystemExit('chrome no devolvio datos de validacion')


def _l(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b


def medir_halo_recorte(p, radio=6, fondo=102.0, paso=2):
    """Mide el HALO VISIBLE del filo de una figura recortada (RGBA), sin numpy.

    Un pixel del filo con alfa a y color L, compuesto sobre un fondo de L=fondo,
    aporta delta = a*(L-fondo). Se cuenta solo donde el frasco es OSCURO cerca
    (nucleo opaco con L<110): ahi una claridad en el filo es halo, no arte.
    Devuelve dict con filo, delta medio, % de pixeles visibles y muy visibles.
    Sin umbral: el numero se reporta, la decision no se automatiza (RULE-015).
    """
    with Image.open(p) as im0:
        im = im0.convert('RGBA')
    w, h = im.size
    px = im.load()  # type: ignore[assignment]

    def oscuro_cerca(x, y):
        for dy in range(-radio, radio + 1, 2):
            yy = y + dy
            if yy < 0 or yy >= h:
                continue
            for dx in range(-radio, radio + 1, 2):
                xx = x + dx
                if xx < 0 or xx >= w:
                    continue
                v = px[xx, yy]
                if v[3] > 250 and _l(v[0], v[1], v[2]) < 110:
                    return True
        return False

    filo = v15 = v30 = 0
    dsum = 0.0
    for y in range(1, h - 1, paso):
        for x in range(1, w - 1, paso):
            v = px[x, y]
            if v[3] < 26 or v[3] > 252:
                continue
            if not oscuro_cerca(x, y):
                continue
            delta = (v[3] / 255.0) * (_l(v[0], v[1], v[2]) - fondo)
            filo += 1
            dsum += delta
            if delta > 15:
                v15 += 1
            if delta > 30:
                v30 += 1
    if not filo:
        return {'filo': 0, 'delta': 0.0, 'pct': 0.0, 'v15': 0, 'v30': 0}
    return {'filo': filo, 'delta': dsum / filo, 'pct': 100.0 * v15 / filo,
            'v15': v15, 'v30': v30}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--limite', type=int, default=1440)
    ap.add_argument('--json')
    ap.add_argument('--fecha', help='YYYY-MM-DD para auditar fichas antiguas (por defecto: hoy)')
    a = ap.parse_args()
    html = os.path.abspath(a.html)
    d, src = dump(html)
    cls, txt = d['cls'], d['txt']

    def has(sel):
        return ' '.join(cls.get(sel, []))

    res = []  # (estado, campo, detalle)
    def add(ok, campo, detalle, aviso=False):
        res.append(('AVISO' if (aviso and ok) else ('OK' if ok else 'FALTA'), campo, detalle))

    any_txt = lambda *pats: all(re.search(p, txt, re.I) for p in pats)
    # 1-8 identidad
    add(bool(has('h1')) and len(has('h1')) > 3, '01 Titulo', has('h1')[:40] or 'vacio')
    add(bool(has('.casa')), '02 Casa', has('.casa')[:30] or 'vacio')
    add(bool(re.search(r'(LUNES|MARTES|MIERCOLES|MIÉRCOLES|JUEVES|VIERNES|SABADO|SÁBADO|DOMINGO)|\d{1,2}\s+DE\s+\w+', txt, re.I)), '03 Fecha', 'dia/mes en la ficha')
    add(bool(re.search(r'\b(19|20)\d{2}\b', txt)), '04 Anio', (re.search(r'\b(19|20)\d{2}\b', txt) or [''])[0])
    add(bool(re.search(r'Eau de Toilette|Eau de Parfum|EDT|EDP|Cologne|Extrait', txt, re.I)), '05 Concentracion', 'etiqueta presente')
    add(bool(re.search(r'Masculin|Femenin|Unisex', txt, re.I)), '06 Genero', 'etiqueta presente')
    fam = r'arom[aá]tic|foug[eè]re|amaderad|c[ií]tric|oriental|floral|gourmand|chipre|cuero|acu[aá]tic|dulce|especiad'
    add(bool(re.search(fam, txt, re.I)), '07 Familia', (re.search(fam, txt, re.I) or [''])[0])
    add(any_txt(r'Perfumista'), '08 Perfumista', 'fila presente (permite "no revelado")')
    # 9-13 datos
    add(bool(has('.r-num')) and any_txt(r'votos'), '09 Rating comunidad', '%s · votos' % (has('.r-num')[:10] or 'sin r-num'))
    add(len(d['svg']) >= 3 or len(cls.get('.lab', [])) >= 3, '10 Piramide completa',
        'svg=%d lab=%d' % (len(d['svg']), len(cls.get('.lab', []))))
    add(any_txt(r'Longevidad', r'\d+\s*h'), '11 Longevidad', 'horas presentes')
    add(any_txt(r'Estela'), '12 Estela', has('.dh')[-1][:20] if cls.get('.dh') else '')
    precio = re.search(r'\d+([.,]\d+)?\s*€[^€]{0,40}100\s*ml|100\s*ml[^€]{0,40}\d+([.,]\d+)?\s*€', txt)
    add(bool(precio), '13 Precio 100 ml', (precio.group(0)[:30] if precio else 'no encontrado'))
    # 14-17 contenido
    add(any_txt(r'Si te gusta') and len(cls.get('.alt-n', [])) >= 2, '14 Si te gusta, prueba',
        '%d alternativas' % len(cls.get('.alt-n', [])))
    citas = [t for t in cls.get('blockquote', []) if len(t) > 20]
    add(bool(citas) and bool(re.search(r'Fragrantica|Parfumo|OnlyFumes', txt, re.I)), '15 Cita comunidad',
        (citas[0][:34] + '...') if citas else 'sin blockquote')
    qr = [i for i in d['imgs'] if 'qr' in (i['src'] or '').lower()]
    add(bool(qr), '16 QR Fragrantica', qr[0]['src'][:34] if qr else 'sin img qr')
    rango = re.search(r'\d+([.,]\d+)?\s*[–-]\s*\d+([.,]\d+)?\s*°C', txt)
    add(bool(rango and re.search(r'media', txt, re.I) and re.search(r'lluvia', txt, re.I)
             and bool(has('.nota-fondo'))), '17 Pie completo',
        '%s · media · lluvia · nota fondo' % (rango.group(0) if rango else 'sin rango'))

    # --- ANTIFALLOS ---
    urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', src)
    locales = [u for u in urls + [i['src'] for i in d['imgs']] if u and not u.startswith(('http', 'data:', '#'))]
    faltan = [u for u in locales if not os.path.exists(u if os.path.isabs(u) else os.path.join(os.path.dirname(html), u))]
    add(not faltan, 'A1 Assets existen', '%d locales, %d ausentes %s' % (len(locales), len(faltan), faltan[:2]))
    restos = [u for u in locales if re.search(r'\.(PRUEBA|PROVISIONAL|bak)', u, re.I)] + \
             [f for f in os.listdir(os.path.dirname(html)) if re.search(r'\.(PRUEBA|PROVISIONAL)\.png$', f)]
    add(not restos, 'A2 Sin restos de prueba', restos[:3] or 'ninguno referenciado')
    fondos = [u for u in urls if re.search(r'fondo', u)] or urls[:1]
    for u in fondos[:1]:
        p = u if os.path.isabs(u) else os.path.join(os.path.dirname(html), u)
        if os.path.exists(p):
            with Image.open(p) as im:
                w, h = im.size
            fac = max(1080.0 / w, a.limite / h)
            add(fac <= 1.5, 'A3 Fondo ampliado x%.2f' % fac,
                '%s %dx%d -> %s' % (os.path.basename(p), w, h,
                                    'sin ampliacion notable' if fac <= 1.5 else 'SE AMPLIA, propuesta: generar a 1024'),
                aviso=True)
    # A4 (18-oct-2026): la fecha de consulta del precio debe ser LA DE HOY. Antes bastaba con que
    # apareciera cualquier "consultado" o un dd/mm/yyyy en cualquier parte del texto: una ficha con
    # el precio consultado la semana pasada pasaba. Se busca la fecha dentro de la ventana del €.
    _hoy = (datetime.date.fromisoformat(a.fecha) if a.fecha else datetime.date.today())
    _mes = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'][_hoy.month - 1]
    _formas = [_hoy.strftime('%d-%m-%Y'), _hoy.strftime('%d/%m/%Y'), _hoy.strftime('%d-%m-%y'),
               '%02d-%s-%d' % (_hoy.day, _mes, _hoy.year), '%d de %s' % (_hoy.day, _mes)]
    _ventanas = []
    for _m in re.finditer('€', txt):
        _ventanas.append(txt[max(0, _m.start() - 90):_m.start() + 90])
    _ctx = ' '.join(_ventanas)
    _fecha_hoy = next((f for f in _formas if f.lower() in _ctx.lower()), None)
    add(bool(_fecha_hoy), 'A4 Precio con fecha de consulta',
        ('%s en la linea de precio: %s' % (_hoy.isoformat(), _fecha_hoy)) if _fecha_hoy else
        'la linea de precio no dice %s (formas validas: %s)' % (
            _hoy.isoformat(), ' | '.join(_formas[:3])), aviso=True)

    # A5 (27-oct-2026): el gate daba 17/17 con el recorte lleno de halo blanco
    # (ficha Basso: 75 % del filo visible brillaba sobre el cuerpo oscuro). No
    # medía alfa. Ahora REPORTA la medida; no bloquea ni fija umbral (RULE-015):
    # se junta evidencia y el criterio se decide con datos, no a priori.
    _fig = None
    for _u in locales:
        _p = _u if os.path.isabs(_u) else os.path.join(os.path.dirname(html), _u)
        try:
            with Image.open(_p) as _im:
                if _im.mode in ('RGBA', 'LA') or 'transparency' in _im.info:
                    _fig = _p
                    break
        except Exception:
            continue
    if _fig is None:
        add(False, 'A5 Recorte sin halo', 'ninguna imagen con canal alfa: no medible')
    else:
        _h = medir_halo_recorte(_fig)
        add(True, 'A5 Recorte sin halo',
            '%s · filo %d px · delta L %+.1f · visibles %.1f%% (%d px, %d muy visibles)'
            % (os.path.basename(_fig), _h['filo'], _h['delta'], _h['pct'], _h['v15'], _h['v30']),
            aviso=True)

    # --- estructura ---
    alto = max(d['scrollH'], d.get('contentBottom') or 0)
    fuentes_ok = (d.get('fontsOk') == 'loaded')
    add(alto <= a.limite and fuentes_ok, 'E1 Altura (contenido real)',
        '%d px (body %d, borde real %d, fuentes %s, img %s/%s)  [limite %d]'
        % (alto, d['scrollH'], d.get('contentBottom') or 0, d.get('fontsOk'),
           d.get('imgsOk'), d.get('imgsTot'), a.limite))
    add((d['pieBottom'] or 0) <= a.limite, 'E2 Pie dentro de la tarjeta',
        'pie bottom %s px · aire %s px' % (d['pieBottom'], a.limite - (d['pieBottom'] or 0)))

    campos = [r for r in res if re.match(r'^\d\d ', r[1])]
    ok_campos = len([r for r in campos if r[0] == 'OK'])
    print('=== GATE PRE-ENVIO · %s ===' % os.path.basename(html))
    for estado, campo, det in res:
        print('[%-5s] %-32s %s' % (estado, campo, det))
    fallos = [r for r in res if r[0] == 'FALTA']
    avisos = [r for r in res if r[0] == 'AVISO']
    print('')
    print('campos            : %d/%d' % (ok_campos, len(campos)))
    print('FALTA             : %d   %s' % (len(fallos), [r[1] for r in fallos]))
    print('AVISO             : %d   %s' % (len(avisos), [r[1] for r in avisos]))
    print('veredicto         : %s' % ('NO ENVIAR' if fallos else ('ENVIAR (con avisos)' if avisos else 'ENVIAR')))
    if a.json:
        json.dump({'res': res, 'campos_ok': ok_campos, 'campos_total': len(campos),
                   'fallos': [r[1] for r in fallos], 'avisos': [r[1] for r in avisos]},
                  open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('json -> %s' % a.json)
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()
