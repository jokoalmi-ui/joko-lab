#!/usr/bin/env python3
"""Pirámide olfativa 3D v2 — 3 LOSAS apiladas (ancho creciente): cada capa tiene
frontal legible (notas DENTRO, sin desborde) + lateral sombreado + techo.
Datos reales: Acqua di Sale (Profumum Roma). Paleta frío->cálido.
"""
import os

# ---- parámetros de las 3 losas (x centro = 0) ----
# cada losa: [nombre, y_techo (borde sup frontal), y_base, media-anchura, color frontal (2), color lateral(2), color techo]
LOSAS = [
    # (nombre, y_top, y_bot, halfW)
    ("FONDO",   120.0, 320.0, 330.0),
    ("CORAZÓN", -60.0, 120.0, 245.0),
    ("SALIDA", -230.0, -60.0, 150.0),
]
PAL = {
    "SALIDA":  {"f": ("#D6EDE2", "#A9CDBB"), "s": ("#83AD9C", "#648A79"), "t": ("#EDF7F2", "#C3E2D3")},
    "CORAZÓN": {"f": ("#C9E2EE", "#93C0D8"), "s": ("#6C97AC", "#4E7487"), "t": ("#E2F0F6", "#B6D6E4")},
    "FONDO":   {"f": ("#F3DCA6", "#D8AA66"), "s": ("#AC8246", "#7C5A2A"), "t": ("#F9ECD0", "#E4C68F")},
}
NOTAS = {
    "SALIDA":  ("SALIDA", ["Lavanda · Jengibre", "Algas Marinas · Mirto"]),
    "CORAZÓN": ("CORAZÓN", ["Sal · Notas Marinas"]),
    "FONDO":   ("FONDO", ["Vainilla · Cedro · Almizcle", "Mirra"]),
}
# extrusión isométrica
SHIFT = (150.0, -86.0)

def pol(pts):
    return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)

def add_shift(pt):
    return (pt[0] + SHIFT[0], pt[1] + SHIFT[1])

parts = []
defs = ['<defs>', '<filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>']

# gradientes por losa
for nombre, pal in PAL.items():
    f1, f2 = pal["f"]; s1, s2 = pal["s"]; t1, t2 = pal["t"]
    defs.append(f'<linearGradient id="gf-{nombre}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{f1}"/><stop offset="100%" stop-color="{f2}"/></linearGradient>')
    defs.append(f'<linearGradient id="gs-{nombre}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{s1}"/><stop offset="100%" stop-color="{s2}"/></linearGradient>')
    defs.append(f'<linearGradient id="gt-{nombre}" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t1}"/><stop offset="100%" stop-color="{t2}"/></linearGradient>')
defs.append('</defs>')

# sombra suelo (bajo la losa inferior)
parts.append(f'<ellipse cx="{60:.0f}" cy="{LOSAS[0][3]+95:.0f}" rx="430" ry="60" fill="rgba(0,0,0,.45)" filter="url(#blurS)"/>')

# Dibujar de ABAJO a ARRIBA: lateral y techo de cada losa, luego frontal, luego la siguiente
# (así las losas superiores tapan lo que corresponde)
for idx, (nombre, y_top, y_bot, hw) in enumerate(LOSAS):
    pal = PAL[nombre]
    xL, xR = -hw, hw
    # ---- lateral derecho (cuadrilátero frontal-der -> trasero-der) ----
    fA = (xR, y_top); fB = (xR, y_bot)
    bA = add_shift(fA); bB = add_shift(fB)
    parts.append(f'<polygon points="{pol([fA, fB, bB, bA])}" fill="url(#gs-{nombre})"/>')
    # ---- techo (rombo: borde superior frontal desplazado) ----
    if idx == len(LOSAS) - 1:
        # losa superior: techo con pico piramidal (punta centrada)
        pA = add_shift((-hw, y_top)); pB = add_shift((hw, y_top))
        # cara superior visible (paralelogramo entre frontal sup y trasero sup) — para el pico
        mid = add_shift((0, y_top - 260))
        parts.append(f'<polygon points="{pol([(-hw, y_top), (hw, y_top), pB, mid, pA])}" fill="url(#gt-{nombre})"/>')
    else:
        pA = add_shift((-hw, y_top)); pB = add_shift((hw, y_top))
        parts.append(f'<polygon points="{pol([(-hw, y_top), (hw, y_top), pB, pA])}" fill="url(#gt-{nombre})"/>')
    # ---- frontal (rectángulo) con texto ----
    parts.append(f'<polygon points="{pol([(xL, y_top), (xR, y_top), (xR, y_bot), (xL, y_bot)])}" fill="url(#gf-{nombre})"/>')
    # borde superior frontal (línea de luz)
    parts.append(f'<line x1="{xL:.1f}" y1="{y_top:.1f}" x2="{xR:.1f}" y2="{y_top:.1f}" stroke="rgba(255,255,255,.65)" stroke-width="2.5"/>')

# ---- texto por losa (dentro del frontal, centrado, con margen) ----
for nombre, y_top, y_bot, hw in LOSAS:
    ym = (y_top + y_bot) / 2
    cap_name, lines = NOTAS[nombre]
    tcolor = "#173" if nombre != "FONDO" else "#4a2c08"
    txt = ''
    txt += f'<text x="0" y="{y_top + 34:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="21" font-weight="800" fill="rgba(15,35,40,.55)" letter-spacing="5">{cap_name}</text>'
    fs = 23 if nombre != "FONDO" else 23
    for i, ln in enumerate(lines):
        txt += f'<text x="0" y="{y_top + 74 + i*32:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="{fs}" font-weight="650" fill="{tcolor}">{ln}</text>'
    parts.append(txt)

# ---- contorno (aristas redondeadas en el frontal exterior) ----
# silueta exterior del conjunto (izquierda)
xs = sorted(p[0] for p in [(-LOSAS[0][3], LOSAS[0][1]), (LOSAS[0][3], LOSAS[0][1]), (-LOSAS[2][3], LOSAS[2][1]), (LOSAS[2][3], LOSAS[2][1])])
# aristas laterales izquierda y derecha del conjunto
parts.append(f'<path d="M {-LOSAS[2][3]:.1f} {LOSAS[2][1]:.1f} L {-LOSAS[0][3]:.1f} {LOSAS[0][3-1]:.1f} L {-LOSAS[0][3]:.1f} {LOSAS[0][2]:.1f}" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="4" stroke-linejoin="round"/>')
parts.append(f'<path d="M {LOSAS[2][3]:.1f} {LOSAS[2][1]:.1f} L {LOSAS[0][3]:.1f} {LOSAS[0][1]:.1f} L {LOSAS[0][3]:.1f} {LOSAS[0][2]:.1f}" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="4" stroke-linejoin="round"/>')
# aristas del perfil trasero (volumen)
parts.append(f'<path d="M {LOSAS[2][3]+SHIFT[0]:.1f} {LOSAS[2][1]+SHIFT[1]:.1f} L {LOSAS[0][3]+SHIFT[0]:.1f} {LOSAS[0][1]+SHIFT[1]:.1f}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="2" stroke-linejoin="round"/>')

# límites
allx = [-LOSAS[0][3], LOSAS[0][3], LOSAS[0][3] + SHIFT[0], -LOSAS[2][3], LOSAS[2][3]]
ally = [LOSAS[2][1], LOSAS[0][2], LOSAS[0][2] + SHIFT[1] + 20, LOSAS[2][1] - 60]
minx, maxx = min(allx) - 60, max(allx) + 60
miny, maxy = min(ally) - 40, max(ally) + 40
Wv, Hv = maxx - minx, maxy - miny

svg = (f'<svg width="{Wv:.0f}" height="{Hv:.0f}" viewBox="{minx:.0f} {miny:.0f} {Wv:.0f} {Hv:.0f}" '
       f'style="filter:drop-shadow(0 24px 44px rgba(0,0,0,.38));">' + "".join(defs) + "".join(parts) + "</svg>")

html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter','Helvetica Neue',Arial,sans-serif; }}
  .slide {{ width:1080px; height:1350px; position:relative; overflow:hidden;
    background:radial-gradient(1100px 760px at 30% -10%, #f3efe6 0%, #e9e3d3 55%, #dcd3bd 100%); }}
  .content {{ position:absolute; inset:0; padding:54px 84px 46px; display:flex; flex-direction:column; }}
  .marca {{ display:flex; align-items:center; gap:10px; }}
  .marca .logo {{ width:36px; height:36px; border-radius:50%; background:#1a1a1a; color:#F5EFE6;
    display:flex; align-items:center; justify-content:center; font-weight:800; font-size:14px; }}
  .marca .nombre {{ font-weight:800; font-size:16px; color:#1a1a1a; letter-spacing:.3px; }}
  .marca .nombre span {{ color:#C77B2E; }}
  .titulo {{ font-size:40px; font-weight:800; color:#1a1a1a; letter-spacing:-1.1px; line-height:1.1; margin-top:20px; }}
  .titulo .accent {{ color:#C77B2E; }}
  .sub {{ font-size:17px; color:#6b6b60; font-weight:500; margin-top:8px; }}
  .sub b {{ color:#1a1a1a; }}
  .escena {{ flex:1; display:flex; align-items:center; justify-content:center; min-height:0; }}
  .pie {{ display:flex; align-items:center; justify-content:space-between; margin-top:6px; }}
  .pie .tec {{ font-size:12px; color:#99998a; }}
  .pie .tec b {{ color:#555; }}
  .chip {{ background:rgba(199,123,46,.14); border:1px solid rgba(199,123,46,.4); color:#C77B2E;
    font-size:12px; font-weight:800; padding:7px 15px; border-radius:20px; letter-spacing:.6px; }}
</style></head>
<body>
<div class="slide">
  <div class="content">
    <div class="marca"><div class="logo">JL</div>
      <div class="nombre">JOKO <span>LAB</span> · PRUEBA DE VOLUMEN</div></div>
    <div class="titulo">Pirámide olfativa con <span class="accent">volumen</span><br>Acqua di Sale · Profumum Roma</div>
    <div class="sub">Tres losas apiladas — <b>cada nota dentro de su capa, sin desbordes</b></div>
    <div class="escena">{svg}</div>
    <div class="pie">
      <div class="tec">SVG 2.5D · losas con techo y lateral · datos reales BD del lab</div>
      <div class="chip">PRUEBA · PIRÁMIDE OLFATIVA 3D</div>
    </div>
  </div>
</div>
</body></html>'''

out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-olfativa-3d/piramide_olfativa_v2.html'
open(out, 'w').write(html)
print('OK', out)
