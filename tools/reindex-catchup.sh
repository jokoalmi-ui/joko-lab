#!/bin/bash
# Joko Lab — Re-indexador con captura de arranque (cada hora)
# Respaldo del daily de las 08:00 (rag-reindex.sh) si el PC estaba apagado o si el
# daily murió a mitad. Va FASE POR FASE con flag propio porque el presupuesto del job
# es GLOBAL (config `cron.script_timeout_seconds`, hoy 300 s) y no se puede subir para
# un solo job: si el daily se corta, la hora siguiente retoma lo que falte sin repetir
# lo ya hecho.
#
#   fase A  indexer.py (notas)                    -> /tmp/.rag-reindex-today
#   fase B  index_query_summary.py (QS)           -> /tmp/.rag-qs-today      [15-oct-2026]
#   fase C  compactación de TODAS las tablas      -> (idempotente)           [15-oct-2026]
#
# Por qué B y C (medido el 15-oct-2026): el catchup solo hacía A + optimize(joko_notes),
# así que un día con timeout del daily (9 casos: 17-ago … 12-oct) dejaba
# joko_summaries/joko_queries sin las filas del día hasta el siguiente daily que
# terminase (10-oct 4.130 → 14-oct 4.167 summaries: +46 de golpe) y dejaba 3 de las 4
# tablas sin compactar (26 versiones el 10-oct, 77 el 14-oct → camino del caso 13 GB
# del 11-ago, skill local-rag). El daily también escribe ambos flags: sin eso, el
# catchup de la tarde repetiría el trabajo del día (pitfall de la skill hermes-cron-jobs).
#
# Si las dos fases ya están hechas hoy, sale SIN IMPRIMIR NADA (la salida del job se
# queda en "silent (empty output)" = normal, como hasta ahora).
FLAG_FILE="${RAG_FLAG_FILE:-/tmp/.rag-reindex-today}"
QS_FLAG_FILE="${RAG_QS_FLAG_FILE:-/tmp/.rag-qs-today}"
INDEXER="${HOME}/joko-lab/tools/indexer.py"
QS_INDEXER="${HOME}/joko-lab/tools/index_query_summary.py"
VENV_PYTHON="${RAG_VENV_PYTHON:-${HOME}/.venv/hermes-rag/bin/python3}"
TODAY=$(date +%Y-%m-%d)

ya_hoy () { [ -f "$1" ] && [ "$(cat "$1" 2>/dev/null)" = "$TODAY" ]; }

# Nada que hacer: mismas condiciones que antes -> salida vacía
if ya_hoy "$FLAG_FILE" && ya_hoy "$QS_FLAG_FILE"; then
    exit 0
fi

# --- fase A: notas nuevas/modificadas -----------------------------------------
if ya_hoy "$FLAG_FILE"; then
    echo "  [i] fase A: notas ya re-indexadas hoy ($TODAY)"
else
    echo "[$(date '+%H:%M')] A) Re-indexando RAG (captura de arranque)..."
    cd "${HOME}" && $VENV_PYTHON "$INDEXER" 2>&1 | tail -3
    # se marca al TERMINAR la fase: un corte posterior (B o C) no re-hace A
    echo "$TODAY" > "$FLAG_FILE"
fi

# --- fase C: compactar TODAS las tablas (evita acumular versiones: 13 GB 11-ago) --
# Va ANTES de B a propósito: la fase B es la más pesada de las tres y en un scope
# de 4 GiB puede ser OOM-killed (pico medido el 15-oct: 4,54 GiB antes de pasar la
# escritura a Arrow, 3,50 GiB después);
# si el OOM se lleva la unidad, con el orden A-B-C la compactación no llegaría a
# correr (justo el riesgo de las 13 GB). Con A-C-B la compactación siempre se hace.
# El daily sí hace A-B-C (allí C limpia las versiones que crea B); aquí B deja 1-2
# versiones extra como mucho hasta el daily de la mañana siguiente.
echo "[$(date '+%H:%M')] C) Compactando LanceDB (todas las tablas)..."
$VENV_PYTHON -c "
import lancedb
db = lancedb.connect('${HOME}/joko-lab/.lancedb')
for tname in sorted(db.table_names()):
    try:
        t = db.open_table(tname)
        antes = len(t.list_versions())
        t.optimize()
        t.cleanup_old_versions(older_than=0)  # garantiza limpieza (no deprecated en todas las versiones)
        print(f'  {tname}: {t.count_rows()} filas, {antes} -> {len(t.list_versions())} versiones')
    except Exception as e:
        print(f'  [aviso] {tname}: compactacion no disponible: {str(e)[:80]}')
" 2>&1 | tail -6

# --- fase B: Query+Summary (incremental, sidecar propio) ----------------------
if ya_hoy "$QS_FLAG_FILE"; then
    echo "  [i] fase B: Query+Summary ya hecho hoy ($TODAY)"
else
    echo "[$(date '+%H:%M')] B) Query+Summary Indexing (joko_summaries/joko_queries)..."
    if salida_qs=$($VENV_PYTHON "$QS_INDEXER" 2>&1); then
        echo "$salida_qs" | tail -4
        echo "$TODAY" > "$QS_FLAG_FILE"
    else
        rc_qs=$?
        echo "$salida_qs" | tail -6
        echo "  [aviso] Query+Summary falló (rc=$rc_qs); sin flag -> se reintenta la hora siguiente"
    fi
fi

echo "[$(date '+%H:%M')] Catch-up de re-indexado terminado."
exit 0
