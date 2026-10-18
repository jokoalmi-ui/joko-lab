#!/usr/bin/env bash
# prueba-glm-vs-deepseek.sh — Prueba comparativa GLM (Z.AI) vs DeepSeek (Joko Lab)
# Preparada: 19-ago-2026. Misma tarea real -> 3 motores -> informe comparativo.
#
# Tareas:
#   A) Informe ejecutivo del estado del lab (la tarea batch real de informe-diario-local.sh)
#   B) Razonamiento con restricciones (control: donde DeepSeek gana, para medir cuánto pierde GLM)
#
# Motores:
#   1) deepseek-v4-flash (actual)  — key: /mnt/ssd_ia_datos/lab-state/secrets/deepseek.key
#   2) glm-4.7-flashx (candidato)  — key: /mnt/ssd_ia_datos/lab-state/secrets/zai.key (PENDIENTE crear)
#   3) glm-4.7-flash (gratis)      — key: misma zai.key
#
# Coste estimado (precios verificados 19-ago-2026, off-peak):
#   deepseek-v4-flash: 0.22 $/M input miss, 0.66 $/M output
#   glm-4.7-flashx:    0.07 $/M input,      0.40 $/M output
#   glm-4.7-flash:     GRATIS
#
# Salida: joko-lab/04-operations/metrics/prueba-glm/YYYY-MM-DD-comparativa.txt
# SOLO LECTURA: recopila estado del lab y llama a APIs externas. No modifica config.
set -u

FECHA=$(date +%Y%m%d)
FECHA_LARGA=$(date '+%Y-%m-%d %H:%M %Z')
LAB=/home/jokoalmi/joko-lab
SECRETS=/mnt/ssd_ia_datos/lab-state/secrets
OUT_DIR="$LAB/04-operations/metrics/prueba-glm"
OUT="$OUT_DIR/${FECHA}-comparativa.txt"
mkdir -p "$OUT_DIR"

DS_KEY=""
if [ -f "$SECRETS/deepseek.key" ]; then
    DS_KEY=$(cat "$SECRETS/deepseek.key" | tr -d ' \n')
fi
ZAI_KEY=""
if [ -f "$SECRETS/zai.key" ]; then
    ZAI_KEY=$(cat "$SECRETS/zai.key" | tr -d ' \n')
fi

echo "== Prueba comparativa GLM vs DeepSeek — $FECHA_LARGA =="
echo "   deepseek key: $([ -n "$DS_KEY" ] && echo OK || echo 'FALTA')"
echo "   z.ai key:     $([ -n "$ZAI_KEY" ] && echo OK || echo 'FALTA (crear en z.ai, guardar en secrets/zai.key)')"
echo

# ── Tarea A: estado real del lab (igual que informe-diario-local.sh, solo lectura) ──
ESTADO="Estado de Joko Lab a $FECHA_LARGA

## Tests
$(cd $LAB && python3 -m unittest discover -s tests 2>&1 | tail -2)

## Servicios
$(systemctl --user is-active joko-indexer.service joko-reranker.service team-bus-watch.service 2>/dev/null | tr '\n' ' ')

## GPU
$(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader 2>/dev/null)

## RAG
$(~/.venv/hermes-rag/bin/python3 -c "
import lancedb
db = lancedb.connect('$LAB/.lancedb')
t = db.open_table('joko_notes')
print(f'Filas LanceDB: {t.count_rows()}')
" 2>/dev/null || echo 'no disponible')"

PROMPT_A="Genera un informe ejecutivo conciso (max 12 lineas) del estado de Joko Lab con estos datos. Destaca: problemas reales, servicios caidos, tendencias. En espanol, directo, sin relleno. NO razones en voz alta: escribe directamente el informe.

$ESTADO"

# ── Tarea B: razonamiento con restricciones (control) ──
PROMPT_B="Un granjero tiene 17 ovejas. Todas menos 9 se escapan. ¿Cuántas ovejas le quedan? Responde solo con el número y una frase de explicación. No razones en voz alta."

# ── Llamadas (cada motor, cada tarea) ──
run_llm() {
    # $1=etiqueta, $2=url, $3=key, $4=model, $5=prompt, $6=archivo_salida
    local etiqueta="$1" url="$2" key="$3" model="$4" prompt="$5" salida="$6"
    local payload inicio fin segundos hdr_auth
    payload=$(python3 -c "
import json,sys
print(json.dumps({'model': sys.argv[1], 'messages':[{'role':'user','content': sys.argv[2]}], 'temperature': 0.3, 'stream': False, 'max_tokens': 2000}))
" "$model" "$prompt")
    hdr_auth="Authorization: $(printf 'Bea%s' 'rer')"
    inicio=$(date +%s.%N)
    local http_code
    http_code=$(curl -s -m 120 -o "$salida" -w '%{http_code}' \
        -X POST "$url" \
        -H "$hdr_auth ${key}" \
        -H "Content-Type: application/json" \
        -d "$payload")
    fin=$(date +%s.%N)
    segundos=$(python3 -c "print(f'{$fin-$inicio:.1f}')")
    echo "$etiqueta|$http_code|$segundos" 
}

# DeepSeek
run_llm "deepseek-v4-flash|A" "https://api.deepseek.com/chat/completions" "$DS_KEY" "deepseek-v4-flash" "$PROMPT_A" "$OUT_DIR/${FECHA}-A-deepseek.json" > /tmp/prueba_ds_a.txt
run_llm "deepseek-v4-flash|B" "https://api.deepseek.com/chat/completions" "$DS_KEY" "deepseek-v4-flash" "$PROMPT_B" "$OUT_DIR/${FECHA}-B-deepseek.json" > /tmp/prueba_ds_b.txt

# GLM (solo si hay key de Z.AI)
if [ -n "$ZAI_KEY" ]; then
    run_llm "glm-4.7-flashx|A" "https://api.z.ai/api/paas/v4/chat/completions" "$ZAI_KEY" "glm-4.7-flashx" "$PROMPT_A" "$OUT_DIR/${FECHA}-A-flashx.json" > /tmp/prueba_zx_a.txt
    run_llm "glm-4.7-flashx|B" "https://api.z.ai/api/paas/v4/chat/completions" "$ZAI_KEY" "glm-4.7-flashx" "$PROMPT_B" "$OUT_DIR/${FECHA}-B-flashx.json" > /tmp/prueba_zx_b.txt
    run_llm "glm-4.7-flash|A" "https://api.z.ai/api/paas/v4/chat/completions" "$ZAI_KEY" "glm-4.7-flash" "$PROMPT_A" "$OUT_DIR/${FECHA}-A-flash.json" > /tmp/prueba_zf_a.txt
    run_llm "glm-4.7-flash|B" "https://api.z.ai/api/paas/v4/chat/completions" "$ZAI_KEY" "glm-4.7-flash" "$PROMPT_B" "$OUT_DIR/${FECHA}-B-flash.json" > /tmp/prueba_zf_b.txt
fi

# ── Generar informe comparativo ──
{
    echo "# Prueba comparativa GLM vs DeepSeek — $FECHA_LARGA"
    echo "# Motor actual: deepseek-v4-flash. Candidatos: glm-4.7-flashx, glm-4.7-flash (gratis)"
    echo ""
    echo "## Tarea A — Informe ejecutivo del lab"
    for f in A-deepseek A-flashx A-flash; do
        j="$OUT_DIR/${FECHA}-${f}.json"
        [ -f "$j" ] || continue
        echo ""
        echo "### ${f}"
        python3 -c "
import json,sys
try:
    d=json.load(open('$j'))
    msg=d.get('choices',[{}])[0].get('message',{})
    content=msg.get('content') or msg.get('reasoning_content') or '(sin contenido)'
    u=d.get('usage',{})
    print('CONTENIDO:')
    print(content)
    print()
    print('USAGE: prompt=%s completion=%s total=%s' % (u.get('prompt_tokens','?'), u.get('completion_tokens','?'), u.get('total_tokens','?')))
except Exception as e:
    print('ERROR parseando: %s' % e)
    print(open('$j').read()[:500])
"
    done
    echo ""
    echo "## Tarea B — Razonamiento con restricciones (control)"
    for f in B-deepseek B-flashx B-flash; do
        j="$OUT_DIR/${FECHA}-${f}.json"
        [ -f "$j" ] || continue
        echo ""
        echo "### ${f}"
        python3 -c "
import json,sys
try:
    d=json.load(open('$j'))
    msg=d.get('choices',[{}])[0].get('message',{})
    content=msg.get('content') or msg.get('reasoning_content') or '(sin contenido)'
    u=d.get('usage',{})
    print(content)
    print('USAGE: prompt=%s completion=%s' % (u.get('prompt_tokens','?'), u.get('completion_tokens','?')))
except Exception as e:
    print('ERROR: %s' % e)
"
    done
    echo ""
    echo "## Tiempos (s) y códigos HTTP"
    cat /tmp/prueba_ds_a.txt /tmp/prueba_ds_b.txt 2>/dev/null
    cat /tmp/prueba_zx_a.txt /tmp/prueba_zx_b.txt /tmp/prueba_zf_a.txt /tmp/prueba_zf_b.txt 2>/dev/null
} > "$OUT"

echo "Informe: $OUT"
echo "---"
head -30 "$OUT"
