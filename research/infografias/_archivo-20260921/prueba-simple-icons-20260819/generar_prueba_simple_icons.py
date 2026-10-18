#!/usr/bin/env python3
"""Genera HTML de prueba con logos REALES de Simple Icons (desde disco).
Convierte fill fijo -> currentColor para colorear con CSS por tarjeta.
Uso: python3 generar_prueba_simple_icons.py <destino.html>"""
import os, re, sys

DEST = "/home/jokoalmi/joko-lab/assets/simple-icons"
# slug -> (nombre visible, clase css, nota)
MARCAS = [
    ("github", "GitHub", "c-github", "código"),
    ("docker", "Docker", "c-docker", "contenedores"),
    ("python", "Python", "c-python", "scripts"),
    ("telegram", "Telegram", "c-telegram", "canal"),
    ("linux", "Linux", "c-linux", "sistema"),
    ("n8n", "n8n", "c-n8n", "automatización"),
    ("ollama", "Ollama", "c-ollama", "LLM local"),
    ("deepseek", "DeepSeek", "c-deepseek", "cloud"),
    ("google", "Google", "c-google", "búsqueda"),
    ("huggingface", "Hugging Face", "c-huggingface", "modelos"),
    ("mistralai", "Mistral AI", "c-mistralai", "alternativa"),
    ("cloudflare", "Cloudflare", "c-cloudflare", "infra"),
]

def svg_coloreable(path):
    with open(path) as f:
        svg = f.read().strip()
    # Quitar title/role innecesarios y convertir fill fijo -> currentColor
    svg = re.sub(r'\s+fill="#[0-9A-Fa-f]{3,8}"', '', svg, count=1)
    svg = re.sub(r'(<svg[^>]*?)(\srole="img")', r'\1', svg, count=1)
    # asegurar fill="currentColor" en el svg raiz
    if 'fill="currentColor"' not in svg:
        svg = svg.replace('<svg ', '<svg fill="currentColor" ', 1)
    return svg

cards = []
for slug, nombre, clase, nota in MARCAS:
    path = os.path.join(DEST, f"{slug}.svg")
    if not os.path.exists(path):
        print(f"⚠️ falta {slug}.svg", file=sys.stderr)
        continue
    svg = svg_coloreable(path)
    cards.append(f'      <div class="logo-card"><svg class="{clase}" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">{svg}</svg><div class="name">{nombre}</div><div class="note">{nota}</div></div>')

html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Prueba Simple Icons — logos reales</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1080px; height:800px; overflow:hidden; font-family:'Open Sans',sans-serif;
         background: linear-gradient(160deg,#FDF8E9 0%,#F7EEDC 55%,#F3E6CF 100%); position:relative; }
  .content { position:relative; z-index:2; padding:48px; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:800; font-size:34px; color:#2D5D62; }
  .sub { font-family:'Caveat',cursive; font-size:24px; color:#7a6a45; margin-bottom:24px; }
  .grid { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; }
  .logo-card { background:rgba(255,255,255,.75); border-radius:18px; padding:22px;
               text-align:center; border-top:5px solid #2D5D62; box-shadow:0 6px 14px rgba(60,45,10,.12); }
  .logo-card svg { width:56px; height:56px; }
  .logo-card .name { font-family:'Montserrat',sans-serif; font-weight:700; font-size:15px; color:#333; margin-top:10px; }
  .logo-card .note { font-size:11px; color:#999; margin-top:2px; }
  .c-github { color:#181717; } .c-docker { color:#2496ED; } .c-python { color:#3776AB; }
  .c-telegram { color:#26A5E4; } .c-linux { color:#FCC624; } .c-n8n { color:#EA4B71; }
  .c-ollama { color:#000000; } .c-deepseek { color:#4D6BFE; } .c-google { color:#4285F4; }
  .c-huggingface { color:#FFD21E; } .c-mistralai { color:#FF7000; } .c-cloudflare { color:#F38020; }
</style>
</head>
<body>
  <div class="content">
    <h1>STACK DEL LAB — LOGOS REALES</h1>
    <div class="sub">Simple Icons incrustados (SVG oficial descargado, coloreado con CSS)</div>
    <div class="grid">
""" + "\n".join(cards) + """
    </div>
  </div>
</body>
</html>
"""

out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/prueba_simple_icons.html"
with open(out, "w") as f:
    f.write(html)
print(f"HTML generado: {out} ({len(cards)} logos reales)")
