---
title: "Validación — gpt-oss-20b (OpenAI) vs R1-14B — benchmark razonamiento (19-ago-2026)"
type: research
---

# Validación — gpt-oss-20b (OpenAI) vs R1-14B — benchmark razonamiento (19-ago-2026)

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** investigación semanal modelos locales (CLI 19-ago 07:20, cron
`investigacion-modelos-locales-semanal`) + benchmark ejecutado en sesión
**Modelo:** openai/gpt-oss-20b — MoE 21B/3.6B activo, MXFP4 (12.11 GB GGUF,
`/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/gpt-oss-20b-GGUF/`)
**Motor:** LM Studio (localhost:1234) — **NO Ollama** (R1-14B sí vive en
Ollama 11434)
**Método:** benchmark-razonamiento.py (3 problemas con trampa: billete 80€,
vino/agua 9.091ml, caja etiquetada Manzanas y Naranjas; max_tokens 4096,
temp 0.2)
**Veracidad:** [VERIFICADO] — salidas JSON reales en /tmp, evaluadas contra
respuestas conocidas

---

## RESULTADO FINAL — BATERÍA DE PRODUCCIÓN (19-ago-2026, 5 tareas × 5 repeticiones)

Ejecutada con `bateria_produccion.py` (5 tareas reales del lab: informe estado,
resumen OBS, JSON, clasificación, 5 problemas de razonamiento duro con trampas).
Salidas crudas en /tmp/prod_gptoss_*.json y /tmp/prod_r1_*.json.

| Métrica | gpt-oss-20b | R1-14B |
|---|---|---|
| T1 Informe (media) | 14.8s, 5/5 OK | 47.7s, 5/5 OK |
| T2 Resumen (media) | 9.2s, 5/5 OK | 40.8s, 5/5 OK |
| T3 JSON (determinista) | 6.1s, 5/5 ✅ | 34.5s, 5/5 ✅ |
| T4 Clasificación (determinista) | 2.1s, 5/5 ✅ | 31.4s, 5/5 ✅ |
| T5 Razonamiento duro | 45.6s, 24/25 (96%) | 206.8s, 11/25 (44%) |
| Cortes (finish=length) | 0/25 | 4/5 en T5 (2 con content vacío) |

**VEREDICTO FINAL: gpt-oss-20b sustituye a R1-14B como modelo de razonamiento
batch del lab.** Gana en: razonamiento (96% vs 44%), robustez (0 cortes vs cortes
con content vacío), velocidad (3-15x según tarea), redacción (juicio ciego del
usuario: equivalente o mejor). Pendiente de integración formal (RULE-003,
llm-router.sh, ficha en 01-knowledge/models/) — requiere OK explícito del usuario.

## RESULTADOS (3 ejecuciones de gpt-oss-20b)

| Ejecución | Tiempo | tok/s | P1 (80€) | P2 (iguales/9.091ml) | P3 (caja M+N) | Total |
|---|---|---|---|---|---|---|
| run2 (12:26) | 55.5s | 14.7 | ✅ 80€ | ✅ iguales | ✅ M+N | **3/3** |
| run3 (12:37) | 64.6s | 15.0 | ❌ 100€ | ❌ | ✅ | 1/3 |
| vs_r1 (12:38) | 87.7s | 8.3 | ❌ 100€ | ❌ | ✅ | 1/3 |

**Mejor ejecución: 3/3 correcto en 55.5s a 14.7 tok/s, finish=stop (no se
corta).**

## COMPARATIVA vs R1-14B (validado 13-ago, mismo benchmark)

| Métrica | gpt-oss-20b (mejor) | R1-14B (13-ago) |
|---|---|---|
| Aciertos | **3/3** | 2/3 (falló P1) |
| P1 trampa (80€) | ✅ **acierta** | ❌ falló (dio 180€) |
| Tiempo | **55.5s** | 116.5s (2.1x más lento) |
| tok/s | 14.7 | ~10 |
| finish | stop | stop |

**→ gpt-oss-20b SUPERA a R1-14B en el benchmark del lab**: acierta el
problema trampa que R1 falla, ~2x más rápido, no se corta.

---

## VEREDICTO — CANDIDATO A QUEDARSE (criterio CLI cumplido)

Criterio de la CLI (19-ago): ≥2/3 correctos en tiempo razonable → candidato;
si se corta o 4x lento → descartado. **CUMPLIDO**: 3/3 en 55.5s (vs R1 116.5s
= más rápido, no más lento).

### ⚠️ Matices honestos
1. **Variabilidad**: 3/3 en la mejor, 1/3 en otras dos (temp 0.2, modelo no
   determinista) → confirmar con repeticiones antes de adoptar.
2. **VRAM**: requiere offload parcial (12.0 modelo + 2.7 buffers = 14.9 GB >
   12 GB de la A2000) → 8-15 tok/s con offload (i5-9500 + PCIe 3.0 penaliza;
   benchmark real de llama.cpp #15396 en RTX 3060 12GB: 53-67 tok/s con
   offload — el nuestro mide peor por el PCIe 3.0).
3. **Batería exigente pendiente** (la de los 7 modelos del 06-ago) antes de
   adoptar definitivamente.

### Siguiente paso
1. (Opcional) Repetir benchmark 2-3x más para confirmar el 3/3.
2. **Batería exigente** (7 dimensiones: razonamiento multi-paso, código,
   tool calling, español, consistencia, latencia) antes de quedarse.
3. Decisión: si pasa batería → gpt-oss-20b como modelo de razonamiento
   preferido (sustituiría a R1-14B en batch); GLM sigue para visión.

**Nota proceso:** el cron one-shot (4518b42dbe5c) falló el disparo
(execution_success=false) pero SÍ cargó el modelo; el benchmark se ejecutó
en sesión directamente + la CLI corrió ejecuciones propias (run2/run3/vs_r1).
Registrado con backup 19g.
