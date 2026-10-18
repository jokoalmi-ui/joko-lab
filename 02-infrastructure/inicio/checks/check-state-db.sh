#!/bin/bash
# check-state-db.sh — Salud de ~/.hermes/state.db (session store de Hermes)
# Protocolo de inicio.sh: exit 0 = OK, 1 = WARN, >=2 = FAIL
#
# Origen: incidente 02-03 sep 2026 (corrupción FTS messages_fts/messages_fts_trigram,
# "database disk image is malformed" / "file is not a database").
# Documentado: LEC-20260814-006, DEC-005.yaml, backlog 2026-09-03.
# Cobertura: quick_check + foreign_key_check + errores recientes en errors.log.
# Umbral (definido 03-sep-2026, revisado 07-sep-2026 con datos): últimas 48h —
#   0 ocurrencias -> OK
#   1-2 ocurrencias de corrupción real -> WARN
#   3+ ocurrencias, O cualquier "file is not a database" -> FAIL
# Nota: "file is not a database" es FAIL directo: marcó la transición a
# corrupción grave en el incidente del 02-sep (22:57), no es tolerable como aislado.
# Revisión 07-sep-2026: el race #94736 ("closed while a write was still in flight")
# se separó de MALFORMED y cuenta como WARN, no FAIL. Datos: 5 ocurrencias el
# 07-sep correlacionadas con crons (multi-writer WAL), BD íntegra en quick_check +
# FK y fix upstream _pread_db_header presente -> el race loguea pero no corrompe.
# Si la corrupción vuelve a ser real, sale por MALFORMED o por la Parte 1.

DB="$HOME/.hermes/state.db"
LOG="$HOME/.hermes/logs/errors.log"
HORAS=48

# --- 1. Integridad de la BD ---
if [ ! -f "$DB" ]; then
    echo "FAIL: $DB no existe"
    exit 2
fi

QUICK=$(sqlite3 "file:$DB?mode=ro" "PRAGMA quick_check;" 2>/dev/null | head -1)
if [ "$QUICK" != "ok" ]; then
    echo "FAIL: state.db quick_check -> ${QUICK:-error al leer la BD}"
    exit 2
fi

FK_VIOL=$(sqlite3 "file:$DB?mode=ro" "PRAGMA foreign_key_check;" 2>/dev/null | head -1)
if [ -n "$FK_VIOL" ]; then
    echo "FAIL: state.db foreign_key_check -> $FK_VIOL"
    exit 2
fi

# --- 2. Errores recientes de corrupción en errors.log (últimas $HORAS horas) ---
if [ ! -f "$LOG" ]; then
    echo "OK: state.db íntegro (quick_check + foreign_key_check); errors.log no existe"
    exit 0
fi

SINCE=$(date -d "$HORAS hours ago" '+%Y-%m-%d %H:%M')

# Baseline post-reparación (añadido 03-sep-2026, opción B validada): toda
# reparación documentada termina reiniciando el gateway -> su ActiveEnterTimestamp
# marca el último punto known-good. Si es MÁS reciente que la ventana de $HORAS
# horas, se usa como inicio de ventana: los rastros del incidente anterior a la
# reparación dejan de dar FAIL (~48h de ruido) y la corrupción NUEVA posterior
# al arranque se sigue contando. Fail-safe: si systemctl --user no está
# disponible, el servicio está parado o el parseo falla -> ventana de $HORAS
# horas (comportamiento previo). La Parte 1 (quick_check + FK) NO se toca: si la
# corrupción persiste en disco, FAIL sale por ahí aunque los logs viejos se ignoren.
GW_TS=$(systemctl --user show hermes-gateway.service -p ActiveEnterTimestamp --value 2>/dev/null | head -1)
if [ -n "$GW_TS" ]; then
    GW_SINCE=$(date -d "$GW_TS" '+%Y-%m-%d %H:%M' 2>/dev/null)
    if [ -n "$GW_SINCE" ] && [ "$GW_SINCE" \> "$SINCE" ]; then
        SINCE="$GW_SINCE"
    fi
fi

# Solo líneas CON timestamp (evita doble conteo de tracebacks sin fecha)
ES_TIMESTAMP='^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'
# La frase de corrupción solo cuenta si aparece en el prefijo REAL del log,
# NO dentro de un payload sanitizado " (was: {...})" (agent.message_sanitization
# loggea tool_calls irreparables cuyo contenido puede citar la frase como texto
# documental -> falso positivo, caso real 03-sep-2026: 3 de 5 hits eran payload).
NOTDB=$(awk -v since="$SINCE" '$0 ~ es && $0 >= since {p=index($0," (was: "); if (match($0,/file is not a database/) && (p==0 || RSTART<p)) c++} END {print c+0}' es="$ES_TIMESTAMP" "$LOG")
MALFORMED=$(awk -v since="$SINCE" '$0 ~ es && $0 >= since {p=index($0," (was: "); if (match($0,/database disk image is malformed|vtable constructor failed/) && (p==0 || RSTART<p)) c++} END {print c+0}' es="$ES_TIMESTAMP" "$LOG")
# Race #94736 (teardown/worker multi-writer WAL): separado desde 07-sep-2026.
# Benigno post-fix upstream #100519 (_pread_db_header): WARN informativo, no FAIL.
RACE=$(awk -v since="$SINCE" '$0 ~ es && $0 >= since {p=index($0," (was: "); if (match($0,/closed while a write was still in flight/) && (p==0 || RSTART<p)) c++} END {print c+0}' es="$ES_TIMESTAMP" "$LOG")

if [ "$NOTDB" -gt 0 ]; then
    echo "FAIL: $NOTDB 'file is not a database' en errors.log (últimas ${HORAS}h)"
    exit 2
elif [ "$MALFORMED" -ge 3 ]; then
    echo "FAIL: $MALFORMED error(es) de corrupción de state.db en errors.log (últimas ${HORAS}h)"
    exit 2
elif [ "$MALFORMED" -ge 1 ]; then
    echo "WARN: $MALFORMED error(es) de corrupción de state.db en errors.log (últimas ${HORAS}h)"
    exit 1
elif [ "$RACE" -ge 1 ]; then
    echo "WARN: $RACE race(s) #94736 (teardown/worker WAL) en errors.log; BD íntegra en quick_check + FK"
    exit 1
fi

echo "OK: state.db íntegro (quick_check + foreign_key_check), sin errores recientes"
exit 0
