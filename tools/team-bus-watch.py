#!/usr/bin/env python3
"""
team-bus-watch.py — Daemon de latencia corta para el file bus (fase 2).

Polling de 5s sobre ~/.hermes/team-context/. Cuando un archivo cambia:
1. Regenera un snapshot consolidado (team-context/README.md) con todos los dominios
2. Actualiza shared-state.json con un "último cambio" por dominio

Sin dependencias externas (no requiere inotify ni sudo).

Uso:
  python3 team-bus-watch.py          # modo daemon (bucle infinito)
  python3 team-bus-watch.py --once   # un solo ciclo (para cron/test)
"""
import os, sys, json, time, hashlib
from pathlib import Path
from datetime import datetime

BUS = Path(os.path.expanduser("~/.hermes/team-context"))
STATE = Path(os.path.expanduser("~/.hermes/shared-state.json"))
POLL_SECONDS = 5

_cache = {}  # archivo -> hash


def snapshot():
    """Genera README.md consolidado con todos los dominios."""
    dominios = sorted(BUS.glob("*.md"))
    lineas = ["# Team Context — Snapshot en vivo", "",
              f"*Actualizado: {datetime.now().isoformat(timespec='seconds')}*", ""]
    for f in dominios:
        if f.name == "README.md":
            continue
        lineas.append(f"## {f.stem}")
        lineas.append(f.read_text(encoding="utf-8").strip())
        lineas.append("")
    (BUS / "README.md").write_text("\n".join(lineas), encoding="utf-8")
    return len(dominios)


def actualizar_state(cambios):
    """Anota en shared-state.json los dominios que cambiaron."""
    try:
        if STATE.exists():
            data = json.loads(STATE.read_text())
        else:
            data = {}
        data.setdefault("team_bus", {})
        for dom in cambios:
            data["team_bus"][dom] = {
                "last_change": datetime.now().isoformat(timespec="seconds"),
            }
        STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[watch] error state: {e}", file=sys.stderr)


def ciclo():
    cambios = []
    for f in BUS.glob("*.md"):
        if f.name == "README.md":
            continue
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if _cache.get(f.name) != h:
            _cache[f.name] = h
            cambios.append(f.stem)
    if cambios:
        n = snapshot()
        actualizar_state(cambios)
        print(f"[watch] {datetime.now().strftime('%H:%M:%S')} cambios: {cambios} ({n} dominios)")
    return cambios


def main():
    if "--once" in sys.argv:
        return ciclo()
    print(f"[watch] Daemon activo: {BUS} (polling {POLL_SECONDS}s)")
    # Primer snapshot
    snapshot()
    print(f"[watch] Snapshot inicial generado: {len(list(BUS.glob('*.md'))) - 1} dominios")
    while True:
        try:
            ciclo()
        except Exception as e:
            print(f"[watch] error: {e}", file=sys.stderr)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
