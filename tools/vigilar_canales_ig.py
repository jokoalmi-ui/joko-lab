#!/usr/bin/env python3
"""vigilar_canales_ig.py — Detecta posts nuevos en los canales vigilados.

Patrón: navega al perfil de cada canal, extrae los shortcodes de los últimos
~12 posts, compara con los ya analizados (backlog + research), e imprime los
nuevos. Vacío = silencio (patrón watchdog).

USO (con el navegador ya abierto en el perfil):
    (este script depende del browser — se usa via la skill instagram-monitor)
"""
import os
import re
import sys

# Canales vigilados (fuente de verdad: skill instagram-monitor/SKILL.md)
# ---------------------------------------------------------------------------
# Lista de canales vigilados.
# Fuente de verdad LEGIBLE: skill `instagram-monitor` (SKILL.md, bloque verde).
# Aviso: el cron `vigilar-canales-ig` (4d64ff821685) es un job de AGENTE: la
# lista que navega de verdad vive en su PROMPT, no aqui. Mantener los tres
# sitios sincronizados (prompt del cron <-> este bloque <-> skill).
# DIETA CERRADA (19-sep -> 03-oct-2026). MEDIDO el 04-oct: la tasa de aplicabilidad
# NO subio con la lista corta -> decision del usuario (04-oct): REACTIVAR los 10 canales
# de apuntes/bait/roadmap. Quedan vigilados de nuevo, con PRIORIDAD BAJA (46 % del flujo:
# 397/894 piezas en 31 dias, ~0 entradas reales) -> el aviso prioriza el nucleo IA.
# ---------------------------------------------------------------------------
CANALES = [
    # Nucleo IA (mantener)
    "mentalhotfix", "datasciencebrain", "dailydoseofds_", "ds_ai_ketan",
    "shiva.bytes", "tarnannrakhangi", "aiseekhobhai", "codewithbrij",
    "codeby.akash", "hackproduct", "deadlockdreams", "thevectorforge",
]

# REACTIVADOS el 04-oct-2026 (dieta cerrada): se navegan y listan de nuevo, pero
# con PRIORIDAD BAJA. NO analizar a fondo salvo que el titulo lo justifique.
# (Nombre anterior de esta lista: CANALES_PAUSA_2SEM — obsoleto, dieta cerrada.)
CANALES_REACTIVADOS = [
    "maurys_alvarez_", "qa_insights", "marketingwithgaurav", "datastreakofficial",
    "codedsoul_05", "abhi_techhub", "codeera.tech", "bazarfungi.chile",
    "_coder_star", "learnbayofficial",
]

# Canales de FINANZAS/BOLSA (alta 10-oct-2026): contenido en espanol con CIFRAS
# comprobables; alimenta bolsa-autonoma (EXP-002) y el dominio financiero del lab.
# Prioridad BAJA: no gasta pipeline tecnico; se analiza solo si trae cifras nuevas.
CANALES_FINANZAS = [
    "invertir_aprendiendo",
]

# `gauravgoyalai` NO se vigila como fuente de tecnica: banco de referencia de
# FORMATO para infografias propias (ver skill instagram-monitor).


BACKLOG = "/home/jokoalmi/joko-lab/04-operations/backlogs/2026-07-31-backlog.md"
RESEARCH_DIR = "/home/jokoalmi/joko-lab/research"


def shortcodes_analizados() -> set:
    """Reúne todos los shortcodes de IG mencionados en backlog y research."""
    codes = set()
    # Backlog
    if os.path.exists(BACKLOG):
        with open(BACKLOG, encoding="utf-8") as f:
            content = f.read()
        codes.update(re.findall(r"[A-Za-z0-9_-]{11}", content))
    # Research (patrón de URL de IG)
    for fn in os.listdir(RESEARCH_DIR):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(RESEARCH_DIR, fn), encoding="utf-8") as f:
            content = f.read()
        codes.update(re.findall(r"instagram\.com/(?:p|reel)/([A-Za-z0-9_-]{11})", content))
    return codes


def main():
    """Nota: la extracción de shortcodes por canal se hace desde el navegador
    (la skill instagram-monitor lo documenta). Este script procesa los códigos
    ya extraídos (pasados por stdin, uno por línea) y los compara."""
    analizados = shortcodes_analizados()
    nuevos = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        partes = line.split()
        canal, code = partes[0], partes[1]
        if code not in analizados:
            nuevos.append((canal, code))

    if not nuevos:
        print("(sin novedades)")
        return

    print(f"📡 {len(nuevos)} posts nuevos no analizados:")
    for canal, code in nuevos:
        print(f"  · https://www.instagram.com/{canal}/p/{code}/")


if __name__ == "__main__":
    main()
