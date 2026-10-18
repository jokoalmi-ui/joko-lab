#!/usr/bin/env python3
"""evidence.py — F2.5 del OBSERVER.

Convierte METRICS (numeros sin interpretar) en OBS-XXX (observaciones
factuales). No propone cambios, no fija umbrales: solo registra hechos
observables (top, porcentajes, ceros, totales) en 01-knowledge/observations/.

Uso:
  python3 evidence.py [--fecha YYYY-MM-DD]
"""
import argparse
import json
import os
from datetime import date

OBS_DIR = os.path.expanduser("~/joko-lab/01-knowledge/observations")
METRICS_DIR = os.path.expanduser("~/joko-lab/04-operations/metrics/telemetria")


def proximo_obs_id():
    """Siguiente OBS-NNN segun archivos existentes en observations/."""
    max_n = 0
    if os.path.isdir(OBS_DIR):
        for fn in os.listdir(OBS_DIR):
            m = fn.startswith("OBS-")
            if m:
                try:
                    n = int(fn.split("-")[1])
                    if n > max_n:
                        max_n = n
                except Exception:
                    pass
    return max_n + 1


def escribir_obs(obs_id, titulo, cuerpo, fecha):
    os.makedirs(OBS_DIR, exist_ok=True)
    slug = titulo.lower().replace(" ", "-")[:40]
    # Dedupe: si ya existe una OBS con el mismo patron y la misma fecha, saltar
    if os.path.isdir(OBS_DIR):
        for fn in os.listdir(OBS_DIR):
            if fn.startswith("OBS-") and fn.endswith(".md") and slug in fn:
                fp = os.path.join(OBS_DIR, fn)
                try:
                    with open(fp, encoding="utf-8") as f:
                        if f"Fecha: {fecha}" in f.read():
                            return None  # ya existe hoy
                except Exception:
                    pass
    path = os.path.join(OBS_DIR, f"OBS-{obs_id:03d}-{slug}.md")
    contenido = (
        f"---\n"
        f"type: knowledge\n"
        f"subtype: observation\n"
        f"status: active\n"
        f"tags: [knowledge, observation, telemetria]\n"
        f"created: {fecha}\n"
        f"---\n"
        f"# OBS-{obs_id:03d}: {titulo}\n"
        f"===============================================\n\n"
        f"## Datos basicos\n"
        f"  ID: OBS-{obs_id:03d}\n"
        f"  Fecha: {fecha}\n"
        f"  Origen: telemetria (observer.py)\n\n"
        f"## Observacion\n\n{cuerpo}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    return path


def _cuerpo_decisiones_por_politica(pols, total):
    """Cuerpo de la observacion de distribucion de decisiones por politica."""
    # 1. Distribucion de decisiones por politica
    if not pols or not total:
        return None
    top = list(pols.items())[:3]
    cuerpo = "Distribucion de decisiones por politica:\n\n"
    for pol, n in top:
        cuerpo += f"- {pol}: {n} ({100*n/total:.1f}%)\n"
    cuerpo += f"\nTotal: {total} decisiones."
    return cuerpo


def _cuerpo_fallback_rate(fr, total, fecha):
    """Cuerpo de la observacion de fallback rate."""
    # 2. Fallback rate
    if not total or fr is None:
        return None
    return f"Fallback rate (Disponibilidad) el {fecha}: {fr:.1%} de {total} decisiones."


def _cuerpo_uso_rules(rules, nunca):
    """Cuerpo de la observacion de uso de RULEs."""
    # 3. RULE mas activada / nunca activadas
    if not rules:
        return None
    top_rule, top_n = list(rules.items())[0]
    cuerpo = f"RULE mas activada: {top_rule} ({top_n} activaciones)."
    if nunca:
        cuerpo += f"\nReglas nunca activadas: {', '.join(nunca)}."
    return cuerpo


def _cuerpo_uso_rag(paths, nunca_rag):
    """Cuerpo de la observacion de uso de RAG."""
    # 4. KO mas recuperado / nunca recuperados
    if not paths:
        return None
    top_path, top_n = list(paths.items())[0]
    cuerpo = f"Documento mas recuperado: {top_path} ({top_n} veces)."
    if nunca_rag:
        cuerpo += f"\nKOs nunca recuperados: {', '.join(nunca_rag)}."
    return cuerpo


def _registrar_obs(creadas, obs_id, p):
    """Registra la observacion creada y devuelve el siguiente obs_id."""
    if p:
        creadas.append(p)
        obs_id += 1
    return obs_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=None)
    args = ap.parse_args()
    fecha = args.fecha or date.today().isoformat()

    mp = os.path.join(METRICS_DIR, fecha + ".json")
    if not os.path.exists(mp):
        print(f"Sin metrics para {fecha}. Ejecuta observer.py primero.")
        return
    with open(mp, encoding="utf-8") as f:
        m = json.load(f)

    obs_id = proximo_obs_id()
    creadas = []

    pols = m.get("decisiones", {}).get("por_politica", {})
    total = m.get("decisiones", {}).get("total", 0)
    cuerpo = _cuerpo_decisiones_por_politica(pols, total)
    if cuerpo is not None:
        p = escribir_obs(obs_id, f"Decisiones por politica ({fecha})", cuerpo, fecha)
        obs_id = _registrar_obs(creadas, obs_id, p)

    fr = m.get("decisiones", {}).get("fallback_rate", 0.0)
    cuerpo = _cuerpo_fallback_rate(fr, total, fecha)
    if cuerpo is not None:
        p = escribir_obs(obs_id, f"Fallback rate {fecha}", cuerpo, fecha)
        obs_id = _registrar_obs(creadas, obs_id, p)

    rules = m.get("activaciones", {}).get("por_rule", {})
    nunca = m.get("activaciones", {}).get("reglas_nunca_activadas", [])
    cuerpo = _cuerpo_uso_rules(rules, nunca)
    if cuerpo is not None:
        p = escribir_obs(obs_id, f"Uso de RULEs {fecha}", cuerpo, fecha)
        obs_id = _registrar_obs(creadas, obs_id, p)

    paths = m.get("rag", {}).get("paths_top", {})
    nunca_rag = m.get("rag", {}).get("kos_nunca_recuperados", [])
    cuerpo = _cuerpo_uso_rag(paths, nunca_rag)
    if cuerpo is not None:
        p = escribir_obs(obs_id, f"Uso RAG {fecha}", cuerpo, fecha)
        obs_id = _registrar_obs(creadas, obs_id, p)

    print(f"OK evidence {fecha}: {len(creadas)} observaciones creadas")
    for c in creadas:
        print(" -", c)


if __name__ == "__main__":
    main()
