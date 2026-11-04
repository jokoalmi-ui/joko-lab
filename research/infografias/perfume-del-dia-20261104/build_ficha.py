#!/usr/bin/env python3
"""build_ficha.py - ficha v5 04-11-2026 · Houbigant Tabac Nomade.
Sustituciones fail-closed sobre plantilla-ficha-v5.html (skill perfume-del-dia).
No toca fichas anteriores (regla de no-retrofit)."""
import os, re, sys

D = '/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20261104'
TPL = '/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html'
OUT = os.path.join(D, 'ficha_tabac_nomade.html')

t = open(TPL, encoding='utf-8').read()
print('template chars:', len(t))

def rep(old, new, why):
    global t
    c = t.count(old)
    if c != 1:
        sys.exit(f'FAIL-CLOSED [{why}]: {c} coincidencias de {old[:60]!r}')
    t = t.replace(old, new, 1)
    print(f'  ok {why}')

# ---------------- cabecera ----------------
rep('MIÉRCOLES · 02 SEPTIEMBRE 2026', 'MIÉRCOLES · 04 NOVIEMBRE 2026', 'fecha-sep')

# ---------------- CSS: fondo del dia ----------------
rep("url('acqua_di_sale_fondo.png')", "url('tabac_fondo_b.png')", 'css fondo')

# ---------------- hero ----------------
rep('src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma"',
    'src="tabac_figura.png" alt="Tabac Nomade Houbigant Paris"', 'img figura')
rep('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
    '<div class="reflejo"><img src="tabac_figura.png" alt=""></div>', 'reflejo')

rep('<div class="casa">Profumum Roma</div>', '<div class="casa">Houbigant Paris</div>', 'casa')
rep('<h1>Acqua di Sale</h1>', '<h1>Tabac Nomade</h1>', 'h1')
rep('<div class="sub">el mar embotellado de Cerdeña</div>',
    '<div class="sub">tabaco, cuero y desierto al atardecer</div>', 'sub')

rep('<div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>',
    '<div class="dh"><b>2023</b><span class="sep">·</span>Eau de Parfum Extrême<span class="sep">·</span>Unisex<span class="sep">·</span>Oriental cuero</div>', 'dh1')
rep('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
    '<div class="dh">Perfumistas: <b>Luca Maffei y Antoine Lie</b></div>', 'dh2')
rep('<div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '<div class="dh">Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>200,00 €</b> / 100 ml<span class="f">Precio: houbigant-parfum.com · consultado 04-11-2026 · Duración: Parfumo 8,3/10</span></div>', 'dh3')

# rating (4,19 / 5 -> estrella parcial al 19 %)
rep('<span class="r-num">4,15</span>', '<span class="r-num">4,19</span>', 'rating')
rep('<stop offset="15%" stop-color="#c9971c"/>', '<stop offset="19%" stop-color="#c9971c"/>', 'estrella parcial a')
rep('<stop offset="15%" stop-color="#d8d4c8"/>', '<stop offset="19%" stop-color="#d8d4c8"/>', 'estrella parcial b')
rep('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
    '<span class="r-meta">471 votos · 47 reseñas · Fragrantica</span>', 'r-meta')

# ---------------- 01 piramide: leyenda ----------------
rep('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
    '<span class="not">la chispa: bergamota, rosa y especias — ámbar cálido y cristalino</span>', 'leg salida')
rep('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
    '<span class="not">el alma: hoja de tabaco, haba tonka y azafrán — el humo dulce</span>', 'leg corazon')
rep('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
    '<span class="not">la estela: cuero y vainilla — lo que queda en la ropa</span>', 'leg fondo')
rep('Notas: Fragrantica / Le Secret du Marais',
    'Notas: houbigant-parfum.com + Fragrantica · consultado 04-11-2026', 'fuente notas')

# ---------------- losas SVG ----------------
rep("""    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }""",
    """    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'ESPECIAS · ROSA · BERGAMOTA' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'TABACO · TONKA · AZAFRÁN' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VAINILLA · CUERO' }""", 'capas svg')

rep("""    t2.setAttribute('text-anchor', 'middle'); t2.setAttribute('font-size', '14.5');""",
    """    t2.setAttribute('text-anchor', 'middle'); t2.setAttribute('font-size', c.w === 300 ? '11' : (c.w === 540 ? '13' : '14.5'));""", 'fuente losa')

# ---------------- 02 inspiracion ----------------
rep('<p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>',
    '<p>“Una composición explosiva que te transporta a la barbarie del desierto: hojas de tabaco refinadas se funden con notas especiadas, como un atardecer en las dunas doradas.”</p>', 'inspiracion')
rep('<span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
    '<span class="fuente-line">— Houbigant · descripción oficial [traducida] · consultado 04-11-2026</span>', 'fuente inspiracion')

# ---------------- 03 alternativas ----------------
rep('<div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>',
    '<div class="alt-item"><span class="alt-n">Tobacolor</span><span class="alt-casa">Dior · 2021</span><span class="alt-rt">4,17/5 · 3.057 votos</span><span class="alt-motivo">el mismo tabaco, más miel y más gourmand</span></div>', 'alt1')
rep('<div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>',
    '<div class="alt-item"><span class="alt-n">Red Tobacco</span><span class="alt-casa">Mancera · 2017</span><span class="alt-rt">4,02/5 · 13.530 votos</span><span class="alt-motivo">tabaco especiado más frutal y mucho más agresivo</span></div>', 'alt2')
rep('<div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>',
    '<div class="alt-item"><span class="alt-n">Herod</span><span class="alt-casa">Parfums de Marly · 2012</span><span class="alt-rt">4,42/5 · 11.121 votos</span><span class="alt-motivo">tabaco y vainilla con canela: más dulce y más suave</span></div>', 'alt3')
rep('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
    'Asociaciones: Parfumo «similar fragrances» + reseñas Fragrantica · consultado 04-11-2026', 'fuente alts')

# ---------------- 04 cita ----------------
rep('<blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>',
    '<blockquote>“Está lejos de ser un tabaco genérico: la nota huele a las hojas secándose en bastidores y enfardadas tras la cosecha de finales de verano. Aromático y resinoso; ligeramente embriagador… Un invento elegante y muy llevable.”</blockquote>', 'cita')
rep('<span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
    '<span class="fuente-line">— WolfScents · Fragrantica, reseña destacada [traducida] · 19-07-2026</span>', 'fuente cita')

# ---------------- pie ----------------
rep('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
    '<div class="clima">8,2–12,7 °C sens · media <b>10,8</b> · 23 % lluvia<br>banda <b>fresco</b> · amplitud 6,6 °C · ventana 08-18</div>', 'clima')
rep('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
    '<div class="sprays">Sprays: <b>3</b> interior · <b>4</b> exterior<br><span class="donde">cuello y pecho · día de trabajo · no en cerrado</span><br><span class="caveat-pie">que el tabaco se note sin cargar</span></div>', 'sprays/donde')

# ---------------- QR ----------------
rep('src="qr_fragrantica.png"', 'src="qr_fragrantica_tabac.png"', 'qr')

# ---------------- intensidad de texto (norma 30-oct-2026) ----------------
CORR = """<style id="intensidad-corr">
/* pase de intensidad de texto (norma 30-oct-2026): solo capa de texto */
.content { padding-bottom:42px !important; }
.dh, .dh b { color:#0a1d27 !important; }
.dh .sep { color:#4e6875 !important; }
.dh .f { color:#445d69 !important; }
.fecha-sep, .r-meta, .alt-casa, .sprays { color:#1f323c !important; }
.alt-motivo { color:#22353f !important; }
.alt-n { color:#0a1d27 !important; }
.alt-rt { color:#7a3d05 !important; }
.fuente-line { color:#2f434c !important; }
.nota-fondo { color:#3d4d55 !important; }
.sub, .caveat-pie, .sello b { color:#8c2e14 !important; }
.inspiracion p { color:#08171f !important; }
.cita blockquote { color:#171f57 !important; }
.cita .fuente-line { color:#33249a !important; }
.r-num { color:#8f6608 !important; }
.donde { color:#08303f !important; }
.pl .not { color:#0e2733 !important; }
.dh, .dh b, .dh .f, .sub, .caveat-pie, .inspiracion p, .alt-motivo, .alt-casa { text-shadow:0 1px 1px rgba(255,255,255,.55); }
.sec-title { text-shadow:0 1px 2px rgba(255,255,255,.50); }
</style>
</body>"""
if t.count('</body>') != 1:
    sys.exit('FAIL-CLOSED: </body> no unico')
t = t.replace('</body>', CORR, 1)
print('  ok pase intensidad')

# hex de titulos de seccion (texto, no iconos ni fondos)
for a, b in [('#12789e', '#0a5d7a'), ('#0e7c7b', '#0a5f5e'), ('#c96f1c', '#8f4409'), ('#5b42e6', '#3a2aa8')]:
    print(f'  hex {a}->{b}: {t.count(a)}'); t = t.replace(a, b)

# ---------------- guards ----------------
m = re.search(r"\.fondo[^{]*\{[^}]*url\('([^']+)'\)", t, re.S) or re.search(r"background:url\('([^']+)'\)", t)
print('CSS fondo:', m.group(1) if m else 'NO ENCONTRADO')
if not m or not os.path.exists(os.path.join(D, m.group(1))):
    sys.exit('FAIL-CLOSED: el fondo del CSS no existe en la carpeta')
for f in ['tabac_figura.png', 'qr_fragrantica_tabac.png']:
    if not os.path.exists(os.path.join(D, f)):
        sys.exit(f'FAIL-CLOSED: falta {f}')
if 'Texto de' in t or 'Alternativa 1' in t or 'nota salida' in t or '000,00' in t:
    sys.exit('FAIL-CLOSED: quedan placeholders de la plantilla')

open(OUT, 'w', encoding='utf-8').write(t)
print('ESCRITO:', OUT, len(t), 'chars')
