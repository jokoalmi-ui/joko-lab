#!/usr/bin/env python3
"""
PIPELINE INSPECTOR — "¿Quién llama a esta función/archivo?"

Antes de tocar cualquier tool del lab, mapea TODAS las dependencias:
  - Qué scripts/tools referencian el archivo o la función
  - Qué crons usan qué script
  - Qué skills referencian qué tool
Genera un CHECKLIST DE IMPACTO para decidir con seguridad.

Uso:
  python3 tools/pipeline_inspector.py tools/llm_as_judge.py
  python3 tools/pipeline_inspector.py --funcion verificar_research
  python3 tools/pipeline_inspector.py --funcion main tools/registrar_hel_diario.py

Salida: checklist de impacto con callers y crons afectados.
"""

import argparse
import os
import re
import sys
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
TOOLS = LAB / "tools"
SCRIPTS = LAB / "scripts"
SKILLS = Path(os.path.expanduser("~/.hermes/skills"))
CRON_DIR = Path(os.path.expanduser("~/.hermes/cron"))
CRON_SCRIPTS = Path(os.path.expanduser("~/.hermes/scripts"))
CRON_JOBS = Path(os.path.expanduser("~/.hermes")) / "cron" / "jobs"


def _targets(ruta: str, funcion: str) -> tuple:
    """Devuelve (nombres_archivo, patrón_funcion)."""
    nombres = set()
    if ruta:
        base = Path(ruta).name
        # quitar extensión para buscar menciones sin .py
        nombres.add(base)
        nombres.add(base.rsplit(".", 1)[0] if "." in base else base)
    return nombres, funcion


def _buscar_en_archivo(path: Path, nombres: set, funcion: str) -> list:
    """Busca menciones de nombres/función en un archivo."""
    try:
        if path.stat().st_size > 2_000_000:
            return []
        texto = path.read_text(errors="ignore")
    except Exception:
        return []
    hits = []
    for n in nombres:
        if n in texto:
            hits.append(f"menciona {n}")
    if funcion and re.search(rf"\b{re.escape(funcion)}\b", texto):
        hits.append(f"llama a {funcion}()")
    return hits


def _escanear_dir(directorio: Path, nombres: set, funcion: str, limite: int = 40) -> list:
    """Escanea un directorio de archivos de texto buscando dependencias."""
    resultados = []
    if not directorio.exists():
        return resultados
    for f in sorted(directorio.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix not in (".py", ".sh", ".md", ".yaml", ".yml", ".json", ".jsonl", ".txt"):
            continue
        if any(x in str(f) for x in (".venv", ".lancedb", "__pycache__", ".git", "node_modules", ".bak")):
            continue
        hits = _buscar_en_archivo(f, nombres, funcion)
        if hits:
            resultados.append((f, hits))
            if len(resultados) >= limite:
                break
    return resultados


def _crons_relacionados(nombres: set) -> list:
    """Busca crons (jobs JSON) que referencien los scripts objetivo."""
    relacionados = []
    if CRON_JOBS.exists():
        for f in sorted(CRON_JOBS.glob("*.json")):
            try:
                contenido = f.read_text(errors="ignore")
                for n in nombres:
                    if n in contenido:
                        relacionados.append(f.name)
                        break
            except Exception:
                continue
    # también buscar en scripts de ~/.hermes/scripts
    if CRON_SCRIPTS.exists():
        for f in sorted(CRON_SCRIPTS.glob("*.sh")) + sorted(CRON_SCRIPTS.glob("*.py")):
            try:
                contenido = f.read_text(errors="ignore")
                for n in nombres:
                    if n in contenido:
                        relacionados.append(f"{f.parent.name}/{f.name}")
                        break
            except Exception:
                continue
    return relacionados


def _skills_relacionados(nombres: set, funcion: str) -> list:
    """Busca skills que referencien la tool/función."""
    relacionados = []
    if not SKILLS.exists():
        return relacionados
    for skill_dir in sorted(SKILLS.rglob("SKILL.md")):
        try:
            contenido = skill_dir.read_text(errors="ignore")
            for n in nombres:
                if n in contenido:
                    relacionados.append(str(skill_dir).replace(str(SKILLS), "~/.hermes/skills"))
                    break
        except Exception:
            continue
    return relacionados


def _checklist_impacto(encontrados: list, crons: list, skills: list) -> str:
    """Genera el checklist final de impacto."""
    lines = []
    lines.append("## ✅ Checklist de impacto")
    lines.append(f"- {'🔴' if encontrados else '🟢'} Tools/scripts afectados: {len(encontrados)}")
    lines.append(f"- {'🔴' if crons else '🟢'} Crons potencialmente afectados: {len(crons)}")
    lines.append(f"- {'🟡' if skills else '🟢'} Skills que referencian: {len(skills)}")
    if not encontrados and not crons:
        lines.append("- ✅ Sin dependencias detectadas: cambio seguro con backup (RULE-008)")
    else:
        lines.append("- ⚠️ Revisar los callers ANTES de modificar y ejecutar la suite tras el cambio")
    return "\n".join(lines)


def _imprimir_seccion(titulo: str, items: list, limite: int = 25, relativo: Path = LAB) -> None:
    """Imprime una sección de resultados (tools/crons/skills)."""
    print(f"## {titulo}")
    if items:
        for f, *resto in items[:limite]:
            if resto:
                print(f"- `{f}`: {', '.join(resto[0])}")
            else:
                print(f"- {f}")
    else:
        print("- (ninguno detectado)")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline Inspector: ¿quién toca este archivo?")
    parser.add_argument("ruta", nargs="?", help="Archivo o tool objetivo (p.ej. tools/llm_as_judge.py)")
    parser.add_argument("--funcion", default=None, help="Nombre de función a rastrear")
    args = parser.parse_args()

    if not args.ruta and not args.funcion:
        print("Uso: pipeline_inspector.py <archivo> [--funcion NOMBRE]", file=sys.stderr)
        return 2

    nombres, funcion = _targets(args.ruta or "", args.funcion)

    print(f"# 🔍 PIPELINE INSPECTOR — objetivo: {args.ruta or '(función ' + funcion + ')'}")
    print()

    if not nombres and not funcion:
        print("Sin objetivo válido.")
        return 1

    en_tools = _escanear_dir(TOOLS, nombres, funcion)
    en_scripts = _escanear_dir(SCRIPTS, nombres, funcion)
    encontrados = en_tools + en_scripts
    items_tools = [(f.relative_to(LAB), hits) for f, hits in encontrados[:25]]
    _imprimir_seccion("🛠️ Tools/scripts que lo referencian", items_tools)

    crons = _crons_relacionados(nombres)
    items_crons = [(c, []) for c in crons[:20]]
    _imprimir_seccion("⏰ Crons que podrían verse afectados", items_crons)

    skills = _skills_relacionados(nombres, funcion)
    items_skills = [(s, []) for s in skills[:15]]
    _imprimir_seccion("📚 Skills que lo referencian", items_skills)

    print()
    print(_checklist_impacto(encontrados, crons, skills))
    return 0


if __name__ == "__main__":
    sys.exit(main())
