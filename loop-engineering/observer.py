#!/usr/bin/env python3
"""
F1 — Observer (Loop Engineering L2) — 04-ago-2026
Convierte decision-ledger.jsonl en estadisticas reales.
NO interpreta. NO propone. NO calcula umbrales. Solo transforma en hechos.

Salida: JSON con frecuencias por regla/provider/model + hechos temporales.

Realidad del ledger (verificada 04-ago, 328 entradas):
- Campos: timestamp, provider, model, reason, nivel, temperature, max_tokens
- NO existe campo de exito/fallo ni de contexto de tarea -> no se inventan.
- La regla se infiere del prefijo del reason ("Gpu:", "Horario:", ...).
"""
import json
import collections
import datetime

LEDGER = "/mnt/ssd_ia_datos/lab-state/decision-ledger.jsonl"


def extraer_regla(reason):
    """Prefijo del motivo = regla que decidio. 'Gpu: GPU: VRAM baja...' -> 'Gpu'."""
    if not reason:
        return "sin_reason"
    prefijo = reason.split(":")[0].split(" ")[0].strip()
    return prefijo if prefijo else "sin_reason"


def main():
    entradas = []
    corruptas = 0
    for line in open(LEDGER, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            entradas.append(json.loads(line))
        except Exception:
            corruptas += 1

    por_regla = collections.Counter()
    por_provider = collections.Counter()
    por_modelo = collections.Counter()
    por_dia = collections.Counter()
    por_regla_provider = collections.defaultdict(collections.Counter)

    primer_ts = {}
    ultimo_ts = {}
    rules_models = collections.defaultdict(set)

    for e in entradas:
        regla = extraer_regla(e.get("reason"))
        provider = e.get("provider") or "desconocido"
        modelo = e.get("model") or "desconocido"
        ts = e.get("timestamp") or ""

        por_regla[regla] += 1
        por_provider[provider] += 1
        por_modelo[modelo] += 1
        por_regla_provider[regla][provider] += 1
        rules_models[regla].add(modelo)

        if ts:
            dia = str(ts)[:10]
            por_dia[dia] += 1
            if regla not in primer_ts or ts < primer_ts[regla]:
                primer_ts[regla] = ts
            if regla not in ultimo_ts or ts > ultimo_ts[regla]:
                ultimo_ts[regla] = ts

    # Hechos por regla
    hechos = []
    for regla, n in por_regla.most_common():
        hechos.append({
            "regla": regla,
            "veces_usada": n,
            "primer_uso": primer_ts.get(regla, ""),
            "ultimo_uso": ultimo_ts.get(regla, ""),
            "providers": dict(por_regla_provider[regla]),
            "modelos": sorted(rules_models[regla]),
        })

    salida = {
        "fuente": LEDGER,
        "generado": datetime.datetime.now().isoformat(timespec="seconds"),
        "entradas_total": len(entradas),
        "lineas_corruptas": corruptas,
        "reglas_distintas": len(por_regla),
        "por_regla": hechos,
        "por_provider": dict(por_provider),
        "por_modelo": dict(por_modelo),
        "por_dia": dict(sorted(por_dia.items())),
        "notas": [
            "El ledger NO registra exito/fallo: solo frecuencias, sin resultado.",
            "El ledger NO registra contexto de tarea ni agente.",
            "La regla se infiere del prefijo del reason (formato del DE).",
        ],
    }
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
