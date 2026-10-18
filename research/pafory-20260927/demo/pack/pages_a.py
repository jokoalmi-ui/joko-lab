"""Piezas 00-05: portada, página de creadora, sistema de atribución y 3 anuncios."""
from tokens import piece, header, footer
import art
import case as C
import index as IDX

D = C.D
PIEZAS = []

def add(name, h, body, wrap="pad", css=""):
    exp = TIT[name][1]
    assert h == exp, f"{name}: altura {h} != índice {exp}"
    PIEZAS.append(piece(name, exp, body, wrap, css))

TIT = {p[0]: p for p in IDX.PIEZAS}

def pie(n, extra=""):
    t = TIT[n]
    return footer(f"<b>{C.CLIENTE}</b> · {C.CLIENTE_SUB} · <span style='color:#8E96A5'>datos de EJEMPLO</span>",
                  f"{t[2]} · pieza {int(t[0][:2]) + 1} / {IDX.TOTAL}{(' · ' + extra) if extra else ''}")

# ============================== 00 PORTADA ==============================
mitad = 5
cols = []
for i in (0, 1):
    regs = IDX.PIEZAS[i*mitad:(i+1)*mitad]
    items = "".join(
        f'<div class="kv"><span class="k" style="font-size:21px">{int(n[:2]) + 1} · {t}</span></div>'
        for n, h, t, d in regs)
    cols.append(f'<div class="card flat grow">{items}</div>')

add("00_portada", 1527, f"""
{header(C.CLIENTE, "pack de colaboradoras", C.INICIALES)}
<div style="margin-top:44px">
  <div class="eyebrow">ejemplo de entrega · cliente y datos ficticios</div>
  <div class="display">Sistema de<br><em class="g">colaboradoras</em></div>
  <div class="lead" style="max-width:960px">Página por creadora, cupón con seguimiento, anuncios listos,
  brief de campaña y el panel que responde una sola pregunta: <b>qué venta vino de quién</b>.
  Son {IDX.TOTAL} piezas.</div>
</div>
<div class="kpis" style="margin-top:26px">
  <div class="kpi"><div class="lbl">Creadoras activas</div><div class="big">3</div>
    <div class="note">con cupón y enlace propios</div></div>
  <div class="kpi"><div class="lbl">Pedidos atribuidos</div><div class="big">{C.inte(D['ped'])}</div>
    <div class="note">{C.MES}</div></div>
  <div class="kpi"><div class="lbl">Ingresos atribuidos</div><div class="big" style="font-size:34px">{C.eur(D['ing'])}</div>
    <div class="note">ticket medio {C.eur(D['ticket'])}</div></div>
  <div class="kpi"><div class="lbl">Retorno</div><div class="big">{f"{D['roas']:.1f}".replace('.', ',')}×</div>
    <div class="note">sobre comisiones + gestión</div></div>
</div>
<div class="eyebrow" style="margin-top:30px">índice del pack</div>
<div class="row" style="gap:18px;margin-top:14px">{''.join(cols)}</div>
<div class="micro" style="margin-top:12px">Cada pieza se entrega en PNG a tamaño de
publicación y en su fichero editable, con los textos y las cifras a la vista.</div>
<div class="spacer"></div>
{pie("00_portada", "generado 27-09-2026")}
""")

# ============================== 01 PÁGINA DE CREADORA ==============================
ana = D["filas"][0]
prods = "".join(f"""
  <div class="prod">{art.vial(96, 176, t[0], t[1])}
    <div class="nm">{p['nm']}</div><div class="ml">{p['ml']} · {p['nota']}</div>
    <div class="pr">{C.eur(p['pr'])}</div></div>"""
  for p, t in zip(C.PRODUCTOS, [("#E7CB84", "#A97F2E"), ("#9FD4C4", "#4E8C7C"), ("#B7C4E8", "#5C6FA8")]))

fila_prods = "".join(f"""
  <div class="rowprod">{art.vial(52, 96, t[0], t[1])}
    <div class="grow"><div class="nm">{p['nm']}</div><div class="ml">{p['ml']} · {p['nota']}</div></div>
    <div class="pr">{C.eur(p['pr'])}<div class="micro" style="font-weight:400">comisión {C.eur(p['pr']*C.COMISION_PCT)}</div></div>
  </div>"""
  for p, t in zip(C.PRODUCTOS, [("#E7CB84", "#A97F2E"), ("#9FD4C4", "#4E8C7C"), ("#B7C4E8", "#5C6FA8")]))

add("01_pagina_creadora", 1920, f"""
{header(C.CLIENTE, "página de creadora", C.INICIALES)}
<div class="row between" style="margin-top:34px">
  <div>
    <div class="eyebrow">colaboradora · {C.MES}</div>
    <div class="h1" style="margin-top:10px">{ana['nom']}<br><em class="g">{ana['h']}</em></div>
  </div>
  <div class="card gold" style="text-align:center;padding:20px 26px">
    <div class="eyebrow" style="color:#E7CB84">cupón</div>
    <div style="font-size:44px;font-weight:800;letter-spacing:1px;margin-top:6px">{C.CUPON}</div>
    <div class="micro">{C.pct(C.DESCUENTO_PILOTO,0)} en su selección</div>
  </div>
</div>
<div class="lead">Su página, su cupón y su enlace. Todo en una URL que puede abrir desde el móvil:
nada que negociar por correo ni PDFs que se pierden.</div>

<div class="card" style="margin-top:26px">
  <div class="kv"><span class="k">Su red y su formato</span><span class="v">{ana['red']} · {ana['formato']}</span></div>
  <div class="kv"><span class="k">Ventana de atribución</span><span class="v">30 días, último clic</span></div>
  <div class="kv"><span class="k">Comisión</span><span class="v">{C.pct(C.COMISION_PCT,0)} del pedido atribuido</span></div>
  <div class="kv"><span class="k">Pago</span><span class="v">el día 5 de cada mes, por transferencia</span></div>
</div>

<div class="eyebrow" style="margin-top:30px">su enlace, con seguimiento</div>
<div class="linkbox" style="margin-top:12px">
  <div class="u">casaaurora.example/ana-decants?creator={C.UTM['creator']}<br>
  &amp;utm_source={C.UTM['utm_source']}&amp;utm_medium={C.UTM['utm_medium']}&amp;utm_campaign={C.UTM['utm_campaign']}</div>
</div>

<div class="eyebrow" style="margin-top:30px">su selección · 3 de 24 referencias</div>
<div class="card" style="margin-top:12px;padding:10px 30px">{fila_prods}</div>

<div class="eyebrow" style="margin-top:30px">cómo funciona</div>
<div class="steps" style="margin-top:12px">
  <div class="step"><div class="n">1</div><div><div class="t">Publica y comparte su enlace</div>
    <div class="d">Enlace en la descripción de la pieza y en su bio. El cupón {C.CUPON} sirve en la tienda.</div></div></div>
  <div class="step"><div class="n">2</div><div><div class="t">Su audiencia compra con su cupón</div>
    <div class="d">Cada pedido queda marcado con su código: no hay que preguntar a nadie de dónde vino.</div></div></div>
  <div class="step"><div class="n">3</div><div><div class="t">Cobra el día 5 con su informe</div>
    <div class="d">Recibe el detalle de clics, pedidos, ingresos y comisión del mes. Sin reclamar nada.</div></div></div>
</div>
<div class="spacer"></div>
{pie("01_pagina_creadora")}
""")

# ============================== 02 SISTEMA DE ATRIBUCIÓN ==============================
cajas = [("Cupón en el carrito", "el cliente escribe el código", art.ic_code()),
         ("Enlace con parámetros", "creator= + utm_*", art.ic_link()),
         ("Pedido con origen", "la tienda lo guarda", art.ic_cart()),
         ("Comisión calculada", "el panel suma y factura", art.ic_chart())]
flow = '<div class="arrow">→</div>'.join(
    f'<div class="box">{ic}<div class="t">{t}</div><div class="d">{d}</div></div>' for t, d, ic in cajas)

add("02_sistema_atribucion", 1350, f"""
{header(C.CLIENTE, "sistema de atribución", C.INICIALES)}
<div class="h1" style="margin-top:30px">Cómo se atribuye <em class="g">una venta</em></div>
<div class="lead">Cuatro eslabones, ninguno depende de la memoria de nadie. Si un eslabón falta,
la venta no se cuenta: el sistema es honesto por diseño.</div>
<div class="flow" style="margin-top:30px">{flow}</div>

<div class="eyebrow" style="margin-top:32px">parámetros que viajan en cada enlace</div>
<div class="linkbox" style="margin-top:12px">
  <div class="u">?creator={C.UTM['creator']}&amp;utm_source={C.UTM['utm_source']}<br>
  &amp;utm_medium={C.UTM['utm_medium']}&amp;utm_campaign={C.UTM['utm_campaign']}<br>
  &amp;ref={C.UTM['ref']}</div>
</div>

<div class="row" style="gap:18px;margin-top:28px">
  <div class="card flat grow">
    <div class="eyebrow">reglas fijadas antes de empezar</div>
    <ul class="list" style="margin-top:12px">
      <li>La ventana es de <b>30 días</b> desde el clic.</li>
      <li>Si hay dos creadoras en el mismo pedido, gana <b>el último clic</b>.</li>
      <li>Los pedidos <b>devueltos no generan comisión</b>.</li>
      <li>Solo se guarda el <b>pedido y el código</b>, nunca datos de la audiencia.</li>
    </ul>
  </div>
  <div class="card flat grow">
    <div class="eyebrow">lo que no se puede medir</div>
    <ul class="list no" style="margin-top:12px">
      <li>Ventas por teléfono o en tienda física.</li>
      <li>Recomendaciones sin enlace ni cupón.</li>
      <li>Guardados, me gusta y reproducciones: solo los da la plataforma.</li>
    </ul>
    <div class="micro" style="margin-top:14px">Ponerlo por escrito evita discusiones de fin de mes.
    Lo que no se puede medir se dice antes, no después.</div>
  </div>
</div>
<div class="spacer"></div>
{pie("02_sistema_atribucion")}
""")

# ============================== 03-05 ANUNCIOS ==============================
CSS_AD = """
.state{display:flex;flex-direction:column;flex:1;justify-content:space-between}
.hero{display:flex;align-items:center;justify-content:center;gap:40px}
"""
add("03_anuncio_a", 1350, f"""
<div class="top"><span class="chip flat">variante A · producto · 4:5</span>
<span class="brand" style="font-size:20px"><span class="mark" style="width:32px;height:32px;font-size:16px">{C.INICIALES}</span>{C.CLIENTE}</span></div>
<div class="state" style="margin-top:40px">
  <div class="eyebrow gold">decants originales · 10 ml</div>
  <div class="hero" style="margin-top:26px">
    {art.bottle(210, 350, "#E7CB84", "#A97F2E")}
    <div>
      <div style="font-size:82px;font-weight:800;line-height:1.02;letter-spacing:-2.4px">
        El frasco grande,<br><em class="g">sin el frasco grande</em>.</div>
      <div class="body" style="margin-top:20px;font-size:25px">10 ml de original dan para 20-30 usos.
      Se prueba, se decide, y solo entonces se compra el grande.</div>
    </div>
  </div>
  <div class="row between" style="align-items:flex-end">
    <div class="pills"><span class="pill on">desde {C.eur(19.0,0)}</span>
      <span class="pill">envío gratis desde 50 €</span><span class="pill">devolución 14 días</span></div>
    <div class="btn">Ver la selección<small>cupón {C.CUPON} · {C.pct(C.DESCUENTO_PILOTO,0)}</small></div>
  </div>
</div>
""", css=CSS_AD)

add("04_anuncio_b", 1350, f"""
<div class="top"><span class="chip flat">variante B · selección · 4:5</span>
<span class="brand" style="font-size:20px"><span class="mark" style="width:32px;height:32px;font-size:16px">{C.INICIALES}</span>{C.CLIENTE}</span></div>
<div class="state" style="margin-top:34px">
  <div>
    <div class="eyebrow gold">tres fragancias, tres perfiles</div>
    <div style="font-size:70px;font-weight:800;line-height:1.03;letter-spacing:-2.2px;margin-top:16px">
      Tres fragancias.<br><em class="g">Cero frascos que sobran</em>.</div>
    <div class="card" style="margin-top:28px;padding:6px 30px">
      {''.join(f'''<div class="rowprod"><div class="grow"><div class="nm">{p['nm']}</div>
        <div class="ml">{p['nota']}</div></div>
        <div class="pr">{C.eur(p['pr'])}</div></div>''' for p in C.PRODUCTOS)}
    </div>
    <div class="body" style="margin-top:20px;font-size:23px">Decantados a mano en Bilbao, el mismo día
    del pedido. Si no aciertas, no has gastado 200 € para averiguarlo.</div>
  </div>
  <div class="row between" style="align-items:flex-end">
    <div class="small">Cupón <b class="gold">{C.CUPON}</b> · {C.pct(C.DESCUENTO_PILOTO,0)} en tu primera selección</div>
    <div class="btn">Elegir las mías<small>3 × 10 ml desde {C.eur(19.0,0)}</small></div>
  </div>
</div>
""", css=CSS_AD)

add("05_anuncio_c", 1350, f"""
<div class="top"><span class="chip flat">variante C · prueba social · 4:5</span>
<span class="brand" style="font-size:20px"><span class="mark" style="width:32px;height:32px;font-size:16px">{C.INICIALES}</span>{C.CLIENTE}</span></div>
<div class="state" style="margin-top:34px">
  <div>
    <div class="row between">
      <div>{art.stars(5, 34)}<div class="small" style="margin-top:10px"><b>4,8 sobre 5</b> · 312 reseñas verificadas</div></div>
      <div class="card flat" style="padding:18px 24px;text-align:right">
        <div class="eyebrow">recomendarían</div>
        <div style="font-size:38px;font-weight:800;margin-top:4px">94<span style="font-size:22px"> %</span></div>
      </div>
    </div>
    <div class="quote" style="margin-top:36px">
      <div class="qm">“</div>
      <div class="txt">Pedí tres decants para dejar de comprar a ciegas. Llevo dos meses
      sin tirar dinero en un frasco entero que no era para mí.</div>
      <div class="who">{art.avatar("LM", 58)}
        <div><div class="small" style="color:#F4F5F7"><b>Lucía M.</b> · clienta desde marzo</div>
        <div class="micro">reseña publicada en la ficha de Verde Norte</div></div></div>
    </div>
    <div class="card" style="margin-top:32px;padding:22px 26px">
      <div class="row between">
        <div class="small">Originales decantados a mano · sin equivalencias ni «dupes»</div>
        <div class="tagmini">cupón {C.CUPON}</div>
      </div>
    </div>
  </div>
  <div class="row between" style="align-items:flex-end">
    <div class="small">Deciden <b>3 de cada 4</b> que prueban: vuelven a pedir en 60 días.</div>
    <div class="btn">Probar la selección<small>{C.pct(C.DESCUENTO_PILOTO,0)} con el cupón {C.CUPON}</small></div>
  </div>
</div>
""", css=CSS_AD)
