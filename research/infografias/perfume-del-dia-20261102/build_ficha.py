#!/usr/bin/env python3
"""Genera la ficha v5 del 02-11-2026 (By the Fireplace, Maison Margiela) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los assets deben
existir antes de escribir el HTML.
Datos: pirámide oficial maisonmargiela-fragrances.eu · Fragrantica 4,20/5 (27.977 votos) ·
Parfumo 7,9/10 (longevidad 7,7) · precio 153,00 €/100 ml Perfumería Julia (consultado 02-11-2026) ·
clima del instrumento ventana_perfume.py (ventana 08-18, consultado 02-11-2026 08:27).
Alternativas con rating/votos: Angels' Share, Ébène Fumé, Woody Chestnut.
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "bythefireplace"
FONDO = os.environ.get("FONDO", "bythefireplace_fondo_c.png")
SUF = os.environ.get("SUF", "a")
FIG = os.environ.get("FIGURA", f"{SLUG}_figura.png")
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
    f'src="{FIG}" alt="By the Fireplace Maison Margiela"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{FIG}" alt=""></div>')
rep('src="qr_fragrantica.png"', f'src="qr_fragrantica_{SLUG}.png"')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">LUNES · 02 NOVIEMBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Maison Margiela</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>By the Fireplace</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">la chimenea de invierno: leña, castaña y vainilla</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2015</b><span class="sep">·</span>Eau de Toilette<span class="sep">·</span>Unisex'
    '<span class="sep">·</span>Amaderada ambarada <span class="f">(oficial)</span></div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Marie Salamagne</b></div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~7-9 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span>'
    '<b>153,00 €</b> / 100 ml'
    '<span class="f">Precio: Perfumería Julia 153,00 € / 100 ml · consultado 02-11-2026 · '
    'Duración: Fragrantica / Parfumo 7,7 de 10</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,20</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="84%" stop-color="#c9971c"/><stop offset="84%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">27.977 votos · 3,1 mil reseñas · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: clavo y pimienta rosa — especiado, casi tostado</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: castaña asada sobre guayaco y el humo del cade</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: vainilla, bálsamo de Perú y cashmeran — la piel</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: maisonmargiela-fragrances.eu · pirámide oficial</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'CLAVO · PIMIENTA ROSA · AZAHAR' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'CASTAÑA · GUAYACO · CADE' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VAINILLA · BÁLSAMO DE PERÚ · CASHMERAN' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“La sensación envolvente de una chimenea en pleno invierno. La chimenea crepita, el fuego '
    'reconforta y todo huele a castañas asándose y a leña que arde: la seguridad de estar dentro '
    'mientras fuera hiela. Una fragancia amaderada y especiada que atrapa la memoria de la '
    'chimenea y la vuelve a encender sobre la piel.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Maison Margiela · descripción oficial [traducida]<br>'
    'El truco del perfil: la castaña y el guayaco dan el «tostado» y el cade pone el humo; '
    'la vainilla y el bálsamo lo vuelven habitable (acordes Fragrantica: amaderado, vainilla, balsámico, especiado cálido)')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Angels\' Share</span><span class="alt-casa">By Kilian · 2020</span>'
    '<span class="alt-rt">4,32/5 · 30.999 votos</span><span class="alt-motivo">el mismo gesto cálido —coñac, '
    'canela, tonka— sin humo: más gourmand y más dulce</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Ébène Fumé</span><span class="alt-casa">Tom Ford · 2021</span>'
    '<span class="alt-rt">4,10/5 · 3.643 votos</span><span class="alt-motivo">humo de palo santo y cuero: '
    'más seco y más ahumado, menos dulce</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Woody Chestnut</span><span class="alt-casa">Dossier · 2021</span>'
    '<span class="alt-rt">4,51/5 · 102 votos</span><span class="alt-motivo">el clon declarado, pirámide '
    'idéntica: más clavo, menos humo, 50 ml</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Fragrantica («reminds me of») · Parfumo («similar») · dossier.co (clon declarado) · consultado 02-11-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Con dos pulverizaciones tienes la experiencia que busca: cálida, acogedora, nostálgica, como la '
    'primera nevada tras la lluvia. Si te pasas, entra en terreno negativo: neumático quemado, cenicero. '
    'Es un perfume que premia la contención.”')
rep('— Reseña en Fragrantica · comunidad [ES]',
    '— Reseña de la comunidad en Fragrantica [traducida]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">10,8–15,0 °C sens · media 13,0 · 0 % lluvia<br>banda fresco · amplitud 4,9 °C '
    '· ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>2-3</b> interior · <b>3</b> exterior<br>'
    '<span class="donde">cuello y pecho · día de trabajo · no en cerrado</span><br>'
    '<span class="caveat-pie">el humo se dobla con cada spray</span></div>')

# ---------- sombra del frasco ----------
SOMBRA = (".frasco-figura{filter:drop-shadow(0 8px 14px rgba(30,17,2,0.70)) drop-shadow(0 22px 44px rgba(58,35,6,0.55)) "
          "drop-shadow(0 0 60px rgba(70,44,10,0.35));}")
html = html.replace("</style>", SOMBRA + "\n</style>", 1)

# ---------- pase de intensidad de texto (norma 30-oct-2026, receta _corr) ----------
if os.environ.get("INTENSIDAD") == "1":
    for old, new in [("#12789e", "#0a5d7a"), ("#0e7c7b", "#0a5f5e"),
                     ("#c96f1c", "#8f4409"), ("#5b42e6", "#3a2aa8")]:
        assert html.count(old) >= 1, f"hex de titulo no encontrado: {old}"
        html = html.replace(old, new)
    INTENS = """
/* intensidad de texto — receta _corr 30-oct-2026 (solo capa de texto) */
.dh, .dh b { color:#0a1d27 !important; }
.dh .sep { color:#4e6875 !important; }
.dh .f { color:#445d69 !important; }
.fecha-sep, .r-meta, .alt-casa, .sprays { color:#1f323c !important; }
.alt-motivo { color:#22353f !important; }
.alt-rt { color:#7a3d05 !important; }
.fuente-line { color:#2f434c !important; }
.nota-fondo { color:#3d4d55 !important; }
.sub, .caveat-pie, .sello b { color:#8c2e14 !important; }
.inspiracion p { color:#08171f !important; }
.cita blockquote { color:#171f57 !important; }
.cita .fuente-line { color:#33249a !important; }
.r-num { color:#8f6608 !important; }
.dh, .dh b, .fecha-sep, .r-meta, .alt-casa, .alt-motivo, .alt-rt, .fuente-line, .sprays,
.sub, .caveat-pie, .inspiracion p, .cita blockquote, .nota-fondo, .donde, .clima, .f
  { text-shadow: 0 1px 1px rgba(255,255,255,.55); }
.sec-title { text-shadow: 0 1px 2px rgba(255,255,255,.50); }
"""
    html = html.replace("</style>", INTENS + "</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{FONDO}'") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
