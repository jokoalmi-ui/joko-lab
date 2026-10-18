#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador FICHA DEL DÍA v5 — 2026-10-12 · Wilgermain Aquafortis
Sustituciones fail-closed sobre la plantilla oficial (copia C4).
Uso: python3 build_ficha.py [fondo_sin_extension]   (def: aquafortis_fondo_b)
Escribe: perfume_del_dia_v5_aquafortis.html (+ CHECK en stdout)
"""
import os, re, sys, json

DIA      = "2026-10-12"
FECHA    = "LUNES · 12 OCTUBRE 2026"
SLUG     = "aquafortis"
CASA     = "Wilgermain"
NOMBRE   = "Aquafortis"
SUB      = "el limón con poso de iris"
BASE     = os.path.dirname(os.path.abspath(__file__))
TPL      = "/home/jokoalmi/.hermes/skills/joko-lab/perfume-del-dia/templates/plantilla-ficha-v5.html"

FONDO    = (sys.argv[1] if len(sys.argv) > 1 else "aquafortis_fondo_b.png")
FIGURA   = f"{SLUG}_figura.png"
QR       = "qr_fragrantica.png"

# ---- datos 100% verificados hoy (12-oct-2026) -------------------------------
DH1 = ('<div class="dh"><b>2020</b><span class="sep">·</span>Eau de Parfum'
       '<span class="sep">·</span>Unisex<span class="sep">·</span>Cítrica floral acuática</div>')
DH2 = '<div class="dh">Perfumista: <b>Rodrigo Flores-Roux</b></div>'
DH3 = ('<div class="dh">Longevidad <b>~7 h</b><span class="sep">·</span>Estela <b>moderada</b>'
       '<span class="sep">·</span><b>180 €</b> / 100 ml<span class="f">'
       'Notas: web oficial · Fragrantica — Precio: ParfuMaria (consultado 12-oct-2026) · '
       'visto a 49 € en eCharme (-72 %)</span></div>')

R_NUM = "3,82"
STARS = ('<span class="stars">\n'
         '            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>\n'
         '            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>\n'
         '            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#c9971c" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>\n'
         '            <svg width="18" height="18" viewBox="0 0 24 24"><defs><linearGradient id="h4"><stop offset="82%" stop-color="#c9971c"/><stop offset="82%" stop-color="#d8d4c8"/></linearGradient></defs><path fill="url(#h4)" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>\n'
         '            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#d8d4c8" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>\n'
         '          </span>')
R_META = ('<span class="r-meta">61 votos · 7 reseñas · Fragrantica</span>')

NOT_1 = ("la chispa: cidra mano de Buda, petitgrain de limonero de Italia y "
         "bergamota Integrale de Calabria (ORPUR)")
NOT_2 = ("el alma: absoluto de jazmín sambac, flor del mandarino (ScentTrek) y lavanda "
         "de Francia — flores blancas sobre cítrico")
NOT_3 = ("el poso: vetiver Coeur de Haití, esencia de cúrcuma (zedoaria) de India y "
         "absoluto de iris de Florencia")
FUENTE_PIR = ('<span class="fuente-line" style="margin-top:4px;">Notas: web oficial Wilgermain / '
              'Fragrantica — consultado 12-oct-2026</span>')

INSP = ("“También percibo siempre un matiz de notas de iris en ciertas naranjas mediterráneas, "
        "y esa idea me llevó a anclar este perfume con lo auténtico: absoluto de iris ultrapuro "
        "de Florencia, reforzado con la mejor esencia de vetiver.”")
FUENTE_INSP = ("<span class=\"fuente-line\">— Rodrigo Flores-Roux, perfumista · web oficial "
               "Wilgermain / Fragrantica [traducida]</span>")

ALT_1 = ('<div class="alt-item"><span class="alt-n">Neroli Portofino</span>'
         '<span class="alt-casa">Tom Ford · 2011</span>'
         '<span class="alt-rt">3,97/5 · 9.861 votos</span>'
         '<span class="alt-motivo">mismo perfumista y mismo eje cítrico-neroli, más floral blanco</span></div>')
ALT_2 = ('<div class="alt-item"><span class="alt-n">Portraits of Portofino</span>'
         '<span class="alt-casa">Birkholz · 2022</span>'
         '<span class="alt-rt">4,36/5 · 214 votos</span>'
         '<span class="alt-motivo">mismo territorio ligur, más verde y con más cuerpo</span></div>')
ALT_3 = ('<div class="alt-item"><span class="alt-n">Aqua Universalis</span>'
         '<span class="alt-casa">Maison Francis Kurkdjian · 2009</span>'
         '<span class="alt-rt">3,93/5 · 3.144 votos</span>'
         '<span class="alt-motivo">el cítrico-floral limpio de manual; una reseña lo llama pariente cercano</span></div>')
FUENTE_ALT = ('<span class="fuente-line" style="margin-left:44px;">Asociaciones de comunidad: reseñas '
              'Fragrantica (applebl0ssom, Gary.D) · “similar fragrances” Parfumo — 12-oct-2026</span>')

CITA = ("“Huele a zumo de limón, a bergamota, a agua de pepino, a hojas amargas y verdes de "
        "petitgrain y a una nota acuática: es como una limonada ácida con hojas verdes.”")
FUENTE_CITA = ('<span class="fuente-line">— JuliaToothFairy · reseña en Fragrantica, '
               '28-jul-2026 [traducida]</span>')

CLIMA = ("17,6 – 25,5 °C de sensación (ventana 08-18) · media 22,5 °C · lluvia 3 %<br>"
         "día 16,6 – 23,7 °C · ventana cálida y húmeda por la tarde: cítrico acuático")
SPRAYS = ("Sprays: <b>3</b> mañana (19,7 °C) · <b>2</b> tarde (24,8 °C)<br>"
          "<span class=\"caveat-pie\">que huela a limón recién cortado</span>")

CAPAS = ("    { w: 300, f:'#d99c26', t:'#f6cf66', l:'#a57112', c1:'SALIDA', txt:'CIDRA · PETITGRAIN · BERGAMOTA' },\n"
         "    { w: 420, f:'#3f8f5f', t:'#8fc98f', l:'#2a6b45', c1:'CORAZÓN', txt:'JAZMÍN SAMBAC · FLOR DE MANDARINO · LAVANDA' },\n"
         "    { w: 540, f:'#244c63', t:'#4d7f9e', l:'#142f40', c1:'FONDO', txt:'VETIVER · CÚRCUMA · IRIS DE FLORENCIA' }")


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
    t = sub1(t, r'<span class="lab" style="color:#177fa3;">', '<span class="lab" style="color:#2f7a4f;">', "lab corazón")
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
        "year": "2020",
        "concentracion": "Eau de Parfum",
        "genero": "Unisex",
        "familia": "Cítrica",
        "rating": R_NUM,
        "longevidad": "Longevidad",
        "estela": "moderada",
        "precio": "180 €",
        "nota-fondo": 'class="nota-fondo"',
        "rango": re.search(r"\d+[.,]\d+\s*[–-]\s*\d+[.,]\d+\s*°C", t) is not None,
        "media": "media 22,5",
        "lluvia": "lluvia 3 %",
    }
    fallos = [k for k, v in req.items() if (v is False or (v is True and False)) or v is None or
              (isinstance(v, str) and v not in t)]
    if req["rango"] is False:
        fallos.append("rango")
    if fallos:
        raise SystemExit("[ABORTA] faltan en el HTML: " + ", ".join(sorted(set(fallos))))

    out = os.path.join(BASE, f"perfume_del_dia_v5_{SLUG}.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(t)
    print(json.dumps({"html": out, "bytes": os.path.getsize(out), "fondo": FONDO}, ensure_ascii=False))


if __name__ == "__main__":
    main()
