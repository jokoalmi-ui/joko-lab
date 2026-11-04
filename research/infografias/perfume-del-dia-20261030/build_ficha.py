#!/usr/bin/env python3
"""Genera la ficha v5 de APEX (Roja Parfums) del 30-oct-2026.
Sustituciones fail-closed sobre la plantilla vigente: si un bloque no aparece
exactamente una vez, aborta sin escribir. Regla de no-retrofit: no toca
ninguna ficha anterior; escribe un fichero nuevo.
"""
import sys, pathlib

TPL = pathlib.Path.home() / ".hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"
OUT = pathlib.Path(__file__).resolve().parent / "perfume_del_dia_v5_apex.html"

SUBS = []

# 0) fondo
SUBS.append((
    "    background:url('acqua_di_sale_fondo.png') center/cover no-repeat;",
    "    background:url('apex_fondo.png') center/cover no-repeat;",
))

# 1) cabecera
SUBS.append(('<div class="fecha-sep">MIÉRCOLES · 02 SEPTIEMBRE 2026</div>',
             '<div class="fecha-sep">VIERNES · 30 OCTUBRE 2026</div>'))

# 2) figura
SUBS.append(('<img class="frasco-figura" src="frasco_figura_acqua_di_sale.png" alt="Acqua di Sale Profumum Roma">',
             '<img class="frasco-figura" src="apex_figura.png" alt="Apex Roja Parfums">'))
SUBS.append(('<div class="reflejo"><img src="frasco_figura_acqua_di_sale.png" alt=""></div>',
             '<div class="reflejo"><img src="apex_figura.png" alt=""></div>'))

# 3) hero
SUBS.append(('      <div class="casa">Profumum Roma</div>\n      <h1>Acqua di Sale</h1>\n      <div class="sub">el mar embotellado de Cerdeña</div>',
             '      <div class="casa">Roja Parfums</div>\n      <h1>Apex</h1>\n      <div class="sub">el bosque antiguo, cítrico y con cuero</div>'))

SUBS.append((
    '        <div class="dh"><b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática</div>\n'
    '        <div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>\n'
    '        <div class="dh">Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span></div>',
    '        <div class="dh"><b>2022</b><span class="sep">·</span>Eau de Parfum<span class="sep">·</span>Masculino<span class="sep">·</span>Chipre</div>\n'
    '        <div class="dh">Perfumista: <b>Roja Dove</b></div>\n'
    '        <div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b><span class="sep">·</span><b>335,00 €</b> / 100 ml · consultado 30-10-2026<span class="f">Duración: BD del lab y reseñas (7-9 h) — Precio: Perfumería Laura</span></div>',
))

SUBS.append(('          <span class="r-num">4,15</span>', '          <span class="r-num">3,87</span>'))
SUBS.append(('<stop offset="15%" stop-color="#c9971c"/><stop offset="15%" stop-color="#d8d4c8"/>',
             '<stop offset="77%" stop-color="#c9971c"/><stop offset="77%" stop-color="#d8d4c8"/>'))
SUBS.append(('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
             '<span class="r-meta">1.324 votos · 288 reseñas · Fragrantica</span>'))

# 4) pirámide
SUBS.append(('<span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
             '<span class="not">la chispa: cítricos brillantes y piña jugosa</span>'))
SUBS.append(('<span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
             '<span class="not">el alma: jazmín, jara y resinas verdes</span>'))
SUBS.append(('<span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
             '<span class="not">la estela: ciprés, musgo de roble, cuero y ámbar — horas en la piel</span>'))
SUBS.append(('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
             '<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial de rojadoveperfumery.com</span>'))

SUBS.append(("""    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }""",
             """    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'LIMÓN · BERGAMOTA · MANDARINA · NARANJA' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'JAZMÍN · JARA · PIÑA' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CIPRÉS · MUSGO DE ROBLE · CUERO · TABACO' }"""))

# 5) inspiración (descripción oficial de la casa, rojadoveperfumery.com)
SUBS.append(('      <p>“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”</p>\n      <span class="fuente-line">— Casa Profumum Roma · inspiración oficial [traducida del italiano]</span>',
             '      <p>“Celebrando las maravillas del mundo natural y a quienes lo recorren, APEX es un acorde chipre fresco y afrutado con matices espirituales y sensuales. Una base chipre rodea el pachulí y el abeto balsámico con los tonos verdes de gálbano, ciprés y musgo de roble hasta crear un entorno verdaderamente de exterior.”</p>\n      <span class="fuente-line">— Roja Dove Perfumery · descripción oficial de APEX [traducida del inglés]</span>'))

# 6) alternativas
SUBS.append(("""      <div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>
      <div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>
      <div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>""",
             """      <div class="alt-item"><span class="alt-n">Polo Green</span><span class="alt-casa">Ralph Lauren · 1978</span><span class="alt-rt">3,79/5 · 7.252 votos</span><span class="alt-motivo">el clásico que Apex reimagina: pino, musgo y tabaco · 139,95 €/118 ml</span></div>
      <div class="alt-item"><span class="alt-n">Drakon</span><span class="alt-casa">Carner Barcelona · 2020</span><span class="alt-rt">3,98/5 · 197 votos</span><span class="alt-motivo">ciprés y cuero, hecha en España · desde 119,99 €/50 ml</span></div>
      <div class="alt-item"><span class="alt-n">Halston Z-14</span><span class="alt-casa">Halston · 1974</span><span class="alt-rt">4,03/5 · 2.073 votos</span><span class="alt-motivo">chipre de ciprés y cuero por 17,59 €/125 ml</span></div>"""))
SUBS.append(('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica</span>',
             '<span class="fuente-line" style="margin-left:44px;">Asociaciones: hilos de Fragrantica, Reddit r/fragrance y Parfumo · precios de pracan, carnerbarcelona/deloox y brasty (consultados 30-oct-2026)</span>'))

# 7) cita comunidad (reseña Fragrantica del EDP, traducida)
SUBS.append(('      <blockquote>“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”</blockquote>\n      <span class="fuente-line">— Reseña en Fragrantica · comunidad [ES]</span>',
             '      <blockquote>“Lo que empieza luminoso y frutal acaba siendo más oscuro, más rico y bastante más complejo: una evolución de cítricos y piña hacia un tapiz de verdes aromáticos, maderas, resinas, cuero y tabaco.”</blockquote>\n      <span class="fuente-line">— Reseña de usuario en Fragrantica, 2026 [traducida del inglés]</span>'))

# 8) pie
SUBS.append(('    <div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
             '    <div class="clima">11,5–18,5 °C · media 15,8 · 0 % lluvia<br>chipre verde y cuero para un día templado</div>'))
SUBS.append(('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="donde">cuello y pecho · exterior y calor · no en cerrado</span><br><span class="caveat-pie">que huela a mar todo el día</span></div>',
             '<div class="sprays">Sprays: <b>3</b> por la mañana · sin retoque<br><span class="donde">cuello y pecho · oficina y ciudad · no en calor</span><br><span class="caveat-pie">el bosque que se queda en la piel</span></div>'))
SUBS.append(("padding:8px 52px 8px; }", "padding:8px 52px 52px; }"))

SUBS.append(('<img class="qr" src="qr_fragrantica.png" alt="QR Fragrantica">',
             '<img class="qr" src="qr_fragrantica_apex.png" alt="QR Fragrantica">'))

txt = TPL.read_text(encoding="utf-8")
for old, new in SUBS:
    n = txt.count(old)
    if n != 1:
        sys.exit(f"FAIL-CLOSED: bloque aparece {n} veces (esperado 1): {old[:70]!r}")
    txt = txt.replace(old, new)

# asertos de contenido final
checks = {
    "Apex": 1, "Roja Parfums": 1, "30 OCTUBRE 2026": 1, "335,00 €": 1,
    "consultado 30-10-2026": 1, "apex_figura.png": 2, "apex_fondo.png": 1,
    'class="donde"': 1, "15,8": 1, "11,5–18,5 °C": 1, "Roja Dove": 1,
}
for k, v in checks.items():
    if txt.count(k) < v:
        sys.exit(f"FAIL-CLOSED: falta {k!r} en la ficha")
tail = txt.split("-->", 1)[-1]
for resto in ("Acqua di Sale", "acqua_di_sale", "Profumum"):
    if resto in tail:
        sys.exit(f"FAIL-CLOSED: quedan restos de la plantilla de ejemplo ({resto})")

OUT.write_text(txt, encoding="utf-8")
print("OK ->", OUT, len(txt), "bytes")
