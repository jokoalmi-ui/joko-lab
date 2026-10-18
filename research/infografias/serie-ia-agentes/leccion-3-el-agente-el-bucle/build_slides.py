#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 3 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 2.
OJO: la slide 6 lleva el dato medible; si la medicion no se ha ejecutado, va con
[PENDIENTE DE MEDIR] y NO se publica."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-3-el-agente-el-bucle"
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
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 3</span>", "1/7") +
 '<h1>EL AGENTE:<br>EL <span class="ac">BUCLE</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Un objetivo y las llaves: no le dictas los pasos</div>'
 f'<div class="arte">{img("s1-noria.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 3 · PIEZA 6</span></div>',
 "1/7"))

# --- S2 que es
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>UN OBJETIVO, <span class="ac">NO UNA LISTA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-caja-herramientas.png", "max-height:250px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">1 · El bucle</span>'
 '<p style="font-size:26px;">Pensar, actuar y mirar el resultado. Y otra vez, hasta cerrar la tarea.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">2 · Las herramientas</span>'
 '<p style="font-size:26px;">Lo que puede hacer de verdad: buscar, sumar, escribir, enviar.</p></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">3 · La memoria</span>'
 '<p style="font-size:26px;">Lo de antes sigue encima de la mesa mientras trabaja.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">4 · Un objetivo</span>'
 '<p style="font-size:26px;">Lo que quieres conseguir. No cómo conseguirlo, paso a paso.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">La diferencia con un chatbot no es el modelo: es el bucle. El mismo modelo, en bucle y con herramientas, deja de ser una máquina de respuestas y pasa a <b>intentar</b> la tarea hasta terminarla... o hasta que se le agoten los pasos.</div>',
 "2/7"))

# --- S3 como funciona
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>CUATRO PASOS, <span class="ac">EN BUCLE</span></h1>'
 '<div class="pasos" style="margin-top:22px;">'
 '<div class="paso"><div class="num">1</div><div><b>PENSAR</b> — el modelo dice qué necesita. Muchas veces, llamar a una herramienta.</div></div>'
 '<div class="paso"><div class="num">2</div><div><b>ACTUAR</b> — tu código la ejecuta de verdad: la búsqueda, la suma, el envío.</div></div>'
 '<div class="paso"><div class="num">3</div><div><b>OBSERVAR</b> — el resultado vuelve al modelo como texto: el dato real.</div></div>'
 '<div class="paso"><div class="num">4</div><div><b>REPETIR</b> — con el dato nuevo vuelve al paso 1. Si ya tiene la respuesta, cierra.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:27px;">Quién decide cuándo parar es el bucle: un máximo de pasos o el modelo diciendo que ha terminado. Y en cada vuelta lleva encima lo de antes: memoria a corto plazo es <b>la conversación de la tarea</b>; a largo plazo es lo que se guarda fuera (un fichero, una base de datos) y se vuelve a leer.</div>',
 "3/7"))

# --- S4 confusion tipica
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1 style="margin-top:20px;font-size:80px;">BUCLE SÍ, <span class="ac">BUCLE NO</span></h1>'
 '<div class="tabla" style="margin-top:12px;gap:8px;">'
 '<div class="fila3"><div class="cel k">NOMBRE</div><div class="cel k">QUÉ ES</div></div>'
 '<div class="fila3"><div class="cel">CoT (cadena de pensamiento)</div><div class="cel" style="text-align:left;">La <b>vuelta única</b>: pensar antes de responder, sin tocar nada de fuera.</div></div>'
 '<div class="fila3"><div class="cel">ReAct</div><div class="cel" style="text-align:left;">El <b>bucle</b>: pensar, actuar sobre el entorno y mirar el resultado.</div></div>'
 '<div class="fila3"><div class="cel">Agente vs chatbot</div><div class="cel" style="text-align:left;">El chatbot <b>contesta</b>; el agente <b>intenta terminar una tarea</b> (y puede fallar).</div></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:10px;">'
 '<div class="col mal" style="padding:14px 20px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:26px;">«Más autonomía = mejor modelo.» Y «si el agente piensa más vueltas, acierta más».</p></div>'
 '<div class="col bien" style="padding:14px 20px;"><span class="tag">✓ Lo correcto</span><p style="font-size:26px;">La autonomía se la da el <b>acceso</b>, no el modelo. Sin entorno no hay datos nuevos: por muchas vueltas que dé, no aparece el número que no tiene.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:8px;font-size:27px;">La prueba rápida: si para terminar hay que mirar algo de fuera (un fichero, una web, un cálculo exacto), necesitas <b>bucle con herramientas</b>. Si solo hay que redactar mejor, basta una vuelta.</div>',
 "4/7"))

# --- S5 ejemplo real  (medicion del 24-sep-2026, medicion-bucle-20260924.json)
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>UNA VUELTA <span class="ac">NO BASTA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-etiquetas-precio.png", "max-height:230px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:14px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Sin bucle</span><p style="font-size:26px;">Le pides el importe del pedido más caro <b>sin darle la tabla</b>: contesta <b>0</b> las seis veces, con el mismo tono seguro que si acertara. Ni una vez dice «no lo sé».</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ En bucle</span><p style="font-size:26px;">Pide la tabla, la recibe, la compara y contesta. Y cuando no tiene con qué —sin herramientas— dice <b>«desconocido»</b>: cinco veces de seis. El dato no sale de su memoria: sale de <b>fuera</b>.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">El bucle no lo hace más listo: le da <b>los datos que le faltan</b>. Con herramientas cierra 5 de 6 tareas; sin ellas, 0 — y encima gasta <b>4,5 veces más tokens</b> pensando vueltas que no llevan a ningún dato.</div>',
 "5/7"))

# --- S6 dato medible: medicion real ejecutada el 24-sep-2026 (medicion-bucle.py)
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>5 DE 6 TAREAS <span class="ac">CERRADAS</span></h1>'
 '<div class="dato" style="margin-top:26px;">5<span class="ac">/6</span></div>'
 '<div class="sub">Mismo modelo, las mismas 6 tareas de varios pasos, temperatura 0. <b>Una vuelta sin herramientas</b>: 0/6, y las seis veces un número inventado (cinco de ellos, un cero). <b>Bucle sin herramientas</b>: 0/6 y 4,5 veces más tokens. <b>Bucle con herramientas</b>: 5/6 cerradas, 3 pasos y 2 herramientas por tarea, 6.660 tokens por tarea resuelta. <b>Control a 0,8</b>: 5/6 igual.</div>'
 '<div class="caja" style="margin-top:20px;font-size:27px;">La que se escapa es la tarea que pide <b>dos cosas</b>: devuelve el nombre y no el importe. El bucle no falla el cálculo: falla al cerrar cuando hay más de un dato que dar.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL), NUM_CTX 8192, SEED 42 · 6 TAREAS × 4 CONDICIONES, UNA PASADA · 24-SEP-2026</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 3 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:30px;">'
 '<div><span>1.</span> Un agente es un modelo con un bucle: pensar, actuar, observar... y otra vez.</div>'
 '<div><span>2.</span> El bucle sin entorno no trae datos: la autonomía la da el acceso.</div>'
 '<div><span>3.</span> CoT piensa y responde; ReAct piensa y actúa. Cambia si toca el mundo.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-llave-etiqueta.png", "max-height:280px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 4</span><br>De uno a muchos: agentes que colaboran.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 3</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-3.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
