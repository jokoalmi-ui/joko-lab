#!/usr/bin/env python3
"""Pirámide ESCALONADA tipo Kelsen — 6 LOSAS rectangulares completas (la idea:
cada nivel es una banda entera con su texto, SIEMPRE cabe). Volumen 2.5D:
frontal + lateral + techo por losa. Demo de FORMA (usuario 03-sep: "en vez de
3 partes, ponle 6 — sigue siendo pirámide pero deja más espacio al texto").
"""
import os

# 6 niveles: [nombre, y_top, y_bot, media-anchura, color texto]
NIV = [
    # arriba (estrecha) -> abajo (ancha)
    ("CONSTITUCIÓN",            -330.0, -190.0, 150.0),
    ("TRATADOS INTERNACIONALES", -190.0, -50.0,  210.0),
    ("LEYES",                    -50.0,  90.0,  270.0),
    ("DECRETOS",                  90.0, 230.0,  330.0),
    ("RESOLUCIONES MINISTERIALES", 230.0, 370.0, 390.0),
    ("OTRAS RESOLUCIONES",        370.0, 510.0, 450.0),
]
# paleta: fríos arriba (legislativo) -> cálidos abajo (administrativo)
PAL = [
    {"f": ("#E8554D", "#C73A33"), "s": ("#9E2B25", "#7A1F1A"), "t": ("#F5A8A3", "#E07570")},  # rojo
    {"f": ("#C05FB0", "#A24492"), "s": ("#7D3672", "#5F2757"), "t": ("#DFA6D4", "#C586B8")},  # magenta
    {"f": ("#4E6FD8", "#3A53B4"), "s": ("#2B3D87", "#1E2C66"), "t": ("#93A7EA", "#7288D9")},  # azul
    {"f": ("#4FA36B", "#3C8557"), "s": ("#2B6240", "#1F4A30"), "t": ("#8FC7A3", "#6DAE87")},  # verde
    {"f": ("#E0A83C", "#C98F28"), "s": ("#9C6D1D", "#775215"), "t": ("#F0CF8A", "#E6BC66")},  # amarillo/ámbar
    {"f": ("#E87B3E", "#D06128"), "s": ("#A0491D", "#7C3714"), "t": ("#F3B58F", "#E99A6B")},  # naranja
]
SHIFT = (170.0, -98.0)  # extrusión isométrica

def pol(pts):
    return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)

def sh(pt):
    return (pt[0] + SHIFT[0], pt[1] + SHIFT[1])

parts, defs = [], ['<defs>', '<filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>']
for i, pal in enumerate(PAL):
    f1, f2 = pal["f"]; s1, s2 = pal["s"]; t1, t2 = pal["t"]
    defs.append(f'<linearGradient id="gf{i}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{f1}"/><stop offset="100%" stop-color="{f2}"/></linearGradient>')
    defs.append(f'<linearGradient id="gs{i}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{s1}"/><stop offset="100%" stop-color="{s2}"/></linearGradient>')
    defs.append(f'<linearGradient id="gt{i}" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t1}"/><stop offset="100%" stop-color="{t2}"/></linearGradient>')
defs.append('</defs>')

# sombra suelo
base = NIV[-1]
parts.append(f'<ellipse cx="{90:.0f}" cy="{base[2]+100:.0f}" rx="560" ry="66" fill="rgba(0,0,0,.45)" filter="url(#blurS)"/>')

# dibujar de abajo a arriba
for i, (nombre, y_top, y_bot, hw) in enumerate(NIV):
    pal = PAL[i]
    xL, xR = -hw, hw
    fA, fB = (xR, y_top), (xR, y_bot)
    bA, bB = sh(fA), sh(fB)
    # lateral derecho (sombra)
    parts.append(f'<polygon points="{pol([fA, fB, bB, bA])}" fill="url(#gs{i})"/>')
    # techo
    pA, pB = sh((-hw, y_top)), sh((hw, y_top))
    parts.append(f'<polygon points="{pol([(-hw, y_top), (hw, y_top), pB, pA])}" fill="url(#gt{i})"/>')
    # frontal
    parts.append(f'<polygon points="{pol([(xL, y_top), (xR, y_top), (xR, y_bot), (xL, y_bot)])}" fill="url(#gf{i})"/>')
    parts.append(f'<line x1="{xL:.1f}" y1="{y_top:.1f}" x2="{xR:.1f}" y2="{y_top:.1f}" stroke="rgba(255,255,255,.55)" stroke-width="2"/>')

# texto por nivel (blanco, 1 línea, legible — cada losa es BANDA COMPLETA)
for i, (nombre, y_top, y_bot, hw) in enumerate(NIV):
    parts.append(f'<text x="0" y="{(y_top+y_bot)/2+9:.0f}" text-anchor="middle" font-family="Inter,Arial" font-size="23" font-weight="800" fill="#fff" letter-spacing="1.5">{nombre}</text>')

# marcas de grupo: ACTOS LEGISLATIVOS (arriba, izquierda) / ACTOS ADMINISTRATIVOS (abajo, derecha)
parts.append(f'<text x="{-NIV[3][3]-80:.0f}" y="{-60:.0f}" transform="rotate(-90 {-NIV[3][3]-80:.0f} {-60:.0f})" text-anchor="middle" font-family="Inter,Arial" font-size="20" font-weight="800" fill="rgba(255,255,255,.8)" letter-spacing="6">ACTOS LEGISLATIVOS</text>')
parts.append(f'<text x="{NIV[3][3]+80:.0f}" y="{310:.0f}" transform="rotate(-90 {NIV[3][3]+80:.0f} {310:.0f})" text-anchor="middle" font-family="Inter,Arial" font-size="20" font-weight="800" fill="rgba(255,255,255,.8)" letter-spacing="6">ACTOS ADMINISTRATIVOS</text>')
# línea separadora entre legislativo (niv 0-2) y administrativo (niv 3-5)
y_sep = (NIV[2][2] + NIV[3][1]) / 2
parts.append(f'<line x1="{-NIV[0][3]-20:.0f}" y1="{y_sep:.0f}" x2="{NIV[0][3]+20:.0f}" y2="{y_sep:.0f}" stroke="rgba(255,255,255,.9)" stroke-width="3" stroke-dasharray="10 8"/>')

# contorno exterior con aristas redondeadas
parts.append(f'<path d="M {-NIV[0][3]:.0f} {NIV[0][1]:.0f} L {-base[3]:.0f} {base[1]:.0f} L {-base[3]:.0f} {base[2]:.0f}" fill="none" stroke="rgba(255,255,255,.65)" stroke-width="4" stroke-linejoin="round"/>')
parts.append(f'<path d="M {NIV[0][3]:.0f} {NIV[0][1]:.0f} L {base[3]:.0f} {base[1]:.0f} L {base[3]:.0f} {base[2]:.0f}" fill="none" stroke="rgba(255,255,255,.65)" stroke-width="4" stroke-linejoin="round"/>')

xs = [-base[3], base[3], base[3] + SHIFT[0], -NIV[0][3], NIV[0][3]]
ys = [NIV[0][1] - 40, base[2], base[2] + SHIFT[1] + 30]
minx, maxx = min(xs) - 150, max(xs) + 150
miny, maxy = min(ys) - 20, max(ys) + 40
Wv, Hv = maxx - minx, maxy - miny

svg = (f'<svg width="{Wv:.0f}" height="{Hv:.0f}" viewBox="{minx:.0f} {miny:.0f} {Wv:.0f} {Hv:.0f}" '
       f'style="filter:drop-shadow(0 26px 48px rgba(0,0,0,.35));">' + "".join(defs) + "".join(parts) + "</svg>")

html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter','Helvetica Neue',Arial,sans-serif; }}
  .slide {{ width:1080px; height:1350px; position:relative; overflow:hidden;
    background:radial-gradient(1100px 760px at 30% -10%, #f6f2ea 0%, #ece5d6 55%, #ddd2ba 100%); }}
  .content {{ position:absolute; inset:0; padding:52px 80px 44px; display:flex; flex-direction:column; }}
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
    <div class="titulo">Pirámide <span class="accent">escalonada</span> · 6 losas</div>
    <div class="sub">Cada nivel es una banda completa — <b>el texto siempre cabe</b>, la forma sigue siendo pirámide</div>
    <div class="escena">{svg}</div>
    <div class="pie">
      <div class="tec">SVG 2.5D · losas con techo y lateral · demo de FORMA (contenido: Kelsen simplificado)</div>
      <div class="chip">DEMO · VOLUMEN 2.5D</div>
    </div>
  </div>
</div>
</body></html>'''

out = '/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-03-piramide-escalonada-kelsen/demo_kelsen_6losas.html'
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write(html)
print('OK', out)
