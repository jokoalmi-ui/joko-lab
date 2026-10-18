#!/usr/bin/env python3
# Alta de OBS-154 con gate fail-closed: citas literales + cifras + intocables.
# SIN --apply = dry-run (no escribe nada). Con --apply escribe y verifica desde disco.
import sys, hashlib, pathlib

REPO = pathlib.Path("/home/jokoalmi/joko-lab")
DEST = REPO / "01-knowledge/observations/OBS-154-curador-edita-skills-sin-ok-2026-09-30.md"
DRAFT = pathlib.Path("/tmp/ig-4posts/OBS-154.draft.md")
APPLY = "--apply" in sys.argv

def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()
def txt(p):
    return pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
def norm(s):
    return " ".join(s.split())

IM = [
    REPO / "04-operations/backlogs/pendientes.md",
    REPO / "01-knowledge/objects/RULE-018.yaml",
    pathlib.Path("/home/jokoalmi/.hermes/skills/media/instagram-content-extraction/SKILL.md"),
    pathlib.Path("/home/jokoalmi/.hermes/skills/media/instagram-content-extraction/references/veredicto-y-cruce-con-el-lab.md"),
]
CITAS = [
    ("bg-review en agent.log", pathlib.Path("/home/jokoalmi/.hermes/logs/agent.log"),
     "msg='Review the conversation above and update the skill library. Be ACTIVE"),
    ("fila del ledger", pathlib.Path("/home/jokoalmi/.hermes/skills/.curator_ledger.jsonl"),
     '"ts": "2026-09-30T14:15:08.079389+00:00"'),
    ("referencia del curador", pathlib.Path("/home/jokoalmi/.hermes/skills/media/instagram-content-extraction/references/veredicto-y-cruce-con-el-lab.md"),
     "Nº de láminas: solo si el bloque JSON del post cuadra con la fecha de ese post"),
    ("RULE-018", REPO / "01-knowledge/objects/RULE-018.yaml",
     "Si el diff es consolidacion en sitio y la leccion ya esta escrita, NO se escribe nada: se reporta."),
    ("rechazo user-owned", pathlib.Path("/home/jokoalmi/.hermes/logs/agent.log"),
     "the skill is not curator-managed (created_by=None). User-owned skills are off-limits to autonomous curation."),
    ("paused:true", pathlib.Path("/home/jokoalmi/.hermes/skills/.curator_state"),
     '"paused": true'),
]
CIFRAS = [("RULEs activas", "01-knowledge/objects/RULE-*.yaml", 18),
          ("OBS previos", "01-knowledge/observations/OBS-*.md", 151)]

err = []
print("== 0. destino ==")
print("DEST:", DEST, "| existe:", DEST.exists())
if DEST.exists():
    err.append("el destino YA existe (no se sobrescribe)")

print("== 1. borrador ==")
if not DRAFT.exists():
    err.append("no existe el borrador %s" % DRAFT)
    print(err[-1]); sys.exit(1)
draft_raw = txt(DRAFT)
draft = norm(draft_raw)
print("borrador: %d B, %d lineas" % (len(DRAFT.read_bytes()), len(DRAFT.read_text(encoding='utf-8').splitlines())))

print("== 2. citas (en la fuente Y en el borrador) ==")
for nombre, src, frag in CITAS:
    f = norm(frag)
    en_src = f in norm(txt(src)) if src.exists() else False
    en_draft = f in draft
    print("  %-22s fuente=%-5s borrador=%-5s" % (nombre, en_src, en_draft))
    if not en_src: err.append("cita NO encontrada en la fuente: %s" % nombre)
    if not en_draft: err.append("cita NO citada en el borrador: %s" % nombre)

print("== 3. cifras ==")
for nombre, pat, esperado in CIFRAS:
    real = len(list(REPO.glob(pat)))
    print("  %-14s esperado=%d real=%d %s" % (nombre, esperado, real, "OK" if real == esperado else "FALLA"))
    if real != esperado: err.append("cifra '%s': esperado %d, real %d" % (nombre, esperado, real))

print("== 4. negativos ==")
neg = [("el destino no existe", lambda: not DEST.exists()),
       ("RULE-018 NO distingue 'curator-managed'", lambda: "curator-managed" not in txt(REPO / "01-knowledge/objects/RULE-018.yaml")),
       ("el borrador NO afirma el rollback ejecutado", lambda: "rollback ejecutado" not in draft)]
for nombre, fn in neg:
    ok = fn(); print("  %-42s %s" % (nombre, ok))
    if not ok: err.append("negativo falla: %s" % nombre)

print("== 5. intocables (md5 PRE) ==")
pre = {p: md5(p) for p in IM}
for p, h in pre.items(): print("  %s %s" % (h[:16], str(p).replace("/home/jokoalmi/", "~/")))

if err:
    print("\nGATE FAIL-CLOSED: %d fallo(s). NO se escribe nada:" % len(err))
    for e in err: print("  -", e)
    sys.exit(1)

if not APPLY:
    print("\nDRY-RUN OK: todo verifica. Volver a lanzar con --apply para escribir.")
    sys.exit(0)

print("== 6. escritura ==")
DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(draft_raw, encoding="utf-8")
b = DEST.read_bytes()
print("escrito: %d B, md5 %s" % (len(b), hashlib.md5(b).hexdigest()))

print("== 7. verificacion desde disco ==")
disco = txt(DEST); disco_n = norm(disco)
print("  md5 disco == md5 escrito:", md5(DEST) == hashlib.md5(b).hexdigest())
print("  lineas:", len(disco.splitlines()))
faltan = [n for n, s, f in CITAS if norm(f) not in disco_n]
print("  citas presentes en el disco:", len(CITAS) - len(faltan), "/", len(CITAS), "| faltan:", faltan)
err2 = []
if disco != draft_raw: err2.append("el contenido en disco NO es identico al borrador")
if faltan: err2.append("faltan citas en disco: %s" % faltan)
print("== 8. intocables (md5 POST) ==")
for p in IM:
    mismo = md5(p) == pre[p]
    print("  %-5s %s" % ("IGUAL" if mismo else "CAMBIO", str(p).replace("/home/jokoalmi/", "~/")))
    if not mismo: err2.append("intocable modificado: %s" % p)
if err2:
    print("\nFALLO TRAS ESCRIBIR:"); [print("  -", e) for e in err2]; sys.exit(2)
print("\nALTA_OK: OBS escrito y verificado desde disco; intocables intactos.")
