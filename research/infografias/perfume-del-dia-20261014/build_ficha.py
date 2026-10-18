#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-14 · Renaissance (Xerjoff)
Sustituciones fail-closed sobre la plantilla oficial (copia C4).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
Escribe el HTML + CHECK en stdout.
"""
import os, re, sys, json

DIA      = "2026-10-14"
FECHA    = "MIÉRCOLES · 14 OCTUBRE 2026"
SLUG     = "renaissance"
CASA     = "Xerjoff"
NOMBRE   = "Renaissance"
SUB      = "cítricos de Amalfi, menta y rosa sobre maderas"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_a.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else f"ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (14-oct-2026) ------------------------------------
DH1 = ('<div class="dh"><b>2011</b><span class="sep">·</span>Eau de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Cítrica aromática</div>')
DH2 = '<div class="dh">Perfumista: <b>no revelado</b></div>'
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>245,00 €</b> / 100 ml<span class="f">'
       'Precio: web oficial Xerjoff, 100 ml · consultado 14-10-2026</span></div>')

R_NUM = "4,30"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_PARCIAL = ('<svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h4">'
                '<stop offset="30%" stop-color="#c9971c"/><stop offset="30%" stop-color="#d8d4c8"/>'
                '</linearGradient></defs><path fill="url(#h4)" '
                'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_PARCIAL + '\n          </span>')
R_META = '<span class="r-meta">5.521 votos · 563 reseñas · Fragrantica</span>'

NOT_1 = ("la salida: limón de Amalfi, mandarina, bergamota y petitgrain")
NOT_2 = ("el corazón: menta fría, muguete y rosa búlgara")
NOT_3 = ("el fondo: almizcle, cedro de Virginia, pachulí y ámbar")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: Fragrantica '
              '(pirámide) / catálogo oficial Xerjoff — consultado 14-oct-2026</span>')

INSP = ("“Renaissance, de la colección 1861, toma su inspiración —y su nombre— de uno de los "
        "periodos artísticos y culturales más importantes de la historia: un movimiento "
        "impulsado por el deseo de revivir y mejorar las grandes ideas y logros del pasado. "
        "Renaissance es una celebración del arte italiano y un homenaje a los artistas que "
        "cambiaron el curso de la historia con su talento, su visión y obras de gran belleza.”")
FUENTE_INSP = ('<span class="fuente-line">— Web oficial Xerjoff [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Torino21</span>'
         '<span class="alt-casa">Xerjoff · 2021</span>'
         '<span class="alt-rt">4,45/5 · 8.880 votos</span>'
         '<span class="alt-motivo">«la versión más cítrica» de la misma casa</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Acqua Decima</span>'
         '<span class="alt-casa">Eau d\'Italie · 2013</span>'
         '<span class="alt-rt">3,89/5 · 254 votos</span>'
         '<span class="alt-motivo">«muy cerca del Renaissance, pero más asequible»</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Ninfeo Mio</span>'
         '<span class="alt-casa">Goutal · 2010</span>'
         '<span class="alt-rt">4,11/5 · 1.803 votos</span>'
         '<span class="alt-motivo">cítrico verde: «un Ninfeo Mio con menos hoja»</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: '
              'reseñas de Renaissance en Fragrantica (12126) y Basenotes — 14-oct-2026</span>')

CITA = ("“Refrescante y juguetón, pero también profundo: uno de los mejores cítricos que "
        "existen. Me recuerda a un refresco italiano de limón de buena calidad; la menta y "
        "unas flores ligeras lo endulzan, y la base de ámbar y almizcle lo prolonga.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña «Italian summer» · Parfumo '
               '(Xerjoff Renaissance) [traducida]</span>')

CLIMA = ("18,6 – 27,7 °C de sensación (ventana 08-14) · media 22,6 °C · lluvia 0 %<br>"
         "amplitud 11,3 °C: mañana templada y mediodía cálido · cítrico fresco, sin extremos")
SPRAYS = ("Sprays: <b>3</b> por la mañana (tramo 08-10) · <b>2</b> al mediodía (tramo 11-14)<br>"
          "<span class=\"caveat-pie\">que se note al pasar, no al entrar</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'LIMÓN DE AMALFI · MANDARINA · BERGAMOTA · PETITGRAIN' },\n"
         "    { w: 420, f:'#3f8f5f', t:'#8fc98f', l:'#2a6b45', c1:'CORAZÓN', txt:'MENTA · MUGUETE · ROSA BÚLGARA' },\n"
         "    { w: 540, f:'#6b4a2a', t:'#a8825a', l:'#4a3020', c1:'FONDO', txt:'ALMIZCLE · CEDRO · PACHULÍ · ÁMBAR' }")


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
    t = sub1(t, r'#4fb6cd,#177fa3', "#8fc98f,#3f8f5f", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#2f7a4f;">', "lab corazón")
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

    # capas del prisma 3D
    t = sub1(t, r"const capas = \[[\s\S]*?\];", "const capas = [\n" + CAPAS + "\n  ];", "capas pirámide")

    # ---- asertos de contenido obligatorio (antes de escribir) --------------
    req = {
        "fondo": f"url('{FONDO}')",
        "figura": f'src="{FIGURA}"',
        "qr": f'src="{QR}"',
        "h1": f"<h1>{NOMBRE}</h1>",
        "casa": CASA,
        "year": "2011",
        "concentracion": "Eau de Parfum",
        "genero": "Unisex",
        "familia": "Cítrica aromática",
        "rating": R_NUM,
        "longevidad": "Longevidad",
        "estela": "moderada",
        "precio": "245,00 €",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 22,6",
        "lluvia": "lluvia 0 %",
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
