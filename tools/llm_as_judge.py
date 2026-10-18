#!/usr/bin/env python3
"""
llm_as_judge.py — LLM-as-Judge formal para el lab (A2, 20-ago-2026).

Dos modelos INDEPENDIENTES puntúan la CALIDAD de una respuesta (no solo la
veracidad — eso ya lo hace el gate-veracidad). Dimensiones:
  1. fidelidad     — ¿la respuesta usa el contexto dado o inventa? (faithfulness)
  2. completitud   — ¿responde TODO lo preguntado?
  3. relevancia    — ¿responde a la pregunta o se va por las ramas?
  4. claridad      — ¿bien estructurada y legible?
  5. utilidad      — ¿accionable para el lab (OBS→HYP→EXP→DEC)?

Veredicto consolidado:
  - PASA     → ambos jueces puntúan ≥3 en todas las dimensiones y promedio ≥3.5
  - REVISA   → al menos un juez puntúa <3 en alguna dimensión (mejorable)
  - FALLA    → ambos puntúan <3 en la misma dimensión (o promedio <2.5)
  - DISCREPANCIA → los jueces divergen (promedio difiere ≥1.5 o veredictos
    opuestos PASA/FALLA) → requiere revisión humana (patrón evaluador
    independiente del estudio Autobots).

Jueces: J1 = glm-4.6v-flash (local), J2 = openai/gpt-oss-20b (local batch).
Ambos via LM Studio API → coste 0 (regla: después de las 12:00 → local).

Uso:
  python3 tools/llm_as_judge.py --pregunta "..." --respuesta "..."
      [--contexto "..." ] [--json] [--juez1 MODELO] [--juez2 MODELO]
  echo '{"pregunta":"...","respuesta":"..."}' | python3 tools/llm_as_judge.py --stdin

Dependencias: urllib (stdlib). No requiere internet.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ENDPOINT = "http://localhost:1234/api/v0/chat/completions"
JUEZ1_DEF = "glm-4.6v-flash"        # local, carga habitual del lab
JUEZ2_DEF = "openai/gpt-oss-20b"    # local batch (validado 19-ago, razonamiento duro)

_PROMPT_JUEZ = """Eres un evaluador de CALIDAD de respuestas en español (Joko Lab). Puntúa la respuesta del 1 al 5 en cada dimensión y responde SOLO en JSON con EXACTAMENTE estas claves:
{"fidelidad": int, "completitud": int, "relevancia": int, "claridad": int, "utilidad": int, "veredicto": "PASA|REVISA|FALLA", "justificacion": "máx 2 frases"}

Reglas de puntuación:
- fidelidad: 5 = usa solo el contexto dado y no inventa; 1 = inventa datos ausentes.
- completitud: 5 = responde todo lo preguntado; 1 = omite partes esenciales.
- relevancia: 5 = directa a la pregunta; 1 = divaga o responde otra cosa.
- claridad: 5 = estructura clara, legible; 1 = confusa o desordenada.
- utilidad: 5 = accionable (qué hacer, cuándo, cómo verificarlo); 1 = no permite actuar.
- veredicto: PASA (≥3 en todo y promedio ≥3.5), REVISA (alguna dimensión <3), FALLA (promedio <2.5).

PREGUNTA: {pregunta}
CONTEXTO DISPONIBLE (puede estar vacío): {contexto}
RESPUESTA A EVALUAR:
{respuesta}
"""


def _json_from_content(content: str) -> dict | None:
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _modelo_cargado(model: str) -> bool:
    """¿Está el modelo cargado en LM Studio? (GET /api/v0/models → state=loaded)"""
    try:
        req = urllib.request.Request(ENDPOINT.rsplit("/chat", 1)[0] + "/models")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        for m in data.get("data", []):
            if m.get("id") == model and m.get("state") == "loaded":
                return True
        return False
    except Exception:
        return False


def _modelos_cargados() -> set:
    """Conjunto de modelos cargados en LM Studio (id con state=loaded)."""
    try:
        req = urllib.request.Request(ENDPOINT.rsplit("/chat", 1)[0] + "/models")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        return {m.get("id") for m in data.get("data", []) if m.get("state") == "loaded"}
    except Exception:
        return set()


def _lms_cmd(*args: str, timeout: int = 200) -> bool:
    import subprocess
    try:
        r = subprocess.run(["lms", *args], capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


def _cargar_bajo_demanda(model: str, swap: bool = False) -> bool:
    """Intenta lms load (patrón llm-router).

    Sin swap: si la VRAM libre no da para el modelo, devuelve False sin intentar
    (evita colgarse 200s — con GLM cargado gpt-oss no cabe en 12 GB).
    Con swap=True (doble juez): descarga el/los modelo(s) que ocupan VRAM y
    carga el necesario (patrón validado 21-ago).
    """
    import subprocess
    # Estimación mínima de VRAM por modelo (GGUF Q4_K_M aproximado)
    VRAM_MIN = {"openai/gpt-oss-20b": 10.5, "glm-4.6v-flash": 7.0}
    need = VRAM_MIN.get(model, 6.0)
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=15)
        free_gb = float(r.stdout.strip().split(",")[0]) / 1024
        if free_gb >= need:
            return _lms_cmd("load", model)
    except Exception:
        pass  # si no se puede medir, intentar lms load igualmente
    if swap:
        print(f"  [juez] swap: descargo ocupantes para {model}", file=sys.stderr)
        for m in _modelos_cargados():
            if m != model:
                _lms_cmd("unload", m, timeout=60)
        time.sleep(2)
        return _lms_cmd("load", model)
    return False


def juzgar(respuesta: str, pregunta: str, contexto: str,
           model: str, timeout: int = 300, swap: bool = False,
           n_juicios: int = 3) -> dict:
    """Pide a UN modelo N veredictos independientes y devuelve el PROMEDIO.

    Robustez (25-ago-2026): una sola llamada podía fallar (JSON inválido,
    timeout, alucinación puntual) → veredicto perdido. Ahora se hacen
    `n_juicios` llamadas (default 3, máx intentos 2*n para tolerar fallos)
    y se promedian las dimensiones. El veredicto se recalcula del promedio
    con las mismas reglas que el prompt. Devuelve dict con dimensiones
    promediadas + n_juicios obtenidos.
    """
    if not _modelo_cargado(model):
        if not _cargar_bajo_demanda(model, swap=swap):
            print(f"  [juez] {model} no cargado — omitido (VRAM insuficiente o lms load falló)", file=sys.stderr)
            return {"modelo": model, "usado": False,
                    "error": "no se pudo cargar (probablemente VRAM ocupada por otro modelo)"}
        print(f"  [juez] {model} cargado bajo demanda", file=sys.stderr)
    prompt = (_PROMPT_JUEZ
              .replace("{pregunta}", pregunta[:2000])
              .replace("{contexto}", (contexto or "")[:3000])
              .replace("{respuesta}", respuesta[:4000]))
    DIMS = ("fidelidad", "completitud", "relevancia", "claridad", "utilidad")
    acum = {d: [] for d in DIMS}
    veredictos = []
    n_obtenidos = 0
    max_intentos = max(2 * n_juicios, 3)
    for intento in range(max_intentos):
        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,  # glm razona en voz alta antes del JSON: 300 no bastaba
                "temperature": 0.2,  # algo de variación para que los N juicios no sean idénticos
            }
            req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.load(r)
            content = (resp.get("choices", [{}])[0].get("message", {}).get("content")
                       or resp.get("choices", [{}])[0].get("message", {}).get("reasoning_content") or "")
            data = _json_from_content(content)
            if data and "veredicto" in data:
                for d in DIMS:
                    v = data.get(d)
                    if isinstance(v, (int, float)):
                        acum[d].append(float(v))
                veredictos.append(data.get("veredicto", "REVISA"))
                n_obtenidos += 1
                if n_obtenidos >= n_juicios:
                    break
        except Exception as e:
            if intento == max_intentos - 1:
                return {"modelo": model, "usado": False, "error": str(e)[:120]}
    if n_obtenidos == 0:
        return {"modelo": model, "usado": False, "error": "sin respuesta JSON válida"}
    prom = {d: round(sum(acum[d]) / len(acum[d]), 2) if acum[d] else 5.0
            for d in DIMS}
    promedio = round(sum(prom.values()) / len(DIMS), 2)
    # Mismas reglas que el prompt: PASA (≥3 en todo y promedio ≥3.5), REVISA (alguna <3), FALLA (promedio <2.5)
    if promedio < 2.5:
        veredicto = "FALLA"
    elif any(prom[d] < 3 for d in DIMS):
        veredicto = "REVISA"
    else:
        veredicto = "PASA"
    # Conserva la regla determinista crítica: fidelidad/completitud ≤1 → FALLA
    if prom["fidelidad"] <= 1 or prom["completitud"] <= 1:
        veredicto = "FALLA"
    return {"modelo": model, "usado": True, **prom,
            "veredicto": veredicto, "n_juicios": n_obtenidos}


def _promedio(v: dict) -> float:
    dims = [v.get(k, 0) for k in ("fidelidad", "completitud", "relevancia", "claridad", "utilidad")]
    return sum(dims) / len(dims) if dims else 0.0


def consolidar(j1: dict, j2: dict) -> dict:
    """Fusiona dos veredictos de jueces independientes."""
    if not j1.get("usado") and not j2.get("usado"):
        return {"estado": "SIN_JUEZ", "detalle": "Ningún juez disponible (LM Studio apagado o sin modelos)."}
    jueces = [j for j in (j1, j2) if j.get("usado")]
    if len(jueces) == 1:
        j = jueces[0]
        # Regla determinista crítica también en UN_JUEZ (fidelidad/completitud ≤1 → FALLA)
        v_forzado = j.get("veredicto")
        if j.get("fidelidad", 5) <= 1 or j.get("completitud", 5) <= 1:
            v_forzado = "FALLA"
        return {"estado": "UN_JUEZ",
                "jueces": [{"modelo": j["modelo"], "promedio": round(_promedio(j), 2),
                            "veredicto": v_forzado,
                            "dimensiones": {k: j.get(k) for k in ("fidelidad", "completitud", "relevancia", "claridad", "utilidad")}}],
                "promedio": round(_promedio(j), 2), "veredicto": v_forzado,
                "detalle": f"Solo {j['modelo']} respondió; falta juez independiente."}
    p1, p2 = _promedio(j1), _promedio(j2)
    v1, v2 = j1.get("veredicto"), j2.get("veredicto")

    # Regla determinista CRÍTICA (20-ago): inventar es fallo, no "revisar".
    # Si un juez puntúa fidelidad o completitud ≤1, el veredicto de ESE juez
    # se fuerza a FALLA (el LLM tiende a suavizar con REVISA si el resto es alto).
    def _forzar_falla(v: dict) -> str:
        if v.get("fidelidad", 5) <= 1 or v.get("completitud", 5) <= 1:
            return "FALLA"
        return v.get("veredicto", "REVISA")

    v1, v2 = _forzar_falla(j1), _forzar_falla(j2)
    discrepa = (abs(p1 - p2) >= 1.5) or (v1 == "PASA" and v2 == "FALLA") or (v1 == "FALLA" and v2 == "PASA")
    if discrepa:
        veredicto = "DISCREPANCIA"
    elif v1 == "FALLA" and v2 == "FALLA":
        veredicto = "FALLA"
    elif v1 == "PASA" and v2 == "PASA":
        veredicto = "PASA"
    else:
        veredicto = "REVISA"
    return {
        "estado": "CONSENSO" if not discrepa else "DISCREPANCIA",
        "jueces": [{"modelo": j1["modelo"], "promedio": round(p1, 2), "veredicto": v1,
                    "dimensiones": {k: j1.get(k) for k in ("fidelidad", "completitud", "relevancia", "claridad", "utilidad")}},
                   {"modelo": j2["modelo"], "promedio": round(p2, 2), "veredicto": v2,
                    "dimensiones": {k: j2.get(k) for k in ("fidelidad", "completitud", "relevancia", "claridad", "utilidad")}}],
        "promedio": round((p1 + p2) / 2, 2),
        "veredicto": veredicto,
        "detalle": ("Divergencia entre jueces (Δ %.2f): revisar manualmente." % abs(p1 - p2)) if discrepa
                   else "Ambos jueces en acuerdo.",
    }


LOG_DB = os.path.expanduser("~/joko-lab/04-operations/metrics/llm_judge_veredictos.db")


def _restaurar_estado(originales: set) -> None:
    """Restaura el estado de modelos previo al swap (no bloquea si falla)."""
    cargados = _modelos_cargados()
    for m in cargados - originales:
        _lms_cmd("unload", m, timeout=60)
    time.sleep(1)
    for m in originales - _modelos_cargados():
        _lms_cmd("load", m, timeout=200)


def _guardar_log(res: dict, pregunta: str, respuesta: str) -> None:
    """Registra el veredicto consolidado + dimensiones por juez en SQLite."""
    import sqlite3
    from datetime import datetime
    try:
        os.makedirs(os.path.dirname(LOG_DB), exist_ok=True)
        con = sqlite3.connect(LOG_DB)
        con.execute("""CREATE TABLE IF NOT EXISTS veredictos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, estado TEXT, veredicto TEXT, promedio REAL, detalle TEXT,
            preg_sha TEXT, resp_len INTEGER)""")
        con.execute("""CREATE TABLE IF NOT EXISTS dimensiones (
            veredicto_id INTEGER, juez TEXT, dimension TEXT, puntuacion INTEGER)""")
        cur = con.execute(
            "INSERT INTO veredictos (ts,estado,veredicto,promedio,detalle,preg_sha,resp_len) VALUES (?,?,?,?,?,?,?)",
            (datetime.now().isoformat(), res.get("estado"), res.get("veredicto"),
             res.get("promedio"), res.get("detalle", ""),
             hashlib.sha1(pregunta.encode()).hexdigest()[:8], len(respuesta)))
        vid = cur.lastrowid
        for j in res.get("jueces", []):
            for dim, val in (j.get("dimensiones") or {}).items():
                con.execute("INSERT INTO dimensiones VALUES (?,?,?,?)",
                            (vid, j.get("modelo", "?"), dim, val))
        con.commit()
        con.close()
    except Exception as e:
        print(f"  [log] no registrado: {e}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description="LLM-as-Judge formal (2 jueces independientes)")
    ap.add_argument("--pregunta", default="")
    ap.add_argument("--respuesta", default="")
    ap.add_argument("--contexto", default="")
    ap.add_argument("--juez1", default=JUEZ1_DEF)
    ap.add_argument("--juez2", default=JUEZ2_DEF)
    ap.add_argument("--n-juicios", type=int, default=3,
                    help="número de llamadas por juez (default 3; 1 = comportamiento anterior)")
    ap.add_argument("--swap", action="store_true",
                    help="swap automático de modelos para el doble juez (restaura el estado original al final)")
    ap.add_argument("--log", action="store_true",
                    help="registra el veredicto en SQLite (metrics/llm_judge_veredictos.db)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--stdin", action="store_true", help="lee JSON {pregunta,respuesta,contexto?}")
    args = ap.parse_args()

    if args.stdin:
        try:
            data = json.load(sys.stdin)
            pregunta = data.get("pregunta", "")
            respuesta = data.get("respuesta", "")
            contexto = data.get("contexto", "")
        except Exception as e:
            print(f"ERROR stdin: {e}")
            return 1
    else:
        pregunta, respuesta, contexto = args.pregunta, args.respuesta, args.contexto
    if not respuesta.strip():
        print("ERROR: --respuesta vacía")
        return 1

    estado_original = _modelos_cargados() if args.swap else set()
    j1 = juzgar(respuesta, pregunta, contexto, args.juez1, swap=args.swap, n_juicios=args.n_juicios)
    j2 = juzgar(respuesta, pregunta, contexto, args.juez2, swap=args.swap, n_juicios=args.n_juicios)
    res = consolidar(j1, j2)

    if args.swap:
        _restaurar_estado(estado_original)
        print(f"  [juez] estado de modelos restaurado", file=sys.stderr)
    if args.log:
        _guardar_log(res, pregunta, respuesta)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"=== LLM-AS-JUDGE (A2) — {res.get('estado')} ===")
        print(f"Veredicto: {res.get('veredicto')} | promedio: {res.get('promedio')}")
        print(f"Detalle: {res.get('detalle')}")
        for j in res.get("jueces", []):
            d = j.get("dimensiones", {})
            print(f"  [{j['modelo']}] promedio {j['promedio']} ({j['veredicto']}) | "
                  f"fid {d.get('fidelidad')} compl {d.get('completitud')} rel {d.get('relevancia')} "
                  f"clar {d.get('claridad')} util {d.get('utilidad')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
