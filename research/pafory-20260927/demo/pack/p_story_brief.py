"""Piezas 06 (story) y 07 (brief de campana)."""
from tokens import piece, header, footer
import art
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


guion = [("0-3 s", "Plano del frasco y del decant en la mano."),
         ("3-8 s", "Qué notas se notan y cuánto dura."),
         ("8-12 s", "Precio, 10 ml y para qué momento."),
         ("12-15 s", "Sticker con el cupón y el enlace.")]
guion_html = "".join(f'<div class="kv"><span class="k">{t}</span>'
                     f'<span class="v micro" style="max-width:520px">{d}</span></div>'
                     for t, d in guion)

add("06_story_9x16", 1920, f"""
<div class="safe" style="top:250px">zona segura de la interfaz · no poner texto importante encima</div>
<div class="safe" style="bottom:250px">zona segura inferior</div>
{header(C.CLIENTE, "story 9:16 · 15 s", C.INICIALES)}
<div class="spacer"></div>
<div class="eyebrow">story 1 de 3 · {C.MES}</div>
<div class="hook" style="font-size:70px;margin-top:16px">¿Por qué<br>oler igual<br>que todos?</div>
<div class="row" style="gap:26px;margin-top:8px;align-items:flex-end">
  <div>{art.vial(150, 300, tint=C.PRODUCTOS[0]["tint"])}</div>
  <div class="grow">
    <div class="sticker">{C.CUPON} · 12 %</div>
    <div class="small" style="margin-top:16px">en su selección de 24 referencias, toca el enlace
    de la bio</div>
  </div>
</div>
<div class="card flat" style="margin-top:22px;padding:6px 30px">
  <div class="up" style="padding:14px 0 6px">guion de la story</div>
  {guion_html}
</div>
<div class="card" style="margin-top:20px">
  <div class="eyebrow">antes de publicar</div>
  <ul class="list" style="margin-top:12px">
    <li>Etiquetar la pieza como colaboración pagada.</li>
    <li>El cupón visible en el primer segundo.</li>
    <li>El enlace de la bio apuntando a su página.</li>
  </ul>
</div>
<div class="micro" style="margin-top:14px">Se publica en vertical y con el enlace de su bio:
la story no lleva enlace propio, así que el clic se mide por el código del cupón.</div>
<div class="spacer"></div>
{pie("06_story_9x16")}
""", css=".safe{font-size:12px;color:rgba(127,168,255,.5);border-top:1px dashed rgba(127,168,255,.28)}")

# --------------------------------------------------------------------- 07 brief
cal = [("reel 9:16", "Ana + tienda", "publicado"),
       ("story x3", "Ana", "publicado"),
       ("reel 9:16", "Ana + tienda", "en revisión"),
       ("carrusel + story", "tienda", "pendiente")]
filas = "".join(
    f'<tr><td class="k">{s}</td><td style="text-align:left">{pz}</td>'
    f'<td>{fo}</td><td>{qu}</td><td>{es}</td></tr>'
    for s, pz, (fo, qu, es) in zip(C.SEMANAS, [
        "Presentación de su selección",
        "Rutina de dos decants en un día normal",
        "Tres perfiles, tres momentos",
        "Cierre de mes: cuál se ha repetido"], cal))
msj = "".join(f'<div class="kv"><span class="k">{t}</span>'
              f'<span class="v micro" style="max-width:560px">{d}</span></div>'
              for t, d in C.MENSAJES)

add("07_brief_campana", 1527, f"""
{header(C.CLIENTE, "brief de campaña", C.INICIALES)}
<div class="h1" style="margin-top:18px">Brief de <em class="g">campaña</em> · {C.MES}</div>
<div class="lead" style="margin-top:12px;max-width:1000px">Objetivo, mensajes y límites, en una
página que se lee antes de grabar.</div>
<div class="kpis" style="margin-top:24px">
  <div class="kpi"><div class="lbl">pedidos atribuidos</div>
    <div class="big">58</div><div class="note">de una sola creadora</div></div>
  <div class="kpi"><div class="lbl">creadoras activas</div>
    <div class="big">3</div><div class="note">una pieza larga al mes</div></div>
  <div class="kpi"><div class="lbl">plazo de revisión</div>
    <div class="big">48 h</div><div class="note">si no hay respuesta, se publica</div></div>
</div>
<div class="row" style="gap:18px;margin-top:24px">
  <div class="card grow"><div class="eyebrow">mensajes clave</div>
    <div style="margin-top:8px">{msj}</div></div>
  <div class="card grow"><div class="eyebrow">lo que no se dice</div>
    <ul class="list no" style="margin-top:14px">
      {''.join(f'<li>{r}</li>' for r in C.NO_DECIR)}</ul></div>
</div>
<div class="eyebrow" style="margin-top:26px">calendario</div>
<table class="tb" style="margin-top:8px">
  <tr><th>semana</th><th style="text-align:left">pieza</th><th>formato</th><th>quien graba</th>
  <th>estado</th></tr>
  {filas}
</table>
<div class="card flat" style="margin-top:18px;padding:4px 30px">
  <div class="kv"><span class="k">Aprobación</span>
    <span class="v micro">la marca revisa el guion en 48 h</span></div>
  <div class="kv"><span class="k">Etiquetado</span>
    <span class="v micro">toda pieza lleva «colaboración pagada» y su cupón</span></div>
</div>
{pie("07_brief_campana")}
""", css="table.tb td,table.tb th{padding:8px 14px}")
