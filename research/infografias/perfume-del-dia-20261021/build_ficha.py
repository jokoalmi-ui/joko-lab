#!/usr/bin/env python3
"""Genera la ficha v5 del 21-10-2026 (Nishane B-612) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los
assets deben existir antes de escribir el HTML. FONDO por env: b612_fondo_a.png|b.
"""
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "b612"
FONDO = os.environ.get("FONDO", "b612_fondo_a.png")
SUF = os.environ.get("SUF", "a")
OUT = os.path.join(DIR, f"perfume_del_dia_v5_b612_{SUF}.html")

ASSETS = [FONDO, f"{SLUG}_figura.png", "qr_fragrantica.png", "pack_b612.png"]
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
rep("url('acqua_di_sale_fondo.png')", f"url('{FONDO}')")
# zona segura 3:4 (skill): aire arriba 45 / abajo 50 -> pie dentro y >=45 px de aire
rep(".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:8px 52px 8px; }",
    ".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:45px 52px 50px; }")
rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    f'src="{SLUG}_figura.png" alt="B-612 Nishane"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{SLUG}_figura.png" alt=""></div>')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">MIÉRCOLES · 21 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Nishane</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>B-612</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">el asteroide del Principito, en clave de fougère</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2018</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Aromática amaderada (fougère)</div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Chris Maurice</b> (Christian Carbonnel)</div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~9 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>450,00 €</b> / 100 ml'
    '<span class="f">Precio: nishane.com (225 €/50 ml) · consultado 21-10-2026 · Duración: Parfumo 9,1/10</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,07</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="7%" stop-color="#c9971c"/><stop offset="7%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">1.495 votos · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: lavanda, geranio y ciprés — aire frío y limpio</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: cashmeran, cedro, sándalo y pachulí — madera seca</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: almizcle, musgo de roble y haba tonka — el abrazo clásico</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: oficial nishane.com · Fragrantica</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'LAVANDA · GERANIO · CIPRÉS' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'CASHMERAN · CEDRO · SÁNDALO' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'ALMIZCLE · MUSGO · TONKA' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“El asteroide del Principito se acerca al mundo con sus aromas para hacer imaginativo a quien lo lleva, '
    'de mente abierta y sensible al misterio y la belleza del mundo, con una estructura seductora que devuelve '
    'los rasgos olvidados de la infancia. Ilustración a través de la exploración.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Casa Nishane · inspiración oficial [traducida] · Colección Imaginative')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Fougère d\'Argent</span><span class="alt-casa">Tom Ford · 2018</span>'
    '<span class="alt-rt">4,28/5 · 1.273 votos</span><span class="alt-motivo">la referencia del fougère especiado · 56 % similitud (47/63, Parfumo)</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Bracken Man</span><span class="alt-casa">Amouage · 2016</span>'
    '<span class="alt-rt">4,18/5 · 1.571 votos</span><span class="alt-motivo">más verde y terroso, con clavo; descatalogado</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Beau de Jour</span><span class="alt-casa">Tom Ford · 2020</span>'
    '<span class="alt-rt">4,30/5 · 4.699 votos</span><span class="alt-motivo">barbershop clásico: más lavanda y musgo, menos madera</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Parfumo · Fragrantica · WhatScent · consultado 21-10-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Recuerda de inmediato a Fougère d\'Argent, pero más suave y cremoso, menos agresivamente especiado; '
    'probablemente dure más pero hable más bajo.”')
rep('— Reseña en Fragrantica · comunidad [ES]', '— TheDunkPapa en Parfumo · comunidad [traducida]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">11,3–14,9 °C sens · media 12,6 · 8 % lluvia<br>banda fresco · amplitud estrecha 4,3 °C · ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3-4</b> mañana · <b>3</b> tarde<br><span class="caveat-pie">fougère limpio, de oficina</span></div>')

rep('fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab',
    'fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab')

# ---------- asertos finales ----------
# Frasco de vidrio claro + tapón dorado: el enemigo es el fondo claro. Halo medido.
HALO = (".frasco-col::before{content:'';position:absolute;left:-36px;right:-36px;top:26px;bottom:52px;"
        "background:radial-gradient(ellipse at 50% 46%, rgba(18,12,6,0.50) 0%, rgba(18,12,6,0.30) 46%, transparent 75%);"
        "filter:blur(20px);z-index:0;}"
        ".frasco-figura{filter:drop-shadow(0 8px 14px rgba(24,14,2,0.75)) drop-shadow(0 22px 44px rgba(34,20,6,0.62)) "
        "drop-shadow(0 0 46px rgba(42,26,8,0.55)) drop-shadow(0 0 90px rgba(42,26,8,0.36));}")
assert "</style>" in html
html = html.replace("</style>", HALO + "\n</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{FONDO}')") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
