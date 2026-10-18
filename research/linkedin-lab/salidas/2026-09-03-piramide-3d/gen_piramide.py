#!/usr/bin/env python3
"""Genera pirámide 3D isométrica SVG con detalle de bloques (prueba volumen 2.5D).
Proyección isométrica: X=(x-y)*c, Y=(x+y)*s - z  (c=cos30, s=sin30).
Pirámide: base cuadrada (±a,±a,0), punta (0,0,h).
Salida: HTML completo listo para render Chrome headless.
"""
import math, os

c = math.cos(math.radians(30))
s = math.sin(math.radians(30))
SC = 1.12  # escala global

def iso(x, y, z):
    return (SC * (x - y) * c, SC * ((x + y) * s - z))

# parámetros de la pirámide (3D)
a = 300.0   # media base
h = 520.0   # altura

# vértices base: (+-a, +-a, 0)
# nombre: FRENTE = (a,a) proyectado abajo (y+ pantalla)... cuidado con orientación:
# (x,y)->X=(x-y)c ; Y=(x+y)s. Frente al espectador: y mayor => elegimos y = +a como "hacia abajo"? 
# En nuestra iso, Y crece con (x+y), así que el punto con x+y máximo es el más bajo en pantalla.
# Para que el vértice "frontal" (0,a) en 3D quede bajo y centrado: (0,a) -> X=-a*c, Y=a*s (izquierda-abajo).
# Preferimos orientación donde el frente sea (a,a): X=0,Y=2a*s (abajo-centro) y la junta punta->frente quede
# vertical central. Esquinas: E1=(a,a) frente abajo centro; E2=(-a,a) izquierda; E3=(a,-a) derecha; E4=(-a,-a) atrás arriba.
pts = {}
for x in (-a, a):
    for y in (-a, a):
        pts[(x, y)] = iso(x, y, 0)
P = iso(0, 0, h)

# Esquinas en pantalla
F = pts[(a, a)]     # frente (abajo, centro)
I = pts[(-a, a)]    # izquierda
D = pts[(a, -a)]    # derecha
A = pts[(-a, -a)]   # atrás (arriba)

def lerp(p1, p2, u):
    return (p1[0] + (p2[0] - p1[0]) * u, p1[1] + (p2[1] - p1[1]) * u)

def poly_str(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

N = 14  # hiladas
bloques_por_banda = 8

# --- Construcción de la malla de la cara delantera-izquierda y delantera-derecha ---
# Secciones horizontales en u_k (0 punta -> 1 base), repartidas con ligera no-linealidad
us = [ (k / N) ** 1.12 for k in range(N + 1) ]
# Puntos de sección k sobre las aristas
secI = [lerp(P, I, u) for u in us]
secF = [lerp(P, F, u) for u in us]
secD = [lerp(P, D, u) for u in us]

def banda_cara(sA, sB, k, grad, borde_arriba):
    """Banda entre sección k y k+1 sobre aristas A,B de una cara triangular.
    Devuelve trapecio (A_k, B_k, B_{k+1}, A_{k+1})."""
    return [sA[k], sB[k], sB[k + 1], sA[k + 1]]

parts = []
def add(s):
    parts.append(s)

# Sombra en suelo (elipse suave bajo la base)
add(f'<ellipse cx="{F[0]:.0f}" cy="{(F[1]+A[1])/2+10:.0f}" rx="{abs(I[0]-D[0])/2+40:.0f}" ry="120" fill="rgba(0,0,0,.45)" filter="url(#blurS)"/>')

# --- Cara izquierda (iluminada) ---
add(f'<polygon points="{poly_str([P, I, F])}" fill="url(#luzI)"/>')
# bandas
for k in range(N):
    quad = banda_cara(secI, secF, k, "luzI", k)
    fill = f"url(#luzI)" if k % 2 == 0 else "url(#luzI2)"
    add(f'<polygon points="{poly_str(quad)}" fill="{fill}"/>')
    # junta inferior (base de la hilada)
    add(f'<line x1="{quad[0][0]:.1f}" y1="{quad[0][1]:.1f}" x2="{quad[1][0]:.1f}" y2="{quad[1][1]:.1f}" stroke="rgba(70,40,5,.45)" stroke-width="2.6"/>')
    # sombreado de bloque: línea paralela inferior de la banda para volumen
    add(f'<line x1="{quad[2][0]:.1f}" y1="{quad[2][1]:.1f}" x2="{quad[3][0]:.1f}" y2="{quad[3][1]:.1f}" stroke="rgba(0,0,0,.08)" stroke-width="1"/>')
# juntas verticales de bloques en cara izquierda (alternadas por banda)
for k in range(N):
    bA, bB = secI[k], secF[k]
    bA2, bB2 = secI[k + 1], secF[k + 1]
    off = (k % 2) * 0.5
    for j in range(1, bloques_por_banda):
        v = (j + off) / (bloques_por_banda + 1)
        p1 = lerp(bA, bB, v)
        p2 = lerp(bA2, bB2, v)
        add(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="rgba(70,40,5,.20)" stroke-width="1.4"/>')

# --- Cara derecha (sombra) ---
add(f'<polygon points="{poly_str([P, F, D])}" fill="url(#somD)"/>')
for k in range(N):
    quad = banda_cara(secF, secD, k, "somD", k)
    fill = f"url(#somD)" if k % 2 == 0 else "url(#somD2)"
    add(f'<polygon points="{poly_str(quad)}" fill="{fill}"/>')
    add(f'<line x1="{quad[0][0]:.1f}" y1="{quad[0][1]:.1f}" x2="{quad[1][0]:.1f}" y2="{quad[1][1]:.1f}" stroke="rgba(40,22,2,.5)" stroke-width="2.6"/>')
    add(f'<line x1="{quad[2][0]:.1f}" y1="{quad[2][1]:.1f}" x2="{quad[3][0]:.1f}" y2="{quad[3][1]:.1f}" stroke="rgba(0,0,0,.15)" stroke-width="1"/>')
for k in range(N):
    bA, bB = secF[k], secD[k]
    bA2, bB2 = secF[k + 1], secD[k + 1]
    off = (k % 2) * 0.5
    for j in range(1, bloques_por_banda):
        v = (j + off) / (bloques_por_banda + 1)
        p1 = lerp(bA, bB, v)
        p2 = lerp(bA2, bB2, v)
        add(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="rgba(40,22,2,.25)" stroke-width="1.4"/>')

# Arista central (punta -> frente) con brillo
add(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{F[0]:.1f}" y2="{F[1]:.1f}" stroke="url(#borde)" stroke-width="4"/>')
# Aristas laterales
add(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{I[0]:.1f}" y2="{I[1]:.1f}" stroke="rgba(255,230,180,.5)" stroke-width="2"/>')
add(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{D[0]:.1f}" y2="{D[1]:.1f}" stroke="rgba(0,0,0,.35)" stroke-width="2"/>')

# Base: contorno frontal visible
add(f'<path d="M {I[0]:.1f} {I[1]:.1f} L {F[0]:.1f} {F[1]:.1f} L {D[0]:.1f} {D[1]:.1f}" fill="none" stroke="rgba(0,0,0,.5)" stroke-width="1.5"/>')

# Vértice dorado
add(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="7" fill="#FFE9B8" stroke="#D9A653" stroke-width="2"/>')
add(f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="2.6" fill="#fff" opacity=".9"/>')

# Límites del dibujo para viewBox
xs = [p[0] for p in [P, I, D, F, A]] + [F[0]]
ys = [p[1] for p in [P, I, D, F, A]]
minx, maxx = min(xs) - 60, max(xs) + 60
miny, maxy = min(ys) - 60, max(ys) + 140
W, H = maxx - minx, maxy - miny

svg = f'''<svg width="{W:.0f}" height="{H:.0f}" viewBox="{minx:.0f} {miny:.0f} {W:.0f} {H:.0f}">
<defs>
  <filter id="blurS" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="18"/></filter>
  <linearGradient id="luzI" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#FFEDC2"/><stop offset="45%" stop-color="#F2CE8B"/><stop offset="100%" stop-color="#E0B268"/>
  </linearGradient>
  <linearGradient id="luzI2" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#F7DCA2"/><stop offset="100%" stop-color="#D8A95C"/>
  </linearGradient>
  <linearGradient id="somD" x1="100%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#C08A4A"/><stop offset="60%" stop-color="#99672F"/><stop offset="100%" stop-color="#6E4A1E"/>
  </linearGradient>
  <linearGradient id="somD2" x1="100%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#A97C3E"/><stop offset="100%" stop-color="#7C5424"/>
  </linearGradient>
  <linearGradient id="borde" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFF8E2"/><stop offset="100%" stop-color="rgba(255,240,200,.25)"/>
  </linearGradient>
</defs>
{''.join(parts)}
</svg>'''

plantilla = open('/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-3d/piramide_plantilla.html').read()
html = plantilla.replace('<!--SVG-->', svg)
out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-3d/piramide_v2.html'
open(out, 'w').write(html)
print('OK', out, f'viewBox {minx:.0f} {miny:.0f} {W:.0f} {H:.0f}')
