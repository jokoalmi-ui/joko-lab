#!/usr/bin/env python3
"""Genera la ficha v5 del 22-10-2026 (Memo Paris Winter Palace) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los
assets deben existir antes de escribir el HTML. FONDO por env: winter_palace_fondo_a.png|b.
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "winter_palace"
FONDO = os.environ.get("FONDO", "winter_palace_fondo_a.png")
SUF = os.environ.get("SUF", "a")
OUT = os.path.join(DIR, f"perfume_del_dia_v5_{SLUG}_{SUF}.html")

ASSETS = [FONDO, f"{SLUG}_figura.png", "qr_fragrantica.png", "pack_winter_palace.jpg"]
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
# zona segura 3:4 (skill): aire arriba 45 / abajo 50
rep(".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:8px 52px 8px; }",
    ".content { position:relative; z-index:2; height:1440px; display:flex; flex-direction:column; padding:40px 52px 50px; }")

# ---------- compactación vertical (E1/E2: 1462-><=1390) ----------
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
    f'src="{SLUG}_figura.png" alt="Winter Palace Memo Paris"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="{SLUG}_figura.png" alt=""></div>')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">JUEVES · 22 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Memo Paris</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>Winter Palace</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">el dragón que despierta sobre una taza de té rojo</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2019</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex'
    '<span class="sep">·</span>Aromática verde <span class="f">(familia en BD: cuero)</span></div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Alienor Massenet</b></div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span>'
    '<b>340,00 €</b> / 100 ml'
    '<span class="f">Precio: memoparis.com 255,00 € / 75 ml · consultado 22-10-2026 · '
    'Duración: 7-8 h en reseñas Fragrantica y Parfumo</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,10</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="7%" stop-color="#c9971c"/><stop offset="7%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">3.395 votos · 283 reseñas · Fragrantica</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: limón, bergamota y clavo — cítrico con filo especiado</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: té rojo, mate y azahar — el dragón respirando té</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: vainilla, benjuí y ládano — resinas cálidas al final</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: oficial memoparis.com · Fragrantica</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'LIMÓN · BERGAMOTA · CLAVO' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'TÉ ROJO · MATE · AZAHAR' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VAINILLA · BENJUÍ · LÁDANO' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“El despertar del dragón, imperial. Ojos que chispean fuego helado. Aceite de naranja. Se alza sobre mi taza '
    'de té rojo y su aliento arremolina el sabor de la bergamota. De pronto el calor crece y la atmósfera pasa del '
    'cítrico a la madera intensa. Alza el vuelo, se desvanece del palacio en un destello de polvo y, a lo lejos, '
    'ondula al compás de la Gran Muralla: el dragón baila de alegría, ebrio de libertad. Siembra una primavera '
    'eterna —té mate, pomelo— y deja tras de sí un rastro de ámbar y vainilla apasionados.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Casa Memo Paris · inspiración oficial [traducida] · colección Graines Vagabondes')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">XJ 1861 Renaissance</span><span class="alt-casa">Xerjoff · 2011</span>'
    '<span class="alt-rt">4,30/5 · 5.534 votos</span><span class="alt-motivo">el cítrico verde al que más se le compara '
    'en Fragrantica; 6-7 h</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Remember Me</span><span class="alt-casa">Jovoy Paris · 2018</span>'
    '<span class="alt-rt">4,17/5 · 3.128 votos</span><span class="alt-motivo">té con leche y cardamomo: mismo eje de '
    'té, más gourmand</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Inlé</span><span class="alt-casa">Memo Paris · 2021</span>'
    '<span class="alt-rt">misma casa · mismo eje de té</span><span class="alt-motivo">té con osmanto y mate, más '
    'floral y luminoso</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Fragrantica (“reminds me of”) · Parfumo · consultado 22-10-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Al principio pensé: ¿tanto dinero por un aroma que huele fuerte a naranja y luego se vuelve dulce? Me '
    'equivocaba. Arranca con una explosión de cítricos y una nota de té muy especial, finísima; después entran '
    'ámbar y vainilla sin volverse empalagoso. La longevidad es bastante buena —7-8 h—, no es estridente, pero la '
    'estela permanece mucho rato.”')
rep('— Reseña en Fragrantica · comunidad [ES]',
    '— Osisi100 en Parfumo (9,5 de aroma) · comunidad [traducida]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">7,7–18,3 °C sens · media 13,7 · 0 % lluvia<br>banda fresco · amplitud amplia 10,8 °C '
    '· ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3-4</b> mañana (9,9 °C) · <b>3</b> tarde (16,8 °C)<br>'
    '<span class="caveat-pie">té rojo y clavo: mejor sin exceso</span></div>')

rep('fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab',
    'fondo: arte generado con ComfyUI · FLUX.2 [klein] local · hecha con el lab')

# ---------- halos (frasco) ----------
HALO_MODE = os.environ.get("HALO", "fuerte")
if HALO_MODE == "none":
    HALO = ""
elif HALO_MODE == "claro":
    HALO = (".frasco-col::before{content:'';position:absolute;left:-58px;right:-58px;top:-18px;bottom:96px;"
            "background:radial-gradient(ellipse at 50% 42%, rgba(246,238,222,0.62) 0%, rgba(240,228,206,0.40) 52%,"
            " rgba(236,222,198,0.10) 78%, transparent 88%);"
            "filter:blur(26px);z-index:0;}"
            ".frasco-figura{filter:drop-shadow(0 10px 18px rgba(30,20,8,0.42)) drop-shadow(0 26px 50px rgba(38,24,10,0.30));}")
else:
    HALO = (".frasco-col::before{content:'';position:absolute;left:-36px;right:-36px;top:26px;bottom:52px;"
            "background:radial-gradient(ellipse at 50% 46%, rgba(18,12,6,0.50) 0%, rgba(18,12,6,0.30) 46%, transparent 75%);"
            "filter:blur(20px);z-index:0;}"
            ".frasco-figura{filter:drop-shadow(0 8px 14px rgba(24,14,2,0.75)) drop-shadow(0 22px 44px rgba(34,20,6,0.62)) "
            "drop-shadow(0 0 46px rgba(42,26,8,0.55)) drop-shadow(0 0 90px rgba(42,26,8,0.36));}")
assert "</style>" in html
if HALO:
    html = html.replace("</style>", HALO + "\n</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{FONDO}')") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
