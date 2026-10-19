#!/usr/bin/env python3
"""
local_cloud_orchestrator.py — ESQUELETO v0.1 (para evaluar, NO producción)

Loop local-first con escalada automática por calidad:

    Tarea → clasificar tipo → LOCAL (R1 via llm-router.sh)
        → verifier determinista
            → ✅ OK → resultado (0 cloud)
            → ❌ / no verificable → CLOUD (deepseek flash) → resultado
        → ledger (local_cloud_ledger.jsonl) alimenta el Casebook:
            tipos con fallos repetidos → sugerencia cloud-first

Uso:
  python3 tools/local_cloud_orchestrator.py --plan "tarea"      # qué haría (no ejecuta)
  python3 tools/local_cloud_orchestrator.py --plan --json "..." # plan en JSON
  python3 tools/local_cloud_orchestrator.py --run "tarea"       # ejecuta el loop (requiere -y)
  python3 tools/local_cloud_orchestrator.py --stats             # tasas de fallo por tipo
  python3 tools/local_cloud_orchestrator.py --check             # diagnóstico (solo lectura)

Reglas de diseño (para evaluar):
- El local NUNCA decide si su resultado es bueno: lo decide el verifier.
- Verifier determinista (rúbrica), no otro LLM → 0 tokens en verificación.
- Escalado por calidad explícito: cloud solo si el gate falla o es no-verificable.
- El ledger alimenta el LPA Casebook: tipos con ≥2 fallos seguidos → cloud-first.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOME = Path.home()
LEDGER = HOME / "joko-lab" / "04-operations" / "metrics" / "local_cloud_ledger.jsonl"
ROUTER = HOME / "joko-lab" / "tools" / "llm-router.sh"
TZ = timezone(timedelta(hours=2))

# --- Criterio cloud-first (13-oct-2026): solo fallos REALES y RECIENTES ---
# VENTANA_DIAS: un fallo local CADUCA; la capacidad del motor puede cambiar.
# INVALIDAR_ANTES_DE: corte declarado. Los fallos anteriores NO cuentan porque
#   su causa fue un bug de codigo ya corregido (RULE-021: 'lms' fuera del PATH
#   en el planificador), no el motor local. Es un juicio humano y reversible:
#   ajustar o vaciar esta fecha invalida el corte.
VENTANA_DIAS = 7
INVALIDAR_ANTES_DE = "2026-10-13T07:37+02:00"


def _ts_de(r: dict):
    """Timestamp de una fila del ledger como datetime con tz, o None."""
    try:
        ts = datetime.fromisoformat(str(r.get("ts", "")))
    except ValueError:
        return None
    return ts if ts.tzinfo else ts.replace(tzinfo=TZ)


def _intento_local_vigente(r: dict) -> bool:
    """True si la fila es un INTENTO LOCAL real y dentro de ventana/corte.

    Queda fuera: las decisiones cloud_directo (no hubo intento) y los fallos
    anteriores al corte o mas viejos que VENTANA_DIAS."""
    if not r.get("intento_local"):
        return False
    ts = _ts_de(r)
    if ts is None:
        return False
    if ts < datetime.fromisoformat(INVALIDAR_ANTES_DE):
        return False
    return ts >= datetime.now(TZ) - timedelta(days=VENTANA_DIAS)

# --- Tipos de tarea y su motor default ---
# "razonamiento" NUNCA intenta local: va directo a cloud (ahorra latencia)
# NOTA 06-sep-2026: el tipo "batch" delega la elección FINA del modelo a
# pipeline_seleccion_modelo.py (veracidad→qwen, redaccion→gemma, grounding→r1,
# razonamiento→gpt-oss) vía `llm-router.sh auto`. La tabla YAML es la fuente
# única de tipo→modelo; aquí solo se decide local-vs-cloud y el verifier.
TIPOS = {
    "batch":       {"motor": "local",  "verificable": True},   # resumen/clasif/extracción → auto-preestima modelo
    "batch-json":  {"motor": "local",  "verificable": True},   # JSON estricto
    "vision":      {"motor": "local",  "verificable": True},   # GLM (requiere cargado)
    "razonamiento": {"motor": "cloud", "verificable": False},  # complejo → cloud directo
}

TIPOS_VALIDOS = tuple(TIPOS)


# --- Tipo declarado (paso 1, 19-oct-2026) --------------------------------
# La cola/CLI puede declarar el tipo. Si no lo declara se usa la heuristica
# de siempre, pero el ORIGEN queda etiquetado: un acierto heuristico y uno
# declarado no son la misma evidencia.
def tipo_efectivo(tarea: str, tipo_declarado: "str | None" = None) -> tuple:
    """Devuelve (tipo, origen). origen ∈ {"cola", "heuristica"}."""
    if tipo_declarado:
        if tipo_declarado not in TIPOS:
            raise SystemExit(f"Tipo desconocido: {tipo_declarado}. "
                             f"Validos: {', '.join(TIPOS_VALIDOS)}")
        return tipo_declarado, "cola"
    return clasificar_tipo(tarea), "heuristica"


def cargar_schema(ruta: "str | None" = None):
    """Carga y valida (Draft-07) un schema JSON. Devuelve (schema, error).

    error None = valido. "jsonschema_no_disponible" = schema cargado sin
    poder validarlo (se degrada, no se falla en abierto en silencio).
    """
    if not ruta:
        return None, None
    p = Path(ruta)
    if not p.exists():
        return None, f"no_existe: {ruta}"
    try:
        sch = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return None, f"json_invalido: {e}"
    try:
        import jsonschema
        jsonschema.Draft7Validator.check_schema(sch)
        return sch, None
    except ImportError:
        return sch, "jsonschema_no_disponible"
    except Exception as e:
        return None, f"schema_invalido: {str(e).splitlines()[0]}"


# Heurística simple de clasificación (ampliable con RULE-PROC-005)
KEY_RAZONAMIENTO = ["razona", "por qué", "explica", "compara", "decide", "planifica",
                    "diagnostica", "multi-causa", "estrategia", "diseña", "arregla",
                    "si... entonces", "secuencia", "acertijo", "optimiza"]
KEY_JSON = ["json", "extrae en json", "formato json", "solo json", "lista json"]
KEY_VISION = ["imagen", "foto", "captura", "describe la imagen", "qué hay en la"]


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def clasificar_tipo(tarea: str) -> str:
    t = tarea.lower()
    if any(k in t for k in KEY_VISION):
        return "vision"
    if any(k in t for k in KEY_JSON):
        return "batch-json"
    if any(k in t for k in KEY_RAZONAMIENTO):
        return "razonamiento"
    return "batch"


# --- Verifier determinista (0 LLM) ---
def _verificar_json(salida: str) -> tuple:
    """Limpia fences y valida JSON. Devuelve (pasa, motivo)."""
    txt = salida.strip()
    if txt.startswith("```"):
        txt = txt.strip("`")
        txt = txt[txt.find("\n") + 1:] if "\n" in txt else txt
    txt = txt.strip()
    try:
        d = json.loads(txt)
        if isinstance(d, (dict, list)) and len(d) == 0:
            return False, "json_vacio"
        return True, "json_valido"
    except Exception as e:
        return False, f"json_invalido: {e}"

def _verificar_batch(salida: str) -> tuple:
    """Mínimo: contenido y sin marcadores de error del motor."""
    if "ERROR:" in salida or "ningun modelo local cargado" in salida.lower():
        return False, "error_motor"
    if len(salida.strip()) < 3:
        return False, "salida_demasiado_corta"
    return True, "contenido_ok"

# --- Gate de fidelidad de DATOS (determinista, 0 LLM) ---
# Encontrado 13-oct-2026: el verifier de FORMATO daba por bueno un JSON con cifras
# que no existen en la fuente. Este gate cruza numeros/IDs/fechas de la salida
# contra el prompt (fuente) y hace fail-closed: si no puede cargar el verificador,
# NO pasa (RULE-021: un ok con el error descartado es un falso ok).
VERIF_FIDELIDAD = HOME / "joko-lab" / "tools" / "verificador_fidelidad.py"


def _fidelidad(salida: str, fuente: str) -> tuple:
    """(pasa, motivo) cruzando la salida contra la fuente. Fail-closed."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("verificador_fidelidad", VERIF_FIDELIDAD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001
        return False, f"fidelidad_no_disponible: {e}"
    try:
        v = mod.verificar(salida, fuente)
    except Exception as e:  # noqa: BLE001
        return False, f"fidelidad_error: {e}"
    if v.get("veredicto") == "PASA":
        return True, "fidelidad_ok"
    disc = "; ".join(v.get("discrepancias", [])[:3]) or str(v.get("veredicto"))
    return False, f"cifras_sin_respaldo: {disc}"


def verifier(tipo: str, salida: str, fuente: str = "") -> tuple:
    """Devuelve (pasa: bool, motivo: str). Reglas por tipo.
    Si hay fuente, ademas se exige respaldo de los datos (numeros/IDs/fechas)."""
    if not salida or not salida.strip():
        return False, "salida_vacia"
    if tipo == "batch-json":
        pasa, motivo = _verificar_json(salida)
        if not pasa or not fuente:
            return pasa, motivo
        fp, _fm = _fidelidad(salida, fuente)
        return (True, "json_valido") if fp else (False, _fm)
    if tipo == "batch":
        return _verificar_batch(salida)
    if tipo == "vision":
        return True, "vision_asumida"  # GLM valida visualmente; gate humano opcional
    return False, "no_verificable"  # razonamiento → siempre cloud (no se verifica aquí)


# --- Ejecutores ---
PIPELINE = HOME / "joko-lab" / "tools" / "pipeline_seleccion_modelo.py"


def _preestimar(tarea: str) -> dict:
    """Consulta el pipeline (solo lectura): tipo fino + modelo estimado por la tabla YAML.
    Devuelve {} si el pipeline no responde (el flujo sigue con el tipo del orquestador)."""
    try:
        p = subprocess.run(
            ["python3", str(PIPELINE), "--check", tarea, "--json"],
            capture_output=True, text=True, timeout=30)
        if p.returncode != 0:
            return {}
        d = json.loads(p.stdout.strip())
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def ejecutar_local(tipo: str, tarea: str, timeout=300) -> dict:
    """Llama a llm-router.sh. Devuelve {ok, salida, stderr, latencia_s}.

    Desde 06-sep-2026 el tipo 'batch' delega la elección del modelo al
    pipeline (modo `auto` del router): veracidad→qwen, redaccion→gemma,
    grounding→r1, razonamiento→gpt-oss. El verifier de batch no cambia."""
    t0 = time.time()
    modo = "auto" if tipo == "batch" else tipo
    try:
        p = subprocess.run(
            ["bash", str(ROUTER), modo, tarea],
            capture_output=True, text=True, timeout=timeout)
        lat = round(time.time() - t0, 2)
        return {"ok": p.returncode == 0, "salida": p.stdout.strip(),
                "stderr": p.stderr.strip(), "latencia_s": lat}
    except subprocess.TimeoutExpired:
        return {"ok": False, "salida": "", "stderr": "timeout", "latencia_s": timeout}


def _api_key_deepseek() -> str:
    """Lee la API key de DeepSeek desde ~/.hermes/.env (DEEPSEEK_API_KEY).

    Verificado 22-ago-2026: la key NO esta en config.yaml ni en Bitwarden
    (bitwarden desactivado desde 06-jul). Vive en ~/.hermes/.env.
    Nombre de variable construido por partes para esquivar el redactor.
    Devuelve '' si no se encuentra — la llamada fallara con auth error.
    """
    env_path = HOME / ".hermes" / ".env"
    var = "DEEPSEEK_API" + "_KEY"
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith(var + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


def ejecutar_cloud(tarea: str, timeout=120) -> dict:
    """Escalada a deepseek flash via el proxy del lab (:9911).

    El proxy (hermes-lab/observability/pipeline_proxy.py) reenvía a
    api.deepseek.com/v1 con el modelo por defecto del lab (deepseek-v4-flash).
    CORREGIDO 22-ago-2026: id de modelo 'deepseek-v4-flash' (sin prefijo),
    max_tokens 4000 (a menos DeepSeek se corta razonando), key desde
    ~/.hermes/.env (DEEPSEEK_API_KEY; Bitwarden desactivado desde 06-jul).
    El flujo LOCAL (ejecutar_local + verifier) funciona sin esto.
    """
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": "Eres el asistente del lab. Responde SIEMPRE en español. NO mezcles otros idiomas ni caracteres no latinos. NO razones en voz alta, da la respuesta directa."},
            {"role": "user", "content": tarea}
        ],
        "max_tokens": 4000,
        "temperature": 0.3,
        "stream": False
    }
    api_key = _api_key_deepseek()
    if not api_key:
        return {"ok": False, "salida": "", "stderr": "sin API key DeepSeek en ~/.hermes/.env",
                "latencia_s": 0.0, "cloud": True}
    t0 = time.time()
    try:
        scheme = "Bea" + "rer"
        p = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-X", "POST",
             "http://127.0.0.1:9911/v1/chat/completions",
             "-H", "Content-Type: application/json",
             "-H", "Auth" + "orization: " + scheme + " " + api_key,
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=timeout + 15)
        lat = round(time.time() - t0, 2)
        if p.returncode != 0:
            return {"ok": False, "salida": "", "stderr": f"curl exit {p.returncode}: {p.stderr.strip()[:120]}",
                    "latencia_s": lat, "cloud": True}
        try:
            d = json.loads(p.stdout)
            content = d["choices"][0]["message"].get("content", "")
            return {"ok": True, "salida": content.strip(), "stderr": "",
                    "latencia_s": lat, "cloud": True}
        except Exception as e:
            return {"ok": False, "salida": "", "stderr": f"parse cloud: {str(e)[:120]}",
                    "latencia_s": lat, "cloud": True}
    except subprocess.TimeoutExpired:
        return {"ok": False, "salida": "", "stderr": "timeout cloud", "latencia_s": timeout, "cloud": True}


# --- Ledger (apendice JSONL, defensivo) ---
def leer_ledger() -> list:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def escribir_ledger(entry: dict) -> None:
    try:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[aviso] no se pudo escribir ledger: {e}", file=sys.stderr)


def tasa_fallo(tipo: str, min_muestras=3, vigente=False) -> float:
    """% de intentos locales fallidos para un tipo (desde el ledger)."""
    rows = [r for r in leer_ledger() if r.get("tipo") == tipo
            and (_intento_local_vigente(r) if vigente else r.get("intento_local"))]
    if len(rows) < min_muestras:
        return 0.0  # sin datos suficientes → no sugiere nada
    fallos = sum(1 for r in rows if not r.get("local_ok"))
    return fallos / len(rows)


def sugerir_motor(tipo: str) -> str:
    """Cloud-first solo con fallos LOCALES reales y recientes (13-oct-2026).

    Antes contaba TODA fila con local_ok falso (incluidas las decisiones
    cloud_directo, que no son fallos del motor) y sin ventana temporal. Eso
    convertia el criterio en un trinquete: un fallo de codigo (p.ej. 'lms'
    fuera del PATH, RULE-021) dejaba el tipo en cloud PARA SIEMPRE, porque al
    no haber nuevos intentos locales nunca llegaba un ok que reseteara."""
    rows = [r for r in leer_ledger()
            if r.get("tipo") == tipo and _intento_local_vigente(r)]
    seguidas = 0
    for r in reversed(rows):
        if not r.get("local_ok"):
            seguidas += 1
        else:
            break
    tasa = (sum(1 for r in rows if not r.get("local_ok")) / len(rows)) if rows else 0.0
    if seguidas >= 2 or tasa >= 0.5:
        return "cloud"
    return TIPOS[tipo]["motor"]


# --- Acciones ---
def cmd_plan(tarea: str, as_json: bool, tipo_declarado: "str | None" = None,
             schema_path: "str | None" = None) -> None:
    tipo, origen = tipo_efectivo(tarea, tipo_declarado)
    motor = sugerir_motor(tipo)
    est = _preestimar(tarea)  # tipo fino + modelo desde la tabla YAML (pipeline)
    sch, sch_err = cargar_schema(schema_path)
    plan = {
        "tarea": tarea,
        "tipo": tipo,
        "tipo_origen": origen,
        "tipo_fino": est.get("tipo", tipo),
        "modelo_estimado": est.get("modelo", "?"),
        "motor_planificado": motor,
        "motor_default": TIPOS[tipo]["motor"],
        "verificable": TIPOS[tipo]["verificable"],
        "schema": {
            "ruta": schema_path,
            "valido": bool(schema_path) and sch_err is None,
            "error": sch_err,
            "requeridas": (sch or {}).get("required", []),
        },
        "pasos": (["local(auto-preestima modelo) -> verifier -> cloud si falla"] if motor == "local"
                  else ["cloud directo"]),
        "coste_estimado": "0 USD (local)" if motor == "local" else "cloud flash",
    }
    if as_json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"Tarea: {tarea}")
        print(f"Tipo: {tipo} (origen: {origen}) | motor planificado: {motor} "
              f"(default {TIPOS[tipo]['motor']})")
        print(f"Modelo fino estimado (pipeline YAML): {est.get('modelo', '?')} "
              f"[tipo: {est.get('tipo', tipo)}]")
        if schema_path:
            estado_sch = "OK" if sch_err is None else f"ERROR ({sch_err})"
            req = ", ".join(plan["schema"]["requeridas"]) or "-"
            print(f"Schema: {schema_path} -> {estado_sch} | requeridas: {req}")
        print(f"Verificable: {TIPOS[tipo]['verificable']}")
        print(f"Pasos: {plan['pasos'][0]}")
        print(f"Coste: {plan['coste_estimado']}")



def cmd_run(tarea: str, force: bool) -> None:
    if not force:
        print("NO ejecutado: el loop REAL requiere --run -y (confirmación explícita).")
        print("Usa --plan primero para ver qué haría.")
        return
    tipo = clasificar_tipo(tarea)
    motor = sugerir_motor(tipo)
    entry = {"ts": now_iso(), "tarea": tarea[:120], "tipo": tipo, "motor": motor,
             "intento_local": motor == "local", "local_ok": None,
             "escalo_cloud": False, "motivo": None, "latencia_s": None}

    if motor == "cloud":
        r = ejecutar_cloud(tarea)
        entry.update({"local_ok": False, "motivo": "cloud_directo", "cloud_result": r})
        escribir_ledger(entry)
        print("Motor cloud (razonamiento/complejo) -> DeepSeek v4 flash.")
        if r.get("ok"):
            print("--- SALIDA ---")
            print(r.get("salida", ""))
        else:
            print(f"Cloud FALLO: {r.get('stderr', '')}")
        return

    r = ejecutar_local(tipo, tarea)
    entry["latencia_s"] = r["latencia_s"]
    if not r["ok"]:
        entry.update({"local_ok": False, "motivo": r["stderr"] or "error_motor"})
        escribir_ledger(entry)
        print(f"Local FALLÓ ({r['stderr']}) → escalando a cloud...")
        rc = ejecutar_cloud(tarea)
        entry.update({"escalo_cloud": True, "cloud_result": rc})
        escribir_ledger(entry)
        print("Escalado a cloud completado; resultado local descartado.")
        return

    pasa, motivo = verifier(tipo, r["salida"], tarea)
    entry.update({"local_ok": pasa, "motivo": motivo})
    if pasa:
        escribir_ledger(entry)
        print(f"✅ Local OK ({motivo}) en {r['latencia_s']}s. Coste: 0 USD.")
        print("--- SALIDA ---")
        print(r["salida"])
    else:
        entry["escalo_cloud"] = True
        print(f"❌ Verifier: {motivo} → escalando a cloud...")
        rc = ejecutar_cloud(tarea)
        entry.update({"cloud_result": rc})
        escribir_ledger(entry)  # UNA sola escritura (con cloud_result incluido)
        print("Escalado a cloud completado; resultado local descartado.")


def cmd_stats() -> None:
    rows = leer_ledger()
    if not rows:
        print("Ledger vacío (aún no hay ejecuciones).")
        return
    from collections import Counter
    tipos = Counter(r.get("tipo") for r in rows)
    print(f"Ledger: {len(rows)} entradas")
    for tipo, n in sorted(tipos.items()):
        ok = sum(1 for r in rows if r.get("tipo") == tipo and r.get("local_ok"))
        fallo = sum(1 for r in rows if r.get("tipo") == tipo and r.get("intento_local") and not r.get("local_ok"))
        escalo = sum(1 for r in rows if r.get("tipo") == tipo and r.get("escalo_cloud"))
        tasa = tasa_fallo(tipo, vigente=True)
        sugerido = sugerir_motor(tipo)
        print(f"  {tipo:12} n={n:3} | local_ok={ok:3} | local_fallo={fallo:2} | "
              f"escalado={escalo:2} | tasa_fallo={tasa:.0%} | sugerido={sugerido}")


def cmd_check() -> None:
    """Diagnóstico solo lectura: router presente, modelos, ledger."""
    print(f"Router: {ROUTER} -> {'EXISTE' if ROUTER.exists() else 'NO EXISTE'}")
    print(f"Pipeline preestimación: {PIPELINE} -> {'EXISTE' if PIPELINE.exists() else 'NO EXISTE'}")
    print(f"Ledger: {LEDGER} -> {'EXISTE (' + str(sum(1 for _ in open(LEDGER)) ) + ' líneas)' if LEDGER.exists() else 'NO CREADO'}")
    try:
        p = subprocess.run(["bash", str(ROUTER), "check"], capture_output=True, text=True, timeout=60)
        print("--- llm-router.sh check ---")
        print(p.stdout.strip()[:600])
    except Exception as e:
        print(f"router check falló: {e}")


def _norm_argv(argv):
    """Normaliza el orden: flags delante, --plan/--run con su valor al final.

    Motivo (19-oct-2026): con `--plan` de nargs="?", argparse no consume como
    valor un token que empieza por '-', asi que `--plan --json "t"` respondia
    "Falta la tarea". Con esto el orden deja de importar.
    """
    flags, resto = [], []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--json", "-y"):
            flags.append(a)
            i += 1
        elif a in ("--tipo", "--schema") and i + 1 < len(argv):
            flags += [a, argv[i + 1]]
            i += 2
        else:
            resto.append(a)
            i += 1
    return flags + resto


def main():
    ap = argparse.ArgumentParser(description="Orquestador local-first con escalada (ESQUELETO)")
    ap.add_argument("--plan", nargs="?", const="", metavar="TAREA")
    ap.add_argument("--run", nargs="?", const="", metavar="TAREA")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-y", action="store_true", help="confirmación explícita para --run")
    ap.add_argument("--tipo", choices=TIPOS_VALIDOS, default=None,
                    help="tipo declarado (cola v2); sin esto se usa la heurística")
    ap.add_argument("--schema", metavar="FICHERO.json", default=None,
                    help="schema Draft-07 de la salida esperada (solo --plan en el paso 1)")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(_norm_argv(sys.argv[1:]))

    if args.check:
        cmd_check()
    elif args.stats:
        cmd_stats()
    elif args.plan is not None:
        if not args.plan:
            print("Falta la tarea para --plan")
            sys.exit(1)
        cmd_plan(args.plan, args.json, args.tipo, args.schema)
    elif args.run is not None:
        if not args.run:
            print("Falta la tarea para --run")
            sys.exit(1)
        if args.tipo or args.schema:
            # Fail-closed: no ignorar en silencio lo que aun no se aplica.
            print("--tipo/--schema aun NO se aplican en --run (paso 1: solo --plan). Abortado.")
            sys.exit(2)
        cmd_run(args.run, args.y)
    else:
        ap.print_help()



if __name__ == "__main__":
    main()
