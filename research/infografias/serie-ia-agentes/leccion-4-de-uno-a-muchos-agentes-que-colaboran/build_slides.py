#!/usr/bin/env python3
"""build_slides.py — carrusel HTML de la Leccion 4 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64.
Adaptado de build_slides.py de la leccion 3 (misma familia visual: crema #F5EFE6,
tinta #111111, acento naranja #FF7A00).
OJO: la slide 6 lleva el dato medible; los numeros salen de
medicion-multiagente-20260927.json (medicion propia, 27-sep-2026)."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-4-de-uno-a-muchos-agentes-que-colaboran"
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
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 4</span>", "1/7") +
 '<h1>DE UNO A<br><span class="ac">MUCHOS</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">Agentes que colaboran: repartir el trabajo y volver a juntarlo</div>'
 f'<div class="arte">{img("s1-tres-robots-crema.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 4 · PIEZA 7</span></div>',
 "1/7"))

# --- S2 que es
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>VARIOS ROLES, <span class="ac">UN TRABAJO</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:10px 0;">{img("s2-fichas-rol-crema.png", "max-height:250px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">1 · El reparto</span>'
 '<p style="font-size:26px;">La tarea se parte en trozos con un encargo claro y un resultado que otro puede revisar.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">2 · Los mensajes</span>'
 '<p style="font-size:26px;">Entre agentes solo viaja texto: el informe, no su cabeza. Lo que no escriba, se pierde.</p></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:12px;">'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">3 · El estado</span>'
 '<p style="font-size:26px;">Lo compartido vive fuera: un fichero, una tabla. Quien llega después lo lee.</p></div>'
 '<div class="col bien" style="padding:18px 20px;"><span class="tag">4 · El mando</span>'
 '<p style="font-size:26px;">Quién decide el siguiente paso y cuándo se cierra. Sin eso no hay equipo: hay ruido.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">Un equipo de agentes no es «un modelo más listo»: son varios trabajos con las mismas limitaciones, y un sitio donde juntarlos. Lo que cambia no es la inteligencia — es el <b>reparto</b>.</div>',
 "2/7"))

# --- S3 como funciona
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>CUATRO FORMAS, <span class="ac">UNA REGLA</span></h1>'
 '<div class="pasos" style="margin-top:22px;">'
 '<div class="paso"><div class="num">1</div><div><b>EN CADENA</b> — el informe del primero es la entrada del siguiente. Lo más simple de depurar.</div></div>'
 '<div class="paso"><div class="num">2</div><div><b>EN PARALELO</b> — varios a la vez y se juntan los resultados. Se gana tiempo, se paga en coordinación.</div></div>'
 '<div class="paso"><div class="num">3</div><div><b>CON SUPERVISOR</b> — uno reparte, revisa y decide cuándo está listo. El más popular… y el que se mide en la slide 6.</div></div>'
 '<div class="paso"><div class="num">4</div><div><b>RELEVO</b> — el testigo pasa: quien atiende decide pasar el caso a otro especialista.</div></div>'
 '</div>'
 '<div class="caja" style="margin-top:18px;font-size:27px;">Tres preguntas antes de montar un equipo: <b>¿hay trozos de verdad?</b> ¿el trozo cabe en un encargo claro? <b>¿qué pasa si dos se contradicen?</b> Si la tercera no tiene respuesta, el problema no es el modelo: es el diseño.</div>',
 "3/7"))

# --- S4 confusion tipica
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1 style="margin-top:8px;font-size:70px;">EQUIPO SÍ, <span class="ac">EQUIPO NO</span></h1>'
 '<div class="tabla" style="margin-top:10px;gap:6px;">'
 '<div class="fila3"><div class="cel k">NOMBRE</div><div class="cel k">QUÉ ES</div></div>'
 '<div class="fila3"><div class="cel">Pasos fijos</div><div class="cel" style="text-align:left;">El camino lo decides tú <b>antes</b>. Barato, auditable y ciego si el caso se sale del guion.</div></div>'
 '<div class="fila3"><div class="cel">Tubería de prompts</div><div class="cel" style="text-align:left;">La salida de uno entra en el siguiente. Sin estado ni herramientas: <b>eso no es un equipo</b>.</div></div>'
 '<div class="fila3"><div class="cel">Agentes de verdad</div><div class="cel" style="text-align:left;">Cada uno decide sus pasos y usa herramientas; comparten estado y <b>alguien cierra</b>.</div></div>'
 '</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:8px;">'
 '<div class="col mal" style="padding:12px 18px;"><span class="tag">✗ Se dice mucho</span><p style="font-size:23px;">«Cuantos más agentes, mejor.» Y «un crítico siempre mejora la respuesta».</p></div>'
 '<div class="col bien" style="padding:12px 18px;"><span class="tag">✓ Lo correcto</span><p style="font-size:23px;">Cada agente añade <b>coste y formas de fallar</b>. El crítico solo vale si el trabajo se puede comprobar con datos — y se mide.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:8px;font-size:24px;">La prueba rápida: si puedes dibujar los pasos y se sostienen, no necesitas agentes — necesitas un <b>workflow</b>. Los agentes se justifican cuando el camino no se sabe de antemano.</div>',
 "4/7"))

# --- S5 ejemplo real  (medicion del 27-sep-2026, medicion-multiagente-20260927.json)
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>EL QUE ESCRIBE Y <span class="ac">EL QUE REVISA</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:6px 0;">{img("s5-lupa-revisora-crema.png", "max-height:230px")}</div>'
 '<div class="dos" style="flex:0 0 auto;margin-top:14px;">'
 '<div class="col mal" style="padding:20px 22px;"><span class="tag">✗ Lo que se esperaba</span><p style="font-size:26px;">«Una segunda mirada caza los errores.» En la tarea 6 el crítico dijo <b>incorrecto</b> sobre una respuesta correcta: el agente rehizo el trabajo y volvió a dar <b>el mismo número</b>.</p></div>'
 '<div class="col bien" style="padding:20px 22px;"><span class="tag">✓ Lo que costó</span><p style="font-size:26px;">La misma tarea: <b>6.530 tokens en 163 s</b> sin crítico → <b>35.633 tokens en 1.114 s</b> con él. Misma respuesta, <b>×5,5 de coste</b> y ×6,8 de tiempo.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:16px;font-size:27px;">El crítico acertó en 5 de 6 tareas. La única vez que dijo «incorrecto», la respuesta era buena. No hace falta que mienta para salir caro: basta con <b>equivocarse una vez</b>.</div>',
 "5/7"))

# --- S6 dato medible: medicion real ejecutada el 27-sep-2026 (medicion-multiagente.py)
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>MISMO RESULTADO, <span class="ac">×3,9 EL COSTE</span></h1>'
 '<div class="dato" style="margin-top:26px;">0<span class="ac">/6</span></div>'
 '<div class="sub">tareas rescatadas por el crítico: en las seis acertaron los dos. <b>A, un agente solo</b>: 6/6 · 22.121 tokens · 537 s · 2,3 llamadas por tarea. <b>B, el mismo agente con crítico</b> (su coste incluye el de A): 6/6 · 86.256 tokens · 2.515 s · 5 llamadas por tarea → ×3,9 tokens y ×4,7 tiempo. Reintentos disparados: 1; resultados cambiados: 0.</div>'
 '<div class="caja" style="margin-top:20px;font-size:27px;">No dice «el crítico no sirve»: dice que en este trabajo — datos que se comprueban y un modelo que ya acierta — no cambia la precisión y <b>multiplica la factura</b>. Con tareas más duras, o con un modelo que falle, la pregunta vuelve a estar abierta.</div>'
 '<div class="metodo">MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL), NUM_CTX 8192, TEMPERATURA 0 · 6 TAREAS × 2 CONDICIONES — A: UN AGENTE CON HERRAMIENTAS · B: EL MISMO AGENTE + CRÍTICO INDEPENDIENTE · 27-SEP-2026</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 4 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:30px;">'
 '<div><span>1.</span> Varios agentes no son un modelo mejor: son varios encargos que se juntan.</div>'
 '<div><span>2.</span> Elige la forma —cadena, paralelo, supervisor, relevo— por el trabajo, no por la moda.</div>'
 '<div><span>3.</span> Un crítico hay que medirlo: si no rescata errores, solo suma factura.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7-fabrica-juguete-crema.png", "max-height:280px")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 5</span><br>El paso a producción: fiabilidad, coste y límites.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 4</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-4.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
