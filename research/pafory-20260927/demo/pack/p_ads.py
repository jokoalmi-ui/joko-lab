"""Piezas 03-05: tres variantes de anuncio (feed 4:5)."""
from tokens import piece, footer
import art
import icons
import case as C
import index as IDX

TIT = {p[0]: p for p in IDX.PIEZAS}
PIEZAS = []
AD_CSS = ".ad{padding:74px 76px;display:flex;flex-direction:column;flex:1;position:relative;z-index:2}" \
         ".hook{font-size:64px;line-height:1.07;font-weight:800;letter-spacing:-1.8px}"


def add(name, body, css=""):
    t = TIT[name]
    PIEZAS.append(piece(name, t[1], body, "ad", AD_CSS + css))


def top(tag):
    return (f'<div class="top"><div class="brand"><span class="mark">{C.INICIALES}</span>'
            f'{C.CLIENTE}</div><span class="chip">{tag}</span></div>')


def pie_ad(n, extra):
    return footer(f"Casa Aurora es un caso ficticio: esta pieza es un EJEMPLO de entrega.",
                  f"anuncio {n} de 3 · {extra}")


def mini(p, w=52, h=100):
    return (f'<div class="mini">{art.vial(w, h, tint=p["tint"])}<div class="nm">{p["nm"]}</div>'
            f'<div class="pr">{C.eur(p["pr"])}</div></div>')


LEGAL = ("<b>Ejemplo.</b> Casa Aurora no existe y las cifras son simuladas. Decants de 10 ml "
         "decantados a mano en Bilbao · frascos originales, sin equivalencias · envío gratis desde "
         "50 € · devoluciones 14 días · ")
CTA = f'<div class="btn" style="padding:16px 30px">Ver la selección<small>cupón {C.CUPON} · 12 %</small></div>'

# ------------------------------------------------------------------ 03 anuncio A
add("03_anuncio_a", f"""
{top("anuncio A · producto")}
<div class="eyebrow" style="margin-top:30px">10 ml · originales, sin equivalencias</div>
<div class="hook" style="margin-top:14px">El frasco grande,<br>sin el frasco grande.</div>
<div class="row" style="gap:34px;margin-top:6px;align-items:center">
  <div style="flex:none">{art.bottle(212, 354, tint=C.PRODUCTOS[0]["tint"])}</div>
  <div class="grow">
    <div class="body" style="font-size:25px">Probar una fragancia de 100 ml cuesta 120-200 € y se
    decide en tres días. Un decant de 10 ml cuesta 19-24 € y da para 20-30 usos.</div>
    <ul class="list" style="margin-top:20px">
      <li>Decantado a mano el mismo día del pedido.</li>
      <li>Frasco y lote a la vista en cada ficha.</li>
      <li>Si no convence, devolución en 14 días.</li>
    </ul>
  </div>
</div>
<div class="strip" style="margin-top:4px">{''.join(mini(p) for p in C.PRODUCTOS)}</div>
<div class="row between" style="margin-top:16px">
  <div><div class="h3">Desde {C.eur(19, 0)} · 3 referencias</div>
  <div class="micro">envío gratis a partir de 50 €</div></div>
  {CTA}
</div>
<div class="legal">{LEGAL}cupón {C.CUPON} válido hasta el 31-10-2026.</div>
{pie_ad("1", "producto")}
""")

# ------------------------------------------------------------------ 04 anuncio B
filas = "".join(
    f'<div class="rowprod"><div style="width:50px;flex:none">'
    f'{art.vial(50, 96, tint=p["tint"])}</div>'
    f'<div style="flex:none;width:250px"><div class="nm">{p["nm"]}</div>'
    f'<div class="ml">{p["nota"]}</div></div><div class="leader"></div>'
    f'<div style="text-align:right;width:170px"><div class="pr" style="width:auto">{C.eur(p["pr"])}</div>'
    f'<div class="ml">{p["ml"]}</div></div></div>' for p in C.PRODUCTOS)

add("04_anuncio_b", f"""
{top("anuncio B · selección")}
<div class="eyebrow" style="margin-top:30px">tres fragancias, tres perfiles</div>
<div class="hook" style="margin-top:14px">Tres fragancias.<br>Cero frascos que sobran.</div>
<div class="body" style="margin-top:16px;font-size:25px">Cada perfil con su ficha: notas, duración y
para qué momento del día. Se elige por lo que te gusta oler, no por lo más vendido.</div>
<div class="card" style="padding:8px 30px;margin-top:14px"><div class="rowprods">{filas}</div></div>
<div class="quote" style="margin-top:22px">
  <div class="qm">«</div>
  <div class="txt" style="font-size:27px">Probé el ámbar porque olía en el vídeo, no porque me lo
  vendieran. Ahora sé lo que me pongo.</div>
  <div class="who">{icons.avatar("LM", 46)}
    <div><div class="small" style="color:#F4F5F7">Lucía M. · Getxo</div>
    <div class="micro">compra verificada · ejemplo</div></div>
  </div>
</div>
<div class="row between" style="margin-top:20px">
  <div><div class="h3">10 ml · desde {C.eur(19, 0)}</div>
  <div class="micro">20-30 usos por decant</div></div>
  {CTA}
</div>
<div class="legal">{LEGAL}cupón {C.CUPON} válido hasta el 31-10-2026.</div>
{pie_ad("2", "selección")}
""")

# ------------------------------------------------------------------ 05 anuncio C
add("05_anuncio_c", f"""
{top("anuncio C · prueba social")}
<div class="row between" style="margin-top:30px">
  <div>{icons.stars(5, 30)}<div class="small" style="margin-top:10px">4,8 sobre 312 valoraciones
  verificadas de compra</div></div>
  <div style="text-align:right"><div class="h1" style="margin-top:0">94 %</div>
  <div class="micro">repite antes de 3 meses</div></div>
</div>
<div class="quote" style="margin-top:26px">
  <div class="qm">«</div>
  <div class="txt">Pedimos cuatro decants entre tres amigas y decidimos una. Comprar 100 ml a ciegas
  se acabó.</div>
  <div class="who">{icons.avatar("NA", 52)}
    <div><div class="small" style="color:#F4F5F7">Nerea A. · Bilbao</div>
    <div class="micro">compra verificada · ejemplo</div></div>
  </div>
</div>
<div class="eyebrow" style="margin-top:30px">lo que más se repite</div>
<div class="strip" style="margin-top:14px">{''.join(mini(p, 60, 116) for p in C.PRODUCTOS)}</div>
<div class="row between" style="margin-top:20px">
  <div><div class="h3">Desde {C.eur(19, 0)} · envío gratis desde 50 €</div>
  <div class="micro">devoluciones 14 días · sin suscripción</div></div>
  {CTA}
</div>
<div class="legal">{LEGAL}las valoraciones también son simuladas.</div>
{pie_ad("3", "prueba social")}
""")
