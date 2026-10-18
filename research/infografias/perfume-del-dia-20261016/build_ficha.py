#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-16 · TORINO21 (Xerjoff)
Sustituciones fail-closed sobre la plantilla oficial; mismo motor que la ficha
de Ocean The Rive / Renaissance (14-15-oct-2026).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
Escribe el HTML + CHECK en stdout.
"""
import os, re, sys, json

DIA      = "2026-10-16"
FECHA    = "VIERNES · 16 OCTUBRE 2026"
SLUG     = "torino21"
CASA     = "Xerjoff"
NOMBRE   = "Torino21"
SUB      = "verde aromática: menta, limón, albahaca y tomillo sobre almizcle y verbena"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_1.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (16-oct-2026) ------------------------------------
# Pirámide: Fragrantica id 70424 (4,45/5 · 8.898 votos · 776 reseñas, 2021) +
# web oficial xerjoff.com (variantes 50 ml 195,00 / 100 ml 295,00; descripción
# oficial "inspired by professional tennis") · BD coleccion.db id 1047 (EDP,
# unisex, 2021, estela moderada, longevidad 7 h, posee=botella, 0 usos) ·
# ventana 08-18 instrumento: sens 21,5/22,3/23,5 °C, banda cálida, amplitud 2,9.
DH1 = ('<div class="dh"><b>2021</b><span class="sep">·</span>Eau de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Aromática verde fresca</div>')
DH2 = ('<div class="dh">Perfumista: <b>no revelado</b>'
       '<span class="f">Xerjoff no acredita la nariz (Fragrantica / Parfumo) · lanzado en 2021</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>295 €</b> / 100 ml<span class="f">'
       'BD de la colección (id 1047) · Precio: <b>295 €</b> (100 ml) y <b>195 €</b> (50 ml) en la '
       'web oficial Xerjoff (xerjoff.com, en stock) — consultado 16-10-2026</span></div>')

R_NUM = "4,45"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_VACIA + '\n          </span>')
R_META = '<span class="r-meta">8.898 votos · 776 reseñas · Fragrantica</span>'

NOT_1 = ("la salida: menta, limón, albahaca y tomillo")
NOT_2 = ("el corazón: grosella negra, romero, lavanda y jazmín")
NOT_3 = ("el fondo: almizcle y verbena (hierba luisa)")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: pirámide oficial en '
              'Fragrantica (id 70424) + web oficial Xerjoff — consultado 16-oct-2026</span>')

INSP = ("“Inspirado en el mundo de la alta competición del tenis profesional, TORINO21 captura "
        "la atmósfera eléctrica de los instantes previos al partido: la concentración de los dos "
        "adversarios antes de medirse en la pista y el aliento contenido del público que espera "
        "presenciar —y vivir— algo espectacular. TORINO21 es una fragancia fresca y revitalizante "
        "que une el arte de la perfumería con la emoción del deporte profesional, preservando la "
        "emoción que ambos despiertan.”")
FUENTE_INSP = ('<span class="fuente-line">— Descripción oficial de la casa (xerjoff.com) [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Platine Blanc</span>'
         '<span class="alt-casa">Aromatix X French Avenue · 2025</span>'
         '<span class="alt-rt">4,35/5 · 1.363 votos</span>'
         '<span class="alt-motivo">el más citado como clon: mismo esqueleto menta-limón-albahaca, un punto más almizclado</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Hawas Verde</span>'
         '<span class="alt-casa">Rasasi · 2025</span>'
         '<span class="alt-rt">4,26/5 · 812 votos</span>'
         '<span class="alt-motivo">más económico (~54 $): lima, manzana verde y pachulí, sin el tomillo</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Mirsaal Valentine</span>'
         '<span class="alt-casa">Le Falconné Perfumes · 2025</span>'
         '<span class="alt-rt">≈45 CAD · 7-8 h según reseñas</span>'
         '<span class="alt-motivo">mismas notas de salida + manzana; reseñas: «literalmente Torino21 de principio a fin»</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: Fragrantica («smells '
              'similar» / reseñas) + Scentsation (acordes compartidos) · consultado 16-oct-2026</span>')

CITA = ("“Cuando la gente decía «mojito», yo pensaba: ¿cómo va a oler un perfume a eso? Casi todo "
        "es «sabor» mentolado. Pero no: esto es mojito puro, de los que me tomo en los bares. "
        "Normalmente las notas verdes y mentoladas me echan para atrás, pero este es ligeramente "
        "dulce, lo justo para que me guste.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica (dance2die) [traducida]</span>')

CLIMA = ("21,5 – 23,5 °C de sensación (ventana 08-18) · media 22,3 °C · lluvia 3 % · humedad 84 %<br>"
         "amplitud 2,9 °C: banda cálida y estable, verde aromático de cuerpo ligero · dosis contenida")
SPRAYS = ("Sprays: <b>2-3</b> por la mañana (tramo 08-12, ~22 °C) · <b>2</b> a mediodía "
          "(pico 23,5 °C a las 12:00)<br>"
          "<span class=\"caveat-pie\">que se note al pasar, no al entrar</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'MENTA · LIMÓN · ALBAHACA · TOMILLO' },\n"
         "    { w: 420, f:'#3f7f6f', t:'#88bfae', l:'#27574b', c1:'CORAZÓN', txt:'GROSELLA NEGRA · ROMERO · JAZMÍN' },\n"
         "    { w: 540, f:'#8a5a2b', t:'#c99a6a', l:'#5d3c1a', c1:'FONDO', txt:'ALMIZCLE · VERBENA' }")


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
        "year": "2021",
        "concentracion": "Eau de Parfum",
        "genero": "Unisex",
        "familia": "Aromática verde",
        "rating": R_NUM,
        "longevidad": "~7 h",
        "estela": "moderada",
        "precio": "295 €",
        "perfumista": "no revelado",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 22,3",
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
