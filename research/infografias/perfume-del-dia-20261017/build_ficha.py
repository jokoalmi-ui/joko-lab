#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-17 · ENCRE NOIRE (Lalique)
Sustituciones fail-closed sobre la plantilla oficial; mismo motor que las
fichas de Torino21 / Ocean The Rive / Renaissance (14-16-oct-2026).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
"""
import os, re, sys, json

DIA      = "2026-10-17"
FECHA    = "SÁBADO · 17 OCTUBRE 2026"
SLUG     = "encre_noire"
CASA     = "Lalique"
NOMBRE   = "Encre Noire"
SUB      = "tinta negra, ciprés y vetiver: el bosque después de la lluvia"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_a.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (17-oct-2026) ------------------------------------
# Pirámide: web oficial Lalique (fr.lalique.com, ficha del producto) — Tête:
# Cyprès, Acétate de Vétiveryle · Cœur: Vétiver d'Haïti, Vétiver Bourbon ·
# Fond: Bois de Cachemire, Muscs. Rating/votos: Fragrantica id 1834.
# Precio: JSON-LD oficial — SKU M13201/1 (100 ml) 103,00 € · M13200/1 (50 ml)
# 77,00 €, ambos InStock. BD coleccion.db id 954 (estela moderada, 7 h,
# posee=botella, 0 usos; concentración corregida EDP→EDT hoy con backup).
DH1 = ('<div class="dh"><b>2006</b><span class="sep">·</span>Eau de Toilette'
       '<span class="sep">·</span>Masculina<span class="sep">·</span>Amaderada aromática</div>')
DH2 = ('<div class="dh">Perfumista: <b>Nathalie Lorson</b>'
       '<span class="f">Fragrantica (id 1834) · casa Lalique, 2006</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>103 €</b> / 100 ml (consultado 17-10-2026)<span class="f">'
       'BD de la colección (id 954) · Precio: <b>103 €</b> (100 ml) y <b>77 €</b> (50 ml) en la '
       'web oficial Lalique (fr.lalique.com, en stock) — consultado 17-10-2026</span></div>')

R_NUM = "4,14"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_PARCIAL = ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h14">'
                '<stop offset="14%" stop-color="#c9971c"/><stop offset="14%" stop-color="#d8d4c8"/>'
                '</linearGradient></defs><path fill="url(#h14)" '
                'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_PARCIAL + '\n          </span>')
R_META = '<span class="r-meta">25.946 votos · Fragrantica</span>'

NOT_1 = ("la salida: ciprés y acetato de vetiverilo — verde, seco, casi tinta")
NOT_2 = ("el corazón: vetiver de Haití y de Bourbon — raíz húmeda y terrosa")
NOT_3 = ("el fondo: madera de cachemira y almizcle — la piel que queda")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial de la '
              'casa (fr.lalique.com) + Fragrantica id 1834 — consultado 17-oct-2026</span>')

INSP = ("“Un frasco negro icónico. La más sofisticada de las notas masculinas —el vetiver oscuro "
        "y amaderado— sublimada en todas sus facetas. Encre Noire, un clásico moderno de Lalique.” "
        "El frasco recupera los códigos de la casa: vidrio negro cuadrado y tapón de wengé, "
        "herederos del tintero «Biches» que René Lalique diseñó en 1913.")
FUENTE_INSP = ('<span class="fuente-line">— Descripción oficial de la casa (fr.lalique.com) '
               '[traducida] · inspiración del frasco: sección «The inspiration»</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Sycomore</span>'
         '<span class="alt-casa">Chanel · Les Exclusifs · 2008</span>'
         '<span class="alt-rt">4,28/5 · 2.332 votos</span>'
         '<span class="alt-motivo">el mismo vetiver ahumado con ciprés, más redondo y con un punto floral; el salto de precio es brutal</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Grey Vetiver</span>'
         '<span class="alt-casa">Tom Ford · 2009</span>'
         '<span class="alt-rt">4,26/5 · 8.757 votos</span>'
         '<span class="alt-motivo">vetiver limpio, cítrico y de oficina: la versión «afeitada» del mismo tema (Druni, 95,95 €/100 ml, consultado 17-10-2026)</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Vetiver</span>'
         '<span class="alt-casa">Guerlain · 1959 (reedición 2000)</span>'
         '<span class="alt-rt">4,17/5 · 6.904 votos</span>'
         '<span class="alt-motivo">el abuelo del género: vetiver con tabaco y nuez moscada, más verde y vintage (85,75 €/100 ml, beautycos.es, consultado 17-10-2026)</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: Fragrantica '
              '(«smells similar» / reseñas) · ratings y votos de Fragrantica — consultado 17-oct-2026</span>')

CITA = ("“Esto dibuja un bosque oscuro después de la lluvia: se huelen los árboles verdes, la tierra "
        "mojada y, por debajo, ese vetiver húmedo y terroso. Tengo un lote de 2018: la duración es "
        "una locura —casi un día en la piel—, la estela es íntima.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica [traducida]</span>')

CLIMA = ("15,6 – 18,1 °C de sensación (ventana 08-18) · media 17,1 °C · lluvia 70 % · humedad 74 %<br>"
         "amplitud 5,2 °C: banda templada estable, perfil medio amaderado-terroso · 3 sprays")
SPRAYS = ("Sprays: <b>3</b> por la mañana (tramo 08-12, ~17 °C)<br>"
          "<span class=\"caveat-pie\">un refuerzo a las 7-8 h si la piel se lo come</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'CIPRÉS · ACETATO DE VETIVERILO' },\n"
         "    { w: 420, f:'#3f6b3a', t:'#8db98a', l:'#24421f', c1:'CORAZÓN', txt:'VETIVER DE HAITÍ · BOURBON' },\n"
         "    { w: 540, f:'#5d4a3a', t:'#a08469', l:'#3a2c20', c1:'FONDO', txt:'MADERA DE CACHEMIRA · ALMIZCLE' }")


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
    t = sub1(t, r'src="frasco_figura_acqua_di_sale\.png"', f'src="{FIGURA}"', "figura+reflejo", n=2)
    t = sub1(t, r'alt="Acqua di Sale Profumum Roma"', f'alt="{NOMBRE} {CASA}"', "alt figura")
    t = sub1(t, r'<div class="casa">[^<]*</div>', f'<div class="casa">{CASA}</div>', "casa")
    t = sub1(t, r"<h1>[^<]*</h1>", f"<h1>{NOMBRE}</h1>", "h1")
    t = sub1(t, r'<div class="sub">[^<]*</div>', f'<div class="sub">{SUB}</div>', "sub")
    t = sub1(t, r'<div class="dh"><b>1996</b>[\s\S]*?</div>', DH1, "dh1")
    t = sub1(t, r'<div class="dh">Perfumistas: [\s\S]*?</div>', DH2, "dh2")
    t = sub1(t, r'<div class="dh">Longevidad <b>~10 h</b>[\s\S]*?</div>', DH3, "dh3")
    t = sub1(t, r'<span class="r-num">[^<]*</span>', f'<span class="r-num">{R_NUM}</span>', "r-num")
    t = sub1(t, r'<span class="stars">[\s\S]*?</span>\n', STARS + "\n", "estrellas")
    t = sub1(t, r'<span class="r-meta">[^<]*</span>', R_META, "r-meta")

    # pirámide: colores del corazón + 3 leyendas + fuente
    t = sub1(t, r'#4fb6cd,#177fa3', "#8db98a,#3f6b3a", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#24421f;">', "lab corazón")
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
              '.sec-head{margin-bottom:2px !important}'
              '.content{padding-top:45px !important;padding-bottom:50px !important}'
              '.inspiracion p{line-height:1.4 !important}'
              '.cita blockquote{line-height:1.4 !important}'
              '.pie .clima{line-height:1.4 !important}'
              '.pie .sprays{line-height:1.4 !important}'
              '.pie{padding-top:8px !important}'
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
        "year": "2006",
        "concentracion": "Eau de Toilette",
        "genero": "Masculina",
        "familia": "Amaderada aromática",
        "rating": R_NUM,
        "longevidad": "~7 h",
        "estela": "moderada",
        "precio": "103 €",
        "perfumista": "Nathalie Lorson",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 17,1",
        "lluvia": "lluvia 70 %",
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
