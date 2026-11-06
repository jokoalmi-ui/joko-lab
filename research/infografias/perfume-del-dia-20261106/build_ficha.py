#!/usr/bin/env python3
# build_ficha.py — ficha del día 2026-11-06 · The Original (Eight & Bob)
# Parte de la plantilla canónica v5 y sustituye por anclas literales
# fail-closed (si un ancla no existe o aparece !=1 vez, aborta sin escribir).
import sys, os

TPL = os.path.expanduser('~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.expanduser('~/.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
OUT = 'ficha_eightbob_v8.html'

html = open(TPL, encoding='utf-8').read()

REPS = [
 ("background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
  "background:url('eightbob_fondo_b.png') center/cover no-repeat;"),

 ('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
  '<div class="fecha-sep">VIERNES · 06 NOVIEMBRE 2026</div>'),

 ('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
  'src="eightbob_figura.png" alt="The Original Eight &amp; Bob"'),
 ('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
  '<div class="reflejo"><img src="eightbob_figura.png" alt=""></div>'),

 ('<div class="casa">Profumum Roma</div>', '<div class="casa">Eight &amp; Bob</div>'),
 ('<h1>Acqua di Sale</h1>', '<h1>The Original</h1>'),
 ('<div class="sub">el mar embotellado de Cerdeña</div>',
  '<div class="sub">el secreto que Kennedy se llevó de París</div>'),

 ('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
  '<div class="dh"><b>2012</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Aromática amaderada</div>'),
 ('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
  '<div class="dh">Perfumista: <b>Albert Fouquet</b> (creación original, 1937)</div>'),
 ('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
  '<div class="dh">Longevidad <b>~7-8 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>220 €</b> / 100 ml<span class="f">Duración: Fragrantica/Parfumo — eightandbob.com · consultado 06-11-2026</span></div>'),
 ('<span class="r-num">4,15</span>', '<span class="r-num">4,05</span>'),
 ('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
  '<span class="r-meta">1.446 votos · 223 reseñas · Fragrantica</span>'),

 # pirámide · leyenda
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">cardamomo, pimienta rosa y limón — especiado limpio, no golpea</span></div>'),
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#116f89);"></span><span class="lab" style="color:#0b5568;">Corazón</span><span class="not">maderas, labdanum y hoja de violeta — el giro seco y algo empolvado</span></div>'),
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#0d1c26;">Fondo</span><span class="not">ámbar, sándalo y vetiver — la parte cálida que aguanta la tarde</span></div>'),
 ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
  '<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial de la casa (eightandbob.com)</span>'),

 # capas SVG
 ("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' }",
  "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'CARDAMOMO · PIMIENTA · LIMÓN' }"),
 ("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' }",
  "{ w: 420, f:'#116f89', t:'#3fa8c4', l:'#0b5568', c1:'CORAZÓN', txt:'MADERAS · LABDANUM · VIOLETA' }"),
 ("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
  "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'ÁMBAR · SÁNDALO · VETIVER' }"),

 # inspiración (historia real de la casa)
 ('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
  '<p>“En los años treinta Albert Fouquet vestía de perfume a la élite de París. Una noche conoció a un joven John F. Kennedy, que le pidió una muestra de más: «eight… and, if possible, one for Bob» — ocho, y a ser posible una para Bob, su hermano Robert.”</p>'),
 ('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
  '<span class="fuente-line">— Casa Eight &amp; Bob · historia oficial [traducida del inglés]</span>'),

 # alternativas
 ('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
  '<div class="alt-item"><span class="alt-n">Fahrenheit 32</span><span class="alt-casa">Dior · 2007</span><span class="alt-rt">4,08/5 · 2.573 votos</span><span class="alt-motivo">la comunidad lo da por equivalente directo (descatalogado)</span></div>'),
 ('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
  '<div class="alt-item"><span class="alt-n">Santal 33</span><span class="alt-casa">Le Labo · 2011</span><span class="alt-rt">3,74/5 · 14.005 votos</span><span class="alt-motivo">mismo cardamomo y hoja de violeta, más sándalo y cuero</span></div>'),
 ('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
  '<div class="alt-item"><span class="alt-n">Cap d\'Antibes</span><span class="alt-casa">Eight &amp; Bob · 2025</span><span class="alt-rt">4,00/5 · 41 votos</span><span class="alt-motivo">la misma casa: hoja de violeta, más verde y luminosa</span></div>'),
 ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
  '<span class="fuente-line" style="margin-left:44px;">Asociaciones: Parfumo · reseñas Fragrantica — consultado 06-nov-2026</span>'),

 # cita comunidad (reseña real, traducida)
 ('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
  '<blockquote>“La longevidad y la estela son buenas: fresco, amaderado y jabonoso, dulce de vainilla y sándalo sin picor, y el cardamomo con los cítricos le dan una dimensión casi textil.”</blockquote>'),
 ('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
  '<span class="fuente-line">— Reseña en Fragrantica · [traducido del inglés]</span>'),

 # pie
 ('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
  '<div class="clima">Ventana 08-18: 5,4–15,5 °C · media 12,1 °C · 0 % lluvia<br>amplitud 10,5 °C · cítrico-amaderado de rango ancho</div>'),
 ('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
  '<div class="sprays">Sprays: <b>4</b> mañana (8,8 °C) · <b>3</b> tarde (14,7 °C)<br><span class="donde">cuello y pecho · trabajo y calle · día fresco</span><br><span class="caveat-pie">que aguante hasta la noche</span></div>'),

 ('<div class="nota-fondo">fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab</div>',
  '<div class="nota-fondo">fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab</div>'),
]

for old, new in REPS:
    n = html.count(old)
    if n != 1:
        sys.exit(f'ABORTA: ancla aparece {n} veces (esperado 1): {old[:70]!r}')
    html = html.replace(old, new)

# estrella parcial al 5 % (rating 4,05)
if html.count('stop offset="15%"') != 2:
    sys.exit('ABORTA: estrella parcial no localizada')
html = html.replace('stop offset="15%"', 'stop offset="5%"')

# suelo tipografico v8 tambien en el rotulo SVG (8,5 -> 12 px; menos tracking para no desbordar)
for old, new in (("t1.setAttribute('font-size', '8.5')", "t1.setAttribute('font-size', '12')"),
                 ("t1.setAttribute('letter-spacing', '2')", "t1.setAttribute('letter-spacing', '1.4')")):
    if html.count(old) != 1:
        sys.exit(f'ABORTA: rotulo SVG ancla {html.count(old)} veces')
    html = html.replace(old, new)
old_fill = "t1.setAttribute('fill', '#fff'); t1.textContent = c.c1;"
new_fill = "t1.setAttribute('fill', (c.f === '#d99c26' ? '#2b1c00' : '#fff')); t1.textContent = c.c1;"
old_fill2 = "t2.setAttribute('font-weight', '800'); t2.setAttribute('fill', '#fff');"
new_fill2 = "t2.setAttribute('font-weight', '800'); t2.setAttribute('fill', (c.f === '#d99c26' ? '#2b1c00' : '#fff'));"
for old, new in ((old_fill, new_fill), (old_fill2, new_fill2)):
    if html.count(old) != 1:
        sys.exit(f'ABORTA: fill SVG ancla {html.count(old)} veces')
    html = html.replace(old, new)

# hex de titulos de seccion Y de los chips .sec-num (llevan texto blanco encima):
# el tono crudo de la plantilla da 3,64:1 con blanco y 3,49:1 sobre crema -> incumple AA.
for old, new in (('#12789e', '#0a5d7a'), ('#0e7c7b', '#0a5f5e'),
                 ('#c96f1c', '#8f4409'), ('#5b42e6', '#3a2aa8')):
    print(f'  hex {old}->{new}: {html.count(old)}')
    html = html.replace(old, new)

# CSS v8 al FINAL DEL BODY (nunca antes de </head>)
css = open(CSS, encoding='utf-8').read()
tag = '<style id="norma-sin-cajas-v8">\n' + css + '\n</style>\n</body>'
if html.count('</body>') != 1:
    sys.exit('ABORTA: </body> no único')
html = html.replace('</body>', tag)

open(OUT, 'w', encoding='utf-8').write(html)
print('OK escrito', OUT, len(html), 'chars')
