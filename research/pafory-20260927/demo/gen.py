#!/usr/bin/env python3
"""Demo: pack de colaborador (pagina de creador + 3 anuncios + informe) para el hueco ES.
Todo CSS, sin assets externos (render determinista). Marca de EJEMPLO bien visible."""
import json, pathlib, re, subprocess, sys

D = pathlib.Path("/tmp/pafory-demo")
D.mkdir(parents=True, exist_ok=True)
CHROME = "/usr/bin/google-chrome"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;
     background:#0e0e11;color:#eee;-webkit-font-smoothing:antialiased}
.canvas{width:1080px;height:%H%px;position:relative;overflow:hidden;
     background:radial-gradient(120% 80% at 20% 0%,#23202a 0%,#0e0e11 60%)}
.wrap{padding:54px 64px 0}
.tag{display:inline-block;font-size:17px;letter-spacing:2.5px;text-transform:uppercase;
     color:#c8a24a;border:1px solid #c8a24a55;border-radius:999px;padding:8px 18px}
.demo{position:absolute;top:26px;right:26px;font-size:15px;letter-spacing:2px;
     color:#ff5c5c;border:1px dashed #ff5c5c88;border-radius:6px;padding:6px 12px}
h1{font-size:56px;line-height:1.06;margin:26px 0 10px;letter-spacing:-1px}
h1 em{color:#c8a24a;font-style:normal}
.sub{font-size:22px;color:#a5a1ac;line-height:1.4}
.card{background:#17171d;border:1px solid #ffffff12;border-radius:18px;padding:26px 30px;margin-top:26px}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:20px;
     padding:13px 0;border-bottom:1px solid #ffffff0d;font-size:21px}
.row:last-child{border-bottom:0}
.row .k{color:#c9c6d1}
.row .v{color:#fff;font-weight:700}
.code{background:linear-gradient(90deg,#c8a24a22,#c8a24a08);border:1px solid #c8a24a66;
      border-radius:18px;padding:26px 30px;margin-top:24px;display:flex;
      justify-content:space-between;align-items:center}
.code .lbl{font-size:18px;letter-spacing:2px;color:#c8a24a;text-transform:uppercase}
.code .val{font-size:46px;font-weight:700;letter-spacing:1px;color:#fff;margin-top:6px}
.code .off{font-size:20px;color:#c9c6d1;margin-top:4px}
.bullets{list-style:none;margin-top:8px}
.bullets li{font-size:20px;color:#c9c6d1;line-height:1.5;padding-left:30px;position:relative;margin-top:10px}
.bullets li:before{content:"";position:absolute;left:6px;top:11px;width:9px;height:9px;
     border-radius:50%;background:#c8a24a}
.pie{margin-top:30px;font-size:16px;color:#7d7a85;line-height:1.5;border-top:1px solid #ffffff10;padding-top:14px}
.sec{font-size:16px;letter-spacing:2.5px;text-transform:uppercase;color:#8f8b98;margin-top:26px}
/* anuncios */
.ad{width:1080px;height:1080px;padding:78px 72px;display:flex;flex-direction:column;
    justify-content:space-between;position:relative;overflow:hidden;
    background:radial-gradient(110% 90% at 80% 0%,#2a2320 0%,#100f13 62%)}
.ad .hook{font-size:92px;line-height:1.02;font-weight:700;letter-spacing:-2px}
.ad .hook em{color:#c8a24a;font-style:normal}
.ad .kicker{font-size:24px;letter-spacing:3px;text-transform:uppercase;color:#c8a24a}
.ad .body{font-size:30px;color:#cfccd6;line-height:1.35;margin-top:22px}
.ad .cta{display:inline-block;background:#c8a24a;color:#14131a;font-size:28px;font-weight:700;
    padding:20px 34px;border-radius:12px}
.ad .cta small{display:block;font-size:19px;font-weight:400;margin-top:6px;color:#3a3423}
.bars{display:flex;align-items:flex-end;gap:26px;height:250px;margin-top:14px}
.bar{flex:1;text-align:center}
.bar i{display:block;background:linear-gradient(180deg,#c8a24a,#8d6f2c);border-radius:8px 8px 0 0}
.bar span{display:block;font-size:18px;color:#9b98a3;margin-top:10px}
.bar b{display:block;font-size:20px;color:#fff;margin-bottom:8px}
"""

def page(name, height, body, css_extra="", wrapper="wrap"):
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>{name}</title><style>{CSS.replace('%H%', str(height))}{css_extra}</style></head>
<body><div class="canvas"><div class="demo">EJEMPLO</div><div class="{wrapper}">{body}</div></div></body></html>"""
    (D / f"{name}.html").write_text(html, encoding="utf-8")

# ---------- 1. PAGINA DE CREADOR ----------
page("01_pagina_creador", 1350, """
<span class="tag">Casa Ejemplo · Perfumería de nicho</span>
<h1>Página de <em>colaboración</em></h1>
<div class="sub">Todo lo que necesita la creadora para publicar hoy: su código, su enlace
con seguimiento y su selección. Sin PDFs, sin correos de ida y vuelta.</div>

<div class="card">
  <div class="row"><span class="k">Creadora</span><span class="v">@creador_ejemplo · YouTube 24,3 mil</span></div>
  <div class="row"><span class="k">Formato acordado</span><span class="v">Reel 9:16 + 3 stories</span></div>
  <div class="row"><span class="k">Ventana de atribución</span><span class="v">30 días</span></div>
  <div class="row"><span class="k">Comisión por venta</span><span class="v">22 € / 7%</span></div>
</div>

<div class="code">
  <div><div class="lbl">Su código</div><div class="val">EJEMPLO55</div>
       <div class="off">55% en el primer pedido</div></div>
  <div><div class="lbl">Su enlace</div>
       <div class="off" style="font-size:17px">casa-ejemplo.es/su-seleccion<br>
       ?creator=creador_ejemplo<br>&amp;utm_medium=influencer<br>&amp;utm_campaign=10-26_cold_reel</div></div>
</div>

<div class="sec">Su selección (3 de 24)</div>
<div class="card">
  <div class="row"><span class="k">Symphony · Louis Vuitton</span><span class="v">≈539 € / 100 ml</span></div>
  <div class="row"><span class="k">Ojar · Oud &amp; Bergamot</span><span class="v">185 € / 50 ml</span></div>
  <div class="row"><span class="k">Memoize London · Iris</span><span class="v">165 € / 50 ml</span></div>
</div>

<div class="sec">Cómo se mide</div>
<ul class="bullets">
  <li>Código propio por creadora: cada venta queda atribuida a su nombre.</li>
  <li>Enlace con <b>creator=</b> + UTMs normalizados (campaña, formato, fecha).</li>
  <li>Informe mensual: clics, pedidos, ingresos y comisión. Se entrega día 1.</li>
</ul>

<div class="pie">Pieza generada con el pipeline del lab (HTML→PNG determinista) el 27-09-2026.
Los nombres, el código y los precios son de EJEMPLO: no corresponden a una colaboración real.</div>
""")

# ---------- 2. PACK DE ANUNCIOS (3 variantes) ----------
page("02_anuncio_a", 1080, """
<div class="kicker">Anuncio · variante A · gancho regalo</div>
<div><div class="hook">El regalo que<br><em>no falla</em>.</div>
  <div class="body">24 fragancias de nicho detrás de 24 puertas. Edición limitada.</div></div>
<div><span class="cta">Reservar el mío<small>código EJEMPLO55</small></span></div>
""", wrapper="ad")

page("03_anuncio_b", 1080, """
<div class="kicker">Anuncio · variante B · gancho descubrimiento</div>
<div><div class="hook">Tu próximo<br>perfume lo<br><em>eliges tú</em>.</div>
  <div class="body">Una fragancia nueva cada mes, 8 ml, entre más de 600 de nicho y lujo.</div></div>
<div><span class="cta">Primer mes 9,50 €<small>envío gratis · código EJEMPLO55</small></span></div>
""", wrapper="ad")

page("04_anuncio_c", 1080, """
<div class="kicker">Anuncio · variante C · gancho prueba social</div>
<div><div class="hook">4,6★ con<br><em>1.800+</em><br>reseñas.</div>
  <div class="body">Solo originales, sin dupes. Perfume de nicho sin pagar el frasco grande.</div></div>
<div><span class="cta">Descubrir la selección<small>código EJEMPLO55</small></span></div>
""", wrapper="ad")

# ---------- 3. INFORME POR CREADOR ----------
page("05_informe_creador", 1350, """
<span class="tag">Informe por creadora · ejemplo de mes</span>
<h1>@creador_ejemplo<br><em>octubre 2026</em></h1>
<div class="sub">Datos del panel interno: cada cifra sale del código y del enlace con <b>creator=</b>.
Esto es lo que recibe la marca — y lo que justifica renovar la colaboración.</div>

<div class="card">
  <div class="row"><span class="k">Visitas con su enlace</span><span class="v">12.480</span></div>
  <div class="row"><span class="k">Clics únicos</span><span class="v">1.204 (9,6%)</span></div>
  <div class="row"><span class="k">Pedidos atribuidos</span><span class="v">86</span></div>
  <div class="row"><span class="k">Ingresos atribuidos</span><span class="v">2.494 €</span></div>
  <div class="row"><span class="k">Comisión de la creadora</span><span class="v">880 €</span></div>
  <div class="row"><span class="k">Coste por pedido</span><span class="v">10,23 €</span></div>
</div>

<div class="sec">Pedidos por semana</div>
<div class="bars">
  <div class="bar"><b>24</b><i style="height:120px"></i><span>S1</span></div>
  <div class="bar"><b>31</b><i style="height:165px"></i><span>S2</span></div>
  <div class="bar"><b>19</b><i style="height:95px"></i><span>S3</span></div>
  <div class="bar"><b>12</b><i style="height:60px"></i><span>S4</span></div>
</div>

<div class="sec">Lectura</div>
<ul class="bullets">
  <li>El pico cae en la semana 2: es cuando publicó el vídeo largo. Las stories solas no sostienen.</li>
  <li>La mitad de los pedidos son del frasco pequeño: el código convierte, el ticket alto no.</li>
  <li>Propuesta: renovar 3 meses con una pieza larga al mes, no 4 stories semanales.</li>
</ul>

<div class="pie">Cifras de EJEMPLO (simuladas) para mostrar el formato del informe, no datos reales.
Un informe real se genera con los parámetros creator= y UTM del panel de la tienda.</div>
""")

# ---------- render + check ----------
CHECK = """<pre id="checkout"></pre><script>
document.getElementById('checkout').textContent=JSON.stringify({
canvas:document.querySelector('.canvas').offsetHeight,
h:document.body.scrollHeight,
pie:Math.round((document.querySelector('.pie')||document.querySelector('.cta')).getBoundingClientRect().bottom)});
</script>"""

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

results = []
for p in sorted(x for x in D.glob("*.html") if not x.name.startswith("chk_")):
    # altura esperada por pieza
    exp = {1: 1350, 2: 1080, 3: 1080, 4: 1080, 5: 1350}[int(p.name[:2])]
    chk = D / f"chk_{p.name}"
    chk.write_text(p.read_text(encoding="utf-8").replace("</body>", CHECK + "</body>"), encoding="utf-8")
    dom = run(f'{CHROME} --headless=new --disable-gpu --virtual-time-budget=8000 --dump-dom "file://{chk}"')
    m = re.search(r'<pre id="checkout">(.*?)</pre>', dom.stdout, re.S)
    data = json.loads(m.group(1)) if m else {}
    png = D / (p.stem + ".png")
    run(f'{CHROME} --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 '
        f'--virtual-time-budget=8000 --window-size=1080,{exp} --screenshot="{png}" "file://{p}"')
    from PIL import Image
    sz = Image.open(png).size
    results.append((p.name, exp, data.get("canvas"), data.get("h"), round(data.get("pie", 0)), sz))

for r in sorted(results):
    ok = (r[2] == r[1]) and (r[4] <= r[1]) and (r[5] == (1080, r[1]))
    print(f"{'OK ' if ok else 'REV'} {r[0]:24s} lienzo={r[1]} canvas={r[2]} scrollHeight={r[3]} pieBottom={r[4]} png={r[5]}")
