#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 0-B (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 0-A."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-0-b-que-puedes-pedirle"
ART = LEC / "arte"
FONTS = BASE / "assets" / "fonts"
CREMA, NEGRO, NARANJA = "#F5EFE6", "#111111", "#FF7A00"

def face(fam, peso, archivo):
    b64 = base64.b64encode((FONTS / archivo).read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';font-weight:{peso};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")

CSS = (
 face("Poppins",400,"Poppins-400.woff2") + face("Poppins",600,"Poppins-600.woff2") +
 face("Poppins",700,"Poppins-700.woff2") + face("Poppins",800,"Poppins-800.woff2") +
 face("Inter",400,"Inter-400.woff2") + face("Inter",700,"Inter-700.woff2") +
 f"""
 @page {{ size: 1080px 1350px; margin: 0; }}
 * {{ margin:0; padding:0; box-sizing:border-box; -webkit-font-smoothing:antialiased; }}
 body {{ background:{CREMA}; font-family:'Poppins','Inter',sans-serif; color:{NEGRO}; }}
 .slide {{ width:1080px; height:1350px; background:{CREMA}; position:relative; overflow:hidden;
   padding:78px 84px 66px; display:flex; flex-direction:column; }}
 .top {{ display:flex; justify-content:space-between; align-items:baseline; }}
 .kicker {{ font-family:'Inter'; font-size:24px; font-weight:700; letter-spacing:3.4px; text-transform:uppercase; }}
 .kicker .n {{ color:{NARANJA}; }}
 .pager {{ font-family:'Inter'; font-size:24px; font-weight:700; color:{NARANJA}; letter-spacing:1px; }}
 h1 {{ font-size:86px; font-weight:800; line-height:0.98; text-transform:uppercase; letter-spacing:-1.6px; margin-top:34px; }}
 h1 .ac {{ color:{NARANJA}; }}
 .arte {{ display:flex; align-items:center; justify-content:center; flex:1; min-height:0; padding:6px 0; }}
 .arte img {{ max-height:520px; max-width:820px; }}
 .cuerpo {{ font-size:41px; line-height:1.34; font-weight:400; }}
 .caja {{ margin-top:26px; border-left:9px solid {NARANJA}; background:rgba(255,122,0,0.10);
   padding:26px 30px; font-size:37px; line-height:1.32; font-weight:600; }}
 .pasos {{ display:flex; flex-direction:column; gap:16px; margin-top:8px; }}
 .paso {{ display:flex; gap:22px; align-items:center; background:#fff; border:2px solid #1a1a1a;
   border-radius:16px; padding:20px 26px; font-size:33px; font-weight:600; }}
 .paso .num {{ font-family:'Inter'; font-weight:800; font-size:33px; color:#fff; background:{NARANJA};
   min-width:56px; height:56px; border-radius:12px; display:flex; align-items:center; justify-content:center; }}
 .dos {{ display:flex; gap:26px; flex:1; align-items:stretch; }}
 .col {{ flex:1; background:#fff; border:3px solid #1a1a1a; border-radius:20px; padding:30px 26px; display:flex; flex-direction:column; gap:14px; }}
 .col.mal {{ border-color:#b8483a; }}
 .col.bien {{ border-color:{NARANJA}; }}
 .col .tag {{ font-family:'Inter'; font-size:23px; font-weight:800; letter-spacing:2px; text-transform:uppercase; }}
 .col.mal .tag {{ color:#b8483a; }}
 .col.bien .tag {{ color:{NARANJA}; }}
 .col p {{ font-size:33px; line-height:1.3; }}
 .dato {{ font-size:104px; font-weight:800; letter-spacing:-3px; line-height:1; }}
 .dato .ac {{ color:{NARANJA}; }}
 .sub {{ font-size:30px; font-weight:600; margin-top:14px; color:#3a3a3a; }}
 .metodo {{ font-family:'Inter'; font-size:20px; color:#6b6459; margin-top:auto; }}
 .cierre-lista {{ display:flex; flex-direction:column; gap:20px; margin-top:10px; }}
 .cierre-lista div {{ font-size:44px; font-weight:700; }}
 .cierre-lista div span {{ color:{NARANJA}; }}
 .next {{ margin-top:auto; background:{NEGRO}; color:{CREMA}; border-radius:18px; padding:28px 30px;
   font-size:31px; font-weight:700; line-height:1.25; }}
 .next span {{ color:{NARANJA}; }}
 .pie {{ margin-top:22px; border-top:4px solid {NEGRO}; padding-top:18px; font-family:'Inter';
   font-size:24px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; display:flex; justify-content:space-between; }}
 .pie .ac {{ color:{NARANJA}; }}
 .tabla {{ display:flex; flex-direction:column; gap:14px; margin-top:8px; }}
 .fila3 {{ display:flex; gap:14px; }}
 .cel {{ flex:1; background:#fff; border:2px solid #1a1a1a; border-radius:14px; padding:18px 20px;
   font-size:27px; font-weight:600; text-align:center; }}
 .cel.k {{ background:{NEGRO}; color:{CREMA}; font-family:'Inter'; font-weight:800; }}
 .cel.ok {{ border-color:#2a9d5f; color:#1f7a48; }}
 .cel.ko {{ border-color:#b8483a; color:#a13c30; }}
 .th {{ font-family:'Inter'; font-size:22px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:#3a3a3a; text-align:center; }}
"""
)

def img(nombre, estilo=""):
    return f'<img src="file://{ART}/{nombre}" style="{estilo}" alt="">'

def slide(inner, pager, extra=""):
    return f'<section class="slide {extra}">\n{inner}\n</section>'

def top(kicker, pager):
    return f'<div class="top"><div class="kicker">{kicker}</div><div class="pager">{pager}</div></div>'

S = []

# --- S1 portada
S.append(slide(
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 0-B</span>", "1/7") +
 '<h1>QUÉ PEDIRLE <span class="ac">Y QUÉ NO</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Los usos que resuelve hoy y lo que cambia el <b>tamaño del modelo</b></div>'
 f'<div class="arte">{img("s1-caja-herramientas.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 0 · PIEZA 3</span></div>',
 "1/7"))

# --- S2 que es: los usos que SI
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>CUATRO USOS <span class="ac">QUE SÍ</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-papeles.png", "max-height:280px")}</div>'
 '<div class="pasos" style="margin-top:12px;">'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">1</div><div><b>RESUMIR</b> — un hilo de 40 correos → 5 líneas.</div></div>'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">2</div><div><b>REDACTAR</b> — un guion de 4 puntos → el correo entero.</div></div>'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">3</div><div><b>CLASIFICAR</b> — 200 reseñas → positivas o negativas.</div></div>'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">4</div><div><b>TRADUCIR / EXTRAER</b> — un texto en inglés → los datos que pides.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:20px;font-size:30px;">Los cuatro comparten una cosa: <b>el material se lo das tú</b>. El modelo no busca nada fuera; reescribe lo que le entregas.</div>',
 "2/7"))

# --- S3 como funciona
def _peligro(txt):
    return f'<div style="font-weight:400;font-size:25px;color:#6b6459;margin-top:6px;">NO le pides: {txt}</div>'

S.append(slide(
 top("LECCIÓN 0 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>ENTRA TEXTO, <span class="ac">SALE TEXTO</span></h1>'
 '<div class="pasos" style="margin-top:24px;">'
 '<div class="paso" style="font-size:31px;padding:15px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">1</div><div>Le das la instrucción y el material.' + _peligro("que busque fuera lo que no le has dado.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:15px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">2</div><div>Predice la siguiente pieza de texto.' + _peligro("cuentas exactas ni datos de hoy.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:15px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">3</div><div>Devuelve el texto con el formato que pediste.' + _peligro("que sepa si lo que dice es verdad.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:15px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">4</div><div>Tú lees, corriges y decides.' + _peligro("que asuma la responsabilidad del resultado.") + '</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:20px;font-size:29px;">Los cuatro usos de la slide anterior funcionan porque el paso 2 basta: <b>reescribir texto que ya existe</b> se le da bien. Lo que falla no es el idioma: es la exactitud.</div>',
 "3/7"))

# --- S4 confusion tipica
svg_tam = (
 '<svg width="900" height="330" viewBox="0 0 900 330" xmlns="http://www.w3.org/2000/svg">'
 '<text x="0" y="24" font-family="Inter,sans-serif" font-size="22" font-weight="700" fill="#6b6459">PARÁMETROS = TAMAÑO DEL MODELO</text>'
 '<rect x="0" y="48" width="150" height="76" rx="10" fill="#111111"/>'
 '<text x="24" y="98" font-family="Poppins,Inter,sans-serif" font-size="34" font-weight="800" fill="#F5EFE6">2,6B</text>'
 '<text x="170" y="98" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#3a3a3a">cabe en un portátil</text>'
 '<rect x="0" y="140" width="340" height="76" rx="10" fill="#FF7A00"/>'
 '<text x="24" y="190" font-family="Poppins,Inter,sans-serif" font-size="34" font-weight="800" fill="#ffffff">8B</text>'
 '<text x="360" y="190" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#3a3a3a">el más común en local</text>'
 '<rect x="0" y="232" width="560" height="76" rx="10" fill="#111111"/>'
 '<text x="24" y="282" font-family="Poppins,Inter,sans-serif" font-size="34" font-weight="800" fill="#F5EFE6">35B</text>'
 '<text x="580" y="282" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#3a3a3a">pide una GPU en serio</text>'
 '</svg>'
)

S.append(slide(
 top("LECCIÓN 0 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1>NO SIEMPRE <span class="ac">MÁS ES MEJOR</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{svg_tam}</div>'
 '<div class="dos" style="flex:0 0 auto;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:28px;">«Cuanto más grande, mejor en todo. Para clasificar necesito el de 70B.»</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ Lo correcto</span><p style="font-size:28px;">El tamaño se nota en la tarea difícil, no en todas. El grande cobra en recursos y en tiempo.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:29px;">Y al revés tampoco: «como es pequeño, no sirve» es falso. Para resumir, redactar o clasificar, un modelo de 2,6B hace el trabajo.</div>',
 "4/7"))

# --- S5 ejemplo real: la misma tarea en tres tamanos
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>LA MISMA TAREA, <span class="ac">TRES TAMAÑOS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-tres-llaves.png", "max-height:230px")}</div>'
 '<div class="tabla" style="margin-top:14px;">'
 '<div class="fila3"><div class="cel k" style="flex:0.75;">&nbsp;</div><div class="th">CLASIFICAR 5 RESEÑAS</div><div class="th">DAR EL IMPORTE</div><div class="th">CALCULAR EL TOTAL</div></div>'
 '<div class="fila3"><div class="cel k">2,6B</div><div class="cel ok">5/5</div><div class="cel ko">no lo da</div><div class="cel ok">360,00</div></div>'
 '<div class="fila3"><div class="cel k">8B</div><div class="cel ok">5/5</div><div class="cel ok">0,3 s</div><div class="cel ko">342,00</div></div>'
 '<div class="fila3"><div class="cel k">35B</div><div class="cel ok">5/5</div><div class="cel ok">48,8 s</div><div class="cel ok">360,00</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:28px;">Mismo texto de entrada para los tres. Lo que cambia no es «entiende o no entiende»: es <b>dónde acierta</b>. Y el que falló la cuenta no fue el pequeño: fue el de 8B.</div>',
 "5/7"))

# --- S6 dato medible (medicion propia 18-sep-2026)
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>CLASIFICAR: 3 DE 3 · <span class="ac">LA CUENTA: FALLA 1</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s6-reloj-arena.png", "max-height:250px")}</div>'
 '<div class="dato">5/5</div>'
 '<div class="sub">los tres modelos clasificaron las cinco reseñas sin fallar. Para reescribir texto, hasta el pequeño sirve.</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:24px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ La cuenta</span><p style="font-size:27px;">El de 8B contestó <b>342,00</b> cuando el total era <b>360,00</b> (4 × 89,50 − 10,00 + 12,00). Ninguno es fiable para aritmética: comprueba el número.</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ El tiempo</span><p style="font-size:27px;">El mismo importe: el 8B en <b>0,3 s</b> y el 35B en <b>48,8 s</b> — unas 160 veces más para el mismo acierto. El de 2,6B se quedó razonando sin llegar a contestar.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:28px;">Para reescribir texto, hasta el pequeño vale. Para exactitud, <b>no lo uses</b>: dale el dato o calcula tú.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · 18-SEP-2026 · LM STUDIO, TEMPERATURA 0, LA MISMA PREGUNTA A 2,6B / 8B / 35B</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:30px;">'
 '<div><span>1.</span> Si la tarea es reescribir texto que le das, hasta un modelo pequeño sirve.</div>'
 '<div><span>2.</span> Para cuentas y datos exactos, dale el dato o calcula tú.</div>'
 '<div><span>3.</span> El tamaño se paga en recursos; se nota en la tarea difícil.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-cuaderno.png", "max-height:300px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 1</span><br>Instrucciones: el prompt. La pieza donde esto se vuelve práctico.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 0-B</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-0-b.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
