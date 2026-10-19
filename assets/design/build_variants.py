#!/usr/bin/env python3
"""build_variants.py - fase 1 del design system de Joko Lab

Coge UNA pieza ya validada, aplica N presets de layout derivados de
design-tokens.yaml, renderiza cada variante con Chrome headless y mide:

  - overflow    px de contenido que se sale del lienzo
  - aire        hueco real entre el ultimo bloque y el pie
  - gap_min     separacion minima entre bloques consecutivos
  - fuera       elementos que rompen el margen lateral
  - contraste   ratio WCAG medido sobre los pixeles del PNG (no declarado)

Uso:
    python3 build_variants.py                 # todas las variantes
    python3 build_variants.py --only v2       # una
    python3 build_variants.py --no-render     # solo escribe HTML

Salida: out/<variante>.html, out/<variante>.png, out/report.json
No toca la pieza original: lee su HTML como base y escribe en out/.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LAB = HERE.parents[1]
TOKENS = HERE / "design-tokens.yaml"
OUT = HERE / "out"
BASE = LAB / "research/infografias/perfume-del-dia-20261019/ficha_d.html"
CHROME = "google-chrome"

# Presets de layout. Cada uno solo mueve geometria; el contenido es el mismo.
PRESETS = {
    "v1_vigente": {
        "label": "V1 vigente (referencia 19-oct)",
        "css": {
            ".frasco-col": "width:300px",
            ".frasco-figura": "height:450px",
            ".hero": "gap:44px",
            "h1": "font-size:72px",
            ".pir3d-svg": "width:470px;height:220px",
            ".inspiracion": "margin-left:44px",
            ".alts": "margin-left:44px",
            ".cita": "margin-left:44px",
        },
    },
    "v2_compacto": {
        "label": "V2 compacto (menos frasco, mas aire de lectura)",
        "css": {
            ".frasco-col": "width:246px",
            ".frasco-figura": "height:376px",
            ".hero": "gap:30px",
            "h1": "font-size:64px;line-height:1.02",
            ".pir3d-svg": "width:420px;height:200px",
            ".sec-head": "margin-bottom:6px",
            ".inspiracion": "margin-left:36px",
            ".alts": "margin-left:36px",
            ".cita": "margin-left:36px",
        },
    },
    "v3_banda": {
        "label": "V3 frasco en banda superior (packshot vertical)",
        "css": {
            ".hero": "flex-direction:column;gap:14px;align-items:center;margin:0",
            ".frasco-col": "width:100%;flex-direction:row;justify-content:center;height:330px",
            ".frasco-figura": "height:320px",
            ".hero-txt": "width:100%",
            "h1": "font-size:58px;text-align:center",
            ".casa": "text-align:center",
            ".sub": "text-align:center",
            ".datos-hero": "align-items:center",
            ".rating-line": "justify-content:center",
            ".pir3d-svg": "width:400px;height:190px",
            ".inspiracion": "margin-left:0",
            ".alts": "margin-left:0",
            ".cita": "margin-left:0",
        },
    },
}

MEASURE_JS = """
<script>
window.addEventListener('load', function () {
  try {
    var H = %(H)d, W = %(W)d, PAD = %(PAD)d, PAD_BOTTOM = %(PB)d;
    var q = function (s) { return document.querySelector(s); };
    var secs = Array.prototype.slice.call(document.querySelectorAll('.sec'));
    var pie = q('.pie');
    var last = secs.length ? secs[secs.length - 1] : null;
    var r = function (el) { return el ? el.getBoundingClientRect() : null; };
    var pieR = r(pie), lastR = r(last);
    var gaps = [];
    for (var i = 1; i < secs.length; i++) {
      gaps.push(Math.round(r(secs[i]).top - r(secs[i - 1]).bottom));
    }
    var fuera = [];
    ['.casa', 'h1', '.datos-hero', '.pir3d-wrap', '.alts', '.cita', '.pie', '.nota-fondo'].forEach(function (s) {
      var e = q(s); if (!e) return; var b = r(e);
      if (b.left < PAD - 1 || b.right > W - PAD + 1) fuera.push(s);
    });
    var boxes = {};
    ['.dh', '.inspiracion p', '.cita blockquote', '.alt-n'].forEach(function (s) {
      var e = q(s); if (!e) return; var b = r(e);
      boxes[s] = [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)];
    });
    // elemento mas bajo del documento: quien provoca el desborde si lo hay
    var maxBottom = 0, culprit = null;
    Array.prototype.slice.call(document.querySelectorAll('body *')).forEach(function (el) {
      var style = getComputedStyle(el);
      if (style.position === 'absolute' || style.position === 'fixed') return;
      var b = r(el);
      if (b && b.bottom > maxBottom) { maxBottom = b.bottom; culprit = el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''); }
    });
    var data = {
      variante: %(VAR)s,
      scroll: document.documentElement.scrollHeight,
      body_scroll: document.body.scrollHeight,
      overflow: Math.max(0, document.body.scrollHeight - H, document.documentElement.scrollHeight - H),
      max_bottom: Math.round(maxBottom),
      culprit: culprit,
      last_bottom: lastR ? Math.round(lastR.bottom) : null,
      pie_top: pieR ? Math.round(pieR.top) : null,
      aire: (pieR && lastR) ? Math.round(pieR.top - lastR.bottom) : null,
      pie_dentro: pieR ? Math.round(H - PAD_BOTTOM - pieR.bottom) : null,
      gaps: gaps,
      gap_min: gaps.length ? Math.min.apply(null, gaps) : null,
      fuera: fuera,
      boxes: boxes,
      fonts: document.fonts ? document.fonts.status : 'n/a',
      wide_ok: document.fonts ? document.fonts.check('16px "Playfair Display"') : null
    };
    document.title = 'METRICS::' + JSON.stringify(data);
  } catch (e) {
    document.title = 'METRICS::{"error":"' + String(e).replace(/"/g, "'") + '"}';
  }
});
</script>
"""


def lum(px):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(px[0]) + 0.7152 * ch(px[1]) + 0.0722 * ch(px[2])


def contrast_in_box(img, box):
    """Contraste medido: percentil 95 de luminancia = fondo, percentil 5 = texto."""
    from PIL import Image
    x1, y1, x2, y2 = box
    crop = img.crop((max(0, x1), max(0, y1), min(img.width, x2), min(img.height, y2))).convert("RGB")
    if crop.width < 4 or crop.height < 4:
        return None
    vals = sorted(lum(p) for p in crop.getdata())
    n = len(vals)
    lo, hi = vals[max(0, int(n * 0.05) - 1)], vals[min(n - 1, int(n * 0.95))]
    return round((hi + 0.05) / (lo + 0.05), 2)


def build_html(tok, name, preset):
    html = BASE.read_text(encoding="utf-8", errors="replace")
    H = tok["canvas"]["vigente"]["height"]
    W = tok["canvas"]["vigente"]["width"]
    pad = tok["layout"]["padding"]["x"]

    # assets absolutos: el HTML vive en out/, no en la carpeta original
    for asset in ("towncountry_figura.png", "towncountry_fondo_c.png", "qr_fragrantica.png"):
        src = (BASE.parent / asset).resolve()
        html = html.replace(f"'{asset}'", f"'{src.as_uri()}'").replace(f'"{asset}"', f'"{src.as_uri()}"')

    rules = "\n".join(f"{sel}{{{css} !important}}" for sel, css in preset["css"].items())
    inject = f"""
<style id="tokens">
html, body {{ width:{W}px !important; height:{H}px !important; }}
.content {{ height:{H}px !important;
  padding:{tok['layout']['padding']['top']}px {pad}px {tok['layout']['padding']['bottom']}px !important; }}
{rules}
</style>
"""
    html = html.replace("</head>", inject + "</head>")
    html = html.replace("</body>", MEASURE_JS % {"H": H, "W": W, "PAD": pad, "PB": tok["layout"]["padding"]["bottom"], "VAR": json.dumps(name)} + "</body>")
    return html


def render(path_html, path_png, H, W):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
           f"--window-size={W},{H}", "--force-device-scale-factor=1",
           "--virtual-time-budget=4000", f"--screenshot={path_png}", path_html.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stderr or "").strip().splitlines()[-1:] if r.stderr else []


def dump_metrics(path_html):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--virtual-time-budget=4000", "--dump-dom", path_html.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    m = re.search(r"<title>METRICS::(.*?)</title>", r.stdout, re.S)
    if not m:
        return {"error": "sin METRICS en el DOM", "rc": r.returncode}
    try:
        return json.loads(m.group(1).replace("&quot;", '"'))
    except json.JSONDecodeError as e:
        return {"error": f"json invalido: {e}", "raw": m.group(1)[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()

    tok = yaml.safe_load(TOKENS.read_text(encoding="utf-8"))
    H, W = tok["canvas"]["vigente"]["height"], tok["canvas"]["vigente"]["width"]
    if not BASE.exists():
        sys.exit(f"FALTA la pieza base: {BASE}")
    OUT.mkdir(exist_ok=True)

    results = []
    for name, preset in PRESETS.items():
        if a.only and name != a.only:
            continue
        p_html = OUT / f"{name}.html"
        p_html.write_text(build_html(tok, name, preset), encoding="utf-8")
        rec = {"variante": name, "label": preset["label"], "html_bytes": p_html.stat().st_size}
        if not a.no_render:
            p_png = OUT / f"{name}.png"
            rc, err = render(p_html, p_png, H, W)
            rec["render_rc"] = rc
            rec["png"] = str(p_png) if p_png.exists() else None
            rec.update(dump_metrics(p_html))
            if p_png.exists():
                from PIL import Image
                img = Image.open(p_png)
                rec["png_size"] = list(img.size)
                rec["contraste"] = {}
                for sel, box in (rec.get("boxes") or {}).items():
                    if box[3] - box[1] >= 4:
                        rec["contraste"][sel] = contrast_in_box(img, box)
        results.append(rec)
        print(json.dumps(rec, ensure_ascii=False)[:400])

    (OUT / "report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== TABLA ===")
    print(f"{'variante':14} {'overflow':>8} {'aire':>6} {'gap_min':>7} {'fuera':>5} {'cuerpo':>7} {'cita':>5}")
    for r in results:
        c = r.get("contraste") or {}
        print(f"{r['variante']:14} {str(r.get('overflow','-')):>8} {str(r.get('aire','-')):>6} "
              f"{str(r.get('gap_min','-')):>7} {str(len(r.get('fuera',[]))):>5} "
              f"{str(c.get('.dh','-')):>7} {str(c.get('.cita blockquote','-')):>5}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
