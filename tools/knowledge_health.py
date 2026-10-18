#!/usr/bin/env python3
"""
Knowledge Health Auditor — Solo lectura.
Evalúa la salud de la base de conocimiento sin modificar nada.

Uso:
    python3 knowledge_health.py
    python3 knowledge_health.py --json   # salida JSON para pipelines
"""

import os
import re
import sys
import json
import yaml
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

# Importar verificador del Evidence Contract (misma carpeta tools/)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_contract import verify_all

LAB_ROOT = Path.home() / "joko-lab"
OBJECTS_DIR = LAB_ROOT / "01-knowledge" / "objects"
KNOWLEDGE_DIRS = [
    LAB_ROOT / "01-knowledge" / "objects",
    LAB_ROOT / "01-knowledge" / "decisions",
    LAB_ROOT / "01-knowledge" / "experiments",
    LAB_ROOT / "01-knowledge" / "observations",
    LAB_ROOT / "01-knowledge" / "rules",
    LAB_ROOT / "01-knowledge" / "policies",
    LAB_ROOT / "lpa" / "pattern-incubator",
]

NOW = datetime.now()
CONFIDENCE_THRESHOLD = 0.6
REVIEW_DAYS = 180
EXPIRY_WARNING_DAYS = 30


def find_knowledge_files():
    """Encuentra todos los archivos de conocimiento (.md, .yaml).
    Excluye backups (.bak-*, .BACKUP) y dotfiles: no son conocimiento activo
    (fix 05-ago-2026: el escaneo contaba .bak-wikilinks como UNKNOWN)."""
    files = []
    for d in KNOWLEDGE_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if f.suffix not in (".md", ".yaml") or f.name == "TEMPLATE.md":
                continue
            rel = str(f.relative_to(LAB_ROOT))
            if ".bak" in rel.lower() or ".backup" in rel.lower() or "/." in rel:
                continue
            files.append(f)
    return files


# Excluidos de la auditoría estructural: backups, sesiones raw, entornos, git,
# y bibliotecas de referencia EXTERNAS (01-knowledge/references/ = skills de
# terceros clonadas bajo demanda, sin frontmatter del lab — fix 06-sep-2026:
# no son conocimiento del lab y hundían Frontmatter al 40% de 3588 docs).
STRUCT_EXCLUDE_PARTS = (".BACKUP", ".backup", "/.git/", "node_modules",
                        ".venv", "metrics/sesiones/raw", ".pytest_cache",
                        "01-knowledge/references/")


def _chequear_estructura_md(txt):
    lines = txt.splitlines()
    has_fm = (len(lines) >= 2 and lines[0].strip() == "---"
              and any(l.strip() == "---" for l in lines[1:min(40, len(lines))]))
    has_h1 = re.search(r"^#\s", txt, re.M) is not None
    has_h2 = re.search(r"^##\s", txt, re.M) is not None
    has_h3 = re.search(r"^###\s", txt, re.M) is not None
    has_enlaces = ("[[" in txt) or (re.search(r"\[[^\]]*\]\([^)]*\)", txt) is not None)
    return {
        "has_fm": has_fm,
        "has_h1": has_h1,
        "has_h2": has_h2,
        "has_h3": has_h3,
        "has_enlaces": has_enlaces,
    }


def _acumular_archivo(p: Path, flags: dict, stats, no_fm: list, no_h1: list):
    """Acumula las estadísticas de un archivo .md en stats y listas."""
    stats["total"] += 1
    if flags["has_fm"]:
        stats["con_frontmatter"] += 1
    else:
        no_fm.append(str(p.relative_to(LAB_ROOT)))
    if flags["has_h1"]:
        stats["con_h1"] += 1
    else:
        no_h1.append(str(p.relative_to(LAB_ROOT)))
    if flags["has_h2"]:
        stats["con_h2"] += 1
    if flags["has_h3"]:
        stats["con_h3"] += 1
    if flags["has_enlaces"]:
        stats["con_enlaces"] += 1


def audit_structure():
    """
    Auditoría estructural de docs de conocimiento (.md).
    Solo lectura. Comprueba: frontmatter YAML cerrado, H1, H2, H3, enlaces.
    Excluye exportaciones de sesiones (raw) y backups.
    """
    stats = defaultdict(int)
    no_fm, no_h1 = [], []

    for dirpath, dirnames, filenames in os.walk(LAB_ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".BACKUP")]
        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            p = Path(dirpath) / fname
            rel = str(p.relative_to(LAB_ROOT))
            if any(x in rel for x in STRUCT_EXCLUDE_PARTS):
                continue
            if p.is_symlink() and not p.exists():
                continue  # symlink roto: no es un doc real
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            flags = _chequear_estructura_md(txt)
            _acumular_archivo(p, flags, stats, no_fm, no_h1)

    return {"stats": dict(stats), "no_frontmatter": no_fm, "no_h1": no_h1}


def parse_frontmatter(path):
    """Extrae metadatos de un archivo .md (frontmatter) o .yaml (documento completo)."""
    try:
        with open(path) as fh:
            content = fh.read()

        # YAML puro (.yaml sin frontmatter)
        if path.suffix == ".yaml" and not content.startswith("---"):
            return yaml.safe_load(content) or {}

        # Markdown con frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
    except Exception:
        pass
    return {}


def _coincide(path, name, substrings, dirname) -> bool:
    """True si el nombre contiene algún substring o el directorio padre coincide."""
    return any(s in name for s in substrings) or path.parent.name == dirname


def _clasificar_por_nombre(path) -> str:
    """Clasifica un archivo por convención de nombre/directorio.

    Orden importa: la primera regla que coincida gana (las prefijos con guion
    antes que los substrings genéricos para evitar colisiones, p.ej. "cp-"
    antes de "policy" si un nombre contuviera ambos).
    """
    name = path.stem.lower()
    reglas = (
        # (substrings, dirname, tipo) — los prefijos de ID y dirs específicos
        # ganan; SIN substring generico "decision" (roba las observaciones
        # OBS-*-decisiones-por-politica → DEC). Fix 2026-09-02 (auditoria).
        (("dec-",), "decisions", "DEC"),
        (("experiment", "exp-"), "experiments", "EXP"),
        (("observation", "obs-"), None, "OBS"),
        (("rule", "rule-"), "rules", "RULE"),
        (("policy", "policy-"), "policies", "POLICY"),
        (("cp-",), "pattern-incubator", "PATTERN"),
    )
    for substrings, dirname, tipo in reglas:
        if _coincide(path, name, substrings, dirname):
            return tipo
    return "UNKNOWN"


def classify_file(path, fm):
    """Clasifica un archivo por tipo de conocimiento."""
    # Knowledge Object v1: usa campo 'type' explícito
    if fm.get("type") in ("DEC", "EXP", "OBS", "PATTERN", "RULE", "POLICY", "PRED"):
        return fm["type"]

    return _clasificar_por_nombre(path)


def extract_date(fm, keys):
    """Extrae la primera fecha encontrada de una lista de claves."""
    for k in keys:
        v = fm.get(k)
        if v:
            if isinstance(v, datetime):
                return v
            if isinstance(v, date):
                # yaml.safe_load convierte ISO a date (pitfall 2 de refactor-seguro)
                return datetime.combine(v, datetime.min.time())
            if isinstance(v, str):
                try:
                    return datetime.fromisoformat(v.replace("Z", "+00:00").split("T")[0])
                except ValueError:
                    pass
    return None


def _construir_item_ko(f, ktype, status, confidence, created, last_validated, expires, evidence):
    return {
        "id": f.stem,
        "type": ktype,
        "path": str(f.relative_to(LAB_ROOT)),
        "status": status,
        "confidence": confidence,
        "created": created.isoformat()[:10] if created else None,
        "last_validated": last_validated.isoformat()[:10] if last_validated else None,
        "expires": expires.isoformat()[:10] if expires else None,
        "evidence_count": len(evidence) if isinstance(evidence, list) else 0,
    }


def _contar_estado_dec(ktype, status, last_validated, stats):
    if status in ("retirado", "retired", "e∅"):
        stats["decs_retired"] = stats.get("decs_retired", 0) + 1
    if status == "expirado":
        stats["decs_expired"] = stats.get("decs_expired", 0) + 1
    if last_validated is not None:
        stats["decs_revalidated"] = stats.get("decs_revalidated", 0) + 1


def _dep_aporta_evidencia(dep_file) -> bool:
    """True si la dependencia tiene evidencia o confianza alta."""
    dep_fm = parse_frontmatter(dep_file)
    dep_evidence = dep_fm.get("evidence") or []
    dep_confidence = dep_fm.get("confidence")
    return (isinstance(dep_evidence, list) and len(dep_evidence) > 0) or \
           (dep_confidence and isinstance(dep_confidence, (int, float)) and dep_confidence >= 0.8)


def _verificar_evidencia_transitiva(fm, ktype, deps):
    has_transitive_evidence = False
    if deps and ktype in ("RULE", "POLICY"):
        for dep_id in deps:
            dep_file = OBJECTS_DIR / f"{dep_id}.yaml"
            if dep_file.exists() and _dep_aporta_evidencia(dep_file):
                has_transitive_evidence = True
                break
    return has_transitive_evidence


def _chequear_expiracion(ktype, expires, f, stats, issues):
    """Issues/stats del bloque de expiración (sin expiración / expirada / próxima)."""
    if not expires:
        issues.append(f"[{ktype}] {f.stem}: sin fecha de expiración")
        stats["sin_expiración"] += 1
    elif expires < NOW:
        issues.append(f"[{ktype}] {f.stem}: EXPIRADA ({expires.isoformat()[:10]})")
        stats["expiradas"] += 1
    elif expires < NOW + timedelta(days=EXPIRY_WARNING_DAYS):
        issues.append(f"[{ktype}] {f.stem}: próxima a expirar ({expires.isoformat()[:10]})")
        stats["proximas_expirar"] += 1


def _chequear_validacion(ktype, last_validated, f, stats, issues):
    """Issues/stats del bloque de validación (nunca validada / sin revisión)."""
    if not last_validated:
        issues.append(f"[{ktype}] {f.stem}: nunca validada")
        stats["sin_validar"] += 1
    elif last_validated < NOW - timedelta(days=REVIEW_DAYS):
        days = (NOW - last_validated).days
        issues.append(f"[{ktype}] {f.stem}: sin revisión hace {days} días")
        stats["sin_revision"] += 1


def _detectar_problemas_ko(ktype, status, last_validated, expires, confidence, evidence, fm, f, stats, issues):
    _chequear_expiracion(ktype, expires, f, stats, issues)
    _chequear_validacion(ktype, last_validated, f, stats, issues)

    if confidence is not None:
        if isinstance(confidence, (int, float)) and confidence < CONFIDENCE_THRESHOLD:
            issues.append(f"[{ktype}] {f.stem}: confianza baja ({confidence})")
            stats["confianza_baja"] += 1

    if isinstance(evidence, list) and len(evidence) == 0:
        deps = fm.get("dependencies") or []
        has_transitive_evidence = _verificar_evidencia_transitiva(fm, ktype, deps)
        if not has_transitive_evidence:
            issues.append(f"[{ktype}] {f.stem}: sin evidencia que la respalde")
            stats["sin_evidencia"] += 1


def _procesar_ko(f, fm, ktype, created, last_validated, expires, confidence, status, evidence, stats, issues):
    item = _construir_item_ko(f, ktype, status, confidence, created, last_validated, expires, evidence)

    if ktype in ("DEC", "RULE", "POLICY"):
        _contar_estado_dec(ktype, status, last_validated, stats)
        _detectar_problemas_ko(ktype, status, last_validated, expires, confidence, evidence, fm, f, stats, issues)

    if ktype == "PATTERN" and status == "E0":
        stats["patrones_e0"] += 1

    return item


def _detectar_contradicciones(dec_items, stats, base_dir=None):
    contradictions = []
    root = base_dir or LAB_ROOT
    for i in range(len(dec_items)):
        for j in range(i + 1, len(dec_items)):
            fi = root / dec_items[i]["path"]
            fj = root / dec_items[j]["path"]
            try:
                ci = fi.read_text().lower()
                cj = fj.read_text().lower()
            except Exception:
                continue
            # Heurística simple: si uno contiene "preferido" y otro "descartado" para el mismo modelo
            common_terms = set(ci.split()) & set(cj.split())
            if len(common_terms) > 5:
                if ("preferido" in ci and "descartado" in cj) or ("descartado" in ci and "preferido" in cj):
                    contradictions.append(f"{dec_items[i]['id']} ↔ {dec_items[j]['id']}: posible contradicción")
                    stats["contradicciones"] += 1
    return contradictions


def _calcular_health(stats):
    penalties = (
        stats.get("expiradas", 0) * 5 +
        stats.get("sin_validar", 0) * 3 +
        stats.get("sin_revision", 0) * 2 +
        stats.get("confianza_baja", 0) * 3 +
        stats.get("sin_evidencia", 0) * 4 +
        stats.get("sin_expiración", 0) * 1 +
        stats.get("contradicciones", 0) * 5
    )
    return max(0, 100 - min(100, penalties))


def audit():
    files = find_knowledge_files()
    stats = defaultdict(int)
    issues = []
    items = []

    for f in files:
        fm = parse_frontmatter(f)
        ktype = classify_file(f, fm)
        stats[f"total_{ktype}"] += 1
        stats["total"] += 1

        created = extract_date(fm, ["created", "date", "fecha"])
        last_validated = extract_date(fm, ["last_validated", "ultima_validacion", "validated"])
        expires = extract_date(fm, ["expires", "next_review", "proxima_revision"])
        confidence = fm.get("confidence") or fm.get("confianza")
        status = fm.get("status") or fm.get("estado", "unknown")
        evidence = fm.get("evidence") or fm.get("evidencias") or fm.get("evidencia", [])

        item = _procesar_ko(f, fm, ktype, created, last_validated, expires, confidence, status, evidence, stats, issues)
        items.append(item)

    # Detectar contradicciones entre DECs
    dec_items = [i for i in items if i["type"] == "DEC"]
    contradictions = _detectar_contradicciones(dec_items, stats)

    # Evidence Contract: verificar promoción EXP→DEC sobre los KOs
    contract_results = verify_all()
    contract_ok = sum(1 for r in contract_results if r.get("passed"))
    contract_total = len(contract_results)
    contract_fail = [r["id"] for r in contract_results if not r.get("passed")]
    stats["contract_cumplen"] = contract_ok
    stats["contract_total"] = contract_total

    # Auditoría estructural de docs de conocimiento
    structure = audit_structure()
    s_stats = structure["stats"]
    stats["struct_total"] = s_stats.get("total", 0)
    stats["struct_frontmatter"] = s_stats.get("con_frontmatter", 0)
    stats["struct_h1"] = s_stats.get("con_h1", 0)
    stats["struct_h2"] = s_stats.get("con_h2", 0)
    stats["struct_h3"] = s_stats.get("con_h3", 0)
    stats["struct_enlaces"] = s_stats.get("con_enlaces", 0)

    # Calcular health score (0-100)
    health = _calcular_health(stats)

    return {
        "stats": dict(stats),
        "issues": issues,
        "contradictions": contradictions,
        "health": health,
        "items": items,
    }


def print_report(result):
    """Formato legible."""
    s = result["stats"]
    print("=" * 60)
    print("KNOWLEDGE HEALTH REPORT")
    print("=" * 60)
    print(f"Fecha: {NOW.isoformat()[:10]}")
    print()
    print(f"Total entidades:     {s.get('total', 0)}")
    print(f"  DEC:               {s.get('total_DEC', 0)}")
    print(f"  EXP:               {s.get('total_EXP', 0)}")
    print(f"  OBS:               {s.get('total_OBS', 0)}")
    print(f"  RULE:              {s.get('total_RULE', 0)}")
    print(f"  POLICY:            {s.get('total_POLICY', 0)}")
    print(f"  PATTERN:           {s.get('total_PATTERN', 0)}")
    print()
    print("Alertas:")
    print(f"  Expiradas:         {s.get('expiradas', 0)}")
    print(f"  Próximas a expirar:{s.get('proximas_expirar', 0)}")
    print(f"  Sin expiración:    {s.get('sin_expiración', 0)}")
    print(f"  Nunca validadas:   {s.get('sin_validar', 0)}")
    print(f"  Sin revisión >180d:{s.get('sin_revision', 0)}")
    print(f"  Confianza baja:    {s.get('confianza_baja', 0)}")
    print(f"  Sin evidencia:     {s.get('sin_evidencia', 0)}")
    print(f"  Contradicciones:   {s.get('contradicciones', 0)}")
    print(f"  Patrones E0:       {s.get('patrones_e0', 0)}")
    print()
    print("Evidence Contract:")
    print(f"  Cumplen contrato:  {s.get('contract_cumplen', 0)}/{s.get('contract_total', 0)}")
    print()
    print("Estructura documental (docs .md de conocimiento):")
    st = s.get("struct_total", 0)
    if st > 0:
        pct = lambda v: f"{100 * v // st}%"
        print(f"  Total docs:        {st}")
        print(f"  Frontmatter:       {s.get('struct_frontmatter', 0)}/{st} ({pct(s.get('struct_frontmatter', 0))})")
        print(f"  H1:                {s.get('struct_h1', 0)}/{st} ({pct(s.get('struct_h1', 0))})")
        print(f"  H2:                {s.get('struct_h2', 0)}/{st} ({pct(s.get('struct_h2', 0))})")
        print(f"  H3:                {s.get('struct_h3', 0)}/{st} ({pct(s.get('struct_h3', 0))})")
        print(f"  Con enlaces:       {s.get('struct_enlaces', 0)}/{st} ({pct(s.get('struct_enlaces', 0))})")
    else:
        print("  (sin docs de conocimiento)")
    print()
    print(f"KNOWLEDGE HEALTH:    {result['health']}/100")
    print("=" * 60)

    # Knowledge Survival Rate
    decs = result["stats"].get("total_DEC", 0)
    if decs > 0:
        retired = result["stats"].get("decs_retired", 0)
        expired = result["stats"].get("decs_expired", 0)
        revalidated = result["stats"].get("decs_revalidated", 0)
        active = decs - retired - expired
        print(f"\nKNOWLEDGE SURVIVAL RATE:")
        print(f"  DEC creadas:       {decs}")
        print(f"  DEC activas:       {active}")
        print(f"  DEC retiradas:     {retired}")
        print(f"  DEC expiradas:     {expired}")
        print(f"  DEC revalidadas:   {revalidated}")
        if decs > 0:
            survival = (active / decs) * 100
            print(f"  Supervivencia:     {survival:.0f}%")
    print("=" * 60)

    if result["issues"]:
        print()
        print("DETALLES:")
        for issue in result["issues"]:
            print(f"  ⚠ {issue}")

    if result["contradictions"]:
        print()
        print("CONTRADICCIONES DETECTADAS:")
        for c in result["contradictions"]:
            print(f"  ⚡ {c}")

    print()


HISTORY_FILE = LAB_ROOT / "04-operations" / "metrics" / "knowledge_health.jsonl"


def save_to_history(result):
    """Guarda el resultado en el historial JSONL."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "date": NOW.isoformat()[:10],
        "health": result["health"],
        "total": result["stats"].get("total", 0),
        "contract": {
            "cumplen": result["stats"].get("contract_cumplen", 0),
            "total": result["stats"].get("contract_total", 0),
        },
        "structure": {
            "total": result["stats"].get("struct_total", 0),
            "frontmatter": result["stats"].get("struct_frontmatter", 0),
            "h1": result["stats"].get("struct_h1", 0),
            "h2": result["stats"].get("struct_h2", 0),
            "h3": result["stats"].get("struct_h3", 0),
            "enlaces": result["stats"].get("struct_enlaces", 0),
        },
        "dimensions": {
            "expiración": 100 - min(100, result["stats"].get("expiradas", 0) * 5 +
                                     result["stats"].get("sin_expiración", 0) * 1),
            "validación": 100 - min(100, result["stats"].get("sin_validar", 0) * 3 +
                                     result["stats"].get("sin_revision", 0) * 2),
            "evidencia": 100 - min(100, result["stats"].get("sin_evidencia", 0) * 4),
            "coherencia": 100 - min(100, result["stats"].get("contradicciones", 0) * 5 +
                                     result["stats"].get("confianza_baja", 0) * 3),
        },
    }
    with open(HISTORY_FILE, "a") as fh:
        fh.write(json.dumps(record) + "\n")


def show_trend():
    """Muestra la tendencia histórica de salud del conocimiento."""
    if not HISTORY_FILE.exists():
        print("No hay historial todavía. Ejecuta sin --trend primero.")
        return

    records = []
    with open(HISTORY_FILE) as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if len(records) < 2:
        print(f"Solo hay {len(records)} registro(s). Necesito al menos 2 para mostrar tendencia.")
        return

    print("=" * 60)
    print("KNOWLEDGE HEALTH TREND")
    print("=" * 60)
    print(f"{'Fecha':<12} {'Health':<8} {'Total':<8} {'Expir':<8} {'Valid':<8} {'Evid':<8} {'Coher':<8}")
    print("-" * 60)

    for r in records:
        d = r["dimensions"]
        print(f"{r['date']:<12} {r['health']:<8} {r['total']:<8} "
              f"{d['expiración']:<8} {d['validación']:<8} {d['evidencia']:<8} {d['coherencia']:<8}")

    # Tendencia
    first = records[0]["health"]
    last = records[-1]["health"]
    delta = last - first
    arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
    print("-" * 60)
    print(f"Tendencia: {first} → {last} ({arrow}{abs(delta)} en {len(records)} mediciones)")
    print("=" * 60)
    print()


def main():
    as_json = "--json" in sys.argv
    as_trend = "--trend" in sys.argv

    if as_trend:
        show_trend()
        return

    result = audit()
    save_to_history(result)

    if as_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
