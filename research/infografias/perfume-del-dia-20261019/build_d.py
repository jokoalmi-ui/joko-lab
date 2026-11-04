#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-19 · TOWN & COUNTRY (Clive Christian)
Sustituciones fail-closed sobre la plantilla oficial; mismo motor que las
fichas de Encre Noire (17-oct) y Safran Colognisé (18-oct).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
"""
import os, re, sys, json

DIA      = "2026-10-19"
FECHA    = "LUNES · 19 OCTUBRE 2026"
SLUG     = "towncountry"
CASA     = "Clive Christian"
NOMBRE   = "Town &amp; Country"
SUB      = "salvia esclarea, ámbar gris y sándalo: el campo inglés en un frasco de 1925"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (19-oct-2026) -----------------------------------
# Pirámide: notas oficiales de la casa = salvia esclarea (salida), ámbar gris
# (corazón), sándalo (fondo) — Fragrantica id 83240, consultado 19-10-2026.
# Desglose de 11 notas: notas_personales de la BD de la colección (id 914) y
# pirámide de Parfumo (coincidentes).
# Rating/votos: Fragrantica 4,22/5 · 1.034 votos · 192 reseñas (id 83240).
# Precio: formato ÚNICO de 50 ml (la casa no vende 100 ml); 294,83 € en
# vesira.com (en stock) → equivalencia 589,66 €/100 ml — consultado 19-10-2026.
# BD coleccion.db id 914 · posee=botella · longevidad 8 h · estela moderada.
DH1 = ('<div class="dh"><b>2023</b><span class="sep">·</span>EDP'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Aromática amaderada</div>')
DH2 = ('<div class="dh">Perfumista: <b>Vincent Ricord</b>'
       '<span class="f">Fragrantica (id 83240) · casa Clive Christian, 2023</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~8 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>589,66 €</b> / 100 ml (consultado 19-10-2026)'
       '<span class="f">BD de la colección (id 914) · formato único 50 ml: <b>294,83 €</b> en '
       'vesira.com, en stock; equivalencia 100 ml · la casa no ofrece 100 ml · <b>25 %</b> de '
       'concentración de perfume (clivechristian.com) — consultado 19-10-2026</span></div>')

R_NUM = "4,22"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_PARCIAL = ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h22">'
                '<stop offset="22%" stop-color="#c9971c"/><stop offset="22%" stop-color="#d8d4c8"/>'
                '</linearGradient></defs><path fill="url(#h22)" '
                'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_PARCIAL + '\n          </span>')
R_META = '<span class="r-meta">1.034 votos · Fragrantica</span>'

NOT_1 = ("la salida: limón, bergamota, enebro y salvia esclarea — cítrico herbal, limpio y verde")
NOT_2 = ("el corazón: cardamomo, olíbano, té blanco y sándalo — especia seca sobre madera cremosa")
NOT_3 = ("el fondo: ámbar gris, cedro, pachulí y cachemira — salado mineral, piel cálida")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas oficiales de la casa (salvia '
              'esclarea · ámbar gris · sándalo), Fragrantica id 83240; desglose de 11 notas de la BD '
              'de la colección (id 914) coincidente con Parfumo — consultado 19-oct-2026</span>')

INSP = ("“Creado originalmente en 1925 y famoso por llevarlo Winston Churchill, Town &amp; Country fue "
        "la estrella de una nueva era de la Crown Perfumery Company. Hoy se reimagina con los sellos "
        "de la casa Clive Christian —complejidad, concentración y los mejores ingredientes— para la "
        "expresión personal: nítido, con notas refrescantes de la más elegante de las hierbas "
        "descansando sobre una base más profunda. Captura la belleza natural del campo y la elegancia "
        "de la ciudad de Londres.”")
FUENTE_INSP = ('<span class="fuente-line">— Descripción oficial de la casa (vía Fragrantica, id 83240) '
               '[traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Lucius</span>'
         '<span class="alt-casa">Fragrance du Bois · 2024 · mismo perfumista (Jordi Fernández)</span>'
         '<span class="alt-rt">8,3/10 · 370 valoraciones</span>'
         '<span class="alt-motivo">Parfumo lo lista en el «smells similar» de Town &amp; Country: cítrico '
         'con madera y ámbar gris; longevidad 8,0</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Haltane</span>'
         '<span class="alt-casa">Parfums de Marly · 2021</span>'
         '<span class="alt-rt">8,3/10 · 1.795 valoraciones</span>'
         '<span class="alt-motivo">la misma salvia esclarea al frente, con azafrán y oud: más dulce y más '
         'de vestir; longevidad 8,3</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Golden Green</span>'
         '<span class="alt-casa">Xerjoff · 2020</span>'
         '<span class="alt-rt">4,12/5 · 416 votos (Parfumo 7,6 · 229)</span>'
         '<span class="alt-motivo">enebro, cardamomo y ámbar gris: el mismo eje verde-especiado, más café '
         'y cuero al fondo; longevidad 8,1</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: «similar fragrances» de '
              'Parfumo y Fragrantica (ratings, votos y longevidad) — consultado 19-oct-2026</span>')

CITA = ("“Un perfume estupendo y muy fácil de llevar, para cualquier ocasión. Es casi de una sola nota: "
        "lo que huelo al abrir se queda toda la vida del perfume. Salvia muy aromática mezclada con un "
        "limón salado y un punto dulce ligero. Me dura bastante: 7-8 horas de media.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica (usuario Chrono_Kid, '
               '10-sep-2026) [traducida]</span>')

CLIMA = ("8,4 – 14,6 °C de sensación (ventana 08-18) · media 12,4 °C · lluvia 40 % · humedad 66 %<br>"
         "amplitud de sensación 7,2 °C: banda fresca estable, perfil amaderado especiado suave · 3-4 sprays")
SPRAYS = ("Sprays: <b>3-4</b> por la mañana (tramo 08-12, ~10,6 °C)<br>"
          "<span class=\"caveat-pie\">si la tarde llega a 14 °C, quédate en 3</span>")

CAPAS = ("    { w: 300, f:'#8aa06a', t:'#bfd49b', l:'#5e7448', c1:'SALIDA', txt:'LIMÓN · BERGAMOTA · ENEBRO · SALVIA' },\n"
         "    { w: 420, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'CORAZÓN', txt:'CARDAMOMO · OLÍBANO · TÉ BLANCO · SÁNDALO' },\n"
         "    { w: 540, f:'#8a6a45', t:'#c09a72', l:'#5a4227', c1:'FONDO', txt:'ÁMBAR GRIS · CEDRO · PACHULÍ · CACHEMIRA' }")


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
    t = sub1(t, r'alt="Acqua di Sale Profumum Roma"', f'alt="Town &amp; Country Clive Christian"', "alt figura")
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
    t = sub1(t, r'#4fb6cd,#177fa3', "#f0d878,#c9a227", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#8e6f12;">', "lab corazón")
    leyes = iter((NOT_1, NOT_2, NOT_3))
    t, k = re.subn(r'<span class="not">[^<]*</span>', lambda m: f'<span class="not">{next(leyes)}</span>', t)
    if k != 3:
        raise SystemExit(f"[ABORTA] leyendas: se esperaban 3 coincidencias, hay {k}")
    print("  OK leyendas (3)")
    t = sub1(t, r'<span class="fuente-line" style="margin-top:4px;">[^<]*</span>', FUENTE_PIR, "fuente pirámide")

    # inspiración
    t = sub1(t, r'<p>“[\s\S]*?”</p>', '<p>'+INSP+'</p>', "inspiración")
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
              '.content{padding-top:45px !important;padding-bottom:50px !important}'
              '.inspiracion p{line-height:1.30 !important}'
              '.inspiracion{margin-top:0 !important}'
              '.cita blockquote{line-height:1.30 !important}'
              '.alts .alt-item{padding:2px 2px !important}'
              '.pie .clima{line-height:1.30 !important}'
              '.pie .sprays{line-height:1.30 !important}'
              '.pie{padding-top:4px !important}'
              '.frasco-figura{filter:drop-shadow(0 6px 10px rgba(30,17,2,0.78)) drop-shadow(0 18px 34px rgba(58,35,6,0.62)) drop-shadow(0 0 58px rgba(70,44,10,0.42)) !important}'
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
        "year": "2023",
        "concentracion": "EDP",
        "genero": "Unisex",
        "familia": "Aromática amaderada",
        "rating": R_NUM,
        "longevidad": "~8 h",
        "estela": "moderada",
        "precio": "589,66 €",
        "perfumista": "Vincent Ricord",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 12,4",
        "lluvia": "lluvia 40 %",
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
