#!/usr/bin/env python3
"""Genera la ficha v5 del 20-10-2026 (Ganymede) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los
assets deben existir antes de escribir el HTML."""
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
OUT = os.path.join(DIR, "perfume_del_dia_v5_ganymede.html")
SLUG = "ganymede"

ASSETS = [f"{SLUG}_fondo.png", f"{SLUG}_figura.png", "qr_fragrantica.png", "pack_ganymede_front.jpg"]
for a in ASSETS:
    p = os.path.join(DIR, a)
    assert os.path.isfile(p) and os.path.getsize(p) > 300, f"ASSET FALTA: {p}"
from PIL import Image as _I
assert _I.open(os.path.join(DIR, "qr_fragrantica.png")).size == (300, 300), "QR no es 300x300"
assert _I.open(os.path.join(DIR, f"{SLUG}_figura.png")).mode in ("RGBA", "LA"), "figura sin alfa"

html = open(TPL, encoding="utf-8").read()


def rep(old, new):
    global html
    n = html.count(old)
    assert n == 1, f"reemplazo no unico ({n}): {old[:70]!r}"
    html = html.replace(old, new)


# ---------- assets ----------
rep("url('acqua_di_sale_fondo.png')", f"url('{SLUG}_fondo.png')")
# zona segura 3:4 (skill): aire arriba 45 / abajo 50 -> pie dentro y >=45 px de aire
rep(".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:8px 52px 8px; }",
    ".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:45px 52px 50px; }")
rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    f'src="{SLUG}_figura.png" alt="Ganymede Marc-Antoine Barrois"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{SLUG}_figura.png" alt=""></div>')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">MARTES · 20 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Marc-Antoine Barrois</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>Ganymede</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">cuero mineral, mandarina y sal</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2019</b><span class="sep">·</span>EDP<span class="sep">·</span>Unisex<span class="sep">·</span>Amaderada especiada</div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Quentin Bisch</b></div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>200,00 €</b> / 100 ml'
    '<span class="f">Precio: web oficial marcantoinebarrois.com · consultado 20-10-2026 · Duración: BD</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,03</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="3%" stop-color="#c9971c"/><stop offset="3%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">13.156 votos · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: mandarina italiana y azafrán — cítrico con filo</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: osmanto chino, helicrisio salado y hoja de violeta</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: cuero, akigalawood, notas minerales, cedro, pachulí y almizcle</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica · oficial marcantoinebarrois.com</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'MANDARINA · AZAFRÁN' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'OSMANTO · HELICRISIO · VIOLETA' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CUERO · AKIGALAWOD · MINERAL · CEDRO' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“El aroma pasa de la mandarina a las notas especiadas y ligeramente saladas de la flor de helicrisio, '
    'para sublimar un cuero mineral casi metálico… Un océano de agua salada barrido por el viento, una estética mítica.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Casa Marc-Antoine Barrois · inspiración oficial [traducida] · lanzado 01-04-2019, nunca reformulado')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Bois Impérial</span><span class="alt-casa">Essential Parfums · 2020</span>'
    '<span class="alt-rt">longevidad 4,4/5 · 157 val.</span><span class="alt-motivo">el mismo akigalawood de Bisch, ~72 €/100 ml</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Encelade</span><span class="alt-casa">Marc-Antoine Barrois · 2022</span>'
    '<span class="alt-rt">3,75/5 · 3.493 votos</span><span class="alt-motivo">misma casa y nariz: ruibarbo y sándalo</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Terre d\'Hermès</span><span class="alt-casa">Hermès · 2006</span>'
    '<span class="alt-rt">4,28/5 · 29.388 votos</span><span class="alt-motivo">el mineral cítrico de referencia (5/10 · Fragrenza)</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Fragrantica · WhatScent · Fragrenza · consultado 20-10-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Ligeramente metálico, huele a «gris», relajante… ¿Huele a nada? Pero a algo. Como una habitación, o papel. '
    'Un consultorio tranquilo. Una pared. Algodón. Desconcertante… y profundamente reconfortante.”')
rep('— Reseña en Fragrantica · comunidad [ES]', '— ratoncita_julicita en Fragrantica · comunidad [traducida]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">8,1–16,0 °C sens · media 13,1 · 0 % lluvia<br>banda fresco · amplitud media 7,9 °C · ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3-4</b> mañana · <b>3</b> tarde<br><span class="caveat-pie">mineral, limpio, sin ruido</span></div>')

rep('fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab',
    'fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab')

# ---------- asertos finales ----------
# Sombra/halo medido (20-10-2026): con fondo claro el cuerpo del frasco daba 1,65:1;
# halo radial 0,55 + drop-shadow apilada lo suben a 2,65:1 (tapón 4,18:1, fondo L 132,3).
HALO = (".frasco-col::before{content:'';position:absolute;left:-36px;right:-36px;top:26px;bottom:52px;"
        "background:radial-gradient(ellipse at 50% 46%, rgba(24,16,8,0.55) 0%, rgba(24,16,8,0.34) 46%, transparent 75%);"
        "filter:blur(20px);z-index:0;}"
        ".frasco-figura{filter:drop-shadow(0 8px 14px rgba(30,17,2,0.78)) drop-shadow(0 22px 44px rgba(40,24,6,0.66)) "
        "drop-shadow(0 0 46px rgba(48,30,8,0.60)) drop-shadow(0 0 90px rgba(48,30,8,0.40));}")
assert "</style>" in html
html = html.replace("</style>", HALO + "\n</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{SLUG}_fondo.png')") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
