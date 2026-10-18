#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RULE-018 -- correccion determinista 30-sep-2026.
  (a) `pause` NO es cortafuegos -> el criterio efectivo es la PROPIEDAD (created_by)
  (b) last_validated -> 2026-09-30 + asiento machine:hermes + 2 asientos de evidence
Procedimiento gobernanza-conocimiento/references/revalidar-ko.md (Paso 4/5).
Dry-run por defecto; con --apply: backup byte-identico y UNA sola escritura.
Fail-closed: aborta SIN escribir si un ancla no aparece exactamente 1 vez.
"""
import hashlib
import shutil
import sys

import yaml

KO = "/home/jokoalmi/joko-lab/01-knowledge/objects/RULE-018.yaml"
BAK = KO + ".bak-20260930-cortafuegos"
APPLY = "--apply" in sys.argv

EM = "\u2014"  # em dash


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


src = open(KO, "rb").read().decode("utf-8")
sha_orig = sha(src)
print("KO:", KO)
print("sha256 original:", sha_orig, "| bytes:", len(src.encode("utf-8")))

# ---------------- anclas verbatim ----------------
A1 = "last_validated: '2026-09-20'\n"
N1 = "last_validated: '2026-09-30'\n"

A2 = "  (consolidation off)` " + EM + " la escritura no viene del pase de consolidacion).\n"
N2 = A2 + (
    "  Re-medido 30-sep-2026 (recuento directo de `.curator_ledger.jsonl`: 1754\n"
    "  filas desde el 01-sep, actores agent=416 / curator=1338; y `hermes curator\n"
    "  ledger`): 55 operaciones con actor `curator` en un dia sobre 7 skills y\n"
    "  subiendo mientras el agente trabajaba (51 a las 16:22 CEST, 55 a las 16:41);\n"
    "  el pase corre POR TURNO dentro de la sesion del propio agente\n"
    "  (`evidence.session_id` = sesion del gateway).\n"
)

A3 = (
    "  Cortafuegos: `hermes curator pin <skill>` (por skill, deja el curador vivo\n"
    "  para el resto " + EM + " opcion preferida por decision del usuario) o\n"
    "  `hermes curator pause` (global, reversible con `resume`). Lo escrito por el\n"
)
N3 = (
    "  Cortafuegos: `hermes curator pin <skill>` (por skill, deja el curador vivo\n"
    "  para el resto " + EM + " opcion preferida por decision del usuario; la ayuda de\n"
    "  la CLI lo describe como \"Pin a skill so the curator never auto-transitions\n"
    "  it\", asi que cubre stale/archive, y NO esta medido que bloquee los parches\n"
    "  de contenido) o `hermes curator pause` (global, reversible con `resume`),\n"
    "  que MEDIDO 30-sep-2026 NO detiene el pase por turno: `hermes curator\n"
    "  status` responde \"curator: PAUSED\" (13 corridas, la ultima hace 6d,\n"
    "  intervalo 7d) y las escrituras con actor `curator` siguieron (25-sep y\n"
    "  30-sep: 55 ops en un dia sobre 7 skills). El criterio efectivo de que el\n"
    "  curador escriba es la PROPIEDAD de la skill (`created_by`): las\n"
    "  curator-managed (96: 71 agent-created + 25 bundled) SI se editan, y las 68\n"
    "  sin marca (`created_by:null`) se RECHAZAN con el literal \"Refusing\n"
    "  background curator patch for skill '<X>': the skill is not curator-managed\n"
    "  (created_by=None). User-owned skills are off-limits to autonomous\n"
    "  curation.\" (30-sep-2026: `diagnostico-stack-local` 07:59 y 08:16,\n"
    "  `perfume-del-dia` 08:32 y 09:05, `perfume-ia` 08:33, `instagram-monitor`\n"
    "  15:15). Lo escrito por el\n"
)

A4 = "verified:\n  - by: human:jokoalmi\n    at: 2026-09-20T00:00:00Z\n"
N4 = A4 + "  - by: machine:hermes\n    at: 2026-09-30T00:00:00Z\n"

A5 = "dependencies: [RULE-008, RULE-014]\n"
EVID = (
    "- 'Re-medido 30-sep-2026 (dos instrumentos: recuento directo de "
    "`.curator_ledger.jsonl` (1754 filas desde el 01-sep, actores agent=416 / "
    "curator=1338) y `hermes curator ledger`): 55 operaciones con actor curator "
    "en un dia sobre 7 skills y subiendo mientras el agente trabajaba (51 a las "
    "16:22 CEST, 55 a las 16:41 CEST) - hermes-cron-jobs 27, "
    "edicion-aditiva-registros 11, render-html-a-imagen 10, "
    "instagram-content-extraction 4, +1 en watchdog-salud-sistema, "
    "delegacion-subagentes y vigilancia-canales-youtube. Escala x3 respecto al "
    "20-sep (16 en 4 h / 4 skills). El pase corre POR TURNO dentro de la sesion "
    "del propio agente: `evidence.session_id` = sesion del gateway (p. ej. "
    "20260930_162343_c83c97 con 4 parches en edicion-aditiva-registros a las "
    "16:27:25-29 CEST, disparada por el turno del agente que reportaba este "
    "mismo hallazgo)'\n"
    "- 'Corregido 30-sep-2026 (esta edicion): el `desc` afirmaba que "
    "`hermes curator pause` es cortafuegos - FALSO medido. `hermes curator "
    "status` responde \"curator: PAUSED\" (runs=13, last run 6d ago, interval 7d, "
    "consolidate off) y las mutaciones con actor curator continuaron (25-sep y "
    "30-sep). El corte efectivo es la PROPIEDAD de la skill: 96 curator-managed "
    "(agent-created=71, bundled=25) editables frente a 68 unmanaged "
    "(`created_by:null`) RECHAZADAS con el literal \"the skill is not "
    "curator-managed (created_by=None). User-owned skills are off-limits to "
    "autonomous curation.\" (30-sep-2026: diagnostico-stack-local 07:59 y 08:16, "
    "perfume-del-dia 08:32 y 09:05, perfume-ia 08:33, instagram-monitor 15:15; "
    "tambien bundled: \"Refusing background curator patch for bundled skill\" "
    "para blocked-page-recovery el 27-sep). Otros dos datos medidos: "
    "`.curator_suppressed` (337 B, 23-sep) lista 32 skills del catalogo bundled "
    "(ninguna del lab) y `~/.hermes/.curator_backups/blobs/` tiene 2713 blobs "
    "(reversibilidad por mutacion confirmada: el previo exacto del SKILL.md de "
    "instagram-content-extraction esta presente)'\n"
)
N5 = EVID + A5

# ---------------- 1. anclas unicas ----------------
ok = True
for name, a in (("A1 last_validated", A1), ("A2 desc-20sep", A2), ("A3 cortafuegos", A3),
                ("A4 verified", A4), ("A5 dependencies", A5)):
    c = src.count(a)
    print("ancla %-18s ocurrencias=%d" % (name, c))
    ok = ok and c == 1
if not ok:
    sys.exit("ABORTADO: alguna ancla no es unica -> NO se escribe nada")

# ---------------- 2. edicion ----------------
new = src.replace(A1, N1).replace(A2, N2).replace(A3, N3).replace(A4, N4).replace(A5, N5)

# ---------------- 3. verificacion estructural ----------------
old_d = yaml.safe_load(src)
new_d = yaml.safe_load(new)
assert set(old_d) == set(new_d), "cambia el conjunto de campos"
changed = [k for k in old_d if old_d[k] != new_d[k]]
print("campos cambiados:", changed)
assert set(changed) == {"last_validated", "desc", "evidence", "verified"}, changed
print("last_validated:", repr(old_d["last_validated"]), "->", repr(new_d["last_validated"]),
      "| tipo:", type(new_d["last_validated"]).__name__)
assert isinstance(new_d["last_validated"], str)
assert "NO detiene el pase por turno" in new_d["desc"]
assert "created_by" in new_d["desc"]
assert "opcion preferida por decision del usuario; la ayuda de" in new_d["desc"]
assert old_d["desc"].count("pause` (global, reversible con `resume`). Lo escrito") == 1
print("verified:", new_d["verified"])
print("evidence:", len(old_d["evidence"]), "->", len(new_d["evidence"]), "asientos")
assert len(new_d["evidence"]) == len(old_d["evidence"]) + 2

# lineas del original ausentes == solo las sustituidas a proposito
missing = [l for l in src.splitlines() if l not in new.splitlines()]
print("lineas del original ausentes (%d):" % len(missing))
for l in missing:
    print("   -", l)
assert len(missing) == 3, missing
assert missing[0] == "last_validated: '2026-09-20'"
assert all(l.startswith("  ") for l in missing[1:])

print("sha256 nuevo:", sha(new), "| bytes:", len(new.encode("utf-8")),
      "| delta:", len(new.encode("utf-8")) - len(src.encode("utf-8")))
print("ultimas 3 lineas nuevas:", new.splitlines()[-3:])

# ---------------- 4. escritura (solo --apply) ----------------
if not APPLY:
    print("DRY-RUN OK: no se ha escrito nada")
    sys.exit(0)

shutil.copy2(KO, BAK)
bak = open(BAK, "rb").read().decode("utf-8")
assert sha(bak) == sha_orig, "el backup no es byte-identico al original"
print("backup:", BAK, "sha256:", sha(bak), "== original:", sha(bak) == sha_orig)
with open(KO, "wb") as f:
    f.write(new.encode("utf-8"))
disk = open(KO, "rb").read().decode("utf-8")
assert sha(disk) == sha(new), "lo escrito en disco no coincide"
d = yaml.safe_load(disk)
assert d["last_validated"] == "2026-09-30" and len(d["evidence"]) == len(old_d["evidence"]) + 2
print("ESCRITO Y REVERIFICADO: sha256", sha(disk), "bytes", len(disk.encode("utf-8")))
