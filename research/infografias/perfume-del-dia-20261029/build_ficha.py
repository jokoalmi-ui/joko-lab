#!/usr/bin/env python3
"""Genera la ficha v5 de ÔIKB (Santi Burgas) del 29-oct-2026.
Sustituciones fail-closed sobre la plantilla vigente: si un bloque no aparece
exactamente una vez, aborta sin escribir. Regla de no-retrofit: no toca
ninguna ficha anterior; escribe un fichero nuevo.
"""
import sys, pathlib

TPL = pathlib.Path.home() / ".hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"
OUT = pathlib.Path(__file__).resolve().parent / "perfume_del_dia_v5_oikb.html"

SUBS = []

# 0) fondo + viñeta (frasco de cuerpo claro: la viñeta oscura detrás sube el contraste)
SUBS.append((
    "    background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "    background:radial-gradient(ellipse 360px 600px at 202px 300px, rgba(12,18,28,0.50) 0%, rgba(12,18,28,0.34) 45%, rgba(12,18,28,0.14) 72%, rgba(12,18,28,0) 100%), url('santi_oikb_fondo_c.png') center/cover no-repeat;",
))

# 1) cabecera
SUBS.append(('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
             '<div class="fecha-sep">JUEVES · 29 OCTUBRE 2026</div>'))

# 2) figura
SUBS.append(('<img class="frasco-figura" src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma">',
             '<img class="frasco-figura" src="santi_oikb_figura.png" alt="ÔIKB Santi Burgas">'))
SUBS.append(('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
             '<div class="reflejo"><img src="santi_oikb_figura.png" alt=""></div>'))

# 3) hero
SUBS.append(('      <div class="casa">Profumum Roma</div>\n      <h1>Acqua di Sale</h1>\n      <div class="sub">el mar embotellado de Cerdeña</div>',
             '      <div class="casa">Santi Burgas</div>\n      <h1>ÔIKB</h1>\n      <div class="sub">iris empolvado y cuero sobre azul Klein</div>'))

SUBS.append((
    '        <div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>\n'
    '        <div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>\n'
    '        <div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '        <div class="dh"><b>2016</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Oriental especiada</div>\n'
    '        <div class="dh">Perfumista: <b>Santi Burgas (Santiago Burgas Bou)</b></div>\n'
    '        <div class="dh">Longevidad <b>9-12 h</b><span class="sep">·</span>Estela <b>moderada-intensa</b><span class="sep">·</span><b>185,00 €</b> / 100 ml · consultado 29-10-2026<span class="f">Duración: Parfumo 8,7/10 · 57 votos y reseñas 9-12 h — Precio: santiburgas.com</span></div>',
))

SUBS.append(('          <span class="r-num">4,15</span>', '          <span class="r-num">4,34</span>'))
SUBS.append(('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
             '<stop offset="34%" stop-color="#c9971c"/><stop offset="34%" stop-color="#d8d4c8"/>'))
SUBS.append(('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
             '<span class="r-meta">246 votos · 19 reseñas · Fragrantica</span>'))

# 4) pirámide
SUBS.append(('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
             '<span class="not">la chispa: lavanda, pimienta negra y nuez moscada</span>'))
SUBS.append(('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
             '<span class="not">el alma: iris arcilloso, raíz de zanahoria y cuero</span>'))
SUBS.append(('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
             '<span class="not">la estela: cedro, haba tonka y piedra de África — horas en la piel</span>'))
SUBS.append(('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
             '<span class="fuente-line" style="margin-top:4px;">Notas: pirámide de Fragrantica y Parfumo</span>'))

SUBS.append(("""    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }""",
             """    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'LAVANDA · PIMIENTA · NUEZ MOSCADA' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'IRIS · CUERO' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · TONKA · PIEDRA DE ÁFRICA' }"""))

# 5) inspiración (descripción oficial de la casa, santiburgas.com)
SUBS.append(('      <p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>\n      <span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
             '      <p>“Tu color es mi aroma. Primero caí en la inmensidad; luego algo emerge de lo profundo y, de repente, mi piel siente una azulidad honda.”</p>\n      <span class="fuente-line">— Santi Burgas · descripción oficial de ÔIKB, «Eau Intense King Blue» [traducida del inglés]</span>'))

# 6) alternativas
SUBS.append(("""      <div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>
      <div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>
      <div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>""",
             """      <div class="alt-item"><span class="alt-n">Cuir Zerzura</span><span class="alt-casa">Armani Privé · 2020</span><span class="alt-rt">4,39/5 · 480 votos</span><span class="alt-motivo">44 % de parecido votado: cuero-iris más seco</span></div>
      <div class="alt-item"><span class="alt-n">Read My Mind</span><span class="alt-casa">Bruno Acampora · 2019</span><span class="alt-rt">3,93/5 · 14 votos</span><span class="alt-motivo">mismo iris+cuero, más resinoso</span></div>
      <div class="alt-item"><span class="alt-n">Knize Ten</span><span class="alt-casa">Knize · 1925</span><span class="alt-rt">4,18/5 · 1.242 votos</span><span class="alt-motivo">el cuero animal clásico, 72 €/50 ml</span></div>"""))
SUBS.append(('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
             '<span class="fuente-line" style="margin-left:44px;">Asociaciones: Parfumistas · Fragrantica · Parfumo · precios de armani.com y knize.at (consultados 29-oct-2026)</span>'))

# 7) cita comunidad (Cribrosa, Fragrantica 25-abr-2026, traducida)
SUBS.append(('      <blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>\n      <span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
             '      <blockquote>“Me encanta esta combinación tan poco habitual de iris empolvado y cuero animal. En mi piel pasa enseguida, en una hora, a un tonka amaderado y cómodo. Edito: es adictivo.”</blockquote>\n      <span class="fuente-line">— Cribrosa · reseña en Fragrantica, 25-abr-2026 [traducida del inglés]</span>'))

# 8) pie
SUBS.append(('    <div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
             '    <div class="clima">11,1–17,9 °C · media 15,8 · 0 % lluvia<br>iris y cuero para un día templado de otoño</div>'))
SUBS.append(('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
             '<div class="sprays">Sprays: <b>3</b> por la mañana · sin retoque<br><span class="donde">cuello y nuca · oficina y ciudad · no en calor</span><br><span class="caveat-pie">el azul que se queda en la piel</span></div>'))
SUBS.append(('<img class="qr" src="qr_fragrantica.png" alt="QR Fragrantica">',
             '<img class="qr" src="qr_fragrantica_oikb.png" alt="QR Fragrantica">'))

# 9) encaje vertical: el pie sube 52 px (canon: pie ≤1394, aire ≥45)
SUBS.append(("padding:8px 52px 8px; }", "padding:8px 52px 52px; }"))

txt = TPL.read_text(encoding="utf-8")
for old, new in SUBS:
    n = txt.count(old)
    if n != 1:
        sys.exit(f"FAIL-CLOSED: bloque aparece {n} veces (esperado 1): {old[:70]!r}")
    txt = txt.replace(old, new)

# asertos de contenido final
checks = {
    "ÔIKB": 1, "Santi Burgas": 1, "29 OCTUBRE 2026": 1, "185,00 €": 1,
    "consultado 29-10-2026": 1, "santi_oikb_figura.png": 2, "santi_oikb_fondo_c.png": 1,
    "class=\"donde\"": 1, "15,8": 1, "11,1–17,9 °C": 1,
}
for k, v in checks.items():
    if txt.count(k) < v:
        sys.exit(f"FAIL-CLOSED: falta {k!r} en la ficha")
if "Acqua di Sale" in txt.split("-->", 1)[-1] or "acqua_di_sale" in txt.split("-->", 1)[-1] or "Profumum" in txt.split("-->", 1)[-1]:
    sys.exit("FAIL-CLOSED: quedan restos de la plantilla de ejemplo")

OUT.write_text(txt, encoding="utf-8")
print("OK ->", OUT, len(txt), "bytes")
