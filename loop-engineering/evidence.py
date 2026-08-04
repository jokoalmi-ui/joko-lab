#!/usr/bin/env python3
"""
F2 — Evidence Dashboard (Loop Engineering L2) — 04-ago-2026
Responde preguntas con datos del ledger. Es un dashboard, NO un sistema de
decision. No propone cambios, no toca policies, no calcula umbrales a priori.

Preguntas que responde (limitado a la realidad del ledger, 328 entradas):
- Que reglas se activan realmente y que % del trafico cubren
- Reglas definidas en policies/ que NUNCA aparecen en el ledger
- Distribucion temporal (por dia)
- Distribucion por provider y modelo
- Concentracion de la toma de decisiones (que regla domina)

NO responde (el ledger no lo registra): exito/fallo por decision, tipo de
tarea, agente, incertidumbre. Se documenta como limitacion, no se inventa.
"""
import json
import collections
import glob
import os
import yaml

LEDGER = "/mnt/ssd_ia_datos/lab-state/decision-ledger.jsonl"
POLICIES_DIR = "/mnt/ssd_ia_datos/lab-state/policies"


def extraer_regla(reason):
    if not reason:
        return "sin_reason"
    prefijo = reason.split(":")[0].split(" ")[0].strip()
    return prefijo if prefijo else "sin_reason"


def reglas_definidas():
    """Reglas declaradas en los YAML de policies/ (si se pueden leer)."""
    reglas = set()
    for f in glob.glob(os.path.join(POLICIES_DIR, "*.yaml")):
        try:
            d = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and "rules" in d and isinstance(d["rules"], list):
            for r in d["rules"]:
                if isinstance(r, dict) and "name" in r:
                    reglas.add(r["name"])
        if isinstance(d, dict) and "id" in d:
            reglas.add(d["id"])
    return reglas


def main():
    entradas = []
    for line in open(LEDGER, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                entradas.append(json.loads(line))
            except Exception:
                pass

    total = len(entradas)
    por_regla = collections.Counter(extraer_regla(e.get("reason")) for e in entradas)
    por_provider = collections.Counter(e.get("provider") or "desconocido" for e in entradas)
    por_modelo = collections.Counter(e.get("model") or "desconocido" for e in entradas)
    por_dia = collections.Counter((e.get("timestamp") or "")[:10] for e in entradas if e.get("timestamp"))

    print("=" * 62)
    print("  EVIDENCE DASHBOARD — Loop Engineering L2 (04-ago-2026)")
    print("=" * 62)
    print(f"  Entradas totales: {total}")
    print(f"  Rango de dias:    {min(por_dia) if por_dia else '-'} a {max(por_dia) if por_dia else '-'}")
    print()

    print("1) REGLAS ACTIVAS (% del trafico)")
    print("-" * 62)
    for regla, n in por_regla.most_common():
        print(f"   {regla:<14} {n:>5}  {100*n/total:5.1f}%")
    print()

    print("2) REGLAS DEFINIDAS EN POLICIES QUE NUNCA SE USAN")
    print("-" * 62)
    definidas = reglas_definidas()
    usadas = set(por_regla.keys())
    nunca = sorted(definidas - usadas)
    if nunca:
        for r in nunca:
            print(f"   [NUNCA USADA] {r}")
    else:
        print("   (todas las reglas declaradas aparecen en el ledger o policies vacias)")
    print()

    print("3) DISTRIBUCION TEMPORAL (por dia)")
    print("-" * 62)
    for dia in sorted(por_dia):
        barra = "#" * int(por_dia[dia] / max(1, max(por_dia.values())) * 30)
        print(f"   {dia}  {por_dia[dia]:>3}  {barra}")
    print()

    print("4) POR PROVIDER")
    print("-" * 62)
    for prov, n in por_provider.most_common():
        print(f"   {prov:<14} {n:>5}  {100*n/total:5.1f}%")
    print()

    print("5) POR MODELO")
    print("-" * 62)
    for mod, n in por_modelo.most_common(10):
        print(f"   {mod:<22} {n:>5}  {100*n/total:5.1f}%")
    print()

    print("6) CONCENTRACION (top-1 regla)")
    print("-" * 62)
    top = por_regla.most_common(1)
    if top:
        r, n = top[0]
        print(f"   {r} decide el {100*n/total:.1f}% del trafico ({n}/{total})")
        print("   -> Se DECIDE el umbral con estos datos; no a priori (decisión 04-ago).")
    print()

    print("LIMITACIONES (realidad del ledger):")
    print("   - No registra exito/fallo por decision (no hay 'times_success').")
    print("   - No registra tipo de tarea ni agente.")
    print("   - 'Reglas nunca usadas' = declaradas en policies/ que no aparecen en el ledger.")


if __name__ == "__main__":
    main()
