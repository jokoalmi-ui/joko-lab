#!/usr/bin/env python3
"""
generar_indice_okf.py — Índice de Knowledge Objects CON VIGENCIA (OKF).

Adaptado del script de referencia (SCRIPT RAG+OKF/generar_indice.py):
- Usa `body` (los KOs no tienen summary) SIN truncar por "." (evita
  "Qwen 3.5" -> "Qwen 3").
- Usa nombre corto del fichero (no ruta completa: pesa menos).
- AÑADE VIGENCIA al índice: status, expires, next_review, superseded_by.
  Sin esto el LLM sabe QUÉ existe pero no QUÉ está vigente (fallo EXP-1/EXP-3).
- Scope explícito + nota anti falso negativo.

Uso:
    python3 generar_indice_okf.py --output ~/joko-lab/verification/indice-okf.md
"""
import argparse
import sys
from pathlib import Path

import yaml


def cargar_ko(ruta: Path) -> dict | None:
    try:
        data = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [AVISO] no se pudo parsear {ruta}: {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict) or "type" not in data:
        return None
    return data


def construir_indice(kos_dir: Path, scope: str) -> str:
    ficheros = sorted(kos_dir.glob("*.yaml")) + sorted(kos_dir.glob("*.yml"))
    lineas = [
        "# Índice de Knowledge Objects — Joko Lab",
        f"# scope: {scope}",
        "# NOTA PARA EL AGENTE: este índice cubre SOLO el scope declarado.",
        "# Si la pregunta cae fuera de ese scope, NO concluyas 'no existe' --",
        "# consulta el RAG antes de responder que algo no está incluido.",
        "# VIGENCIA: si un KO tiene superseded_by o status distinto de activo,",
        "# NO lo cites como vigente. El KO que lo sustituye es el que manda.",
        "",
    ]
    total = 0
    for f in ficheros:
        if "template" in f.name or ".bak-" in f.name:
            continue
        ko = cargar_ko(f)
        if ko is None:
            continue
        total += 1
        kid = str(ko.get("id", f.stem))
        ktype = str(ko.get("type", "?"))
        estado = str(ko.get("status", "sin-status"))
        exp = ko.get("expires") or "-"
        sup = ko.get("superseded_by") or "-"
        # Las RULEs recientes guardan la descripcion en 'desc', no en 'body':
        # sin el fallback el indice las listaba con el campo vacio (RULE-014..018).
        body = str(ko.get("body") or ko.get("desc") or "").strip().replace("\n", " ")
        if len(body) > 160:
            body = body[:160].rstrip() + "..."
        # Trampa de nombres: usar ID completo siempre
        lineas.append(
            f"- {kid} [{ktype}/{estado}] exp:{exp} sup:{sup} | {body}"
        )
    lineas.append("")
    lineas.append(f"# Total: {total} objetos indexados")
    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kos-dir", default=str(Path.home() / "joko-lab/01-knowledge/objects"))
    parser.add_argument("--output", default=str(Path.home() / "joko-lab/verification/indice-okf.md"))
    parser.add_argument("--scope", default="decisions_rules_policies_predictions_only")
    args = parser.parse_args()

    kos_dir = Path(args.kos_dir)
    if not kos_dir.is_dir():
        print(f"Directorio no encontrado: {kos_dir}", file=sys.stderr)
        sys.exit(1)

    indice = construir_indice(kos_dir, args.scope)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(indice, encoding="utf-8")
    print(indice)
    aprox = len(indice) // 4
    print(f"\n--- Guardado en {out} ---")
    print(f"Tamaño aproximado: ~{aprox} tokens (heurística 4c/token)")


if __name__ == "__main__":
    main()
