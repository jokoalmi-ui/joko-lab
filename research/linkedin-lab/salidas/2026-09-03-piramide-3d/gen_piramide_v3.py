#!/usr/bin/env python3
"""Genera pirámide 3D isométrica SVG v3 — bloques individuales con tono propio,
bisel de luz por ladrillo, contorno de aristas redondeadas, piramidión.
Proyección isométrica: X=(x-y)*c, Y=(x+y)*s - z. Base (±a,±a,0), punta (0,0,h).
"""
import math

c = math.cos(math.radians(30))
s = math.sin(math.radians(30))
SC = 1.12

def iso(x, y, z):
    return (SC * (x - y) * c, SC * ((x + y) * s - z))

# ---- utilidades de color ----
def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_rgb(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def mix_stops(stops, t):
    """stops: [(pos, hex)] ordenados; interpola en t∈[0,1]."""
    if t <= stops[0][0]:
        return hex2rgb(stops[0][1])
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if t <= p1:
            return lerp_rgb(hex2rgb(c0), hex2rgb(c1), (t - p0) / (p1 - p0))
    return hex2rgb(stops[-1][1])

def rgb2hex(c):
    return '#{:02X}{:02X}{:02X}'.format(*c)

def vary(rgb, seed):
    """Variación tonal determinista por bloque (±5 por canal)."""
    v = ((seed * 2654435761) % 11) - 5
    return tuple(max(0, min(255, ch + v)) for ch in rgb)

def lerp(p1, p2, u):
    return (p1[0] + (p2[0] - p1[0]) * u, p1[1] + (p2[1] - p1[1]) * u)

def poly(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

# ---- parámetros ----
a, h = 300.0, 520.0
N = 18          # hiladas
B = 10          # bloques por banda
pts = { (x, y): iso(x, y, 0) for x in (-a, a) for y in (-a, a) }
P = iso(0, 0, h)
F, I, D, A = pts[(a, a)], pts[(-a, a)], pts[(a, -a)], pts[(-a, -a)]

# secciones verticales (u: 0 punta → 1 base), ligera no-linealidad
us = [(k / N) ** 1.10 for k in range(N + 1)]
secI = [lerp(P, I, u) for u in us]
secF = [lerp(P, F, u) for u in us]
secD = [lerp(P, D, u) for u in us]

# gradientes de luz por cara (de arriba claro a abajo más saturado)
LIGHT = [(0.0, '#FFF3D0'), (0.5, '#F0C97C'), (1.0, '#DEA658')]   # cara iluminada
DARK  = [(0.0, '#CD9C58'), (0.5, '#9A6B31'), (1.0, '#6B4720')]   # cara sombra

parts = []

def draw_face(secL, secR, palette):
    """Dibuja bloques individuales entre las aristas secL (izquierda de la cara) y secR."""
    for k in range(N):
        A1, B1 = secL[k], secR[k]     # sección superior (más cerca de punta)
        A2, B2 = secL[k + 1], secR[k + 1]
        u_mid = (us[k] + us[k + 1]) / 2
        off = (k % 2) * 0.5
        step = 1.0 / B
        for j in range(B):
            v0 = j * step + off * step
            v1 = v0 + step
            v0, v1 = max(0.0, v0), min(1.0, v1)
            p1 = lerp(A1, B1, v0); p2 = lerp(A1, B1, v1)
            p3 = lerp(A2, B2, v1); p4 = lerp(A2, B2, v0)
            base_c = mix_stops(palette, u_mid)
            c = vary(base_c, k * 131 + j * 17 + (13 if palette is DARK else 0))
            parts.append(f'<polygon points="{poly([p1,p2,p3,p4])}" fill="{rgb2hex(c)}"/>')
            # bisel de luz en la arista superior del ladrillo
            parts.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="rgba(255,255,235,.30)" stroke-width="1.6"/>')
            # sombra en la arista inferior (da relieve)
            parts.append(f'<line x1="{p4[0]:.1f}" y1="{p4[1]:.1f}" x2="{p3[0]:.1f}" y2="{p3[1]:.1f}" stroke="rgba(40,20,0,.32)" stroke-width="1.8"/>')
        # junta de hilada (entre bandas) más marcada
        parts.append(f'<line x1="{A1[0]:.1f}" y1="{A1[1]:.1f}" x2="{B1[0]:.1f}" y2="{B1[1]:.1f}" stroke="rgba(50,28,2,.5)" stroke-width="2.2"/>')

# sombra en suelo
parts.append(f'<ellipse cx="{F[0]:.0f}" cy="{F[1]+26:.0f}" rx="{abs(I[0]-D[0])/2+50:.0f}" ry="130" fill="rgba(0,0,0,.5)" filter="url(#blurS)"/>')

# CARA IZQUIERDA (iluminada)
draw_face(secI, secF, LIGHT)
# CARA DERECHA (sombra)
draw_face(secF, secD, DARK)

# ---- contorno redondeado (aristas suaves, linejoin round, trazo del color de cara) ----
# arista izquierda completa P->I->F (luz)
parts.append(f'<path d="M {P[0]:.1f} {P[1]:.1f} L {I[0]:.1f} {I[1]:.1f} L {F[0]:.1f} {F[1]:.1f}" fill="none" stroke="#F4DCA6" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity=".85"/>')
# arista derecha P->D->F (sombra)
parts.append(f'<path d="M {P[0]:.1f} {P[1]:.1f} L {D[0]:.1f} {D[1]:.1f} L {F[0]:.1f} {F[1]:.1f}" fill="none" stroke="#5d3c17" stroke-width="5.5" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>')
# arista central con brillo (redondeada: trazo grueso degradado + línea fina clara)
parts.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{F[0]:.1f}" y2="{F[1]:.1f}" stroke="rgba(255,236,180,.28)" stroke-width="13" stroke-linecap="round"/>')
parts.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{F[0]:.1f}" y2="{F[1]:.1f}" stroke="rgba(255,250,235,.92)" stroke-width="3.4" stroke-linecap="round"/>')
# base delantera (I->F->D) redondeada
parts.append(f'<path d="M {I[0]:.1f} {I[1]:.1f} L {F[0]:.1f} {F[1]:.1f} L {D[0]:.1f} {D[1]:.1f}" fill="none" stroke="#241402" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" opacity=".55"/>')

# ---- piramidión (remate dorado redondeado de la punta) ----
px, py = P
pr = 13
parts.append(f'<polygon points="{px-pr:.1f},{py-2:.1f} {px:.1f},{py-pr-7:.1f} {px+pr:.1f},{py-2:.1f} {px:.1f},{py+6:.1f}" fill="url(#capstone)" stroke="#FFE9B8" stroke-width="1.6" stroke-linejoin="round"/>')
parts.append(f'<ellipse cx="{px:.1f}" cy="{py-2:.1f}" rx="10" ry="4" fill="rgba(255,255,255,.75)" opacity=".6"/>')
# halo suave en la punta
parts.append(f'<circle cx="{px:.1f}" cy="{py-6:.1f}" r="26" fill="rgba(255,220,150,.14)" filter="url(#blurS)"/>')

# límites
xs = [p[0] for p in [P, I, D, F, A]]
ys = [p[1] for p in [P, I, D, F, A]]
minx, maxx = min(xs) - 70, max(xs) + 70
miny, maxy = min(ys) - 90, max(ys) + 150
W, H = maxx - minx, maxy - miny

svg = f'''<svg width="{W:.0f}" height="{H:.0f}" viewBox="{minx:.0f} {miny:.0f} {W:.0f} {H:.0f}" style="filter:drop-shadow(0 24px 44px rgba(0,0,0,.5));">
<defs>
  <filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
  <linearGradient id="capstone" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFF3CE"/><stop offset="100%" stop-color="#E3B25F"/>
  </linearGradient>
</defs>
{''.join(parts)}
</svg>'''

html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter','Helvetica Neue',Arial,sans-serif; }}
  .slide {{ width:1080px; height:1350px; position:relative; overflow:hidden;
    background:radial-gradient(1200px 800px at 50% -10%, #2a3550 0%, #1a2035 45%, #10131f 100%); }}
  .stars {{ position:absolute; inset:0; opacity:.5;
    background-image:
      radial-gradient(1.2px 1.2px at 120px 90px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 340px 60px, #fff 50%, transparent 51%),
      radial-gradient(1.4px 1.4px at 520px 140px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 700px 70px, #fff 50%, transparent 51%),
      radial-gradient(1.2px 1.2px at 900px 120px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 980px 50px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 60px 220px, #fff 50%, transparent 51%),
      radial-gradient(1.2px 1.2px at 260px 300px, rgba(255,255,255,.6) 50%, transparent 51%),
      radial-gradient(1px 1px at 1000px 280px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 150px 400px, rgba(255,255,255,.5) 50%, transparent 51%),
      radial-gradient(1.2px 1.2px at 820px 380px, #fff 50%, transparent 51%),
      radial-gradient(1px 1px at 460px 200px, rgba(255,255,255,.4) 50%, transparent 51%),
      radial-gradient(1px 1px at 640px 320px, rgba(255,255,255,.35) 50%, transparent 51%),
      radial-gradient(1px 1px at 240px 520px, rgba(255,255,255,.3) 50%, transparent 51%),
      radial-gradient(1px 1px at 890px 470px, rgba(255,255,255,.3) 50%, transparent 51%); }}
  .content {{ position:absolute; inset:0; padding:52px 80px 42px; display:flex; flex-direction:column; }}
  .marca {{ display:flex; align-items:center; gap:10px; }}
  .marca .logo {{ width:34px; height:34px; border-radius:50%; background:#FFC55A;
    display:flex; align-items:center; justify-content:center; color:#1a2035;
    font-weight:800; font-size:14px; box-shadow:0 0 18px rgba(255,197,90,.4); }}
  .marca .nombre {{ font-weight:700; font-size:15px; color:#cfd6e8; letter-spacing:.4px; }}
  .marca .nombre span {{ color:#FFC55A; }}
  .titulo {{ font-size:42px; font-weight:800; color:#f5f1e6; letter-spacing:-1.2px;
    line-height:1.12; margin-top:22px; }}
  .titulo .accent {{ color:#FFC55A; }}
  .sub {{ font-size:17px; color:#9aa3bd; font-weight:500; margin-top:8px; line-height:1.5; }}
  .sub b {{ color:#cfd6e8; }}
  .escena {{ flex:1; position:relative; display:flex; align-items:center; justify-content:center; min-height:0; padding-top:6px; }}
  .pie {{ display:flex; align-items:center; justify-content:space-between; margin-top:6px; }}
  .pie .tec {{ font-size:12px; color:#77809c; letter-spacing:.3px; }}
  .pie .tec b {{ color:#cfd6e8; font-weight:600; }}
  .chip {{ background:rgba(255,197,90,.12); border:1px solid rgba(255,197,90,.35);
    color:#FFC55A; font-size:12px; font-weight:700; padding:7px 15px; border-radius:20px; letter-spacing:.5px; }}
</style></head>
<body>
<div class="slide">
  <div class="stars"></div>
  <div class="content">
    <div class="marca"><div class="logo">JL</div>
      <div class="nombre">JOKO <span>LAB</span> · PRUEBA DE VOLUMEN 3D</div></div>
    <div class="titulo">Pirámide <span class="accent">isométrica</span><br>ladrillo a ladrillo</div>
    <div class="sub">18 hiladas · 180 bloques con tono propio · aristas redondeadas · <b>0&nbsp;€ · 100% local</b></div>
    <div class="escena">{svg}</div>
    <div class="pie">
      <div class="tec">SVG generado por script · luz/sombra por cara · bisel de luz por ladrillo</div>
      <div class="chip">PRUEBA · VOLUMEN 2.5D</div>
    </div>
  </div>
</div>
</body></html>'''

out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-3d/piramide_v3.html'
open(out, 'w').write(html)
print('OK', out, f'viewBox {minx:.0f} {miny:.0f} {W:.0f} {H:.0f}')
