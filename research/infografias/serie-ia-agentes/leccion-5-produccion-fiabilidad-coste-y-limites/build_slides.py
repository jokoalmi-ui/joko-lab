#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 5 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 4 (misma familia visual: crema #F5EFE6,
tinta #111111, acento naranja #FF7A00).
OJO: la slide 6 lleva el dato medible; los numeros salen de
medicion-alucinaciones-20260914.json (medicion propia del 14-sep-2026, 27 casos
x 3 pasadas con el razonamiento DESACTIVADO; el limite del medidor va en la caja).
La pieza es la ULTIMA del plan de niveles: el cierre no anuncia nivel siguiente."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-5-produccion-fiabilidad-coste-y-limites"
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
 face("Inter",400,"Inter-400.woff2") + face("Inter",600,"Inter-600.woff2") +
 face("Inter",700,"Inter-700.woff2") + face("Inter",800,"Inter-800.woff2") +
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
 .cel {{ flex:1; background:#fff; border:2px solid #1a1a1a; border-radius:14px; padding:12px 18px;
   font-size:23px; font-weight:600; text-align:center; }}
 .cel.k {{ background:{NEGRO}; color:{CREMA}; font-family:'Inter'; font-weight:800; }}
 .cel.ok {{ border-color:#2a9d5f; color:#1f7a48; }}
 .cel.ko {{ border-color:#b8483a; color:#a13c30; }}
 .th {{ font-family:'Inter'; font-size:22px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:#3a3a3a; text-align:center; }}
""")

def img(nombre, estilo=""):
    return f'<img src="file://{ART}/{nombre}" style="{estilo}" alt="">'

def slide(inner, pager, extra=""):
    return f'<section class="slide {extra}">\n{inner}\n</section>'

def top(kicker, pager):
    return f'<div class="top"><div class="kicker">{kicker}</div><div class="pager">{pager}</div></div>'

S = []

# --- S1 portada
S.append(slide(
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 5</span>", "1/7") +
 '<h1>A <span class="ac">PRODUCCIÓN</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Fiabilidad, coste y límites: la demo no es la prueba</div>'
 f'<div class="arte">{img("s1-balanza-crema.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 5 · PIEZA 8</span></div>',
 "1/7"))

# --- S2 que es
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>MEDIR, VERIFICAR, <span class="ac">LIMITAR</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-fichero-pruebas-crema.png", "max-height:250px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">1 · La medida</span>'
 '<p style="font-size:26px;">Un juego fijo de casos con respuesta conocida. Sin eso, «funciona» es una impresión, no un dato.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">2 · La comprobación</span>'
 '<p style="font-size:26px;">Que la salida se verifique sola: una cita, un JSON que valida, un número que se recalcula.</p></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">3 · Los permisos</span>'
 '<p style="font-size:26px;">Que pueda hacer solo lo que la tarea necesita. Un borrado no se deshace: se confirma antes.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">4 · El techo de gasto</span>'
 '<p style="font-size:26px;">Presupuesto por tarea y corte automático. El coste no sube de golpe: sube en silencio.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">Un agente fiable no es el que nunca falla: es el que falla <b>donde tú lo puedes ver</b>, y a un precio que aceptaste antes de encenderlo.</div>',
 "2/7"))

# --- S3 como funciona
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1 style="font-size:72px;margin-top:20px;">CINCO PIEZAS, <span class="ac">UN SISTEMA</span></h1>'
 '<div class="pasos" style="margin-top:12px;gap:9px;">'
 '<div class="paso" style="padding:13px 22px;font-size:29px;"><div class="num">1</div><div><b>CASOS DE PRUEBA</b> — batería fija con respuesta conocida, trampas incluidas, repetida en cada cambio.</div></div>'
 '<div class="paso" style="padding:13px 22px;font-size:29px;"><div class="num">2</div><div><b>SALIDA VERIFICABLE</b> — formato exigido, cita obligatoria, número recomputable. Lo que no se comprueba, no se sabe.</div></div>'
 '<div class="paso" style="padding:13px 22px;font-size:29px;"><div class="num">3</div><div><b>PERMISOS MÍNIMOS</b> — solo las herramientas que la tarea pide; las que escriben, con confirmación.</div></div>'
 '<div class="paso" style="padding:13px 22px;font-size:29px;"><div class="num">4</div><div><b>TRAZA</b> — cada paso con su entrada, su salida y su coste. Sin traza, un fallo es un misterio.</div></div>'
 '<div class="paso" style="padding:13px 22px;font-size:29px;"><div class="num">5</div><div><b>TECHO DE GASTO</b> — límite por tarea y por día; al llegar, para en vez de seguir.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:12px;font-size:25px;padding:20px 26px;">Ninguna de las cinco piezas es «inteligencia»: son <b>controles</b>. La calidad de un agente en producción la fija el control más flojo, no el modelo más caro.</div>',
 "3/7"))

# --- S4 confusion tipica
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1 style="margin-top:8px;font-size:66px;">SI FUNCIONA EN LA DEMO, <span class="ac">FUNCIONA</span></h1>'
 '<div class="tabla" style="margin-top:14px;gap:8px;">'
 '<div class="fila3"><div class="cel k">SE DICE</div><div class="cel k">QUÉ PASA</div></div>'
 '<div class="fila3"><div class="cel">«Ya me contesta bien»</div><div class="cel" style="text-align:left;">Tres pruebas no son una muestra. Hacen falta casos con respuesta conocida, contados y repetibles.</div></div>'
 '<div class="fila3"><div class="cel">«Alucinar es de modelos malos»</div><div class="cel" style="text-align:left;">Inventar es estadístico, no una tara de marca: se mide una <b>tasa</b> y se decide cuál es tolerable.</div></div>'
 '<div class="fila3"><div class="cel">«El gasto lo corto a mano»</div><div class="cel" style="text-align:left;">Sin techo por tarea, el coste lo decide el bucle. Y lo descubres en la factura, no antes.</div></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:10px;">'
 '<div class="col mal" style="padding:12px 18px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:23px;">«Si aprueba la demo, ya está listo.» Y «con un modelo mejor el problema desaparece».</p></div>'
 '<div class="col bien" style="padding:12px 18px;"><span class="tag">✓ Lo correcto</span><p style="font-size:23px;">El listón no es la demo: es la <b>batería repetida</b> + el coste aceptado + los permisos mínimos. El modelo, solo, no arregla eso.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:8px;font-size:24px;">La pregunta útil no es «¿falla?» — falla siempre. Es: <b>¿cuánto falla, de qué forma y cuánto cuesta cada fallo?</b></div>',
 "4/7"))

# --- S5 ejemplo real (bateria de casos trampa)
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>LA PREGUNTA QUE <span class="ac">NO TIENE RESPUESTA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-iman-trampa-crema.png", "max-height:230px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:14px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ El caso normal</span><p style="font-size:26px;">Se pregunta por algo que <b>existe</b> y hay que acertar el dato. Aquí el modelo acierta casi siempre: no separa.</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ El caso trampa</span><p style="font-size:26px;">Se pregunta por algo que <b>no existe</b> («¿cuándo presentó X el modelo Y?»). Lo correcto es decir que no se sabe; el fallo, rellenar el hueco con algo verosímil.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">Un caso trampa no mide cultura general: mide si el sistema <b>sabe callarse</b>. Y las trampas se eligen una a una — no las inventa el modelo que vas a examinar.</div>',
 "5/7"))

# --- S6 dato medible (medicion propia del 14-sep-2026, medicion-alucinaciones-20260914.json)
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>0 VECES SE LO <span class="ac">INVENTÓ</span></h1>'
 '<div class="dato" style="margin-top:26px;">0<span class="ac">/27</span></div>'
 '<div class="sub">veces que el modelo se inventó un dato, en <b>3 pasadas</b> de la misma batería de 27 casos: 16 aciertos y 11 abstenciones correctas en cada pasada. Cero invenciones, tres veces seguidas.</div>'
 '<div class="caja" style="margin-top:20px;font-size:25px;">El límite está en el <b>medidor</b>, no solo en el modelo: al leer las respuestas una a una, el contador automático había marcado como «invención» rechazos honestos («aún no ha habido ningún astronauta que haya pisado Marte» contaba como alucinación). La tasa con el razonamiento largo activado (3,7 %–14,8 %) es del contador, no del modelo — una de esas pasadas quedó invalidada en el registro con ese motivo. Quien mide tiene que auditar su propia medida.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL) · NUM_CTX 8192 · TEMPERATURA 0,2 · RAZONAMIENTO DESACTIVADO · 27 CASOS × 3 PASADAS (SEEDS 42/43/44) · 14-SEP-2026</div>',
 "6/7"))

# --- S7 cierre (ultima pieza del plan de niveles)
S.append(slide(
 top("LECCIÓN 5 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:12px;gap:14px;">'
 '<div style="font-size:38px;"><span>1.</span> Fiable no es «no falla»: es saber cuánto falla, con qué casos y a qué precio.</div>'
 '<div style="font-size:38px;"><span>2.</span> Mide antes y después de cada cambio: lo que no se repite no es una medida, es una anécdota.</div>'
 '<div style="font-size:38px;"><span>3.</span> Desconfía de tu propio medidor: el error de esta lección estaba en mi contador, no en el modelo.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-candado-limite-crema.png", "max-height:215px")}</div>'
 '<div class="next" style="padding:22px 26px;font-size:29px;">FIN DEL RECORRIDO · <span>5 LECCIONES</span><br>De «qué es un LLM» a sacarlo a producción. ¿Qué te falta para tu caso?</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 5</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-5.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
