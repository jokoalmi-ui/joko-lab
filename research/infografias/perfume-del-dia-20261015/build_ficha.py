#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-15 · OCEAN THE RIVE (Unique'e Luxury)
Sustituciones fail-closed sobre la plantilla oficial; mismo motor que la ficha
de Renaissance / Hespéridé Colognisé (14-oct-2026).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
Escribe el HTML + CHECK en stdout.
"""
import os, re, sys, json

DIA      = "2026-10-15"
FECHA    = "JUEVES · 15 OCTUBRE 2026"
SLUG     = "ocean_the_rive"
CASA     = "Unique'e Luxury"
NOMBRE   = "Ocean The Rive"
SUB      = "extrait cítrico-marino: brisa de mar, manzanilla azul y cachemira"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_a.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (15-oct-2026) ------------------------------------
# Web oficial uniqueeluxury.com: Extrait de Parfum, 100 ml, 349,00 $ (consultado
# 15-10-2026) · Fragrantica 104325: 3,96/5 con 272 votos, 52 reseñas, lanzado
# feb-2025, nariz Gökhan Şimşek · BD coleccion.db id 1041 (posee=botella,
# estela moderada, longevidad 7 h) · parfumistas.fr: 3,98/5 (263 votos)
DH1 = ('<div class="dh"><b>2025</b><span class="sep">·</span>Extrait de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Cítrica aromática marina</div>')
DH2 = ('<div class="dh">Perfumista: <b>Gökhan Şimşek</b>'
       '<span class="f">Fragrantica · lanzado en febrero de 2025</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>345 €</b> / 100 ml<span class="f">'
       'BD de la colección (id 1041) · Precio: <b>345 €</b> (jolieprofumerie.es, en stock; '
       'envío a España) y 349,00 $ en la web oficial Unique\'e Luxury — ambos extrait 100 ml · '
       'consultado 15-10-2026</span></div>')

R_NUM = "3,96"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_VACIA + '\n          </span>')
R_META = '<span class="r-meta">272 votos · Fragrantica</span>'

NOT_1 = ("la salida: bergamota, mandarina, pomelo y brisa marina")
NOT_2 = ("el corazón: armoise, albahaca y manzanilla azul sobre brisa de mar")
NOT_3 = ("el fondo: madera de cachemira, pachulí, vainilla, almizcle y ámbar")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: web oficial '
              'Unique\'e Luxury / Fragrantica — consultado 15-oct-2026</span>')

INSP = ("“Una mezcla refrescante y vigorizante de acordes marinos, cálida y sensual "
        "manzanilla azul y albahaca, y un fondo de cítricos vivos. Su brisa marina y sus "
        "notas herbales —armoise y albahaca— junto a la calmante manzanilla azul toman el "
        "protagonismo y ofrecen una experiencia nítida, acuática y estimulante; los cítricos "
        "aportan profundidad aromática, y la madera de cachemira, el pachulí, la vainilla, el "
        "almizcle y el ámbar dejan una impresión cálida, suave y duradera.”")
FUENTE_INSP = ('<span class="fuente-line">— Descripción de la casa '
               '(publicada en Fragrantica) [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Akdeniz</span>'
         '<span class="alt-casa">Unique\'e Luxury · 2019</span>'
         '<span class="alt-rt">4,10/5 · 773 votos</span>'
         '<span class="alt-motivo">misma casa: más fruta (piña) y cuero, mucho más rotunda</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Ocean of a Midnight Moon</span>'
         '<span class="alt-casa">Simone Andreoli · 2022</span>'
         '<span class="alt-rt">3,98/5 · 457 votos</span>'
         '<span class="alt-motivo">marino con ginebro y menta; Parfumo lo puntúa 7,6/10</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Megamare</span>'
         '<span class="alt-casa">Orto Parisi</span>'
         '<span class="alt-rt">3,92/5 · 7.343 votos</span>'
         '<span class="alt-motivo">el marino de referencia: más oscuro, salino y bestia</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: Parfumo '
              '(«smells similar») + Fragrantica (valoraciones) · consultado 15-oct-2026</span>')

CITA = ("“Una deliciosa brisa de notas marinas, acompañada de especias ligeras (manzanilla, "
        "albahaca) y pomelo, te lleva de viaje; una vainilla agradable y serena te sostiene por "
        "el camino y pasa a una suave lana de cachemira, un ámbar reconfortante y un pachulí "
        "discreto. Un viaje excelente de principio a fin. 10/10”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica '
               '(obw, 12-sep-2026) [traducida]</span>')

CLIMA = ("20,5 – 28,0 °C de sensación (ventana 08-18) · media 25,0 °C · lluvia 0 % · humedad 69 %<br>"
         "amplitud 7,5 °C: banda cálida, cítrico-marino de cuerpo ligero · dosis contenida")
SPRAYS = ("Sprays: <b>2-3</b> por la mañana (tramo 08-12, ~24 °C) · <b>2</b> por la tarde "
          "(tramo 13-18, ~26 °C)<br>"
          "<span class=\"caveat-pie\">que se note al pasar, no al entrar</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'BERGAMOTA · MANDARINA · POMELO · BRISA MARINA' },\n"
         "    { w: 420, f:'#3f7f6f', t:'#88bfae', l:'#27574b', c1:'CORAZÓN', txt:'ARMOISE · ALBAHACA · MANZANILLA AZUL' },\n"
         "    { w: 540, f:'#3f5f8f', t:'#8fa8cf', l:'#2a4166', c1:'FONDO', txt:'CACHEMIRA · PACHULÍ · VAINILLA · ALMIZCLE · ÁMBAR' }")


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
    t = sub1(t, r'<div class="dh">Perfumistas: <b>[^<]*</b></div>', DH2, "dh2")
    t = sub1(t, r'<div class="dh">Longevidad <b>~10 h</b>[\s\S]*?</div>', DH3, "dh3")
    t = sub1(t, r'<span class="r-num">[^<]*</span>', f'<span class="r-num">{R_NUM}</span>', "r-num")
    t = sub1(t, r'<span class="stars">[\s\S]*?</span>\n', STARS + "\n", "estrellas")
    t = sub1(t, r'<span class="r-meta">[^<]*</span>', R_META, "r-meta")

    # pirámide: colores del corazón + 3 leyendas + fuente
    t = sub1(t, r'#4fb6cd,#177fa3', "#88bfae,#3f7f6f", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#27574b;">', "lab corazón")
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
              '.sec-head{margin-bottom:3px !important}'
              '.content{padding-top:4px !important;padding-bottom:4px !important}'
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
        "year": "2025",
        "concentracion": "Extrait de Parfum",
        "genero": "Unisex",
        "familia": "Cítrica aromática marina",
        "rating": R_NUM,
        "longevidad": "~7 h",
        "estela": "moderada",
        "precio": "345 €",
        "perfumista": "Gökhan Şimşek",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 25,0",
        "lluvia": "lluvia 0 %",
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
