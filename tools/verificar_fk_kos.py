#!/usr/bin/env python3
"""
verificar_fk_kos.py — Detector de integridad referencial (solo lectura).

Clase de defecto: referencia_ko_no_verificada (MEL-...004, 06-ago). Un ID de
KO citado (en campos estructurados o en prosa) que no resuelve a un fichero
real en 01-knowledge/objects/. El caso real: DEC-004 citaba "RULE-CONF-001"
que no existe; lo detecto el revisor manual, no el gate.

Este script NO es un gate: es el INSTRUMENTO que permite medir la clase de
defecto (paso previo a la ficha EVF de extender SVP/KVC). Solo lectura, nunca
modifica nada.

Regla FK (solo IDs de KO): un ID se considera referencia a KO si su prefijo
esta en PREFIJOS_KO (DEC, RULE, POLICY, PRED, PATTERN, OBS, HYP). Otros
prefijos (EXP-, JL-, CP-, M-, V00x...) son referencias externas y se ignoran:
no son foreign keys de Knowledge Objects.

Alcance:
  - Sin argumentos: solo los KOs (01-knowledge/objects/*.yaml), campos
    estructurados (dependencies, superseded_by, contradicts) y prosa
    (body/nota/canal_nota y cualquier campo string con menciones tipo ID).
  - --docs: ademas escanea documentos markdown de joko-lab (01-knowledge/,
    lpa/, research/, GUIA*.md) buscando menciones [[ID]] o ID sueltos con
    prefijo KO.

Uso:
  python3 tools/verificar_fk_kos.py [--docs] [--json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path.home() / "joko-lab"
OBJECTS_DIR = ROOT / "01-knowledge" / "objects"
PREFIJOS_KO = ("DEC", "RULE", "POLICY", "PRED", "PATTERN", "OBS", "HYP")

# ID tipo KO: prefijo + guiones/digitos opcionales + digitos (ej: RULE-CONF-001,
# DEC-001, PRED-002). El prefijo debe estar en PREFIJOS_KO.
RE_ID_KO = re.compile(r"\b((?:%s)-[A-Z0-9]*-?\d{1,4})\b" % "|".join(PREFIJOS_KO))


def ids_ko_reales(directorio: Path) -> set:
    ids = set()
    for f in directorio.glob("*.yaml"):
        if f.name == "PRED-template.yaml" or ".bak" in f.name:
            continue
        ids.add(f.name.replace(".yaml", ""))
    # Los OBS y HYP viven como markdown (01-knowledge/observations/,
    # 01-knowledge/hypotheses/), no como objetos YAML: tambien son IDs validos.
    for sub in ("observations", "hypotheses"):
        d = directorio.parent / sub
        if d.is_dir():
            for f in d.glob("*.md"):
                if ".bak" in f.name:
                    continue
                # OBS-005-decisiones-por-politica-(2026-08-04).md -> OBS-005
                id_cand = re.match(r"((?:%s)-\d+)" % "|".join(PREFIJOS_KO), f.name)
                if id_cand:
                    ids.add(id_cand.group(1))
    return ids


def id_es_ko(id_candidato: str) -> bool:
    return id_candidato.split("-")[0] in PREFIJOS_KO


def _chequear_ref(valor, campo, path, ko_id, ids_validos, rotas, tipo="structured"):
    """Registra una referencia rota si el valor es KO y no es válido."""
    v = str(valor).strip()
    if v and id_es_ko(v) and v not in ids_validos:
        rotas.append((str(path), ko_id, campo, v, tipo))


def _escanear_estructurados(data, path, ko_id, ids_validos, rotas):
    for campo in ("dependencies", "contradicts"):
        valores = data.get(campo) or []
        if isinstance(valores, str):
            valores = [valores]
        for v in valores:
            _chequear_ref(v, campo, path, ko_id, ids_validos, rotas)

    sup = data.get("superseded_by")
    if sup:
        _chequear_ref(str(sup), "superseded_by", path, ko_id, ids_validos, rotas)


def _revisar_texto(texto, campo, path, ko_id, ids_validos, rotas):
    if not isinstance(texto, str):
        return
    for m in RE_ID_KO.findall(texto):
        if m not in ids_validos:
            rotas.append((str(path), ko_id, campo, m, "prosa"))


def _revisar_valor_prosa(valor, campo, path, ko_id, ids_validos, rotas):
    """Revisa un valor en prosa: str directo, lista de str o dict de str."""
    if isinstance(valor, str):
        _revisar_texto(valor, campo, path, ko_id, ids_validos, rotas)
    elif isinstance(valor, list):
        for item in valor:
            if isinstance(item, str):
                _revisar_texto(item, campo, path, ko_id, ids_validos, rotas)
    elif isinstance(valor, dict):
        for sub in valor.values():
            if isinstance(sub, str):
                _revisar_texto(sub, campo, path, ko_id, ids_validos, rotas)


def _revisar_prosa(data: dict, path: Path, ko_id: str, ids_validos: set, rotas: list):
    """Revisa campos en prosa: strings directos, listas y dicts anidados."""
    for campo, valor in data.items():
        if campo.startswith("_") or campo in ("id", "type", "status"):
            continue
        _revisar_valor_prosa(valor, campo, path, ko_id, ids_validos, rotas)


def escanear_ko(path: Path, ids_validos: set, rotas: list):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [AVISO] no se pudo leer {path.name}: {e}", file=sys.stderr)
        return
    if not isinstance(data, dict):
        return
    ko_id = data.get("id", path.stem)

    _escanear_estructurados(data, path, ko_id, ids_validos, rotas)

    # 2) Prosa: body, nota, canal_nota y cualquier campo string
    _revisar_prosa(data, path, ko_id, ids_validos, rotas)


def _escanear_archivo_doc(f: Path, ids_validos: set, rotas: list):
    """Escanea un archivo .md: wikilinks explícitos + menciones sueltas."""
    try:
        texto = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return
    # 1) Wikilinks explicitos [[ID]]: BLOQUEANTES en modo gate
    for m in re.findall(r"\[\[([A-Z]+-[A-Z0-9]*-?\d+)\]\]", texto):
        if m not in ids_validos:
            rotas.append((str(f), "-", "wikilink", m, "wikilink"))
    # 2) Menciones sueltas: AVISO (no bloqueo). Se quitan los wikilinks
    #    ya capturados para no duplicar.
    texto_sin_wl = re.sub(r"\[\[[A-Z]+-[A-Z0-9]*-?\d+\]\]", "", texto)
    for m in RE_ID_KO.findall(texto_sin_wl):
        if m not in ids_validos:
            rotas.append((str(f), "-", "prosa-doc", m, "doc"))


def escanear_docs(ids_validos: set, rotas: list):
    rutas = [ROOT / "01-knowledge", ROOT / "lpa", ROOT / "research"]
    rutas += [ROOT / "GUIA-JOKO-LAB.md", ROOT / "GUIA-APRENDIZAJE-JOKO-LAB.md"]
    for base in rutas:
        if base.is_dir():
            archivos = base.rglob("*.md")
        else:
            archivos = [base] if base.exists() else []
        for f in archivos:
            if ".bak" in str(f):
                continue  # backups fuera del escaneo (ruido)
            _escanear_archivo_doc(f, ids_validos, rotas)


def _dedupe_mantener_orden(rotas: list) -> list:
    # Dedupe manteniendo orden
    vistos = set()
    rotas_unicas = []
    for r in rotas:
        if r not in vistos:
            vistos.add(r)
            rotas_unicas.append(r)
    return rotas_unicas


def _salida_json(ids_validos, rotas_unicas) -> None:
    print(json.dumps({
        "ids_ko_validos": len(ids_validos),
        "referencias_rotas": len(rotas_unicas),
        "detalle": [{"archivo": a, "ko": k, "campo": c, "id_roto": i, "tipo": t}
                    for a, k, c, i, t in rotas_unicas],
    }, ensure_ascii=False, indent=2))


def _salida_texto(ids_validos, rotas_unicas, docs: bool) -> bool:
    if not rotas_unicas:
        print(f"OK: integridad referencial correcta en {len(ids_validos)} KOs"
              + (" (+ docs)" if docs else ""))
        return True

    print(f"Referencias a revisar: {len(rotas_unicas)}")
    print("Nota: las menciones en prosa pueden ser historicas (caso DEC-004/"
          "RULE-CONF-001: nota de correccion, no defecto activo) o ejemplos de "
          "diseno (DEC-005/007 en contracts). Revisar antes de tratar como rota.")
    for archivo, ko, campo, id_roto, tipo in rotas_unicas:
        print(f"  - {archivo} | KO {ko} | campo {campo} | {id_roto} [{tipo}]")
    return False


def _salida_gate(rotas_unicas) -> None:
    # Gate SVP/FK (adoptado 07-ago): structured y wikilink BLOQUEAN; prosa avisa.
    bloqueantes = [r for r in rotas_unicas if r[4] in ("structured", "wikilink")]
    if bloqueantes:
        print(f"\nGATE FK: BLOQUEADO — {len(bloqueantes)} rotas bloqueantes")
        for archivo, ko, campo, id_roto, tipo in bloqueantes:
            print(f"  - {archivo} | {id_roto} [{tipo}]")
        sys.exit(1)
    print("\nGATE FK: OK (sin rotas bloqueantes; avisos de prosa no bloquean)")
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", action="store_true",
                    help="Escanea tambien documentos (01-knowledge, lpa, research, GUIA)")
    ap.add_argument("--gate", action="store_true",
                    help="Modo gate SVP: exit 1 si hay rotas BLOQUEANTES "
                         "(structured en KOs o wikilink en docs); los avisos "
                         "(prosa) no bloquean. Implica --docs.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.gate:
        args.docs = True

    ids_validos = ids_ko_reales(OBJECTS_DIR)
    rotas = []
    for f in sorted(OBJECTS_DIR.glob("*.yaml")):
        if f.name == "PRED-template.yaml":
            continue
        escanear_ko(f, ids_validos, rotas)
    if args.docs:
        escanear_docs(ids_validos, rotas)

    rotas_unicas = _dedupe_mantener_orden(rotas)

    if args.json:
        _salida_json(ids_validos, rotas_unicas)
        return

    if _salida_texto(ids_validos, rotas_unicas, args.docs):
        return

    if args.gate:
        _salida_gate(rotas_unicas)


if __name__ == "__main__":
    main()
