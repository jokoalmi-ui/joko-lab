#!/usr/bin/env python3
"""
pipeline_seleccion_modelo.py — Preestimación + carga automática de modelo por tarea.

Resuelve: «¿se puede determinar QUÉ modelo se necesita ANTES de cargarlo?»
→ SÍ: se clasifica la tarea (keywords) contra la tabla fuente única
  (01-knowledge/modelos_por_tarea.yaml) y se carga automáticamente el modelo
  ganador si no está ya en memoria (o se hace swap si hay otro cargado).

USO (todo local, 0 €):
  python3 pipeline_seleccion_modelo.py --check "describe la tarea"
      → SOLO estima y muestra qué modelo haría falta. NO toca LM Studio.
  python3 pipeline_seleccion_modelo.py --run "describe la tarea"
      → estima Y carga automáticamente el modelo (swap si otro ocupa VRAM).
  python3 pipeline_seleccion_modelo.py --estado
      → qué modelo está cargado ahora en :1234.
  python3 pipeline_seleccion_modelo.py --tipos
      → lista los tipos de tarea conocidos de la tabla.

MODO SEGURO: el default es --check (solo lectura). --run es la única vía
que modifica el estado de LM Studio y exige confirmación explícita.

Fuentes:
  - Tabla de decisión: /home/jokoalmi/joko-lab/01-knowledge/modelos_por_tarea.yaml
  - Modelos instalados: `~/.lmstudio/bin/lms ls`
  - Estado de carga: GET http://localhost:1234/api/v0/models
  - Ledger de decisiones: /home/jokoalmi/joko-lab/04-operations/metrics/pipeline_seleccion_ledger.jsonl
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

LAB = "/home/jokoalmi/joko-lab"
TABLA = os.path.join(LAB, "01-knowledge", "modelos_por_tarea.yaml")
LEDGER = os.path.join(LAB, "04-operations", "metrics", "pipeline_seleccion_ledger.jsonl")
LMS = "/home/jokoalmi/.lmstudio/bin/lms"
LMSTUDIO_URL = "http://localhost:1234/api/v0/models"

TZ = timezone(timedelta(hours=2))  # CEST


def now_iso():
    return datetime.now(TZ).isoformat(timespec="seconds")


# ---------------------------------------------------------------- YAML mínimo
def load_yaml(path):
    """Carga la tabla de decisión YAML con PyYAML (disponible en el sistema)."""
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------- estado LM Studio
def modelo_cargado():
    """Devuelve id del modelo cargado en :1234, o None."""
    try:
        req = urllib.request.Request(LMSTUDIO_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode())
        loaded = [m.get("id") for m in data.get("data", []) if m.get("state") == "loaded"]
        return loaded[0] if loaded else None
    except Exception:
        return "server_off"


def lms_ls():
    """Ids de modelos instalados según el CLI real."""
    try:
        out = subprocess.run([LMS, "ls"], capture_output=True, text=True, timeout=25).stdout
        return out
    except Exception as e:
        return f"error: {e}"


# ----------------------------------------------------------------- clasificación
def _normalizar(t):
    """Minúsculas + quitar acentos para que 'conversación' matchee 'conversacion'."""
    import unicodedata
    t = t.lower()
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return t


def detectar_tipo(texto, tabla):
    texto_l = " " + _normalizar(texto) + " "
    tipos = tabla.get("modelos_por_tarea", {})
    coincidencias = []
    for tipo, cfg in tipos.items():
        claves = cfg.get("cuando", [])
        if not isinstance(claves, list):
            continue
        golpes = 0
        for c in claves:
            c_l = _normalizar(c).strip()
            if c_l and c_l in texto_l:
                golpes += 1
        if golpes:
            coincidencias.append((golpes, tipo))
    if not coincidencias:
        return "fallback", tabla.get("fallback", {})
    coincidencias.sort(key=lambda x: -x[0])
    tipo = coincidencias[0][1]
    return tipo, tipos[tipo]


def clasificar_tipo_generico(texto):
    """Detecta tipo genérico de la tarea (sin depender de la tabla) — usado solo
    para el registro en el ledger; la decisión de modelo la hace detectar_tipo."""
    t = _normalizar(texto)
    if any(p in t for p in ["imagen", "foto", "screenshot", "captura", "ve esta", "visual"]):
        return "vision"
    if any(p in t for p in ["json", "extrae", "clasifica", "codigo", "funcion", "script"]):
        return "batch-json"
    if any(p in t for p in ["razon", "logica", "paso a paso", "analiza"]):
        return "razonamiento"
    if any(p in t for p in ["hecho", "verdad", "inventado", "alucina", "fiable", "es cierto"]):
        return "veracidad"
    if any(p in t for p in ["informe", "resumen", "redacta", "ficha", "describe"]):
        return "redaccion"
    return "no_detectado"


# -------------------------------------------------------------------- acciones
def cargar_modelo(cadena, confirmado):
    """Carga el PRIMER modelo de `cadena` que se deje cargar.

    `cadena` = id o lista de ids (principal + alternativas, EN ORDEN). Si un load falla,
    prueba el siguiente. Antes se rendía al primer fallo y la tarea se quedaba sin motor.
    """
    if isinstance(cadena, str):
        cadena = [cadena]
    if not confirmado:
        return {"ok": False, "motivo": "requiere_confirmacion_explicita"}
    pasos = []
    for i, modelo_id in enumerate(cadena):
        actual = modelo_cargado()
        if actual and actual != modelo_id and actual not in ("server_off",):
            r = subprocess.run([LMS, "unload", actual], capture_output=True, text=True, timeout=120)
            pasos.append({"accion": "unload", "modelo": actual, "rc": r.returncode,
                          "salida": (r.stdout or r.stderr).strip()[-300:]})
            time.sleep(2)
        r = subprocess.run([LMS, "load", modelo_id], capture_output=True, text=True, timeout=180)
        pasos.append({"accion": "load", "modelo": modelo_id, "rc": r.returncode,
                      "salida": (r.stdout or r.stderr).strip()[-300:]})
        time.sleep(3)
        tras = modelo_cargado()
        if r.returncode == 0 and tras == modelo_id:
            return {"ok": True, "pasos": pasos, "cargado": tras, "cadena": cadena,
                    "intento": i + 1, "alternativa_usada": i > 0}
        pasos.append({"accion": "descartado", "modelo": modelo_id,
                      "motivo": f"rc={r.returncode} cargado={tras}"})
    return {"ok": False, "pasos": pasos, "cargado": modelo_cargado(), "cadena": cadena}


def cadena_de(cfg):
    """[modelo principal] + `alternativas` del bucket, en orden, sin nulos ni repetidos."""
    ids = []
    for m in [cfg.get("modelo")] + list(cfg.get("alternativas") or []):
        if m and m not in ids:
            ids.append(m)
    return ids


# ----------------------------------------------------------------------- ledger
def registrar(entrada):
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[aviso] no se pudo escribir ledger: {e}", file=sys.stderr)


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Preestima y carga modelo por tarea (LM Studio local).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", metavar="TAREA", help="SOLO estima (no toca LM Studio)")
    g.add_argument("--run", metavar="TAREA", help="Estima Y carga automáticamente (pide confirmación)")
    g.add_argument("--estado", action="store_true", help="Modelo cargado ahora en :1234")
    g.add_argument("--tipos", action="store_true", help="Tipos de tarea conocidos")
    ap.add_argument("--force", action="store_true", help="--run sin confirmación interactiva (solo si sabes)")
    ap.add_argument("--json", action="store_true", help="Salida JSON compacta (para integrar con llm-router.sh auto)")
    args = ap.parse_args()

    if args.estado:
        cargado = modelo_cargado()
        print(f"modelo_cargado: {cargado}")
        return

    tabla = load_yaml(TABLA)
    if args.tipos:
        print("Tipos de tarea conocidos (modelos_por_tarea.yaml):")
        for tipo, cfg in tabla.get("modelos_por_tarea", {}).items():
            if cfg.get("modelo"):
                m = cfg["modelo"]
            elif cfg.get("herramienta"):
                m = f"FUERA DE LM STUDIO ({cfg['herramienta']})"
            else:
                m = "(cloud)"
            alts = cfg.get("alternativas") or []
            extra = f"   [alternativas: {' → '.join(alts)}]" if alts else ""
            print(f"  - {tipo}: {m}{extra}")
        fb = tabla.get("fallback", {})
        print(f"  - fallback: {fb.get('modelo')}")
        return

    texto = args.check or args.run
    tipo, cfg = detectar_tipo(texto, tabla)
    modelo_id = cfg.get("modelo")
    evidencia = cfg.get("evidencia", "sin evidencia registrada")
    prioridad = cfg.get("prioridad", "balance")
    herramienta = cfg.get("herramienta")
    cadena = cadena_de(cfg)
    fuera = bool(herramienta) and not cfg.get("cloud")

    def entrada_base(t):
        return {
            "ts": now_iso(),
            "tarea": t[:180],
            "tipo": tipo,
            "tipo_generico": clasificar_tipo_generico(t),
            "modelo_estimado": modelo_id,
            "fuente": "modelos_por_tarea.yaml",
        }

    cargado = modelo_cargado()
    decision = {
        "tipo": tipo,
        "modelo": modelo_id if modelo_id else ("cloud" if cfg.get("cloud", True) else None),
        "prioridad": prioridad,
        "evidencia": evidencia,
        "cargado_ahora": cargado,
        "local": bool(modelo_id),
        "alternativas": cadena[1:] if modelo_id else list(cfg.get("alternativas") or []),
        "fuera_de_lmstudio": fuera,
        "herramienta": herramienta,
    }

    if args.json:
        # Salida JSON compacta para integrar con llm-router.sh auto (una línea)
        registrar({**entrada_base(texto), **decision, "modo": "json"})
        print(json.dumps(decision, ensure_ascii=False))
        return

    print(f"tipo_detectado: {tipo}")
    if modelo_id:
        print(f"modelo_estimado: {modelo_id}")
        if len(cadena) > 1:
            print(f"alternativas:    {' → '.join(cadena[1:])}")
    elif fuera:
        print(f"modelo_estimado: FUERA DE LM STUDIO → usar {herramienta} (no se carga nada)")
    else:
        print("modelo_estimado: (cloud, no tocar LM Studio)")
    print(f"prioridad: {prioridad}")
    print(f"evidencia: {evidencia}")

    entrada = entrada_base(texto)

    if args.check:
        if modelo_id:
            ya = "YA cargado ✅" if cargado == modelo_id else (
                "NO cargado (habría que cargar)" if cargado in (None, "server_off") else f"otro cargado: {cargado} (habría swap)")
            print(f"estado_actual: {ya}")
            entrada["estado_actual"] = cargado
        registrar(entrada)
        print("\n[check] No se ha modificado LM Studio. Usa --run para cargar automáticamente.")
        return

    # --run
    if not modelo_id:
        if fuera:
            print(f"\n[run] Tarea FUERA de LM Studio → corresponde a {herramienta}. No se toca LM Studio.")
        else:
            print("\n[run] Tarea clasificada como cloud/interactiva → NO se toca LM Studio.")
        entrada["accion"] = "no_local"
        registrar(entrada)
        return

    if not args.force:
        print("\n[confirmación] Para cargar automáticamente se necesita OK explícito.")
        print("  Opciones: 1) ejecuta con --force  (solo si ya lo autorizaste)")
        print("  O 2) dime «hazlo» y lo lanzo con --force desde la sesión.")
        entrada["accion"] = "espera_confirmacion"
        registrar(entrada)
        return

    print(f"\n[run] Cadena de carga: {' → '.join(cadena)}")
    print("[run] Cargando modelo automáticamente (si el primero falla, prueba la alternativa)...")
    res = cargar_modelo(cadena, confirmado=True)
    entrada["accion"] = "carga_automatica"
    entrada["cadena"] = cadena
    entrada["resultado"] = res
    registrar(entrada)
    print(json.dumps({k: v for k, v in res.items() if k != "pasos"}, ensure_ascii=False, indent=2))
    for p in res.get("pasos", []):
        if "rc" in p:
            print(f"  → {p['accion']} {p['modelo']}: rc={p['rc']} {p['salida']}")
        else:
            print(f"  → {p['accion']} {p['modelo']}: {p['motivo']}")


if __name__ == "__main__":
    main()
