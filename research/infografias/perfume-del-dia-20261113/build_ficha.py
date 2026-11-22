#!/usr/bin/env python3
# Ficha 2026-11-13 · B683 Extrait (Marc-Antoine Barrois)
# Genera el HTML del dia desde la plantilla canonica v5 con sustituciones fail-closed.
import os
import sys

HOME = os.path.expanduser('~')
TPL = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
D = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261113')
OUT = os.path.join(D, 'ficha_20261113.html')
FONDO = 'b683ext_fondo.png'
FRASCO = 'b683_extrait_frasco.png'

html = open(TPL, encoding='utf-8').read()

REPS = []


def rep(old, new):
    REPS.append((old, new))


rep("background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "background:url('%s') center/cover no-repeat;" % FONDO)

rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">VIERNES · 13 NOVIEMBRE 2026</div>')

rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    'src="%s" alt="B683 Extrait Marc-Antoine Barrois"' % FRASCO)

rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    '<div class="reflejo"><img src="%s" alt=""></div>' % FRASCO)

rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Marc-Antoine Barrois</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>B683 Extrait</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">manzana verde, oud de Laos y cuero</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2020</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Especiada cuero amaderada</div>')

rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Quentin Bisch</b></div>')

rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>intensa</b>'
    '<span class="sep">·</span><b>275,00 €</b> / 50 ml'
    '<span class="f">marcantoinebarrois.com · formato único · equivale a 550,00 € / 100 ml'
    ' · consultado 12-11-2026 · precio de la ficha del 13-11-2026</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,07</span>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">851 votos · Fragrantica · consultado 12-11-2026</span>')

# piramide: leyenda
rep('<span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="lab" style="color:#a57112;">Salida</span><span class="not">el mordisco: manzana verde, pimienta negra y comino</span>')
rep('<span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el giro: oud de Laos, safraleine y hoja de violeta</span>')
rep('<span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: pachulí, sándalo y vainilla — cuero final</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica (ficha oficial) · reparto por capas: Parfumo</span>')

# piramide: losas SVG
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'MANZANA · PIMIENTA · COMINO' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'OUD · SAFRALEINE · VIOLETA' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'PACHULÍ · SÁNDALO · VAINILLA' }")

# inspiracion oficial
INSP = ('«Más que una nueva intensidad, B683 EXTRAIT explora un mundo nuevo. Un planeta imaginado por '
        'Marc-Antoine Barrois y Quentin Bisch, donde la naturaleza transfigura sus esencias e hibrida lo '
        'animal y lo vegetal. El mordisco del chile, el olor a piel caliente del comino, la caricia lechosa '
        'del sándalo, la frescura verde de la hoja de violeta, la nota aterciopelada del azafrán. Un acorde '
        'poderoso de elegancia felina que toma su seducción nocturna de un precioso oud de Laos con tonos de '
        'cuero y ámbar. Al contacto, el pachulí de Indonesia se convierte en cuero. Un extrait del 40 % de '
        'concentración con la manzana verde ácida como firma.»')
rep('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
    '<p>%s</p>' % INSP)
rep('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
    '<span class="fuente-line">— Marc-Antoine Barrois · ficha oficial [traducida del inglés]</span>')

# alternativas
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">B683 EDP</span><span class="alt-casa">Barrois · 2016</span>'
    '<span class="alt-rt">7,7/10 · 528 votos</span><span class="alt-motivo">el original, más fresco y sin oud</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Ganymede</span><span class="alt-casa">Barrois · 2019</span>'
    '<span class="alt-rt">8,0/10 · 4.064 votos</span><span class="alt-motivo">misma casa, más aire y menos cuero</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Angham</span><span class="alt-casa">Lattafa · 2024</span>'
    '<span class="alt-rt">8,4/10 · 591 votos</span><span class="alt-motivo">la vía asequible: manzana y cuero dulce</span></div>')
rep('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
    '<span class="fuente-line" style="margin-left:44px;">Similitudes: Parfumo «smells similar» y reseñas comparativas · ratings Parfumo · consultado 12-11-2026</span>')

# cita comunidad
rep('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
    '<blockquote>“En conjunto es una mezcla algo especiada, dulce y amaderada: se siente a medio camino '
    'entre una tarta de manzana y el cuero. Y es justo el cuero y la manzana lo que resulta más '
    'prominente que en el EDP, algo más suave y fresco. Como era de esperar, el Extrait es más denso '
    'y rinde más, y encaja mejor con tiempo fresco y de noche.”</blockquote>')
rep('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
    '<span class="fuente-line">— Reseña en Parfumo · comunidad [traducida del inglés]</span>')

# pie
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">Ventana 08-18: 14,3–17,3 °C · media 15,5 °C · 20 % lluvia<br>'
    'amplitud 4,5 °C · humedad 79 % · especiada cuero amaderada para día templado y gris</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3</b> · bajar a <b>2</b> si la tarde pasa de 17 °C<br>'
    '<span class="donde">cuello y pecho · oficina y calle · discreto</span><br>'
    '<span class="caveat-pie">extrait del 40 %: poco ya es mucho</span></div>')

for old, new in REPS:
    n = html.count(old)
    if n != 1:
        sys.exit('ABORTA: ancla aparece %d veces (esperado 1): %r' % (n, old[:80]))
    html = html.replace(old, new)

# estrella parcial: 4,07/5 -> 7 %
if html.count('stop offset="15%"') != 2:
    sys.exit('ABORTA: estrella parcial no localizada (%d)' % html.count('stop offset="15%"'))
html = html.replace('stop offset="15%"', 'stop offset="7%"')

# hex de titulos de seccion Y fondo de .sec-num (llevan texto blanco encima)
for old, new in (('#12789e', '#0a5d7a'), ('#0e7c7b', '#0a5f5e'),
                 ('#c96f1c', '#8f4409'), ('#5b42e6', '#3a2aa8')):
    print('  hex %s->%s: %d' % (old, new, html.count(old)))
    html = html.replace(old, new)

# CSS v8 al FINAL DEL BODY
css = open(CSS, encoding='utf-8').read()
if html.count('</body>') != 1:
    sys.exit('ABORTA: </body> no unico')
html = html.replace('</body>', '<style id="norma-sin-cajas-v8">\n' + css + '\n</style>\n</body>')

open(OUT, 'w', encoding='utf-8').write(html)
print('OK escrito', OUT, len(html), 'chars')
