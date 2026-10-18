#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 1 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 0-B."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-1-instrucciones-el-prompt"
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
 .mono {{ font-family:'Inter',monospace; font-size:24px; line-height:1.35; background:#f3ecdf; border-radius:10px; padding:14px 16px; word-break:break-word; }}
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
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 1</span>", "1/7") +
 '<h1>LA <span class="ac">INSTRUCCIÓN</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Tarea, formato y rol: las tres cosas que cambian la respuesta</div>'
 f'<div class="arte">{img("s1-cartel-flecha.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 1 · PIEZA 4</span></div>',
 "1/7"))

# --- S2 que es: las tres piezas
S.append(slide(
 top("LECCIÓN 1 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>TRES COSAS, <span class="ac">NO UNA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-tres-piezas.png", "max-height:300px")}</div>'
 '<div class="pasos" style="margin-top:12px;">'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">1</div><div><b>TAREA</b> — qué quieres que haga: «clasifica estas reseñas».</div></div>'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">2</div><div><b>FORMATO</b> — cómo quieres la salida: «una línea por reseña: POSITIVA o NEGATIVA».</div></div>'
 '<div class="paso" style="font-size:29px;padding:15px 24px;"><div class="num" style="font-size:25px;min-width:46px;height:46px;">3</div><div><b>ROL</b> — desde dónde lo hace: «eres un revisor de producto».</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:20px;font-size:29px;">Si falta la tarea, no sabe qué hacer. Si falta el formato, acierta pero no te sirve para pegarlo en otro sitio. El rol no es obligatorio: cambia el tono, no los datos.</div>',
 "2/7"))

# --- S3 como funciona
def _peligro(txt):
    return f'<div style="font-weight:400;font-size:25px;color:#6b6459;margin-top:6px;">NO le pides: {txt}</div>'

S.append(slide(
 top("LECCIÓN 1 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>LA INSTRUCCIÓN <span class="ac">ES CONTEXTO</span></h1>'
 '<div class="pasos" style="margin-top:24px;">'
 '<div class="paso" style="font-size:30px;padding:14px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">1</div><div>Le das la instrucción y el material.' + _peligro("que adivine lo que no le has dicho.") + '</div></div>'
 '<div class="paso" style="font-size:30px;padding:14px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">2</div><div>Un ejemplo pesa más que una explicación larga.' + _peligro("deduzca un formato que no le has enseñado.") + '</div></div>'
 '<div class="paso" style="font-size:30px;padding:14px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">3</div><div>El formato exigido hace que su salida la lea otro programa.' + _peligro("que sepa qué vas a hacer tú con esa salida.") + '</div></div>'
 '<div class="paso" style="font-size:30px;padding:14px 24px;"><div class="num" style="min-width:52px;height:52px;font-size:30px;">4</div><div>La temperatura cambia cuánto varía, no lo que sabe.' + _peligro("que la variedad y el contenido sean lo mismo.") + '</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:20px;font-size:29px;">Casi todo lo que se llama «prompt engineering» es esto: <b>escribir la tarea y el formato</b>. No hay frase mágica; hay instrucción concreta.</div>',
 "3/7"))

# --- S4 confusion tipica
svg_len = (
 '<svg width="900" height="300" viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg">'
 '<text x="0" y="24" font-family="Inter,sans-serif" font-size="22" font-weight="700" fill="#6b6459">CARACTERES DE RESPUESTA · MISMA TAREA, MISMA TANDA</text>'
 '<rect x="0" y="52" width="620" height="82" rx="10" fill="#111111"/>'
 '<text x="24" y="105" font-family="Poppins,Inter,sans-serif" font-size="34" font-weight="800" fill="#F5EFE6">1.600</text>'
 '<text x="650" y="105" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#3a3a3a">sin decir el formato</text>'
 '<rect x="0" y="154" width="88" height="82" rx="10" fill="#FF7A00"/>'
 '<text x="112" y="207" font-family="Poppins,Inter,sans-serif" font-size="34" font-weight="800" fill="#3a3a3a">228</text>'
 '<text x="230" y="207" font-family="Inter,sans-serif" font-size="26" font-weight="600" fill="#3a3a3a">con el formato exigido</text>'
 '<text x="0" y="284" font-family="Inter,sans-serif" font-size="23" font-weight="600" fill="#6b6459">Las dos clasificaron bien las seis reseñas. Solo una se puede usar con código.</text>'
 '</svg>'
)

S.append(slide(
 top("LECCIÓN 1 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1>NO ES <span class="ac">UNA FRASE MÁGICA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{svg_len}</div>'
 '<div class="dos" style="flex:0 0 auto;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:28px;">«El truco está en una frase mágica: "eres un experto en…".» Y «cuanto más larga, mejor».</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ Lo correcto</span><p style="font-size:28px;">El rol cambia el tono, no los datos: lo que arregla la salida es la tarea y el formato. Más texto no es más precisión.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:29px;">Y una trampa de al lado: subir la temperatura no hace al modelo «más listo». En la prueba cambió la respuesta —205 frente a 228 caracteres— pero mantuvo el formato.</div>',
 "4/7"))

# --- S5 ejemplo real: la misma peticion en dos formas
S.append(slide(
 top("LECCIÓN 1 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>LA MISMA PETICIÓN, <span class="ac">DOS FORMAS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-dos-formas.png", "max-height:260px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:16px;">'
 '<div class="col mal" style="padding:22px 22px;"><span class="tag">✗ Sin decir el formato</span><p style="font-size:27px;">«1. POSITIVA. 2. NEGATIVA… Explicación breve (por ítem): la primera reseña habla de…»</p><div class="mono">1.600 caracteres · se lee, no se procesa</div></div>'
 '<div class="col bien" style="padding:22px 22px;"><span class="tag">✓ Formato exigido</span><div class="mono">[{"id":1,"sentimiento":"positiva"}, {"id":2,"sentimiento":"negativa"}, …]</div><p style="font-size:27px;">Se pega en cualquier sitio y otro programa lo lee.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:28px;">La diferencia no es que entienda mejor: es que le has dicho <b>dónde cortar</b>. Exigir el formato es la frontera entre un texto que se lee y una salida que se procesa.</div>',
 "5/7"))

# --- S6 dato medible (medicion propia 20-sep-2026)
S.append(slide(
 top("LECCIÓN 1 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>ACERTÓ IGUAL, <span class="ac">SIRVIÓ DISTINTO</span></h1>'
 '<div class="dato" style="margin-top:26px;">6/6</div>'
 '<div class="sub">las seis reseñas clasificadas bien en <b>las tres condiciones</b>: la instrucción vaga acertó tanto como la que exigía JSON.</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:26px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Sin decir el formato</span><p style="font-size:27px;"><b>1.600 caracteres</b> · 52,8 s · texto con explicación por ítem, imposible de leer con código.</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ Formato exigido</span><p style="font-size:27px;"><b>228 caracteres</b> · 30,0 s · JSON válido tal cual, listo para usar.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:28px;">El formato no arregla los aciertos: <b>arregla el uso</b>. Si la salida la lees tú, la prosa vale; si la lee un programa, exige el formato.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · 20-SEP-2026 · IBM/GRANITE4.2:8B EN OLLAMA · 6 RESEÑAS · TEMPERATURA 0 (CONTROL A 0,8)</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 1 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:30px;">'
 '<div><span>1.</span> Toda instrucción útil dice la tarea y el formato.</div>'
 '<div><span>2.</span> Lo que se llama «truco» casi siempre es haber escrito lo que querías.</div>'
 '<div><span>3.</span> El formato no mejora la respuesta: la hace usable.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-cuaderno.png", "max-height:300px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 2</span><br>El modelo conectado al mundo: datos y herramientas.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 1</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-1.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
