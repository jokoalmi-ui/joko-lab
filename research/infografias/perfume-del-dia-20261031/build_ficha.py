#!/usr/bin/env python3
"""Genera la ficha v5 de PEGASUS (Parfums de Marly) del 31-oct-2026.
Sustituciones fail-closed sobre la plantilla vigente: si un bloque no aparece
exactamente una vez, aborta sin escribir. Regla de no-retrofit: no toca
ninguna ficha anterior; escribe un fichero nuevo.
Incluye el pase de intensidad de texto (_corr, 30-oct-2026) ya en el generador.
"""
import sys, pathlib

TPL = pathlib.Path.home() / ".hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"
OUT = pathlib.Path(__file__).resolve().parent / "perfume_del_dia_v5_pegasus.html"

SUBS = []

# 0) fondo
SUBS.append((
    "    background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "    background:url('pegasus_fondo.png') center/cover no-repeat;",
))

# 1) cabecera
SUBS.append(('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
             '<div class="fecha-sep">SÁBADO · 31 OCTUBRE 2026</div>'))

# 2) figura
SUBS.append(('<img class="frasco-figura" src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma">',
             '<img class="frasco-figura" src="pegasus_figura.png" alt="Pegasus Parfums de Marly">'))
SUBS.append(('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
             '<div class="reflejo"><img src="pegasus_figura.png" alt=""></div>'))

# 3) hero
SUBS.append(('      <div class="casa">Profumum Roma</div>\n      <h1>Acqua di Sale</h1>\n      <div class="sub">el mar embotellado de Cerdeña</div>',
             '      <div class="casa">Parfums de Marly</div>\n      <h1>Pegasus</h1>\n      <div class="sub">almendra amarga, lavanda y vainilla sobre sándalo</div>'))

SUBS.append((
    '        <div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>\n'
    '        <div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>\n'
    '        <div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '        <div class="dh"><b>2011</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Fougère oriental</div>\n'
    '        <div class="dh">Perfumista: <b>Hamid Merati-Kashani</b></div>\n'
    '        <div class="dh">Longevidad <b>~7-8 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>290,00 €</b> / 125 ml · <b>232,00 €</b> / 100 ml · consultado 31-10-2026<span class="f">Duración: BD del lab y Parfumo (8,1/10) — Precio: parfums-de-marly.com</span></div>',
))

SUBS.append(('          <span class="r-num">4,15</span>', '          <span class="r-num">4,07</span>'))
SUBS.append(('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
             '<stop offset="81%" stop-color="#c9971c"/><stop offset="81%" stop-color="#d8d4c8"/>'))
SUBS.append(('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
             '<span class="r-meta">6.812 votos · 39 reseñas · Fragrantica</span>'))

# 4) pirámide (OFICIAL del fabricante)
SUBS.append(('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
             '<span class="not">la chispa: bergamota radiante y anís sobre almendra tostada</span>'))
SUBS.append(('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
             '<span class="not">el alma: jazmín y lavanda con la almendra amarga al mando</span>'))
SUBS.append(('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
             '<span class="not">la estela: vainilla cálida, ámbar y sándalo — horas en la piel</span>'))
SUBS.append(('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
             '<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial de parfums-de-marly.com · consultada 31-10-2026</span>'))

SUBS.append(("""    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }""",
             """    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'ANÍS · BERGAMOTA · ALMENDRA' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'JAZMÍN · LAVANDA · ALMENDRA AMARGA' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VAINILLA · ÁMBAR · SÁNDALO' }"""))

# 5) inspiración (descripción oficial, ya en español)
SUBS.append(('      <p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>\n      <span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
             '      <p>“Pegasus se abre con una radiante bergamota, suavizada por la delicadeza de la almendra, para desplegarse en unas cálidas y cautivadoras notas de fondo de vainilla. Vibrante, adictivo y sensual.”</p>\n      <span class="fuente-line">— Parfums de Marly · descripción oficial · consultada 31-10-2026</span>'))

# 6) alternativas
SUBS.append(("""      <div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>
      <div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>
      <div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>""",
             """      <div class="alt-item"><span class="alt-n">Craze</span><span class="alt-casa">Armaf · 2013</span><span class="alt-rt">7,6/10 · 565 votos</span><span class="alt-motivo">el clon más citado: misma almendra y vainilla · 19 £/100 ml</span></div>
      <div class="alt-item"><span class="alt-n">Perseus</span><span class="alt-casa">Maison Alhambra · 2023</span><span class="alt-rt">90 % de notas en común</span><span class="alt-motivo">«se parece muchísimo… un 98 %» (Fragrantica ES) · 17 £/100 ml</span></div>
      <div class="alt-item"><span class="alt-n">Hypnotic Poison</span><span class="alt-casa">Dior · 1998</span><span class="alt-rt">4,08/5 · 30.857 votos</span><span class="alt-motivo">la versión femenina del acorde almendra-vainilla</span></div>"""))
SUBS.append(('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
             '<span class="fuente-line" style="margin-left:44px;">Asociaciones: reseñas Fragrantica ES, Parfumo y thescentatlas · precios de thescentatlas (consultados 31-10-2026)</span>'))

# 7) cita comunidad (reseña real Fragrantica ES, en español)
SUBS.append(('      <blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>\n      <span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
             '      <blockquote>“La almendra se le siente muchísimo, se siente bastante especiado y cálido… su escenario es la noche y el clima fresco le favorece.”</blockquote>\n      <span class="fuente-line">— peterMartinez · reseña en Fragrantica ES, 25-dic-2025</span>'))

# 8) pie
SUBS.append(('    <div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
             '    <div class="clima">10,4–17,4 °C · media 15,0 · 0 % lluvia<br>fougère de almendra para un día templado</div>'))
SUBS.append(('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
             '<div class="sprays">Sprays: <b>3</b> a las 08:00 · <b>3</b> si repites de tarde<br><span class="donde">cuello y pecho · oficina y ciudad · no en calor</span><br><span class="caveat-pie">la almendra que abriga sin empalagar</span></div>'))
SUBS.append(("padding:8px 52px 8px; }", "padding:8px 52px 52px; }"))

SUBS.append(('<img class="qr" src="qr_fragrantica.png" alt="QR Fragrantica">',
             '<img class="qr" src="qr_fragrantica_pegasus.png" alt="QR Fragrantica">'))

# 8bis) sombra del frasco medida: sube el cuerpo de 2,19 a 2,46:1 (tapón 3,32:1)
SUBS.append(('  .frasco-figura { height:450px; width:auto; filter:drop-shadow(0 8px 14px rgba(30,17,2,0.70)) drop-shadow(0 22px 44px rgba(58,35,6,0.55)) drop-shadow(0 0 60px rgba(70,44,10,0.35)); position:relative; z-index:2; }',
             '  .frasco-figura { height:450px; width:auto; filter:drop-shadow(0 6px 10px rgba(26,14,2,0.80)) drop-shadow(0 18px 34px rgba(48,28,6,0.65)) drop-shadow(0 0 46px rgba(58,36,8,0.55)) drop-shadow(0 0 18px rgba(40,22,2,0.45)); position:relative; z-index:2; }'))

# 9) pase de intensidad del texto (receta _corr del 30-oct-2026)
SUBS.append(("</style>", """
/* ---- corr: intensidad del texto. NO toca foto, velo, cajas ni pesos (evita reflow) ---- */
.r-num{color:#8f6608 !important;}
.cita .fuente-line{color:#33249a;}
.sec-title{text-shadow:0 1px 2px rgba(255,255,255,.50);}
.dh .f,.fuente-line,.nota-fondo{letter-spacing:.1px;}
.dh, .dh b { color:#0a1d27; }
.dh .sep { color:#4e6875; }
.dh .f { color:#445d69; }
.fecha-sep, .r-meta, .alt-casa, .sprays { color:#1f323c; }
.alt-motivo { color:#22353f; }
.alt-rt { color:#7a3d05; }
.fuente-line { color:#2f434c; }
.nota-fondo { color:#3d4d55; }
.sub, .caveat-pie, .sello b { color:#8c2e14; }
.inspiracion p { color:#08171f; }
.cita blockquote { color:#171f57; }
.dh, .dh b, .fuente-line, .alt-casa, .alt-motivo, .alt-rt, .nota-fondo, .sprays, .fecha-sep, .r-meta, .inspiracion p {
  text-shadow: 0 1px 1px rgba(255,255,255,.55);
}
</style>"""))

# títulos de sección: hex oscurecidos (inline, ganan a la clase)
for old, new in (("color:#12789e;", "color:#0a5d7a;"), ("color:#0e7c7b;", "color:#0a5f5e;"),
                 ("color:#c96f1c;", "color:#8f4409;"), ("color:#5b42e6;", "color:#3a2aa8;")):
    SUBS.append((old, new))

txt = TPL.read_text(encoding="utf-8")
PERMITIDOS = {"color:#c96f1c;": 2}
for old, new in SUBS:
    n = txt.count(old)
    if n != PERMITIDOS.get(old, 1):
        sys.exit(f"FAIL-CLOSED: bloque aparece {n} veces (esperado {PERMITIDOS.get(old,1)}): {old[:70]!r}")
    txt = txt.replace(old, new)

# asertos de contenido final
checks = {
    "Pegasus": 1, "Parfums de Marly": 1, "31 OCTUBRE 2026": 1, "290,00 €": 1,
    "consultado 31-10-2026": 1, "pegasus_figura.png": 2, "pegasus_fondo.png": 1,
    'class="donde"': 1, "15,0": 1, "10,4–17,4 °C": 1, "Hamid Merati-Kashani": 1,
    "ALMENDRA AMARGA": 1, "color:#0a5d7a;": 1, "text-shadow: 0 1px 1px": 1,
}
for k, v in checks.items():
    if txt.count(k) < v:
        sys.exit(f"FAIL-CLOSED: falta {k!r} en la ficha")
tail = txt.split("-->", 1)[-1]
for resto in ("Acqua di Sale", "acqua_di_sale", "Profumum", "Megamare", "Kenzo"):
    if resto in tail:
        sys.exit(f"FAIL-CLOSED: quedan restos de la plantilla de ejemplo ({resto})")

OUT.write_text(txt, encoding="utf-8")
print("OK ->", OUT, len(txt), "bytes")
