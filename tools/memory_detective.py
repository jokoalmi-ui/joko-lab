#!/usr/bin/env python3
"""
MEMORY DETECTIVE — "¿Qué sabíamos ya de esto?"

Antes de investigar un tema desde cero, excava la memoria del lab:
  1. RAG (LanceDB joko_notes, vía search.py)
  2. research/ (análisis previos)
  3. backlog (decisiones/futuribles)
Y devuelve: lo que YA se sabe + huecos reales + qué buscar fuera.

Uso:
  python3 tools/memory_detective.py "fine-tuning vs RAG"
  python3 tools/memory_detective.py "n8n MCP" --top 5

Salida: resumen estructurado con fuentes [VERIFICADO en disco].
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
RESEARCH = LAB / "research"
BACKLOG = LAB / "04-operations" / "backlogs"
SEARCH_PY = LAB / "tools" / "search.py"


def _normalizar(tema: str) -> str:
    """Normaliza el tema para búsquedas: minúsculas, sin tildes."""
    t = tema.lower().strip()
    t = t.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return t


VENV_RAG = Path(os.path.expanduser("~/.venv/hermes-rag/bin/python"))


def _buscar_rag(tema: str, top_k: int) -> list:
    """Busca en el RAG vía search.py (devuelve lista de hits)."""
    # search.py necesita lancedb/torch → usar el venv RAG, no el python del sistema
    python = str(VENV_RAG) if VENV_RAG.exists() else sys.executable
    try:
        r = subprocess.run(
            [python, str(SEARCH_PY), "-q", tema, "-k", str(top_k)],
            capture_output=True, text=True, timeout=90,
            cwd=str(LAB),
        )
        out = r.stdout
        if r.returncode != 0:
            return [{"error": f"search.py exit {r.returncode}: {r.stderr[:200]}"}]
        # parsear salida: buscar líneas con rutas/títulos
        hits = []
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            if re.search(r"\.md|\.py|\.sh|score|relevancia|ruta|path|hit|result", line, re.I):
                hits.append(line[:200])
        return hits[:top_k * 3]
    except Exception as e:
        return [{"error": f"RAG falló: {e}"}]


def _buscar_research(tema: str) -> list:
    """Busca en research/ por nombre de archivo y contenido."""
    t = _normalizar(tema)
    palabras = [p for p in t.split() if len(p) > 2][:4]
    hits = []
    for f in sorted(RESEARCH.glob("*.md")):
        try:
            texto = f.read_text(errors="ignore")[:4000].lower()
            contenido = _normalizar(texto)
            score = 0
            for p in palabras:
                if p in contenido:
                    score += 1
            if score >= 2 or (palabras and any(p in f.name.lower() for p in palabras)):
                hits.append(f.name)
        except Exception:
            continue
    return hits[:10]


def _buscar_backlog(tema: str) -> list:
    """Busca en el backlog más reciente por contenido."""
    t = _normalizar(tema)
    palabras = [p for p in t.split() if len(p) > 2][:4]
    hits = []
    if not BACKLOG.exists():
        return hits
    b = sorted(BACKLOG.glob("*.md"))
    if not b:
        return hits
    ultimo = b[-1]
    try:
        texto = _normalizar(ultimo.read_text(errors="ignore"))
        for i, linea in enumerate(texto.splitlines()):
            if any(p in linea for p in palabras):
                hits.append(f"{ultimo.name}:{i + 1}: {linea.strip()[:160]}")
                if len(hits) >= 8:
                    break
    except Exception:
        pass
    return hits


def _resumir(tema: str, rag: list, research: list, backlog: list) -> str:
    """Construye el resumen estructurado."""
    n_rag = len([h for h in rag if "error" not in h])
    n_research = len(research)
    n_backlog = len(backlog)
    total = n_rag + n_research + n_backlog

    lines = []
    lines.append(f"# 🧠 MEMORY DETECTIVE — «{tema}»")
    lines.append("")
    lines.append(f"**Total de señales en disco: {total}** (RAG {n_rag} · research {n_research} · backlog {n_backlog})")
    lines.append("")

    if research:
        lines.append("## 📁 Ya hay research previo")
        for f in research[:6]:
            lines.append(f"- `{f}`")
        lines.append("")
        lines.append("> ✅ **Probablemente YA está investigado.** Consulta los archivos antes de buscar fuera.")
        lines.append("")
    elif total == 0:
        lines.append("## 🔍 SIN señales en disco")
        lines.append("")
        lines.append("> ⚠️ **Tema nuevo** — no hay research ni backlog previo. Buscar fuera está justificado.")
        lines.append("")

    if rag:
        lines.append("## 🗄️ Señales RAG")
        for h in rag[:5]:
            lines.append(f"- {h}")
        lines.append("")

    if backlog:
        lines.append("## 📋 Señales backlog")
        for h in backlog[:5]:
            lines.append(f"- {h}")
        lines.append("")

    lines.append("## 🎯 Conclusión")
    lines.append("")
    if n_research >= 2:
        lines.append("- **Ya está investigado** → verificar en disco, no repetir.")
        lines.append("- **Hueco posible**: solo si el research es anterior a hechos nuevos.")
    elif n_research == 1:
        lines.append("- **Hay algo previo** → revisar y decidir si el nuevo dato aporta.")
        lines.append("- **Hueco real**: evaluar si el tema evolucionó.")
    else:
        lines.append("- **Tema nuevo** → investigar desde cero está justificado.")
        lines.append("- **Fuentes a probar**: web, YT/IG, docs oficiales.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Memory Detective: ¿qué sabíamos ya de esto?")
    parser.add_argument("tema", help="Tema a buscar en la memoria del lab")
    parser.add_argument("--top", type=int, default=5, help="Resultados RAG (default 5)")
    args = parser.parse_args()

    print(f"Buscando «{args.tema}» en la memoria del lab...", file=sys.stderr)
    rag = _buscar_rag(args.tema, args.top)
    research = _buscar_research(args.tema)
    backlog = _buscar_backlog(args.tema)
    print(_resumir(args.tema, rag, research, backlog))
    return 0


if __name__ == "__main__":
    sys.exit(main())
