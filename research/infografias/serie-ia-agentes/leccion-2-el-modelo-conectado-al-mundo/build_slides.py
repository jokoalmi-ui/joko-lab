#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 2 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 1.
OJO: la slide 6 lleva el dato medible; si la medicion no se ha ejecutado, va con
[PENDIENTE DE MEDIR] y NO se publica."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-2-el-modelo-conectado-al-mundo"
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
 .mini {{ font-size:25px; line-height:1.34; font-weight:600; }}
 .mini b {{ font-family:'Inter'; font-weight:800; }}
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
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 2</span>", "1/7") +
 '<h1>CONECTADO<br>AL <span class="ac">MUNDO</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Tus datos y tus acciones: dos formas de que deje de adivinar</div>'
 f'<div class="arte">{img("s1-puente.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 2 · PIEZA 5</span></div>',
 "1/7"))

# --- S2 que es: dos formas
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>DOS FORMAS, <span class="ac">NO UNA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-libro-llave.png", "max-height:290px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:14px;">'
 '<div class="col bien" style="padding:22px 22px;"><span class="tag">1 · Tus datos (RAG)</span>'
 '<p style="font-size:28px;">El modelo <b>consulta antes de responder</b>: tus documentos, tus facturas, tus notas.</p>'
 '<div class="mono">pregunta → busca en tus ficheros → responde citando</div></div>'
 '<div class="col bien" style="padding:22px 22px;"><span class="tag">2 · Tus acciones (herramientas)</span>'
 '<p style="font-size:28px;">El modelo <b>pide que ejecutes algo</b>: una búsqueda, una suma, crear un evento.</p>'
 '<div class="mono">pregunta → pide la función → ejecuta tu código</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:28px;">En los dos casos deja de adivinar: en uno porque <b>lee</b>, en el otro porque <b>delega</b>. Lo que NO hace en ninguno de los dos es aprender: eso es otra cosa.</div>',
 "2/7"))

# --- S3 como funciona
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>DOS CAMINOS <span class="ac">DISTINTOS</span></h1>'
 '<div class="dos" style="flex:0 0 auto;margin-top:24px;">'
 '<div class="col" style="padding:22px 20px;"><span class="tag">Camino 1 · RAG</span>'
 '<div class="mini">1. <b>Trocear</b> tus documentos en fragmentos pequeños.</div>'
 '<div class="mini">2. Convertir cada fragmento en <b>vectores</b> y guardarlos.</div>'
 '<div class="mini">3. <b>Buscar por similitud</b> los que encajan con la pregunta.</div>'
 '<div class="mini">4. Meter esos fragmentos en el prompt: responde <b>leyéndolos</b>.</div>'
 '</div>'
 '<div class="col" style="padding:22px 20px;"><span class="tag">Camino 2 · Herramientas</span>'
 '<div class="mini">1. Le <b>declaras</b> qué funciones existen y qué necesitan.</div>'
 '<div class="mini">2. El modelo devuelve una <b>llamada</b>: nombre + argumentos.</div>'
 '<div class="mini">3. Tu código la <b>ejecuta</b> de verdad: aquí sí se calcula.</div>'
 '<div class="mini">4. El resultado vuelve y el modelo <b>redacta</b> la respuesta.</div>'
 '</div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:28px;">El modelo no ejecuta nada: <b>pide</b>. El que ejecuta es tu código, y por eso el resultado es verificable. «Razonar antes de responder» es un tercer truco, pero no conecta con nada: solo ordena el razonamiento.</div>',
 "3/7"))

# --- S4 confusion tipica
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1 style="margin-top:20px;font-size:80px;">CUATRO NOMBRES, <span class="ac">TRES COSAS</span></h1>'
 '<div class="tabla" style="margin-top:12px;gap:8px;">'
 '<div class="fila3"><div class="cel k">NOMBRE</div><div class="cel k">QUÉ ES</div></div>'
 '<div class="fila3"><div class="cel">Herramientas (tools)</div><div class="cel" style="text-align:left;">La <b>capacidad</b>: funciones que le declaras.</div></div>'
 '<div class="fila3"><div class="cel">Tool calling / function calling</div><div class="cel" style="text-align:left;">El <b>mecanismo</b>: cómo las pide. Dos nombres, lo mismo.</div></div>'
 '<div class="fila3"><div class="cel">MCP</div><div class="cel" style="text-align:left;">El <b>estándar</b>: un enchufe común para no reescribir cada integración.</div></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:10px;">'
 '<div class="col mal" style="padding:14px 20px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:27px;">«RAG es lo mismo que fine-tuning.» Y «si le doy mis datos, el modelo los aprende».</p></div>'
 '<div class="col bien" style="padding:14px 20px;"><span class="tag">✓ Lo correcto</span><p style="font-size:27px;">RAG es <b>memoria consultable</b>: se actualiza sin reentrenar y se puede citar la fuente. Fine-tuning <b>no es una base de datos</b>: cambia el tono, el formato o la tarea.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:8px;font-size:27px;">La prueba rápida: si te importa <b>qué fuente lo dice</b> y que esté al día, es RAG. Si te importa que responda con <b>tu formato y tu tono</b>, es fine-tuning.</div>',
 "4/7"))

# --- S5 ejemplo real
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>NO SABE, Y <span class="ac">NO TE LO DICE</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-calculadora-recibos.png", "max-height:250px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:14px;">'
 '<div class="col mal" style="padding:22px 22px;"><span class="tag">✗ Sin los datos (6/6)</span><p style="font-size:27px;">Le pides el total de luz <b>sin darle la tabla</b>. Respuesta literal, las seis veces: <b>0</b>. Ni un «no lo sé»: un cero con el mismo tono seguro.</p></div>'
 '<div class="col bien" style="padding:22px 22px;"><span class="tag">✓ Con los datos (6/6)</span><p style="font-size:27px;">Con la tabla delante acierta los seis totales —<b>1302,25</b> el de luz— pero el número sale de <b>su</b> aritmética: no hay nada que auditar.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:28px;">Con datos acierta y sin datos se lo inventa, y las dos respuestas suenan igual de firmes. Eso es lo que resuelve la herramienta: el número sale de tu código, no de su memoria.</div>',
 "5/7"))

# --- S6 dato medible: medicion real ejecutada el 22-sep-2026 (medicion-herramientas.py)
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>6/6 LLAMADAS <span class="ac">BIEN FORMADAS</span></h1>'
 '<div class="dato" style="margin-top:26px;">6/6</div>'
 '<div class="sub">Mismo modelo, mismas 6 preguntas, temperatura 0. <b>Sin los datos</b>: 6/6 respuestas «0». <b>Con la tabla delante</b>: 6/6 aciertos calculando él. <b>Con la función declarada</b>: 6/6 llamadas bien formadas y ejecutables, y el número lo devuelve el código. Control con la temperatura a 0,8: 6/6 también.</div>'
 '<div class="caja" style="margin-top:20px;font-size:28px;">Lo que separa una respuesta plausible de una verificable no es el acierto: es <b>de dónde sale el número</b>. Declararle la herramienta no lo hace más listo; lo hace auditable.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL) · N=6 POR CONDICIÓN, UNA PASADA · 22-SEP-2026</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 2 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:30px;">'
 '<div><span>1.</span> Conectar el modelo son dos cosas: tus datos y tus acciones.</div>'
 '<div><span>2.</span> Con datos consulta; con herramientas delega: el que calcula es tu código.</div>'
 '<div><span>3.</span> Herramientas, tool calling y MCP no son lo mismo: capacidad, mecanismo y estándar.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-candado.png", "max-height:280px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 3</span><br>El agente: el bucle.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 2</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-2.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
