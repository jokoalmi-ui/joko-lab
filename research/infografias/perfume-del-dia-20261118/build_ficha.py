#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la ficha del 2026-11-18 (Vibrato, Sospiro) desde la plantilla v5.
Fail-closed: cada sustitucion debe aparecer exactamente 1 vez."""
import os, sys

HOME = os.path.expanduser('~')
TPL = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html')
CSS = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
DIR = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261118')
FONDO = os.environ.get('FONDO', 'vibrato_fondo.png')
SUF = os.environ.get('SUFIJO', '')
OUT = os.path.join(DIR, 'ficha_20261118%s.html' % SUF)

STAR = '<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>'


def star_pct(p):
    return ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h5">'
            '<stop offset="%d%%" stop-color="#c9971c"/><stop offset="%d%%" stop-color="#d8d4c8"/>'
            '</linearGradient></defs><path fill="url(#h5)" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>' % (p, p))


REPS = [
    # fondo y figura
    ("url('acqua_di_sale_fondo.png')", "url('__FONDO__')", 'fondo'),
    ('<img class="frasco-figura" src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma">',
     '<img class="frasco-figura" src="vibrato_figura.png" alt="Vibrato Sospiro">', 'figura'),
    ('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
     '<div class="reflejo"><img src="vibrato_figura.png" alt=""></div>', 'reflejo-src'),
    # cabecera
    ('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
     '<div class="fecha-sep">MIÉRCOLES · 18 NOVIEMBRE 2026</div>', 'fecha'),
    ('<div class="casa">Profumum Roma</div>', '<div class="casa">Sospiro</div>', 'casa'),
    ('<h1>Acqua di Sale</h1>', '<h1>Vibrato</h1>', 'h1'),
    ('<div class="sub">el mar embotellado de Cerdeña</div>',
     '<div class="sub">pomelo, jengibre y madera rubia</div>', 'sub'),
    ('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
     '<div class="dh"><b>2022</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Cítrico aromático</div>', 'dh1'),
    ('Perfumistas: <b>Felice, Luciano y Maria Durante</b>', 'Perfumista: <b>Christian Provenzano</b>', 'perfumista'),
    ('Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span>',
     'Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>249,95 €</b> / 100 ml<span class="f">sabina.com · consultado 17-11-2026 · ficha 18-11-2026 · longevidad: BD del lab</span>', 'precio'),
    ('<span class="r-num">4,15</span>', '<span class="r-num">4,54</span>', 'rnum'),
    ('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
     '<span class="r-meta">7.185 votos · 947 reseñas · Fragrantica · consultado 17-11-2026</span>', 'rmeta'),
    (STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + star_pct(15),
     STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + star_pct(91), 'estrellas'),
    # piramide: leyenda
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: pomelo, bergamota y mandarina — cítrico con jengibre</span></div>', 'pl1'),
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: magnolia, rosa damascena y madera rubia</span></div>', 'pl2'),
    ('<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span></div>',
     '<div class="pl"><span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: vetiver, sándalo y ámbar cristal — horas en la piel</span></div>', 'pl3'),
    ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
     '<span class="fuente-line" style="margin-top:4px;">Pirámide: sospirointernational.com · consultado 17-11-2026</span>', 'notas-fuente'),
    # losas 3D
    ("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
     "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'POMELO · BERGAMOTA · MANDARINA' },", 'capa1'),
    ("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
     "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'MAGNOLIA · ROSA · MADERA RUBIA' },", 'capa2'),
    ("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
     "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VETIVER · SÁNDALO · ÁMBAR' }", 'capa3'),
    # inspiracion
    ('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
     '<p>Vibrato es un cítrico-aromático de autor: abre con pomelo, bergamota, mandarina y jengibre sobre un corazón de magnolia y rosa damascena, y se cierra con vetiver, sándalo indio y ámbar cristal. La comunidad lo describe como un cítrico con cuerpo —verde, con un punto dulce de jengibre— y con una duración muy por encima de lo habitual en su familia.</p>', 'insp'),
    ('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
     '<span class="fuente-line">— Casa Sospiro · pirámide oficial + reseñas Fragrantica [síntesis, no cita literal] · 17-11-2026</span>', 'insp-fuente'),
    # alternativas
    ('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
     '<div class="alt-item"><span class="alt-n">Tygar</span><span class="alt-casa">Bvlgari · 2016</span><span class="alt-rt">4,45/5 · 4.857 votos</span><span class="alt-motivo">mismo pomelo amaderado, más seco</span></div>', 'alt1'),
    ('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
     '<div class="alt-item"><span class="alt-n">Turathi Blue</span><span class="alt-casa">Afnan · 2020</span><span class="alt-rt">4,34/5 · 6.345 votos</span><span class="alt-motivo">el clon económico del ADN Tygar</span></div>', 'alt2'),
    ('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
     '<div class="alt-item"><span class="alt-n">Vibrato Nero</span><span class="alt-casa">Sospiro · 2026</span><span class="alt-rt">4,00/5 · 8 votos</span><span class="alt-motivo">el flanker nuevo, más dulce y con cuero</span></div>', 'alt3'),
    ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
     '<span class="fuente-line" style="margin-left:44px;">Similitudes: reseñas Fragrantica (Tygar/Ingenious Ginger) · ratings Fragrantica · consultado 17-11-2026</span>', 'alt-fuente'),
    # comunidad
    ('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
     '<blockquote>“Fresco y veraniego. Sabe a verde, a dulce y a jengibre. Muy agradable y fácil de entender. La duración en piel es muy buena: llega a la noche con buena intensidad y estela.”</blockquote>', 'cita'),
    ('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
     '<span class="fuente-line">— Edoardo2005 en Fragrantica.it · comunidad [traducida] · 28-06-2026</span>', 'cita-fuente'),
    # pie
    ('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
     '<div class="clima">08-18 h: <b>15,6–19,3 °C</b> · media 17,7 · 48 % lluvia<br>amplitud 4,3 °C · cítrico aromático para un día templado y húmedo</div>', 'clima'),
    ('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
     '<div class="sprays">Sprays: <b>3</b> oficina · <b>3</b> calle<br><span class="donde">cuello y pecho · oficina y calle · no en cerrado</span><br><span class="caveat-pie">un cítrico con cuerpo, no una colonia</span></div>', 'sprays'),
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
