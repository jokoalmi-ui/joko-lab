#!/usr/bin/env python3
"""Genera la ficha v5 del 24-10-2026 (Xerjoff Alexandria II Parfum) desde la plantilla oficial.
Sustituciones fail-closed: cada reemplazo debe ocurrir EXACTAMENTE 1 vez y los
assets deben existir antes de escribir el HTML. FONDO por env: alexandria2_fondo_a.png|b.
Datos: xerjoff.com (notas, precio, inspiración), Parfumo (2012, perfumista, ratings),
MFK/TF/PdM oficiales para el precio en España de las alternativas. Consultado 24-10-2026.
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html")
SLUG = "alexandria2"
FONDO = os.environ.get("FONDO", "alexandria2_fondo_b.png")
SUF = os.environ.get("SUF", "b")
OUT = os.path.join(DIR, f"perfume_del_dia_v5_{SLUG}_{SUF}.html")

ASSETS = [FONDO, f"figura_{SLUG}.png", f"qr_fragrantica_{SLUG}.png"]
for a in ASSETS:
    p = os.path.join(DIR, a)
    assert os.path.isfile(p) and os.path.getsize(p) > 300, f"ASSET FALTA: {p}"
from PIL import Image as _I
_qr = _I.open(os.path.join(DIR, f"qr_fragrantica_{SLUG}.png"))
assert min(_qr.size) >= 300 and _qr.size[0] == _qr.size[1], f"QR no cuadrado >=300: {_qr.size}"
assert _I.open(os.path.join(DIR, f"figura_{SLUG}.png")).mode in ("RGBA", "LA"), "figura sin alfa"
assert _I.open(os.path.join(DIR, FONDO)).size == (1024, 1024), "fondo no es 1024"

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

# ---------- compactación vertical (E1/E2: <=1390) ----------
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
    f'src="figura_{SLUG}.png" alt="Alexandria II Xerjoff"')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    f'<div class="reflejo"><img src="figura_{SLUG}.png" alt=""></div>')

# ---------- cabecera ----------
rep('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
    '<div class="fecha-sep">SÁBADO · 24 OCTUBRE 2026</div>')
rep('<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>',
    '<div class="sello"><div>Elei&shy;cción<br>del Lab</div><b>2026</b></div>')

# ---------- hero ----------
rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Xerjoff</div>')
rep('<h1>Acqua di Sale</h1>', '<h1>Alexandria II</h1>')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">la ciudad antigua en ámbar y oud</div>')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2012</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex'
    '<span class="sep">·</span>Oriental amaderado <span class="f">(colección Oud Stars)</span></div>')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumista: <b>Christian Carbonnel</b> (Chris Maurice)</div>')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~8-9 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span>'
    '<b>545,00 €</b> / 100 ml'
    '<span class="f">Precio: xerjoff.com 545,00 € / 100 ml (50 ml 325,00 €) · consultado 24-10-2026 · '
    'Duración: Parfumo 9,1/10 sobre 6.934 votos</span></div>')

rep('<span class="r-num">4,15</span>', '<span class="r-num">4,30</span>')
rep('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
    '<stop offset="86%" stop-color="#c9971c"/><stop offset="86%" stop-color="#d8d4c8"/>')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">8,6/10 · 7.233 votos · Parfumo</span>')

# ---------- pirámide: leyenda ----------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: manzana y canela sobre lavanda — apertura rara y luminosa</span>')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: rosa búlgara y cedro — el puente floral del oud</span>')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: oud laosiano, ámbar, sándalo y vainilla — horas en la piel</span>')
rep('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
    '<span class="fuente-line" style="margin-top:4px;">Notas: oficial xerjoff.com · Parfumo</span>')

# ---------- pirámide: capas SVG ----------
rep("{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },",
    "{ w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'MANZANA · CANELA · LAVANDA' },")
rep("{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },",
    "{ w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'CEDRO · LIRIO · ROSA BÚLGARA' },")
rep("{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }",
    "{ w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'OUD LAOSIANO · ÁMBAR · SÁNDALO · VAINILLA' }")

# ---------- inspiración ----------
rep('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
    '“Inspirada en el antiguo arte árabe de la perfumería, Alexandria II captura la esencia de la ciudad que '
    'durante siglos fue cruce de culturas, historia y comercio. Como Alejandría —un mosaico vibrante de tradición '
    'e innovación—, esta fragancia une elegancia atemporal con un espíritu fresco y vivo.”')
rep('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
    '— Casa Xerjoff · inspiración oficial [traducida] · colección Oud Stars<br>'
    'Alexandria y Alexandria II solo se diferencian en la edad del oud: 25 años frente a 5 (Sergio Momo, fundador)')

# ---------- alternativas ----------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Oud Satin Mood</span><span class="alt-casa">MFK · 2015</span>'
    '<span class="alt-rt">8,2/10 · long 9,1</span><span class="alt-motivo">rosa búlgara + oud laosiano + '
    'vainilla: casi la misma arquitectura · 255 €/70 ml</span></div>')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Oud Wood</span><span class="alt-casa">Tom Ford · 2007</span>'
    '<span class="alt-rt">8,4/10 · long 7,1</span><span class="alt-motivo">oud domesticado con sándalo y '
    'ámbar: más seco y llevadero</span></div>')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Layton</span><span class="alt-casa">Parfums de Marly · 2016</span>'
    '<span class="alt-rt">8,6/10 · long 8,2</span><span class="alt-motivo">manzana, lavanda y vainilla: la '
    'apertura de Alexandria II sin el oud · 290 €/125 ml</span></div>')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Parfumo («smells similar») · Fragrantica · consultado 24-10-2026')

# ---------- cita comunidad ----------
rep('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
    '“Femenina, envolvente como una noche perezosa, sexy hasta el mareo, una poción fuerte. Dulce y '
    'desconcertante para quien pasa por al lado. Te hace volver y preguntar: ¿QUÉ ES ESTO? Un maravilloso '
    'antidepresivo.”')
rep('— Reseña en Fragrantica · comunidad [ES]',
    '— Appie en Parfumo (10 de aroma) · comunidad [traducida del alemán]')

# ---------- pie ----------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">10,9–15,9 °C sens · media 14,0 · 0 % lluvia<br>banda fresco · amplitud 6,0 °C '
    '· ventana 08-18</div>')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>2</b> tarde · <b>3</b> si refresca<br>'
    '<span class="caveat-pie">proyecta mucho: mejor quedarse corto</span></div>')

# ---------- sombra del frasco (vidrio ámbar oscuro: cuerpo L 92,7 sobre fondo claro) ----------
SOMBRA = (".frasco-figura{filter:drop-shadow(0 8px 14px rgba(30,17,2,0.72)) drop-shadow(0 22px 44px rgba(58,35,6,0.58)) "
          "drop-shadow(0 0 60px rgba(70,44,10,0.40));}")
html = html.replace("</style>", SOMBRA + "\n</style>", 1)

assert "acqua_di_sale" not in html and "Profumum" not in html and "1996" not in html, "resto de la plantilla"
assert html.count(f"url('{FONDO}')") == 1

open(OUT, "w", encoding="utf-8").write(html)
print("OK ->", OUT, len(html), "bytes")
