#!/usr/bin/env python3
"""
vigia_complejidad.py — "¿la complejidad del lab EMPEORA?"

`complejidad_crap.py` mide el ESTADO (cuántas funciones complejas hay hoy).
Este vigía mide el CAMBIO: guarda un snapshot por ejecución en
`04-operations/metrics/complejidad_historial.jsonl` y compara con el último,
de modo que el drift de complejidad (pitfall 24 del skill refactor-seguro)
deja de pasar inadvertido: sin histórico, la cifra se lee y se olvida.

Qué reporta (contra el snapshot anterior):
  🔴 deuda DURA nueva o agravada  -> función nueva >20, o existente que cruza a >20
  🟠 nuevas complejas (11-20)     -> deuda blanda: se reporta, no rompe el exit
  ⬇️  mejoradas / fuera del radar  -> funciones que bajan de umbral
  ✅ sin cambios

Solo se guardan en el snapshot las funciones con complejidad > 10 (las que
están en el radar). Entrada que cruza de 10 a 12 aparece como "nueva": es
correcto — ha entrado en el radar. Los umbrales NO son nuevos: se heredan de
`complejidad_crap` (UMBRAL_COMPLEJO=10, UMBRAL_MUY_COMPLEJO=20), los mismos
que usa el resto del lab.

Uso:
  python3 tools/vigia_complejidad.py                  # mide, compara y guarda
  python3 tools/vigia_complejidad.py --sin-guardar     # solo compara
  python3 tools/vigia_complejidad.py --json            # salida para cron/L2
  python3 tools/vigia_complejidad.py --historial /tmp/x.jsonl --directorio /tmp/tools

Exit: 0 = sin deuda dura nueva · 1 = deuda dura nueva o agravada.
Solo lectura sobre el código; escribe únicamente su propio histórico.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
TOOLS = LAB / "tools"
HISTORIAL = LAB / "04-operations" / "metrics" / "complejidad_historial.jsonl"

# El motor McCabe del lab: se importa para NO duplicar el criterio de cálculo.
sys.path.insert(0, str(TOOLS))
import complejidad_crap as cc  # noqa: E402  (requiere TOOLS en sys.path)

UMBRAL = cc.UMBRAL_COMPLEJO       # > 10  → función en el radar (compleja)
DURA = cc.UMBRAL_MUY_COMPLEJO     # > 20  → muy compleja (prioridad de refactor)


def _clave(registro: dict) -> str:
    """Identidad estable de una función: 'archivo.py::funcion'."""
    return f"{Path(registro['archivo']).name}::{registro['funcion']}"


def _indexar(registros: list) -> dict:
    """Convierte la salida de complejidad_crap en {clave: complejidad} (solo radar)."""
    return {
        _clave(r): r["complejidad"]
        for r in registros
        if r.get("complejidad", 0) > UMBRAL
    }


def _resumen(radar: dict) -> dict:
    """Totales del snapshot: funciones en radar, complejas y muy complejas."""
    muy = sum(1 for v in radar.values() if v > DURA)
    comp = sum(1 for v in radar.values() if UMBRAL < v <= DURA)
    return {"en_radar": len(radar), "complejas": comp, "muy_complejas": muy}


def _comparar(previo, actual: dict) -> dict:
    """Delta entre dos radares. Devuelve listas [(clave, antes, ahora)]."""
    previo = previo or {}
    nuevas = [(k, 0, v) for k, v in actual.items() if k not in previo]
    empeoradas = [
        (k, previo[k], v) for k, v in actual.items() if k in previo and v > previo[k]
    ]
    mejoradas = [
        (k, previo[k], v) for k, v in actual.items() if k in previo and v < previo[k]
    ]
    salidas = [(k, v, 0) for k, v in previo.items() if k not in actual]
    return {
        "nuevas": sorted(nuevas, key=lambda x: -x[2]),
        "empeoradas": sorted(empeoradas, key=lambda x: -(x[2] - x[1])),
        "mejoradas": sorted(mejoradas, key=lambda x: x[2] - x[1]),
        "salidas": sorted(salidas, key=lambda x: -x[1]),
    }


def _deuda_dura(delta: dict) -> list:
    """Funciones que son deuda dura NUEVA (>20) o que CRUZAN el umbral 20."""
    duras = [x for x in delta["nuevas"] if x[2] > DURA]
    duras += [x for x in delta["empeoradas"] if x[1] <= DURA < x[2]]
    return sorted(duras, key=lambda x: -x[2])


def _delta_y_duras(previo, radar: dict) -> tuple:
    """Delta y deuda dura. SIN snapshot previo no hay delta: solo línea base."""
    if not previo:
        return _comparar(None, {}), []
    delta = _comparar(previo.get("funciones") or {}, radar)
    return delta, _deuda_dura(delta)


def _leer_ultimo(ruta: Path):
    """Último snapshot válido del histórico, o None si no hay/no se puede leer."""
    if not ruta.exists():
        return None
    ultimo = None
    try:
        for linea in ruta.read_text(encoding="utf-8", errors="replace").splitlines():
            linea = linea.strip()
            if not linea:
                continue
            try:
                ultimo = json.loads(linea)
            except json.JSONDecodeError:
                continue
    except OSError:
        return None
    return ultimo


def _guardar(ruta: Path, radar: dict, ahora=None) -> dict:
    """Anexa un snapshot al histórico. Devuelve el snapshot escrito."""
    ahora = ahora or datetime.now()
    snapshot = {"ts": ahora.isoformat(timespec="seconds")}
    snapshot.update(_resumen(radar))
    snapshot["funciones"] = dict(sorted(radar.items(), key=lambda x: -x[1]))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
    return snapshot


def _cabecera(radar: dict, previo) -> str:
    """Encabezado con el estado actual y el del snapshot previo."""
    hoy = _resumen(radar)
    lines = [
        "# 🔭 VIGÍA DE COMPLEJIDAD — ¿empeora el lab?",
        "",
        f"Actual: {hoy['en_radar']} funciones en radar (> {UMBRAL}) · "
        f"{hoy['complejas']} complejas (11-20) · {hoy['muy_complejas']} muy complejas (>20)",
    ]
    if previo:
        lines.append(
            f"Previo ({previo.get('ts', 'sin fecha')}): {previo.get('en_radar', '?')} en radar · "
            f"{previo.get('complejas', '?')} complejas · {previo.get('muy_complejas', '?')} muy complejas"
        )
    else:
        lines.append("Previo: SIN HISTÓRICO — esta ejecución fija la línea base.")
    return "\n".join(lines)


def _bullets(titulo: str, filas: list, marca: str, limite: int) -> list:
    """Sección de bullets con tope (y aviso de los que quedan fuera)."""
    if not filas:
        return []
    lines = ["", f"## {titulo} ({len(filas)})"]
    for clave, antes, ahora in filas[:limite]:
        lines.append(f"- {marca} `{clave}` {antes} → {ahora}")
    if len(filas) > limite:
        lines.append(f"- … y {len(filas) - limite} más (sube --top)")
    return lines


def _informe_delta(radar: dict, previo, delta: dict, duras: list, limite: int) -> str:
    """Cuerpo del informe: deuda dura, nuevas blandas, mejoras y salidas."""
    if previo is None:
        return "\n".join([
            "",
            "## 🆕 Línea base creada",
            f"- Se han registrado {_resumen(radar)['en_radar']} funciones en radar.",
            "- La próxima ejecución ya dará el delta (nuevas / empeoradas / mejoradas).",
        ])
    lines = _bullets("🔴 Deuda DURA nueva o agravada (>20)", duras, "🔴", limite)
    blandas = [x for x in delta["nuevas"] if x[2] <= DURA]
    lines += _bullets("🟠 Nuevas en el radar (11-20)", blandas, "🟠", limite)
    lines += _bullets("📈 Empeoradas sin cruzar umbral", delta["empeoradas"], "📈", limite)
    lines += _bullets("⬇️ Mejoradas en el radar", delta["mejoradas"], "⬇️", limite)
    lines += _bullets("✅ Fuera del radar (bajaron a ≤10 o desaparecieron)", delta["salidas"], "✅", limite)
    if not any(delta.values()):
        lines += ["", "## ✅ Sin cambios respecto al snapshot anterior"]
    return "\n".join(lines)


def _salida_json(radar: dict, previo, delta: dict, duras: list) -> str:
    """Salida JSON (serializable: tuplas → listas)."""
    datos = {
        "actual": _resumen(radar),
        "previo": {"ts": previo.get("ts"), **_resumen(previo.get("funciones") or {})} if previo else None,
        "delta": delta,
        "deuda_dura": duras,
    }
    return json.dumps(datos, ensure_ascii=False, indent=2, default=str)


def _parsear(argv=None):
    """Argumentos de la CLI."""
    p = argparse.ArgumentParser(description="¿La complejidad del lab empeora? (delta entre snapshots)")
    p.add_argument("--directorio", default=str(TOOLS), help="Directorio a medir (por defecto tools/)")
    p.add_argument("--historial", default=str(HISTORIAL), help="JSONL de snapshots")
    p.add_argument("--sin-guardar", action="store_true", help="No anexar snapshot (solo comparar)")
    p.add_argument("--json", action="store_true", help="Salida JSON")
    p.add_argument("--top", type=int, default=10, help="Máximo de filas por sección (defecto 10)")
    return p.parse_args(argv)


def main(argv=None) -> int:
    """Mide, compara con el último snapshot, informa y guarda."""
    args = _parsear(argv)
    ruta = Path(args.historial)
    radar = _indexar(cc.analizar_dir(Path(args.directorio)))
    previo = _leer_ultimo(ruta)
    delta, duras = _delta_y_duras(previo, radar)

    if args.json:
        print(_salida_json(radar, previo, delta, duras))
    else:
        print(_cabecera(radar, previo))
        print(_informe_delta(radar, previo, delta, duras, args.top))
        if duras:
            print("\n## 🎯 Siguiente paso\n- Refactorizar la deuda dura (skill refactor-seguro, "
                  "backup RULE-008 + suite verde antes de registrar).")

    if not args.sin_guardar:
        _guardar(ruta, radar)
    return 1 if duras else 0


if __name__ == "__main__":
    sys.exit(main())
