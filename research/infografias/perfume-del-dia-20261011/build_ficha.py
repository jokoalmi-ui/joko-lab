#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye la ficha v5 de hoy partiendo de la plantilla oficial del lab.

Método: NO se reescribe la plantilla — se sustituyen campos por texto EXACTO
(assert de coincidencia, fail-closed). El head CSS se conserva íntegro salvo
el nombre del fondo, que debe coincidir con el fichero real de la carpeta.
"""
import os, re, sys, difflib

TPL = '/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html'
D   = '/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20261011'
OUT = os.path.join(D, 'perfume_del_dia_v5_reflection_man.html')

# --- fail-closed: los assets deben existir y llamarse EXACTAMENTE así (26-sep/06-oct)
for f in ('reflection_man_fondo.png', 'reflection_man_figura.png', 'qr_fragrantica.png'):
    p = os.path.join(D, f)
    if not os.path.exists(p):
        sys.exit('ABORTA: falta %s' % p)

h = open(TPL, encoding='utf-8').read()

CAPAS = """    { w: 300, f:'#7ba428', t:'#a9cc63', l:'#587821', c1:'SALIDA', txt:'ROMERO · PIMIENTA ROSA · PETITGRAIN' },
    { w: 420, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'CORAZÓN', txt:'IRIS · NEROLI · JAZMÍN · YLANG' },
    { w: 540, f:'#6b4a2f', t:'#9a7350', l:'#4a3220', c1:'FONDO', txt:'SÁNDALO · CEDRO · PACHULÍ · VETIVER' }"""

CAPAS_OLD = """    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'SAL · LAVANDA · MIRTO' },
    { w: 420, f:'#177fa3', t:'#4fb6cd', l:'#0f5f7c', c1:'CORAZÓN', txt:'ALGA · NOTAS MARINAS · JENGIBRE' },
    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'CEDRO · ALMIZCLE · MIRRA · VAINILLA' }"""

ALTS_OLD = """      <div class="alt-item"><span class="alt-n">Megamare</span><span class="alt-casa">Orto Parisi · 2019</span><span class="alt-rt">3,89/5 · 8.485 votos</span><span class="alt-motivo">el mar profundo, más oscuro y salino</span></div>
      <div class="alt-item"><span class="alt-n">Kenzo pour Homme</span><span class="alt-casa">Kenzo · 1991</span><span class="alt-rt">4,07/5 · 3.984 votos</span><span class="alt-motivo">“recrea el mar como Acqua di Sale”</span></div>
      <div class="alt-item"><span class="alt-n">Costarela</span><span class="alt-casa">Carner Barcelona · 2016</span><span class="alt-rt">3,71/5 · 663 votos</span><span class="alt-motivo">mismo campo, giro más suave y mejor precio</span></div>"""

ALTS_NEW = """      <div class="alt-item"><span class="alt-n">Reflection 45</span><span class="alt-casa">Amouage · 2021</span><span class="alt-rt">8,8/10 · 2.191 votos</span><span class="alt-motivo">el mismo ramo con 45 % de aceite: más profundo y mucho más caro</span></div>
      <div class="alt-item"><span class="alt-n">Guilty Elixir de Parfum pour Homme</span><span class="alt-casa">Gucci · 2023</span><span class="alt-rt">8,2/10 · 1.401 votos</span><span class="alt-motivo">floral ambarado moderno con la misma limpieza</span></div>
      <div class="alt-item"><span class="alt-n">Le Mâle</span><span class="alt-casa">Jean Paul Gaultier · 1995</span><span class="alt-rt">7,6/10 · 4.902 votos</span><span class="alt-motivo">una reseña de Parfumo dice que su salida «recuerda mucho a Le Mâle»</span></div>
      <div class="alt-item"><span class="alt-n">Shiyaaka for Men</span><span class="alt-casa">Khadlaj · ya en tu colección</span><span class="alt-rt">sin rating verificado</span><span class="alt-motivo">el clon declarado: compáralo con el original</span></div>"""

PAIRS = [
 ("background:url('acqua_di_sale_fondo.png')", "background:url('reflection_man_fondo.png')", 1),
 ("MIÉRCOLES · 02 SEPTIEMBRE 2026", "DOMINGO · 11 OCTUBRE 2026", 1),
 ("frasco_figura_acqua_di_sale.png", "reflection_man_figura.png", 2),
 ('alt="Acqua di Sale Profumum Roma"', 'alt="Amouage Reflection Man"', 1),
 ('<div class="casa">Profumum Roma</div>', '<div class="casa">Amouage</div>', 1),
 ('<h1>Acqua di Sale</h1>', '<h1>Reflection Man</h1>', 1),
 ('<div class="sub">el mar embotellado de Cerdeña</div>', '<div class="sub">el ramo blanco mejor trajeado</div>', 1),
 ('<b>1996</b><span class="sep">·</span>Extrait de Parfum<span class="sep">·</span>Unisex<span class="sep">·</span>Marina acuática',
  '<b>2006</b><span class="sep">·</span>Eau de Parfum (EDP)<span class="sep">·</span>Masculino<span class="sep">·</span>Floral', 1),
 ('<div class="dh">Perfumistas: <b>Felice, Luciano y Maria Durante</b></div>',
  '<div class="dh">Perfumista: <b>Lucas Sieuzac</b></div>', 1),
 ('Longevidad <b>~10 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>206,61 €</b> / 100 ml<span class="f">Duración: Parfumo · reseñas — Precio: web oficial</span>',
  'Longevidad <b>11 h</b><span class="sep">·</span>Estela <b>intensa</b><span class="sep">·</span><b>365 €</b> / 100 ml<span class="f">Duración: BD coleccion.db — Precio: Isolée · consultado 11-oct-2026</span>', 1),
 ('<span class="r-num">4,15</span>', '<span class="r-num">4,39</span>', 1),
 ('<stop offset="15%"', '<stop offset="39%"', 2),
 ('<span class="r-meta">2.494 votos · 273 reseñas · Fragrantica</span>',
  '<span class="r-meta">10.694 votos · Fragrantica · 8,6/10 Parfumo</span>', 1),
 # --- 01: color de sección + capas + leyenda + fuente
 ('style="background:#12789e;">01', 'style="background:#2e7d4f;">01', 1),
 ('style="color:#12789e;">', 'style="color:#2e7d4f;">', 1),
 (CAPAS_OLD, CAPAS, 1),
 ('<span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Salida</span><span class="not">la chispa: sal, lavanda y mirto — lo primero que golpea</span>',
  '<span class="sw" style="background:linear-gradient(135deg,#a9cc63,#7ba428);"></span><span class="lab" style="color:#587821;">Salida</span><span class="not">la chispa: romero y pimienta rosa — limpio y herbáceo</span>', 1),
 ('<span class="sw" style="background:linear-gradient(135deg,#4fb6cd,#177fa3);"></span><span class="lab" style="color:#177fa3;">Corazón</span><span class="not">el alma: alga y notas marinas — la profundidad del mar</span>',
  '<span class="sw" style="background:linear-gradient(135deg,#f6cf66,#d99c26);"></span><span class="lab" style="color:#a57112;">Corazón</span><span class="not">el ramo blanco: iris, neroli, jazmín y ylang — la firma</span>', 1),
 ('<span class="sw" style="background:linear-gradient(135deg,#4d7f9e,#244c63);"></span><span class="lab" style="color:#244c63;">Fondo</span><span class="not">la estela: cedro, almizcle, mirra y vainilla — horas en la piel</span>',
  '<span class="sw" style="background:linear-gradient(135deg,#9a7350,#6b4a2f);"></span><span class="lab" style="color:#4a3220;">Fondo</span><span class="not">la estela: sándalo, cedro, pachulí y vetiver — horas en la piel</span>', 1),
 ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica / Le Secret du Marais</span>',
  '<span class="fuente-line" style="margin-top:4px;">Notas: web oficial Amouage · Fragrantica [consultado 11-oct-2026]</span>', 1),
 # --- 02
 ('“Las olas que rompen en la orilla regalan nuevas conchas a la arena que brilla bajo el sol de agosto. En la playa desierta flotan la despreocupación y la libertad.”',
  '«Reflection for Man encarna el espíritu del refinamiento: cautivador, distintivo e inconfundiblemente masculino, con un atractivo atemporal. 25 % de concentración de aceite y 8 semanas de reposo — 5 de maceración y 3 de maduración.»', 1),
 ('— Casa Profumum Roma · inspiración oficial [traducida del italiano]',
  '— Amouage · ficha oficial [traducida del inglés] · consultado 11-oct-2026', 1),
 # --- 03
 (ALTS_OLD, ALTS_NEW, 1),
 ('Asociaciones de comunidad: Bloom Perfumery · reseñas Fragrantica',
  'Asociaciones: Parfumo (similar) · reseñas de comunidad · tu colección · consultado 11-oct-2026', 1),
 # --- 04
 ('“Robusto en aroma, duración y proyección… una bestia. Marcar un precedente en su arquetipo lo convierte en un aroma legendario (a considerar que es de 1996).”',
  '«¿Le Mâle? Sí, la salida me recordó mucho a Le Mâle. Esa combinación floral de rosa y jazmín, junto con el almizcle, me recuerda a una sábana blanca, muy limpia y perfumada: esa fue la imagen que me vino a la mente.»', 1),
 ('— Reseña en Fragrantica · comunidad [ES]',
  '— Reseña en Parfumo, en alemán [traducida] · consultado 11-oct-2026', 1),
 # --- PIE
 ('<div class="clima">27 °C · 0 % lluvia · final de verano<br>marino mineral para el calor</div>',
  '<div class="clima">Ventana 08-18 · 14,7 – 23,0 °C (media 19,6)<br>humedad 69 % · lluvia ≤11 % · floral limpio</div>', 1),
 ('<div class="sprays">Sprays: <b>2</b> interior · <b>3</b> exterior<br><span class="caveat-pie">que huela a mar todo el día</span></div>',
  '<div class="sprays">Sprays: <b>3</b> mañana (16 °C) · <b>2-3</b> tarde (22 °C)<br><span class="caveat-pie">un ramo blanco sin gritar</span></div>', 1),
]

for old, new, exp in PAIRS:
    n = h.count(old)
    if n != exp:
        sys.exit('ABORTA: "%s..." aparece %d veces (esperado %d)' % (old[:60], n, exp))
    h = h.replace(old, new)

# --- HERO del frasco: integración por SOMBRA (fail-closed, 11-oct-2026) ---------------
# El head CSS de la plantilla traía la sombra AZUL del fondo marino (rgba(10,40,60,...)):
# con un fondo claro/cálido el frasco queda sin integrar (medido 11-oct en Reflection Man:
# cuerpo 2,06:1 y fondo contiguo L 141 -> el frasco "flota" pegado). La receta MEDIDA es la
# sombra cálida APILADA + .sombra-suelo grande: 08-oct Naxos 1,84 -> 2,46:1; 11-oct 2,06 ->
# 2,70:1, con la columna de texto y la puerta intactas. Este bloque la IMPONE: si la
# plantilla vuelve a traer la azul, el generador la sustituye; si no hay sombra cálida
# posible, ABORTA en vez de publicar una ficha con el frasco pegado.
HERO_CAL = ("filter:drop-shadow(0 8px 14px rgba(30,17,2,0.70)) "
            "drop-shadow(0 22px 44px rgba(58,35,6,0.55)) "
            "drop-shadow(0 0 60px rgba(70,44,10,0.35))")
HERO_VIEJAS = [
    "filter:drop-shadow(0 18px 26px rgba(10,40,60,0.38))",
    "filter:brightness(1.06) drop-shadow(0 0 26px rgba(22,13,2,0.82)) "
    "drop-shadow(0 10px 34px rgba(30,18,4,0.72)) drop-shadow(0 0 78px rgba(40,24,6,0.60))",
]
for v in HERO_VIEJAS:
    if v in h:
        h = h.replace(v, HERO_CAL)
        print('HERO: sombra sustituida por la cálida medida ->', v[:46], '...')
SUELO_VIEJO = ("width:285px; height:26px; background:radial-gradient(ellipse, "
               "rgba(10,40,60,0.30) 0%, transparent 70%)")
if SUELO_VIEJO in h:
    h = h.replace(SUELO_VIEJO, "width:330px; height:48px; background:radial-gradient(ellipse, "
                  "rgba(30,17,2,0.62) 0%, rgba(46,28,8,0.34) 45%, transparent 72%)")
    print('HERO: .sombra-suelo ampliada a 330x48 y cálida')
if 'rgba(10,40,60,0.38)' in h:
    sys.exit('ABORTA: queda la sombra AZUL en .frasco-figura (11-oct-2026)')
if not ('rgba(30,17,2,' in h or 'rgba(22,13,2,' in h or 'rgba(58,35,6,' in h):
    sys.exit('ABORTA: el hero no lleva sombra cálida (11-oct-2026) — el frasco se pega al fondo')

open(OUT, 'w', encoding='utf-8').write(h)
print('OK', OUT, len(h), 'chars')
print('fondo en CSS:', re.findall(r"url\('([^']+)'\)", h)[:4])
print('fuentes distintas de asset:', sorted(set(re.findall(r'src="([^"]+)"', h))))
