#!/usr/bin/env python3
"""generar_carrusel_linkedin.py — Pipeline LinkedIn Lab (B2, 20-ago-2026).

Tema → guion (6 arquetipos maurys) → HTML por slide → render PNG (Chrome
headless 1080×1350) → verificación visual (GLM/browser) → caption + hashtags.

Uso:
  python3 generar_carrusel_linkedin.py "tema del carrusel" [--outdir dir]
  python3 generar_carrusel_linkedin.py --demo     # caso real: RAG 26GB→320MB

El guion usa DATOS REALES del lab (el diferenciador): mediciones, logs, OPs.
El script genera un guion por defecto desde el tema; el usuario puede editarlo
(salida guion.json) y re-renderizar con --guion guion.json.

Requiere: el helper ~/joko-lab/tools/render_html.sh (elige el binario de Chrome) + la plantilla plantilla-maurys.html.
Verificación visual: ver cada PNG con browser_vision/GLM antes de publicar.
"""
import json, os, re, subprocess, sys, tempfile, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PLANTILLA = os.path.join(BASE, "plantilla-maurys.html")
RENDER = "/home/jokoalmi/joko-lab/tools/render_html.sh"  # helper unico HTML->PNG/PDF del lab
CHROME = "/usr/bin/google-chrome"  # ya no se invoca directo: lo usa el helper
OUT_DEFAULT = os.path.join(BASE, "salidas")

ARQUETIPOS = ("gancho", "concepto", "como", "por_que", "escala", "cta")

# ---------- Plantillas de slide por arquetipo (maurys: título arriba, gráfico central, listas, pasos) ----------

def slide_gancho(titulo, subtitulo, dato, unidad):
    return f"""
<div class="slide" data-arquetipo="gancho">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{titulo}</div>
  <div class="subtitulo">{subtitulo}</div>
  <div class="cuerpo">
    <div class="grafico">
      <div class="caja"><div class="num">{dato}</div><div class="lbl">{unidad}</div></div>
    </div>
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span> · 1/{1}</div><div class="nslide">HILO ↓</div></div>
</div>"""

def slide_concepto(num, titulo, items, grafico=None, pasos=None):
    items_html = "".join(
        f'<div class="item"><div class="icono">{i+1}</div><div class="txt">{t}<small>{s}</small></div></div>'
        for i, (t, s) in enumerate(items)
    )
    pasos_html = ""
    if pasos:
        pasos_html = '<div class="pasos">' + "".join(
            f'<div class="paso"><span class="n">{i+1}</span>{p}</div>' for i, p in enumerate(pasos)
        ) + '</div>'
    return f"""
<div class="slide" data-arquetipo="concepto">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{num}. {titulo}</div>
  <div class="cuerpo">
    <div class="lista">{items_html}</div>
    {pasos_html}
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span></div><div class="nslide">2/6 · CONCEPTO</div></div>
</div>"""

def slide_metricas(num, titulo, subtitulo, metricas, pasos=None):
    """Gráfico central con métricas (cajas numeradas) — el 'gráficos bonitos'."""
    cajas = "".join(
        f'<div class="caja"><div class="num">{v}</div><div class="lbl">{l}</div></div>'
        for v, l in metricas
    )
    flechas = '<div class="flecha">→</div>' * (len(metricas) - 1)
    pasos_html = ""
    if pasos:
        pasos_html = '<div class="pasos">' + "".join(
            f'<div class="paso"><span class="n">{i+1}</span>{p}</div>' for i, p in enumerate(pasos)
        ) + '</div>'
    return f"""
<div class="slide" data-arquetipo="como">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{num}. {titulo}</div>
  <div class="subtitulo">{subtitulo}</div>
  <div class="cuerpo">
    <div class="grafico">{cajas}{flechas}</div>
    {pasos_html}
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span></div><div class="nslide">3/6 · CÓMO</div></div>
</div>"""

def slide_por_que(num, titulo, items, pasos=None):
    items_html = "".join(
        f'<div class="item"><div class="icono acc">{i+1}</div><div class="txt">{t}<small>{s}</small></div></div>'
        for i, (t, s) in enumerate(items)
    )
    pasos_html = ""
    if pasos:
        pasos_html = '<div class="pasos">' + "".join(
            f'<div class="paso"><span class="n">{i+1}</span>{p}</div>' for i, p in enumerate(pasos)
        ) + '</div>'
    return f"""
<div class="slide" data-arquetipo="por_que">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{num}. {titulo}</div>
  <div class="cuerpo">
    <div class="lista">{items_html}</div>
    {pasos_html}
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span></div><div class="nslide">4/6 · POR QUÉ</div></div>
</div>"""

def slide_escala(num, titulo, items):
    items_html = "".join(
        f'<div class="item"><div class="icono acc">{i+1}</div><div class="txt">{t}<small>{s}</small></div></div>'
        for i, (t, s) in enumerate(items)
    )
    return f"""
<div class="slide" data-arquetipo="escala">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{num}. {titulo}</div>
  <div class="cuerpo">
    <div class="lista">{items_html}</div>
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span></div><div class="nslide">5/6 · ESCALA</div></div>
</div>"""

def slide_cta(titulo, subtitulo, hashtags):
    return f"""
<div class="slide" data-arquetipo="cta">
  <div class="marca">
    <div class="logo">JL</div>
    <div>
      <div class="nombre">Joko <span>Lab</span></div>
      <div class="tag">IA local · datos reales</div>
    </div>
  </div>
  <div class="titulo">{titulo}</div>
  <div class="subtitulo">{subtitulo}</div>
  <div class="cuerpo">
    <div class="grafico" style="flex-direction:column; gap:16px;">
      <div style="font-size:30px; font-weight:800; color:#1a1a1a;">¿TE HA SERVIDO?</div>
      <div style="font-size:22px; color:#555;">Comenta o comparte — aprendemos todos</div>
    </div>
  </div>
  <div class="pie"><div class="joko">Joko <span>Lab</span></div><div class="nslide">6/6 · CTA</div></div>
</div>"""

# ---------- Guion por defecto (demo: A5 real del lab) ----------

def guion_demo():
    return {
        "tema": "LanceDB: de 26 GB a 320 MB sin tocar una sola fila",
        "slides": [
            {"tipo": "gancho",
             "titulo": "Mi RAG ocupaba <span class='accent'>26 GB</span> y no lo sabía",
             "subtitulo": "No era el contenido. Eran las <b>versiones viejas</b> que el índice iba acumulando cada día.",
             "dato": "98.8%", "unidad": "de disco liberado"},
            {"tipo": "concepto", "num": "1",
             "titulo": "El problema: cada reindexado engorda",
             "items": [
                 ("Cada daily crea una versión nueva", "LanceDB guarda el histórico de cada escritura"),
                 ("13 días sin limpiar = 453 versiones", "El índice real del lab, medido el 20-ago"),
                 ("La tabla 'joko_notes' pesaba 26 GB", "Aunque solo tenía ~21.000 fragmentos de texto"),
             ]},
            {"tipo": "metricas", "num": "2",
             "titulo": "Un fix de una línea… que no era suficiente",
             "subtitulo": "<b>optimize() solo</b> compacta, pero <b>no borra</b> las versiones viejas",
             "metricas": [("453", "versiones"), ("26 GB", "peso real"), ("311 MB", "tras limpiar")],
             "pasos": ["compact_files", "cleanup_old_versions", "optimize"]},
            {"tipo": "por_que", "num": "3",
             "titulo": "Por qué importa (y no es solo disco)",
             "items": [
                 ("Búsquedas más lentas", "cada consulta mira versiones muertas"),
                 ("Backups enormes", "copiar 26 GB para guardar 320 MB"),
                 ("El SSD se llena sin avisar", "en mi caso, en ~2 semanas"),
             ]},
            {"tipo": "escala", "num": "4",
             "titulo": "Lo que aprendí (datos reales)",
             "items": [
                 ("Medir antes de optimizar", "no sabía el peso hasta que lo miré"),
                 ("El recall NO bajó", "100% (8/8) antes y después"),
                 ("Hoy el daily compacta solo", "1-2 versiones por tabla, estable"),
             ]},
            {"tipo": "cta",
             "titulo": "¿Tu RAG también <span class='accent'>engorda</span>?",
             "subtitulo": "Mira cuántas versiones tiene tu índice: du -sh .lancedb te lo dice en 1 segundo",
             "hashtags": "#RAG #LanceDB #LocalAI #DataEngineering"},
        ],
        "caption": "Mi RAG ocupaba 26 GB por un motivo invisible: cada reindexado diario creaba una versión nueva del índice y nadie las borraba.\n\nUn fix de una línea (optimize) no bastaba. La secuencia completa: compact_files + cleanup_old_versions + optimize.\n\nResultado: 26 GB → 320 MB (-98.8%), recall@5 al 100%, y el daily ya compacta solo.\n\n¿Sabías cuánto ocupa tu índice?",
        "alt": "Carrusel: de 26 GB a 320 MB en un índice LanceDB — el fix de compactación real del lab, con métricas reales.",
        "hashtags": "#RAG #LanceDB #LocalAI #DataEngineering #OpenSource",
    }

# ---------- Render ----------

def render_slide(html_slide, out_png):
    with open(PLANTILLA) as f:
        plantilla = f.read()
    html = plantilla.replace("<!-- @@SLIDE@@ -->", html_slide)
    tmp_html = out_png.replace(".png", ".html")
    with open(tmp_html, "w") as f:
        f.write(html)
    cmd = ["bash", RENDER, "--espera=10000", tmp_html, out_png, "1080", "1350"]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return tmp_html

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Carrusel LinkedIn Lab (B2)")
    ap.add_argument("tema", nargs="?", default=None, help="tema del carrusel")
    ap.add_argument("--demo", action="store_true", help="generar el caso demo (datos reales A5)")
    ap.add_argument("--guion", default=None, help="JSON con guion custom")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    if args.guion:
        with open(args.guion) as f:
            guion = json.load(f)
    elif args.demo:
        guion = guion_demo()
    elif args.tema:
        guion = {"tema": args.tema, "slides": [], "caption": "", "alt": "", "hashtags": ""}
        print("⚠️  Guion automático para tema libre: edita guion.json (salida) o usa --demo")
    else:
        print(__doc__)
        sys.exit(1)

    fecha = datetime.date.today().isoformat()
    slug = re.sub(r"[^a-z0-9]+", "-", guion["tema"].lower()).strip("-")[:50]
    outdir = args.outdir or os.path.join(OUT_DEFAULT, f"{fecha}-{slug}")
    os.makedirs(outdir, exist_ok=True)

    # Guardar guion (editable para re-render)
    with open(os.path.join(outdir, "guion.json"), "w") as f:
        json.dump(guion, f, ensure_ascii=False, indent=2)

    n = len(guion["slides"])
    pngs = []
    for i, s in enumerate(guion["slides"], 1):
        tipo = s["tipo"]
        if tipo == "gancho":
            html = slide_gancho(s["titulo"], s["subtitulo"], s["dato"], s["unidad"])
        elif tipo == "concepto":
            html = slide_concepto(s.get("num", str(i)), s["titulo"], s["items"])
        elif tipo == "metricas":
            html = slide_metricas(s.get("num", str(i)), s["titulo"], s["subtitulo"],
                                  s["metricas"], s.get("pasos"))
        elif tipo == "por_que":
            html = slide_por_que(s.get("num", str(i)), s["titulo"], s["items"])
        elif tipo == "escala":
            html = slide_escala(s.get("num", str(i)), s["titulo"], s["items"])
        elif tipo == "cta":
            html = slide_cta(s["titulo"], s["subtitulo"], s.get("hashtags", ""))
        else:
            print(f"⚠️  arquetipo desconocido: {tipo} (slide {i})")
            continue
        png = os.path.join(outdir, f"slide-{i:02d}.png")
        render_slide(html, png)
        pngs.append(png)
        print(f"  [{i}/{n}] {tipo} → {png}")

    print(f"\n✅ Carrusel generado: {outdir}")
    print(f"   Slides: {len(pngs)} · Guion editable: guion.json")
    print("   ⚠️  VERIFICAR cada PNG con visión (browser_vision/GLM) ANTES de publicar.")
    return outdir

if __name__ == "__main__":
    main()
