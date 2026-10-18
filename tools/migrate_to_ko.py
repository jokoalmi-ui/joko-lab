#!/usr/bin/env python3
"""
Migra DECs actuales a Knowledge Object schema v1.
Solo lectura primero, escribe con --apply.

Uso:
    python3 migrate_to_ko.py              # dry-run: muestra lo que haría
    python3 migrate_to_ko.py --apply      # escribe los nuevos archivos
"""

import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path

LAB = Path.home() / "joko-lab"
SOURCE = LAB / "01-knowledge" / "decisions"
TARGET = LAB / "01-knowledge" / "objects"
BACKUP = LAB / "01-knowledge" / "decisions.BACKUP"

NOW = datetime.now()
DEFAULT_EXPIRY_MONTHS = 6
DEFAULT_REVIEW_MONTHS = 3

DOMAIN = "ai-architecture"
SCOPE = "todo_joko_lab"


def parse_date(s):
    """Intenta parsear una fecha en varios formatos."""
    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
        try:
            return datetime.strptime(s.split("T")[0].split(" ")[0], "%Y-%m-%d")
        except (ValueError, AttributeError):
            continue
    return NOW  # fallback


def _inferir_tipo(source_path: Path, old: dict) -> str:
    if "rules" in str(source_path):
        return "RULE"
    elif "policies" in str(source_path):
        return "POLICY"
    else:
        return old.get("type", "DEC")


def _inferir_confianza(confidence, validaciones) -> tuple:
    if confidence is not None:
        if confidence >= 0.8:
            conf_label = "ALTA"
        elif confidence >= 0.5:
            conf_label = "MEDIA"
        else:
            conf_label = "BAJA"
    else:
        conf_label = "NO_EVALUADA"

    if validaciones and isinstance(validaciones, (int, float)):
        if validaciones >= 3:
            conf_label = "ALTA"
            if confidence is None:
                confidence = 0.85
        elif validaciones >= 1:
            if confidence is None:
                confidence = 0.70

    return confidence, conf_label


def _construir_ko_base(ko_id, ktype, created, last_validated, confidence, conf_label, evidence, desc) -> dict:
    """Construye el Knowledge Object base con la misma estructura y orden de claves."""
    ko = {
        "id": ko_id,
        "type": ktype,
        "status": "activo",
        "version": 1,
        "created": created.strftime("%Y-%m-%d"),
        "last_validated": last_validated.strftime("%Y-%m-%d") if last_validated else None,
        "next_review": (created + timedelta(days=DEFAULT_REVIEW_MONTHS * 30)).strftime("%Y-%m-%d"),
        "expires": (created + timedelta(days=DEFAULT_EXPIRY_MONTHS * 30)).strftime("%Y-%m-%d"),
        "confidence": confidence,
        "confidence_label": conf_label,
        "evidence": evidence,
        "dependencies": [],
        "contradicts": [],
        "superseded_by": None,
        "domain": DOMAIN,
        "scope": SCOPE,
        "monitoring": {
            "metric": None,
            "baseline": None,
            "current": None,
            "last_checked": None,
        },
        "history": [
            {
                "date": created.strftime("%Y-%m-%d"),
                "event": "created",
            },
            {
                "date": NOW.strftime("%Y-%m-%d"),
                "event": "migrated_to_ko",
                "note": "Migrado de formato YAML plano a Knowledge Object v1",
            },
        ],
        "body": desc,
        "legacy_fields": {},
    }

    return ko


def _preservar_legacy_fields(ko: dict, old: dict) -> None:
    # Preservar campos específicos
    if old.get("origen"):
        ko["dependencies"] = [old["origen"]]
    if old.get("condicion"):
        ko["legacy_fields"]["condicion"] = old["condicion"]
    if old.get("accion"):
        ko["legacy_fields"]["accion"] = old["accion"]
    if old.get("prioridad") is not None:
        ko["legacy_fields"]["prioridad"] = old["prioridad"]
    if old.get("activa") is not None:
        ko["legacy_fields"]["activa"] = old["activa"]
    if old.get("nota"):
        ko["legacy_fields"]["nota"] = old["nota"]
    if old.get("alcance"):
        ko["legacy_fields"]["alcance"] = old["alcance"]
    if old.get("validaciones"):
        ko["legacy_fields"]["validaciones"] = old["validaciones"]


def migrate_dec(source_path):
    """Convierte un DEC/RULE/POLICY YAML actual a Knowledge Object."""
    with open(source_path) as fh:
        old = yaml.safe_load(fh)

    ko_id = old.get("id", source_path.stem)
    created = parse_date(old.get("fecha") or old.get("created") or old.get("date") or old.get("ultima_revision"))
    desc = old.get("desc", "")
    evidence_raw = old.get("evidencia") or old.get("evidence") or []
    evidence = [e for e in evidence_raw if isinstance(e, str)]
    confidence = old.get("confianza") or old.get("confidence")

    # Detectar tipo por directorio de origen o campo 'type'
    ktype = _inferir_tipo(source_path, old)

    # Inferir confidence_label
    validaciones = old.get("validaciones")
    confidence, conf_label = _inferir_confianza(confidence, validaciones)

    # Prioridad de RULE/POLICY
    prioridad = old.get("prioridad")

    # Calcular last_validated
    last_validated = parse_date(old.get("ultima_revision") or old.get("last_validated") or old.get("validated"))

    ko = _construir_ko_base(ko_id, ktype, created, last_validated, confidence, conf_label, evidence, desc)
    _preservar_legacy_fields(ko, old)

    return ko


SOURCE_DIRS = [
    (LAB / "01-knowledge" / "decisions", "decisions"),
    (LAB / "01-knowledge" / "rules", "rules"),
    (LAB / "01-knowledge" / "policies", "policies"),
]

def main():
    apply_flag = "--apply" in sys.argv

    all_files = []
    for src_dir, _ in SOURCE_DIRS:
        if src_dir.exists():
            all_files.extend([(f, src_dir) for f in sorted(src_dir.glob("*.yaml"))])

    if not all_files:
        print("No hay archivos .yaml para migrar")
        return 0

    print(f"Archivos a migrar: {len(all_files)}")
    print(f"Destino: {TARGET}")
    print(f"Backup:  {BACKUP}")
    print()

    if not apply_flag:
        print("=== DRY RUN (usa --apply para escribir) ===\n")

    for yf, src_dir in all_files:
        ko = migrate_dec(yf)
        target_file = TARGET / f"{ko['id']}.yaml"

        print(f"  {yf.name} → {target_file.name}")
        print(f"    status:       {ko['status']}")
        print(f"    confidence:   {ko['confidence']} ({ko['confidence_label']})")
        print(f"    created:      {ko['created']}")
        print(f"    next_review:  {ko['next_review']}")
        print(f"    expires:      {ko['expires']}")
        print(f"    evidence:     {len(ko['evidence'])} items")
        print()

        if apply_flag:
            # Backup
            BACKUP.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(yf, BACKUP / yf.name)

            # Escribir Knowledge Object
            TARGET.mkdir(parents=True, exist_ok=True)
            with open(target_file, "w") as fh:
                fh.write(yaml.dump(ko, allow_unicode=True, default_flow_style=False, sort_keys=False))
            print(f"    ✅ Escrito\n")

    if apply_flag:
        print(f"\nMigración completada. {len(all_files)} archivos migrados.")
        print(f"Backup en: {BACKUP}")
        print(f"Nuevos objetos en: {TARGET}")
        print(f"\nLos archivos originales NO se han borrado.")
    else:
        print(f"\nDry run completado. {len(all_files)} archivos simulados.")
        print("Ejecuta con --apply para escribir.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
