#!/usr/bin/env python3
# Anexo aditivo a 04-operations/backlogs/pendientes.md - TRIAJE de los 4 posts de IG (30-sep-2026)
# v3: fail-closed. TODOS los asertos se comprueban ANTES de escribir. Registro autorreferencial por punto fijo.
import collections, hashlib, os, shutil, subprocess, sys

REPO = "/home/jokoalmi/joko-lab"
PEND = os.path.join(REPO, "04-operations/backlogs/pendientes.md")
BAK  = os.path.join(REPO, "04-operations/backlogs/pendientes.md.bak-20260930-triaje-4posts")
SKILL = "/home/jokoalmi/.hermes/skills/media/instagram-content-extraction/SKILL.md"
MARCA = "triaje-4posts-ig-20260930"
REPORT = []

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def log(t, s=""):
    REPORT.append("===== %s =====\n%s\n" % (t, s))

def abor(t):
    log("ABORTADO", t)
    open("/tmp/ig-4posts/registro.txt", "w").write("".join(REPORT)); sys.exit(1)

# ---------- gates previos ----------
raw = open(PEND, "rb").read()
SIZE_BEFORE, MD5_BEFORE, LINES_BEFORE = len(raw), hashlib.md5(raw).hexdigest(), raw.count(b"\n")
log("antes", "size=%d md5=%s lines=%d" % (SIZE_BEFORE, MD5_BEFORE, LINES_BEFORE))
if MARCA in raw.decode("utf-8"): abor("la MARCA ya estaba (idempotencia)")
if os.path.exists(BAK): abor("el backup ya existia: %s" % BAK)

# ---------- evidencia viva (solo lectura) ----------
SHORTS = [("dailydoseofds_","Dd5sce1DF4W"),("datasciencebrain","Dd5X-6WGH1n"),
          ("codewithbrij","Dd5a_mmuZwY"),("hackproduct","Dd3stOat159")]
hits = {sc: int(sh("grep -rl --exclude-dir=.git '%s' %s 2>/dev/null | wc -l" % (sc, REPO)) or 0)
        for _, sc in SHORTS}
log("shortcodes en el lab (0 = ausente)", str(hits))
if any(hits.values()): abor("alguna pieza ya estaba en el lab: %s" % hits)

def fnum(path):
    if not os.path.exists(path): return None
    d = open(path, "rb").read()
    return (len(d), d.count(b"\n"), hashlib.md5(d).hexdigest()[:12])

WK  = os.path.join(REPO, "research/analisis-wikiskill-2026-09-17.md")
DSB = os.path.join(REPO, "research/analisis-datasciencebrain-rag.md")
CWB = os.path.join(REPO, "research/analisis-codewithbrij-top5-rag.md")
wk, dsb, cwb = fnum(WK), fnum(DSB), fnum(CWB)
for nm, v in (("wikiskill",wk),("datasciencebrain-rag",dsb),("codewithbrij-top5-rag",cwb)):
    if v is None: abor("falta el analisis previo: %s" % nm)
log("analisis previos (bytes, lineas, md5-12)", "wikiskill=%s dsb=%s cwb=%s" % (wk, dsb, cwb))

nchunk = sh("grep -rl --exclude-dir=.git --exclude-dir=.BACKUP* --exclude-dir=.archive* -i 'chunking' %s/research | wc -l" % REPO)
log("analisis con 'chunking' en research/ (SOLO vivo)", nchunk)
log("nombres vivos", sh("grep -rl --exclude-dir=.git --exclude-dir=.BACKUP* --exclude-dir=.archive* -i 'chunking' %s/research | sed 's|.*/||' | sort | tr '\\n' ' '" % REPO))

idx = sh("grep -n -E 'TextSplitter|chunk_size|chunk_overlap|separators|DB_PATH *=' %s/tools/indexer.py" % REPO)
log("indexer.py (grep -n)", idx)
for must in ("144:    splitter = RecursiveCharacterTextSplitter(", "145:        chunk_size=1000, chunk_overlap=150,",
             "146:        separators=", '25:DB_PATH = VAULT_PATH / ".lancedb"'):
    if must not in idx: abor("indexer.py no casa con lo declarado (falta %r): %s" % (must, idx))

herramientas = {}
for f in ("tools/llm_as_judge.py","tools/evaluar_rag.py","tools/rag_telemetry.py",
          "tools/banco_validacion_juez.json","tools/indexer.py","tools/juez_alucinaciones.py",
          "tools/tests/test_llm_as_judge.py","research/analisis-dailydoseofds-finetuning-5-tecnicas.md",
          "research/analisis-dailydoseofds-qm-yc-20260909.md"):
    herramientas[f] = os.path.exists(os.path.join(REPO, f))
log("rutas declaradas presentes", str(herramientas))
if not all(herramientas.values()): abor("falta alguna ruta declarada: %s" % herramientas)

src_eval = open(os.path.join(REPO,"tools/evaluar_rag.py"), encoding="utf-8", errors="replace").read().lower()
log("evaluar_rag.py: recall/precision", "recall=%s precision=%s" % ("recall" in src_eval, "precision" in src_eval))
if not ("recall" in src_eval and "precision" in src_eval): abor("evaluar_rag.py no mide recall+precision")

wk_txt = open(WK, encoding="utf-8").read()
cifras = [c for c in ("48,7","48.7","63,7","63.7") if c in wk_txt]
log("wikiskill: cifras Table 3 presentes", str(cifras))
if len(cifras) < 2: abor("no se localizan 48,7/63,7 en el analisis previo: %s" % cifras)

npurpose = sh("find %s -name 'PURPOSE.md' -not -path '*/.git/*' | wc -l" % REPO)
nskilimp = sh("find %s -name 'skill-impact.md' -not -path '*/.git/*' | wc -l" % REPO)
log("PURPOSE.md / skill-impact.md", "%s / %s" % (npurpose, nskilimp))

led = {}
for nm in ("lecciones_ledger.jsonl","retrabajo_ledger.jsonl"):
    p = sh("find %s -name '%s' -not -path '*/.git/*' | head -1" % (REPO, nm))
    led[nm] = (p, int(sh("wc -l < '%s'" % p)) if p else None)
log("ledgers (ruta, filas)", str(led))
if not all(v[1] for v in led.values()): abor("no se localizan los ledgers: %s" % led)
ninc = sh("ls %s/lpa/incidentes/revision-fallos-*.md 2>/dev/null | wc -l" % REPO)
log("revision-fallos-*.md", ninc)

skill_bytes = open(SKILL, "rb").read()
log("skill instagram (leida, sin cambios)", "%d B md5=%s" % (len(skill_bytes), hashlib.md5(skill_bytes).hexdigest()))

FECHA = sh("date '+%Y-%m-%d %H:%M:%S %Z'")

# ---------- bloque (con placeholders autorreferenciales) ----------
TMPL = """
## {fecha} — TRIAJE de los 4 posts de Instagram elegidos por el usuario: 1 ya estaba en el lab, 2 validaciones, 1 sin entrada, y UN futurible real (WikiSkill)

MARCA: {marca}

- **Que se hizo y con que**: los 4 posts se extrajeron **sin login** (caption integro y fecha por `og:description` / `og:title` de la pagina del post) y cada uno se cruzo contra el lab **en solo lectura**. 0 GPU, 0 modelos cargados, 0 escrituras fuera de `/tmp/ig-4posts/`. **Ninguno de los 4 shortcodes aparecia en el lab**: `grep -rl` = 0 para `Dd5sce1DF4W` (dailydoseofds_), `Dd5X-6WGH1n` (datasciencebrain), `Dd5a_mmuZwY` (codewithbrij) y `Dd3stOat159` (hackproduct).
- **1) `dailydoseofds_` `Dd5sce1DF4W` (29-sep-2026, 44 likes, 0 comentarios) — difusion de WikiSkill: YA ESTABA, sin entrada nueva.** El paper es real (arXiv 2608.27454v1, Google Research + Virginia Tech) y el lab **ya lo analizo el 17-sep**: `research/analisis-wikiskill-2026-09-17.md` ({wkb} B, {wkl} lineas). La unica cifra del post («cae un cuarto») **se sostiene** con la Table 3 de ese analisis: sin wiki 48,7 vs 63,7 de media -> **-23,6 %**. El post no aporta tecnica ni cifra nueva. El canal tampoco era nuevo: ya tenia dos analisis vivos en `research/` (`analisis-dailydoseofds-finetuning-5-tecnicas.md` y `analisis-dailydoseofds-qm-yc-20260909.md`); un tercero (`...-finetuning-lora-rag.md`) esta archivado en `research/.archive-20260902/` y NO se cuenta como vigente.
- **2) `datasciencebrain` `Dd5X-6WGH1n` — «RAG observability»: VALIDACION.** El lab ya tiene juez propio (`tools/llm_as_judge.py`, `tools/juez_alucinaciones.py` y su test `tools/tests/test_llm_as_judge.py`), banco de validacion (`tools/banco_validacion_juez.json`), metricas (`tools/evaluar_rag.py`: recall y precision) y telemetria (`tools/rag_telemetry.py`); y ya analizo a este mismo canal el 03-sep (`research/analisis-datasciencebrain-rag.md`, {dsbb} B, {dsbl} lineas). Lo unico distinto es el **envase**: el PDF va tras suscripcion de Rs.45/mes (mismo embudo que el post de agosto ya analizado).
- **Lo que NO se puede verificar del post 2**: el «el juez acerto 38-40 de 40» es **CLAIM del post** y el PDF esta detras de pago -> no se contrasta. No se da por bueno.
- **3) `codewithbrij` `Dd5a_mmuZwY` — diagrama del bucle plan -> act -> observe: SIN ENTRADA.** Material didactico: sin tecnica nueva, sin cifra, sin recurso medible. Solo **CONFIRMA** dos cosas ya vigentes en el lab: guardarrailes antes de ejecutar (`least-privilege-lab`) y OK humano para acciones irreversibles (la regla de escritura del lab). El canal ya estaba analizado (`research/analisis-codewithbrij-top5-rag.md`).
- **4) `hackproduct` `Dd3stOat159` — «6 estrategias de chunking»: CONFIRMA, cero novedad.** El lab usa **exactamente la #3 (recursive)**, con separadores markdown: `tools/indexer.py` (clase importada en la L16; **L144-146** `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\\n## ", "\\n### ", "\\n\\n", "\\n", " "])` sobre `.lancedb` (L25)). El tema esta tratado en **{nchunk} ficheros** de `research/` (entre ellos `analisis-techwithram-chunking-rag`, `analisis-thinklab-chunking-rag`, `analisis-chunkless-rag-docling`, `analisis-rag-indexing-strategies`, `analisis-datasciencebrain-rag`, `analisis-atareao-graphrag`). El post **no trae ninguna medicion**: solo recomendaciones.
- **Autocorreccion medida (para que no se repita)**: la primera version de esta entrada citaba dos datos **mal**: `verification/banco_validacion_juez.json` (ruta inexistente; el fichero real es `tools/banco_validacion_juez.json`) y `indexer.py:47-50` (las lineas reales son **144-146**). Los asertos previos del script de anexo **abortaron antes de escribir nada**; el gate funciono. Leccion: en citas de fichero/linea, medir con `grep -n` antes de afirmar, no tirar de la memoria de una salida anterior.
- **Limite declarado (no se inventa)**: el **numero de laminas** de cada post NO se afirma. El JSON embebido de la pagina del post devuelve el bloque del **feed lateral** (`carousel_media_count: 20` en un post suelto) y las claves van con comillas escapadas. El caption, la fecha y las interacciones SI son fiables por `og:title`/`og:description`. Es lo que ya avisa la skill `instagram-content-extraction` (lineas 87-97): **hoy se ha comportado como dice y no ha hecho falta tocarla** (md5 `{md5skill}`, {sizekskill} B, sin cambios).
- **FUTURIBLE anotado (unico hueco real) — WikiSkill**: la idea aprovechable (una wiki persistente por skill con el **por que** de cada intento fallido) el lab ya la tiene **a mano pero dispersa**. Medido: `PURPOSE.md` por skill = **{npurpose} ficheros**; `skill-impact.md` = **{nskilimp} ficheros**; el «por que» vive hoy en `lpa/incidentes/revision-fallos-*.md` (**{ninc}**) y en los ledgers `lecciones_ledger.jsonl` (**{nlec} filas**) y `retrabajo_ledger.jsonl` (**{nret} filas**). **Senal real, no urgente**: no se instala nada y no se toca ninguna skill; solo se evaluaria si el usuario lo pide.
- **No tocado**: n8n, Docker, stack, servicios, BD de perfumes, `/mnt/ssd_ia_datos`, ledgers y `~/.hermes` (de las skills solo se ha LEIDO `instagram-content-extraction`). Scripts y volcados de trabajo en `/tmp/ig-4posts/`.
- **Registro de escritura**: `04-operations/backlogs/pendientes.md`, **{sb} B y {lb} lineas** antes (md5 `{mb}`, backup `pendientes.md.bak-20260930-triaje-4posts`) -> **{sa} B y {la} lineas** tras la entrada (bloque de **{bl} B**). Solo se anade: **0 lineas eliminadas** (membresia de TODAS las lineas del backup = True). MARCA unica: `{marca}`. Gates del anexo: destino byte a byte el medido (tamano + md5 predichos), backup inexistente antes, entrada ausente antes (idempotencia), puramente aditivo y relectura **del disco**.
"""

fmt = dict(fecha=FECHA, marca=MARCA, wkb=wk[0], wkl=wk[1], dsbb=dsb[0], dsbl=dsb[1], nchunk=nchunk,
           md5skill=hashlib.md5(skill_bytes).hexdigest(), sizekskill=len(skill_bytes),
           npurpose=npurpose, nskilimp=nskilimp, ninc=ninc,
           nlec=led["lecciones_ledger.jsonl"][1], nret=led["retrabajo_ledger.jsonl"][1],
           sb=SIZE_BEFORE, lb=LINES_BEFORE, mb=MD5_BEFORE)

# punto fijo: el bloque declara su propio tamano y las lineas del fichero final
sa, la, bl = SIZE_BEFORE, LINES_BEFORE, 0
for i in range(12):
    txt = TMPL.format(sa=sa, la=la, bl=bl, **fmt)
    nsa, nla, nbl = SIZE_BEFORE + len(txt.encode()), LINES_BEFORE + txt.count("\n"), len(txt.encode())
    log("iteracion %d" % i, "bl=%d sa=%d la=%d" % (nbl, nsa, nla))
    if (nsa, nla, nbl) == (sa, la, bl):
        break
    sa, la, bl = nsa, nla, nbl
else:
    abor("el punto fijo no converge")
bloque = TMPL.format(sa=sa, la=la, bl=bl, **fmt)
assert len(bloque.encode()) == bl and SIZE_BEFORE + len(bloque.encode()) == sa
log("bloque final", "bytes=%d lineas=%d" % (bl, bloque.count("\n")))

final = raw + bloque.encode("utf-8")
MD5_AFTER_PRED = hashlib.md5(final).hexdigest()
log("prediccion destino", "size=%d lines=%d md5=%s" % (len(final), final.count(b"\n"), MD5_AFTER_PRED))

# ---------- escritura ----------
shutil.copy2(PEND, BAK)
if hashlib.md5(open(BAK, "rb").read()).hexdigest() != MD5_BEFORE: abor("el backup no es byte a byte el original")
with open(PEND, "ab") as f: f.write(bloque.encode("utf-8"))

# ---------- verificacion leyendo el otro lado ----------
raw2 = open(PEND, "rb").read()
log("despues (disco)", "size=%d md5=%s lines=%d" % (len(raw2), hashlib.md5(raw2).hexdigest(), raw2.count(b"\n")))
a = collections.Counter(raw.decode("utf-8").splitlines())
b = collections.Counter(raw2.decode("utf-8").splitlines())
ok_add = all(b[l] >= n for l, n in a.items())
gates = dict(size_ok=len(raw2) == sa, md5_ok=hashlib.md5(raw2).hexdigest() == MD5_AFTER_PRED,
             lines_ok=raw2.count(b"\n") == la, aditivo=ok_add,
             marca_1_vez=raw2.decode("utf-8").count(MARCA) == 1)
log("GATES", str(gates))
log("git status", sh("cd %s && git status --porcelain && git diff --stat" % REPO))
log("cola (ultimas 3 lineas)", "\n".join(raw2.decode("utf-8").splitlines()[-3:]))
open("/tmp/ig-4posts/registro.txt", "w").write("".join(REPORT))
print("FIN: ", gates)
