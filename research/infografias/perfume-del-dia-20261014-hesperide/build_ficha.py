#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-14 · HESPÉRIDÉ COLOGNISÉ (Nishane)
Ficha EXTRA (el usuario lo pidió el mismo día). Sustituciones fail-closed
sobre la plantilla oficial; mismo motor que la ficha de Renaissance del 14-oct.
Uso: python3 build_ficha.py [fondo.png] [salida.html]
Escribe el HTML + CHECK en stdout.
"""
import os, re, sys, json

DIA      = "2026-10-14"
FECHA    = "MIÉRCOLES · 14 OCTUBRE 2026"
SLUG     = "hesperide"
CASA     = "Nishane"
NOMBRE   = "Hespéridé Colognisé"
SUB      = "colonia de lima turca: jazmín e iris sobre musgo y vetiver"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else f"{SLUG}_fondo_a.png")
OUT      = (sys.argv[2] if len(sys.argv) > 2 else "ficha_a.html")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos verificados hoy (14-oct-2026) ------------------------------------
# Fragrantica 87331 (lanzado 2023, 4,00/5 con 123 votos) · web oficial Nishane
# (categoría «Extrait de Cologne Collection», 175,00 EUR / 100 ml) · BD coleccion.db id 981
DH1 = ('<div class="dh"><b>2023</b><span class="sep">·</span>Extrait de Cologne'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Cítrica aromática amaderada</div>')
DH2 = ('<div class="dh">Perfumista: <b>Olaf Larsen</b>'
       '<span class="f">Fragrantica (la casa no lo acredita en la ficha de producto)</span></div>')
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>175,00 €</b> / 100 ml<span class="f">'
       'BD de la colección (id 981) · Precio: web oficial Nishane, 100 ml · consultado 14-10-2026</span></div>')

R_NUM = "4,00"
_SVG_LLENA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
_SVG_VACIA = ('<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" '
              'd="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>')
STARS = ('<span class="stars">\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_LLENA + '\n            ' + _SVG_LLENA +
         '\n            ' + _SVG_VACIA + '\n          </span>')
R_META = '<span class="r-meta">123 votos · Fragrantica</span>'

NOT_1 = ("la salida: bergamota, naranja y lima (la colonia de limón turca)")
NOT_2 = ("el corazón: jazmín, iris, cedro y madera de cachemira")
NOT_3 = ("el fondo: ámbar gris, musgo, almizcle y vetiver")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: web oficial Nishane '
              '(pirámide) / Fragrantica — consultado 14-oct-2026</span>')

INSP = ("“Hespéridé Colognisé es una incorporación notable a nuestra colección Extrait de "
        "Cologne. Es un homenaje a la tradición turca de ofrecer colonia de limón a los "
        "invitados como símbolo de hospitalidad: el corazón del proyecto fue crear una "
        "fragancia de base de lima que rindiera homenaje a esa tradición y, a la vez, fuera "
        "un aroma distinguido y duradero. Para reforzar su frescura unimos los cítricos con "
        "un almizcle rotundo y notas florales delicadas; jazmín, iris, cedro y cachemira en "
        "el corazón aportan complejidad, y el ámbar gris, el musgo, el almizcle y el vetiver "
        "dan profundidad.”")
FUENTE_INSP = ('<span class="fuente-line">— Web oficial Nishane [traducida]</span>')

ALT_1 = ('<div class="alt-item"><span class="alt-n">Colognisé</span>'
         '<span class="alt-casa">Nishane · 2018</span>'
         '<span class="alt-rt">4,14/5 · 1.141 votos</span>'
         '<span class="alt-motivo">misma casa y colección: la primera de la serie</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Safran Colognisé</span>'
         '<span class="alt-casa">Nishane · 2019</span>'
         '<span class="alt-rt">4,34/5 · 1.514 votos</span>'
         '<span class="alt-motivo">misma casa: la hermana con azafrán, más cálida</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Colonia</span>'
         '<span class="alt-casa">Acqua di Parma · 1916</span>'
         '<span class="alt-rt">4,13/5 · 4.309 votos</span>'
         '<span class="alt-motivo">el clásico italiano del que bebe toda colonia cítrica</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Selección: misma casa (colección '
              'Extrait de Cologne) + el clásico de referencia · valoraciones de Fragrantica 14-oct-2026</span>')

CITA = ("“Huele a sorbete de lima. Me lo puse para ir al gimnasio y, aún sudando, la mujer "
        "de la caja me dijo que olía increíble: creo que funciona muy bien con el calor del "
        "cuerpo; en la piel gana con las horas.”")
FUENTE_CITA = ('<span class="fuente-line">— Reseña de comunidad · Fragrantica '
               '(Hespéridé Colognisé) [traducida]</span>')

CLIMA = ("24,6 – 30,0 °C de sensación (ventana 16-22) · media 27,5 °C · lluvia 0 %<br>"
         "amplitud 11,5 °C: media tarde a ~30 °C y noche templada · cítrico ligero, baja dosis")
SPRAYS = ("Sprays: <b>1-2</b> a media tarde (tramo 16-18, ~30 °C) · <b>2</b> por la noche (tramo 19-22)<br>"
          "<span class=\"caveat-pie\">que se note al pasar, no al entrar</span>")

CAPAS = ("    { w: 300, f:'#c9a227', t:'#f0d878', l:'#8e6f12', c1:'SALIDA', txt:'BERGAMOTA · NARANJA · LIMA' },\n"
         "    { w: 420, f:'#8a7ab8', t:'#bfb3e0', l:'#5f5286', c1:'CORAZÓN', txt:'JAZMÍN · IRIS · CEDRO · CACHEMIRA' },\n"
         "    { w: 540, f:'#4a6b3f', t:'#8fae7f', l:'#2f4a28', c1:'FONDO', txt:'ÁMBAR GRIS · MUSGO · ALMIZCLE · VETIVER' }")


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
    t = sub1(t, r'#4fb6cd,#177fa3', "#bfb3e0,#8a7ab8", "swatch corazón")
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">',
             '<span class="lab" style="color:#5f5286;">', "lab corazón")
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

    # ---- encaje vertical (14-oct-2026) -------------------------------------
    # El pie se salía 28 px por debajo del lienzo (1350) y el caveat + QR
    # quedaban cortados. Se comprime SOLO interlineado/márgenes (ni un dato
    # ni un tamaño de fuente cambian) hasta que el pie acaba en y<=1346,
    # igual que la ficha de referencia validada (Renaissance, 14-oct).
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
        "concentracion": "Extrait de Cologne",
        "genero": "Unisex",
        "familia": "Cítrica aromática",
        "rating": R_NUM,
        "longevidad": "~7 h",
        "estela": "moderada",
        "precio": "175,00 €",
        "perfumista": "Olaf Larsen",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 27,5",
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
