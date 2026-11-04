#!/usr/bin/env python3
"""Genera la ficha v5 del 25-10-2026 (Bois Impérial, Essential Parfums) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los assets deben
existir antes de escribir el HTML.
Datos: essentialparfums.com (notas, %, precio, inspiración) · Fragrantica 4,16/5 (17.084) ·
Parfumo (scent 8,1 · long 8,5 sobre 4.428 · sillage 8,1) · alternativas: Benegas/Druni/makeup.es.
Consultado 25-10-2026.
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "bois_imperial"
FONDO = os.environ.get("FONDO", "bois_imperial_fondo.png")
SUF = os.environ.get("SUF", "a")
FIG = os.environ.get("FIGURA", f"figura_{SLUG}.png")
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


# ---------- assets ----------
rep("url('acqua_di_sale_fondo.png')", f"url('{FONDO}')")
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
    f'src="{FIG}" alt="Bois Impérial Essential Parfums"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{FIG}" alt=""></div>')
rep('src="qr_fragrantica.png"', f'src="qr_fragrantica_{SLUG}.png"')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">DOMINGO · 25 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Essential Parfums</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>Bois Impérial</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">albahaca recién rota y pimienta de Timut</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2020</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex'
    '<span class="sep">·</span>Amaderada aromática <span class="f">(16 % · 93 % natural)</span></div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Quentin Bisch</b></div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span>'
    '<b>94,00 €</b> / 100 ml'
    '<span class="f">Precio: essentialparfums.com 94,00 € / 100 ml (recargable) · consultado 25-10-2026 · '
    'Duración: Parfumo 8,5/10 sobre 4.428 votos · estela 8,1/10</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,16</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="83%" stop-color="#c9971c"/><stop offset="83%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">17.084 votos · 1,5K reseñas · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: albahaca tailandesa y pimienta de Timut — verde y picante</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: akigalawood — madera de pachulí upcycled, seca y especiada</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: vetiver de Haití, pachulí, Ambrofix y Georgywood</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: oficial essentialparfums.com · Parfumo</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'ALBAHACA · TIMUT · POMELO' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'AKIGALAWOOD · PETALIA' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VETIVER · PACHULÍ · AMBROFIX' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“Las hojas de albahaca tailandesa, recién machacadas y picantes, se encuentran con el pomelo y la pimienta '
    'chispeante del absoluto de Timut de Nepal. Un vetiver de Haití verde, rico y terroso dialoga con Georgywood, '
    'molécula exclusiva de tonos de cedro; la floralidad de Petalia lo ilumina. Y el majestuoso Akigalawood firma '
    'la fragancia: un ingrediente natural exclusivo, upcycled del pachulí por biotecnología.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Casa Essential Parfums · descripción oficial [traducida] · EDP al 16 %, 93 % de origen natural<br>'
    'Compuesta por Quentin Bisch; frasco recargable (refill 100 ml)')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Encelade</span><span class="alt-casa">Marc-Antoine Barrois · 2022</span>'
    '<span class="alt-rt">7,4/10 · long 8,9</span><span class="alt-motivo">mismo perfumista: ruibarbo, vetiver y '
    'cuero ahumado — más oscuro y más serio · 120 €/30 ml (Benegas)</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Grey Vetiver</span><span class="alt-casa">Tom Ford · 2009</span>'
    '<span class="alt-rt">7,9/10 · long 7,5</span><span class="alt-motivo">vetiver limpio, cítrico y seco, sin la '
    'albahaca: el mismo oficio en clave de oficina · desde 95,95 €/100 ml (Druni)</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Lunar Vetiver</span><span class="alt-casa">Amouroud · 2018</span>'
    '<span class="alt-rt">8,3/10 · long 8,6</span><span class="alt-motivo">vetiver de Java con pimienta rosa y flor '
    'de tabaco: más redondo y más caro · 146 €/100 ml (makeup.es)</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Parfumo («smells similar») · Fragrantica · precios consultados 25-10-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Una obra maestra de la contención: es amaderada, ligera, aireada y picante al mismo tiempo. Arranca '
    'pimiento y algo cítrico, y acaba en una madera de akigalawood que no pierde la luz. A mí me dura unas '
    '12 horas con una estela sana de principio a fin.”')
rep('— Reseña en Fragrantica · comunidad [ES]',
    '— Reseña en Fragrantica (4,16/5 · 17.084 votos) · comunidad [traducida del inglés]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">12,1–19,7 °C sens · media 17,6 · 33 % lluvia<br>banda templado · amplitud 10,5 °C '
    '· ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3</b> por la mañana<br>'
    '<span class="caveat-pie">a las 8 h, 1 toque en la ropa si hace falta</span></div>')

# ---------- sombra del frasco ----------
SOMBRA = (".frasco-figura{filter:drop-shadow(0 8px 14px rgba(30,17,2,0.70)) drop-shadow(0 22px 44px rgba(58,35,6,0.55)) "
          "drop-shadow(0 0 60px rgba(70,44,10,0.35));}")
html = html.replace("</style>", SOMBRA + "\n</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{FONDO}'") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
