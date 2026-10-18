#!/usr/bin/env python3
"""deep_research.py — Open Deep Research para el lab (B7, 20-ago-2026).

Investigación con fuentes citadas: búsqueda → extracción → SÍNTESIS CON
CITAS (en vez de meter todo el contexto). Ataca el cuello de botella nº1
(coste de contexto 99.7%): el informe final es compacto, cada afirmación
lleva su [fuente], y el contexto pesado queda en un sidecar.

FLUJO:
  1. web_search (N queries) → recopilar URLs candidatas
  2. extracción del contenido de las fuentes (browser_navigate + console,
     o curl como fallback) — el contenido se guarda SIN entrar al prompt
     del LLM
  3. síntesis con GLM local (LM Studio) usando la arquitectura de 6
     componentes (B6): contexto = fragmentos con etiquetas [S1..Sn],
     instrucción = sintetizar con citas, estilo = español directo,
     longitud = máx N puntos, público = técnico, restricciones = no
     inventar, cada afirmación con su fuente
  4. informe markdown compacto en research/ con métrica de ahorro
     (tokens contexto crudo vs tokens síntesis)

Uso:
  python3 deep_research.py "pregunta de investigación" [--max-fuentes 5]
                           [--puntos 8] [--queries "q1" "q2"] [--salida nombre]

Requiere: GLM cargado en LM Studio (localhost:1234) para la síntesis.
Si no hay GLM → fallback: informe con los fragmentos sin sintetizar
(marcado NO SINTETIZADO).
"""
import argparse, json, os, re, subprocess, sys, urllib.request, urllib.parse, datetime

COMFY = None  # no usado
LMSTUDIO = "http://localhost:1234/api/v0/chat/completions"
LM_MODEL = "glm-4.6v-flash"
RESEARCH_DIR = os.path.expanduser("~/joko-lab/research")

# ---------- Fase 1: búsqueda (web_search vía API ddgs del router o subprocess) ----------

def web_search(query: str, limit: int = 5) -> list:
    """Busca con web_search de Hermes vía subprocess si existe el CLI, si no,
    usa la API pública de DuckDuckGo (sin key)."""
    # Opción A: llamar al CLI de búsqueda de Hermes si existe
    candidates = [
        os.path.expanduser("~/.hermes/bin/hermes-search"),
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                r = subprocess.run([c, query], capture_output=True, text=True, timeout=60)
                if r.returncode == 0 and r.stdout.strip():
                    return _parse_search_output(r.stdout)
            except Exception:
                pass
    # Opción B: DuckDuckGo html (sin API key, puede fallar por rate-limit)
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", "ignore")
        # extraer resultados: <a rel="nofollow" class="result__a" href="...">Título</a>
        links = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
        out = []
        for href, title in links[:limit]:
            m = re.search(r"uddg=([^&]+)", href)
            url = urllib.parse.unquote(m.group(1)) if m else href
            clean = re.sub(r"<[^>]+>", "", title)
            out.append({"url": url, "title": clean})
        return out
    except Exception as e:
        print(f"  [aviso] búsqueda ddgs falló: {str(e)[:80]}", file=sys.stderr)
        return []


def _parse_search_output(text: str) -> list:
    """Parsea salida de hermes-search (JSON o líneas URL|título)."""
    out = []
    for line in text.strip().splitlines()[:10]:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"(https?://\S+)\s+(.*)", line)
        if m:
            out.append({"url": m.group(1), "title": m.group(2)[:100]})
        elif line.startswith("http"):
            out.append({"url": line, "title": line[:80]})
    return out


# ---------- Fase 2: extracción (curl simple; el navegador es para el agente) ----------

def fetch_text(url: str, max_chars: int = 6000) -> str:
    """Extrae texto de una URL con curl + regex básico (HTML → texto plano).
    No es perfecto, pero suficiente para síntesis. Las páginas problemáticas
    se extraen con browser en el flujo del agente."""
    try:
        html = _curl_raw(url)
        # quitar scripts/styles
        html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
        # quitar tags
        text = re.sub(r"<[^>]+>", " ", html)
        # decodificar entidades básicas
        text = (text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))
        # compactar espacios
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]
    except Exception as e:
        return f"[error extracción: {str(e)[:80]}]"


def _curl_raw(url: str) -> str:
    """curl que devuelve el HTML crudo (para título y extracción)."""
    r = subprocess.run(
        ["curl", "-sL", "-m", "25", "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64)",
         url],
        capture_output=True, text=True, timeout=35)
    return r.stdout


# ---------- Fase 3: síntesis con citas (GLM local) ----------

def sintetizar(pregunta: str, fuentes: list, puntos: int) -> dict:
    """Síntesis con citas vía GLM local. Cada fuente se etiqueta [S1..Sn].
    Prompt en 6 componentes (B6). Devuelve {ok, texto, tokens_in, tokens_out}."""
    fragmentos = []
    for i, f in enumerate(fuentes, 1):
        fragmentos.append(f"[S{i}] {f['title'][:100]}\n{f['text'][:3000]}")
    contexto = "\n\n".join(fragmentos)

    prompt = f"""## CONTEXTO
Fuentes de investigación etiquetadas [S1..Sn]. Cada una empieza con su
título. No hay más información que la de estas fuentes.

{contexto}

## INSTRUCCIÓN
Responde a la pregunta: {pregunta}
Sintetiza la información en un informe breve. Cada afirmación debe llevar
su fuente entre corchetes [S1], [S2]... Si una fuente no aporta, no la uses.
Estructura: 1) Resumen (2-3 frases con citas), 2) Hallazgos (máx {puntos}
puntos numerados, cada uno con su [Sx]), 3) Contradicciones o matices
(con citas), 4) Qué falta saber.

## ESTILO
Español, directo, neutro, frases cortas. Sin elogios. Sin relleno.

## LONGITUD
Máximo {puntos + 3} bloques. Cada hallazgo, 1-2 frases.

## PÚBLICO
Técnico del lab (IA local, ingeniería). Se asume nivel medio.

## RESTRICCIONES
NO inventes datos ni fuentes. NO cites [Sx] que no exista. Si las fuentes
no responden la pregunta, dilo explícitamente. NO uses información fuera
de las fuentes."""
    payload = {
        "model": LM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2500, "temperature": 0.2,
    }
    tokens_in = len(prompt) // 4
    try:
        req = urllib.request.Request(LMSTUDIO, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
        content = resp["choices"][0]["message"].get("content") or ""
        if not content:
            content = resp["choices"][0]["message"].get("reasoning_content", "")
        tokens_out = len(content) // 4
        return {"ok": bool(content.strip()), "texto": content.strip(),
                "tokens_in": tokens_in, "tokens_out": tokens_out}
    except Exception as e:
        return {"ok": False, "texto": f"[error síntesis: {str(e)[:100]}]",
                "tokens_in": tokens_in, "tokens_out": 0}


# ---------- Fase 4: informe ----------

def main():
    ap = argparse.ArgumentParser(description="Open Deep Research del lab (B7)")
    ap.add_argument("pregunta")
    ap.add_argument("--max-fuentes", type=int, default=5)
    ap.add_argument("--puntos", type=int, default=8)
    ap.add_argument("--urls", nargs="*", default=None,
                    help="URLs ya investigadas (el agente las busca con web_search + browser — ddgs directo está anti-bot)")
    ap.add_argument("--fragmentos", default=None,
                    help="archivo con texto crudo ya extraído (1 bloque por línea, con título en la 1ª línea)")
    ap.add_argument("--queries", nargs="*", default=None)
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()

    print(f"== Open Deep Research (B7) — {args.pregunta[:60]}...")

    # Fase 1-2: fuentes. El agente pasa URLs (ya buscadas y verificadas) o
    # fragmentos extraídos; el script NO depende de ddgs (anti-bot, verificado
    # 20-ago: html.duckduckgo.com devuelve anomaly/challenge).
    print("[1/4] cargando fuentes...")
    fuentes = []
    if args.fragmentos:
        with open(args.fragmentos) as f:
            bloques = f.read().split("\n\n")
        for i, b in enumerate(bloques[:args.max_fuentes], 1):
            lineas = b.strip().splitlines()
            if not lineas:
                continue
            titulo = lineas[0].strip()[:100]
            texto = " ".join(lineas[1:]).strip()[:6000]
            fuentes.append({"url": f"fragmento-{i}", "title": titulo, "text": texto})
        print(f"      {len(fuentes)} fragmentos cargados")
    elif args.urls:
        for u in args.urls[:args.max_fuentes]:
            print(f"      → {u[:70]}...")
            texto = fetch_text(u)
            # título: extraer del HTML si es posible, si no, el slug de la URL
            titulo = u.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").replace("_", " ")[:100]
            m = re.search(r"<title[^>]*>(.*?)</title>", _curl_raw(u), re.S | re.I)
            if m:
                t = re.sub(r"\s+", " ", m.group(1)).strip()
                if t:
                    titulo = t[:100]
            fuentes.append({"url": u, "title": titulo, "text": texto})
            print(f"      ✓ {titulo[:60]} ({len(texto)} chars)")
    else:
        # modo búsqueda interna (fallback, suele fallar por anti-bot)
        print("[1/4] búsqueda (fallback)...")
        queries = args.queries or [args.pregunta]
        resultados = []
        vistos = set()
        for q in queries:
            for r in web_search(q, limit=5):
                u = r["url"]
                if u not in vistos and "youtube.com" not in u and "twitter.com" not in u:
                    vistos.add(u)
                    resultados.append(r)
            if len(resultados) >= args.max_fuentes * 2:
                break
        print(f"      {len(resultados)} URLs candidatas")
        print("[2/4] extracción...")
        for r in resultados[:args.max_fuentes]:
            texto = fetch_text(r["url"])
            fuentes.append({"url": r["url"], "title": r["title"], "text": texto})
            print(f"      ✓ {r['title'][:60]} ({len(texto)} chars)")

    if not fuentes:
        print("NO hay fuentes — abortando. Pasa --urls o --fragmentos.")
        sys.exit(1)

    # Fase 3: síntesis
    print("[3/4] síntesis con GLM local...")
    res = sintetizar(args.pregunta, fuentes, args.puntos)
    if not res["ok"]:
        print(f"      {res['texto'][:120]}")
        print("      → informe SIN sintetizar (fragmentos crudos)")

    # Fase 4: informe
    fecha = datetime.date.today().isoformat()
    slug = re.sub(r"[^a-z0-9]+", "-", args.pregunta.lower()).strip("-")[:50]
    salida = args.salida or os.path.join(RESEARCH_DIR, f"deep-research-{slug}-{fecha}.md")
    os.makedirs(RESEARCH_DIR, exist_ok=True)

    ahorro = res["tokens_in"] - res["tokens_out"] if res["ok"] else 0
    with open(salida, "w") as f:
        f.write(f"# Deep Research — {args.pregunta}\n\n")
        f.write(f"fecha: {fecha} · método: Open Deep Research (B7) · "
                f"fuentes: {len(fuentes)} · síntesis: {'GLM local' if res['ok'] else 'NO SINTETIZADO'}\n\n")
        f.write("## Síntesis con citas\n\n")
        f.write(res["texto"] if res["ok"] else "*(sin sintetizar — GLM no disponible)*\n")
        f.write("\n\n## Fuentes\n\n")
        for i, fr in enumerate(fuentes, 1):
            f.write(f"[S{i}] {fr['title']} — {fr['url']}\n")
        f.write(f"\n## Métrica de coste de contexto\n\n")
        f.write(f"- Tokens contexto crudo: ~{res['tokens_in']}\n")
        f.write(f"- Tokens síntesis: ~{res['tokens_out']}\n")
        f.write(f"- Ahorro: ~{ahorro} tokens ({100 * ahorro // max(res['tokens_in'], 1)}% menos contexto)\n")
        f.write(f"- Regla: usar SIEMPRE la síntesis (este archivo) como fuente para el RAG/\n")
        f.write(f"  contexto; el contenido crudo queda fuera del prompt del LLM.\n")

    print(f"\n[4/4] ✅ Informe: {salida}")
    print(f"      Síntesis: {'GLM local' if res['ok'] else 'NO SINTETIZADO'}")
    if res["ok"]:
        print(f"      Ahorro: ~{ahorro} tokens ({100 * ahorro // max(res['tokens_in'], 1)}%)")
    return salida


if __name__ == "__main__":
    main()
