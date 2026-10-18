#!/usr/bin/env python3
"""
verificador_fidelidad.py — Verificador DETERMINISTA de fidelidad de datos (25-ago-2026).

Pieza que falta para que la fusión total (#13) sea fiable en redacción con datos:
todo dato factual (fecha, número, ID) presente en la respuesta DEBE tener respaldo
en la fuente (prompt + contexto que el modelo recibió). Si no, fail-closed: no emitir.

Filosofía tirith del lab: un dato sin respaldo en la fuente es una alucinación
hasta que se demuestre lo contrario.

Uso:
  python3 tools/verificador_fidelidad.py --respuesta "..." --fuente "..." [--json]
  python3 tools/verificador_fidelidad.py --archivo /tmp/fusion_bateria_resultados.json

Salida: veredicto PASA / REVISA (discrepancias menores) / FALLA (dato sin respaldo)
        + lista de discrepancias detectadas.

Validado contra la batería del 25-ago: debe atrapar T2 "OBS-067/24 agosto" y
T3 "51.6%/996" (fuentes reales OBS-049/OBS-048) y NO bloquear T1/T4/T5 correctos.

Diseño: normaliza primero (Unicode NFKC corrige U+202F del 19-ago), extrae
entidades con regex, compara contra la fuente normalizada. Números con unidad
o >= 10 son significativos; números < 10 sin unidad se ignoran (ruido).
"""
import argparse
import json
import re
import sys
import unicodedata

# ── NORMALIZACIÓN ──────────────────────────────────────────────────────

def normalizar(texto: str) -> str:
    """NFKC (corrige espacios finos U+202F, comillas tipográficas), lower, colapsa espacios."""
    t = unicodedata.normalize("NFKC", texto or "")
    t = t.lower()
    t = re.sub(r"\s+", " ", t)
    return t.strip()


# ── EXTRACCIÓN DE ENTIDADES ────────────────────────────────────────────

_ID_RE = re.compile(
    r"\b(?:obs|dec|rule|policy|pred|exp|ko|prd)-\d+[a-z0-9-]*\b"
    r"|\b(?:obs|dec|rule|policy|pred|exp|ko)\s?\d{3}\b",
    re.I)

_FECHA_ISO_RE = re.compile(r"\b(?:19|20)\d{2}-\d{1,2}-\d{1,2}\b")
_FECHA_DMA_RE = re.compile(
    r"\b(\d{1,2})\s+(?:de\s+)?(enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
    r"septiembre|octubre|noviembre|diciembre|sep|oct|nov|dic)\s+(?:de\s+)?((?:19|20)\d{2})\b",
    re.I)
_MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
          "julio": 7, "agosto": 8, "septiembre": 9, "sep": 9, "octubre": 10, "oct": 10,
          "noviembre": 11, "nov": 11, "diciembre": 12, "dic": 12}

_NUMERO_RE = re.compile(
    r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*(?:%|€|eur|gb|gib|mb|mib|cm|km/h|kmh|veces|tok/s|s|min|h)\b"
    r"|\b\d+(?:[.,]\d+)?\b")


def _normaliza_fecha_dma(m: re.Match) -> str:
    dia, mes, anio = m.group(1), m.group(2).lower(), m.group(3)
    return f"{anio}-{_MESES[mes]:02d}-{int(dia):02d}"


def extraer_entidades(texto: str) -> dict:
    """Devuelve {ids: [...], fechas: [...], numeros: [...]} de un texto normalizado."""
    ids = [x.replace(" ", "-").lower() for x in _ID_RE.findall(texto)]
    fechas = list(_FECHA_ISO_RE.findall(texto))
    for m in _FECHA_DMA_RE.finditer(texto):
        fechas.append(_normaliza_fecha_dma(m))
    nums = []
    for tok in _NUMERO_RE.findall(texto):
        tok = tok.strip()
        if not tok:
            continue
        # Limpiar separadores de miles para comparar: "1.234" → "1234", "40,5" → "40.5"
        if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", tok.replace(" ", "")):
            tok = tok.replace(".", "").replace(",", "")
        else:
            tok = tok.replace(" ", "").replace(",", ".")
        nums.append(tok)
    return {"ids": ids, "fechas": fechas, "numeros": nums}


def _filtrar_numeros_significativos(numeros: list) -> list:
    """Solo números >= 10 o con unidad. Los <10 sin unidad son ruido (p.ej. 'max 12' queda,
    pero '3 lineas' se conserva solo si está en la fuente — el filtro es para la respuesta)."""
    out = []
    for n in numeros:
        m = re.match(r"^(\d+(?:\.\d+)?)\s*(.*)$", n)
        if not m:
            continue
        valor = float(m.group(1))
        unidad = m.group(2).strip()
        if valor >= 10 or unidad:
            out.append(n)
    return out


# ── VERIFICACIÓN ───────────────────────────────────────────────────────

def verificar(respuesta: str, fuente: str, umbral_falla: int = 1) -> dict:
    """Compara entidades de la respuesta contra la fuente. Fail-closed.

    - FALLA si hay >= umbral_falla entidades de la respuesta sin respaldo en la fuente.
    - PASA si todas las entidades significativas tienen respaldo.
    - Devuelve detalle de discrepancias para diagnóstico.
    """
    r_norm = normalizar(respuesta)
    f_norm = normalizar(fuente)

    re_ids = extraer_entidades(r_norm)
    rf_ids = extraer_entidades(f_norm)
    # Para IDs/fechas: TODOS los de la respuesta deben estar en la fuente
    ids_sin = sorted(set(re_ids["ids"]) - set(rf_ids["ids"]))
    fechas_sin = sorted(set(re_ids["fechas"]) - set(rf_ids["fechas"]))

    # Números: solo los significativos de la respuesta deben estar en la fuente
    nums_resp = _filtrar_numeros_significativos(re_ids["numeros"])
    nums_fuente = set(rf_ids["numeros"])
    # Comparación relajada: el número de la respuesta debe aparecer como substring
    # de algún número de la fuente (p.ej. "40.5" vs "40.5%" → "40.5" in "40.5%").
    nums_sin = []
    for n in nums_resp:
        base = re.match(r"^(\d+(?:\.\d+)?)", n).group(1)
        if not any(base in f for f in nums_fuente):
            nums_sin.append(n)

    discrepancias = [f"ID sin respaldo: {x}" for x in ids_sin]
    discrepancias += [f"fecha sin respaldo: {x}" for x in fechas_sin]
    discrepancias += [f"número sin respaldo: {x}" for x in nums_sin]

    if len(discrepancias) >= umbral_falla:
        veredicto = "FALLA"
    elif discrepancias:
        veredicto = "REVISA"
    else:
        veredicto = "PASA"

    return {
        "veredicto": veredicto,
        "discrepancias": discrepancias,
        "resumen": {
            "ids_respuesta": sorted(set(re_ids["ids"])),
            "fechas_respuesta": sorted(set(re_ids["fechas"])),
            "numeros_respuesta_significativos": nums_resp,
            "ids_fuente": sorted(set(rf_ids["ids"])),
            "fechas_fuente": sorted(set(rf_ids["fechas"])),
            "numeros_fuente": sorted(nums_fuente)[:60],
        },
    }


# ── CLI ────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Verificador determinista de fidelidad")
    ap.add_argument("--respuesta", default="")
    ap.add_argument("--fuente", default="")
    ap.add_argument("--archivo", default="",
                    help="JSON de batería de fusión (/tmp/fusion_bateria_resultados.json) "
                         "para validar contra los casos reales del 25-ago")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.archivo:
        with open(args.archivo) as f:
            datos = json.load(f)
        for r in datos:
            # La fuente que vio el modelo: prompt + contexto (en la batería el contexto
            # iba dentro del prompt de la tarea). Usamos la respuesta ganadora y su tarea.
            resp = r.get("respuesta_ganadora", "")
            if not resp:
                print(f"{r.get('tarea')}: SIN respuesta ganadora", file=sys.stderr)
                continue
            # Fuente real: leemos la OBS correspondiente cuando existe, si no el prompt.
            fuente = ""
            if r["tarea"] == "T2_resumen":
                fuente = open("/home/jokoalmi/joko-lab/01-knowledge/observations/OBS-049-uso-rag-2026-08-18.md").read()
            elif r["tarea"] == "T3_json":
                fuente = open("/home/jokoalmi/joko-lab/01-knowledge/observations/OBS-048-fallback-rate-2026-08-18.md").read()
            else:
                fuente = "estado real del lab recopilado en batería (contexto T1)"
            v = verificar(resp, fuente)
            print(f"{r['tarea']} [{r.get('mejor', {}).get('escritor', '?')}] → {v['veredicto']}")
            for d in v["discrepancias"]:
                print(f"    ✗ {d}")
        return 0

    if not args.respuesta or not args.fuente:
        print("ERROR: usa --respuesta + --fuente, o --archivo")
        return 1

    v = verificar(args.respuesta, args.fuente)
    if args.json:
        print(json.dumps(v, ensure_ascii=False, indent=2))
    else:
        print(f"VEREDICTO: {v['veredicto']}")
        for d in v["discrepancias"]:
            print(f"  ✗ {d}")
        if not v["discrepancias"]:
            print("  ✓ todas las entidades significativas tienen respaldo en la fuente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
