#!/usr/bin/env bash
# informe-diario-local.sh — Informe diario de Joko Lab con R1-14B LOCAL
# Piloto del router local/cloud (09-ago-2026).
#
# Recopila el estado real del lab (solo lectura) y lo resume con
# llm-router.sh batch (R1-14B local) en vez de DeepSeek cloud.
# Salida: reports/YYYY-MM-DD-informe-local.txt
set -euo pipefail

FECHA=$(date +%Y%m%d)
FECHA_LARGA=$(date '+%Y-%m-%d %H:%M %Z')
LAB=/home/jokoalmi/joko-lab
OUT_DIR="$LAB/04-operations/reports"
OUT="$OUT_DIR/${FECHA}-informe-local.txt"

# ── 1. Recopilar estado (solo lectura) ──
ESTADO="Estado de Joko Lab a $FECHA_LARGA

## Tests
$(cd $LAB && python3 -m unittest discover -s tests 2>&1 | tail -2)

## Complejidad de codigo
$(python3 $LAB/tools/complejidad_crap.py 2>&1 | sed -n '4,6p')

## Servicios
$(systemctl --user is-active joko-indexer.service joko-reranker.service team-bus-watch.service 2>/dev/null | tr '\n' ' ')

## GPU
memoria_usada_mb | memoria_total_mb | uso_gpu_pct | temperatura_c   (ese es el orden de los numeros; crudo de nvidia-smi)
$(timeout 20 nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader 2>/dev/null || echo "GPU: sin respuesta — nvidia-smi no devolvio nada en 20 s (NVML colgada?)")

## RAG
$(~/.venv/hermes-rag/bin/python3 -c "
import lancedb
db = lancedb.connect('$LAB/.lancedb')
t = db.open_table('joko_notes')
print(f'Filas LanceDB: {t.count_rows()}')
" 2>/dev/null || echo 'no disponible')

## Pendientes con fecha
$(grep -E 'INT-[0-9]+' $LAB/04-operations/prospective-memory.md 2>/dev/null | head -5 || echo 'sin prospective')"

# ── 2. Resumir con el modelo LOCAL (router batch) ──
# MAX_TOKENS=1200: R1 razona antes de responder (benchmark 13-ago: completa
# ~1150 tokens). Con el default 400 se queda en el pensamiento y el informe
# sale como razonamiento en voz alta, no como resumen.
# Se captura el exit code sin que set -e aborte (if en línea) para poder
# generar el informe degradado si el motor local no está disponible.
# ADEMÁS (fix 15-ago): si R1 no carga, el router cae al fallback GLM y GLM
# responde en reasoning_content ("Got it, let's tackle...") → ese razonamiento
# NO es un resumen válido. Se valida el resumen y se degrada si huele a
# razonamiento o error de motor.
# R3 (14-oct-2026): cuando el resumen se descarta, el TEXTO que devolvio el
# router se registra en un ledger (antes se perdia: el "motor ocupado" era
# indiagnosticable). No cambia el comportamiento del informe; solo añade una
# nota con la ruta del volcado.
DESCARTES="$LAB/04-operations/metrics/informe_descartes.jsonl"
NOTA_DESCARTE=""
registrar_descarte() {   # $1 = motivo  ($2 = texto, opcional: se llama con 1 arg)
    DESCARTE_MOTIVO="$1" DESCARTE_TEXTO="${2:-}" DESCARTE_LEDGER="$DESCARTES" \
    /usr/bin/python3 - <<'PY' 2>/dev/null || true
import json, os, pathlib
from datetime import datetime, timedelta, timezone
txt = os.environ.get("DESCARTE_TEXTO", "")
p = pathlib.Path(os.environ["DESCARTE_LEDGER"])
p.parent.mkdir(parents=True, exist_ok=True)
fila = {"ts": datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds"),
        "fuente": "informe-diario-local.sh",
        "motivo": os.environ.get("DESCARTE_MOTIVO", ""),
        "chars": len(txt), "texto": txt[:4000]}
with p.open("a", encoding="utf-8") as f:
    f.write(json.dumps(fila, ensure_ascii=False) + "\n")
PY
}
# stderr del router a fichero: sus avisos ("Cargando modelo ...") NO son el resumen.
# Antes se capturaban con 2>&1 y contaminaban $RESUMEN -> descarte falso de un resumen valido.
ERR_ROUTER="${TMPDIR:-/tmp}/informe-router-$(date +%Y%m%d).err"
if RESUMEN=$(MAX_TOKENS=1200 bash $LAB/tools/llm-router.sh batch "Genera un informe ejecutivo conciso (max 12 lineas) del estado de Joko Lab con estos datos. Destaca: problemas reales, servicios caidos, tendencias. En espanol, directo, sin relleno: Los numeros del bloque ## GPU van en este orden: memoria_usada_mb, memoria_total_mb, uso_gpu_pct y temperatura_c. No hay memoria disponible ni procesos en cola: no los menciones; y si un dato no tiene etiqueta, no lo interpretes.

$ESTADO" 2>"$ERR_ROUTER"); then
    # Validar que el resumen es un resumen, no razonamiento/error del motor
    case "$RESUMEN" in
        *"Got it"*|*"let's tackle"*|*"Cargando modelo"*|*"ERROR:"*|*"no se pudo cargar"*)
            echo "⚠️ resumen inválido (razonamiento o error de motor) → degradado" >&2
            registrar_descarte "descarte_heuristica" "$RESUMEN"
            NOTA_DESCARTE=$'\n# Descarte del resumen local: 04-operations/metrics/informe_descartes.jsonl (motivo: descarte_heuristica)'
            RESUMEN="(resumen local no disponible — motor ocupado; ver datos crudos)"
            ;;
    esac
else
    echo "ERROR: el router local fallo — se genera informe sin resumen LLM" >> "$OUT"
    registrar_descarte "router_fallo" "$RESUMEN"
    NOTA_DESCARTE=$'\n# Descarte del resumen local: 04-operations/metrics/informe_descartes.jsonl (motivo: router_fallo)'
    RESUMEN="(resumen local no disponible)"
fi

# ── 3. Verificar veracidad del resumen (gate 16-ago-2026) ──
# Etiqueta de certeza visible: [VERIFICADO] / [ALCANCE INTERNO] / [NO VERIFICADO] / [REVISAR]
# El informe recopila estado INTERNO del lab → se espera ALCANCE_INTERNO o VERIFICADO.
# Si el gate marca NO VERIFICADO o REVISAR, se anota en el informe (no bloquea).
VERIFICADOR=$LAB/tools/verificador_alucinaciones.py
if [ -f "$VERIFICADOR" ]; then
    # Caso especial: resumen degradado (placeholder) → no es contenido factual, etiqueta neutra
    case "$RESUMEN" in
        "(resumen local no disponible"*|"ERROR: el router local fallo"*)
            ETIQUETA="[SIN RESUMEN — GATE OMITIDO]"
            VEREDICTO="GATE_OMITIDO"
            ;;
        *)
            # Ejecutar UNA vez con `|| true` para no disparar pipefail (el verificador
            # sale exit 1 cuando bloquea; sin esto el fallback se añade a la salida).
            VER_RESULT=$(python3 "$VERIFICADOR" --texto "$RESUMEN" --tema "estado de Joko Lab" --json 2>/dev/null || true)
            ETIQUETA=$(echo "$VER_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('etiqueta','[NO VERIFICADO]'))" 2>/dev/null || echo "[NO VERIFICADO]")
            VEREDICTO=$(echo "$VER_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('veredicto','ERROR'))" 2>/dev/null || echo "ERROR")
            ;;
    esac
else
    ETIQUETA="[gate no disponible]"
    VEREDICTO="GATE_AUSENTE"
fi

# ── 3.5. Juez de calidad (LLM-as-Judge, integrado 22-ago-2026) ──
# El gate de veracidad dice si es CIERTO; el juez dice si está BIEN HECHO.
# UN_JUEZ probable (gpt-oss ya cargado para el resumen; GLM no cabe con él).
# No bloquea: si tarda >45s o no hay juez, anota "omitido" y el informe sale igual.
JUEZ=$LAB/tools/llm_as_judge.py
JUEZ_TAG="CALIDAD: omitido"
if [ -f "$JUEZ" ] && [[ "$RESUMEN" != "(resumen local no disponible"* ]]; then
    JUEZ_RESULT=$(timeout 45 python3 "$JUEZ" --pregunta "Genera un informe ejecutivo conciso (max 12 lineas) del estado de Joko Lab con estos datos. Destaca: problemas reales, servicios caidos, tendencias. En espanol, directo, sin relleno" --respuesta "$RESUMEN" --contexto "$ESTADO" --json 2>/dev/null || true)
    JUEZ_TAG=$(echo "$JUEZ_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('CALIDAD: ' + d.get('veredicto','ERROR') + ' (' + str(d.get('promedio','?')) + ')')" 2>/dev/null || echo "CALIDAD: omitido")
fi

# ── 4. Guardar informe ──
mkdir -p "$OUT_DIR"
cat > "$OUT" <<EOF
# Informe diario de Joko Lab — ${FECHA_LARGA}
# Motor: gpt-oss LOCAL (llm-router.sh batch) — piloto local/cloud
# Gate de veracidad: ${ETIQUETA} (${VEREDICTO})
# Juez de calidad: ${JUEZ_TAG}${NOTA_DESCARTE}

## Resumen (gpt-oss local)
$RESUMEN

---
## Datos crudos
$ESTADO
EOF

echo "Informe guardado: $OUT"
echo "---"
cat "$OUT" | head -20
