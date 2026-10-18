#!/usr/bin/env python3
"""Pirámide de Kelsen v2 — silueta TRIANGULAR REAL. Cada nivel = tajada horizontal
del triángulo (trapecio apilado, mismo centro X), texto dentro + volumen por
extrusión lateral del perfil completo (como bloque sólido). Niveles UNO ENCIMA DE OTRO.
Contenido de ejemplo (la FORMA es lo validado). 6 tajadas.
"""
import os, math

# ---- triángulo base ----
cx, ty = 0.0, -430.0     # punta
W, by = 470.0, 230.0     # media base y base
H = by - ty
# 6 tajadas de ALTURA IGUAL (franjas del triángulo, como la imagen)
N = 6
CAPAS = [
    # texto, color frontal f1->f2, lateral s1->s2, fs
    ("CONSTITUCIÓN",              ("#E8554D", "#C73A33"), ("#9E2B25", "#7A1F1A"), 17),
    ("TRATADOS INTERNACIONALES",  ("#C05FB0", "#A24492"), ("#7D3672", "#5F2757"), 19),
    ("LEYES",                     ("#4E6FD8", "#3A53B4"), ("#2B3D87", "#1E2C66"), 21),
    ("DECRETOS LEGISLATIVOS",     ("#4FA36B", "#3C8557"), ("#2B6240", "#1F4A30"), 21),
    ("RESOLUCIONES MINISTERIALES",("#E0A83C", "#C98F28"), ("#9C6D1D", "#775215"), 21),
    ("OTRAS RESOLUCIONES",        ("#E87B3E", "#D06128"), ("#A0491D", "#7C3714"), 22),
]
SHIFT = (210.0, -122.0)   # extrusión isométrica del PERFIL (bloque sólido)

def x_at(y):   # media anchura de la pirámide a esa altura (coordenada X del borde izq/der)
    return W * (y - ty) / H

def pol(pts):
    return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)

def sh(pt):
    return (pt[0] + SHIFT[0], pt[1] + SHIFT[1])

# niveles y: ty = tope tajada 1, luego reparto igual
ys = [ty + i * H / N for i in range(N + 1)]   # ys[0]=punta ... ys[N]=base

parts, defs = [], ['<defs>', '<filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>']
for i in range(N):
    f1, f2 = CAPAS[i][1]; s1, s2 = CAPAS[i][2]
    defs.append(f'<linearGradient id="gf{i}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{f1}"/><stop offset="100%" stop-color="{f2}"/></linearGradient>')
    defs.append(f'<linearGradient id="gs{i}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{s1}"/><stop offset="100%" stop-color="{s2}"/></linearGradient>')
defs.append('</defs>')

# ---- LATERAL DERECHO CONVERGENTE (pirámide real: profundidad -> 0 en el pico) ----
# La cara lateral derecha es el triángulo P -> der_base_F -> der_base_T (trasero en la
# base). A una altura y, u=(y-ty)/H: la sección corta la arista frontal en (x_at(y), y)
# y la arista trasera en t(y) = P + (der_T - P)*u. Ambos comparten P -> el lateral
# CONVERGE al pico (sin cresta Toblerone). Cada tajada del lateral = cuadrilátero.
SHIFT_BASE = (SHIFT[0], SHIFT[1])   # desplazamiento APLICADO SOLO a la base (by)

def trasero_at(y):
    """Punto de la arista trasera derecha a la altura y (converge a P cuando y->ty)."""
    u = (y - ty) / H if y > ty else 0.0
    return (cx + (W + SHIFT_BASE[0] - cx) * u, ty + (by + SHIFT_BASE[1] - ty) * u)

for i in range(N):
    ya, yb = ys[i], ys[i+1]
    f_top = (x_at(ya), ya)
    f_bot = (x_at(yb), yb)
    b_top = trasero_at(ya)
    b_bot = trasero_at(yb)
    pts = [f_top, f_bot, b_bot, b_top]
    parts.append(f'<polygon points="{pol(pts)}" fill="url(#gs{i})"/>')
    if i == 0:
        # arista superior del lateral: en la tajada 1 degenera en P (pico único)
        pass

# ---- FRONTAL: tajadas del triángulo (trapecios apilados, silueta triangular) ----
for i in range(N):
    ya, yb = ys[i], ys[i+1]
    xa, xb = x_at(ya), x_at(yb)
    if i == 0:
        pts_f = [(cx, ty), (xb, yb), (-xb, yb)]
    else:
        pts_f = [(-xa, ya), (xa, ya), (xb, yb), (-xb, yb)]
    parts.append(f'<polygon points="{pol(pts_f)}" fill="url(#gf{i})"/>')
    # línea divisoria inferior (marca el escalón entre tajadas)
    if i < N - 1:
        parts.append(f'<line x1="{-x_at(ys[i+1]):.1f}" y1="{ys[i+1]:.1f}" x2="{x_at(ys[i+1]):.1f}" y2="{ys[i+1]:.1f}" stroke="rgba(15,20,30,.55)" stroke-width="4"/>')
        # línea divisoria también en el lateral (profundidad, converge al pico)
        tb = trasero_at(ys[i+1])
        parts.append(f'<line x1="{x_at(ys[i+1]):.1f}" y1="{ys[i+1]:.1f}" x2="{tb[0]:.1f}" y2="{tb[1]:.1f}" stroke="rgba(0,0,0,.35)" stroke-width="3"/>')

# ---- texto por tajada (centrado, en la franja del triángulo; autoescala para caber) ----
for i in range(N):
    nombre, _, _, fs = CAPAS[i]
    ya, yb = ys[i], ys[i+1]
    ym = (ya + yb) / 2
    xm = x_at(ym)          # media anchura de la tajada a la altura del texto
    # caber: estimar ancho del texto ~ 0.62*fs por char; si no cabe, bajar fs
    f = fs
    while len(nombre) * f * 0.60 > xm * 1.7 and f > 9:
        f -= 1
    parts.append(f'<text x="{cx:.0f}" y="{ym+ f*0.35:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="{f}" font-weight="800" fill="#fff" letter-spacing="1">{nombre}</text>')

# ---- arista central (punta -> base) con brillo suave para reforzar volumen ----
parts.append(f'<line x1="{cx:.1f}" y1="{ty:.1f}" x2="{cx:.1f}" y2="{by:.1f}" stroke="rgba(255,255,255,.35)" stroke-width="2"/>')

# ---- contorno exterior de la silueta (redondeado) ----
parts.append(f'<path d="M {cx:.1f} {ty:.1f} L {-W:.1f} {by:.1f} L {W:.1f} {by:.1f} Z" fill="none" stroke="rgba(255,255,255,.9)" stroke-width="5" stroke-linejoin="round"/>')
# perfil trasero (volumen): arista trasera derecha converge a la punta P (pico único)
tbase = trasero_at(by)
parts.append(f'<path d="M {cx:.1f} {ty:.1f} L {tbase[0]:.1f} {tbase[1]:.1f}" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="3" stroke-linejoin="round"/>')
parts.append(f'<path d="M {W:.1f} {by:.1f} L {tbase[0]:.1f} {tbase[1]:.1f}" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="2.5" stroke-linejoin="round"/>')

# ---- grupos laterales (rotados) ----
gx = -W - 150
parts.append(f'<text x="{gx:.0f}" y="{-60:.0f}" transform="rotate(-90 {gx:.0f} {-60:.0f})" text-anchor="middle" font-family="Inter,Arial" font-size="22" font-weight="800" fill="rgba(199,123,46,.95)" letter-spacing="7">ACTOS LEGISLATIVOS</text>')
parts.append(f'<text x="{gx:.0f}" y="{220:.0f}" transform="rotate(-90 {gx:.0f} {220:.0f})" text-anchor="middle" font-family="Inter,Arial" font-size="22" font-weight="800" fill="rgba(120,90,40,.9)" letter-spacing="7">ACTOS ADMINISTRATIVOS</text>')

# separación entre bloque legislativo (0-2) y administrativo (3-5) con línea blanca
y_sep = ys[3]
parts.append(f'<line x1="{-x_at(y_sep)-10:.1f}" y1="{y_sep:.0f}" x2="{x_at(y_sep)+10:.1f}" y2="{y_sep:.0f}" stroke="#fff" stroke-width="5" stroke-dasharray="14 10"/>')
tb_sep = trasero_at(y_sep)
parts.append(f'<line x1="{x_at(y_sep):.1f}" y1="{y_sep:.0f}" x2="{tb_sep[0]:.1f}" y2="{tb_sep[1]:.1f}" stroke="rgba(255,255,255,.85)" stroke-width="4" stroke-dasharray="14 10"/>')

# ---- sombra suelo ----
parts.append(f'<ellipse cx="{cx+90:.0f}" cy="{by+60:.0f}" rx="{W*0.75:.0f}" ry="52" fill="rgba(0,0,0,.5)" filter="url(#blurS)"/>')

xs = [cx - W, cx + W + SHIFT[0], cx + SHIFT[0], gx - 40, cx]
ys_all = [ty - 10, by + 20, by + SHIFT[1] + 30, ty + SHIFT[1] - 30]
minx, maxx = min(xs) - 60, max(xs) + 60
miny, maxy = min(ys_all) - 30, max(ys_all) + 70
Wv, Hv = maxx - minx, maxy - miny

svg = (f'<svg width="{Wv:.0f}" height="{Hv:.0f}" viewBox="{minx:.0f} {miny:.0f} {Wv:.0f} {Hv:.0f}" '
       f'style="filter:drop-shadow(0 28px 50px rgba(0,0,0,.38));">' + "".join(defs) + "".join(parts) + "</svg>")

html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter','Helvetica Neue',Arial,sans-serif; }}
  .slide {{ width:1080px; height:1350px; position:relative; overflow:hidden;
    background:radial-gradient(1100px 760px at 30% -10%, #f6f2ea 0%, #ece5d6 55%, #ddd2ba 100%); }}
  .content {{ position:absolute; inset:0; padding:52px 76px 44px; display:flex; flex-direction:column; }}
  .marca {{ display:flex; align-items:center; gap:10px; }}
  .marca .logo {{ width:36px; height:36px; border-radius:50%; background:#1a1a1a; color:#F5EFE6;
    display:flex; align-items:center; justify-content:center; font-weight:800; font-size:14px; }}
  .marca .nombre {{ font-weight:800; font-size:16px; color:#1a1a1a; letter-spacing:.3px; }}
  .marca .nombre span {{ color:#C77B2E; }}
  .titulo {{ font-size:42px; font-weight:800; color:#1a1a1a; letter-spacing:-1.1px; line-height:1.1; margin-top:18px; }}
  .titulo .accent {{ color:#C77B2E; }}
  .sub {{ font-size:17px; color:#6b6b60; font-weight:500; margin-top:8px; }}
  .sub b {{ color:#1a1a1a; }}
  .escena {{ flex:1; display:flex; align-items:center; justify-content:center; min-height:0; }}
  .pie {{ display:flex; align-items:center; justify-content:space-between; margin-top:4px; }}
  .pie .tec {{ font-size:12px; color:#99998a; }}
  .pie .tec b {{ color:#555; }}
  .chip {{ background:rgba(199,123,46,.14); border:1px solid rgba(199,123,46,.4); color:#C77B2E;
    font-size:12px; font-weight:800; padding:7px 15px; border-radius:20px; letter-spacing:.6px; }}
</style></head>
<body>
<div class="slide">
  <div class="content">
    <div class="marca"><div class="logo">JL</div>
      <div class="nombre">JOKO <span>LAB</span> · DEMO DE FORMA</div></div>
    <div class="titulo">Pirámide <span class="accent">triangular</span> · 6 tajadas</div>
    <div class="sub">Niveles apilados con silueta de pirámide — <b>texto centrado en cada tajada</b>, volumen lateral</div>
    <div class="escena">{svg}</div>
    <div class="pie">
      <div class="tec">SVG 2.5D · tajadas del triángulo · demo de FORMA (contenido: Kelsen simplificado)</div>
      <div class="chip">DEMO · VOLUMEN 2.5D</div>
    </div>
  </div>
</div>
</body></html>'''

out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-escalonada-kelsen/demo_kelsen_triangular.html'
open(out, 'w').write(html)
print('OK', out)
