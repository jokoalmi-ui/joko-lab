#!/usr/bin/env python3
"""descargar_modelos_inactivos.py — Descarga modelos de LM Studio por inactividad.

Comprueba si hay un modelo cargado y si el server de LM Studio lleva más de
INACTIVIDAD_MIN sin peticiones REALES de inferencia (chat/completions o
embeddings en el log del server). Si es así, descarga el modelo cargado.

Proxy de actividad: la última línea "Received request: POST to
/api/v0/chat/completions" o "/api/v0/embeddings" del log del server.
NO se usa el mtime del log porque las consultas de estado (GET /models) lo
actualizan constantemente (validado 12-ago: el mtime cambia con cada check).

Patrón "LM Studio libre sin ocupar GPU" (idea del usuario, 11-ago-2026):
- Carga bajo demanda: llm-router.sh (implementado)
- Swap automático: llm-router.sh (implementado)
- ESTE script: la pieza que faltaba — descarga por inactividad.

Cron sugerido: cada 30 min. Umbral: 30 min sin inferencia.

Silencio si no hay nada que hacer (patrón watchdog).
"""
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone, timedelta

INACTIVIDAD_MIN = 30          # minutos sin inferencia antes de descargar
SERVER_LOGS = os.path.expanduser('~/.lmstudio/server-logs')
LM_API = 'http://localhost:1234/api/v0/models'
TZ = timezone(timedelta(hours=2))

# Patrones de inferencia real (los GET /models NO cuentan)
PATRON_INFERENCIA = re.compile(
    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(chat/completions|embeddings)')

def modelo_cargado() -> str | None:
    """Devuelve el id del modelo cargado (o None)."""
    try:
        import urllib.request
        with urllib.request.urlopen(LM_API, timeout=5) as r:
            d = json.loads(r.read())
        for m in d.get('data', []):
            if m.get('state') == 'loaded':
                return m.get('id')
    except Exception:
        return None
    return None

def log_mas_reciente() -> str | None:
    """Último log del server de LM Studio (por mtime)."""
    if not os.path.isdir(SERVER_LOGS):
        return None
    mejor = None
    mejor_mtime = 0
    for raiz, _, archivos in os.walk(SERVER_LOGS):
        for a in archivos:
            if a.endswith('.log'):
                p = os.path.join(raiz, a)
                mt = os.path.getmtime(p)
                if mt > mejor_mtime:
                    mejor_mtime = mt
                    mejor = p
    return mejor

def ultima_inferencia(log: str) -> float | None:
    """Timestamp (epoch) de la última petición real de inferencia en el log."""
    ultimo = None
    try:
        with open(log, encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = PATRON_INFERENCIA.search(line)
                if m:
                    try:
                        ts = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')
                        ts = ts.replace(tzinfo=TZ)
                        ultimo = ts.timestamp()
                    except ValueError:
                        continue
    except Exception:
        return None
    return ultimo

def main():
    modelo = modelo_cargado()
    if not modelo:
        return  # sin modelo cargado → nada que hacer (silencio)

    log = log_mas_reciente()
    if not log:
        print(f'📴 [descargador-inactividad] {modelo} cargado pero sin log — se deja.')
        return

    ultima = ultima_inferencia(log)
    if ultima is None:
        # No hay registro de inferencia en el log de hoy (puede ser log nuevo
        # o el modelo se cargó sin inferir todavía) — NO descargar (prudente)
        return

    inactivo_min = (time.time() - ultima) / 60
    if inactivo_min < INACTIVIDAD_MIN:
        return  # hubo inferencia reciente → no descargar (silencio)

    # Inactivo el tiempo suficiente → descargar
    print(f'📴 [descargador-inactividad] {modelo} lleva {inactivo_min:.0f} min sin inferencia — descargando (libera VRAM).')
    try:
        subprocess.run(['lms', 'unload', modelo], capture_output=True, text=True, timeout=60)
    except Exception as e:
        print(f'  ERROR descargando: {e}')
        return
    time.sleep(2)
    if not modelo_cargado():
        print(f'  ✅ {modelo} descargado — LM Studio libre.')
    else:
        print(f'  ⚠️ {modelo} sigue cargado (puede estar en uso) — no se fuerza.')

if __name__ == '__main__':
    main()
