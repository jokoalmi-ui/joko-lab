#!/usr/bin/env python3
"""Extrae el bloque PUBLICABLE de post-linkedin.md a post-linkedin.txt.

Serie «IA y agentes» (research/infografias/serie-ia-agentes/).

Por que existe: post-linkedin.md mezcla material publicable con material de
trabajo (cabecera, titulo del documento, notas para publicar, datos de la
medicion). Pegar el .md entero en LinkedIn arrastra ese material de trabajo.
Este script deja en post-linkedin.txt SOLO lo que se pega, y comprueba que el
.txt y el .md llevan exactamente el mismo texto (sha256).

Uso:
    python3 extraer_post.py <carpeta-de-la-pieza | post-linkedin.md>
    python3 extraer_post.py <ruta> --check     # solo compara, no escribe
    python3 extraer_post.py --todas           # recorre todas las piezas

Formatos de marcador admitidos (los dos que hay en la serie):
    "## Texto del post"
    "**Texto de la publicacion (pegar tal cual):**"
El bloque termina en el primer separador "---", en el siguiente "## " o al
final del fichero.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD = "post-linkedin.md"
TXT = "post-linkedin.txt"
SEPARADORES = {"---", "--", "***", "___"}


def _norm(s: str) -> str:
    """minusculas y sin acentos, para reconocer los marcadores."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def localizar_md(ruta: Path) -> Path:
    if ruta.is_file():
        return ruta
    if ruta.is_dir():
        md = ruta / MD
        if not md.exists():
            raise SystemExit(f"[ERROR] no existe {md}")
        return md
    raise SystemExit(f"[ERROR] ruta no encontrada: {ruta}")


def extraer(md: Path) -> str:
    lineas = md.read_text(encoding="utf-8").split("\n")

    ini = None
    for i, linea in enumerate(lineas):
        s = linea.strip()
        n = _norm(s)
        if s.startswith("## ") and "texto del post" in n:
            ini = i + 1
            break
        if s.startswith("**") and "texto de la publicacion" in n:
            ini = i + 1
            break
    if ini is None:
        raise SystemExit(
            f"[ERROR] {md} no tiene marcador del bloque publicable "
            '("## Texto del post" o "**Texto de la publicacion (pegar tal cual):**")'
        )

    fin = len(lineas)
    for j in range(ini, len(lineas)):
        s = lineas[j].strip()
        if s in SEPARADORES or s.startswith("## "):
            fin = j
            break

    bloque = "\n".join(lineas[ini:fin]).strip()
    if not bloque:
        raise SystemExit(f"[ERROR] el bloque publicable de {md} esta VACIO")
    return bloque


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def procesar(ruta: Path, check: bool) -> bool:
    md = localizar_md(ruta)
    carpeta = md.parent
    txt = carpeta / TXT
    bloque = extraer(md)
    h = sha(bloque)

    print(f"PIEZA      : {carpeta.name}")
    print(f"MD         : {md}")
    print(f"CARACTERES : {len(bloque)} | LINEAS: {bloque.count(chr(10)) + 1}")
    print(f"SHA256     : {h[:16]}")
    print(f"1a linea   : {bloque.split(chr(10))[0][:70]}")

    if check:
        if not txt.exists():
            print(f"CHECK      : NO EXISTE {TXT}")
            print()
            return False
        actual = txt.read_text(encoding="utf-8").strip()
        iguales = actual == bloque
        print(f"CHECK      : {'IGUAL al .md' if iguales else 'DIFIERE del .md'}")
        if not iguales:
            print(f"             .txt {len(actual)} car. sha {sha(actual)[:16]}")
        print()
        return iguales

    if txt.exists() and txt.read_text(encoding="utf-8").strip() != bloque:
        marca = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = carpeta / f"{TXT}.bak-{marca}"
        shutil.copy2(txt, bak)
        print(f"BACKUP     : {bak.name} (el .txt anterior era distinto)")

    previo = txt.read_text(encoding="utf-8") if txt.exists() else None
    txt.write_text(bloque + "\n", encoding="utf-8")

    releido = txt.read_text(encoding="utf-8").strip()
    if releido != bloque:
        if previo is not None:
            txt.write_text(previo, encoding="utf-8")
        raise SystemExit("[ERROR] el .txt releido NO coincide con el bloque: revertido")

    print(f"ESCRITO    : {txt}")
    print(f"VERIFICADO : .txt == bloque del .md (sha256 {sha(releido)[:16]})")
    print()
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ruta", nargs="?", help="carpeta de la pieza o su post-linkedin.md")
    ap.add_argument("--check", action="store_true", help="solo comparar, no escribir")
    ap.add_argument("--todas", action="store_true", help="recorrer todas las piezas de la serie")
    args = ap.parse_args()

    if args.todas:
        piezas = sorted(p for p in BASE.glob("leccion-*") if (p / MD).exists())
        if not piezas:
            print("[ERROR] no hay piezas con post-linkedin.md")
            return 1
        print(f"PIEZAS CON {MD}: {len(piezas)}\n")
        ok = [procesar(p, args.check) for p in piezas]
        print(f"RESULTADO: {sum(ok)}/{len(ok)} OK")
        return 0 if all(ok) else 1

    if not args.ruta:
        ap.error("hace falta la carpeta de la pieza (o --todas)")
    return 0 if procesar(Path(args.ruta), args.check) else 1


if __name__ == "__main__":
    sys.exit(main())
