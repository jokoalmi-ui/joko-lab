#!/bin/bash
# Commit con recibo: OBS-154 + pendientes.md (30-sep-2026). Fail-closed.
set -e
cd /home/jokoalmi/joko-lab
OBS="01-knowledge/observations/OBS-154-curador-edita-skills-sin-ok-2026-09-30.md"
P="04-operations/backlogs/pendientes.md"

echo "== 1. staging SOLO los dos ficheros =="
git add -- "$OBS" "$P"
n=$(git diff --cached --name-only | wc -l)
[ "$n" -eq 2 ] || { echo "ABORTA: staged=$n ficheros (esperado 2)"; exit 1; }
git diff --cached --name-only

echo "== 2. blob del indice == blob del disco =="
for f in "$OBS" "$P"; do
  a=$(git ls-files -s -- "$f" | awk '{print $2}')
  b=$(git hash-object -- "$f")
  echo "$f  index=$a  disco=$b"
  [ "$a" = "$b" ] || { echo "ABORTA: blob distinto en $f"; exit 1; }
done

echo "== 3. resumen del diff =="
git diff --cached --stat

echo "== 4. lineas anadidas en pendientes.md =="
git diff --cached -- "$P" | grep '^+' | cut -c1-150

echo "== 5. cabecera del OBS anadido =="
git diff --cached -- "$OBS" | grep '^+' | sed -n '1,12p' | cut -c1-110

echo "== 6. recibo (aprobado por: joseba) =="
bash hooks/generar_recibo.sh joseba "OBS-154: hallazgo del curador de Hermes (51 ops / 7 skills el 30-sep) + aviso en pendientes"

echo "== 7. commit =="
git commit -m "obs: OBS-154 - el curador de Hermes edita skills del lab sin OK (51 operaciones sobre 7 skills el 30-sep) + aviso en pendientes.md"

echo "== 8. verificacion post-commit =="
git log -1 --format='%H|%h|%ad|%s' --date=iso
T=$(git rev-parse HEAD^{tree})
RT=$(python3 -c "import json;print(json.load(open('.git/joko-recibo.json'))['tree_sha'])")
echo "tree recibo=$RT"
echo "tree HEAD  =$T"
[ "$T" = "$RT" ] && echo "RECIBO_OK: tree_sha == HEAD^{tree}" || { echo "FALLO: recibo != HEAD^{tree}"; exit 1; }
git show --stat --format= HEAD
echo "== 9. estado final del arbol =="
git status --porcelain
echo FIN_OK
