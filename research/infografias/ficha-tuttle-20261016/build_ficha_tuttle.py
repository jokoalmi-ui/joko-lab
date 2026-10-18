#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA v5 — 2026-10-16 · TUTTLE (Tiziana Terenzi) — FICHA A PETICIÓN.
Mismo motor fail-closed que la ficha del día (perfume-del-dia-20261016).
Uso: python3 build_ficha_tuttle.py [fondo.png] [salida.html]
"""
import os, re, sys, json

DIA      = "2026-10-16"
FECHA    = "VIERNES · 16 OCTUBRE 2026"
SLUG     = "tuttle"
CASA     = "Tiziana Terenzi"
NOMBRE   = "Tuttle"
SUB      = "extraít de parfum frutal-amaderada: pomelo siciliano, cassis y melocotón de Romaña sobre flores blancas y maderas"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_1.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_tuttle.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (16-oct-2026) ------------------------------------
# Pirámide + rating: Fragrantica id 66358 (4,09/5 · 273 votos · 31 reseñas, 2021).
# Casa/narración/precio: boutique oficial terenziboutique.com (colección Comete,
# extrait 100 ml — 435,00 €). Longevidad/estela: reseñas de comunidad (Fragrantica:
# de 3 h en algunas pieles a 18-20 h; Parfumo: duración muy larga). Alternativas:
# comparador The Last Spritz (coincidencia %) + reseñas Fragrantica/Parfumo.
# Clima del pie: parte real del lab (ventana 08-18, Erandio, 16-oct-2026).
DH1 = ('<div class="dh"><b>2021</b><span class="sep">·</span>Extrait de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Frutal amaderada floral</div>')
DH2 = ('<div class="dh">Perfumista: <b>Paolo Terenzi</b>'
       '<span class="f">Colección Comete de Tiziana Terenzi · Fragrantica (id 66358) y web oficial de la casa</span></div>')
DH3 = ('<div class="dh">Longevidad <b>8-10 h</b><span class="sep">·</span>Estela <b>fuerte</b>'
       '<span class="sep">·</span><b>435 € (100 ml)</b>'
       '<span class="f">Reseñas: de 3 h a 20 h+ según piel · precio 435 € (100 ml) de tarifa en '
       'derparfumeur.com (-50 % → 217,50 €) y 425 € en agoratopia.com — consultado 16-10-2026</span></div>')

R_NUM = "4,09"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_VACIA + '\n          </span>')
R_META = '<span class="r-meta">273 votos · 31 reseñas · Fragrantica</span>'

NOT_1 = ("la salida: pomelo siciliano, cassis y melocotón de Romaña")
NOT_2 = ("el corazón: tuberosa, iris, magnolia, muguet y jazmín real con ámbar gris")
NOT_3 = ("el fondo: pachulí rojo, sándalo indio, cedro cubano, abedul italiano y vetiver de Haití")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial en '
              'Fragrantica (id 66358) — consultado 16-10-2026</span>')

INSP = ("“Tuttle es un cometa periódico de nuestro Sistema Solar, de la familia del cometa Halley. […] En Tuttle se "
        "oyen resonancias de Halley, de la misma colección Comete: es una de las cometas con mayor influencia "
        "beneficiosa sobre nuestro universo […]. La creación abre con un bouquet efervescente y alegre de frutas y "
        "cítricos, donde manda el pomelo siciliano abrazado por la fuerza salvaje del cassis y por el revolucionario "
        "melocotón de Romaña, utilizado por primera vez en perfumería.”")
FUENTE_INSP = ('<span class="fuente-line">— Descripción oficial de la casa (terenziboutique.com) [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Rosso Pompei</span>'
         '<span class="alt-casa">Tiziana Terenzi · la misma casa</span>'
         '<span class="alt-rt">74 % de coincidencia · The Last Spritz</span>'
         '<span class="alt-motivo">el clon de casa: en Fragrantica, «no noto ninguna diferencia entre este y Rosso Pompei»</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Tygar</span>'
         '<span class="alt-casa">Bvlgari · colección Le Gemme</span>'
         '<span class="alt-rt">69 % de coincidencia · The Last Spritz</span>'
         '<span class="alt-motivo">el mismo pomelo cítrico con maderas limpias, fuera de la casa Terenzi</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Vibrato</span>'
         '<span class="alt-casa">Sospiro · la referencia fresca de la familia</span>'
         '<span class="alt-rt">60 % de coincidencia · The Last Spritz</span>'
         '<span class="alt-motivo">reseñas de Parfumo: «la salida me recuerda al jengibre de Vibrato»</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: comparador The Last Spritz '
              '(coincidencia %) + reseñas de Fragrantica y Parfumo · consultado 16-10-2026</span>')

CITA = ("“Pasé por la tienda a probar Rosso Pompei y acabé completamente prendado de Tuttle: son muy "
        "parecidos, pero Tuttle es algo más suave, fresco y delicado. […] Para mí, el mejor "
        "descubrimiento de la temporada: un unisex con estela y duración impresionantes.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica (schomj) [traducida]</span>')

CLIMA = ("21,4 – 22,6 °C de sensación (ventana 08-18 · open-meteo, Erandio) · media 22,1 °C · lluvia 3 %<br>"
         "encaje (The Last Spritz): primavera 99 % · verano 92 % · día 100 %")
SPRAYS = ("Sprays: <b>2</b> en interior · <b>2-3</b> en exterior<br>"
          '<span class="caveat-pie">no pasarse: empalaga</span>')

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'POMELO · CASSIS · MELOCOTÓN' },\n"
         "    { w: 420, f:'#a8708e', t:'#d8aec3', l:'#7c4a63', c1:'CORAZÓN', txt:'TUBEROSA · IRIS · MAGNOLIA · ÁMBAR GRIS' },\n"
         "    { w: 540, f:'#8a5a2b', t:'#c99a6a', l:'#5d3c1a', c1:'FONDO', txt:'PACHULÍ · SÁNDALO · CEDRO · VETIVER' }")

SELLO_OLD = '<div class="sello"><div>Elección<br>del Lab</div><b>2026</b></div>'
SELLO_NEW = '<div class="sello"><div>A petición<br>del Lab</div><b>2026</b></div>'


def sub1(txt, pat, rep, label, flags=0, n=1):
    """Sustitución fail-closed: exige exactamente n coincidencias."""
    txt2, k = re.subn(pat, lambda m: rep, txt, flags=flags)
    if k != n:
        raise SystemExit(f"[ABORTA] {label}: se esperaban {n} coincidencias, hay {k}")
    print(f"  OK {label} ({k})")
    return txt2


def main():
    for f in (FONDO, FIGURA, QR):
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            raise SystemExit(f"[ABORTA] falta el asset: {p}")
    t = open(TPL, encoding="utf-8").read()

    t = sub1(t, r"background:url\('[^']+'\)", f"background:url('{FONDO}')", "fondo CSS")
    t = sub1(t, r'<div class="fecha-sep">[^<]*</div>',
             f'<div class="fecha-sep">{FECHA}</div>', "fecha-sep")
    t = sub1(t, re.escape(SELLO_OLD), SELLO_NEW, "sello (a petición)")
    t = sub1(t, r'src="frasco_figura_acqua_di_sale\.png"', f'src="{FIGURA}"', "figura+reflejo", n=2)
    t = sub1(t, r'alt="Acqua di Sale Profumum Roma"', f'alt="{NOMBRE} {CASA}"', "alt figura")
    t = sub1(t, r'<div class="casa">[^<]*</div>', f'<div class="casa">{CASA}</div>', "casa")
    t = sub1(t, r"<h1>[^<]*</h1>", f"<h1>{NOMBRE}</h1>", "h1")
    t = sub1(t, r'<div class="sub">[^<]*</div>', f'<div class="sub">{SUB}</div>', "sub")
    t = sub1(t, r'<div class="dh"><b>1996</b>[\s\S]*?</div>', DH1, "dh1")
    t = sub1(t, r'<div class="dh">Perfumistas: <b>[^<]*</b></div>', DH2, "dh2")
    t = sub1(t, r'<div class="dh">Longevidad <b>~10 h</b>[\s\S]*?</div>', DH3, "dh3")
    t = sub1(t, r'<span class="r-num">[^<]*</span>', f'<span class="r-num">{R_NUM}</span>', "r-num")
    t = sub1(t, r'<span class="stars">[\s\S]*?</span>\n', STARS + "\n", "estrellas")
    t = sub1(t, r'<span class="r-meta">[^<]*</span>', R_META, "r-meta")

    # pirámide: colores del corazón + 3 leyendas + fuente
    t = sub1(t, r'#4fb6cd,#177fa3', "#d8aec3,#a8708e", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#7c4a63;">', "lab corazón")
    leyes = iter((NOT_1, NOT_2, NOT_3))
    t, k = re.subn(r'<span class="not">[^<]*</span>', lambda m: f'<span class="not">{next(leyes)}</span>', t)
    if k != 3:
        raise SystemExit(f"[ABORTA] leyendas: se esperaban 3 coincidencias, hay {k}")
    print("  OK leyendas (3)")
    t = sub1(t, r'<span class="fuente-line" style="margin-top:4px;">[^<]*</span>', FUENTE_PIR, "fuente pirámide")

    # inspiración
    t = sub1(t, r'<p>“[\s\S]*?”</p>', f"<p>{INSP}</p>", "inspiración")
    t = sub1(t, r'<span class="fuente-line">— Casa Profumum Roma[^<]*</span>', FUENTE_INSP, "fuente inspiración")

    # alternativas (3) + fuente
    alts = iter((ALT_1, ALT_2, ALT_3))
    t, k = re.subn(r'<div class="alt-item">[\s\S]*?</div>\n', lambda m: next(alts) + "\n", t)
    if k != 3:
        raise SystemExit(f"[ABORTA] alternativas: se esperaban 3 coincidencias, hay {k}")
    print("  OK alternativas (3)")
    t = sub1(t, r'<span class="fuente-line" style="margin-left:44px;">[^<]*</span>', FUENTE_ALT, "fuente alternativas")

    # cita comunidad
    t = sub1(t, r"<blockquote>[\s\S]*?</blockquote>", f"<blockquote>{CITA}</blockquote>", "cita")
    t = sub1(t, r'<span class="fuente-line">— Reseña en Fragrantica[^<]*</span>', FUENTE_CITA, "fuente cita")

    # pie
    t = sub1(t, r'<div class="clima">[\s\S]*?</div>', f'<div class="clima">{CLIMA}</div>', "clima")
    t = sub1(t, r'<div class="sprays">[\s\S]*?</div>', f'<div class="sprays">{SPRAYS}</div>', "sprays")

    # ---- encaje vertical ----------------------------------------------------
    AJUSTE = ('<style id="ajuste-encaje">'
              '.sec{margin-top:0 !important}'
              '.sec-head{margin-bottom:0 !important}'
              '.hero{margin-bottom:0 !important}'
              '.alts .alt-item{padding-top:4px !important;padding-bottom:4px !important}'
              '.content{padding-top:50px !important;padding-bottom:45px !important}'
              '.inspiracion p{line-height:1.4 !important}'
              '.cita blockquote{line-height:1.4 !important}'
              '.pie .clima{line-height:1.4 !important}'
              '.pie .sprays{line-height:1.4 !important}'
              '.pie{padding-top:2px !important}'
              '.qr{width:58px !important;height:58px !important}'
              '.nota-fondo{bottom:7px !important}'
              '</style>')
    t = sub1(t, r'</head>', AJUSTE + '</head>', "ajuste de encaje")

    # capas del prisma 3D
    t = sub1(t, r"const capas = \[[\s\S]*?\];", "const capas = [\n" + CAPAS + "\n  ];", "capas pirámide")

    # ---- asertos de contenido obligatorio (antes de escribir) --------------
    req = {
        "fondo": f"url('{FONDO}')",
        "figura": f'src="{FIGURA}"',
        "qr": f'src="{QR}"',
        "h1": f"<h1>{NOMBRE}</h1>",
        "casa": CASA,
        "year": "2021",
        "concentracion": "Extrait de Parfum",
        "genero": "Unisex",
        "familia": "Frutal",
        "rating": R_NUM,
        "longevidad": "8-10 h",
        "estela": "fuerte",
        "precio": "435 €",
        "perfumista": "Paolo Terenzi",
        "sello": "A petición",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 22,1",
        "lluvia": "lluvia 3 %",
        "ajuste-encaje": 'id="ajuste-encaje"',
    }
    fallos = [k for k, v in req.items() if v is None or (isinstance(v, str) and v not in t)]
    if req["rango"] is False:
        fallos.append("rango")
    if fallos:
        raise SystemExit("[ABORTA] faltan en el HTML: " + ", ".join(sorted(set(fallos))))

    out = os.path.join(BASE, OUT)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(t)
    print(json.dumps({"html": out, "bytes": os.path.getsize(out), "fondo": FONDO}, ensure_ascii=False))


if __name__ == "__main__":
    main()
