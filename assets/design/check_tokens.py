#!/usr/bin/env python3
"""check_tokens.py - gate de trazabilidad de design-tokens.yaml

Verifica que CADA valor de color, tipografia y geometria declarado en
design-tokens.yaml existe literalmente en el CSS de las piezas de origen
(meta.measured_from). Ningun token puede ser inventado.

Uso:
    python3 check_tokens.py            # valida
    python3 check_tokens.py --quiet    # solo resumen

Salida: exit 0 si todo traza, exit 1 si hay tokens sin fuente.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("FALTA pyyaml: instalar en un venv, no en el python del sistema")

LAB = Path(__file__).resolve().parents[2]          # ~/joko-lab
TOKENS = Path(__file__).resolve().parent / "design-tokens.yaml"


def css_text(rel):
    """CSS embebido, sin espacios y con hex de 3 expandido a 6."""
    p = LAB / rel
    if not p.exists():
        return None
    h = p.read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"\s+", "", "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", h, re.S))).lower()
    return re.sub(r"#([0-9a-f]{3})\b", lambda m: "#" + "".join(c * 2 for c in m.group(1)), s)


def norm_color(c):
    c = re.sub(r"\s+", "", str(c)).lower()
    if re.fullmatch(r"#[0-9a-f]{3}", c):
        c = "#" + "".join(ch * 2 for ch in c[1:])
    if c.startswith("rgb("):
        c = "rgba(" + c[4:-1] + ",1)"
    return c


def flatten(node, prefix=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, node


def main():
    tok = yaml.safe_load(TOKENS.read_text(encoding="utf-8"))
    sources = [m["path"] for m in tok["meta"]["measured_from"]]
    corpus = ""
    for rel in sources:
        s = css_text(rel)
        if s is None:
            print(f"AVISO fuente ausente: {rel}")
            continue
        corpus += s

    items = dict(flatten(tok))
    fails = []

    # 1. colores: literal (o terna rgb) en el CSS de origen
    for k, v in items.items():
        if not re.match(r"^#?[0-9a-f]|^rgba?\(", str(v)):
            continue
        if not re.match(r"^(#[0-9a-fA-F]{3,6}|rgba?\()", str(v)):
            continue
        n = norm_color(v)
        if n.startswith("rgba("):
            terna = n[5:n.index(",1)")] if ",1)" in n else n[5:n.rindex(",")]
            ok = terna in corpus
        else:
            ok = n in corpus
        if not ok:
            fails.append(f"COLOR {k} = {v}")

    # 2. geometria y tamanos: numero desnudo presente en el CSS
    numeric_sections = ("canvas", "layout", "typography")
    for k, v in items.items():
        if not k.startswith(numeric_sections):
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            continue
        s = ("%g" % v)
        if s not in corpus and f"{s}px" not in corpus:
            fails.append(f"NUM {k} = {v}")

    if fails:
        print(f"FALLO: {len(fails)} tokens sin fuente")
        for f in fails:
            print("  " + f)
        return 1
    colors = sum(1 for k, v in items.items() if re.match(r"^(#[0-9a-fA-F]{3,6}|rgba?\()", str(v)))
    nums = sum(1 for k, v in items.items() if k.startswith(numeric_sections) and isinstance(v, (int, float)) and not isinstance(v, bool))
    print(f"OK trazabilidad: {colors} colores + {nums} numeros contra {len(sources)} fuentes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
