#!/usr/bin/env python3
"""med_fit.py — encaje vertical REAL de la ficha.

Escribe la sonda EN LA MISMA CARPETA que el HTML (asi el fondo y las <img>
cargan igual que en el render), espera a document.fonts.ready y a que todas
las imagenes esten decodificadas, y mide:
  body.scrollHeight · ultimo elemento por abajo · .pie · aire hasta el limite

Uso: med_fit.py <ficha.html> [limite=1440]
"""
import base64, json, os, re, subprocess, sys

html = os.path.abspath(sys.argv[1])
limite = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
JS = r"""
(function(){
  var LIM = %d;
  function go(){
    var out = {limite: LIM};
    var b = document.body, h = document.documentElement;
    out.body = {scrollH:b.scrollHeight, clientH:b.clientHeight, offsetH:b.offsetHeight};
    out.html = {scrollH:h.scrollHeight, clientH:h.clientHeight};
    var pie = document.querySelector('.pie');
    if (pie){ var r = pie.getBoundingClientRect(); out.pie = {top:Math.round(r.top), bot:Math.round(r.bottom)}; }
    var cont = document.querySelector('.content');
    if (cont){ var r2 = cont.getBoundingClientRect();
      out.content = {top:Math.round(r2.top), bot:Math.round(r2.bottom), h:Math.round(r2.height),
                     padT:getComputedStyle(cont).paddingTop, padB:getComputedStyle(cont).paddingBottom}; }
    var maxB = 0, who = '';
    Array.prototype.forEach.call(document.querySelectorAll('body *'), function(e){
      var r = e.getBoundingClientRect();
      if (r.height > 2 && r.bottom > maxB && getComputedStyle(e).position !== 'fixed'
          && !/(^|\s)(velo|content|card)(\s|$)/.test(typeof e.className==='string'?e.className:'')){
        maxB = r.bottom;
        who = e.tagName.toLowerCase() + '.' + (typeof e.className==='string' ? e.className.trim().split(/\s+/)[0] : '')
              + ' "' + ((e.innerText||'').replace(/\s+/g,' ').slice(0,38)) + '"';
      }
    });
    out.mas_bajo = {bot: Math.round(maxB), quien: who};
    if (cont){ out.bloques = Array.prototype.map.call(cont.children, function(e){
      var r = e.getBoundingClientRect();
      return [e.tagName.toLowerCase() + '.' + (typeof e.className==='string'?e.className.trim().split(/\s+/)[0]:''),
              Math.round(r.top), Math.round(r.bottom), getComputedStyle(e).marginTop]; }); }
    out.aire_inferior = Math.round(LIM - maxB);
    out.aire_superior = Math.round(document.querySelector('.topline') ? document.querySelector('.topline').getBoundingClientRect().top : -1);
    out.imgs = Array.prototype.map.call(document.images, function(i){
      return (i.getAttribute('src')||'') + ' ' + i.naturalWidth + 'x' + i.naturalHeight; });
    out.fonts_status = document.fonts ? document.fonts.status : 'n/a';
    out.familias = ['Caveat','Playfair Display','Inter'].map(function(f){
      return f + ':' + ((document.fonts && document.fonts.check('16px "'+f+'"')) ? 'SI' : 'NO'); });
    var p = document.createElement('pre'); p.id='mfit';
    p.textContent = btoa(unescape(encodeURIComponent(JSON.stringify(out))));
    document.body.appendChild(p);
  }
  var esperas = [document.fonts ? document.fonts.ready : Promise.resolve()];
  Array.prototype.forEach.call(document.images, function(i){
    if (i.complete) return;
    esperas.push(new Promise(function(res){ i.addEventListener('load', res); i.addEventListener('error', res); }));
  });
  Promise.all(esperas).then(function(){ requestAnimationFrame(function(){ requestAnimationFrame(go); }); });
  setTimeout(go, 8000);
})();
""" % limite

src = open(html, encoding='utf-8').read()
probe = os.path.join(os.path.dirname(html), '.probe_med_fit_%d.html' % os.getpid())
open(probe, 'w', encoding='utf-8').write(src.replace('</body>', '<script>%s</script></body>' % JS))
try:
    pr = subprocess.run(['google-chrome', '--headless=new', '--hide-scrollbars', '--no-sandbox',
                         '--window-size=1080,%d' % limite, '--virtual-time-budget=20000', '--dump-dom',
                         'file://' + probe], capture_output=True, text=True, timeout=240)
finally:
    pass
m = re.search(r'<pre id="mfit">([A-Za-z0-9+/=]+)</pre>', pr.stdout or '')
if not m:
    os.unlink(probe)
    print('chrome sin datos'); sys.exit(1)
d = json.loads(base64.b64decode(m.group(1)).decode('utf-8'))
os.unlink(probe)
print('limite          :', d['limite'])
print('body.scrollH    :', d['body']['scrollH'], ' clientH', d['body']['clientH'])
print('html.scrollH    :', d['html']['scrollH'], ' clientH', d['html']['clientH'])
print('content         :', d.get('content'))
print('pie             :', d.get('pie'))
print('mas bajo        :', d['mas_bajo'])
print('aire inferior   :', d['aire_inferior'], 'px')
print('topline.top     :', d['aire_superior'], 'px')
print('bloques         :')
for b in d.get('bloques') or []:
    print('   %-22s %4d-%4d  mt=%s' % (b[0], b[1], b[2], b[3]))
print('imgs            :', d['imgs'])
print('fonts           :', d['fonts_status'], d['familias'])
if d['body']['scrollH'] > d['limite']:
    print('VEREDICTO       : DESBORDA %d px' % (d['body']['scrollH'] - d['limite']))
elif d['aire_inferior'] < 0:
    print('VEREDICTO       : contenido fuera del lienzo %d px' % (-d['aire_inferior']))
else:
    print('VEREDICTO       : cabe, aire inferior %d px' % d['aire_inferior'])
