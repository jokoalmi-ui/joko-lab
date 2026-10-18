#!/usr/bin/env python3
"""
agentic_loop.py — EVALUATE determinista del Agentic RAG Loop (Fase 1)

Diseño: references/agentic-rag-loop-20260804.md (skill local-rag)
Fase 1: encapsular EVALUATE (cobertura + vigencia) para NO depender del
criterio del LLM en cada iteración del loop.

Qué hace:
  1. RETRIEVE: ejecuta search.py (subprocess, venv hermes-rag) para obtener
     los paths recuperados para una query.
  2. EVALUATE cobertura: aplica el evaluador de verification/comparador.py
     (completitud_parcial / keywords / numerico) sobre el TEXTO COMPLETO de
     los archivos recuperados. Si evaluar(item, texto) es True, la
     información que exige el item está en lo recuperado.
  3. EVALUATE vigencia: para cada path recuperado que sea un Knowledge Object
     (01-knowledge/objects/*.yaml), lee status / expires / superseded_by y
     marca advertencias si el documento recuperado NO es el vigente.
  4. Cobertura de FUENTES: compara los paths esperados del item (campo
     `fuente` del banco) contra los paths recuperados.
  5. REFORMULATE determinista: si faltan keywords, añade las que faltan a la
     query y reintenta (máx --max-iter). Criterio de parada: cobertura OK o
     agotadas las iteraciones.

Modos:
  --query: query libre + --requiere (keywords) + --prohibido (opcional).
  --bank: evaluar un item del banco (bank.yaml) por --item ID: usa la
          pregunta, respuesta_esperada, prohibido y fuente del item.

Salida: legible por defecto; --json para la medición (Fase 3 clásico vs
agentic con aciertos + tokens, sin tocar nada).

Solo lectura: no modifica índices, KOs ni banco. search.py registra telemetría
en rag-query-ledger.jsonl (comportamiento normal del pipeline).
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "joko-lab"
SEARCH_PY = VAULT / "tools" / "search.py"
VENV_PY = Path.home() / ".venv" / "hermes-rag" / "bin" / "python3"
VERIFICATION_DIR = VAULT / "verification"
OBJECTS_DIR = VAULT / "01-knowledge" / "objects"
DEFAULT_BANK = VERIFICATION_DIR / "bank.yaml"
MAX_CHARS_POR_ARCHIVO = 50_000

# Asegurar import del comparador (mismo directorio que el banco)
if str(VERIFICATION_DIR) not in sys.path:
    sys.path.insert(0, str(VERIFICATION_DIR))
try:
    from comparador import evaluar, normalizar, contiene_palabra
except ImportError as e:
    print(f"ERROR: no se pudo importar verification/comparador.py: {e}", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────── RECUPERACIÓN ───────────────────────────

def recuperar(query: str, top_k: int = 5) -> list:
    """Ejecuta search.py y devuelve la lista de paths recuperados (relativos al vault)."""
    cmd = [str(VENV_PY), str(SEARCH_PY), "--query", query, "--top_k", str(top_k)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    paths = []
    for linea in proc.stdout.splitlines():
        # Formato real de search.py: "[1] 01-knowledge/objects/RULE-003.yaml  (cos: ...)"
        m = re.match(r"^\[\d+\]\s+(\S+)\s+\(cos:", linea.strip())
        if m:
            paths.append(m.group(1))
    return paths


def leer_texto(path_relativo: str) -> str:
    """Lee el archivo completo del vault (truncado por seguridad) como texto."""
    ruta = VAULT / path_relativo
    if not ruta.exists():
        return ""
    try:
        datos = ruta.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    return datos[:MAX_CHARS_POR_ARCHIVO]


def texto_concatenado(paths: list) -> str:
    """Concatena los textos de los paths recuperados, separados por marcador."""
    trozos = []
    for p in paths:
        txt = leer_texto(p)
        if txt:
            trozos.append(f"=== {p} ===\n{txt}")
    return "\n\n".join(trozos)


# ─────────────────────────── VIGENCIA ───────────────────────────

def _motivo_no_vigente(ko: dict, hoy: datetime.date) -> str | None:
    """Devuelve el motivo de no vigencia de un KO, o None si está vigente.
    Comprueba status, expires y superseded_by (en ese orden)."""
    status = str(ko.get("status", "")).strip().lower()
    if status and status != "activo":
        return f"status={status}"
    expires = ko.get("expires")
    if expires:
        try:
            if datetime.fromisoformat(str(expires)).date() < hoy:
                return f"expires={expires} (pasada)"
        except ValueError:
            pass
    superseded = ko.get("superseded_by")
    if superseded:
        return f"superseded_by={superseded}"
    return None


def evaluar_vigencia(paths: list) -> list:
    """Para KOs recuperados, comprueba status/expires/superseded_by.

    Devuelve lista de dicts: {path, vigente, motivo}.
    Un KO se marca NO vigente si status != 'activo', expires ya pasada, o
    superseded_by no vacío.
    """
    import yaml

    hoy = datetime.now().date()
    advertencias = []
    for p in paths:
        ruta = VAULT / p
        if not (ruta.exists() and ruta.suffix in (".yaml", ".yml") and "objects" in p):
            continue
        try:
            ko = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(ko, dict):
            continue
        motivo = _motivo_no_vigente(ko, hoy)
        advertencias.append({
            "path": p,
            "vigente": motivo is None,
            "motivo": motivo,
        })
    return advertencias


# ─────────────────────────── COBERTURA ───────────────────────────

def evaluar_cobertura(item: dict, paths: list) -> dict:
    """Cobertura sobre el texto COMPLETO de lo recuperado.

    - keywords: evaluar(item, texto) de comparador (completitud_parcial /
      keywords_obligatorias / numerico) sobre el texto concatenado.
    - fuentes: qué paths esperados del item (campo `fuente`, puede ser
      'A.yaml + B.yaml') están entre los recuperados.
    """
    texto = texto_concatenado(paths)
    try:
        cobertura_ok = evaluar(item, texto)
    except Exception as e:
        cobertura_ok = False

    # Detalle por keyword (para reformular con las que faltan)
    esperadas = item.get("respuesta_esperada", [])
    if isinstance(esperadas, (int, float)):
        esperadas = [str(esperadas)]
    if isinstance(esperadas, str):
        esperadas = [esperadas]
    faltantes = []
    texto_norm = normalizar(texto)
    for kw in esperadas:
        if not contiene_palabra(texto_norm, normalizar(str(kw))):
            faltantes.append(str(kw))

    # Cobertura de fuentes. El banco a veces abrevia la 2ª fuente
    # (ej: "01-knowledge/objects/RULE-003.yaml + DEC-002.yaml"): comparar
    # también por nombre de archivo, no solo por ruta exacta.
    fuente = item.get("fuente", "")
    esperadas_fuentes = [f.strip() for f in re.split(r"\s*\+\s*", fuente) if f.strip()]
    nombres_recuperados = [Path(p).name for p in paths]
    encontradas_fuentes = [f for f in esperadas_fuentes
                           if f in paths or Path(f).name in nombres_recuperados]

    return {
        "cobertura_ok": cobertura_ok,
        "faltantes": faltantes,
        "fuentes_esperadas": esperadas_fuentes,
        "fuentes_encontradas": encontradas_fuentes,
        "fuentes_completas": len(encontradas_fuentes) == len(esperadas_fuentes),
    }


# ─────────────────────────── LOOP ───────────────────────────

def ejecutar_loop(item: dict, top_k: int = 5, max_iter: int = 3) -> dict:
    """PLAN→RETRIEVE→EVALUATE→(REFORMULATE)→SYNTHESIZE determinista.

    PLAN es externo (el agente decide la query); aquí la query inicial es la
    pregunta del item. La reformulación es determinista: añadir keywords
    faltantes a la query (el FTS las capta mejor). Criterios de parada del
    diseño: cobertura OK, o máx 3 iteraciones.
    """
    query = item["pregunta"]
    iteraciones = []
    resultado_final = None

    for i in range(1, max_iter + 1):
        paths = recuperar(query, top_k)
        cobertura = evaluar_cobertura(item, paths)
        vigencia = evaluar_vigencia(paths)
        iteraciones.append({
            "iteracion": i,
            "query": query,
            "paths": paths,
            "cobertura": cobertura,
            "vigencia": vigencia,
        })
        if cobertura["cobertura_ok"]:
            resultado_final = {
                "parada": "cobertura_ok",
                "iteraciones": i,
            }
            break
        faltantes = cobertura["faltantes"]
        if faltantes:
            # Reformulación determinista: la keyword faltante pasa a la query
            query = f"{query} {' '.join(faltantes)}"
        else:
            # Keywords OK pero fuentes incompletas: reformular con la fuente que falta
            faltantes_fuente = [f for f in cobertura["fuentes_esperadas"]
                                if f not in cobertura["fuentes_encontradas"]]
            if faltantes_fuente:
                query = f"{query} {' '.join(faltantes_fuente)}"
            else:
                resultado_final = {
                    "parada": "sin_progreso_posible",
                    "iteraciones": i,
                }
                break
    else:
        resultado_final = {
            "parada": "max_iteraciones",
            "iteraciones": max_iter,
        }

    return {
        "item_id": item.get("id", "?"),
        "pregunta": item["pregunta"],
        "top_k": top_k,
        "max_iter": max_iter,
        "parada": resultado_final["parada"],
        "iteraciones_usadas": resultado_final["iteraciones"],
        "ultima_cobertura": iteraciones[-1]["cobertura"],
        "ultima_vigencia": iteraciones[-1]["vigencia"],
        "iteraciones": iteraciones,
    }


# ─────────────────────────── BANCO ───────────────────────────

def cargar_item_banco(ruta_bank, item_id):
    import yaml

    with open(ruta_bank, "r", encoding="utf-8") as f:
        banco = yaml.safe_load(f)
    for item in banco:
        if item.get("id") == item_id:
            return item
    print(f"ERROR: item '{item_id}' no existe en {ruta_bank}", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────── SALIDA ───────────────────────────

def _imprimir_fuentes(ult: dict):
    """Imprime el bloque de fuentes: encontradas ✓ y esperadas no recuperadas ✗."""
    print(f"Fuentes: {len(ult['fuentes_encontradas'])}/{len(ult['fuentes_esperadas'])} "
          f"({ult['fuentes_esperadas']})")
    if ult["fuentes_encontradas"]:
        for f in ult["fuentes_encontradas"]:
            print(f"  ✓ {f}")
    for f in [x for x in ult["fuentes_esperadas"] if x not in ult["fuentes_encontradas"]]:
        print(f"  ✗ {f} (no recuperada)")


def _imprimir_vigencia(resultado: dict):
    """Imprime los KOs recuperados no vigentes (⚠ con motivo)."""
    no_vigentes = [v for v in resultado["ultima_vigencia"] if not v["vigente"]]
    if no_vigentes:
        print("Vigencia:")
        for v in no_vigentes:
            print(f"  ⚠ {v['path']} NO vigente ({v['motivo']})")


def imprimir_informe(resultado: dict):
    ult = resultado["ultima_cobertura"]
    print(f"\n=== Agentic RAG Loop — EVALUATE (Fase 1) ===")
    print(f"Item:    {resultado['item_id']}")
    print(f"Pregunta: {resultado['pregunta']}")
    print(f"Parada:  {resultado['parada']} ({resultado['iteraciones_usadas']} iteración/iteraciones)")
    print(f"Cobertura final: {'OK' if ult['cobertura_ok'] else 'INCOMPLETA'}")
    if ult["faltantes"]:
        print(f"  Keywords faltantes: {ult['faltantes']}")
    _imprimir_fuentes(ult)
    _imprimir_vigencia(resultado)
    print("\nIteraciones:")
    for it in resultado["iteraciones"]:
        print(f"  [{it['iteracion']}] {it['query'][:90]}")
        for p in it["paths"]:
            print(f"       {p}")


def main():
    parser = argparse.ArgumentParser(description="EVALUATE determinista del Agentic RAG Loop (Fase 1)")
    parser.add_argument("--query", help="Query libre (modo manual)")
    parser.add_argument("--requiere", action="append", default=[],
                        help="Keyword obligatoria (repetible). Solo con --query.")
    parser.add_argument("--prohibido", action="append", default=[],
                        help="Keyword prohibida (repetible). Solo con --query.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK), help="Ruta al banco YAML")
    parser.add_argument("--item", help="ID del item del banco (ej: EXP3-001)")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-iter", type=int, default=3)
    parser.add_argument("--json", action="store_true", help="Salida JSON (para medición Fase 3)")
    args = parser.parse_args()

    if args.item:
        item = cargar_item_banco(args.bank, args.item)
    elif args.query:
        if not args.requiere:
            print("ERROR: con --query hace falta al menos un --requiere", file=sys.stderr)
            sys.exit(1)
        item = {
            "id": "MANUAL",
            "pregunta": args.query,
            "tipo": "completitud_parcial",
            "respuesta_esperada": args.requiere,
            "prohibido": args.prohibido,
            "fuente": "",
        }
    else:
        parser.print_help()
        sys.exit(1)

    resultado = ejecutar_loop(item, top_k=args.top_k, max_iter=args.max_iter)
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        imprimir_informe(resultado)


if __name__ == "__main__":
    main()
