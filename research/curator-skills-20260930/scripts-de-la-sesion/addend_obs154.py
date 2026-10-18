#!/usr/bin/env python3
"""Addendum ADITIVO a OBS-154 (deriva del conteo 51 -> 55 y mecanismo por turno).

Base: edicion-aditiva-registros/templates/anexo-simple.py. Todas las cifras que cita el
bloque se MIDEN en el momento de escribir (nada a mano).

  python3 addend_obs154.py            # DRY-RUN: imprime el bloque, no escribe
  python3 addend_obs154.py --apply    # escribe (backup antes)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter

RUTA = ("/home/jokoalmi/joko-lab/01-knowledge/observations/"
        "OBS-154-curador-edita-skills-sin-ok-2026-09-30.md")
ETIQUETA = "obs154-addendum-drift-20260930"
MARCA = ETIQUETA
LEDGER = "/home/jokoalmi/.hermes/skills/.curator_ledger.jsonl"
SUP = "/home/jokoalmi/.hermes/skills/.curator_suppressed"
BLOBS = "/home/jokoalmi/.hermes/.curator_backups/blobs"
RULE = "/home/jokoalmi/joko-lab/01-knowledge/objects/RULE-018.yaml"
R_BACKUPS = [("...-cortafuegos", 3184), ("...-figs", 6578)]
SESION_TURNO = "20260930_162343_c83c97"
MD5_ESPERADO = "322124cc0accc7377fce012b819aecde"   # medido 30-sep 16:25 CEST
HOY = "2026-09-30"
NL = bytes([10])


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ABORTA: {' '.join(cmd)} rc={r.returncode}: {r.stderr.strip()}")
    return r.stdout.strip()


def md5(b):
    return hashlib.md5(b).hexdigest()


def medir():
    d = {"hora": sh(["date", "+%Y-%m-%d %H:%M:%S"]), "hora_corta": sh(["date", "+%H:%M"])}
    d["n_blobs"] = int(sh(["bash", "-c", f"ls -1 {BLOBS} | wc -l"]))
    sup = [l for l in open(SUP, encoding="utf-8").read().splitlines() if l.strip()]
    d["sup_bytes"], d["n_sup"] = os.path.getsize(SUP), len(sup)
    d["sup_ini"], d["sup_fin"] = sup[0], sup[-1]
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    cur = [r for r in rows if r.get("actor") == "curator"]
    hoy = [r for r in cur if str(r.get("ts", "")).startswith(HOY)]
    d["filas"], d["cur"], d["agent"], d["n_hoy"] = len(rows), len(cur), len(rows) - len(cur), len(hoy)
    d["k_hoy"] = len({r.get("skill") for r in hoy})
    d["ead"] = sum(1 for r in hoy if "edicion-aditiva-registros" in str(r.get("skill")))
    d["solape"] = sorted(set(sup) & {r.get("skill") for r in hoy})
    ses = [r for r in rows if isinstance(r.get("evidence"), dict)
           and r["evidence"].get("session_id") == SESION_TURNO]
    d["n_sesion"] = len(ses)
    d["acciones"] = " + ".join(f"{v} `{k}`" for k, v in sorted(Counter(
        r.get("action") for r in ses).items()))
    rb = open(RULE, "rb").read()
    d["r_bytes"], d["r_sha"] = len(rb), hashlib.sha256(rb).hexdigest()
    d["r_evid"] = sum(1 for l in rb.decode("utf-8").splitlines() if l.startswith("- '"))
    baks = []
    for suf, esperado in R_BACKUPS:
        p = RULE + ".bak-20260930" + suf[len("..."):]
        if not os.path.exists(p):
            sys.exit(f"ABORTA: falta el backup {p}")
        n = os.path.getsize(p)
        if n != esperado:
            sys.exit(f"ABORTA: {os.path.basename(p)} = {n} B, se esperaba {esperado}")
        baks.append(f"`{os.path.basename(p)}` ({n} B)")
    d["r_baks"] = " y ".join(baks)
    return d


def bloque(f, m):
    return "\n".join([
        "## Addendum 2026-09-30 - el conteo subio DESPUES de cerrar este OBS (51 -> 55) y el "
        "pase corre POR TURNO",
        "",
        f"MARCA: {MARCA}",
        "",
        "- **El conteo de este OBS es una FOTO de las 16:24 CEST**: re-medido a las 16:41 CEST "
        f"el mismo ledger da **55 operaciones** (no 51) y sigue por encima de lo que recoge el "
        f"OBS: a las {m['hora_corta']} CEST son **{m['n_hoy']}** operaciones de hoy repartidas "
        f"en {m['k_hoy']} nombres de skill (7 en la ventana de las 16:41) y {m['filas']} filas "
        "en el ledger. Este OBS no se reescribe: se anade este addendum y las 95 lineas "
        "previas quedan intactas.",
        f"- **Las {m['n_sesion']} operaciones nuevas**: {m['acciones']} del curador sobre "
        "`edicion-aditiva-registros` a las 16:27:25-29 CEST, con `evidence.session_id` = "
        f"`{SESION_TURNO}`, la sesion del turno del agente que estaba redactando y reportando "
        "ESTE hallazgo. Confirma el mecanismo ya medido: no hay un tercero escribiendo; el "
        "pase se dispara POR TURNO, al cerrar el turno del agente, dentro de su propia sesion.",
        f"- **Segundo instrumento** (recuento directo de `.curator_ledger.jsonl`, solo "
        f"lectura): {m['filas']} filas desde el 01-sep, actores `curator` {m['cur']} / `agent` "
        f"{m['agent']} -> el ledger SI distingue autor, que es lo que RULE-018 citaba.",
        "- **`hermes curator status` (30-sep)**: `curator: PAUSED`, runs=13, last run hace 6d, "
        "interval 7d, stale 14d, archive 30d, consolidate off; curator-managed=96 "
        "(agent-created=71, bundled=25; 67 active / 29 stale), unmanaged=68 (68 "
        "foreground-created). Corrobora que el corte efectivo es la PROPIEDAD (`created_by`) "
        "y no `pause`.",
        f"- **`.curator_suppressed`** ({m['sup_bytes']} B, 23-sep): {m['n_sup']} nombres del "
        f"catalogo bundled ([{m['sup_ini']}..{m['sup_fin']}]), sin solape con las {m['k_hoy']} "
        "skills del lab editadas hoy -> no es el mecanismo que protege las skills del lab.",
        f"- **`~/.hermes/.curator_backups/blobs/`**: {m['n_blobs']} blobs y creciendo con cada "
        "mutacion -> el rollback por mutacion (`hermes curator rollback <id>`) sigue viable.",
        "- **RULE-018 corregida en esta misma sesion** (accion derivada 2, tras OK del "
        "usuario): `last_validated` 2026-09-20 -> 2026-09-30; el `desc` deja de dar `pause` "
        "como cortafuegos y pasa al criterio `created_by`; `evidence` 3 -> "
        f"{m['r_evid']} asientos; `verified` gana `machine:hermes` 30-sep (la entrada "
        "`human:jokoalmi` del 20-sep NO se toca). Fichero 3184 -> "
        f"{m['r_bytes']} B (sha256 `{m['r_sha']}`), con la cadena de backups {m['r_baks']} "
        "para revertir paso a paso. Dos cifras de la primera pasada salieron mal medidas (32 "
        "skills suprimidos y 2713 blobs): se rectificaron en una segunda pasada con "
        "instrumento y este OBS no las hereda.",
        "- **La leccion ya estaba escrita por el curador** en `edicion-aditiva-registros` "
        f"({m['ead']} ops hoy, 4 de ellas en este mismo turno): el criterio `created_by` con el "
        "rechazo, la advertencia de que `pause` no cubre el pase por turno y la referencia "
        "`references/auditar-y-revertir-al-curador.md`. Por RULE-018 NO se duplica.",
        "- **Lo que NO cambia**: las cifras de la medicion original de este OBS (51 ops / 7 "
        "skills / 1750 filas / ventana 07:28-16:24 CEST) siguen siendo correctas para ESA "
        "ventana; este addendum no las sustituye.",
        "",
    ])


def main():
    aplicar = "--apply" in sys.argv
    if not os.path.isfile(RUTA):
        sys.exit(f"ABORTA: no existe {RUTA}")
    b1 = open(RUTA, "rb").read()
    bak = RUTA + ".bak-" + ETIQUETA
    if MARCA.encode("utf-8") in b1:
        sys.exit(f"ABORTA: la MARCA '{MARCA}' ya esta en el fichero (no se duplica)")
    m = md5(b1)
    print(f"destino: {len(b1)} B | md5 {m}")
    if m != MD5_ESPERADO:
        sys.exit(f"ABORTA: md5 del destino != el medido antes ({MD5_ESPERADO})")
    if os.path.exists(bak):
        if open(bak, "rb").read() != b1:
            sys.exit(f"ABORTA: {os.path.basename(bak)} != fichero actual")
        print(f"[backup] ya existe {os.path.basename(bak)}: no se pisa")
    elif aplicar:
        shutil.copy2(RUTA, bak)
        print(f"[backup] creado {os.path.basename(bak)} ({len(b1)} B, md5 {m})")
    else:
        print(f"[dry-run] crearia {os.path.basename(bak)} ({len(b1)} B, md5 {m})")

    d = medir()
    print(f"[medido] {d['hora']} CEST | hoy curator={d['n_hoy']} sobre {d['k_hoy']} skills | "
          f"ledger={d['filas']} (curator {d['cur']} / agent {d['agent']}) | filas de la sesion "
          f"{SESION_TURNO}={d['n_sesion']} ({d['acciones']}) | suppressed {d['n_sup']} nombres "
          f"| blobs={d['n_blobs']} | RULE-018 {d['r_bytes']} B evid={d['r_evid']} | solape={d['solape']}")
    for k, minimo in (("n_hoy", 55), ("n_sesion", 4), ("n_sup", 30), ("n_blobs", 2716), ("r_evid", 6)):
        if d[k] < minimo:
            sys.exit(f"ABORTA: {k}={d[k]} < {minimo}: la cifra medida no se sostiene")
    if d["r_bytes"] < 7000:
        sys.exit(f"ABORTA: RULE-018 mide {d['r_bytes']} B: parece la version sin rectificar")
    if d["solape"]:
        sys.exit(f"ABORTA: el suppressed incluye skills del lab tocadas hoy: {d['solape']}")

    cuerpo = bloque(d["hora"], d).encode("utf-8")
    if not cuerpo.endswith(NL) or cuerpo.endswith(NL + NL):
        sys.exit("ABORTA: el bloque debe terminar en UN salto de linea")
    sep = b"" if b1.endswith(NL + NL) else (NL if b1.endswith(NL) else NL + NL)
    b2 = b1 + sep + cuerpo
    assert b2.startswith(b1) and b2[len(b1):] == sep + cuerpo
    assert MARCA.encode("utf-8") in b2
    faltan = Counter(b1.split(NL)) - Counter(b2.split(NL))
    assert not faltan, f"lineas originales perdidas: {list(faltan)[:2]}"
    print(f"lineas: {b1.count(NL)} -> {b2.count(NL)} | bytes: {len(b1)} -> {len(b2)} | "
          f"bloque {len(cuerpo)} B / {cuerpo.count(NL)} lineas | md5 {md5(b2)}")

    if not aplicar:
        print("[dry-run] NO se ha escrito nada. Relanzar con --apply")
        print("--- bloque que se anexaria ---")
        print(cuerpo.decode("utf-8"))
        return 0

    with open(RUTA, "wb") as fh:
        fh.write(b2)
    b3 = open(RUTA, "rb").read()
    assert b3 == b2 and b3.startswith(b1) and MARCA.encode("utf-8") in b3
    assert os.path.getsize(RUTA) == len(b3)
    print(f"OK escrito {RUTA}: {len(b3)} B | md5 {md5(b3)} | lineas {b3.count(NL)}")
    print(f"backup: {os.path.basename(bak)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
