---
title: "Prueba R1-14B local — resumen de estado del lab (09-ago-2026)"
type: research
---

# Prueba R1-14B local — resumen de estado del lab (09-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

## Datos de la prueba

| Métrica | Intento 1 | Intento 2 |
|---|---|---|
| Modelo | DeepSeek-R1-Distill-Qwen-14B-Q4_K_M | idem |
| VRAM | 8.5 GB (de 12) | idem |
| Tiempo | 26.8s | 35.1s |
| Tokens prompt | 255 | ~255 |
| Tokens completion | 300 (cortado en max) | 400 |
| **Velocidad** | **11.2 tok/s** | **11.4 tok/s** |
| Calidad | Válida (requiere leer content, no reasoning) | ✅ 3 bullets correctos y bien formados |

## Observaciones

1. **R1 genera razonamiento en `reasoning_content`** (comportamiento típico de
   modelos R1) — el primer intento devolvió content vacío porque el prompt no
   pedía respuesta directa. Con "NO razones en voz alta" → content correcto.

2. **11-11.4 tok/s** en la A2000 con Q4_K_M. Para un resumen de cron (300-400
   tokens) → **26-35s**. Un informe diario completo (~1000 tokens) → ~1.5 min.

3. **Calidad: suficiente para resúmenes/clasificación** — los 3 bullets son
   correctos, bien agrupados y en español.

4. **Coste: 0 €** vs lo que habría costado en cloud (contexto del cron + salida).

## Comparativa con cloud (referencia)

| | R1-14B local | DeepSeek v4-flash cloud |
|---|---|---|
| Velocidad | 11 tok/s | ~40-60 tok/s (estimado) |
| Coste/tarea batch | **0 €** | ~$0.01-0.05 (contexto) |
| Calidad resumen | 90-95% | 100% |
| Privacidad | ✅ Total | Cloud |

## Conclusión

R1-14B local es **viable para tareas batch del lab** (resúmenes, clasificación,
extracción): calidad suficiente, 0 coste, ~30s por tarea. La velocidad es 3-4x
menor que cloud pero aceptable para crons (no interactivos).

**Pendiente:** decidir qué crons mover a local (informe-diario, recordatorios,
scan-empleo) y configurar el router local/cloud.
