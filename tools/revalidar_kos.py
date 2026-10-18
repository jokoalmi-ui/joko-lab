#!/usr/bin/env python3
"""
revalidar_kos.py — Watchdog de revalidacion KEL (solo lectura).

Escanea los Knowledge Objects de 01-knowledge/objects/ y avisa cuando un KO
activo (no superseded) se acerca a su next_review o expires. Es el disparador
temporal de la fase REVALIDACION de la maquina de estados KEL:
  REVALIDACION periodica -> ¿sigue siendo valida? -> Si: mantener / No: retirar.

NO modifica ningun KO. La revalidacion en si (releer el KO, decidir mantener,
reabrir, degradar o retirar) la hace el agente/humano con KVC en sesion,
cuando el aviso llega. Mismo patron que tools/escanear_predicciones.py.

Salida (patron watchdog):
  - Sin argumentos: imprime SOLO si hay algo que avisar (vencidos, proximos a
    next_review, o KOs sin fechas). Si todo esta en orden, stdout vacio
    (silencio total para el cron no_agent).
  - --all: imprime el estado completo de todos los KOs (uso manual).
  - --json: salida JSON (para consumo por scripts).

Uso:
  python3 tools/revalidar_kos.py [--all|--json]

HORIZONTE_AVISO dias: cuantos dias antes de next_review se avisa. Es un
horizonte de aviso de producto (configurable), no un umbral de calibracion:
no fija calidad, solo decide con que antelacion recordar.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

import yaml

OBJECTS_DIR = Path.home() / "joko-lab" / "01-knowledge" / "objects"
HORIZONTE_AVISO_DIAS = 7  # avisar N dias antes de next_review


def cargar_kos(directorio: Path) -> list:
    kos = []
    for f in sorted(directorio.glob("*.yaml")):
        if f.name == "PRED-template.yaml":
            continue
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [AVISO] no se pudo leer {f}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        data["_ruta"] = str(f)
        kos.append(data)
    return kos


def parse_fecha(valor):
    if not valor:
        return None
    try:
        return datetime.date.fromisoformat(str(valor))
    except Exception:
        return None


def _clase_por_dias(dias_rev, dias_exp, horizonte) -> str:
    """Clase según días: vencido si alguna fecha pasó, próximo si next_review
    cae en el horizonte, en_orden en el resto."""
    if (dias_rev is not None and dias_rev < 0) or (dias_exp is not None and dias_exp < 0):
        return "vencido"
    if dias_rev is not None and dias_rev <= horizonte:
        return "proximo"
    return "en_orden"


def _clasificar_ko(ko: dict, hoy: datetime.date, horizonte: int) -> tuple:
    """Clasifica un KO individual. Devuelve (item, clase).
    La clase puede ser: superseded, no_revalidable, sin_fechas, vencido,
    proximo, en_orden."""
    ko_id = ko.get("id", "?")
    tipo = ko.get("type", "?")
    status = ko.get("status", "?")
    superseded = ko.get("superseded_by")
    next_rev = parse_fecha(ko.get("next_review"))
    expires = parse_fecha(ko.get("expires"))

    item = {
        "id": ko_id,
        "type": tipo,
        "status": status,
        "next_review": ko.get("next_review"),
        "expires": ko.get("expires"),
        "last_validated": ko.get("last_validated"),
        "superseded_by": superseded,
        "ruta": ko["_ruta"],
    }

    # Solo se revalidan los activos; los superseded ya tienen sustitucion
    if superseded:
        item["clase"] = "superseded"
        return item, "superseded"

    if status not in ("activo", "active", "draft"):
        item["clase"] = "no_revalidable"
        return item, "no_revalidable"

    if next_rev is None and expires is None:
        item["clase"] = "sin_fechas"
        return item, "sin_fechas"

    # Dias hasta la revision mas cercana (next_review o expires)
    dias_rev = (next_rev - hoy).days if next_rev else None
    dias_exp = (expires - hoy).days if expires else None
    item["dias_next_review"] = dias_rev
    item["dias_expires"] = dias_exp

    clase = _clase_por_dias(dias_rev, dias_exp, horizonte)
    item["clase"] = clase
    return item, clase


def clasificar(kos: list, hoy: datetime.date, horizonte: int):
    vencidos = []      # next_review o expires ya pasados (y aun activos)
    proximos = []      # next_review dentro del horizonte
    sin_fechas = []    # KO activo sin next_review/expires (deuda)
    en_orden = []

    destino = {
        "vencido": vencidos, "proximo": proximos,
        "sin_fechas": sin_fechas, "en_orden": en_orden,
    }
    for ko in kos:
        item, clase = _clasificar_ko(ko, hoy, horizonte)
        if clase in ("superseded", "no_revalidable"):
            en_orden.append(item)
        else:
            destino[clase].append(item)

    return {"vencidos": vencidos, "proximos": proximos,
            "sin_fechas": sin_fechas, "en_orden": en_orden}


def formato_linea(item) -> str:
    partes = [f"{item['id']} [{item['type']}]"]
    if item.get("next_review"):
        partes.append(f"next_review={item['next_review']}")
        if item.get("dias_next_review") is not None:
            partes.append(f"({item['dias_next_review']}d)")
    if item.get("expires"):
        partes.append(f"expires={item['expires']}")
        if item.get("dias_expires") is not None:
            partes.append(f"({item['dias_expires']}d)")
    return " ".join(partes)


def _imprimir_grupo(titulo: str, items: list, etiqueta: str):
    """Imprime un grupo de KOs con su título y etiqueta (si no está vacío)."""
    if not items:
        return
    print(titulo.format(n=len(items)))
    for it in items:
        print(f"  - {formato_linea(it)}  [{etiqueta}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="Mostrar estado completo")
    ap.add_argument("--json", action="store_true", help="Salida JSON")
    args = ap.parse_args()

    hoy = datetime.date.today()
    kos = cargar_kos(OBJECTS_DIR)
    res = clasificar(kos, hoy, HORIZONTE_AVISO_DIAS)

    if args.json:
        print(json.dumps({"fecha": hoy.isoformat(), **res}, ensure_ascii=False,
                         indent=2, default=str))
        return

    hay_aviso = res["vencidos"] or res["proximos"] or res["sin_fechas"]
    if not args.all and not hay_aviso:
        return  # silencio (watchdog): todo en orden

    _imprimir_grupo(f"KOs VENCIDOS (revisar ya): {{n}}", res["vencidos"], "VENCIDO")
    _imprimir_grupo(f"KOs PROXIMOS a next_review (<= {HORIZONTE_AVISO_DIAS}d): {{n}}",
                    res["proximos"], "PROXIMO")
    _imprimir_grupo("KOs ACTIVOS SIN FECHAS (deuda, fijar next_review/expires): {n}",
                    res["sin_fechas"], "SIN FECHAS")

    if args.all:
        print(f"\nEn orden: {len(res['en_orden'])} | Total: {len(kos)} | "
              f"Fecha: {hoy.isoformat()}")
        for it in res["en_orden"]:
            print(f"  - {formato_linea(it)}")


if __name__ == "__main__":
    main()
