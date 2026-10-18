#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la PIEZA DE CIERRE (estilo MAURYS, 1080x1350).

Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado del build_slides.py de la Leccion 5 (misma familia visual: crema #F5EFE6,
tinta #111111, acento naranja #FF7A00).

Es la pieza 9: NO es una leccion del curso (6 niveles, 0-5) — es el mapa que cierra
el arco. Por eso los kickers dicen CIERRE y no LECCION: 7 slides, la primera con el
indice de niveles, la segunda pieza a pieza, y la slide 6 con las cifras que se
recalculan (no se heredan) con verificar_cifras.py desde los dos crudos copiados
a esta carpeta: medicion-multiagente-20260927.json y medicion-alucinaciones-20260914.json.
"""
import base64
import pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-cierre-mapa-de-la-serie"
ART = LEC / "arte"
FONTS = BASE / "assets" / "fonts"
CREMA, NEGRO, NARANJA = "#F5EFE6", "#111111", "#FF7A00"


def face(fam, peso, archivo):
    b64 = base64.b64encode((FONTS / archivo).read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';font-weight:{peso};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


CSS = (
 face("Poppins", 400, "Poppins-400.woff2") + face("Poppins", 600, "Poppins-600.woff2") +
 face("Poppins", 700, "Poppins-700.woff2") + face("Poppins", 800, "Poppins-800.woff2") +
 face("Inter", 400, "Inter-400.woff2") + face("Inter", 600, "Inter-600.woff2") +
 face("Inter", 700, "Inter-700.woff2") + face("Inter", 800, "Inter-800.woff2") +
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
 .paso .idp {{ font-family:'Inter'; font-weight:800; font-size:22px; color:#fff; background:{NARANJA};
   min-width:112px; padding:0 8px; height:52px; border-radius:12px; display:flex; align-items:center; justify-content:center; }}
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
 .cel {{ flex:1; background:#fff; border:2px solid #1a1a1a; border-radius:14px; padding:12px 18px;
   font-size:23px; font-weight:600; text-align:center; }}
 .cel.k {{ background:{NEGRO}; color:{CREMA}; font-family:'Inter'; font-weight:800; }}
 .cel.ok {{ border-color:#2a9d5f; color:#1f7a48; }}
 .cel.ko {{ border-color:#b8483a; color:#a13c30; }}
 .cel b {{ font-family:'Inter'; font-weight:800; }}
 .th {{ font-family:'Inter'; font-size:22px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:#3a3a3a; text-align:center; }}
""")


def img(nombre, estilo=""):
    return f'<img src="file://{ART}/{nombre}" style="{estilo}" alt="">'


def slide(inner, extra=""):
    return f'<section class="slide {extra}">\n{inner}\n</section>'


def top(kicker, pager):
    return f'<div class="top"><div class="kicker">{kicker}</div><div class="pager">{pager}</div></div>'


S = []

# --- S1 portada
S.append(slide(
 top("CURSO DE IA Y AGENTES · <span class='n'>CIERRE</span>", "1/7") +
 '<h1>EL MAPA DE LA <span class="ac">SERIE</span></h1>'
 '<div class="sub" style="font-size:36px;margin-top:16px;">6 niveles y 8 piezas: de «qué es un LLM» a sacarlo a producción</div>'
 f'<div class="arte">{img("s1-escalera-crema.png")}</div>'
 '<div class="pie"><span>6 NIVELES · 8 PIEZAS</span><span class="ac">CIERRE · PIEZA 9</span></div>'))

# --- S2 el mapa (indice de niveles)
S.append(slide(
 top("CIERRE · <span class='n'>1/5 EL MAPA</span>", "2/7") +
 '<h1 style="font-size:68px;margin-top:8px;">SEIS NIVELES, <span class="ac">UNA ESCALERA</span></h1>'
 '<div class="pasos" style="margin-top:10px;gap:6px;">'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">0</div>'
 '<div><b>FUNDAMENTOS</b> — Qué es un LLM, la escalera de términos y qué puedes pedirle. <b>Te llevas</b>: no busca, genera, y tiene un techo de contexto.</div></div>'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">1</div>'
 '<div><b>INSTRUCCIONES</b> — Cómo pedirlo: formato, ejemplos y rol. <b>Te llevas</b>: el mismo modelo, otra instrucción, otra salida.</div></div>'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">2</div>'
 '<div><b>CONECTADO AL MUNDO</b> — Tus documentos (RAG) y herramientas. <b>Te llevas</b>: pasa de hablar a tocar tus ficheros.</div></div>'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">3</div>'
 '<div><b>EL BUCLE</b> — Percibir, razonar, actuar y revisar. <b>Te llevas</b>: contestar no es lo mismo que hacer.</div></div>'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">4</div>'
 '<div><b>DE UNO A MUCHOS</b> — Varios agentes con un crítico. <b>Te llevas</b>: colaborar cuesta x3,90 en tokens y x4,68 en tiempo (medido).</div></div>'
 '<div class="paso" style="padding:10px 20px;font-size:25px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:26px;">5</div>'
 '<div><b>PRODUCCIÓN</b> — Fiabilidad, coste y límites. <b>Te llevas</b>: el listón lo fija una batería de casos, no una demo.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:12px;font-size:24px;padding:16px 22px;">El orden no es decorativo: casi todos los atascos que veo son <b>una pieza usada sin la anterior</b>. Si una te suena a chino, el hueco está antes.</div>'
 ))

# --- S3 pieza a pieza (que te llevas de cada una)
S.append(slide(
 top("CIERRE · <span class='n'>2/5 PIEZA A PIEZA</span>", "3/7") +
 '<h1 style="font-size:66px;margin-top:6px;">QUÉ TE LLEVAS DE <span class="ac">CADA UNA</span></h1>'
 '<div class="pasos" style="margin-top:10px;gap:7px;">'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L0</div>'
 '<div><b>Qué es un LLM</b> — genera, no consulta; y cada palabra cuesta ~1,4 tokens (medido).</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L0-A</div>'
 '<div><b>La escalera de términos</b> — dejar de mezclar cuatro palabras que no son lo mismo.</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L0-B</div>'
 '<div><b>Qué puedes pedirle</b> — lo que sí (resumir, clasificar, traducir) y por qué el tamaño decide.</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L1</div>'
 '<div><b>Instrucciones: el prompt</b> — formato, ejemplos y rol: pedir bien cambia la salida.</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L2</div>'
 '<div><b>El modelo conectado al mundo</b> — tus documentos (RAG) y herramientas: de hablar a hacer.</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L3</div>'
 '<div><b>El agente: el bucle</b> — percibir, razonar, actuar, revisar: la diferencia con un chat.</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L4</div>'
 '<div><b>De uno a muchos</b> — colaborar cuesta x3,90 tokens y x4,68 tiempo para el mismo acierto (medido).</div></div>'
 '<div class="paso" style="padding:9px 16px;font-size:25px;gap:14px;"><div class="idp">L5</div>'
 '<div><b>Producción: fiabilidad, coste y límites</b> — el listón es una batería de casos, no una demo.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:14px;font-size:25px;padding:18px 22px;">Ocho piezas, una idea cada una. Ninguna pide programar: piden <b>leerlas en orden</b>.</div>'
 ))

# --- S4 confusion tipica
S.append(slide(
 top("CIERRE · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1 style="margin-top:10px;font-size:80px;">EMPEZAR POR <span class="ac">EL FINAL</span></h1>'
 '<div class="tabla" style="margin-top:16px;gap:8px;">'
 '<div class="fila3"><div class="cel k">SE DICE</div><div class="cel k">QUÉ PASA</div></div>'
 '<div class="fila3"><div class="cel">«Con ChatGPT ya sé lo suficiente»</div><div class="cel" style="text-align:left;">El chat te da la salida; la pieza que falta es la que la vuelve <b>repetible</b>.</div></div>'
 '<div class="fila3"><div class="cel">«Los agentes son lo importante»</div><div class="cel" style="text-align:left;">Un agente sin instrucciones ni datos es un bucle que se equivoca rápido y caro.</div></div>'
 '<div class="fila3"><div class="cel">«Un modelo mejor lo arregla»</div><div class="cel" style="text-align:left;">El modelo es una pieza: el listón lo fija el control más flojo.</div></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col mal" style="padding:14px 18px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:23px;">«Salto directo al nivel 5 y monto un agente el primer día.»</p></div>'
 '<div class="col bien" style="padding:14px 18px;"><span class="tag">✓ Lo correcto</span><p style="font-size:23px;">Entrar por la pieza que cubre tu duda y subir de una en una: cada nivel ahorra un atasco del siguiente.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:10px;font-size:27px;">El orden de la serie no es un temario: es el orden en el que aparecen los atascos.</div>'
 ))

# --- S5 ejemplo real (una tarea, seis capas)
S.append(slide(
 top("CIERRE · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1 style="font-size:74px;margin-top:6px;">UNA TAREA, <span class="ac">SEIS CAPAS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:2px 0;">{img("s5-torre-capas-crema.png", "max-height:190px")}</div>'
 '<div class="sub" style="font-size:26px;margin-top:6px;">«Resume este PDF y avísame por correo»: lo mismo, con lo que añade cada nivel.</div>'
 '<div class="pasos" style="margin-top:10px;gap:7px;">'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">0</div><div>Saber qué puede hacer: resume, pero <b>no copia</b> literalmente.</div></div>'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">1</div><div>Pedirlo bien: formato, longitud y a quién va dirigido.</div></div>'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">2</div><div>Darle el PDF y el correo: el dato y la herramienta.</div></div>'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">3</div><div>Dejarlo en bucle: que lo mande, lo compruebe y se repita si falta algo.</div></div>'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">4</div><div>Poner dos: uno resume y otro revisa (y cuesta x3,90).</div></div>'
 '<div class="paso" style="padding:10px 18px;font-size:26px;gap:16px;"><div class="num" style="min-width:48px;height:48px;font-size:24px;">5</div><div>Medirlo: diez PDFs de prueba y un techo de gasto.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:12px;font-size:26px;padding:18px 22px;">La misma tarea existe en el nivel 0 y en el nivel 5. Lo que cambia es <b>lo que se cae por el camino</b>.</div>'
 ))

# --- S6 dato medible (cifras recalculadas del crudo, no heredadas)
S.append(slide(
 top("CIERRE · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1 style="font-size:76px;margin-top:6px;">LA SERIE EN <span class="ac">NÚMEROS</span></h1>'
 '<div class="dato" style="margin-top:14px;">0<span class="ac">/81</span></div>'
 '<div class="sub" style="font-size:27px;">respuestas que se inventaron un dato: <b>27 casos x 3 pasadas</b>, con 16 aciertos y 11 abstenciones correctas en cada una.</div>'
 '<div class="tabla" style="margin-top:14px;gap:8px;">'
 '<div class="fila3"><div class="cel">8 piezas · 6 niveles</div><div class="cel">3 mediciones propias</div></div>'
 '<div class="fila3"><div class="cel">1,4 tokens por palabra (nivel 0)</div><div class="cel">x3,90 tokens y x4,68 tiempo al colaborar (nivel 4)</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:14px;font-size:23px;padding:20px 24px;">El límite de la última medición estaba en el <b>medidor</b>, no en el modelo: el contador marcaba rechazos honestos como «invención» (una pasada quedó invalidada en el crudo por eso). Quien mide tiene que auditar su propia medida.</div>'
 '<div class="metodo">MEDICIONES PROPIAS · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL) · 14-SEP / 27-SEP / 30-SEP-2026 · CRUDO EN LA CARPETA DE CADA PIEZA</div>'
 ))

# --- S7 cierre
S.append(slide(
 top("CIERRE · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>POR DÓNDE <span class="ac">EMPEZAR</span></h1>'
 '<div class="cierre-lista" style="margin-top:16px;gap:16px;">'
 '<div style="font-size:35px;"><span>1.</span> ¿Aún no sabes qué es un LLM? Empieza por el nivel 0.</div>'
 '<div style="font-size:35px;"><span>2.</span> ¿Ya lo usas y quieres que haga cosas? Niveles 1 y 2: instrucciones y herramientas.</div>'
 '<div style="font-size:35px;"><span>3.</span> ¿Quieres que trabaje solo y sin sustos? Niveles 3, 4 y 5: el bucle, varios agentes y la medición.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-llave-crema.png", "max-height:200px")}</div>'
 '<div class="next" style="padding:22px 26px;font-size:29px;">FIN DE LA SERIE · <span>8 PIEZAS + ESTE MAPA</span><br>Nueve entregas, de cero a producción. Si una te sirvió, dime cuál.</div>'
 ))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — El mapa de la serie (cierre)</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-cierre.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
