#!/usr/bin/env python3
"""mapa_conocimiento.py — Mapa temático visual del conocimiento real del RAG.

Genera un HTML interactivo autónomo (scatter TSNE + clusters) con los fragmentos
de CONOCIMIENTO del lab (research, lpa, 01-knowledge, guías, biohacking, docs),
excluyendo 04-operations (backlogs/sesiones = 84% del índice y no son conocimiento).

Pipeline (100% local, 0 LLM):
  1. Lee joko_notes (LanceDB) — solo lectura.
  2. Filtra por dominios de conocimiento real.
  3. PCA (50d) -> TSNE (2d) -> KMeans (18 clusters por defecto).
  4. Etiqueta clusters por frecuencia de palabras en títulos.
  5. Escribe un HTML único y autónomo (sin servidor ni dependencias externas).

Uso:
  python3 mapa_conocimiento.py                     # salida: /tmp/mapa_conocimiento.html
  python3 mapa_conocimiento.py --out informe.html  # salida en otra ruta
  python3 mapa_conocimiento.py --k 12              # número de clusters
  python3 mapa_conocimiento.py --infer             # NO usar por defecto: el pase semántico
                                                   # requeriría un LLM; el script es 100% local.

Requiere el venv hermes-rag (lancedb, sklearn, numpy):
  ~/.venv/hermes-rag/bin/python3 mapa_conocimiento.py
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import lancedb
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

PREF = "/home/jokoalmi/joko-lab/"
DB_PATH = "/home/jokoalmi/joko-lab/.lancedb"
TABLE = "joko_notes"
KNOW_DOMS = {"research", "lpa", "biohacking", "docs", "tfm", "instruments"}

COLORS = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0",
          "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324", "#fffac8",
          "#800000", "#aaffc3", "#808000", "#000075", "#808080", "#ffd8b1"]

STOP = set("el la los las de del al a y o u en con por para un una unos unas que es se su "
           "sus lo como mas las esta este esto estas estos ese esa eso le les me mi tu "
           "nuestro nuestros no si ya ni pero sin sobre entre hacia hasta desde ante tras "
           "bajo cada muy poco mucho mucha toda todo todos todas ser haber estar tiene "
           "tienen ha han he hemos hay fue eran sido siendo porque cual cuales quien "
           "quienes cuando donde como cual cuyo cuya segun durante mediante".split())


def dominio(path):
    p = str(path).replace(PREF, "").replace("/home/jokoalmi/", "")
    parts = [x for x in p.split("/") if x]
    if not parts:
        return "(raiz)"
    if parts[0] == "01-knowledge":
        return "01-knowledge"
    return parts[0]


def top_words(titles, n=6):
    c = Counter()
    for t in titles:
        for w in re.split(r"[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]+", str(t)):
            w = w.strip().lower()
            if len(w) < 4 or w in STOP or w.isdigit():
                continue
            c[w] += 1
    return [w for w, _ in c.most_common(n)]


def load_subset():
    db = lancedb.connect(DB_PATH)
    t = db.open_table(TABLE)
    ds = t.to_lance()
    df = ds.to_table(columns=["path", "title", "tags", "type", "status", "vector"]).to_pandas()
    df["dom"] = df["path"].apply(dominio)
    df["keep"] = df["dom"].isin(KNOW_DOMS) | df["path"].str.contains("01-knowledge/") | \
                 df["path"].str.contains("GUIA-JOKO-LAB.md") | \
                 df["path"].str.contains("GUIA-APRENDIZAJE-JOKO-LAB.md") | \
                 df["path"].str.contains("README.md")
    sub = df[df["keep"]].copy()
    vecs = np.stack(sub["vector"].values).astype(np.float32)
    return sub, vecs


def project_cluster(vecs, k):
    pca = PCA(n_components=50, random_state=42)
    low = pca.fit_transform(vecs)
    tsne = TSNE(n_components=2, perplexity=30, init="pca", random_state=42,
                learning_rate="auto", n_jobs=-1)
    xy = tsne.fit_transform(low)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(low)
    return xy, labels, pca.explained_variance_ratio_.sum()


def build_html(points, cluster_names, k):
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    W, H, PAD = 1400, 900, 60

    def sx(v):
        return PAD + (v - xmin) / (xmax - xmin) * (W - 2 * PAD)

    def sy(v):
        return PAD + (v - ymin) / (ymax - ymin) * (H - 2 * PAD)

    for p in points:
        p["px"] = round(sx(p["x"]), 1)
        p["py"] = round(sy(p["y"]), 1)

    dom_by_c = {}
    for p in points:
        dom_by_c.setdefault(p["c"], Counter())[p["d"]] += 1
    legend = []
    for c in sorted(dom_by_c):
        sizes = sum(1 for p in points if p["c"] == c)
        top = ", ".join(d for d, _ in dom_by_c[c].most_common(3))
        legend.append({"c": c, "n": sizes, "name": " ".join(cluster_names.get(str(c), [])), "doms": top})

    pts_json = json.dumps([{"x": p["px"], "y": p["py"], "c": p["c"], "t": p["t"],
                            "p": p["p"], "d": p["d"]} for p in points], ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Mapa del conocimiento — Joko Lab</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 0; background: #0f1117; color: #e8e8e8; }}
  h1 {{ font-size: 18px; margin: 10px 14px 2px; }}
  .sub {{ font-size: 12px; color: #999; margin: 0 14px 10px; }}
  #wrap {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 0 10px; }}
  #canvasBox {{ flex: 1 1 900px; min-width: 500px; position: relative; }}
  canvas {{ width: 100%; height: auto; background: #14161d; border-radius: 8px; cursor: crosshair; }}
  #tooltip {{ position: fixed; background: #1c1f28; border: 1px solid #444; border-radius: 6px;
              padding: 6px 9px; font-size: 11px; max-width: 420px; pointer-events: none; display: none; z-index: 9; }}
  #sidebar {{ flex: 0 1 300px; font-size: 11px; max-height: 900px; overflow-y: auto; }}
  .lrow {{ display: flex; align-items: center; gap: 6px; padding: 2px 4px; border-radius: 4px; cursor: pointer; }}
  .lrow:hover {{ background: #232733; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; flex: 0 0 auto; }}
  .lname {{ font-weight: 600; }}
  .ln {{ color: #999; margin-left: auto; white-space: nowrap; }}
  .doms {{ color: #6b7280; }}
  input[type=text] {{ width: 90%; margin: 6px 10px; padding: 5px 8px; background:#1c1f28; border:1px solid #444;
                    color:#e8e8e8; border-radius:5px; }}
  .domchip {{ display:inline-block; font-size:10px; padding:1px 6px; border-radius:8px; background:#232733; margin:1px; cursor:pointer; }}
  .domchip.on {{ background:#2f5fd0; }}
  #filters {{ padding: 0 10px 6px; }}
</style></head><body>
<h1>🗺️ Mapa del conocimiento — Joko Lab</h1>
<div class="sub">{len(points)} fragmentos de conocimiento real · TSNE · {k} clusters · 0 LLM</div>
<input type="text" id="q" placeholder="🔍 Buscar en títulos... (escribe y filtra)">
<div id="filters"></div>
<div id="wrap">
  <div id="canvasBox"><canvas id="cv" width="{W}" height="{H}"></canvas></div>
  <div id="sidebar"></div>
</div>
<div id="tooltip"></div>
<script>
const PTS = {pts_json};
const COLORS = {json.dumps(COLORS)};
const LEGEND = {json.dumps(legend, ensure_ascii=False)};
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
const tip = document.getElementById('tooltip');
let hiddenClusters = new Set();
let domOn = new Set();
let query = '';

const doms = [...new Set(PTS.map(p => p.d))];
const filtBox = document.getElementById('filters');
doms.forEach(d => {{ const s = document.createElement('span'); s.className='domchip on'; s.textContent=d;
  s.onclick=()=>{{ s.classList.toggle('on'); domOn.has(d)?domOn.delete(d):domOn.add(d); draw(); }}; filtBox.appendChild(s); }});

function visible(p) {{
  if (hiddenClusters.has(p.c)) return false;
  if (domOn.size && !domOn.has(p.d)) return false;
  if (query) {{
    const hay = (p.t + ' ' + p.p + ' ' + p.d).toLowerCase();
    if (!hay.includes(query)) return false;
  }}
  return true;
}}

function draw() {{
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.strokeStyle='#1d2029'; ctx.lineWidth=1;
  for (let gx=0; gx<cv.width; gx+=70) {{ ctx.beginPath(); ctx.moveTo(gx,0); ctx.lineTo(gx,cv.height); ctx.stroke(); }}
  for (let gy=0; gy<cv.height; gy+=70) {{ ctx.beginPath(); ctx.moveTo(0,gy); ctx.lineTo(cv.width,gy); ctx.stroke(); }}
  const vp = PTS.filter(visible);
  const r = Math.max(1.2, 2.6 - vp.length/6000);
  vp.forEach(p => {{
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI*2);
    ctx.fillStyle = COLORS[p.c % COLORS.length];
    ctx.globalAlpha = 0.55;
    ctx.fill();
  }});
  ctx.globalAlpha = 1;
  drawSidebar(vp.length);
}}

const sb = document.getElementById('sidebar');
function drawSidebar(shown) {{
  sb.innerHTML = '';
  const items = LEGEND.slice().sort((a,b)=>b.n-a.n);
  items.forEach(l => {{
    const row = document.createElement('div');
    row.className = 'lrow';
    const dot = document.createElement('span'); dot.className='dot';
    dot.style.background = COLORS[l.c % COLORS.length];
    const nm = document.createElement('span'); nm.className='lname'; nm.textContent = l.name;
    const nn = document.createElement('span'); nn.className='ln'; nn.textContent = l.n;
    const dm = document.createElement('span'); dm.className='doms'; dm.textContent = ' — ' + l.doms;
    row.append(dot, nm, dm, nn);
    row.onclick = () => {{ hiddenClusters.has(l.c)?hiddenClusters.delete(l.c):hiddenClusters.add(l.c);
      row.style.opacity = hiddenClusters.has(l.c)?'0.35':'1'; draw(); }};
    row.style.opacity = hiddenClusters.has(l.c)?'0.35':'1';
    sb.appendChild(row);
  }});
  const cnt = document.createElement('div');
  cnt.style.cssText = 'color:#6b7280;margin-top:8px;font-size:10px';
  cnt.textContent = 'Mostrando ' + shown + ' / ' + PTS.length + ' puntos';
  sb.appendChild(cnt);
}}

cv.addEventListener('mousemove', e => {{
  const rect = cv.getBoundingClientRect();
  const mx = (e.clientX-rect.left) * cv.width/rect.width;
  const my = (e.clientY-rect.top) * cv.height/rect.height;
  let best=null, bd=1e9;
  for (const p of PTS) {{
    if (!visible(p)) continue;
    const dx=p.x-mx, dy=p.y-my, dd=dx*dx+dy*dy;
    if (dd<bd) {{ bd=dd; best=p; }}
  }}
  if (best && bd < 120) {{
    tip.style.display='block';
    tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px';
    tip.innerHTML = '<b>'+best.t+'</b><br><span style="color:#888">'+best.p+'</span><br><span style="color:#58a">#'+best.c+' · '+best.d+'</span>';
  }} else tip.style.display='none';
}});

const qin = document.getElementById('q');
qin.addEventListener('input', () => {{ query = qin.value.trim().toLowerCase(); draw(); }});
draw();
</script></body></html>"""
    return html


def main():
    ap = argparse.ArgumentParser(description="Mapa temático del conocimiento del RAG (Joko Lab)")
    ap.add_argument("--out", default="/tmp/mapa_conocimiento.html", help="Ruta HTML de salida")
    ap.add_argument("--k", type=int, default=18, help="Número de clusters (default 18)")
    ap.add_argument("--infer", action="store_true", help="Reservado: pase semántico con LLM (no implementado, 0 LLM por diseño)")
    args = ap.parse_args()

    print("1/5 Leyendo joko_notes (solo lectura)...")
    sub, vecs = load_subset()
    n = vecs.shape[0]
    print(f"   -> {n} fragmentos de conocimiento (research+lpa+01-knowledge+guías+biohacking)")

    print("2/5 PCA + TSNE + KMeans...")
    xy, labels, var = project_cluster(vecs, args.k)
    print(f"   -> proyección 2D OK · varianza explicada (50d): {var:.3f} · {args.k} clusters")

    titles_by_cluster = {}
    for i, lab in enumerate(labels):
        titles_by_cluster.setdefault(int(lab), []).append(str(sub["title"].iloc[i]))

    cluster_names = {str(k): top_words(titles_by_cluster[k]) for k in titles_by_cluster}

    print("3/5 Construyendo puntos...")
    points = []
    for i in range(n):
        points.append({"x": float(xy[i, 0]), "y": float(xy[i, 1]), "c": int(labels[i]),
                       "t": str(sub["title"].iloc[i])[:140], "p": str(sub["path"].iloc[i]),
                       "d": dominio(str(sub["path"].iloc[i]))})

    print("4/5 Generando HTML...")
    html = build_html(points, cluster_names, args.k)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        f.write(html)
    print(f"5/5 HTML guardado: {args.out} ({os.path.getsize(args.out)//1024} KB)")

    print("\nClusters detectados:")
    dom_by_c = {}
    for p in points:
        dom_by_c.setdefault(p["c"], Counter())[p["d"]] += 1
    for c in sorted(dom_by_c):
        n_c = sum(1 for p in points if p["c"] == c)
        top = ", ".join(d for d, _ in dom_by_c[c].most_common(3))
        name = " ".join(cluster_names.get(str(c), []))
        print(f"  #{c:2d} n={n_c:4d} | {name:40s} | {top}")


if __name__ == "__main__":
    main()
