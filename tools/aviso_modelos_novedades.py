#!/usr/bin/env python3
"""Watchdog de NOVEDADES del registro de candidatos a modelo local (12GB VRAM).

Patron cron no_agent: imprime SOLO si hay candidatos con avisado=false;
stdout vacio = silencio (nada nuevo que contar). Marca como avisados los que
imprime, para que cada novedad se avise UNA sola vez.

Registro (memoria del cron investigacion-modelos-locales-semanal):
  /home/jokoalmi/joko-lab/04-operations/metrics/modelos-locales/candidatos-modelos-locales.json

Reglas del lab: solo lee/escribe ese JSON (backup .bak-<fecha> antes de tocarlo),
no descarga ni carga modelos, no toca n8n/Docker/systemd.
"""
import json
import os
import shutil
import sys
from datetime import date

REGISTRO = ("/home/jokoalmi/joko-lab/04-operations/metrics/"
            "modelos-locales/candidatos-modelos-locales.json")


def leer(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def pendientes(datos):
    return [c for c in datos.get("candidatos", []) if c.get("avisado") is not True]


def formatear(cands):
    lineas = [f"🔔 Novedades en modelos locales: {len(cands)}", ""]
    for c in cands:
        veredicto = c.get("veredicto_actual", "")
        lineas.append(f"• {c['nombre']} — {c.get('estado', '?')} {veredicto}".rstrip())
        detalle = c.get("nota") or c.get("evidencia") or ""
        if detalle:
            lineas.append(f"   {detalle}")
    lineas += ["", "Registro: 04-operations/metrics/modelos-locales/candidatos-modelos-locales.json",
               "Nada se descarga ni se prueba sin tu OK (JL-006)."]
    return "\n".join(lineas)


def guardar(ruta, datos, hoy):
    bak = f"{ruta}.bak-{hoy}"
    if not os.path.exists(bak):
        shutil.copy2(ruta, bak)
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.replace(tmp, ruta)


def main():
    datos = leer(REGISTRO)
    nuevos = pendientes(datos)
    if not nuevos:
        return 0
    print(formatear(nuevos))
    for cand in nuevos:
        cand["avisado"] = True
    datos["actualizado"] = date.today().isoformat()
    guardar(REGISTRO, datos, datos["actualizado"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
