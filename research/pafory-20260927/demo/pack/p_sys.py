"""Pieza 02: como se atribuye una venta (metodo, reglas y limites)."""
from tokens import piece, header, footer
import icons
import case as C
import index as IDX

TIT = {p[0]: p for p in IDX.PIEZAS}
PIEZAS = []


def add(name, h, body, wrap="pad", css=""):
    exp = TIT[name][1]
    assert h == exp, f"{name}: altura {h} != indice {exp}"
    PIEZAS.append(piece(name, exp, body, wrap, css))


def pie(n):
    t = TIT[n]
    return footer(
        f"<b>{C.CLIENTE}</b> · {C.CLIENTE_SUB} · "
        "<span style=\"color:#8E96A5\">datos de EJEMPLO</span>",
        f"{t[2]} · pieza {int(t[0][:2]) + 1} de {len(IDX.PIEZAS)}",
    )


cajas = [("ic_cart", "El cupón entra en el carrito", "ANA12 - 12 % en su selección"),
         ("ic_link", "El enlace lleva su nombre", "creator=ana.ortiz en la URL"),
         ("ic_code", "El pedido guarda el origen", "la tienda anota cupón y parámetros"),
         ("ic_chart", "El panel calcula la comisión", "10 % del pedido atribuido")]
flow = []
for i, (ic, t, d) in enumerate(cajas):
    if i:
        flow.append('<div class="arrow">→</div>')
    flow.append(f'<div class="box">{getattr(icons, ic)(30)}<div class="t">{t}</div>'
                f'<div class="d">{d}</div></div>')

reglas = ["Ventana de 30 días: cuenta el último clic antes de comprar.",
          "Un pedido con devolución no cuenta como venta.",
          "Se cuenta el pedido, no la visita ni el «me gusta».",
          "Si dos creadoras tocan el mismo pedido, cobra la del último clic."]
limites = ["Ventas por teléfono o en tienda física: no se pueden atribuir.",
           "Recomendaciones de viva voz o en un grupo privado: no dejan rastro.",
           "Guardados y comentarios: solo los ve la plataforma, no la tienda."]

U = C.UTM
params = "&amp;".join(f"{k}={v}" for k, v in U.items())

PIEZAS.append(piece("02_sistema_atribucion", TIT["02_sistema_atribucion"][1], f"""
{header(C.CLIENTE, "método de atribución", C.INICIALES)}
<div class="h1" style="margin-top:26px">Cómo se atribuye <em class="g">una venta</em></div>
<div class="lead" style="max-width:980px">Sin esto, pagar a una creadora es fe: se manda dinero
y no se sabe qué volvió. Este es el circuito completo, y también lo que no se puede medir.</div>
<div class="flow" style="margin-top:30px">{''.join(flow)}</div>
<div class="card flat" style="margin-top:18px;padding:18px 26px">
  <div class="up" style="margin-bottom:10px">lo que viaja dentro del enlace de {C.D['filas'][0]['h']}</div>
  <div class="mono" style="font-size:18px">casaaurora.example/ana-decants?{params}</div>
</div>
<div class="row" style="gap:18px;margin-top:22px">
  <div class="card grow"><div class="eyebrow">reglas</div>
    <ul class="list" style="margin-top:14px">{''.join(f'<li>{r}</li>' for r in reglas)}</ul></div>
  <div class="card grow"><div class="eyebrow">lo que no se puede medir</div>
    <ul class="list no" style="margin-top:14px">{''.join(f'<li>{r}</li>' for r in limites)}</ul></div>
</div>
<div class="card gold" style="margin-top:22px">
  <div class="row between">
    <div><div class="h3">Coste del mes</div>
      <div class="small" style="margin-top:6px">comisiones pagadas + honorarios del servicio</div></div>
    <div style="text-align:right"><div class="h2">{C.eur(C.D['coste'], 0)}</div>
      <div class="micro">{C.eur(C.D['com'], 0)} en comisiones · {C.eur(C.HONORARIOS, 0)} de gestión</div></div>
  </div>
</div>
<div class="micro" style="margin-top:14px">Los honorarios de gestión son del piloto: 120 €/mes por
la red completa, no por creadora.</div>
{pie("02_sistema_atribucion")}
"""))
