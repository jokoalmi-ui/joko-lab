#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ficha del día 10-11-2026 · Bois Mystique (Houbigant) · sustitución fail-closed sobre plantilla v5."""
import os, sys

TPL = os.path.expanduser('~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.expanduser('~/.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
OUT = 'ficha_boismystique_v8.html'

html = open(TPL, encoding='utf-8').read()

REPS = [
 ("background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
  "background:url('bois_mystique_fondo.png') center/cover no-repeat;"),

 ('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
  '<div class="fecha-sep">MARTES · 10 NOVIEMBRE 2026</div>'),

 ('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
  'src="bois_mystique_figura.png" alt="Bois Mystique Houbigant"'),
 ('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
  '<div class="reflejo"><img src="bois_mystique_figura.png" alt=""></div>'),

 ('<div class="casa">Profumum Roma</div>', '<div class="casa">Houbigant</div>'),
 ('<h1>Acqua di Sale</h1>', '<h1>Bois Mystique</h1>'),
 ('<div class="sub">el mar embotellado de Cerdeña</div>',
  '<div class="sub">cardamomo, olibano y cedro</div>'),

 ('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
  '<div class="dh"><b>2018</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Amaderada especiada</div>'),
 ('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
  '<div class="dh">Perfumista: <b>Luca Maffei</b></div>'),
 ('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
  '<div class="dh">Longevidad <b>~9 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>200,00 €</b> / 100 ml<span class="f">100 ml · houbigant-parfum.com · consultado 10-11-2026</span></div>'),
 ('<span class="r-num">4,15</span>', '<span class="r-num">4,38</span>'),
 ('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
  '<span class="r-meta">499 votos · Fragrantica</span>'),

 # pirámide · leyenda
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">cardamomo, jengibre y neroli — el arranque especiado</span></div>'),
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#116f89);"></span><span class="lab" style="color:#0b5568;">Corazón</span><span class="not">olibano, cipriol e iris — el humo de iglesia</span></div>'),
 ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span></div>',
  '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#0d1c26;">Fondo</span><span class="not">cedro, mirra y guayaco — la madera seca que queda</span></div>'),
 ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
  '<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica — contrastadas con Parfumo</span>'),

 # capas SVG
 ("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' }",
  "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'CARDAMOMO · JENGIBRE · NEROLI' }"),
 ("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' }",
  "{ w: 420, f:'#116f89', t:'#3fa8c4', l:'#0b5568', c1:'CORAZÓN', txt:'OLIBANO · CIPRIOL · IRIS' }"),
 ("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
  "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · MIRRA · GUAYACO' }"),

 # inspiración
 ('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
  '<p>Un bois especiado construido en tres columnas: cardamomo, jengibre y neroli arriba; olibano —incienso— y cipriol en el corazón; y un fondo de cedro, mirra y guayaco. Lo firma Luca Maffei para una casa parisina fundada en 1775, la misma que en 1882 puso el primer fougère en el mercado con Fougère Royale. Aquí el gesto es otro: madera seca, resina y un punto de iglesia, sin dulzor.</p>'),
 ('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
  '<span class="fuente-line">— Casa Houbigant · ficha oficial y perfumista [traducida del inglés]</span>'),

 # alternativas
 ('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
  '<div class="alt-item"><span class="alt-n">Royal Oud</span><span class="alt-casa">Creed · 2011</span><span class="alt-rt">8,2/10 · 2.018 votos</span><span class="alt-motivo">mismo incienso y cedro, con más cuerpo</span></div>'),
 ('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
  '<div class="alt-item"><span class="alt-n">Equus</span><span class="alt-casa">Lalique · 2001</span><span class="alt-rt">7,5/10 · 167 votos</span><span class="alt-motivo">especiado amaderado clásico, mucho más barato</span></div>'),
 ('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
  '<div class="alt-item"><span class="alt-n">Bo</span><span class="alt-casa">Liis · 2021</span><span class="alt-rt">7,8/10 · 390 votos</span><span class="alt-motivo">la lectura moderna y limpia del mismo bosque</span></div>'),
 ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
  '<span class="fuente-line" style="margin-left:44px;">Asociaciones: similares de Parfumo · reseñas Fragrantica — consultado 10-nov-2026</span>'),

 # cita comunidad
 ('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
  '<blockquote>“De esta casa no encuentro un perfume malo: todos son clásicos, para llevar con traje o ropa formal. Un aroma de oficina sofisticado.”</blockquote>'),
 ('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
  '<span class="fuente-line">— Reseña de MKramer en Parfumo · [traducida del inglés]</span>'),

 # pie
 ('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
  '<div class="clima">Ventana 08-18: 18,6–21,9 °C · media 20,2 °C · 48 % lluvia<br>amplitud 5,2 °C · amaderada de incienso para día templado</div>'),
 ('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
  '<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · oficina y calle · templado</span><br><span class="caveat-pie">que llegue a la tarde sin cansar</span></div>'),

 ('<div class="nota-fondo">fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab</div>',
  '<div class="nota-fondo">fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab</div>'),
]

for old, new in REPS:
    n = html.count(old)
    if n != 1:
        sys.exit(f'ABORTA: ancla aparece {n} veces (esperado 1): {old[:70]!r}')
    html = html.replace(old, new)

# estrella parcial al 38 % (rating 4,38)
if html.count('stop offset="15%"') != 2:
    sys.exit('ABORTA: estrella parcial no localizada')
html = html.replace('stop offset="15%"', 'stop offset="38%"')

# suelo tipografico v8 tambien en el rotulo SVG
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

# hex de titulos de seccion Y de los chips .sec-num (llevan texto blanco encima)
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
