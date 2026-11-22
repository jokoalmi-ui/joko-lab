#!/usr/bin/env python3
# Ficha 2026-11-14 · Prada L'Homme Intense (Prada)
# Genera el HTML del dia desde la plantilla canonica v5 con sustituciones fail-closed.
import os
import sys

HOME = os.path.expanduser('~')
TPL = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
D = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261114')
OUT = os.path.join(D, 'ficha_20261114.html')
FONDO = 'prada_lhomme_intense_fondo.png'
FRASCO = 'prada_figura.png'

html = open(TPL, encoding='utf-8').read()

REPS = []


def rep(old, new):
    REPS.append((old, new))


rep("background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "background:url('%s') center/cover no-repeat;" % FONDO)

rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">SÁBADO · 14 NOVIEMBRE 2026</div>')

rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    'src="%s" alt="Prada L\'Homme Intense"' % FRASCO)

rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    '<div class="reflejo"><img src="%s" alt=""></div>' % FRASCO)

rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Prada</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>L\'Homme Intense</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">iris empolvado, ámbar y cuero</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2017</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Oriental amaderada</div>')

rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Daniela Andrier</b></div>')

rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
    '<span class="sep">·</span><b>86,94 €</b> / 100 ml'
    '<span class="f">primor.eu · PVP 153,00 € · consultado 13-11-2026 · precio de la ficha del 14-11-2026</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">8,4</span>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">8,4/10 · 2.709 valoraciones · Parfumo · consultado 13-11-2026</span>')

# piramide: leyenda
rep('<span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="lab" style="color:#a57112;">Salida</span><span class="not">el arranque: iris empolvado, limpio y seco</span>')
rep('<span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el giro: ámbar cálido y cuero suave</span>')
rep('<span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: sándalo, pachulí y haba tonka</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: Prada (descripción oficial) · listado Parfumo · reparto por capas: reseña Parfumo</span>')

# piramide: losas SVG
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'IRIS' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ÁMBAR · CUERO' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'SÁNDALO · PACHULÍ · HABA TONKA' }")

# inspiracion oficial
INSP = ('«L\'Homme Prada Intense expresa la multiplicidad de la identidad masculina. En el corazón de la '
        'fragancia, el ámbar, el pachulí, el iris y las habas tonka crean combinaciones de notas que acentúan '
        'las infinitas facetas del hombre de Prada, aportando una dimensión oriental y etérea a las notas de '
        'salida que acentúan su fondo amaderado. Es un aroma creado a base de contraposiciones, que representa '
        'la dualidad de la identidad masculina: una fragancia poderosa para un hombre carismático y decidido.»')
rep('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
    '<p>%s</p>' % INSP)
rep('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
    '<span class="fuente-line">— Prada · descripción oficial del producto (vía primor.eu, consultado 13-11-2026)</span>')

# alternativas
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Homme Intense</span><span class="alt-casa">Dior · 2007</span>'
    '<span class="alt-rt">8,5/10 · 461 votos</span><span class="alt-motivo">el iris con cuero, más denso</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Gentleman EDP</span><span class="alt-casa">Givenchy · 2018</span>'
    '<span class="alt-rt">8,0/10 · 1.928 votos</span><span class="alt-motivo">iris y pachulí, más seco</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">L\'Homme</span><span class="alt-casa">Prada · 2016</span>'
    '<span class="alt-rt">8,4/10 · 8.202 votos</span><span class="alt-motivo">misma casa, más limpio y cítrico</span></div>')
rep('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
    '<span class="fuente-line" style="margin-left:44px;">Similitudes: Parfumo «similar» y reseñas comparativas · ratings Parfumo · consultado 13-11-2026</span>')

# cita comunidad
rep('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
    '<blockquote>“Arranca con la consabida nota de iris, su aroma empolvado, un ámbar cálido y un cuero suave '
    'y rico. Es muy agradable y tiene un perfil notablemente más oscuro que el L\'Homme original. […] Más '
    'avanzado el uso llegamos a una base de sándalo y pachulí; aprecio lo sutiles que son estas notas finales '
    'y cómo se limitan a realzar el conjunto.”</blockquote>')
rep('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
    '<span class="fuente-line">— Reseña en Parfumo · comunidad [traducida del inglés] · consultado 13-11-2026</span>')

# pie
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">Ventana 08-18: 9,1–17,1 °C · media 14,9 °C · 35 % lluvia<br>'
    'amplitud 8,2 °C · humedad 82 % · amaderada oriental para día fresco de otoño</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3</b> · mañana 3-4, tarde 3<br>'
    '<span class="donde">cuello y pecho · oficina y calle · discreto</span><br>'
    '<span class="caveat-pie">iris y cuero: elegante sin gritar</span></div>')

for old, new in REPS:
    n = html.count(old)
    if n != 1:
        sys.exit('ABORTA: ancla aparece %d veces (esperado 1): %r' % (n, old[:80]))
    html = html.replace(old, new)

# estrella parcial: 8,4/10 = 4,2/5 -> 20 %
if html.count('stop offset="15%"') != 2:
    sys.exit('ABORTA: estrella parcial no localizada (%d)' % html.count('stop offset="15%"'))
html = html.replace('stop offset="15%"', 'stop offset="20%"')

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
