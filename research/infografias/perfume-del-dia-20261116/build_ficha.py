#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la ficha del 2026-11-16 (Tuttle, Tiziana Terenzi) desde la plantilla v5.
Fail-closed: cada sustitucion debe aparecer exactamente 1 vez."""
import os, sys

HOME = os.path.expanduser('~')
TPL = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
DIR = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261116')
FONDO = os.environ.get('FONDO', 'tuttle_fondo.png')      # palanca de tono (11-11-2026)
SUF = os.environ.get('SUFIJO', '')                        # '' = version base; '_d80' = variante
OUT = os.path.join(DIR, 'ficha_20261116%s.html' % SUF)

STAR = '<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>'
STAR_OFF = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
            'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STAR_5 = ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h5">'
          '<stop offset="5%" stop-color="#c9971c"/><stop offset="5%" stop-color="#d8d4c8"/>'
          '</linearGradient></defs><path fill="url(#h5)" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')

REPS = [
    # fondo y figura
    ("url('acqua_di_sale_fondo.png')", "url('__FONDO__')", 'fondo'),
    ('<img class="frasco-figura" src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma">',
     '<img class="frasco-figura" src="tuttle_figura.png" alt="Tuttle Tiziana Terenzi">', 'figura'),
    ('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
     '<div class="reflejo"><img src="tuttle_figura.png" alt=""></div>', 'reflejo-src'),
    # cabecera
    ('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
     '<div class="fecha-sep">LUNES · 16 NOVIEMBRE 2026</div>', 'fecha'),
    ('<div class="casa">Profumum Roma</div>', '<div class="casa">Tiziana Terenzi</div>', 'casa'),
    ('<h1>Acqua di Sale</h1>', '<h1>Tuttle</h1>', 'h1'),
    ('<div class="sub">el mar embotellado de Cerdeña</div>',
     '<div class="sub">pomelo, melocotón y ámbar gris</div>', 'sub'),
    ('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
     '<div class="dh"><b>2021</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Frutal amaderada</div>', 'dh1'),
    ('Perfumistas: <b>Felice, Luciano y Maria Durante</b>', 'Perfumista: <b>Paolo Terenzi</b>', 'perfumista'),
    ('Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span>',
     'Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>425,00 €</b> / 100 ml<span class="f">perfumerialaura.com · consultado 15-11-2026 · ficha 16-11-2026</span>', 'precio'),
    ('<span class="r-num">4,15</span>', '<span class="r-num">8,1</span>', 'rnum'),
    ('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
     '<span class="r-meta">8,1/10 · 109 votos · Parfumo · consultado 15-11-2026</span>', 'rmeta'),
    # estrellas: 4 llenas + 1 al 5 %  == 4,05/5 == 8,1/10
    (STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            '
     + '<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h5"><stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/></linearGradient></defs><path fill="url(#h5)" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>',
     STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR_5, 'estrellas'),
    # piramide: leyenda
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: pomelo siciliano, grosella negra y melocotón — fruta al sol</span></div>', 'pl1'),
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: tuberosa, magnolia e iris — nata floral con ámbar gris</span></div>', 'pl2'),
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: sándalo, cedro, pachulí y vetiver — madera cálida en la piel</span></div>', 'pl3'),
    ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
     '<span class="fuente-line" style="margin-top:4px;">Pirámide: parfumo.com (pirámide de la casa) · consultado 15-11-2026</span>', 'notas-fuente'),
    # losas 3D
    ("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
     "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'POMELO · GROSELLA NEGRA' },", 'capa1'),
    ("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
     "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'TUBEROSA · MAGNOLIA · IRIS' },", 'capa2'),
    ("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
     "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'SÁNDALO · CEDRO · PACHULÍ · VETIVER' }", 'capa3'),
    # inspiracion
    ('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
     '<p>Tuttle es un cometa que vuelve: la casa lo incluye en la colección Comete y lo describe como un golpe de fruta luminosa —pomelo siciliano, grosella negra y melocotón— que se asienta en un fondo de maderas, pachulí y ámbar gris. Un aroma brillante de salida y cálido de fondo, pensado para dejar rastro sin gritar.</p>', 'insp'),
    ('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
     '<span class="fuente-line">— Casa Tiziana Terenzi · colección Comete [síntesis de la descripción, no cita literal] · 15-11-2026</span>', 'insp-fuente'),
    # alternativas
    ('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
     '<div class="alt-item"><span class="alt-n">Rosso Pompei</span><span class="alt-casa">Tiziana Terenzi</span><span class="alt-rt">8,1/10 · 1.180 votos</span><span class="alt-motivo">misma casa, más cítrico y rotundo</span></div>', 'alt1'),
    ('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
     '<div class="alt-item"><span class="alt-n">Turathi Blue</span><span class="alt-casa">Afnan · 2021</span><span class="alt-rt">8,1/10 · 4.057 votos</span><span class="alt-motivo">mismo ADN cítrico, ya en tu colección</span></div>', 'alt2'),
    ('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
     '<div class="alt-item"><span class="alt-n">Vibrato</span><span class="alt-casa">Sospiro · 2022</span><span class="alt-rt">8,8/10 · 2.951 votos</span><span class="alt-motivo">pomelo y jengibre, más fresco</span></div>', 'alt3'),
    ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
     '<span class="fuente-line" style="margin-left:44px;">Similitudes: Parfumo «smells similar» · ratings Parfumo · consultado 15-11-2026</span>', 'alt-fuente'),
    # comunidad
    ('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
     '<blockquote>“Puedo decir con firmeza que es mi descubrimiento del verano. Sale un pomelo punzante delicioso que en pocos minutos se calma con un melocotón y una grosella negra deliciosos… Proyección brutal las tres primeras horas y después se percibe a menos de un metro durante otras cinco.”</blockquote>', 'cita'),
    ('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
     '<span class="fuente-line">— Jaular en Parfumo · comunidad [traducida] · 15-11-2026</span>', 'cita-fuente'),
    # pie
    ('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
     '<div class="clima">08-18 h: <b>14,3–16,9 °C</b> · media 15,6 · 13 % lluvia<br>amplitud 5,1 °C · frutal amaderada para un día templado</div>', 'clima'),
    ('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
     '<div class="sprays">Sprays: <b>2</b> oficina · <b>3</b> calle<br><span class="donde">cuello y pecho · oficina y calle · no en cerrado</span><br><span class="caveat-pie">fruta luminosa que deja rastro</span></div>', 'sprays'),
]

html = open(TPL, encoding='utf-8').read()
for old, new, tag in REPS:
    new = new.replace('__FONDO__', FONDO)
    n = html.count(old)
    if n != 1:
        sys.exit('FAIL %s: %d ocurrencias' % (tag, n))
    html = html.replace(old, new)

css = open(CSS, encoding='utf-8').read()
if '</body>' not in html:
    sys.exit('FAIL: sin </body>')
html = html.replace('</body>', '<style id="norma-sin-cajas-v8">\n' + css + '\n</style>\n</body>')

open(OUT, 'w', encoding='utf-8').write(html)
print('OK', OUT, len(html), 'bytes')
