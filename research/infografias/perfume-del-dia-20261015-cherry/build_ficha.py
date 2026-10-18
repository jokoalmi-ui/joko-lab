#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-15 · CHERRY ON TOP (Joterc)
Ficha EXTRA pedida por el usuario el mismo día. Sustituciones fail-closed
sobre la plantilla oficial; mismo motor que la ficha del 14-oct (Hespéridé).
Uso: python3 build_ficha.py [fondo.png] [salida.html]
Escribe el HTML + CHECK en stdout.
"""
import os, re, sys, json

DIA      = "2026-10-15"
FECHA    = "JUEVES · 15 OCTUBRE 2026"
SLUG     = "cherry"
CASA     = "Joterc"
NOMBRE   = "Cherry on Top"
SUB      = "cereza y almendra amarga sobre gamuza, canela y pachulí oscuro"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_a.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (15-oct-2026) -----------------------------------
# Fragrantica 98658 (lanzado 2023, 4,38/5 con 21 votos, perfumista Daniel
# Josier) · Parfumo (7,6/10 con 5 votos; longevidad 6,0/10, estela 5,8/10)
# · Sanchotena Durango (PVP 90,00 EUR / 80,00 EUR en oferta, 100 ml)
# · BD coleccion.db: decant id 70, casa id 512 (Joterc)
DH1 = ('<div class="dh"><b>2023</b><span class="sep">·</span>Eau de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Floral frutal gourmand</div>')
DH2 = ('<div class="dh">Perfumista: <b>Daniel Josier</b>'
       '<span class="f">Fragrantica (la casa no lo acredita en su web: dominio aparcado)</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~6-7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>80,00 €</b> / 100 ml (PVP 90,00 €)<span class="f">'
       'Precio: Perfumería Sanchotena (Durango), consultado 15-10-2026 · '
       'longevidad y estela: comunidad Parfumo, 6,0/10 y 5,8/10 (5 valoraciones)</span></div>')

R_NUM = "4,38"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_VACIA + '\n          </span>')
R_META = '<span class="r-meta">21 votos · Fragrantica (15-oct-2026)</span>'

NOT_1 = ("la salida: canela dulce, heliotropo y ante (gamuza)")
NOT_2 = ("el corazón: cereza, praliné rosa y almendra amarga")
NOT_3 = ("el fondo: maderas de cachemira, musgo de roble y pachulí oscuro")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: Perfumería Sanchotena '
              '(Durango) [textual] · coincidentes en Fragrantica y Parfumo — consultado 15-oct-2026</span>')

INSP = ("“Descubre la dulzura de Michigan con Cherry on Top. Esta cautivadora fragancia captura "
        "la esencia de las jugosas cerezas, un ingrediente fundamental en algunos de los postres y "
        "platos más deliciosos. Cherry on Top es un viaje olfativo a través de los campos de "
        "cerezos en flor, donde cada nota es un bocado dulce y tentador.”")
FUENTE_INSP = ('<span class="fuente-line">— Descripción de la marca · Perfumería Sanchotena '
               '(distribuidor en España) [textual]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">New Orleans Soul</span>'
         '<span class="alt-casa">Joterc · 2023</span>'
         '<span class="alt-rt">8,6/10 · 7 votos</span>'
         '<span class="alt-motivo">misma casa: la mejor valorada de la colección</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Maple Cedar</span>'
         '<span class="alt-casa">Joterc · 2023</span>'
         '<span class="alt-rt">8,4/10 · 5 votos</span>'
         '<span class="alt-motivo">misma casa: longevidad 7,8/10, la más duradera</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Lost Cherry</span>'
         '<span class="alt-casa">Tom Ford · 2018</span>'
         '<span class="alt-rt">4,05/5 · 18.536 votos</span>'
         '<span class="alt-motivo">el clásico cereza-almendra al que se compara</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: misma casa '
              '(colección Joterc) + el clásico de referencia · Parfumo y Fragrantica, 15-oct-2026</span>')

CITA = ("“Cereza, cereza y más cereza… pero, desgraciadamente, es lo único que noto. La salida es "
        "luminosa y frutal, pero nunca termina de evolucionar. Si te gusta la cereza pura puede "
        "gustarte; a mí me resulta un poco plano y demasiado dulce.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de cliente verificada (4/5, 26-09-2024) · '
               'Daring Light, distribuidor de Joterc [traducida del inglés]</span>')

CLIMA = ("20,5 – 27,7 °C de sensación (ventana 08-18) · media 24,1 °C · lluvia 0 %<br>"
         "amplitud 7,2 °C: mañana suave y sobremesa cálida · gourmand denso en día cálido, "
         "dosis contenida")
SPRAYS = ("Sprays: <b>2-3</b> por la mañana (tramo 08-12, ~23,5 °C) · <b>2</b> por la tarde "
          "(tramo 13-18, ~24,6 °C)<br>"
          "<span class=\"caveat-pie\">que se note al pasar, no al entrar</span>")

CAPAS = ("    { w: 300, f:'#b06a2c', t:'#e0a35f', l:'#7a4413', c1:'SALIDA', txt:'CANELA · HELIOTROPO · GAMUZA' },\n"
         "    { w: 420, f:'#a01f38', t:'#e06a80', l:'#6d1024', c1:'CORAZÓN', txt:'CEREZA · PRALINÉ · ALMENDRA AMARGA' },\n"
         "    { w: 540, f:'#4a5a3a', t:'#8fa77a', l:'#2c3a22', c1:'FONDO', txt:'PACHULÍ · CACHEMIRA · MUSGO DE ROBLE' }")


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
    t = sub1(t, r'#4fb6cd,#177fa3', "#e06a80,#a01f38", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#6d1024;">', "lab corazón")
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

    # ---- encaje vertical (mismo ajuste que la ficha del 14-oct) -------------
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
        "year": "2023",
        "concentracion": "Eau de Parfum",
        "genero": "Unisex",
        "familia": "Floral frutal gourmand",
        "rating": R_NUM,
        "longevidad": "~6-7 h",
        "estela": "moderada",
        "precio": "80,00 €",
        "perfumista": "Daniel Josier",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 24,1",
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
