"""Piezas 08 (informe mensual) y 09 (panel de seguimiento)."""
from tokens import piece, header, footer
import art
import icons
import case as C
import index as IDX

D = C.D
TIT = {p[0]: p for p in IDX.PIEZAS}
PIEZAS = []
A = D["filas"][0]


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


def mini(p, incl, w=56, h=92):
    return (f'<div class="mini">{art.vial(w, h, tint=p["tint"])}<div class="nm">{p["nm"]}</div>'
            f'<div class="pr">{C.eur(p["pr"])}</div>'
            f'<div class="micro">en {incl} de cada 10 pedidos</div></div>')


# ------------------------------------------------------------------ 08 informe
sem = A["pedidos"]
mx = max(sem)
barras = "".join(
    f'<div class="col"><div class="val">{v}</div>'
    f'<div class="bar{" dim" if v != mx else ""}" style="height:{round(180 * v / mx)}px"></div>'
    f'<div class="lb">{lb}<br><span style="color:#7B828F">{C.eur(v * C.TICKET, 0)}</span></div></div>'
    for v, lb in zip(sem, C.SEMANAS))
comp = [("pedidos", D["sep"]["ped"], A["ped"]), ("ingresos", D["sep"]["ing"], A["ing"]),
        ("comisión", D["sep"]["com"], A["com"])]
filas_piezas = "".join(
    f'<tr><td class="k">{f}</td><td style="text-align:left">{pz}</td><td>{fo}</td>'
    f'<td>{C.inte(cl)}</td><td>{pe}</td><td>{C.pct(pe / cl)}</td></tr>'
    for f, pz, fo, cl, pe in C.PIEZAS_MES)
_mejor_conv = max(C.PIEZAS_MES, key=lambda x: x[4] / x[3])
_mas_clics = max(C.PIEZAS_MES, key=lambda x: x[3])
insight = (f"El {_mas_clics[2]} trajo el volumen ({C.inte(_mas_clics[3])} clics) y el "
           f"{_mejor_conv[2]} la mejor conversión ({C.pct(_mejor_conv[4] / _mejor_conv[3])}): "
           "conviene alternar una pieza larga con un cierre corto.")
filas_comp = "".join(
    f'<div class="kv"><span class="k">{k}</span><span class="v">{C.eur(a, 0)} → '
    f'<b class="gold">{C.eur(b, 0)}</b> <span class="micro">+{C.pct(b / a - 1, 0)}</span></span></div>'
    for k, a, b in comp)

add("08_informe_mensual", 1920, f"""
{header(C.CLIENTE, "informe por creadora", C.INICIALES)}
<div class="h1" style="margin-top:26px">Informe de <em class="g">{A["h"]}</em> · {C.MES}</div>
<div class="lead" style="max-width:1000px">Una página al mes por creadora: qué pasó, de dónde salió
cada pedido y qué se repite el mes siguiente.</div>
<div class="kpis" style="margin-top:26px">
  <div class="kpi"><div class="lbl">clics con su enlace</div><div class="big">{C.inte(A["clics"])}</div>
    <div class="note">conversión {C.pct(A["conv"])}</div></div>
  <div class="kpi"><div class="lbl">pedidos</div><div class="big">{A["ped"]}</div>
    <div class="note">ticket medio {C.eur(D["ticket"], 0)}</div></div>
  <div class="kpi"><div class="lbl">ingresos atribuidos</div>
    <div class="big">{C.eur(A["ing"], 0)}</div><div class="note">medidos por cupón y enlace</div></div>
  <div class="kpi"><div class="lbl">comisión</div><div class="big">{C.eur(A["com"], 0)}</div>
    <div class="note">{C.eur(A["cpo"], 2)} por pedido</div></div>
</div>
<div class="eyebrow" style="margin-top:30px">pedidos por semana</div>
<div class="chart">{barras}</div>
<div class="row" style="gap:18px;margin-top:26px">
  <div class="card grow"><div class="eyebrow">lectura</div>
    <ul class="list" style="margin-top:14px">
      <li>El pico está en la semana del 19-25 oct: <b>{24}</b> de los {A["ped"]} pedidos
      ({C.pct(mx / A["ped"], 0)} del mes), con el vídeo largo.</li>
      <li>La conversión ({C.pct(A["conv"])}) va por encima de la media de la tienda (3,1 %).</li>
      <li>Cada pedido deja {C.eur(D["ticket"], 0)}: casi todos llevan dos decants.</li>
    </ul>
  </div>
  <div class="card grow"><div class="eyebrow">recomendación para el mes siguiente</div>
    <ul class="list" style="margin-top:14px">
      <li>Repetir una pieza larga al mes: es la que trae el pico.</li>
      <li>Subir a 3 stories por semana con el mismo cupón.</li>
      <li>Probar 10 € de publicidad sobre el vídeo que mejor funcione.</li>
    </ul>
  </div>
</div>
<div class="eyebrow" style="margin-top:26px">las cuatro piezas del mes</div>
<table class="tb" style="margin-top:8px">
  <tr><th style="width:120px">semana</th><th style="text-align:left">pieza</th>
  <th style="width:160px">formato</th><th style="width:90px">clics</th>
  <th style="width:100px">pedidos</th><th style="width:110px">conv.</th></tr>
  {filas_piezas}
</table>
<div class="micro" style="margin-top:12px">{insight}</div>
<div class="row" style="gap:18px;margin-top:22px">
  <div class="card flat grow"><div class="eyebrow">de dónde vienen los pedidos</div>
    <div class="splitbar">
      <div class="a" style="width:{round(D["sh_cup"] * 100)}%">cupón {round(D["sh_cup"] * 100)} %</div>
      <div class="b" style="width:{round(D["sh_enl"] * 100)}%">enlace {round(D["sh_enl"] * 100)} %</div>
    </div>
    <div class="micro" style="margin-top:12px">{D["cup"]} pedidos entraron escribiendo el cupón (sin
    pasar por el enlace) y {D["enl"]} por el enlace de su bio. Sin el cupón, los primeros no se
    contarían.</div>
  </div>
  <div class="card flat grow"><div class="eyebrow">comparado con septiembre</div>
    <div style="margin-top:6px">{filas_comp}</div>
  </div>
</div>
{pie("08_informe_mensual")}
""", css="table.tb td,table.tb th{padding:8px 14px}.chart{height:270px}")

# -------------------------------------------------------------------- 09 panel
filas = "".join(
    f'<tr><td class="k">{f["nom"]}<div class="micro">{f["h"]}</div></td>'
    f'<td class="mono" style="font-size:19px">{f["codigo"]}</td><td>{C.inte(f["clics"])}</td>'
    f'<td>{C.pct(f["conv"])}</td><td>{f["ped"]}</td><td>{C.eur(f["ing"], 0)}</td>'
    f'<td style="color:#E7CB84;font-weight:700">{C.eur(f["com"], 0)}</td></tr>'
    for f in D["filas"])

add("09_panel_seguimiento", 1350, f"""
{header(C.CLIENTE, "panel de seguimiento", C.INICIALES)}
<div class="h1" style="margin-top:24px">Quién trae <em class="g">qué</em> · {C.MES}</div>
<div class="lead" style="max-width:1000px">El mes entero en siete columnas. Se rellena con el export
de pedidos de la tienda y los parámetros que viajan en cada enlace.</div>
<table class="tb" style="margin-top:26px">
  <tr><th style="width:230px">creadora</th><th style="width:110px">cupón</th>
  <th style="width:90px">clics</th><th style="width:90px">conv.</th><th style="width:100px">pedidos</th>
  <th style="width:150px">ingresos</th><th style="width:140px">comisión</th></tr>
  {filas}
  <tr class="tot"><td>TOTAL</td><td></td><td>{C.inte(D["clics"])}</td>
  <td>{C.pct(D["conv"])}</td><td>{D["ped"]}</td><td>{C.eur(D["ing"], 0)}</td>
  <td class="warn">{C.eur(D["com"], 0)}</td></tr>
</table>
<div class="row" style="gap:18px;margin-top:30px">
  <div class="card grow"><div class="eyebrow">coste y retorno del mes</div>
    <div class="kpis" style="margin-top:14px">
      <div class="kpi"><div class="lbl">comisiones</div>
        <div class="big">{C.eur(D["com"], 0)}</div></div>
      <div class="kpi"><div class="lbl">gestión</div>
        <div class="big">{C.eur(C.HONORARIOS, 0)}</div></div>
      <div class="kpi"><div class="lbl">retorno</div>
        <div class="big">{D["roas"]:.1f}×</div></div>
    </div>
    <div class="micro" style="margin-top:14px">Cada 1 € pagado en comisiones y gestión devolvió
    {D["roas"]:.1f} € en pedidos atribuidos.</div>
  </div>
  <div class="card grow"><div class="eyebrow">cómo se rellena</div>
    <ul class="list" style="margin-top:14px">
      <li>Export de pedidos del mes con la columna de origen.</li>
      <li>Cada pedido se cruza con <span class="mono" style="font-size:18px">creator=</span> y con el cupón.</li>
      <li>Las devoluciones se descuentan antes de calcular la comisión.</li>
    </ul>
  </div>
</div>
<div class="eyebrow" style="margin-top:26px">qué se está comprando</div>
<div class="strip" style="margin-top:14px">
  {''.join(mini(p, n) for p, (_, n) in zip(C.PRODUCTOS, C.INCLUSION))}
</div>
<div class="micro" style="margin-top:12px">No son excluyentes entre sí (casi todos los pedidos llevan
dos decants) y no aparece ni un nombre de cliente: el panel trabaja con pedidos agregados por origen.</div>
{pie("09_panel_seguimiento")}
""", css=".mini{padding:14px 12px;gap:8px}.mini .nm{font-size:18px}")
