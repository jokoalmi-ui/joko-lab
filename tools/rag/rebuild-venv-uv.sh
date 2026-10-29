#!/usr/bin/env bash
# Reconstruye el venv del RAG con uv a partir del lockfile (rapido y reproducible).
#
#   bash tools/rag/rebuild-venv-uv.sh                       # crea/actualiza $VENV
#   bash tools/rag/rebuild-venv-uv.sh /ruta/otro-venv       # en otra ruta
#   bash tools/rag/rebuild-venv-uv.sh --check               # solo compara con el lock
#
# uv resuelve e instala en paralelo (~10x mas rapido que pip) y `uv pip sync`
# deja el entorno EXACTAMENTE en las versiones del lock: borra lo que sobra.
# No se toca el venv vivo salvo que se le pase su ruta a proposito.
#
# TRAMPA VISTA (29-oct): con la cache de uv corrupta, `uv pip sync` dejo el venv
# SIN `certifi/cacert.pem` y todo HTTPS petaba con FileNotFoundError dentro de
# ssl.create_default_context (parecia un fallo de red). Sintoma tipico: un
# `Failed to install ... RECORD: No such file or directory`. Solucion:
#   uv cache clean && uv pip sync --python ... --reinstall --no-cache <lock>
# y comprobar integridad: cada fichero del RECORD debe existir en disco.
set -euo pipefail

LAB="/home/jokoalmi/joko-lab"
LOCK="$LAB/tools/rag/requirements.lock.txt"
VENV="${VENV_OBJETIVO:-/home/jokoalmi/.venv/hermes-rag}"
PYBIN="$VENV/bin/python3"
UV="$(command -v uv || true)"

[ -n "$UV" ] || { echo "ERROR: uv no esta en el PATH"; exit 1; }
[ -f "$LOCK" ] || { echo "ERROR: falta $LOCK"; exit 1; }
echo "[uv] $("$UV" --version) | lock: $(grep -c '==' "$LOCK") paquetes"

if [ "${1:-}" = "--check" ]; then
    # OJO: un venv creado por `uv venv` NO trae pip -> `python -m pip freeze`
    # devuelve 0 paquetes y el diff daria OK falso. Se usa `uv pip freeze`.
    # La comparacion normaliza el nombre (jaraco.classes / jaraco_classes /
    # jaraco-classes son el mismo paquete) e ignora pip, que no va en el lock.
    "$UV" pip check --python "$PYBIN"
    "$UV" pip freeze --python "$PYBIN" > /tmp/_rag_freeze_$$.txt
    # OJO: con `set -e`, un `python ... ; rc=$?` mata el script en el fallo y se
    # pierden el mensaje y el rm. Por eso el patron `rc=0` + `|| rc=$?`.
    rc=0
    "$PYBIN" - "$LOCK" /tmp/_rag_freeze_$$.txt <<'EOF' || rc=$?
import re, sys
def norma(path):
    d = {}
    for l in open(path):
        l = l.strip()
        if not l or l.startswith("#") or "==" not in l:
            continue
        n, v = l.split("==", 1)
        n = n.split("[")[0].strip().lower().replace("_", "-").replace(".", "-")
        if n in ("pip", "setuptools", "wheel"):
            continue
        d[n] = v.strip()
    return d
lock, vivo = norma(sys.argv[1]), norma(sys.argv[2])
faltan = {k: v for k, v in lock.items() if k not in vivo}
sobran = {k: v for k, v in vivo.items() if k not in lock}
distintas = {k: (lock[k], vivo[k]) for k in lock if k in vivo and lock[k] != vivo[k]}
print(f"lock={len(lock)} vivo={len(vivo)} faltan={len(faltan)} sobran={len(sobran)} distintas={len(distintas)}")
for k, v in list(faltan.items())[:5]:
    print("  FALTA", k, v)
for k, v in list(distintas.items())[:5]:
    print("  DISTINTA", k, v)
# `sobran` NO tumba el check (un venv puede tener paquetes de mas a proposito),
# pero se LISTA: antes se contaba en el resumen y nunca se veia el nombre.
for k, v in list(sobran.items())[:5]:
    print("  SOBRA", k, v)
sys.exit(0 if not (faltan or distintas) else 1)
EOF
    if [ $rc -eq 0 ]; then echo "OK: el venv coincide con el lock"; else echo "DIFERENCIAS venv vs lock (arriba)"; fi
    rm -f /tmp/_rag_freeze_$$.txt
    exit $rc
fi

[ $# -ge 1 ] && VENV="$1" && PYBIN="$VENV/bin/python3"

if [ ! -x "$PYBIN" ]; then
    echo "[uv] creando venv en $VENV (python 3.14)"
    "$UV" venv --python 3.14 "$VENV"
fi

echo "[uv] sync del lock..."
"$UV" pip sync --python "$PYBIN" "$LOCK"

echo "[check] imports clave:"
"$PYBIN" - <<'EOF'
import importlib
mods = ["lancedb", "lance", "pyarrow", "numpy", "torch", "transformers",
        "sentence_transformers", "sklearn", "pandas"]
# `flask` estaba en esta lista y NO pertenece a este venv: no lo importa ningun
# modulo del RAG (solo aparece en skills de referencia vendorizadas), no esta en
# el lock y no estaba ni en el venv viejo. Su ausencia tumbaba el script con rc=1
# DESPUES de un sync correcto, que es la peor forma de fallar: invita a hacer
# rollback de un venv bueno.
for m in mods:
    try:
        mod = importlib.import_module(m)
        print(f"  {m:22s} {getattr(mod, '__version__', 'ok')}")
    except Exception as e:
        print(f"  {m:22s} FALLA: {e}")
        raise SystemExit(1)
# El lock NO registra el sufijo local de torch (`uv pip freeze` imprime 2.13.0
# aunque este instalado 2.13.0+cu130), asi que un rebuild puede dejar un torch
# sin GPU y el resto del check pasaria igual. Esta es la unica puerta de CUDA.
import torch
if not torch.cuda.is_available():
    print(f"  {'CUDA':22s} FALLA: torch {torch.__version__} sin CUDA (indice/whl equivocado)")
    raise SystemExit(1)
print(f"  {'cuda':22s} {torch.version.cuda} · {torch.cuda.get_device_name(0)}")
EOF
echo "OK: venv listo en $VENV"
