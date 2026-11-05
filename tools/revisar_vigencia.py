#!/usr/bin/env python3
"""Vigencia de los analisis de research/ — lee el frontmatter, no el cuerpo.

Campos que mira (todos opcionales; se alinean con el esquema de RULE-*.yaml):

  data_as_of:      fecha en que se midio el dato
  last_validated:  ultima vez que alguien lo comprobo contra el mundo
  next_review:     fecha en que el dato caduca y hay que re-medirlo
  superseded_by:   lista de rutas que reemplazan a este fichero
  invalidated:     lista de {claim, since, evidence} — afirmaciones que ya no son ciertas
                   dentro de un fichero que sigue vivo

Salida: CADUCADOS, INVALIDADOS, SIN FECHAR. Solo lectura (no escribe nada).
Exit 0 siempre: es un informe, no un gate. Un fichero sin campos no es un error,
es deuda tecnica contable.

Uso:
  python3 tools/revisar_vigencia.py                 # todo research/
  python3 tools/revisar_vigencia.py --dias 30       # avisa de lo que caduca en 30 dias
  python3 tools/revisar_vigencia.py --solo-caducados
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("falta pyyaml: /usr/bin/python3 -m pip install --user pyyaml")

CAMPOS = ("data_as_of", "last_validated", "next_review", "superseded_by", "invalidated")


def frontmatter(path):
    """Devuelve el dict del frontmatter YAML, o None si no hay o no parsea."""
    try:
        texto = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not texto.startswith("---"):
        return None
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if not m:
        return None
    try:
        d = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return d if isinstance(d, dict) else None


def como_fecha(valor):
    if isinstance(valor, (dt.date, dt.datetime)):
        return valor if isinstance(valor, dt.date) else valor.date()
    if isinstance(valor, str):
        try:
            return dt.date.fromisoformat(valor.strip()[:10])
        except ValueError:
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="research", help="carpeta a revisar (def. research)")
    ap.add_argument("--dias", type=int, default=0, help="avisa tambien de lo que caduca en N dias")
    ap.add_argument("--solo-caducados", action="store_true", help="oculta el recuento de sin fechar")
    args = ap.parse_args()

    hoy = dt.date.today()
    limite = hoy + dt.timedelta(days=args.dias)

    raiz = Path(args.dir)
    if not raiz.is_dir():
        sys.exit(f"no existe la carpeta {raiz}")

    total = con_campos = 0
    caducados, proximos, invalidados = [], [], []

    for f in sorted(raiz.glob("*.md")):
        total += 1
        d = frontmatter(f)
        if not d:
            continue
        if any(k in d for k in CAMPOS):
            con_campos += 1

        nxt = como_fecha(d.get("next_review"))
        if nxt:
            if nxt <= hoy:
                caducados.append((nxt, f.name))
            elif args.dias and nxt <= limite:
                proximos.append((nxt, f.name))

        for inv in d.get("invalidated") or []:
            if isinstance(inv, dict):
                invalidados.append((
                    str(como_fecha(inv.get("since")) or "?"),
                    f.name,
                    inv.get("claim", "?"),
                    inv.get("evidence", "?"),
                ))

        sup = d.get("superseded_by") or []
        if isinstance(sup, str):
            sup = [sup]
        for s in sup:
            invalidados.append(("reemplazo", f.name, "fichero entero", s))

    print(f"REVISADOS {total} ficheros en {raiz}/ | con campos de vigencia: {con_campos}")
    print(f"CADUCADOS {len(caducados)}" + (f" (+{len(proximos)} caducan en {args.dias} d)" if args.dias else ""))
    for nxt, nombre in sorted(caducados):
        print(f"  - {nxt}  {nombre}")
    for nxt, nombre in sorted(proximos):
        print(f"  ~ {nxt}  {nombre}")
    print(f"INVALIDADOS {len(invalidados)}")
    for since, nombre, claim, ev in invalidados:
        print(f"  ! [{since}] {nombre}\n      {claim}\n      -> {ev}")
    if not args.solo_caducados:
        print(f"SIN FECHAR {total - con_campos} (no es error: es deuda)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
