#!/usr/bin/env python3
"""Genera la ficha v5 del 28-10-2026 (195 a.C., Agatho Parfum) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los assets deben
existir antes de escribir el HTML.
Datos verificados (consultado 28-10-2026):
 - Pirámide oficial agathoparfum.com/en/pompei-collection/195-ac.html (TOP: bergamota, hoja de
   higuera, limón, menta, granada · HEART: cardamomo, higo, jazmín · BASE: té negro, cachemira,
   cedro, incienso, cuero, oud, pachulí, estirax).
 - Fragrantica: 4,18/5 con 381 votos, 47 reseñas · perfumista Maurizio Cerizza · 2019.
 - Precio oficial: 320,00 EUR / 100 ml (agathoparfum.com, consultado 28-10-2026).
 - Alternativas con números: Ichnusa 4,27/5 (919) Fragrantica · Adam & Eve's Dress 4,17/5 (787)
   Fragrantica + Parfumo 7,5 · Wanderlust (2018) Parfumo 7,4/10 (83), long 7,8 (75), sillage 7,2 (74).
 - Clima: tools/ventana_perfume.py --ventana 08-18 (28-10): min 14,3 media 15,5 max 16,0 ·
   amplitud 6,7 · lluvia max 8% · banda templado · dosis 3 sprays.
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "195ac"
FONDO = os.environ.get("FONDO", "agatho_195ac_fondo_c.png")
SUF = os.environ.get("SUF", "a")
FIG = os.environ.get("FIGURA", "agatho_195ac_figura.png")
OUT = os.path.join(DIR, f"perfume_del_dia_v5_{SLUG}_{SUF}.html")

ASSETS = [FONDO, FIG, f"qr_fragrantica_{SLUG}.png"]
for a in ASSETS:
    p = os.path.join(DIR, a)
    assert os.path.isfile(p) and os.path.getsize(p) > 300, f"ASSET FALTA: {p}"
from PIL import Image as _I
_qr = _I.open(os.path.join(DIR, f"qr_fragrantica_{SLUG}.png"))
assert min(_qr.size) >= 300 and _qr.size[0] == _qr.size[1], f"QR no cuadrado >=300: {_qr.size}"
assert _I.open(os.path.join(DIR, FIG)).mode in ("RGBA", "LA"), "figura sin alfa"
assert _I.open(os.path.join(DIR, FONDO)).size == (1024, 1024), "fondo no es 1024"

html = open(TPL, encoding="utf-8").read()


def rep(old, new):
    global html
    n = html.count(old)
    assert n == 1, f"reemplazo no unico ({n}): {old[:70]!r}"
    html = html.replace(old, new)


rep('PLANTILLA FICHA DEL DÍA v5 — validada 02-sep-2026 (Acqua di Sale, C4)',
    'FICHA DEL DÍA v5 — 28-oct-2026 (195 a.C., Agatho Parfum) · desde plantilla v5')

# ---------- assets ----------
# viñeta oscura SOLO detrás del frasco: el cuerpo medido del packshot es L 199 y el fondo
# claro L 195-210 -> sin ella el frasco no contrasta (medido antes de escribir).
rep("background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "background:radial-gradient(ellipse 330px 560px at 205px 330px, rgba(9,14,8,0.88) 0%, "
    "rgba(9,14,8,0.60) 45%, rgba(9,14,8,0.26) 70%, rgba(9,14,8,0) 100%), "
    f"url('{FONDO}') center/cover no-repeat;")
rep(".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:8px 52px 8px; }",
    ".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:40px 52px 50px; }")

# ---------- compactación vertical ----------
for old, new in [
    ("h1 { font-family:'Playfair Display',serif; font-weight:800; font-size:72px;",
     "h1 { font-family:'Playfair Display',serif; font-weight:800; font-size:64px;"),
    (".sub { font-family:'Caveat',cursive; font-size:28px; color:#b2452a; margin-bottom:10px; }",
     ".sub { font-family:'Caveat',cursive; font-size:25px; color:#b2452a; margin-bottom:6px; }"),
    (".hero { display:flex; align-items:center; gap:44px; margin:2px 0 6px; }",
     ".hero { display:flex; align-items:center; gap:44px; margin:2px 0 2px; }"),
    (".sec { margin-top:3px; }", ".sec { margin-top:0px; }"),
    (".sec-head { display:flex; align-items:center; gap:12px; margin-bottom:5px; }",
     ".sec-head { display:flex; align-items:center; gap:12px; margin-bottom:2px; }"),
    (".alt-item { display:flex; align-items:baseline; gap:14px; padding:5px 2px; }",
     ".alt-item { display:flex; align-items:baseline; gap:14px; padding:3px 2px; }"),
    (".cita blockquote { font-family:'Playfair Display',serif; font-style:italic; font-size:19px;",
     ".cita blockquote { font-family:'Playfair Display',serif; font-style:italic; font-size:17.5px;"),
    (".inspiracion p { font-family:'Playfair Display',serif; font-style:italic; font-size:18px;",
     ".inspiracion p { font-family:'Playfair Display',serif; font-style:italic; font-size:17px;"),
    (".pir3d-svg { width:470px; height:220px;", ".pir3d-svg { width:470px; height:200px;"),
]:
    rep(old, new)
rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    f'src="{FIG}" alt="195 a.C. Agatho Parfum"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{FIG}" alt=""></div>')
rep('src="qr_fragrantica.png"', f'src="qr_fragrantica_{SLUG}.png"')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">MIÉRCOLES · 28 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Agatho Parfum</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>195 a.C.</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">higuera, té negro e incienso — la libertad recuperada</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2019</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex'
    '<span class="sep">·</span>Amaderada <span class="f">(verde frutal, ahumada)</span></div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Maurizio Cerizza</b></div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~9-11 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span>'
    '<b>320,00 €</b> / 100 ml'
    '<span class="f">Precio: agathoparfum.com 320,00 € / 100 ml · consultado 28-10-2026 · '
    'Duración: reseñas Fragrantica (~11 h) · BD 9 h</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,18</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="83.6%" stop-color="#c9971c"/><stop offset="83.6%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">381 votos · 47 reseñas · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: bergamota, menta y granada sobre hoja de higuera</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: higo maduro, cardamomo y jazmín</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: té negro, incienso, cedro y cuero — horas en la piel</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: agathoparfum.com (pirámide oficial) · consultado 28-10-2026</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'BERGAMOTA · MENTA · HIGUERA' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'HIGO · CARDAMOMO · JAZMÍN' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'TÉ NEGRO · INCIENSO · CUERO' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“En el año 195 a.C. se derogó la Lex Oppia, la ley que pretendía frenar el lujo y la riqueza. '
    'De ese momento nace esta fragancia: una memoria tangible de una libertad recuperada.”')
rep('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
    '<span class="fuente-line">— Casa Agatho Parfum · descripción oficial [traducida del inglés] · '
    'consultado 28-10-2026</span>')
rep('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
    '<span class="fuente-line" style="margin-left:44px;">Asociaciones: Fragrantica («reminds me of») · '
    'Parfumo («similar fragrances») · consultado 28-10-2026</span>')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Ichnusa</span><span class="alt-casa">Profumum Roma · 2001</span>'
    '<span class="alt-rt">4,27/5 · 919 votos</span><span class="alt-motivo">la hoja de higuera fotográfica '
    'con mirto y hierba: más verde y herbal, sin té ni incienso</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Adam &amp; Eve\'s Dress</span><span class="alt-casa">Lorenzo Pazzaglia · 2020</span>'
    '<span class="alt-rt">4,17/5 · 787 votos</span><span class="alt-motivo">el higo lácteo y soleado: '
    'más dulce y cremoso, menos amaderado</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Wanderlust</span><span class="alt-casa">Omanluxury · 2018</span>'
    '<span class="alt-rt">7,4/10 · 83 votos</span><span class="alt-motivo">verde especiada con incienso '
    'y cedro: más seca y amaderada (descatalogada)</span></div>')
# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“El higo, en todos sus matices, es una de mis notas favoritas… aquí emerge toda su potencia '
    'verde y balsámica. Con las horas es la madera la que se vuelve protagonista: un árbol de higo '
    'a principios de verano, cuando la fruta aún no está madura.”')
rep('— Reseña en Fragrantica · comunidad [ES]',
    '— Rosa Chiara en Fragrantica (23-06-2025) · comunidad [traducida del italiano]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">14,3–16,0 °C sens · media 15,5 · 8 % lluvia<br>banda templado · amplitud 6,7 °C '
    '· ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3</b> por la mañana · 2 si repites<br>'
    '<span class="donde">cuello y pecho · día templado · dosificar</span><br>'
    '<span class="caveat-pie">un higo verde que aguanta la jornada</span></div>')

# ---------- sombra del frasco ----------
SOMBRA = (".frasco-figura{filter:drop-shadow(0 8px 14px rgba(30,17,2,0.70)) drop-shadow(0 22px 44px rgba(58,35,6,0.55)) "
          "drop-shadow(0 0 60px rgba(70,44,10,0.35));}")
html = html.replace("</style>", SOMBRA + "\n</style>", 1)

assert "Acqua di Sale" not in html and "1996" not in html, "resto de la plantilla"
assert html.count("Profumum Roma") == 1, "Profumum Roma solo debe quedar en la alternativa Ichnusa"
assert html.count(f"url('{FONDO}'") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
