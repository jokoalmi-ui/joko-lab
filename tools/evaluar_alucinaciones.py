#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluador de alucinaciones con golden set (Joko Lab, 24-ago-2026).

Mide 3 cosas de un modelo local:
  - ALUCINACION: inventa datos (afirma hechos fabricados o que no están en el contexto).
  - GROUNDING: con contexto, responde con el dato del contexto (o dice NO_SÉ si no está).
  - HONESTIDAD: cuando no sabe, dice NO_SÉ en vez de inventar.

Uso:
  python3 tools/evaluar_alucinaciones.py --modelo gpt-oss-20b --backend auto
  python3 tools/evaluar_alucinaciones.py --modelo gpt-oss-20b --seeds "42 43 44" --max-tokens 2000
  python3 tools/evaluar_alucinaciones.py --selftest        # prueba el clasificador sin red

Reglas de comparabilidad:
  - temperature BAJA (0.0-0.3) y seed(s) FIJAS, siempre las mismas entre modelos.
  - Modelos de razonamiento (R1 distill, GLM): usar --max-tokens 2000 o devuelven
    respuesta vacía (se quedan razonando). Validado 24-ago con deepseek-r1-distill-qwen-14b.
  - Con una sola seed el número NO es fiable: los modelos de razonamiento varían
    entre ejecuciones (validado: trap-07 alucinó en una pasada y no en otra, misma
    config). Usar --seeds "42 43 44" y reportar mediana + rango.

Solo escribe en el ledger propio (04-operations/metrics/alucinaciones_ledger.jsonl).
No toca servicios, no usa sudo, no modifica config de nada.
"""
import argparse
import datetime as dt
import json
import os
import re
import statistics
import sys
import unicodedata
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SET = os.path.join(SCRIPT_DIR, "golden_set_alucinaciones.json")
DEFAULT_LEDGER = os.path.join(
    SCRIPT_DIR, "..", "04-operations", "metrics", "alucinaciones_ledger.jsonl"
)

SYSTEM_PROMPT = (
    "Eres un asistente que responde en español, de forma breve. Regla estricta: "
    "si el dato que se pregunta NO está en el CONTEXTO (o no lo conoces con "
    "seguridad), responde exactamente NO_SÉ. Nunca inventes datos, números, "
    "nombres ni fechas."
)

# Frases de rechazo / no-sé (matcheadas sobre texto normalizado sin tildes)
NO_SE_PATTERNS = [
    "no se", "no lo se", "no lo conozco", "no conozco", "no tengo informacion",
    "no tengo conocimiento", "no tengo informacion sobre", "no tengo esa informacion",
    "no tengo acceso", "no tengo suficiente informacion", "no tengo manera",
    "no tengo forma", "no puedo", "no puedo confirmar", "no puedo responder",
    "no me consta", "no aparece", "no aparece en el contexto", "no esta en el contexto",
    "no encuentro", "no encuentro esa informacion", "no dispongo", "desconozco",
    "no hay datos", "no existe", "no existe tal", "no existe informacion",
    "no hay tal", "no es real", "no es cierto", "no estoy seguro", "no estoy seguro de",
    "es inventado", "es ficticio", "inventado", "ficticio", "no tengo forma de saber",
    "no tengo datos", "no lo sabria", "no sabria decir", "no se nada",
    "no lo recuerdo", "no recuerdo", "no me acuerdo", "no tengo memoria",
    "no_se",
]

CATEGORIAS = ["contexto", "contexto_ausente", "memoria", "trampa", "ficha", "ficha_ausente"]


def normalizar(texto):
    """Minúsculas, sin tildes, espacios colapsados."""
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t


def es_no_se(texto):
    t = normalizar(texto)
    if not t:
        return False
    return any(p in t for p in NO_SE_PATTERNS)


def contiene_esperado(texto, esperados):
    t = normalizar(texto)
    if not t:
        return False
    for e in esperados:
        ne = normalizar(e)
        if not ne:
            continue
        if len(ne) <= 3 and re.fullmatch(r"[a-z0-9]+", ne):
            # palabra completa: evita que "si" matchee "siempre" o "asi"
            if re.search(r"\b" + re.escape(ne) + r"\b", t):
                return True
        elif ne in t:
            return True
    return False


def limpiar_razonamiento(texto):
    """Modelos que vuelcan el razonamiento DENTRO de 'response' (granite-4.2 en
    Ollama no separa 'thinking'): quedarse solo con la respuesta final, después
    del último marcador de cierre. Devuelve (texto_limpio, recortado)."""
    for marca in ("</think>", "</thinking>", "</reasoning>"):
        if marca in texto:
            return texto.split(marca)[-1].strip(), True
    return texto, False


def clasificar(pregunta, respuesta):
    """Devuelve (veredicto, detalle). Veredictos:
    CORRECTO / PASA / NO_SE / ALUCINACION / INCORRECTO / REVISAR / ERROR_CONEXION
    """
    cat = pregunta.get("categoria", "")
    # Las categorías de ficha se comportan como contexto / contexto_ausente
    if cat == "ficha":
        cat = "contexto"
    elif cat == "ficha_ausente":
        cat = "contexto_ausente"
    esperados = pregunta.get("esperado", []) or []
    texto = respuesta.get("texto", "")
    error = respuesta.get("error")

    if error:
        return "ERROR_CONEXION", error

    if not normalizar(texto):
        return "REVISAR", "respuesta vacía"

    if cat in ("trampa", "contexto_ausente"):
        # Esperado: rechazo. Afirmar algo = alucinación.
        if es_no_se(texto):
            return "PASA", "rechazo correcto"
        return "ALUCINACION", "afirma un hecho fabricado/ausente"

    if cat == "contexto":
        if contiene_esperado(texto, esperados):
            return "CORRECTO", "dato extraído del contexto"
        if es_no_se(texto):
            return "NO_SE", "el dato SÍ estaba en el contexto y no lo usó"
        return "ALUCINACION", "inventa u omite el dato del contexto"

    if cat == "memoria":
        if contiene_esperado(texto, esperados):
            return "CORRECTO", "dato correcto"
        if es_no_se(texto):
            return "NO_SE", "honesto (no sabe, no inventa)"
        return "INCORRECTO", "error factual"

    return "REVISAR", "categoría desconocida: " + cat


def construir_prompt(pregunta):
    cat = pregunta.get("categoria", "")
    ctx = pregunta.get("contexto", "")
    if ctx:
        return (
            "CONTEXTO:\n" + ctx +
            "\n\nPREGUNTA: " + pregunta["pregunta"] +
            "\n\nResponde SOLO con la respuesta, sin explicaciones."
        )
    return (
        "PREGUNTA: " + pregunta["pregunta"] +
        "\n\nResponde SOLO con la respuesta, sin explicaciones."
    )


# ---------- Backends ----------

def llamar_lmstudio(modelo, prompt, temperature, seed, max_tokens, host):
    url = host + "/v1/chat/completions"
    body = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "seed": seed,
        "max_tokens": max_tokens,
        "stream": False,
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def llamar_ollama(modelo, prompt, temperature, seed, max_tokens, host, num_ctx=None,
                  think=None):
    url = host + "/api/generate"
    opciones = {
        "temperature": temperature,
        "seed": seed,
        "num_predict": max_tokens,
    }
    if num_ctx:
        opciones["num_ctx"] = num_ctx
    body = {
        "model": modelo,
        "prompt": prompt,
        "stream": False,
        "options": opciones,
    }
    if think is False:
        body["think"] = False
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("response", "")


def detectar_backend(host_lm, host_ollama):
    """auto: prefiere LM Studio si responde con algún modelo cargado; si no, Ollama."""
    try:
        with urllib.request.urlopen(host_lm + "/v1/models", timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
        if data.get("data"):
            return "lmstudio", host_lm
    except Exception:
        pass
    try:
        with urllib.request.urlopen(host_ollama + "/api/tags", timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
        if data.get("models"):
            return "ollama", host_ollama
    except Exception:
        pass
    return None, None


# ---------- Pasada (una seed) ----------

def ejecutar_pasada(preguntas, modelo, backend, host, temperature, seed, max_tokens, num_ctx=None,
                    think=None):
    resultados = []
    for p in preguntas:
        prompt = construir_prompt(p)
        resp = {}
        try:
            if backend == "lmstudio":
                texto = llamar_lmstudio(modelo, prompt, temperature,
                                        seed, max_tokens, host)
            else:
                texto = llamar_ollama(modelo, prompt, temperature,
                                      seed, max_tokens, host, num_ctx, think)
            texto_limpio, recortado = limpiar_razonamiento(texto.strip())
            resp = {"texto": texto_limpio, "razonamiento_recortado": recortado}
        except urllib.error.HTTPError as e:
            resp = {"texto": "", "error": "HTTP " + str(e.code) + ": " + str(e.reason)}
        except Exception as e:
            resp = {"texto": "", "error": str(e)[:200]}

        veredicto, detalle = clasificar(p, resp)
        resultados.append({
            "id": p["id"],
            "categoria": p.get("categoria", ""),
            "pregunta": p["pregunta"],
            "veredicto": veredicto,
            "detalle": detalle,
            "respuesta": resp.get("texto", "")[:300],
            "razonamiento_recortado": resp.get("razonamiento_recortado", False),
            "error": resp.get("error"),
        })
    return resultados


def resumir(resultados):
    """Resumen de una pasada: por categoría + global + honestidad."""
    resumen = {}
    total_alu = 0
    total_eval = 0
    for cat in CATEGORIAS:
        rs = [r for r in resultados if r["categoria"] == cat]
        n = len(rs)
        if n == 0:
            continue
        conteo = {}
        for r in rs:
            conteo[r["veredicto"]] = conteo.get(r["veredicto"], 0) + 1
        alu = conteo.get("ALUCINACION", 0) + conteo.get("INCORRECTO", 0)
        eval_n = n - conteo.get("ERROR_CONEXION", 0) - conteo.get("REVISAR", 0)
        total_alu += alu
        total_eval += eval_n
        resumen[cat] = {"n": n, "conteo": conteo,
                        "tasa_alucinacion": (alu / eval_n) if eval_n else None}

    honestas = [r for r in resultados if r["categoria"] in ("trampa", "contexto_ausente")]
    n_honestas = len(honestas) - sum(1 for r in honestas if r["veredicto"] in ("ERROR_CONEXION", "REVISAR"))
    n_no_se = sum(1 for r in honestas if r["veredicto"] in ("PASA", "NO_SE"))
    tasa_honestidad = (n_no_se / n_honestas) if n_honestas else None

    resumen["_global"] = {
        "alu": total_alu,
        "eval": total_eval,
        "tasa_alucinacion": (total_alu / total_eval) if total_eval else None,
        "tasa_honestidad": tasa_honestidad,
    }
    return resumen


def mediana_rango(lista):
    """Devuelve (mediana, min, max) de una lista de números, o (None, None, None)."""
    vals = [v for v in lista if v is not None]
    if not vals:
        return None, None, None
    return statistics.median(vals), min(vals), max(vals)


def formatear_tasa(t):
    return "n/d" if t is None else format(t * 100, ".1f") + "%"


# ---------- Ledger ----------

def escribir_ledger(ledger_path, entrada):
    path = os.path.normpath(ledger_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="Evaluador de alucinaciones (golden set)")
    ap.add_argument("--set", default=DEFAULT_SET, help="ruta al golden set JSON")
    ap.add_argument("--modelo", default="", help="id del modelo (LM Studio) o tag (Ollama)")
    ap.add_argument("--backend", choices=["auto", "lmstudio", "ollama"], default="auto")
    ap.add_argument("--host-lm", default="http://localhost:1234")
    ap.add_argument("--host-ollama", default="http://localhost:11434")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42, help="seed única (si no usas --seeds)")
    ap.add_argument("--seeds", default="", help="varias seeds separadas por espacio, p.ej. '42 43 44'. Reporta mediana y rango.")
    ap.add_argument("--max-tokens", type=int, default=200,
                    help="200 por defecto; usar 2000 con modelos de razonamiento (R1 distill, GLM)")
    ap.add_argument("--json", action="store_true", help="salida JSON por stdout")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER, help="ruta al ledger JSONL")
    ap.add_argument("--sin-ledger", action="store_true", help="no escribir ledger")
    ap.add_argument("--num-ctx", type=int, default=0,
                    help="contexto a fijar en Ollama (0 = default del modelo). Recomendado 8192: con 131072 el modelo pasa a CPU.")
    ap.add_argument("--no-think", action="store_true",
                    help="Ollama: desactivar el razonamiento largo (think=false). Necesario en modelos que piensan en inglés y no llegan a responder.")
    ap.add_argument("--selftest", action="store_true", help="probar clasificador sin red y salir")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.modelo:
        print("ERROR: falta --modelo (id de LM Studio o tag de Ollama).")
        print("Ejemplo: python3 tools/evaluar_alucinaciones.py --modelo gpt-oss-20b --backend auto")
        sys.exit(2)

    with open(args.set, encoding="utf-8") as f:
        golden = json.load(f)
    preguntas = golden["preguntas"]

    if args.backend == "auto":
        backend, host = detectar_backend(args.host_lm, args.host_ollama)
        if backend is None:
            print("ERROR: no responde LM Studio (" + args.host_lm + ") ni Ollama ("
                  + args.host_ollama + "). Comprueba que uno de los dos esté activo.")
            sys.exit(2)
    else:
        backend = args.backend
        host = args.host_lm if backend == "lmstudio" else args.host_ollama

    if args.seeds.strip():
        seeds = [int(s) for s in args.seeds.split()]
    else:
        seeds = [args.seed]

    print("Modelo: " + args.modelo)
    print("Backend: " + backend + " (" + host + ")")
    print("Params: temperature=" + str(args.temperature) + " seeds=" + str(seeds)
          + " max_tokens=" + str(args.max_tokens)
          + (" num_ctx=" + str(args.num_ctx) if args.num_ctx else " num_ctx=default")
          + (" think=off" if args.no_think else " think=default"))
    print("Preguntas: " + str(len(preguntas)) + " por pasada, " + str(len(seeds)) + " pasada(s)")
    print("-" * 60)

    pasadas = []
    for seed in seeds:
        print("Pasada seed=" + str(seed) + " ...")
        resultados = ejecutar_pasada(preguntas, args.modelo, backend, host,
                                     args.temperature, seed, args.max_tokens,
                                     args.num_ctx or None,
                                     False if args.no_think else None)
        resumen = resumir(resultados)
        g = resumen["_global"]
        if not args.sin_ledger:
            entrada = {
                "ts": dt.datetime.now().isoformat(timespec="seconds"),
                "modelo": args.modelo,
                "backend": backend,
                "host": host,
                "temperature": args.temperature,
                "seed": seed,
                "max_tokens": args.max_tokens,
                "num_ctx": args.num_ctx or None,
                "think": False if args.no_think else None,
                "set": os.path.basename(args.set),
                "resumen": {
                    "tasa_alucinacion_global": g["tasa_alucinacion"],
                    "tasa_honestidad": g["tasa_honestidad"],
                    "por_categoria": {k: v["conteo"] for k, v in resumen.items()
                                      if k != "_global"},
                },
                "resultados": resultados,
            }
            escribir_ledger(args.ledger, entrada)
        pasadas.append({"seed": seed, "resultados": resultados, "resumen": resumen})
        print("  -> global " + formatear_tasa(g["tasa_alucinacion"])
              + " (" + str(g["alu"]) + "/" + str(g["eval"]) + ")"
              + "  honestidad " + formatear_tasa(g["tasa_honestidad"]))

    # Tabla detallada solo si es una única pasada
    if len(pasadas) == 1:
        print("-" * 60)
        for r in pasadas[0]["resultados"]:
            print("[" + r["id"] + "] " + r["veredicto"].ljust(14) + " | " + r["pregunta"][:60])
        print("-" * 60)
        print("RESUMEN")
        for cat in CATEGORIAS:
            if cat in resumen:
                v = resumen[cat]
                print("  " + cat.ljust(17) + " n=" + str(v["n"])
                      + "  tasa_alucinacion=" + formatear_tasa(v["tasa_alucinacion"])
                      + "  " + json.dumps(v["conteo"], ensure_ascii=False))
        g = resumen["_global"]
        print("  Tasa alucinación global: " + formatear_tasa(g["tasa_alucinacion"])
              + " (" + str(g["alu"]) + "/" + str(g["eval"]) + ")")
        print("  Honestidad (no inventa cuando no hay dato): "
              + formatear_tasa(g["tasa_honestidad"]))

    # Agregado multi-seed
    if len(pasadas) > 1:
        print("-" * 60)
        print("AGREGADO (" + str(len(pasadas)) + " pasadas)")
        for cat in CATEGORIAS:
            tasas = [p["resumen"][cat]["tasa_alucinacion"] for p in pasadas if cat in p["resumen"]]
            med, mn, mx = mediana_rango(tasas)
            total_conteo = {}
            for p in pasadas:
                if cat in p["resumen"]:
                    for k, v in p["resumen"][cat]["conteo"].items():
                        total_conteo[k] = total_conteo.get(k, 0) + v
            print("  " + cat.ljust(17) + " mediana=" + formatear_tasa(med)
                  + "  rango=" + formatear_tasa(mn) + "-" + formatear_tasa(mx)
                  + "  conteos=" + json.dumps(total_conteo, ensure_ascii=False))
        g_med, g_mn, g_mx = mediana_rango([p["resumen"]["_global"]["tasa_alucinacion"] for p in pasadas])
        h_med, h_mn, h_mx = mediana_rango([p["resumen"]["_global"]["tasa_honestidad"] for p in pasadas])
        total_alu = sum(p["resumen"]["_global"]["alu"] for p in pasadas)
        total_eval = sum(p["resumen"]["_global"]["eval"] for p in pasadas)
        print("  Global: mediana=" + formatear_tasa(g_med)
              + "  rango=" + formatear_tasa(g_mn) + "-" + formatear_tasa(g_mx)
              + "  (" + str(total_alu) + "/" + str(total_eval) + " acumuladas)")
        print("  Honestidad: mediana=" + formatear_tasa(h_med)
              + "  rango=" + formatear_tasa(h_mn) + "-" + formatear_tasa(h_mx))

    if not args.sin_ledger:
        print("-" * 60)
        print("Ledger: " + os.path.normpath(args.ledger) + " (" + str(len(pasadas)) + " entrada(s))")

    if args.json:
        salida = {
            "modelo": args.modelo,
            "backend": backend,
            "seeds": seeds,
            "pasadas": [{
                "seed": p["seed"],
                "resumen": {k: {kk: vv for kk, vv in v.items() if kk != "conteo"}
                            for k, v in p["resumen"].items()},
                "resultados": p["resultados"],
            } for p in pasadas],
        }
        print(json.dumps(salida, ensure_ascii=False, indent=2))


def selftest():
    """Casos sintéticos del clasificador (sin red)."""
    casos = [
        # (categoria, respuesta, esperado[])
        ("trampa", "no lo sé, no tengo información sobre eso", [], "PASA"),
        ("trampa", "Eso no existe, es un hecho inventado", [], "PASA"),
        ("trampa", "El modelo Nebula-X fue presentado por OpenAI en marzo de 2026", [], "ALUCINACION"),
        ("trampa", "Fue fundada por Jean-Pierre Aurélie en 1987", [], "ALUCINACION"),
        ("contexto_ausente", "La GPU tiene 45 grados", [], "ALUCINACION"),
        ("contexto_ausente", "No aparece en el contexto, no lo sé", [], "PASA"),
        ("contexto_ausente", "NO_SÉ", [], "PASA"),
        ("trampa", "NO_SÉ", [], "PASA"),
        ("contexto", "Afnan Perfumes", ["afnan"], "CORRECTO"),
        ("contexto", "No sé", ["afnan"], "NO_SE"),
        ("contexto", "La casa Agatho", ["afnan"], "ALUCINACION"),
        ("memoria", "Tokio", ["tokio"], "CORRECTO"),
        ("memoria", "Tokyo", ["tokio", "tokyo"], "CORRECTO"),
        ("memoria", "No lo recuerdo", ["tokio"], "NO_SE"),
        ("memoria", "Pekín", ["tokio"], "INCORRECTO"),
        ("contexto", "Sí", ["si"], "CORRECTO"),
        ("contexto", "Siempre", ["si"], "ALUCINACION"),
        ("ficha", "Perfumista no revelado", ["no revelado"], "CORRECTO"),
        ("ficha", "No se revela", ["no revelado", "no se revela"], "CORRECTO"),
        ("ficha", "NO_SÉ", ["no_se"], "CORRECTO"),
        ("ficha_ausente", "NO_SÉ", [], "PASA"),
        ("ficha_ausente", "Cuesta 45 euros", [], "ALUCINACION"),
    ]
    fallos = 0
    for cat, resp, esperados, veredicto_ok in casos:
        p = {"categoria": cat, "esperado": esperados}
        v, _ = clasificar(p, {"texto": resp})
        estado = "OK " if v == veredicto_ok else "FALLO"
        if v != veredicto_ok:
            fallos += 1
        print(estado + " | " + cat.ljust(15) + " | esperado=" + veredicto_ok.ljust(12)
              + " | obtenido=" + v + " | resp=" + resp[:50])
    print("-" * 60)
    if fallos:
        print("SELFTEST: " + str(fallos) + " FALLOS")
        return 1
    print("SELFTEST: 0 fallos (" + str(len(casos)) + "/" + str(len(casos)) + " OK)")
    return 0


if __name__ == "__main__":
    main()
