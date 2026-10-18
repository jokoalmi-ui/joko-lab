#!/usr/bin/env python3
"""debt_detector.py — Detección automática de deuda técnica en conocimiento

6 checks:
  ALTA:  huérfano (RULE sin DEC origen), huerfano DEC (referencia EXP inexistente)
  MEDIA: conflicto (2+ RULEs misma tarea), sin_validar (>180d), version_antigua
  BAJA:  no_usado (RULE activa nunca invocada en 90d)

Uso:
  python3 debt_detector.py --full
  python3 debt_detector.py --check huerfano
"""

import os, sys, yaml
from datetime import datetime, timedelta
from pathlib import Path

LAB_DIR = os.path.expanduser("~/joko-lab")
RULES_DIR = os.path.join(LAB_DIR, "01-knowledge", "rules")
DECISIONS_DIR = os.path.join(LAB_DIR, "01-knowledge", "decisions")
EXPERIMENTS_DIR = os.path.join(LAB_DIR, "01-knowledge", "experiments")
MODELS_DIR = os.path.join(LAB_DIR, "01-knowledge", "models")


def load_yaml_dir(directory: str) -> dict:
    """Carga todos los YAML de un directorio."""
    items = {}
    if not os.path.isdir(directory):
        return items
    for fname in os.listdir(directory):
        if fname.endswith((".yaml", ".yml")):
            try:
                with open(os.path.join(directory, fname)) as f:
                    items[fname] = yaml.safe_load(f)
            except Exception:
                pass
    return items


def list_ids(directory: str, prefix: str) -> set:
    """Lista IDs (ej: DEC-003) en un directorio."""
    ids = set()
    if not os.path.isdir(directory):
        return ids
    for fname in os.listdir(directory):
        # Buscar IDs en nombres de archivo
        for part in fname.replace(".yaml", "").replace(".yml", "").replace(".md", "").split("-"):
            if part.startswith(prefix) and len(part) > len(prefix):
                ids.add(fname)
    return ids


# ─── CHECKS ────────────────────────────────────────────

def check_huerfano_rules(rules: dict) -> list:
    """RULEs cuyo origen (DEC/EXP) no existe."""
    issues = []
    existing_decs = list_ids(DECISIONS_DIR, "DEC")
    existing_exps = list_ids(EXPERIMENTS_DIR, "EXP")
    
    for fname, rule in rules.items():
        origen = rule.get("origen", "")
        if not origen:
            continue
        
        # Verificar si el origen existe como archivo
        origen_file, origen_md = _nombres_origen(origen)
        
        if not _origen_existe(origen_file, origen_md):
            # Verificar si al menos está referenciado en algún otro archivo
            if not _origen_referenciado(origen):
                issues.append({
                    "check": "huerfano",
                    "severidad": "ALTA",
                    "rule": rule.get("id", fname),
                    "file": fname,
                    "origen": origen,
                    "detalle": f"RULE {rule.get('id', fname)} referencia {origen} que no existe"
                })
    
    return issues


def _nombres_origen(origen: str) -> tuple[str, str]:
    """Nombres de archivo .yaml y .md para un origen dado."""
    origen_file = origen + ".yaml" if not origen.endswith(".yaml") else origen
    origen_md = origen + ".md" if not origen.endswith(".md") else origen
    return origen_file, origen_md


def _origen_existe(origen_file: str, origen_md: str) -> bool:
    """True si el origen existe como archivo o md en DEC/EXP."""
    found = False
    for d in [DECISIONS_DIR, EXPERIMENTS_DIR]:
        if os.path.exists(os.path.join(d, origen_file)) or os.path.exists(os.path.join(d, origen_md)):
            found = True
            break
    return found


def _origen_referenciado(origen: str) -> bool:
    """True si el origen está referenciado en algún otro archivo."""
    referenced = False
    for d in [DECISIONS_DIR, EXPERIMENTS_DIR]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                try:
                    with open(os.path.join(d, f)) as fh:
                        if origen in fh.read():
                            referenced = True
                            break
                except Exception:
                    pass
    return referenced


def check_conflictos(rules: dict) -> list:
    """2+ RULEs activas para el mismo tipo de tarea con modelos distintos."""
    issues = []
    task_model_map = {}
    
    for fname, rule in rules.items():
        if not rule.get("activa", True):
            continue
        
        cond = rule.get("condicion", {})
        tipos = cond.get("tipo_tarea", [])
        accion = rule.get("accion", {})
        modelo = accion.get("modelo", "") if isinstance(accion, dict) else ""
        
        for t in tipos:
            if t == "cualquiera":
                continue
            if t not in task_model_map:
                task_model_map[t] = []
            task_model_map[t].append((rule.get("id"), modelo, rule.get("prioridad", 50)))
    
    for task_type, entries in task_model_map.items():
        modelos = set(m for _, m, _ in entries)
        if len(modelos) > 1:
            issues.append({
                "check": "conflicto",
                "severidad": "MEDIA",
                "tarea": task_type,
                "detalle": f"Tarea '{task_type}' tiene {len(modelos)} modelos distintos: {modelos}",
                "rules": [e[0] for e in entries]
            })
    
    return issues


def check_sin_validar(rules: dict, max_days: int = 180) -> list:
    """RULEs sin revisión en > N días."""
    issues = []
    now = datetime.now()
    
    for fname, rule in rules.items():
        fecha_str = rule.get("ultima_revision", "")
        if not fecha_str:
            issues.append({
                "check": "sin_validar",
                "severidad": "MEDIA",
                "rule": rule.get("id", fname),
                "detalle": f"RULE {rule.get('id', fname)} sin fecha de revisión"
            })
            continue
        
        try:
            fecha = datetime.strptime(fecha_str[:10], "%Y-%m-%d")
            days = (now - fecha).days
            if days > max_days:
                issues.append({
                    "check": "sin_validar",
                    "severidad": "MEDIA",
                    "rule": rule.get("id", fname),
                    "dias": days,
                    "detalle": f"RULE {rule.get('id', fname)} sin validar en {days} días"
                })
        except ValueError:
            pass
    
    return issues


def _leer_versiones_modelos() -> dict:
    """Lee versiones actuales desde las fichas de modelo (.md)."""
    import re
    versions = {}
    if not os.path.isdir(MODELS_DIR):
        return versions
    for fname in os.listdir(MODELS_DIR):
        if not fname.endswith(".md"):
            continue
        try:
            with open(os.path.join(MODELS_DIR, fname)) as f:
                content = f.read()
            ver_match = re.search(r'(?:versi[oó]n|version)[:\s]*(\d+\.\d+)', content, re.IGNORECASE)
            if ver_match:
                versions[fname.replace(".md", "")] = ver_match.group(1)
        except Exception:
            pass
    return versions


def check_version_antigua(rules: dict) -> list:
    """RULEs basadas en versiones de modelo que han sido superadas."""
    issues = []
    
    # Buscar versiones actuales en fichas de modelo
    model_versions = _leer_versiones_modelos()
    
    for fname, rule in rules.items():
        accion = rule.get("accion", {})
        modelo = accion.get("modelo", "") if isinstance(accion, dict) else ""
        nota = rule.get("nota", "")
        
        # Simple: si el modelo menciona una versión y hay ficha más reciente
        for model_file, version in model_versions.items():
            if model_file.lower() in modelo.lower() or model_file.lower() in nota.lower():
                # La versión en la ficha podría ser más nueva
                issues.append({
                    "check": "version_antigua",
                    "severidad": "MEDIA",
                    "rule": rule.get("id", fname),
                    "modelo": modelo,
                    "version_ficha": version,
                    "detalle": f"RULE {rule.get('id', fname)} usa {modelo} — verificar si la versión {version} de la ficha es más reciente"
                })
    
    return issues


def check_no_usado(rules: dict, max_days: int = 90) -> list:
    """RULEs activas que no se han usado en N días (según última_revision)."""
    issues = []
    now = datetime.now()
    
    for fname, rule in rules.items():
        if not rule.get("activa", True):
            continue
        
        fecha_str = rule.get("ultima_revision", "")
        if not fecha_str:
            continue
        
        try:
            fecha = datetime.strptime(fecha_str[:10], "%Y-%m-%d")
            days = (now - fecha).days
            if days > max_days:
                issues.append({
                    "check": "no_usado",
                    "severidad": "BAJA",
                    "rule": rule.get("id", fname),
                    "dias": days,
                    "detalle": f"RULE {rule.get('id', fname)} activa pero sin uso en {days} días"
                })
        except ValueError:
            pass
    
    return issues


# ─── Core ───────────────────────────────────────────────

def run_all_checks() -> dict:
    """Ejecuta todos los checks."""
    rules = load_yaml_dir(RULES_DIR)
    
    all_issues = []
    all_issues.extend(check_huerfano_rules(rules))
    all_issues.extend(check_conflictos(rules))
    all_issues.extend(check_sin_validar(rules))
    all_issues.extend(check_version_antigua(rules))
    all_issues.extend(check_no_usado(rules))
    
    return {
        "total_rules": len(rules),
        "total_issues": len(all_issues),
        "alta": [i for i in all_issues if i["severidad"] == "ALTA"],
        "media": [i for i in all_issues if i["severidad"] == "MEDIA"],
        "baja": [i for i in all_issues if i["severidad"] == "BAJA"],
        "all": all_issues,
    }


def format_report(result: dict) -> str:
    """Formatea el informe de deuda técnica."""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  DEBT DETECTOR — Deuda técnica de conocimiento")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  RULEs analizadas: {result['total_rules']}")
    lines.append(f"  Issues: {result['total_issues']}")
    lines.append("")
    
    for sev, icon, label in [("alta", "🔴", "ALTA"), ("media", "🟡", "MEDIA"), ("baja", "🟢", "BAJA")]:
        issues = result[sev]
        if not issues:
            continue
        lines.append(f"── {icon} {label} ({len(issues)}) ──")
        for i in issues:
            lines.append(f"  [{i['check']}] {i['detalle'][:120]}")
        lines.append("")
    
    if result["total_issues"] == 0:
        lines.append("  ✅ Sin deuda técnica detectada.")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Debt Detector — deuda técnica Joko Lab")
    parser.add_argument("--full", action="store_true", default=True)
    
    args = parser.parse_args()
    
    result = run_all_checks()
    print(format_report(result))
