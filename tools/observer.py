#!/usr/bin/env python3
"""observer.py — F1+F2 del OBSERVER (telemetria del proceso de decision).

Lee los ledgers (decision, activation, rag-query) y produce METRICS sin
interpretar: numeros y porcentajes. No modifica nada. No fija umbrales.

Salida:
  ~/joko-lab/04-operations/metrics/telemetria/YYYY-MM-DD.md  (legible)
  ~/joko-lab/04-operations/metrics/telemetria/YYYY-MM-DD.json (para evidence.py)

Uso:
  python3 observer.py [--fecha YYYY-MM-DD]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import date, datetime

LAB_STATE = "/mnt/ssd_ia_datos/lab-state/"
DECISION_LEDGER = os.path.join(LAB_STATE, "decision-ledger.jsonl")
ACTIVATION_LEDGER = os.path.join(LAB_STATE, "activation-ledger.jsonl")
RAG_LEDGER = os.path.join(LAB_STATE, "rag-query-ledger.jsonl")
OBJECTS_DIR = os.path.expanduser("~/joko-lab/01-knowledge/objects")
OUT_DIR = os.path.expanduser("~/joko-lab/04-operations/metrics/telemetria")


def leer_jsonl(path):
    filas = []
    if not os.path.exists(path):
        return filas
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    filas.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        pass
    return filas


def politica_de_reason(reason):
    if not reason:
        return "desconocido"
    m = re.match(r"^([^:]+):", reason)
    return m.group(1).strip() if m else reason[:30]


def calcular_metricas_activaciones(activations, conocidas):
    rule_counter = Counter()
    pol_act_counter = Counter()
    blocks_counter = Counter()
    ms_counter = Counter()
    for a in activations:
        for rid in (a.get("active_rules") or []):
            rule_counter[str(rid)] += 1
        for pid in (a.get("policies") or []):
            pol_act_counter[str(pid)] += 1
        for bid in (a.get("blocks") or []):
            blocks_counter[str(bid)] += 1
        ms = a.get("model_selection")
        if ms:
            ms_counter[str(ms)] += 1
    # Una RULE "participó" si aparece en cualquiera de los canales: active_rules,
    # blocks o model_selection. Antes solo se contaba active_rules, que siempre
    # sale vacío (las RULEs de modelo aparecen como model_selection) -> falso
    # negativo "nunca activadas" (lección: validar el instrumento, caso 07-ago).
    participaron = set(rule_counter.keys()) | set(blocks_counter.keys()) | set(ms_counter.keys())
    nunca_activadas = sorted(conocidas - participaron)
    por_tipo = {}
    for k in nunca_activadas:
        pref = k.split("-")[0]
        por_tipo[pref] = por_tipo.get(pref, 0) + 1
    return rule_counter, pol_act_counter, blocks_counter, ms_counter, nunca_activadas, por_tipo


def _cargar_kos_conocidas(prefix=""):
    items = set()
    try:
        for fn in os.listdir(OBJECTS_DIR):
            if fn.endswith(".yaml") and "template" not in fn and fn.startswith(prefix):
                items.add(fn.replace(".yaml", ""))
    except Exception:
        pass
    return items


def _metricas_decisiones(decisions, total_dec):
    pol_counter = Counter(politica_de_reason(d.get("reason")) for d in decisions)
    por_dia = Counter((d.get("timestamp") or "")[:10] for d in decisions)
    fallback = pol_counter.get("Disponibilidad", 0)
    return {
        "pol_counter": pol_counter,
        "por_dia": por_dia,
        "fallback": fallback,
        "por_politica": dict(pol_counter.most_common()),
        "sorted_por_dia": dict(sorted(por_dia.items())[-10:]),
        "fallback_rate": round(fallback / total_dec, 4) if total_dec else 0.0,
    }


def _metricas_activaciones(activations, conocidas):
    rule_counter, pol_act_counter, blocks_counter, ms_counter, nunca_activadas, _por_tipo = calcular_metricas_activaciones(activations, conocidas)
    total_act = len(activations)
    return {
        "total": total_act,
        "rule_counter": rule_counter,
        "pol_act_counter": pol_act_counter,
        "blocks_counter": blocks_counter,
        "ms_counter": ms_counter,
        "nunca_activadas": nunca_activadas,
        "por_rule": dict(rule_counter.most_common()),
        "por_politica_activada": dict(pol_act_counter.most_common()),
        "blocks": dict(blocks_counter.most_common()),
        "model_selection": dict(ms_counter.most_common()),
        "reglas_conocidas": len(conocidas),
        "reglas_nunca_activadas": nunca_activadas,
    }


def _metricas_rag(rag, kos):
    path_counter = Counter()
    for q in rag:
        for p in (q.get("paths") or []):
            path_counter[str(p)] += 1
    total_rag = len(rag)
    recuperados_ids = set()
    for p in path_counter:
        for k in kos:
            if k in p:
                recuperados_ids.add(k)
    nunca_recuperados = sorted(kos - recuperados_ids)
    por_tipo = {}
    for k in nunca_recuperados:
        pref = k.split("-")[0]
        por_tipo[pref] = por_tipo.get(pref, 0) + 1
    return {
        "path_counter": path_counter,
        "total_rag": total_rag,
        "nunca_recuperados": nunca_recuperados,
        "por_tipo": por_tipo,
        "paths_top": dict(path_counter.most_common(15)),
        "kos_conocidos": len(kos),
        "kos_nunca_recuperados": nunca_recuperados,
        "no_recuperados_por_tipo": por_tipo,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=None)
    args = ap.parse_args()
    hoy = args.fecha or date.today().isoformat()

    decisions = leer_jsonl(DECISION_LEDGER)
    activations = leer_jsonl(ACTIVATION_LEDGER)
    rag = leer_jsonl(RAG_LEDGER)

    total_dec = len(decisions)
    md = _metricas_decisiones(decisions, total_dec)

    conocidas = _cargar_kos_conocidas("RULE-")
    ma = _metricas_activaciones(activations, conocidas)

    kos = _cargar_kos_conocidas()
    mr = _metricas_rag(rag, kos)

    metrics = {
        "fecha": hoy,
        "decisiones": {
            "total": total_dec,
            "por_politica": md["por_politica"],
            "por_dia": md["sorted_por_dia"],
            "fallback_rate": md["fallback_rate"],
        },
        "activaciones": {
            "total": ma["total"],
            "por_rule": ma["por_rule"],
            "por_politica_activada": ma["por_politica_activada"],
            "blocks": ma["blocks"],
            "model_selection": ma["model_selection"],
            "reglas_conocidas": ma["reglas_conocidas"],
            "reglas_nunca_activadas": ma["reglas_nunca_activadas"],
        },
        "rag": {
            "total_consultas": mr["total_rag"],
            "paths_top": mr["paths_top"],
            "kos_conocidos": mr["kos_conocidos"],
            "kos_nunca_recuperados": mr["kos_nunca_recuperados"],
            "no_recuperados_por_tipo": mr["no_recuperados_por_tipo"],
        },
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, hoy + ".json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append(f"# Telemetria {hoy}")
    lines.append("")
    lines.append(f"## Decisiones ({total_dec})")
    if total_dec:
        for pol, n in md["pol_counter"].most_common():
            lines.append(f"- {pol}: {n} ({100*n/total_dec:.1f}%)")
        lines.append(f"- **fallback rate: {md['fallback_rate']:.1%}**")
    lines.append("")
    lines.append(f"## Activaciones ({ma['total']})")
    for rid, n in ma["rule_counter"].most_common(15):
        lines.append(f"- {rid}: {n}")
    if ma["ms_counter"]:
        lines.append(f"- model_selection: {', '.join(f'{k} ({v})' for k, v in ma['ms_counter'].most_common())}")
    if ma["blocks_counter"]:
        lines.append(f"- blocks: {', '.join(f'{k} ({v})' for k, v in ma['blocks_counter'].most_common())}")
    if ma["nunca_activadas"]:
        lines.append(f"- **Nunca participaron: {', '.join(ma['nunca_activadas'])}**")
    lines.append("")
    lines.append(f"## RAG ({mr['total_rag']} consultas)")
    for p, n in mr["path_counter"].most_common(10):
        lines.append(f"- {p}: {n}")
    if mr["nunca_recuperados"]:
        lines.append(f"- **KOs no recuperados en el periodo (mide universo de consultas, NO recuperabilidad; verificar con consulta dirigida): {', '.join(mr['nunca_recuperados'])}**")
        lines.append(f"- desglose por tipo: {', '.join(f'{t}: {n}' for t, n in sorted(mr['por_tipo'].items()))}")

    with open(os.path.join(OUT_DIR, hoy + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"OK telemetria {hoy}: decisiones={total_dec} activaciones={ma['total']} rag={mr['total_rag']}")
    print("Informe:", os.path.join(OUT_DIR, hoy + ".md"))


if __name__ == "__main__":
    main()
