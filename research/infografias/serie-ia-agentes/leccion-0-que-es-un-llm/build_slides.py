#!/usr/bin/env python3
"""build_slides.py — construye el carrusel HTML de la Leccion 0 (estilo MAURYS, 1080x1350).
Serie divulgativa IA/agentes (Joko Lab). Fuentes Poppins/Inter embebidas en base64."""
import base64, pathlib

BASE = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes")
LEC = BASE / "leccion-0-que-es-un-llm"
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
 .tokens {{ display:flex; align-items:center; justify-content:center; gap:12px; margin-top:44px; }}
 .tk {{ background:#fff; border:3px solid #111; border-radius:14px; padding:22px 26px; font-size:36px; font-weight:700; }}
 .tk.ac {{ background:{NARANJA}; border-color:{NARANJA}; color:#fff; }}
 .tk.hueco {{ border-style:dashed; color:#b9b2a6; }}
 .fl {{ font-size:34px; font-weight:800; }}
 .nota-diag {{ margin-top:34px; font-size:33px; line-height:1.3; text-align:center; }}
 .pie {{ margin-top:22px; border-top:4px solid {NEGRO}; padding-top:18px; font-family:'Inter';
   font-size:24px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; display:flex; justify-content:space-between; }}
 .pie .ac {{ color:{NARANJA}; }}
 """
)

def img(nombre, estilo=""):
    return f'<img src="file://{ART}/{nombre}" style="{estilo}" alt="">' 

def slide(inner, pager, extra=""):
    return f'<section class="slide {extra}">\n{inner}\n</section>'

def top(kicker, pager, naranja=""):
    k = kicker.replace("§", f'<span class="n">{naranja}</span>') if naranja else kicker
    return f'<div class="top"><div class="kicker">{k}</div><div class="pager">{pager}</div></div>'

S = []

# --- S1 portada
S.append(slide(
 top("CURSO DE IA Y AGENTES · <span class='n'>LECCIÓN 0</span>", "1/7") +
 '<h1>QUÉ ES UN <span class="ac">LLM</span></h1>'
 '<div class="sub" style="font-size:38px;margin-top:16px;">La máquina que no busca: <b>genera</b></div>'
 f'<div class="arte">{img("s1_portada.png")}</div>'
 '<div class="pie"><span>6 LECCIONES · DE LO BÁSICO A LO AVANZADO</span><span class="ac">LECCIÓN 0</span></div>',
 "1/7"))

# --- S2 que es
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>1/5 QUÉ ES</span>", "2/7") +
 '<h1>UN MODELO DE <span class="ac">LENGUAJE</span></h1>'
 f'<div class="arte">{img("s2_que_es.png")}</div>'
 '<div class="cuerpo">Ha leído muchísimo texto y ha aprendido un patrón: <b>qué palabra suele venir después de cada palabra</b>.</div>'
 '<div class="caja">No guarda frases. Guarda la estadística del idioma.</div>',
 "2/7"))

# --- S3 como funciona
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>2/5 CÓMO FUNCIONA</span>", "3/7") +
 '<h1>ESCRIBE <span class="ac">TOKEN</span> A TOKEN</h1>'
 '<div class="pasos" style="margin-top:36px;">'
 '<div class="paso"><div class="num">1</div><div>Tu texto se parte en trozos: <b>tokens</b>.</div></div>'
 '<div class="paso"><div class="num">2</div><div>Calcula qué token es <b>más probable</b> que venga después.</div></div>'
 '<div class="paso"><div class="num">3</div><div>Elige uno y lo <b>añade</b> al final.</div></div>'
 '<div class="paso"><div class="num">4</div><div>Repite mirando <b>todo lo anterior</b>. Por eso escribe en cadena.</div></div>'
 '</div>'

 '<div class="tokens">'
 '<div class="tk">El</div><div class="fl">&rarr;</div><div class="tk">gato</div><div class="fl">&rarr;</div>'
 '<div class="tk">duerme</div><div class="fl">&rarr;</div><div class="tk ac">en</div><div class="fl">&rarr;</div>'
 '<div class="tk hueco">?</div>'
 '</div>'
 '<div class="nota-diag">El modelo elige el siguiente token mirando <b>todos los anteriores</b>. Repite, y ya tienes una frase.</div>',
 "3/7"))

# --- S4 confusion
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>3/5 LA CONFUSIÓN TÍPICA</span>", "4/7") +
 '<h1>NO BUSCA: <span class="ac">GENERA</span></h1>'
 '<div class="arte" style="padding:6px 0;">'
 '<svg width="640" height="330" viewBox="0 0 640 330" xmlns="http://www.w3.org/2000/svg">'
 '<circle cx="200" cy="150" r="88" fill="none" stroke="#111111" stroke-width="12"/>'
 '<line x1="263" y1="213" x2="345" y2="295" stroke="#111111" stroke-width="22" stroke-linecap="round"/>'
 '<line x1="140" y1="90" x2="262" y2="212" stroke="#FF7A00" stroke-width="16" stroke-linecap="round"/>'
 '<text x="352" y="104" font-family="Inter,sans-serif" font-size="32" font-weight="800" fill="#111111">BUSCAR</text>'
 '<g transform="translate(505,150)">'
 '<circle r="60" fill="none" stroke="#111111" stroke-width="12"/>'
 '<circle r="24" fill="#FF7A00"/>'
 '<g stroke="#111111" stroke-width="12" stroke-linecap="round">'
 '<line x1="0" y1="-72" x2="0" y2="-88"/><line x1="0" y1="72" x2="0" y2="88"/>'
 '<line x1="-72" y1="0" x2="-88" y2="0"/><line x1="72" y1="0" x2="88" y2="0"/>'
 '</g></g>'
 '<path d="M400 150 L428 150 M420 138 L432 150 L420 162" stroke="#FF7A00" stroke-width="10" fill="none" stroke-linecap="round"/>'
 '<text x="470" y="300" font-family="Inter,sans-serif" font-size="32" font-weight="800" fill="#111111">GENERAR</text>'
 '</svg></div>'
 '<div class="dos" style="flex:0 0 auto;">'
 '<div class="col mal"><span class="tag">✗ Se cree que</span><p>Consulta internet o una base de datos y te lee el dato.</p></div>'
 '<div class="col bien"><span class="tag">✓ Lo que hace</span><p>Calcula la respuesta que más probablemente encaja.</p></div>'
 '</div>'
 '<div class="caja" style="margin-top:22px;">Si no lo sabe, no se queda en blanco: <b>inventa algo plausible</b>. Eso es una alucinación.</div>',
 "4/7"))

# --- S5 ejemplo real
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>4/5 EJEMPLO REAL</span>", "5/7") +
 '<h1>MISMO MODELO, <span class="ac">DOS</span> RESULTADOS</h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:14px 0;">{img("s5_ejemplo.png")}</div>'
 '<div class="dos">'
 '<div class="col mal"><span class="tag">Sin tus datos</span><p>Le preguntas por un informe interno que nunca ha visto: <b>te da un nombre inventado, con total seguridad</b>.</p></div>'
 '<div class="col bien"><span class="tag">Con tus documentos</span><p>Conectas tus archivos (RAG, <b>lección 2</b>): responde y <b>cita de dónde lo saca</b>.</p></div>'
 '</div>',
 "5/7"))

# --- S6 dato medible
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>5/5 DATO MEDIBLE</span>", "6/7") +
 '<h1>SE MIDE EN <span class="ac">TOKENS</span></h1>'
 f'<div class="arte" style="flex:0 0 auto;padding:2px 0 0;">{img("s6_dato.png", "max-height:240px")}</div>'
 '<div class="dato" style="font-size:82px;">1 palabra ≈ <span class="ac">1,4</span> tokens</div>'
 '<div class="sub" style="font-size:26px;margin-top:6px;">En español. Medido: 141 palabras → 195 tokens · 51 palabras → 69 tokens.</div>'
 '<div class="caja" style="margin-top:16px;font-size:31px;">La <b>ventana de contexto</b> es cuántos tokens puede tener delante a la vez: '
 '131.072 (~128.000). Si se llena, empieza a olvidar lo del principio.</div>'
 '<div class="metodo">Medición propia · Ollama en local · modelo ibm/granite4.2:8b · 14-sep-2026 · descontando 15 tokens de plantilla interna</div>',
 "6/7"))

# --- S7 cierre
S.append(slide(
 top("LECCIÓN 0 · <span class='n'>CIERRE</span>", "7/7") +
 '<h1>EN <span class="ac">1 MINUTO</span></h1>'
 '<div class="cierre-lista" style="margin-top:40px;">'
 '<div><span>1.</span> Genera, no consulta.</div>'
 '<div><span>2.</span> Escribe token a token, no de golpe.</div>'
 '<div><span>3.</span> Se equivoca con seguridad: verifica.</div>'
 '</div>'
 f'<div class="arte" style="flex:0 0 auto;">{img("s7_cierre.png")}</div>'
 '<div class="next">SIGUIENTE · <span>LECCIÓN 1</span><br>Aprender a pedirle las cosas: instrucciones, formato y ejemplos.</div>',
 "7/7"))

html = ("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><title>Curso IA y agentes — Lección 0</title>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(S) + "\n</body></html>")
out = LEC / "carrusel-leccion-0.html"
out.write_text(html, encoding="utf-8")
print("HTML:", out, len(html), "bytes,", html.count('class="slide'), "slides")
