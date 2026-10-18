"""Piezas 00 (portada) y 01 (pagina de la creadora)."""
from tokens import piece, header, footer
import art
import icons
import case as C
import index as IDX

D = C.D
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


CSS_AD = """
.ad{padding:74px 76px;display:flex;flex-direction:column;flex:1;position:relative;z-index:2}
.ad .hook{font-size:66px;line-height:1.06;font-weight:800;letter-spacing:-1.8px}
"""


def kpi(lbl, big, note, cls=""):
    return (f'<div class="kpi {cls}"><div class="lbl">{lbl}</div>'
            f'<div class="big">{big}</div><div class="note">{note}</div></div>')


# ---------------------------------------------------------------- 00 portada
a = D["filas"][0]
mitad = len(IDX.PIEZAS) // 2
cols = []
for i in (0, 1):
    regs = IDX.PIEZAS[i * mitad:(i + 1) * mitad]
    items = "".join(
        f'<div class="kv"><span class="k" style="font-size:21px">'
        f'{int(n[:2]) + 1} · {t}</span></div>' for n, h, t, d in regs)
    cols.append(f'<div class="card flat grow" style="padding:6px 30px">{items}</div>')

add("00_portada", 1527, f"""
{header(C.CLIENTE, "pack de colaboradoras", C.INICIALES)}
<div class="eyebrow" style="margin-top:38px">ejemplo de entrega · caso ficticio</div>
<div class="display">Sistema de <em class="g">colaboradoras</em></div>
<div class="lead" style="max-width:960px">Piezas listas, textos escritos y cifras cuadradas:
página por creadora, anuncios, brief de campaña, informe mensual y panel de seguimiento.
Esto es lo que se entrega, no lo que se promete.</div>
<div class="kpis" style="margin-top:30px">
  {kpi("creadoras", str(len(D["filas"])), "con cupón propio")}
  {kpi("pedidos atribuidos", C.inte(D["ped"]), f"en {C.MES}")}
  {kpi("ingresos", C.eur(D["ing"], 0), "atribuidos a su red", "big2")}
  {kpi("retorno", f"{D['roas']:.1f}×", "sobre el coste del mes")}
</div>
<div class="eyebrow" style="margin-top:34px">índice del pack</div>
<div class="row" style="gap:18px;margin-top:14px">{''.join(cols)}</div>
<div class="micro" style="margin-top:12px">Cada pieza se entrega en PNG a tamaño de publicación
y en su fichero editable, con los textos y las cifras a la vista.</div>
{pie("00_portada")}
""")

# ------------------------------------------------------- 01 pagina de creadora
filas = "".join(
    f'<div class="rowprod"><div style="width:54px;flex:none">'
    f'{art.vial(54, 104, tint=p["tint"])}</div>'
    f'<div style="flex:none;width:236px"><div class="nm">{p["nm"]}</div>'
    f'<div class="ml">{p["nota"]}</div></div><div class="leader"></div>'
    f'<div style="text-align:right;width:196px"><div class="pr" style="width:auto">{C.eur(p["pr"])}</div>'
    f'<div class="ml">{C.eur(p["pr"] * C.COMISION_PCT)} de comisión</div></div></div>'
    for p in C.PRODUCTOS)

pasos = [("1", "Publica", "Sube la pieza y marca «colaboración pagada»."),
         ("2", "Comparte", "Su enlace en la bio y su cupón en el vídeo y en las stories."),
         ("3", "Cobra", f"El día 5 del mes siguiente, con el informe delante.")]
steps = "".join(f'<div class="step"><span class="n">{n}</span><div>'
                f'<div class="t">{t}</div><div class="d">{d}</div></div></div>'
                for n, t, d in pasos)

add("01_pagina_creadora", 1920, f"""
{header(C.CLIENTE, "página de colaboradora", C.INICIALES)}
<div class="row" style="margin-top:34px;align-items:flex-start">
  <div class="grow">
    <div class="eyebrow">colaboradora de {C.MES}</div>
    <div class="h1" style="margin-top:12px">{a["nom"]}<br><em class="g">{a["h"]}</em></div>
  </div>
  <div style="text-align:center">{icons.avatar(a["ini"], 104)}
    <div class="micro" style="margin-top:10px">{a["red"]}</div></div>
</div>
<div class="row" style="gap:16px;margin-top:26px">
  <div class="btn grow" style="flex:1">Ver su selección<small>24 referencias · desde {C.eur(19, 0)}</small></div>
  <div class="btn ghost" style="flex:1">Copiar enlace<small>con su nombre dentro</small></div>
</div>
<div class="eyebrow" style="margin-top:30px">su enlace, con seguimiento</div>
<div class="linkbox" style="margin-top:12px;padding:22px 28px">
  <div class="u">casaaurora.example/ana-decants</div>
  <div class="u2">?creator=ana.ortiz&amp;utm_source=instagram&amp;utm_medium=influencer&amp;utm_campaign=2026-10_reel_ana&amp;ref=pagina-creadora</div>
</div>
<div class="coupon" style="margin-top:20px;padding:24px 32px">
  <div>
    <div class="lbl">cupón de su audiencia</div>
    <div class="val" style="margin-top:8px;font-size:42px">{C.pct(C.DESCUENTO_PILOTO, 0)} de descuento</div>
    <div class="micro" style="margin-top:10px;max-width:520px">En su selección de 24 referencias · válido
    hasta el 31-10-2026 · se aplica en el carrito, sin mínimo</div>
  </div>
  <div style="border-left:1px dashed rgba(255,255,255,.28);padding-left:30px;text-align:center">
    <div class="micro" style="margin-bottom:8px">código</div>
    <div class="tagmini" style="font-size:32px;padding:14px 22px;letter-spacing:3px">{C.CUPON}</div>
  </div>
</div>
<div class="card" style="margin-top:22px">
  <div class="kv"><span class="k">Formato pactado</span><span class="v">{a["formato"]}</span></div>
  <div class="kv"><span class="k">Ventana de atribución</span><span class="v">30 días · gana el último clic</span></div>
  <div class="kv"><span class="k">Comisión</span><span class="v">{C.pct(C.COMISION_PCT, 0)} del pedido atribuido</span></div>
  <div class="kv"><span class="k">Pago</span><span class="v">día 5 del mes siguiente, por transferencia</span></div>
</div>
<div class="eyebrow" style="margin-top:24px">su selección</div>
<div class="card" style="padding:10px 30px;margin-top:12px"><div class="rowprods">{filas}</div></div>
<div class="eyebrow" style="margin-top:24px">cómo funciona</div>
<div class="steps c3" style="margin-top:14px">{steps}</div>
<div class="micro" style="margin-top:14px">De su audiencia solo se guardan el pedido y el cupón:
ni nombres ni correos.</div>
{pie("01_pagina_creadora")}
""")
