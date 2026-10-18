#!/usr/bin/env python3
"""Pirámide olfativa 3D con volumen — datos REALES de Acqua di Sale (Profumum Roma).
Frontal plano legible (notas) + extrusión lateral isométrica = cuerpo/volumen.
Capas: salida (fresco) -> corazón (salino) -> fondo (cálido): la evolución del perfume.
"""
import math

# ---- geometría del frontal ----
cx, ty = 0.0, -400.0     # punta
W, by = 300.0, 240.0     # media base y base inferior
# reparto vertical de capas (% de altura desde punta)
CAPAS = [
    ("SALIDA",  0.00, 0.30),
    ("CORAZÓN", 0.30, 0.62),
    ("FONDO",   0.62, 1.00),
]
# paleta por capa: frontal iluminado (grad 2 tonos) y lateral sombreado (2 tonos)
PALETA = {
    "SALIDA":  {"f": ("#D6EDE2", "#A3CDB9"), "s": ("#7FA999", "#5E8A7A")},   # fresco: lavanda, algas, mirto
    "CORAZÓN": {"f": ("#C9E2EE", "#8FBFD6"), "s": ("#6996AC", "#4E7487")},   # salino: sal, notas marinas
    "FONDO":   {"f": ("#F3DCA6", "#D6A763"), "s": ("#A97F43", "#7C5A2A")},   # cálido: vainilla, cedro, almizcle, mirra
}
NOTAS = {
    "SALIDA":  ["Lavanda · Jengibre", "Algas · Mirto"],
    "CORAZÓN": ["Sal · Notas Marinas"],
    "FONDO":   ["Vainilla · Cedro", "Almizcle · Mirra"],
}
# extrusión isométrica (dx>0, dy<0, relación tan30)
SHIFT = (118.0, -68.0)

def x_at(y):
    return cx + W * (y - ty) / (by - ty)

def lerp(p1, p2, u):
    return (p1[0] + (p2[0] - p1[0]) * u, p1[1] + (p2[1] - p1[1]) * u)

def pol(pts):
    return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)

parts = []

# niveles y (y0 arriba, y1 abajo de cada capa)
niv = [(ty + f * (by - ty), ty + g * (by - ty)) for _, f, g in CAPAS]

# ---- CUELLO/CUERPO: dibujar primero la extrusión lateral completa por capa (de atrás a delante) ----
for (nombre, f0, f1), (ya, yb) in zip(CAPAS, niv):
    pal = PALETA[nombre]
    # puntos frontales del borde DERECHO entre ya..yb
    pA = (x_at(ya), ya); pB = (x_at(yb), yb)
    # puntos traseros (perfil extruido)
    pA2 = (pA[0] + SHIFT[0], pA[1] + SHIFT[1])
    pB2 = (pB[0] + SHIFT[0], pB[1] + SHIFT[1])
    # cara lateral derecha (cuadrilátero: frontal arriba-der, trasero arriba-der, trasero abajo, frontal abajo)
    parts.append(f'<polygon points="{pol([pA, pB, pB2, pA2])}" fill="url(#grad-{nombre}-lateral)"/>')

# ---- techo (cara superior del sólido: desde la punta al perfil trasero) ----
# cara superior = triángulo punta frontal -> punta trasera -> (punto superior del perfil: borde izq? )
# En la vista 3/4 con extrusión a la derecha-arriba, la cara superior visible conecta
# la arista izquierda del frontal con la izquierda del trasero: solo visible si inclinamos.
# Para esta proyección (frontal erguido + profundidad hacia atrás-arriba), la cara superior
# NO es visible (el frontal la tapa). La dibujamos ligeramente asomando por la punta.

# ---- FRONTAL: polígonos por capa con texto ----
for (nombre, f0, f1), (ya, yb) in zip(CAPAS, niv):
    pal = PALETA[nombre]
    # frontal izquierda y derecha
    xa, xb = x_at(ya), x_at(yb)
    if f0 == 0.0:
        pts_f = [(cx, ty), (xb, yb), (-xb, yb)]   # triángulo superior (salida) o trapecio
        if ya == ty:
            pts_f = [(cx, ty), (x_at(yb), yb), (-x_at(yb), yb)]
        else:
            pts_f = [(x_at(ya), ya), (x_at(yb), yb), (-x_at(yb), yb), (-x_at(ya), ya)]
    else:
        pts_f = [(xa, ya), (xb, yb), (-xb, yb), (-xa, ya)]
    parts.append(f'<polygon points="{pol(pts_f)}" fill="url(#grad-{nombre}-frontal)"/>')
    # línea de separación inferior de capa
    parts.append(f'<line x1="{-x_at(yb):.1f}" y1="{yb:.1f}" x2="{x_at(yb):.1f}" y2="{yb:.1f}" stroke="rgba(20,40,45,.35)" stroke-width="2.5"/>')

# ---- texto por capa (frontal, centrado, legible) ----
for (nombre, f0, f1), (ya, yb) in zip(CAPAS, niv):
    ym = (ya + yb) / 2
    tcolor = "#123" if nombre != "FONDO" else "#4a2c08"
    lines = NOTAS[nombre]
    txt = ""
    # nombre capa (diminuto, espaciado)
    txt += f'<text x="{cx:.0f}" y="{ym-26:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="23" font-weight="800" fill="rgba(20,40,45,.55)" letter-spacing="4">{nombre}</text>'
    # notas (2 líneas max)
    lh = 0
    for i, ln in enumerate(lines):
        txt += f'<text x="{cx:.0f}" y="{ym+6+i*30:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="21" font-weight="600" fill="{tcolor}">{ln}</text>'
        lh = i
    parts.append(txt)

# ---- contorno del sólido (aristas redondeadas: linejoin round) ----
parts.append(f'<path d="M {cx:.1f} {ty:.1f} L {-W:.1f} {by:.1f} L {W:.1f} {by:.1f} Z" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="4" stroke-linejoin="round"/>')
# arista del perfil trasero (derecha) para dar profundidad
parts.append(f'<path d="M {cx+SHIFT[0]:.1f} {ty+SHIFT[1]:.1f} L {W+SHIFT[0]:.1f} {by+SHIFT[1]:.1f}" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="2" stroke-linejoin="round"/>')

# ---- sombra de suelo ----
sx, sy = cx + 60, by + 46
parts.append(f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="300" ry="52" fill="rgba(0,0,0,.5)" filter="url(#blurS)"/>')

# ---- defs gradientes ----
defs = ['<defs>', '<filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>']
for nombre, pal in PALETA.items():
    f1, f2 = pal["f"]; s1, s2 = pal["s"]
    defs.append(f'<linearGradient id="grad-{nombre}-frontal" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{f1}"/><stop offset="100%" stop-color="{f2}"/></linearGradient>')
    defs.append(f'<linearGradient id="grad-{nombre}-lateral" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{s1}"/><stop offset="100%" stop-color="{s2}"/></linearGradient>')
defs.append('</defs>')

# límites
xs = [cx, -W, W, cx + SHIFT[0], W + SHIFT[0]]
ys = [ty, by, by + SHIFT[1] + 10]
minx, maxx = min(xs) - 80, max(xs) + 80
miny, maxy = min(ys) - 60, max(ys) + 70
Wv, Hv = maxx - minx, maxy - miny

svg = (f'<svg width="{Wv:.0f}" height="{Hv:.0f}" viewBox="{minx:.0f} {miny:.0f} {Wv:.0f} {Hv:.0f}" '
       f'style="filter:drop-shadow(0 22px 40px rgba(0,0,0,.4));">' + "".join(defs) + "".join(parts) + "</svg>")

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
  .etiqueta {{ position:absolute; font-size:14px; color:#8a8a7c; font-weight:600; letter-spacing:.4px; }}
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
    <div class="sub">De la espuma fría al fondo cálido — <b>las 3 capas con cuerpo, no un triángulo plano</b></div>
    <div class="escena">{svg}</div>
    <div class="pie">
      <div class="tec">SVG 2.5D · frontal legible + cuerpo lateral · datos reales de la BD del lab</div>
      <div class="chip">PRUEBA · PIRÁMIDE OLFATIVA 3D</div>
    </div>
  </div>
</div>
</body></html>'''

out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-olfativa-3d/piramide_olfativa_v1.html'
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write(html)
print('OK', out)
