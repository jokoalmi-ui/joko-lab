#!/usr/bin/env python3
"""confidence_decayer.py — Envejecimiento automático de confianza

Las decisiones envejecen. La confianza debe reflejarlo.

Fórmula:
  confidence = evidencia × recencia × validaciones × compatibilidad

Donde:
  - evidencia: confianza base (0.0-1.0)
  - recencia: factor temporal (30d=1.0, 90d=0.8, 180d=0.5, >365d=0.3)
  - validaciones: min(n/5, 1.0) — satura en 5
  - compatibilidad: 1.0 si no hay nueva versión del modelo

Umbral de desactivación: confianza < 0.4 → activa: false

Uso:
  python3 confidence_decayer.py --check        # Solo informe
  python3 confidence_decayer.py --apply        # Aplicar decay a YAML
  python3 confidence_decayer.py --rule RULE-001 # Una regla específica
"""

import os, sys, yaml
from datetime import datetime, timedelta
from pathlib import Path

OBJECTS_DIR = os.path.expanduser("~/joko-lab/01-knowledge/objects")


def _ko_to_legacy(ko: dict) -> dict:
    """Convierte un Knowledge Object v1 (objects/) al formato plano legacy."""
    legacy = dict(ko.get("legacy_fields", {}) or {})
    legacy.setdefault("id", ko.get("id"))
    legacy.setdefault("type", ko.get("type"))
    legacy.setdefault("status", ko.get("status", "activo"))
    legacy.setdefault("desc", ko.get("body", ""))
    legacy.setdefault("confianza", ko.get("confidence"))
    legacy.setdefault("ultima_revision", ko.get("last_validated") or ko.get("created"))
    if not legacy.get("origen"):
        deps = ko.get("dependencies") or []
        legacy["origen"] = deps[0] if deps else None
    return legacy


def recency_factor(last_review_str: str) -> float:
    """Calcula factor de recencia basado en días desde última revisión."""
    if not last_review_str:
        return 0.5
    
    try:
        last_review = datetime.strptime(last_review_str[:10], "%Y-%m-%d")
        days = (datetime.now() - last_review).days
    except (ValueError, TypeError):
        return 0.5
    
    if days < 30:
        return 1.0
    elif days < 90:
        return 0.8
    elif days < 180:
        return 0.5
    else:
        return 0.3


def validation_factor(validaciones: int) -> float:
    """Factor de validaciones: satura en 5."""
    return min(validaciones / 5, 1.0) if validaciones else 0.2


def recalculate_confidence(rule: dict) -> dict:
    """Recalcula la confianza de una RULE."""
    evidencia = rule.get("confianza", 0.5)
    recencia = recency_factor(rule.get("ultima_revision", ""))
    validaciones = validation_factor(rule.get("validaciones", 1))
    compatibilidad = 1.0  # Por ahora siempre 1.0
    
    nueva_confianza = round(evidencia * recencia * validaciones * compatibilidad, 3)
    
    # Período de gracia: RULEs con < 7 días nunca se desactivan
    dias = _days_since(rule.get("ultima_revision", ""))
    desactivar = nueva_confianza < 0.3 and dias >= 7
    
    return {
        "id": rule.get("id", "?"),
        "origen": rule.get("origen", "?"),
        "confianza_original": evidencia,
        "recencia": round(recencia, 2),
        "validaciones_factor": round(validaciones, 2),
        "nueva_confianza": nueva_confianza,
        "activa": rule.get("activa", True),
        "desactivar": desactivar,
        "dias_desde_revision": dias,
    }


def _days_since(date_str: str) -> int:
    """Días desde una fecha."""
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return (datetime.now() - dt).days
    except (ValueError, TypeError):
        return 999


def check_all() -> list:
    """Verifica todas las RULEs (type=RULE) desde objects/ sin modificar."""
    results = []
    if not os.path.isdir(OBJECTS_DIR):
        return results
    
    for fname in sorted(os.listdir(OBJECTS_DIR)):
        if not fname.endswith(".yaml"):
            continue
        try:
            with open(os.path.join(OBJECTS_DIR, fname)) as f:
                ko = yaml.safe_load(f)
            if not isinstance(ko, dict) or ko.get("type") != "RULE":
                continue
            rule = _ko_to_legacy(ko)
            result = recalculate_confidence(rule)
            result["file"] = fname
            results.append(result)
        except Exception as e:
            results.append({"id": fname, "error": str(e)})
    
    return results


def apply_decay(dry_run: bool = True) -> list:
    """Aplica decay a todas las RULEs."""
    results = check_all()
    updated = []
    
    for result in results:
        if result.get("error"):
            continue
        
        fname = result["file"]
        filepath = os.path.join(OBJECTS_DIR, fname)
        
        try:
            with open(filepath) as f:
                ko = yaml.safe_load(f)
            if not isinstance(ko, dict) or ko.get("type") != "RULE":
                continue
            rule = _ko_to_legacy(ko)
            legacy = ko.get("legacy_fields", {}) or {}
            
            old_conf = rule.get("confianza", 0.5)
            new_conf = result["nueva_confianza"]
            
            if abs(old_conf - new_conf) < 0.01:
                continue  # Sin cambio significativo
            
            if not dry_run:
                ko["confidence"] = new_conf
                ko["last_validated"] = datetime.now().strftime("%Y-%m-%d")
                if result["desactivar"]:
                    ko["status"] = "desactivado"
                    legacy["activa"] = False
                    ko["legacy_fields"] = legacy
                
                with open(filepath, "w") as f:
                    yaml.dump(ko, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            updated.append({
                "id": result["id"],
                "file": fname,
                "old_conf": old_conf,
                "new_conf": new_conf,
                "desactivada": result["desactivar"],
                "dry_run": dry_run,
            })
        except Exception as e:
            updated.append({"id": result.get("id", fname), "error": str(e)})
    
    return updated


def format_report(results: list) -> str:
    """Formatea el informe de decay."""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  CONFIDENCE DECAY — Envejecimiento de RULEs")
    lines.append("═══════════════════════════════════════════")
    lines.append("")
    
    if not results:
        lines.append("  Sin RULEs para analizar.")
        lines.append("═══════════════════════════════════════════")
        return "\n".join(lines)
    
    # Tabla
    lines.append(f"  {'RULE':<12} {'Orig':<8} {'Días':>5} {'Rec':>5} {'Val':>5} {'Conf':>6} {'Nueva':>6} {'Estado':<10}")
    lines.append("  " + "-" * 65)
    
    warnings = []
    for r in results:
        if r.get("error"):
            lines.append(f"  ❌ {r['id']}: ERROR - {r['error']}")
            continue
        
        status = "🔴 DESACTIVAR" if r["desactivar"] else "🟢 OK" if r["nueva_confianza"] >= 0.6 else "🟡 VIGILAR"
        lines.append(
            f"  {r['id']:<12} {r['origen']:<8} {r['dias_desde_revision']:>4}d "
            f"{r['recencia']:>4.1f} {r['validaciones_factor']:>4.1f} "
            f"{r['confianza_original']:>5.2f} {r['nueva_confianza']:>5.2f} {status:<10}"
        )
        
        if r["desactivar"]:
            warnings.append(r)
    
    lines.append("")
    
    if warnings:
        lines.append(f"  ⚠ {len(warnings)} RULEs por debajo del umbral (0.4):")
        for w in warnings:
            lines.append(f"    - {w['id']}: {w['confianza_original']} → {w['nueva_confianza']} ({w['dias_desde_revision']}d sin revisión)")
        lines.append("")
        lines.append("  Acción: python3 confidence_decayer.py --apply")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Confidence Decay — envejecimiento de RULEs")
    parser.add_argument("--check", action="store_true", default=True, help="Solo informe (default)")
    parser.add_argument("--apply", action="store_true", help="Aplicar decay a archivos YAML")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin escribir")
    
    args = parser.parse_args()
    
    if args.apply:
        dry = args.dry_run
        updated = apply_decay(dry_run=dry)
        if not updated:
            print("Sin cambios necesarios.")
        else:
            mode = "DRY RUN" if dry else "APLICADO"
            print(f"── {mode} ──")
            for u in updated:
                if u.get("error"):
                    print(f"  ❌ {u['id']}: {u['error']}")
                else:
                    icon = "🔴" if u["desactivada"] else "🟡"
                    print(f"  {icon} {u['id']}: {u['old_conf']:.2f} → {u['new_conf']:.2f}")
    else:
        results = check_all()
        print(format_report(results))
