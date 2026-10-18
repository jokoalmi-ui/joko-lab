"""Piezas 06-09: story, brief de campaña, informe mensual y panel de seguimiento."""
from tokens import piece, header, footer
import art
import case as C
import index as IDX

D = C.D
PIEZAS = []
TIT = {p[0]: p for p in IDX.PIEZAS}

def add(name, h, body, wrap="pad", css=""):
    exp = TIT[name][1]
    assert h == exp, f"{name}: altura {h} != índice {exp}"
    PIEZAS.append(piece(name, exp, body, wrap, css))

def pie(n, extra=""):
    t = TIT[n]
    return footer(f"<b>{C.CLIENTE}</b> · {C.CLIENTE_SUB} · <span style='color:#8E96A5'>datos de EJEMPLO</span>",
                  f"{t[2]} · pieza {t[0][:2].lstrip('0')} / {IDX.TOTAL}{(' · ' + extra) if extra else ''}")

# ============================== 06 STORY 9:16 ==============================
add("06_story_9x16", 1920, f"""
<div class="safe" style="top:250px">zona segura · 250 px</div>
<div class="safe" style="bottom:250px;border-top:0;border-bottom:1px dashed rgba(127,168,255,.45);
  padding-bottom:6px;text-align:right">zona segura · 250 px</div>
<div style="position:relative;z-index:3;display:flex;flex-direction:column;flex:1">
  <div class="top"><span class="chip flat">story · 9:16 · 15 s</span>
    <span class="brand" style="font-size:20px"><span class="mark" style="width:32px;height:32px;font-size:16px">{C.INICIALES}</span>{C.CLIENTE}</span></div>
  <div class="spacer"></div>
  <div class="eyebrow gold">variante vertical de la campaña</div>
  <div style="font-size:78px;font-weight:800;line-height:1.02;letter-spacing:-2.4px;margin-top:14px">
    ¿Por qué oler<br>igual que<br><em class="g">todos los demás</em>?</div>
  <div class="body" style="margin-top:22px;font-size:25px">Tres decants, tres perfiles. Prueba antes
  de comprar el frasco grande: 10 ml dan para un mes largo.</div>
  <div class="row" style="align-items:center;gap:36px;margin-top:34px">
    {art.vial(140, 258, "#E7CB84", "#A97F2E")}
    <div>
      <div class="sticker">{C.CUPON} · {C.pct(C.DESCUENTO_PILOTO,0)}</div>
      <div class="micro" style="margin-top:14px">sticker con el cupón: se puede arrastrar a la historia</div>
    </div>
  </div>
  <div class="spacer"></div>
  <div class="row between" style="align-items:center">
    <div class="small">Texto sobreimpreso: «toca el enlace y elige la tuya» · sin música con copyright</div>
    <div class="btn ghost">Toca el enlace<small>casaaurora.example/ana-decants</small></div>
  </div>
  <div class="ft"><div class="l"><b>{C.CLIENTE}</b> · {C.CLIENTE_SUB} ·
    <span style="color:#8E96A5">las líneas discontinuas azules son las zonas seguras de la interfaz de la red social</span></div>
    <div class="r">Story 9:16 · pieza {int(TIT['06_story_9x16'][0][:2]) + 1} / {IDX.TOTAL}</div></div>
</div>
""")

# ============================== 07 BRIEF DE CAMPAÑA ==============================
cal = [("S1 · 05-11 oct", "Vídeo largo de presentación", "Reel 9:16 · 60-90 s", "Ana", "publicado"),
       ("S2 · 12-18 oct", "Prueba de los 3 decants", "Carrusel 4:5 + 2 stories", "María", "en producción"),
       ("S3 · 19-25 oct", "«Cuál es para ti» por perfil", "TikTok 3 piezas", "Julia", "guion enviado"),
       ("S4 · 26 oct-01 nov", "Recopilación y cupón", "Story + post estático", "las tres", "pendiente")]
filas_cal = "".join(f"<tr><td class='k'>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td>"
                    f"<td><span class='tagmini'>{e}</span></td></tr>" for a, b, c, d, e in cal)

add("07_brief_campana", 1527, f"""
{header(C.CLIENTE, "brief de campaña", C.INICIALES)}
<div class="h1" style="margin-top:18px">Brief de <em class="g">campaña</em> · {C.MES}</div>
<div class="lead" style="margin-top:12px;max-width:1000px">Objetivo, mensajes y límites, en una página.</div>

<div class="card" style="margin-top:24px;padding:8px 30px">
  <div class="kv"><span class="k">Objetivo del mes</span><span class="v">{C.inte(D['ped'])} pedidos atribuidos y 3 creadoras activas</span></div>
  <div class="kv"><span class="k">Qué cuenta como éxito</span><span class="v">poder listar de dónde vino cada pedido</span></div>
  <div class="kv"><span class="k">Presupuesto de comisiones</span><span class="v">{C.eur(D['com'])} ({C.pct(C.COMISION_PCT,0)} del pedido)</span></div>
</div>

<div class="eyebrow" style="margin-top:26px">mensajes clave · los tres que sí</div>
<div class="card" style="margin-top:12px;padding:8px 30px">
  {''.join(f'<div class="kv"><span class="k" style="color:#F4F5F7">{i+1}. {t}</span>'
           f'<span class="v micro" style="max-width:430px">{d}</span></div>'
           for i, (t, d) in enumerate(C.MENSAJES))}
</div>

<div class="row" style="gap:18px;margin-top:24px">
  <div class="card flat grow">
    <div class="eyebrow">lo que no se dice</div>
    <ul class="list no" style="margin-top:12px">{''.join(f'<li>{x}</li>' for x in C.NO_DECIR)}</ul>
  </div>
</div>

<div class="eyebrow" style="margin-top:26px">calendario de 4 semanas</div>
<table class="tb" style="margin-top:10px">
  <tr><th>semana</th><th>pieza</th><th>formato</th><th>responsable</th><th>estado</th></tr>
  {filas_cal}
</table>

<div class="card flat" style="margin-top:18px;padding:4px 30px">
  <div class="kv"><span class="k">Aprobación</span><span class="v micro">la marca revisa el guion en 48 h</span></div>
  <div class="kv"><span class="k">Etiquetado</span><span class="v micro">«colaboración pagada» + cupón, siempre</span></div>
</div>
<div class="spacer"></div>
{pie("07_brief_campana")}
""", css="table.tb td,table.tb th{padding:6px 14px}")

# ============================== 08 INFORME MENSUAL ==============================
ana = D["filas"][0]
maxsem = max(D["semanas_ana"])
barras = "".join(
    f'<div class="col"><div class="val">{v}</div>'
    f'<div class="bar{" dim" if i != D["semanas_ana"].index(maxsem) else ""}" '
    f'style="height:{round(210*v/maxsem)}px"></div><div class="lb">{C.SEMANAS[i]}</div></div>'
    for i, v in enumerate(D["semanas_ana"]))
max_share = maxsem / D["filas"][0]["ped"]
otros = D["filas"][0]["ped"] - maxsem

add("08_informe_mensual", 1920, f"""
{header(C.CLIENTE, "informe mensual · {C.MES}", C.INICIALES)}
<div class="row between" style="margin-top:30px;align-items:flex-end">
  <div>
    <div class="eyebrow">creadora · {ana['h']}</div>
    <div class="h1" style="margin-top:10px">Informe de <em class="g">{C.MES}</em></div>
    <div class="small" style="margin-top:12px;max-width:640px">Cada cifra sale del cupón
    <b class="gold">{C.CUPON}</b> y de su enlace con <span class="mono">creator=</span>.
    Nada estimado a ojo.</div>
  </div>
  {art.avatar("AO", 84)}
</div>

<div class="kpis" style="margin-top:30px">
  <div class="kpi"><div class="lbl">Clics únicos</div><div class="big">{C.inte(ana['clics'])}</div>
    <div class="note">conv. {C.pct(ana['conv'])}</div></div>
  <div class="kpi"><div class="lbl">Pedidos</div><div class="big">{ana['ped']}</div>
    <div class="note">coste por pedido {C.eur(ana['cpo'])}</div></div>
  <div class="kpi"><div class="lbl">Ingresos</div><div class="big" style="font-size:34px">{C.eur(ana['ing'])}</div>
    <div class="note">ticket medio {C.eur(C.TICKET)}</div></div>
  <div class="kpi"><div class="lbl">Su comisión</div><div class="big" style="font-size:34px">{C.eur(ana['com'])}</div>
    <div class="note">{C.pct(C.COMISION_PCT,0)} del pedido</div></div>
</div>

<div class="eyebrow" style="margin-top:32px">pedidos por semana</div>
<div class="chart" style="margin-top:16px">{barras}</div>
<div class="axis"><span>inicio del mes</span><span>hoy</span></div>

<div class="row" style="gap:18px;margin-top:28px">
  <div class="card flat grow">
    <div class="eyebrow">lectura de los datos</div>
    <ul class="list" style="margin-top:12px">
      <li>El pico es la <b>semana 3</b>: {maxsem} pedidos, el {C.pct(max_share,0)} del mes.
        Coincide con el vídeo largo del 20 de octubre.</li>
      <li>El vídeo largo trajo <b>{maxsem}</b> pedidos y las stories del resto del mes,
        <b>{otros}</b>: la pieza larga sostiene el mes.</li>
      <li>Cada pedido cuesta <b>{C.eur(ana['cpo'])}</b> de comisión y deja {C.eur(C.TICKET)} de ingreso.</li>
    </ul>
  </div>
  <div class="card gold grow">
    <div class="eyebrow" style="color:#E7CB84">recomendación</div>
    <div class="small" style="margin-top:10px;color:#EFE4C6">Renovar 3 meses con <b>una pieza larga al
    mes</b> y dos stories de apoyo, no cuatro stories semanales. Probar 10 € de publicidad al post
    que mejor funcione y medir si baja el coste por pedido.</div>
    <div class="micro" style="margin-top:12px">Decisión de la marca, no del informe.</div>
  </div>
</div>
<div class="spacer"></div>
{pie("08_informe_mensual", "cierre 31-10-2026")}
""")

# ============================== 09 PANEL DE SEGUIMIENTO ==============================
filas = "".join(
    f"<tr><td class='k'>{f['h']}<div class='micro' style='font-weight:400'>{f['nom']} · {f['red']}</div></td>"
    f"<td><span class='tagmini'>{f['codigo']}</span></td>"
    f"<td>{C.inte(f['clics'])}</td><td>{C.pct(f['conv'])}</td><td class='k'>{f['ped']}</td>"
    f"<td>{C.eur(f['ing'],0)}</td><td>{C.eur(f['com'],0)}</td></tr>" for f in D["filas"])

add("09_panel_seguimiento", 1350, f"""
{header(C.CLIENTE, "panel de seguimiento", C.INICIALES)}
<div class="h1" style="margin-top:28px">Quién trajo <em class="g">qué</em> · {C.MES}</div>
<div class="lead" style="margin-top:12px">La tabla que se mira una vez al mes para decidir a quién
renovar. Se rellena sola desde el panel de la tienda, filtrando por cupón y origen.</div>

<table class="tb" style="margin-top:26px">
  <tr><th>creadora</th><th>cupón</th><th>clics</th><th>conv.</th><th>pedidos</th>
      <th>ingresos</th><th>comisión</th></tr>
  {filas}
  <tr class="tot"><td>total</td><td></td><td>{C.inte(D['clics'])}</td><td>{C.pct(D['conv'])}</td>
      <td>{D['ped']}</td><td>{C.eur(D['ing'],0)}</td><td class="warn">{C.eur(D['com'],0)}</td></tr>
</table>

<div class="row" style="gap:18px;margin-top:28px">
  <div class="kpi"><div class="lbl">Ingresos atribuidos</div><div class="big" style="font-size:34px">{C.eur(D['ing'])}</div>
    <div class="note">ticket medio {C.eur(D['ticket'])}</div></div>
  <div class="kpi"><div class="lbl">Comisiones</div><div class="big" style="font-size:34px">{C.eur(D['com'])}</div>
    <div class="note">{C.pct(C.COMISION_PCT,0)} del pedido atribuido</div></div>
  <div class="kpi"><div class="lbl">Gestión</div><div class="big" style="font-size:34px">{C.eur(C.HONORARIOS,0)}</div>
    <div class="note">tarifa mensual del sistema</div></div>
  <div class="kpi"><div class="lbl">Retorno</div><div class="big">{f"{D['roas']:.1f}".replace('.', ',')}×</div>
    <div class="note">sobre {C.eur(D['coste'],0)} de coste total</div></div>
</div>

<div class="card" style="margin-top:26px">
  <div class="eyebrow">cómo se rellena esta tabla (y por qué no engaña)</div>
  <ul class="list" style="margin-top:10px">
    <li>Pedidos e ingresos: <b>export del panel de la tienda</b>, columna de origen = cupón o parámetro <span class="mono">creator=</span>.</li>
    <li>Clics: parámetro <span class="mono">utm_campaign</span> por pieza; separa vídeo largo, stories y carrusel.</li>
    <li>Devoluciones: se descuentan del mes en que entran, no del mes en que se vendió.</li>
    <li>Nadie edita cifras a mano: si un dato no cuadra, se revisa el enlace, no la tabla.</li>
  </ul>
</div>
<div class="spacer"></div>
{pie("09_panel_seguimiento")}
""")
