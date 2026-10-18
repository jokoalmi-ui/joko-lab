#!/usr/bin/env python3
"""Rectifica DOS cifras mal medidas en RULE-018 (32->30 skills suprimidos; 2713->2716 blobs)
y anade la entrada de evidence correspondiente. Backup + una sola escritura + dry-run.

  python3 fix_rule018_figs.py            # DRY-RUN (imprime diff, no escribe)
  python3 fix_rule018_figs.py --apply
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter

RUTA = "/home/jokoalmi/joko-lab/01-knowledge/objects/RULE-018.yaml"
BAK = RUTA + ".bak-20260930-figs"
LEDGER = "/home/jokoalmi/.hermes/skills/.curator_ledger.jsonl"
SUP = "/home/jokoalmi/.hermes/skills/.curator_suppressed"
BLOBS = "/home/jokoalmi/.hermes/.curator_backups/blobs"
HOY = "2026-09-30"


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ABORTA: {' '.join(cmd)} rc={r.returncode}: {r.stderr.strip()}")
    return r.stdout.strip()


def medir():
    hora = sh(["date", "+%H:%M:%S"])
    n_blobs = int(sh(["bash", "-c", f"ls -1 {BLOBS} | wc -l"]))
    sup_raw = open(SUP, "r", encoding="utf-8").read()
    sup_lineas = [l for l in sup_raw.splitlines() if l.strip()]
    sup_bytes = os.path.getsize(SUP)
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    cur = [r for r in rows if r.get("actor") == "curator"]
    hoy = [r for r in cur if str(r.get("ts", "")).startswith(HOY)]
    skills_hoy = sorted({r.get("skill") for r in hoy})
    solape = sorted(set(sup_lineas) & set(skills_hoy))
    return dict(hora=hora, n_blobs=n_blobs, sup_lineas=sup_lineas, sup_bytes=sup_bytes,
                filas=len(rows), cur=len(cur), agent=len(rows) - len(cur),
                hoy=len(hoy), skills_hoy=skills_hoy, solape=solape)


def main():
    aplicar = "--apply" in sys.argv
    m = medir()
    print(f"[medido] {m['hora']} CEST | blobs={m['n_blobs']} | suppressed: {m['sup_bytes']} B, "
          f"{len(m['sup_lineas'])} nombres [{m['sup_lineas'][0]}..{m['sup_lineas'][-1]}] | "
          f"ledger={m['filas']} filas (curator {m['cur']} / agent {m['agent']}) | "
          f"hoy curator={m['hoy']} sobre {len(m['skills_hoy'])} skills | solape suppressed-lab={m['solape']}")

    if len(m["sup_lineas"]) != 30:
        sys.exit(f"ABORTA: .curator_suppressed tiene {len(m['sup_lineas'])} nombres, no 30")
    if m["solape"]:
        sys.exit(f"ABORTA: el suppressed incluye skills del lab tocadas hoy: {m['solape']}")
    if m["n_blobs"] < 2716:
        sys.exit(f"ABORTA: blobs={m['n_blobs']} < 2716")
    if m["hoy"] < 55:
        sys.exit(f"ABORTA: hoy(curator)={m['hoy']} < 55")

    viejo = open(RUTA, "r", encoding="utf-8").read()

    n_sup, k_hoy = len(m["sup_lineas"]), len(m["skills_hoy"])
    anclas = [
        ("lista 32 skills del catalogo bundled (ninguna del lab)",
         f"lista {n_sup} skills del catalogo bundled (medido 30-sep-2026 {m['hora']} CEST con "
         f"`wc -l`: {m['sup_bytes']} B / {n_sup} nombres, [{m['sup_lineas'][0]}.."
         f"{m['sup_lineas'][-1]}], sin solape con las {k_hoy} skills del lab editadas hoy)"),
        ("tiene 2713 blobs",
         f"tiene {m['n_blobs']} blobs (medido 30-sep-2026 {m['hora']} CEST con "
         f"`ls -1 .../blobs/ | wc -l`)"),
        ("1754\n  filas desde el 01-sep, actores agent=416 / curator=1338",
         f"1754\n  filas desde el 01-sep (foto de las 16:41 CEST; {m['filas']} filas y "
         f"curator={m['cur']}\n  a las {m['hora']}), actores agent=416 / curator=1338"),
        ("recuento directo de `.curator_ledger.jsonl` (1754 filas desde el 01-sep",
         "recuento directo de `.curator_ledger.jsonl` (1754 filas desde el 01-sep, foto 16:41"),
        ("sobre 7 skills y\n  subiendo mientras",
         "sobre 7-8 nombres de\n  skill (7 en la ventana de las 16:41 y 8 a las 17:03 CEST) y\n"
         "  subiendo mientras"),
        ("30-sep: 55 ops en un dia sobre 7 skills)",
         "30-sep: 55 ops en un dia sobre 7-8 nombres de skill: 7 en la ventana de las\n"
         "  16:41 y 8 a las 17:03 CEST)"),
        ("55 operaciones con actor curator en un dia sobre 7 skills y subiendo",
         "55 operaciones con actor curator en un dia sobre 7-8 nombres de skill (7 en la "
         "ventana de las 16:41 y 8 a las 17:03 CEST) y subiendo"),
    ]
    ESPERADOS = {}
    nuevo = viejo
    for vie, nue in anclas:
        esp = ESPERADOS.get(vie, 1)
        n = nuevo.count(vie)
        if n != esp:
            sys.exit(f"ABORTA: el ancla {vie!r} aparece {n} veces (se esperaba {esp})")
        nuevo = nuevo.replace(vie, nue)

    evid_nueva = (
        "- 'Corregido 30-sep-2026 (segunda pasada, misma sesion, tras OK del usuario): dos "
        "cifras de la entrada anterior estaban mal medidas y se rectifican con instrumento - "
        f"`.curator_suppressed` NO lista 32 skills sino {len(m['sup_lineas'])} "
        f"({m['sup_bytes']} B, 23-sep, `wc -l` = {len(m['sup_lineas'])}; nombres del catalogo "
        f"bundled [{m['sup_lineas'][0]}..{m['sup_lineas'][-1]}], sin solape con las "
        f"{len(m['skills_hoy'])} skills del lab editadas hoy), y los blobs del curador NO son "
        f"2713 sino {m['n_blobs']} (medido {m['hora']} CEST con `ls -1 .../blobs/ | wc -l`; "
        "crecen con cada mutacion, luego la cifra va con fecha). El ledger, recontado a esa "
        f"hora, da {m['filas']} filas (curator {m['cur']} / agent {m['agent']}; {m['hoy']} ops "
        f"de hoy repartidas en {len(m['skills_hoy'])} nombres de skill distintos): la deriva "
        "del dia sigue viva y los skills distintos tambien (el `desc` y la entrada previa "
        "decian 7: se declara el rango sin reescribir la cifra previa). La entrada anterior "
        "se conserva tal cual y se rectifica aqui, no se reescribe (RULE-008 / "
        "edicion-aditiva-registros).'\n")
    marca = "\ndependencies: [RULE-008, RULE-014]"
    if nuevo.count(marca) != 1:
        sys.exit("ABORTA: no encuentro la linea de dependencies")
    nuevo = nuevo.replace(marca, "\n" + evid_nueva + "dependencies: [RULE-008, RULE-014]")

    assert nuevo.count(evid_nueva) == 1 and nuevo != viejo
    for k in ("id: RULE-018", "last_validated: '2026-09-30'", "confidence: 0.9",
              "scope: skills_del_lab", "version: 1"):
        assert k in nuevo, f"campo perdido: {k}"

    vie_b, nue_b = viejo.encode("utf-8"), nuevo.encode("utf-8")
    print(f"bytes: {len(vie_b)} -> {len(nue_b)} | md5 {hashlib.md5(vie_b).hexdigest()} -> "
          f"{hashlib.md5(nue_b).hexdigest()}")
    print(f"sha256 nuevo: {hashlib.sha256(nue_b).hexdigest()}")
    d = list(difflib.unified_diff(viejo.splitlines(True), nuevo.splitlines(True),
                                 "RULE-018.yaml", "RULE-018.yaml(bak-20260930-figs)", n=1))
    add = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
    rem = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
    print(f"diff: +{add} / -{rem} lineas ({len(d)} de diff)")
    print("".join(d))

    if not aplicar:
        print("[dry-run] NO se ha escrito nada. Relanzar con --apply")
        return 0

    if not os.path.exists(BAK):
        shutil.copy2(RUTA, BAK)
        print(f"[backup] {os.path.basename(BAK)} creado ({os.path.getsize(BAK)} B)")
    elif open(BAK, "rb").read() != vie_b:
        sys.exit("ABORTA: el backup existente != fichero actual")
    else:
        print(f"[backup] {os.path.basename(BAK)} ya existe e identico")

    with open(RUTA, "wb") as fh:
        fh.write(nue_b)
    disco = open(RUTA, "rb").read()
    assert disco == nue_b, "el disco no coincide con lo escrito"
    print(f"OK escrito {RUTA}: {len(disco)} B | sha256 {hashlib.sha256(disco).hexdigest()}")
    print(f"backup para revertir: cp -p {BAK} {RUTA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
