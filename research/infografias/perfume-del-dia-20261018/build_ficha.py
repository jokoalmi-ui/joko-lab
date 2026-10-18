#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-18 · SAFRAN COLOGNISÉ (Nishane)
Sustituciones fail-closed sobre la plantilla oficial; mismo motor que la
ficha de Encre Noire (17-oct-2026).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
"""
import os, re, sys, json

DIA      = "2026-10-18"
FECHA    = "DOMINGO · 18 OCTUBRE 2026"
SLUG     = "safran"
CASA     = "Nishane"
NOMBRE   = "Safran Colognisé"
SUB      = "azafrán, pomelo rosa y cuero suave: una colonia con memoria de otoño"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (18-oct-2026) -----------------------------------
# Pirámide: web oficial nishane.com (ficha del producto) — TOP: cedrat, passion
# fruit, pink grapefruit · HEART: saffron, magnolia, pink pepper · BASE: musk,
# ambergris, leather. Coincide con Perfumería Julia (ficha 208576).
# Rating/votos: Fragrantica.es 4,35/5 · 1.436 votos (id 54790).
# Precio: 175 €/100 ml en Perfumería Julia (consultado 18-10-2026); 155 € en
# Notino.es y 195 $ en la web oficial. Etiqueta del packshot: EXTRAIT DE
# COLOGNE (18 % de esencia, según la casa) · BD coleccion.db id 982, posee=botella.
DH1 = ('<div class="dh"><b>2019</b><span class="sep">·</span>Extrait de Cologne (18 %)'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Cuero cítrico especiado</div>')
DH2 = ('<div class="dh">Perfumista: <b>Jorge Lee</b>'
       '<span class="f">Fragrantica.es (id 54790) · casa Nishane, 2019</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>175 €</b> / 100 ml (consultado 18-10-2026)<span class="f">'
       'BD de la colección (id 982) · Precio: <b>175 €</b> (100 ml) en Perfumería Julia · '
       '<b>155 €</b> en Notino.es · <b>195 $</b> en nishane.com — consultado 18-10-2026</span></div>')

R_NUM = "4,35"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_PARCIAL = ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h35">'
                '<stop offset="35%" stop-color="#c9971c"/><stop offset="35%" stop-color="#d8d4c8"/>'
                '</linearGradient></defs><path fill="url(#h35)" '
                'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_PARCIAL + '\n          </span>')
R_META = '<span class="r-meta">1.436 votos · Fragrantica</span>'

NOT_1 = ("la salida: cidra, maracuyá y pomelo rosa — cítrico jugoso, casi tropical")
NOT_2 = ("el corazón: azafrán, magnolia y pimienta rosa — especia seca sobre flor blanca")
NOT_3 = ("el fondo: cuero, ámbar gris y almizcle — piel cálida y salada")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial de la '
              'casa (nishane.com) + Perfumería Julia (ficha 208576) — consultado 18-oct-2026</span>')

INSP = ("“Tras el éxito global de Colognisé, Nishane decidió ampliar la colección «Extrait de "
        "Cologne» con nuevas propuestas que recordaran al original pero con otro enfoque en algunos "
        "acordes. La nota principal de azafrán ayuda a añadir un atractivo misterioso y rico al "
        "perfume.” La casa moderniza así la tradición turca de ofrecer colonia de limón a los "
        "invitados, con un extracto al 18 % de esencia.")
FUENTE_INSP = ('<span class="fuente-line">— Descripción oficial de la casa (nishane.com y '
               'Perfumería Julia) [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Suede et Safran</span>'
         '<span class="alt-casa">Nishane · 2015 · mismo perfumista (Jorge Lee)</span>'
         '<span class="alt-rt">4,22/5 · 703 votos</span>'
         '<span class="alt-motivo">más cuero y más cuerpo: 49 % de los votos le da 6-8 h</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Hayaati Gold Elixir</span>'
         '<span class="alt-casa">Lattafa · económico</span>'
         '<span class="alt-rt">3,90/5 · 1.024 votos</span>'
         '<span class="alt-motivo">el clon más citado: 41 % de similitud y longevidad más corta (4-6 h)</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Saffron Extrait</span>'
         '<span class="alt-casa">Aurora Scents</span>'
         '<span class="alt-rt">3,88/5 · 16 votos</span>'
         '<span class="alt-motivo">75 % de similitud, pero con solo 16 votos: pista, no equivalencia</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: parfumistas.fr '
              '(«similitudes»), Fragrantica y reseñas · ratings y votos — consultado 18-oct-2026</span>')

CITA = ("“Ha sido mi perfume firma durante el invierno… ahora que empiezan los días de temperaturas "
        "por encima de los 25° es cuando empiezo a no disfrutarlo tanto… más que un perfume cítrico "
        "es un perfume con mucho azafrán y mucha gamuza.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica.es (usuario Perecioso, '
               '15-abr-2026)</span>')

CLIMA = ("12,7 – 14,6 °C de sensación (ventana 08-18) · media 13,7 °C · lluvia 13 % · humedad 60 %<br>"
         "amplitud de sensación 3,6 °C: banda fresca estable, perfil especiado suave · 3-4 sprays")
SPRAYS = ("Sprays: <b>3-4</b> por la mañana (tramo 08-12, ~13 °C)<br>"
          "<span class=\"caveat-pie\">si la tarde llega a 15 °C, quédate en 3</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'CIDRA · MARACUYÁ · POMELO ROSA' },\n"
         "    { w: 420, f:'#c47a1e', t:'#f0b45e', l:'#8a5210', c1:'CORAZÓN', txt:'AZAFRÁN · MAGNOLIA · PIMIENTA ROSA' },\n"
         "    { w: 540, f:'#5d4a3a', t:'#a08469', l:'#3a2c20', c1:'FONDO', txt:'CUERO · ÁMBAR GRIS · ALMIZCLE' }")


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
    t = sub1(t, r'#4fb6cd,#177fa3', "#f0b45e,#c47a1e", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#8a5210;">', "lab corazón")
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
        "year": "2019",
        "concentracion": "Extrait de Cologne",
        "genero": "Unisex",
        "familia": "Cuero cítrico especiado",
        "rating": R_NUM,
        "longevidad": "~7 h",
        "estela": "moderada",
        "precio": "175 €",
        "perfumista": "Jorge Lee",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 13,7",
        "lluvia": "lluvia 13 %",
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
