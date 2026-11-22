#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la ficha del 2026-11-22 (Lalique Encre Noire a L'Extreme) partiendo del HTML
canonico del 21-11 (plantilla v5 + norma v8), sin tocar la ficha publicada del 21.
Fail-closed: cada sustitucion debe aparecer exactamente 1 vez.
"""
import os, re, sys

HOME = os.path.expanduser('~')
BASE = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261121/ficha_20261121.html')
CSS = os.path.join(HOME, '.hermes/skills/joko-lab/perfume-del-dia/templates/norma-legibilidad-v8.css')
DIR = os.path.join(HOME, 'joko-lab/research/infografias/perfume-del-dia-20261122')
FONDO = os.environ.get('FONDO', 'encre_noire_extreme_fondo.png')
FIGURA = os.environ.get('FIGURA', 'encre_noire_extreme_figura.png')
OUT = os.path.join(DIR, 'ficha_20261122.html')

STAR = '<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>'


def star_pct(p):
    return ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h5">'
            '<stop offset="%d%%" stop-color="#c9971c"/><stop offset="%d%%" stop-color="#d8d4c8"/>'
            '</linearGradient></defs><path fill="url(#h5)" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>' % (p, p))


REPS = [
    # fondo y figura
    ("url('ambre_fondo.png')", "url('__FONDO__')", 'fondo'),
    ('<img class="frasco-figura" src="ambre_figura.png" alt="Ambre Tabac Daniel Josier">',
     '<img class="frasco-figura" src="__FIGURA__" alt="Encre Noire a L\'Extreme Lalique">', 'figura'),
    ('<div class="reflejo"><img src="ambre_figura.png" alt=""></div>',
     '<div class="reflejo"><img src="__FIGURA__" alt=""></div>', 'reflejo-src'),
    # cabecera
    ('<div class="fecha-sep">SÁBADO · 21 NOVIEMBRE 2026</div>',
     '<div class="fecha-sep">DOMINGO · 22 NOVIEMBRE 2026</div>', 'fecha'),
    ('<div class="casa">Daniel Josier</div>', '<div class="casa">Lalique</div>', 'casa'),
    ('<h1>Ambre Tabac</h1>', '<h1>Encre Noire à L\'Extrême</h1>', 'h1'),
    ('<div class="sub">el ámbar que huele a tabaco dulce</div>',
     '<div class="sub">el vetiver que se vuelve tinta</div>', 'sub'),
    ('<div class="dh"><b>2014</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Oriental amaderado</div>',
     '<div class="dh"><b>2015</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Amaderada aromática</div>', 'dh1'),
    ('<div class="dh">Perfumista: <b>Daniel Josier</b></div>',
     '<div class="dh">Perfumista: <b>Nathalie Lorson</b></div>', 'perfumista'),
    ('<div class="dh">Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>90,00 €</b> / 100 ml<span class="f">danieljosier.com · consultado 20-11-2026 · ficha 21-11-2026</span></div>',
     '<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>69,98 €</b> / 100 ml<span class="f">Perfumería Laura · consultado 21-11-2026 · ficha 22-11-2026</span></div>', 'precio'),
    ('<span class="r-num">4,57</span>', '<span class="r-num">4,21</span>', 'rnum'),
    ('<span class="r-meta">866 votos · Fragrantica · consultado 20-11-2026</span>',
     '<span class="r-meta">8.491 votos · Fragrantica · consultado 21-11-2026</span>', 'rmeta'),
    (STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + star_pct(57),
     STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + STAR + '\n            ' + star_pct(21), 'estrellas'),
    # piramide: leyenda
    ('<span class="not">humo frío: incienso de África y bergamota</span>',
     '<span class="not">humo y resina: ciprés, elemí y bergamota</span>', 'pl1'),
    ('<span class="not">el alma: sándalo y pachulí — madera cremosa</span>',
     '<span class="not">el alma: dos vetiver, incienso e iris — tinta y ceniza</span>', 'pl2'),
    ('<span class="not">el abrigo: hoja de tabaco, ámbar y vainilla</span>',
     '<span class="not">el abrigo: sándalo, pachulí y benjuí</span>', 'pl3'),
    ('<span class="fuente-line" style="margin-top:4px;">Pirámide: danieljosier.com + Fragrantica · consultado 20-11-2026</span>',
     '<span class="fuente-line" style="margin-top:4px;">Pirámide: Fragrantica + Parfumo · consultado 21-11-2026</span>', 'notas-fuente'),
    # losas 3D
    ("c1:'SALIDA', txt:'INCIENSO · BERGAMOTA' },",
     "c1:'SALIDA', txt:'CIPRÉS · ELEMÍ · BERGAMOTA' },", 'capa1'),
    ("c1:'CORAZÓN', txt:'SÁNDALO · PACHULÍ' },",
     "c1:'CORAZÓN', txt:'VETIVER HAITÍ · JAVA · INCIENSO' },", 'capa2'),
    ("c1:'FONDO', txt:'TABACO · ÁMBAR · VAINILLA' }",
     "c1:'FONDO', txt:'SÁNDALO · PACHULÍ · BENJUÍ' }", 'capa3'),
    # inspiracion
    ('<p>Daniel Josier lleva desde 2014 haciendo perfumería de autor desde Madrid, y Ambre Tabac es su fragancia más votada. La idea es simple y difícil a la vez: hoja de tabaco dulce sobre ámbar y vainilla, con un incienso frío que evita que empalague. Parfumo la sitúa en el puesto 152 de perfumes unisex con 8,5/10 y longevidad por encima de la media; Fragrantica le da 4,57 con 866 votos. Su ADN viene del ámbar especiado de Ambre Narguilé (2004) y Oajan (2013), y a la vez se adelanta a Angels\' Share (2020).</p>',
     '<p>En octubre de 2015 Lalique cerró el círculo que había abierto en 2006 con Encre Noire: misma perfumista, Nathalie Lorson, y mismo frasco, inspirado en el tintero «Encrier» que René Lalique diseñó en 1913. La diferencia es de temperatura: donde el original era tinta seca y viruta de lápiz, el Extrême entra antes con ciprés y elemí y se queda con incienso, benjuí y sándalo. Fragrantica le da 4,21 con 8.491 votos y Parfumo 7,9 con 1.452; en las votaciones de temporada de Parfumo mandan otoño (356) e invierno (316), y la relación calidad-precio es la mejor puntuada de la casa (9,1/10).</p>', 'insp'),
    ('<span class="fuente-line">— Casa Daniel Josier · Parfumo y Fragrantica [traducido] · 20-11-2026</span>',
     '<span class="fuente-line">— Casa Lalique · Fragrantica y Parfumo [traducido] · consultado 21-11-2026</span>', 'insp-fuente'),
    # alternativas
    ('<div class="alt-item"><span class="alt-n">Oajan</span><span class="alt-casa">Parfums de Marly · 2013</span><span class="alt-rt">4,41/5 · 7.274 votos</span><span class="alt-motivo">más rudo y especiado</span></div>',
     '<div class="alt-item"><span class="alt-n">Encre Noire</span><span class="alt-casa">Lalique · 2006</span><span class="alt-rt">4,14/5 · 26.276 votos</span><span class="alt-motivo">el original: más seco, menos resina</span></div>', 'alt1'),
    ('<div class="alt-item"><span class="alt-n">Angels\' Share</span><span class="alt-casa">By Kilian · 2020</span><span class="alt-rt">4,35/5 · 24.795 votos</span><span class="alt-motivo">coñac, más gourmand</span></div>',
     '<div class="alt-item"><span class="alt-n">Memoir Man</span><span class="alt-casa">Amouage · 2010</span><span class="alt-rt">8,0/10 · 1.204 votos</span><span class="alt-motivo">más especiado y ahumado</span></div>', 'alt2'),
    ('<div class="alt-item"><span class="alt-n">Khaltat Night</span><span class="alt-casa">Attar Collection · 2016</span><span class="alt-rt">4,19/5 · 3.230 votos</span><span class="alt-motivo">más dulce y goloso</span></div>',
     '<div class="alt-item"><span class="alt-n">Laudano Nero</span><span class="alt-casa">Tiziana Terenzi · 2014</span><span class="alt-rt">4,06/5 · 3.135 votos</span><span class="alt-motivo">resinoso, casi licoroso</span></div>', 'alt3'),
    ('<span class="fuente-line" style="margin-left:44px;">Similitudes: «Smells similar» de Parfumo · ratings Fragrantica · consultado 20-11-2026</span>',
     '<span class="fuente-line" style="margin-left:44px;">Similitudes: «Smells similar» de Parfumo · Fragrantica · consultado 21-11-2026</span>', 'alt-fuente'),
    # comunidad
    ('<blockquote>“No llena la habitación, no es abrumador y no grita: para mí es un perfume discretamente elegante. La salida está bien, pero en días fríos es en el secado donde brilla de verdad. En piel me dura unas 8 horas y en la ropa probablemente 12. Imagina que acabas de entrar en un humidor climatizado dentro de la mansión de un sultán multimillonario.”</blockquote>',
     '<blockquote>“Huele básicamente a Encre Noire bañado un instante en maderas balsámicas húmedas —ciprés— y espolvoreado con virutas de lápiz y ceniza de incienso.”</blockquote>', 'cita'),
    ('<span class="fuente-line">— JHusker en Fragrantica · comunidad [traducida] · 31-10-2026</span>',
     '<span class="fuente-line">— ColinM en Parfumo · comunidad [traducida] · 10-05-2016</span>', 'cita-fuente'),
    # pie
    ('<div class="clima">08-18 h: <b>12,7–14,4 °C</b> · media 13,6 · 83 % lluvia<br>amplitud 3,9 °C · banda fresca · ámbar y tabaco para un sábado de agua</div>',
     '<div class="clima">08-18 h: <b>9,9–11,9 °C</b> · media 11,1 · 0 % lluvia<br>amplitud 5,3 °C · banda fresca · vetiver y resina para un domingo de niebla</div>', 'clima'),
    ('<div class="sprays">Sprays: <b>3</b> interior · <b>4</b> exterior<br><span class="donde">cuello y pecho · día de lluvia · no en cerrado</span><br><span class="caveat-pie">tabaco dulce, sin empalagar</span></div>',
     '<div class="sprays">Sprays: <b>3</b> interior · <b>4</b> exterior<br><span class="donde">cuello y pecho · día frío y seco · no en cerrado</span><br><span class="caveat-pie">retoca a media tarde</span></div>', 'sprays'),
]

html = open(BASE, encoding='utf-8').read()
# quitar el CSS v8 ya inyectado en el HTML base y reinyectarlo al final (fuente canonica)
html, ncss = re.subn(r'<style id="norma-sin-cajas-v8">.*?</style>\n?', '', html, flags=re.S)
if ncss != 1:
    sys.exit('FAIL: bloques v8 encontrados = %d' % ncss)

for old, new, tag in REPS:
    new = new.replace('__FONDO__', FONDO).replace('__FIGURA__', FIGURA)
    n = html.count(old)
    if n != 1:
        sys.exit('FAIL %s: %d ocurrencias' % (tag, n))
    html = html.replace(old, new)

css = open(CSS, encoding='utf-8').read()
html = html.replace('</body>', '<style id="norma-sin-cajas-v8">\n' + css + '\n</style>\n</body>')
open(OUT, 'w', encoding='utf-8').write(html)
print('OK', OUT, len(html), 'bytes')
