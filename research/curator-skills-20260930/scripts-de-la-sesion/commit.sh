#!/bin/bash
# Commit con recibo de la entrada de pendientes.md (30-sep-2026). Fail-closed.
set -e
cd /home/jokoalmi/joko-lab
R="04-operations/backlogs/pendientes.md"

echo "== 1. staging SOLO el fichero =="
git add -- "$R"
echo "-- git diff --cached --name-only --"; git diff --cached --name-only
N=$(git diff --cached --name-only | wc -l)
test "$N" -eq 1
test "$(git diff --cached --name-only)" = "$R"

echo "== 2. blob del INDICE vs blob del DISCO =="
BI=$(git ls-files -s -- "$R" | awk '{print $2}')
BD=$(git hash-object -- "$R")
echo "index=$BI  disco=$BD"
test "$BI" = "$BD"

echo "== 3. lineas ANADIDAS del diff staged (para leerlas antes de firmar) =="
git diff --cached -- "$R" | grep '^+' | grep -v '^+++' | wc -l
git diff --cached -- "$R" | grep '^+' | grep -v '^+++' | cut -c1-120

echo "== 4. recibo =="
bash hooks/generar_recibo.sh joseba "cierre 30-sep: triaje de los 4 posts IG + futurible WikiSkill"
cat .git/joko-recibo.json
RT=$(python3 -c "import json;print(json.load(open('.git/joko-recibo.json'))['tree_sha'])")
WT=$(git write-tree)
echo "tree recibo=$RT  write-tree=$WT"
test "$RT" = "$WT"

echo "== 5. commit (el gate valida) =="
git commit -m "backlog: cierre 30-sep - triaje de los 4 posts IG elegidos (1 ya en el lab, 2 validaciones, 1 sin entrada) + futurible WikiSkill (PURPOSE.md y skill-impact.md = 0 ficheros)"
echo "== 6. verificacion leyendo el otro lado =="
git log -1 --format='%h %ad %s' --date=iso
HEADT=$(git rev-parse HEAD^{tree})
echo "tree recibo=$RT  HEAD^{tree}=$HEADT"
test "$RT" = "$HEADT" && echo "RECIBO_OK: tree_sha == HEAD^{tree}"
git show --stat --format= HEAD
echo "-- ficheros trackeados --"; git ls-files -- "$R"
echo "-- status (repr linea a linea) --"; git status --porcelain | python3 -c "import sys;[print(repr(l.rstrip())) for l in sys.stdin]"
echo "-- log del gate --"; tail -2 ~/.hermes/logs/joko-rdd.log
echo "FIN_OK"
