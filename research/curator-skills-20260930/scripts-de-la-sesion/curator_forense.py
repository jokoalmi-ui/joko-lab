#!/usr/bin/env python3
# Forense: que escribio el curador de fondo en las skills (30-sep-2026)
import json, os, re, difflib, glob

SP = "/home/jokoalmi/.hermes/cache/spillover"
OUT = "/tmp/ig-4posts/curator_diff.txt"
L = []
def p(*a): L.append(" ".join(str(x) for x in a))

SK = "/home/jokoalmi/.hermes/skills/media/instagram-content-extraction/SKILL.md"
EAD = "/home/jokoalmi/.hermes/skills/joko-lab/edicion-aditiva-registros/SKILL.md"
VYT = "/home/jokoalmi/.hermes/skills/joko-lab/vigilancia-canales-youtube/SKILL.md"

# 1) inventario de spillovers: a que skill corresponde cada uno
p("=== SPILLOVERS (identificacion) ===")
sp_files = sorted(glob.glob(SP + "/*.txt"), key=os.path.getmtime)
mtime = {}
for f in sp_files:
    mtime[f] = os.path.getmtime(f)
# solo los de hoy (>= 2026-09-30 14:00)
import time
CUT = time.mktime(time.strptime("2026-09-30 14:00:00", "%Y-%m-%d %H:%M:%S"))
for f in sp_files:
    raw = open(f, encoding="utf-8", errors="replace").read()
    head = raw[:400].replace("\n", " ")
    # buscar marca de skill
    m = re.findall(r'name="([a-z0-9_\-/]+)"', raw[:2000]) or re.findall(r"'name':\s*'([^']+)'", raw[:2000])
    p("-", os.path.basename(f), "| mtime", time.strftime("%H:%M:%S", time.localtime(mtime[f])), "| bytes", len(raw), "| skill?", (m[0] if m else "?"), "| head:", head[:120])

# 2) diff del volcado ANTERIOR al patch vs fichero ACTUAL
def payload(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    try:
        j = json.loads(raw)
        if isinstance(j, dict):
            for k in ("content", "text", "result", "body"):
                if k in j and isinstance(j[k], str):
                    return j[k]
            return json.dumps(j)[:0] or raw
    except Exception:
        pass
    return raw

p("")
p("=== DIFF: volcado del curador (16:13:30) vs SKILL.md ACTUAL (16:15:08) ===")
cand = [f for f in sp_files if "987" in f or "9285" in f]
if not cand:
    cand = [f for f in sp_files if mtime[f] > CUT]
p("ficheros candidatos:", [os.path.basename(c) for c in cand])
cur = open(SK, encoding="utf-8").read()
for f in cand:
    pl = payload(f)
    if "Antes de contar slides" not in pl and "instagram" not in pl[:2000].lower():
        p("  (descartado:", os.path.basename(f), ")")
        continue
    a = pl.splitlines()
    b = cur.splitlines()
    d = list(difflib.unified_diff(a, b, fromfile="curador_16:13:30", tofile="actual_16:15:08", lineterm="", n=1))
    p("--- diff de", os.path.basename(f), "--- lineas:", len(d))
    for line in d[:80]:
        p("   ", line[:300])
    if len([x for x in d if x.startswith("+") and not x.startswith("+++")]) == 0:
        p("    (sin diferencias)")

# 3) tamano actual de las 3 skills
p("")
p("=== ESTADO ACTUAL DE LAS 3 SKILLS TOCADAS HOY ===")
import hashlib
for f in (SK, EAD, VYT):
    st = os.stat(f)
    md5 = hashlib.md5(open(f, "rb").read()).hexdigest()
    p("-", f.replace("/home/jokoalmi/.hermes/skills/", ""), "| bytes", st.st_size, "| lineas", sum(1 for _ in open(f, encoding="utf-8", errors="replace")), "| md5", md5, "| mtime", time.strftime("%H:%M:%S", time.localtime(st.st_mtime)))

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("OK ->", OUT, len(L), "lineas")
