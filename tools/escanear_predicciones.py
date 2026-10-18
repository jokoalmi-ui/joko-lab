#!/usr/bin/env python3
"""
Escanea los PRED-*.yaml del lab. v2 — incorpora la revisión de Hermes
del 2026-08-04:

  - fecha_revision se parsea con manejo de error (no crashea con
    fechas mal formadas ni con datetime en vez de date).
  - status del YAML se valida contra el estado derivado de
    resultado+fecha_revision; discrepancia = aviso, no fuente de verdad.
    El script NUNCA reescribe los YAML: solo avisa por stderr.
  - resuelto_por es obligatorio si resultado != 'pendiente', y DEBE
    ser distinto de quien_predice — si coinciden, se rechaza el
    fichero entero (nadie se autoevalúa, sin excepción).
  - tasa_acierto documentada: acierto / total: 'parcial' y 'fallo'
    cuentan igual en el denominador, ninguno se pondera aparte.
  - resultado='sin_veredicto' (anadido 2026-10-13): cierra una
    prediccion que NO se pudo evaluar (criterio no medible o
    experimento nunca ejecutado). Cuenta como resuelta para el
    escaner pero queda FUERA del denominador de la tasa de acierto:
    declarar el fallo de instrumentacion es dato, no se maquilla.

Uso:
    python3 escanear_predicciones.py --dir 01-knowledge/objects
"""
import argparse
import datetime
import sys
from pathlib import Path

import yaml

RESULTADOS_VALIDOS = {"pendiente", "acierto", "fallo", "parcial", "sin_veredicto"}
AUTORES_VALIDOS = {"joseba", "hermes", "conjunta"}


def parsear_fecha(valor, contexto: str):
    """Acepta date o datetime en el YAML; devuelve date o None si es inválida."""
    if isinstance(valor, datetime.datetime):
        return valor.date()
    if isinstance(valor, datetime.date):
        return valor
    if isinstance(valor, str):
        try:
            return datetime.date.fromisoformat(valor[:10])
        except ValueError:
            print(f"  [AVISO] {contexto}: fecha_revision mal formada ('{valor}'), se omite", file=sys.stderr)
            return None
    print(f"  [AVISO] {contexto}: fecha_revision de tipo inesperado ({type(valor)}), se omite", file=sys.stderr)
    return None


def _validar_campos(data: dict, f) -> bool:
    """Valida campos obligatorios y valores. Devuelve True si es válida."""
    campos_obligatorios = ("id", "quien_predice", "prediccion", "criterio_exito",
                            "fecha_revision", "resultado")
    faltante = next((c for c in campos_obligatorios if c not in data), None)
    if faltante:
        print(f"  [AVISO] {f}: falta campo obligatorio '{faltante}', se omite", file=sys.stderr)
        return False

    if data["resultado"] not in RESULTADOS_VALIDOS:
        print(f"  [AVISO] {f}: resultado inválido '{data['resultado']}', se omite", file=sys.stderr)
        return False

    if data["quien_predice"] not in AUTORES_VALIDOS:
        print(f"  [AVISO] {f}: quien_predice inválido '{data['quien_predice']}', se omite", file=sys.stderr)
        return False
    return True


def _validar_no_autoeval(data: dict, f) -> bool:
    """Regla dura: nadie se autoevalúa. Devuelve True si pasa."""
    if data["resultado"] == "pendiente":
        return True
    resuelto_por = data.get("resuelto_por")
    if not resuelto_por:
        print(f"  [ERROR] {f}: resultado='{data['resultado']}' pero falta 'resuelto_por' — SE OMITE", file=sys.stderr)
        return False
    if resuelto_por == data["quien_predice"]:
        print(f"  [ERROR] {f}: resuelto_por == quien_predice ('{resuelto_por}') — "
              f"AUTOEVALUACIÓN NO PERMITIDA, SE OMITE", file=sys.stderr)
        return False
    return True


def cargar_predicciones(directorio: Path) -> list:
    preds = []
    for f in sorted(directorio.glob("PRED-*.yaml")):
        if f.name == "PRED-template.yaml":
            continue
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [AVISO] no se pudo leer {f}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict) or data.get("type") != "PRED":
            continue

        if not _validar_campos(data, f):
            continue

        fecha_rev = parsear_fecha(data["fecha_revision"], str(f))
        if fecha_rev is None:
            continue
        data["_fecha_revision_parseada"] = fecha_rev

        if not _validar_no_autoeval(data, f):
            continue

        data["_ruta"] = str(f)
        preds.append(data)
    return preds


def estado_derivado(p: dict, hoy: datetime.date) -> str:
    if p["resultado"] != "pendiente":
        return "resuelta"
    if p["_fecha_revision_parseada"] < hoy:
        return "vencida_sin_revisar"
    return "pendiente"


def validar_consistencia_status(preds: list, hoy: datetime.date):
    for p in preds:
        declarado = p.get("status")
        derivado = estado_derivado(p, hoy)
        if declarado != derivado:
            print(f"  [AVISO] {p['id']}: status declarado ('{declarado}') no coincide "
                  f"con el estado derivado ('{derivado}'). El script usa el derivado y "
                  f"NO reescribe el YAML: corrige el 'status' a mano.", file=sys.stderr)


def separar(preds: list, hoy: datetime.date):
    vencidas, resueltas, futuras = [], [], []
    for p in preds:
        estado = estado_derivado(p, hoy)
        if estado == "vencida_sin_revisar":
            vencidas.append(p)
        elif estado == "resuelta":
            resueltas.append(p)
        else:
            futuras.append(p)
    return vencidas, resueltas, futuras


def calibracion_por_autor(resueltas: list) -> dict:
    stats = {}
    for p in resueltas:
        autor = p["quien_predice"]
        stats.setdefault(autor, {"acierto": 0, "fallo": 0, "parcial": 0,
                                 "sin_veredicto": 0})
        stats[autor][p["resultado"]] += 1
    resumen = {}
    for autor, c in stats.items():
        total = sum(c.values())
        # Convención (documentada, no ambigua): tasa_acierto = acierto / total.
        # 'parcial' cuenta en el denominador pero no en el numerador — un
        # acierto parcial NO suma como acierto. Si preferís ponderar parcial
        # como 0.5, hacedlo explícito aquí, no lo asumáis del número solo.
        evaluables = c["acierto"] + c["fallo"] + c["parcial"]
        resumen[autor] = {
            **c, "total": total, "evaluables": evaluables,
            "tasa_acierto": round(c["acierto"] / evaluables, 2) if evaluables else None,
        }
    return resumen


def imprimir_reporte(vencidas, resueltas, futuras, hoy):
    print(f"\n=== Prediction Log — {hoy.isoformat()} ===\n")

    if vencidas:
        print(f"⚠️  {len(vencidas)} predicción(es) VENCIDA(S) SIN REVISAR:")
        for p in vencidas:
            print(f"   {p['id']} ({p['quien_predice']}) — vencía {p['_fecha_revision_parseada']}")
            print(f"      \"{p['prediccion'].strip()[:100]}...\"")
        print()
    else:
        print("✓ No hay predicciones vencidas sin revisar.\n")

    if resueltas:
        print(f"Calibración ({len(resueltas)} predicciones resueltas):")
        print("  [convención: tasa_acierto = acierto / evaluables; 'parcial' no puntúa")
        print("   como acierto y 'sin_veredicto' queda fuera del denominador]")
        for autor, s in calibracion_por_autor(resueltas).items():
            tasa = f"{s['tasa_acierto']*100:.0f}%" if s["tasa_acierto"] is not None else "n/a"
            print(f"   {autor}: {s['acierto']} acierto / {s['fallo']} fallo / "
                  f"{s['parcial']} parcial / {s['sin_veredicto']} sin veredicto — "
                  f"tasa de acierto (sin veredicto excluidos): {tasa}")
        print()
    else:
        print("Todavía no hay predicciones resueltas para calcular calibración.\n")

    if futuras:
        print(f"{len(futuras)} predicción(es) pendiente(s), aún dentro de plazo:")
        for p in sorted(futuras, key=lambda x: x["_fecha_revision_parseada"]):
            print(f"   {p['id']} — revisar el {p['_fecha_revision_parseada']}")
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directorio con los PRED-*.yaml")
    args = parser.parse_args()

    directorio = Path(args.dir)
    if not directorio.is_dir():
        print(f"Directorio no encontrado: {directorio}", file=sys.stderr)
        sys.exit(1)

    preds = cargar_predicciones(directorio)
    hoy = datetime.date.today()
    validar_consistencia_status(preds, hoy)
    vencidas, resueltas, futuras = separar(preds, hoy)
    imprimir_reporte(vencidas, resueltas, futuras, hoy)

    if vencidas:
        sys.exit(1)


if __name__ == "__main__":
    main()
