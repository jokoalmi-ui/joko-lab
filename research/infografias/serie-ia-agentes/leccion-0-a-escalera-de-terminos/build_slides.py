#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 0-A (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-0-a-escalera-de-terminos"
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
 .cuerpo b {{ font-weight:700; }}
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
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 0-A</span>", "1/7") +
 '<h1>LA ESCALERA DE <span class="ac">TÉRMINOS</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">IA, machine learning, deep learning y LLM: <b>qué es cada cosa</b></div>'
 f'<div class="arte">{img("s1-escalera.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 0 · PIEZA 2</span></div>',
 "1/7"))

# --- S2 que es
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>CUATRO PALABRAS, CUATRO <span class="ac">ALTURAS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-munecas.png", "max-height:300px")}</div>'
 '<div class="pasos" style="margin-top:14px;">'
 '<div class="paso" style="font-size:30px;padding:16px 24px;"><div class="num" style="font-size:26px;min-width:46px;height:46px;">1</div><div><b>IA</b> — cualquier máquina que hace algo que llamamos inteligente.</div></div>'
 '<div class="paso" style="font-size:30px;padding:16px 24px;"><div class="num" style="font-size:26px;min-width:46px;height:46px;">2</div><div><b>ML</b> — aprende de datos, no de reglas escritas.</div></div>'
 '<div class="paso" style="font-size:30px;padding:16px 24px;"><div class="num" style="font-size:26px;min-width:46px;height:46px;">3</div><div><b>DL</b> — redes neuronales con muchas capas.</div></div>'
 '<div class="paso" style="font-size:30px;padding:16px 24px;"><div class="num" style="font-size:26px;min-width:46px;height:46px;">4</div><div><b>LLM</b> — deep learning especializado en lenguaje.</div></div>'
 '</div>',
 "2/7"))

# --- S3 como funciona
def _peligro(txt):
    return f'<div style="font-weight:400;font-size:25px;color:#6b6459;margin-top:6px;">NO le pides: {txt}</div>'

S.append(slide(
 top("LECCIÓN 0 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>LOS CUATRO <span class="ac">PELDAÑOS</span></h1>'
 '<div class="pasos" style="margin-top:26px;">'
 '<div class="paso" style="font-size:31px;padding:16px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">1</div><div><b>IA</b> — un rival de ajedrez con reglas fijas.' + _peligro("que aprenda de tus datos.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:16px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">2</div><div><b>ML</b> — predecir qué cliente se dará de baja.' + _peligro("que te explique el porqué.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:16px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">3</div><div><b>DL</b> — reconocer una cara en una foto.' + _peligro("que te diga en qué se fija.") + '</div></div>'
 '<div class="paso" style="font-size:31px;padding:16px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">4</div><div><b>LLM</b> — escribirte un correo entero.' + _peligro("tus datos ni cuentas exactas.") + '</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:22px;font-size:30px;">Cada peldaño <b>hereda</b> el anterior. Por eso a cada uno le pides una cosa: cumplir reglas, acertar una predicción, escribir texto.</div>',
 "3/7"))

# --- S4 confusion típica
svg_barras = (
 '<svg width="900" height="400" viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">'
 '<rect x="0" y="0" width="430" height="72" rx="10" fill="#111111"/>'
 '<text x="26" y="49" font-family="Poppins,Inter,sans-serif" font-size="36" font-weight="800" fill="#F5EFE6">IA</text>'
 '<text x="470" y="49" font-family="Inter,sans-serif" font-size="27" font-weight="600" fill="#3a3a3a">cualquier máquina &#171;inteligente&#187;</text>'
 '<rect x="0" y="104" width="336" height="72" rx="10" fill="#FF7A00"/>'
 '<text x="26" y="153" font-family="Poppins,Inter,sans-serif" font-size="36" font-weight="800" fill="#ffffff">ML</text>'
 '<text x="376" y="153" font-family="Inter,sans-serif" font-size="27" font-weight="600" fill="#3a3a3a">aprende de datos</text>'
 '<rect x="0" y="208" width="242" height="72" rx="10" fill="#111111"/>'
 '<text x="26" y="257" font-family="Poppins,Inter,sans-serif" font-size="36" font-weight="800" fill="#F5EFE6">DL</text>'
 '<text x="282" y="257" font-family="Inter,sans-serif" font-size="27" font-weight="600" fill="#3a3a3a">redes profundas</text>'
 '<rect x="0" y="312" width="152" height="72" rx="10" fill="#FF7A00"/>'
 '<text x="26" y="361" font-family="Poppins,Inter,sans-serif" font-size="36" font-weight="800" fill="#ffffff">LLM</text>'
 '<text x="192" y="361" font-family="Inter,sans-serif" font-size="27" font-weight="600" fill="#3a3a3a">escribe texto</text>'
 '</svg>'
)

S.append(slide(
 top("LECCIÓN 0 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1>NO SON <span class="ac">SINÓNIMOS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:16px 0;">{svg_barras}</div>'
 '<div class="dos" style="flex:0 0 auto;">'
 '<div class="col mal" style="padding:22px 24px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:30px;">«La IA, el machine learning y ChatGPT son lo mismo.»</p></div>'
 '<div class="col bien" style="padding:22px 24px;"><span class="tag">✓ Lo correcto</span><p style="font-size:30px;">Todo LLM es IA. Casi ninguna IA es un LLM.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:20px;font-size:31px;">Un filtro de spam es ML y no es deep learning. Y un LLM no "sabe" cosas: <b>predice texto</b>.</div>',
 "4/7"))

# --- S5 ejemplo real
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>LA MISMA TIENDA, CUATRO <span class="ac">SOLUCIONES</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:8px 0;">{img("s5-cesta.png", "max-height:230px")}</div>'
 '<div class="pasos" style="margin-top:12px;">'
 '<div class="paso" style="font-size:29px;padding:14px 24px;"><div><b>Reglas</b> → si compra pan, ofrecer mantequilla.</div></div>'
 '<div class="paso" style="font-size:29px;padding:14px 24px;"><div><b>ML</b> → predecir qué producto se va a agotar.</div></div>'
 '<div class="paso" style="font-size:29px;padding:14px 24px;"><div><b>DL</b> → leer la matrícula de un coche en el parking.</div></div>'
 '<div class="paso" style="font-size:29px;padding:14px 24px;"><div><b>LLM</b> → contestar por escrito una reclamación.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:22px;font-size:31px;">Los cuatro son IA. Solo el último <b>escribe como una persona</b>.</div>',
 "5/7"))

# --- S6 dato medible (prueba real: sin el dato inventa, con el dato acierta)
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>SIN EL DATO, <span class="ac">SE LO INVENTA</span></h1>'
 '<div class="dato" style="font-size:96px;margin-top:24px;">0/3 <span class="ac">→ 3/3</span></div>'
 '<div class="sub" style="font-size:27px;margin-top:6px;">aciertos sin el dato en el texto · con el dato en el texto</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:20px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Sin darle el dato</span>'
 '<p style="font-size:30px;">No dijo «no lo sé». Contestó <b>1</b>, <b>45</b> y <b>1234.56</b>.</p>'
 '<p style="font-size:24px;color:#6b6459;">Le pregunté cuántos modelos de IA tengo instalados, cuántas piezas tiene esta serie y el total de un albarán que no existe.</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ Dándole el dato</span>'
 '<p style="font-size:30px;">Contestó <b>15</b>, <b>8</b> y <b>30.50</b>. Las tres correctas.</p>'
 '<p style="font-size:24px;color:#6b6459;">El mismo dato, escrito por mí en la pregunta. Ni una cifra inventada.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:29px;">Un LLM no consulta tu ordenador: <b>predice texto</b>. Si el dato no está en lo que le escribes, se lo inventa con toda la seguridad del mundo.</div>'
 '<div class="metodo">Medición propia · 16-sep-2026 · qwen2.5:7b en local (CPU, temperatura 0), 3 preguntas con y sin el dato en el contexto</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:34px;">'
 '<div><span>1.</span> IA es el paraguas; el LLM es la punta.</div>'
 '<div><span>2.</span> ML aprende de datos; DL son redes profundas.</div>'
 '<div><span>3.</span> Pide texto al LLM; no le pidas exactitud.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-mochila.png", "max-height:300px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 0-B</span><br>Qué puedes pedirle y qué no: usos y tamaño del modelo.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 0-A</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-0-a.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
