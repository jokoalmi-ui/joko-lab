#!/usr/bin/env python3
"""
Evidence Contract — Verificador de promoción EXP→DEC.
Solo lectura. No modifica nada.

Implementa el contrato definido en:
    lpa/contracts/evidence-contract.md

Verifica que un Knowledge Object cumpla los umbrales mínimos
antes de que pueda promocionarse a DEC (o RULE/POLICY/PATTERN).

Uso:
    python3 evidence_contract.py                          # verifica TODOS los KOs
    python3 evidence_contract.py DEC-001                  # verifica uno
    python3 evidence_contract.py --json                   # salida JSON
    python3 evidence_contract.py --json DEC-001 RULE-001  # varios, JSON
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

LAB_ROOT = Path.home() / "joko-lab"
OBJECTS_DIR = LAB_ROOT / "01-knowledge" / "objects"

# Umbrales por tipo (fuente: lpa/contracts/evidence-contract.md)
CONTRACT = {
    "DEC":    {"minimum_experiments": 2, "minimum_independent_review": 1,
               "minimum_contradictory_tests": 1, "minimum_confidence": 0.80},
    "RULE":   {"minimum_experiments": 2, "minimum_independent_review": 1,
               "minimum_contradictory_tests": 1, "minimum_confidence": 0.85},
    "POLICY": {"minimum_experiments": 1, "minimum_independent_review": 2,
               "minimum_contradictory_tests": 1, "minimum_confidence": 0.90},
    "PATTERN":{"minimum_experiments": 3, "minimum_independent_review": 1,
               "minimum_contradictory_tests": 2, "minimum_confidence": 0.70},
}

# Aliases tolerantes (inglés/español) para campos del KO
FIELD_ALIASES = {
    "evidence": ["evidence", "evidencia", "evidencias", "experiments", "experimentos"],
    "independent_reviews": ["independent_reviews", "independent_review", "reviews",
                            "revisiones", "revision_independiente", "revisores"],
    "falsification_attempts": ["falsification_attempts", "falsification", "falsacion",
                               "falsificación", "contradictory_tests", "intentos_falsacion"],
    "confidence": ["confidence", "confianza"],
}


def _procesar_linea_clave(stripped: str, result: dict, current_key: str, current_list: list):
    """Procesa una línea sin indentar (clave o clave: valor).
    Devuelve (current_key, current_list) actualizados."""
    if current_key and current_list:
        result[current_key] = current_list
        current_list = []
    if ":" in stripped:
        current_key = stripped.split(":")[0].strip()
        rest = ":".join(stripped.split(":")[1:]).strip()
        if rest:
            result[current_key] = _parse_value(rest)
        else:
            current_key = current_key
    return current_key, current_list


def _parse_yaml_simple(text: str) -> dict:
    """Parser YAML mínimo para KOs simples (sin librería externa)."""
    result = {}
    current_key = None
    current_list = []
    in_list = False
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and not line.startswith("\t"):
            in_list = False
            current_key, current_list = _procesar_linea_clave(
                stripped, result, current_key, current_list)
        elif stripped.startswith("- "):
            in_list = True
            current_list.append(_parse_value(stripped[2:]))
    if current_key and current_list:
        result[current_key] = current_list
    return result


def _parse_value(v: str):
    v = v.strip().strip('"').strip("'")
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v.lower() == "null" or v.lower() == "none":
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def load_ko(path: Path) -> dict:
    """Carga un Knowledge Object (YAML plano o YAML con frontmatter)."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if yaml:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    return _parse_yaml_simple(text)


def _first_present(ko: dict, keys: list):
    """Devuelve (valor, clave_encontrada) para la primera clave presente."""
    for k in keys:
        if k in ko and ko[k] is not None:
            return ko[k], k
    return None, None


def _count_evidence(val) -> int:
    """Cuenta evidencia: lista → len; str → 1 si no vacío; int → valor."""
    if val is None:
        return 0
    if isinstance(val, list):
        return len([e for e in val if e])
    if isinstance(val, str):
        return 1 if val.strip() else 0
    if isinstance(val, (int, float)):
        return int(val)
    return 0


def _chequear_minimo(valor, minimo, campo, tiene, requiere, missing, notes, campo_ausente, ausente_a_missing=False):
    """Patrón común: si valor < mínimo → missing; si el campo no existe → nota
    (o missing si ausente_a_missing=True, como exige el caso evidence)."""
    if valor < minimo:
        missing.append(f"faltan {minimo - valor} {campo} "
                       f"(tiene {valor}, requiere {minimo})")
    elif not tiene:
        destino = missing if ausente_a_missing else notes
        destino.append(campo_ausente)


def verify_ko(ko: dict) -> dict:
    """
    Verifica un KO contra el Evidence Contract.
    Devuelve dict con: id, type, thresholds, actual, passed, missing, notes
    """
    ko_id = ko.get("id", "?")
    ktype = ko.get("type", "").upper()
    if ktype not in CONTRACT:
        return {
            "id": ko_id, "type": ktype, "passed": False,
            "status": ko.get("status", "unknown"),
            "missing": [f"tipo '{ktype}' no contemplado en el contrato"],
            "notes": ["Tipo no verificable"],
        }

    thr = CONTRACT[ktype]

    evidence_val, ev_key = _first_present(ko, FIELD_ALIASES["evidence"])
    reviews_val, rev_key = _first_present(ko, FIELD_ALIASES["independent_reviews"])
    fals_val, fals_key = _first_present(ko, FIELD_ALIASES["falsification_attempts"])
    conf_val, conf_key = _first_present(ko, FIELD_ALIASES["confidence"])

    evidence_count = _count_evidence(evidence_val)
    reviews_count = _count_evidence(reviews_val)
    fals_count = _count_evidence(fals_val)
    confidence = float(conf_val) if isinstance(conf_val, (int, float)) else None

    actual = {
        "evidence_count": evidence_count,
        "independent_reviews": reviews_count,
        "falsification_attempts": fals_count,
        "confidence": confidence,
    }

    missing = []
    notes = []

    _chequear_minimo(evidence_count, thr["minimum_experiments"], "experimento(s)",
                     ev_key, evidence_count, missing, notes, "sin campo evidence",
                     ausente_a_missing=True)
    _chequear_minimo(reviews_count, thr["minimum_independent_review"], "revisión(es) independiente(s)",
                     rev_key, reviews_count, missing, notes,
                     "campo independent_reviews ausente → contado como 0")
    _chequear_minimo(fals_count, thr["minimum_contradictory_tests"], "test(s) de falsación",
                     fals_key, fals_count, missing, notes,
                     "campo falsification_attempts ausente → contado como 0")

    if confidence is None:
        missing.append(f"sin confidence (requiere >= {thr['minimum_confidence']})")
    elif confidence < thr["minimum_confidence"]:
        missing.append(f"confidence {confidence} < umbral {thr['minimum_confidence']}")

    # Dependencias como evidencia transitiva (solo nota informativa, no satisface el contrato)
    deps = ko.get("dependencies") or []
    if deps and evidence_count == 0:
        notes.append(f"tiene {len(deps)} dependencia(s) (evidencia transitiva posible, "
                     "no cuenta como experimento en el contrato)")

    passed = len(missing) == 0

    return {
        "id": ko_id,
        "type": ktype,
        "status": ko.get("status", "unknown"),
        "thresholds": thr,
        "actual": actual,
        "passed": passed,
        "missing": missing,
        "notes": notes,
        "field_keys": {"evidence": ev_key, "reviews": rev_key,
                       "falsation": fals_key, "confidence": conf_key},
    }


def verify_all() -> list:
    results = []
    if not OBJECTS_DIR.exists():
        return results
    for f in sorted(OBJECTS_DIR.glob("*.yaml")):
        ko = load_ko(f)
        if ko:
            results.append(verify_ko(ko))
    return results


def print_report(results: list) -> None:
    now = datetime.now().isoformat()[:16]
    print("=" * 66)
    print("EVIDENCE CONTRACT — Verificación de promoción EXP→DEC")
    print(f"Fecha: {now} | Contrato: lpa/contracts/evidence-contract.md")
    print("=" * 66)
    if not results:
        print("No hay Knowledge Objects para verificar.")
        return

    passed_n = sum(1 for r in results if r["passed"])
    print(f"\nCumplen el contrato: {passed_n}/{len(results)}\n")
    print("Nota (decision 02-09-2026): los KOs existentes son LEGACY — este contrato es")
    print("gate de PROMOCION EXP→DEC para KOs NUEVOS; no se re-verifican retroactivamente.")
    print("El 0/N es informativo y NO penaliza el Health Score (deuda conocida desde 31-07-2026).\n")

    for r in results:
        mark = "✅" if r["passed"] else "❌"
        print(f"{mark} {r['id']} ({r['type']}, {r.get('status', '?')})")
        a = r.get("actual")
        if a is not None:
            print(f"    evidence={a['evidence_count']} reviews={a['independent_reviews']} "
                  f"falsacion={a['falsification_attempts']} confidence={a['confidence']}")
        if r.get("missing"):
            print("    FALTA:")
            for m in r["missing"]:
                print(f"      - {m}")
        for n in r.get("notes", []):
            print(f"    nota: {n}")
    print("=" * 66)
    print("Un KO que no cumple NO puede promocionarse. El contrato decide, no la opinión.")


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    targets = [a for a in args if not a.startswith("--")]

    if targets:
        results = []
        for t in targets:
            # Aceptar con o sin extensión
            path = OBJECTS_DIR / (t if t.endswith(".yaml") else t + ".yaml")
            ko = load_ko(path)
            if ko:
                results.append(verify_ko(ko))
            else:
                results.append({"id": t, "type": "?", "passed": False,
                                "missing": [f"no encontrado en {OBJECTS_DIR}"],
                                "notes": [], "status": "?"})
    else:
        results = verify_all()

    if as_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_report(results)


if __name__ == "__main__":
    main()
