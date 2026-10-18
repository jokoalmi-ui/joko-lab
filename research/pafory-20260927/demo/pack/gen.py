#!/usr/bin/env python3
"""Genera el pack de colaboradoras (10 piezas HTML→PNG) y verifica cada una.
Determinista: Inter local, SVG inline, sin recursos de red.
Uso: python3 gen.py [--solo nombre_pieza]"""
import json, pathlib, re, subprocess, sys
from PIL import Image

import index as IDX
import p_front, p_sys, p_ads, p_story_brief, p_report
import case as C

REG = [p_front, p_sys, p_ads, p_story_brief, p_report]
RESTOS = ("{C.", "{IDX.", "{A[", "{D[", "{p[", "{f[")

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
CHROME = "/usr/bin/google-chrome"
CHECK_JS = """<pre id="checkout"></pre><script>
const last=[...document.querySelectorAll('.ft,.btn,.chart,.kpi,.linkbox')].pop();
document.getElementById('checkout').textContent=JSON.stringify({
canvas:document.querySelector('.piece').offsetHeight,
scroll:document.body.scrollHeight,
last:Math.round((last||document.querySelector('.piece')).getBoundingClientRect().bottom)});
</script>"""

def html(nombre, h, body, wrap, css):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>{nombre} · pack de colaboradoras</title><style>{css}</style></head>
<body><div class="piece"><div class="demo">EJEMPLO</div><div class="{wrap}">{body}</div></div></body></html>"""

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def main(solo=None):
    orden = {p[0]: i for i, p in enumerate(IDX.PIEZAS)}
    piezas = sorted([p for m in REG for p in m.PIEZAS], key=lambda p: orden[p["name"]])
    idx_names = [p[0] for p in IDX.PIEZAS]
    print("== índice vs realidad ==")
    ok_idx = [p["name"] for p in piezas] == idx_names
    print(f"{'OK  ' if ok_idx else 'FAIL'} piezas generadas ({len(piezas)}) == índice ({IDX.TOTAL}): "
          f"{[p['name'] for p in piezas] if not ok_idx else 'mismo orden y nombres'}")
    faltan = [n for n in idx_names if n not in [p["name"] for p in piezas]]
    sobran = [p["name"] for p in piezas if p["name"] not in idx_names]
    if faltan or sobran:
        print(f"FAIL índice desajustado · faltan={faltan} sobran={sobran}")

    res, fallos = [], 0
    for p in piezas:
        if solo and p["name"] != solo:
            continue
        exp = dict((n, h) for n, h, *_ in IDX.PIEZAS)[p["name"]]
        if exp != p["h"]:
            print(f"FAIL {p['name']}: altura {p['h']} != índice {exp}"); fallos += 1
        f = OUT / f"{p['name']}.html"
        texto = html(p["name"], p["h"], p["body"], p["wrap"], p["css"])
        restos = [r for r in RESTOS if r in texto.replace("&amp;", "&")]
        if restos:
            print(f"FAIL {p['name']}: marcador de plantilla sin sustituir {restos}")
            fallos += 1
        if "{C." in texto or "{IDX." in texto:
            print(f"FAIL {p['name']}: f-string sin formatear")
            fallos += 1
        f.write_text(texto, encoding="utf-8")
        chk = OUT / f"chk_{p['name']}.html"
        chk.write_text(f.read_text(encoding="utf-8").replace("</body>", CHECK_JS + "</body>"), encoding="utf-8")
        dom = run(f'{CHROME} --headless=new --disable-gpu --virtual-time-budget=6000 --dump-dom "file://{chk}"')
        m = re.search(r'<pre id="checkout">(.*?)</pre>', dom.stdout, re.S)
        d = json.loads(m.group(1)) if m else {}
        png = OUT / f"{p['name']}.png"
        run(f'{CHROME} --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 '
            f'--font-render-hinting=none --virtual-time-budget=6000 --window-size=1080,{p["h"]} '
            f'--screenshot="{png}" "file://{f}"')
        sz = Image.open(png).size
        ok = (d.get("canvas") == p["h"]) and (d.get("scroll", 10**9) <= p["h"]) \
             and (d.get("last", 10**9) <= p["h"]) and (sz == (1080, p["h"]))
        if not ok:
            fallos += 1
        res.append((p["name"], p["h"], d.get("canvas"), d.get("scroll"), d.get("last"), sz, ok))
        print(f"{'OK  ' if ok else 'REV '} {p['name']:22s} alto={p['h']:4d} lienzo={d.get('canvas')} "
              f"scroll={d.get('scroll')} ultimo={d.get('last')} png={sz}")

    print("\n== coherencia de cifras ==")
    for l in C.check()[0]:
        print("   " + l)
    if not C.check()[1]:
        fallos += 1

    print(f"\n== resultado: {len(res)} piezas renderizadas · {fallos} incidencias ==")
    return 1 if fallos else 0

if __name__ == "__main__":
    solo = sys.argv[sys.argv.index("--solo")+1] if "--solo" in sys.argv else None
    sys.exit(main(solo))
