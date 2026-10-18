---
type: EXP
subtype: experiment
status: index
tags: [knowledge, experiment]
created: 2026-07-28
---
# EXP-20260726-001: Comparativa de 7 modelos
==============================================

Fecha: 2026-07-26
Autor: jokoalmi
Estado: COMPLETADO
Tipo: Benchmark comparativo

## Objetivo

Evaluar el rendimiento de 7 modelos locales en 5 tareas
estandarizadas para determinar fortalezas, debilidades y
anti-patrones de cada uno.

## Condiciones

- GPU: RTX A2000 12GB
- Engine: LM Studio
- Temperature: 0.7
- top_p: 0.9
- Modelos cargados uno a uno (no concurrente)

## Modelos evaluados

1. dolphin-cyber-lora-8b
2. llama-3.1-instruct-8b
3. deepseek-r1-distill-qwen-14b
4. qwen3.5-9b
5. qwen3-14b
6. glm-4.6v-flash
7. gemma-4-12b-qat

## Tests

| ID | Tipo | Descripcion | max_tokens |
|---|---|---|---|
| T1 | Conocimiento | Explica inyeccion SQL | 1024 |
| T2 | Razonamiento | Problema Monty Hall | 1024 |
| T3 | JSON | 3 recetas de verano en JSON | 1024 |
| T4 | Codigo | Funcion Python filtrar CSV | 1024 |
| T5 | Creatividad | Microrrelato asistente IA | 1024 |

## Resultados agregados

| Modelo | T1 | T2 | T3 | T4 | T5 | Puntuacion |
|---|---|---|---|---|---|---|
| dolphin-cyber-lora-8b | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| llama-3.1-instruct-8b | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| deepseek-r1-distill-qwen-14b | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| gemma-4-12b-qat | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| glm-4.6v-flash | ✅ | ✅ | ✅ | ⚠️ | ✅ | 4/5 |
| qwen3-14b | ✅ | ❌ | ✅ | ⚠️ | ✅ | 3/5 |
| qwen3.5-9b | ⚠️ | ❌ | ❌ | ⚠️ | ❌ | 0/5 |

## Conclusiones

### E3 validados (3)
1. DeepSeek R1 = Pensador del laboratorio
2. Gemma 4 = Director Creativo
3. Qwen 3.5 9B = Descartado

### E2 hipotesis (5)
1. Dolphin responde en texto, no function calls
2. Llama 3.1 Instruct entrenado para tool-use
3. GLM funciona con prompts atomicos y max_tokens alto
4. Qwen3 14B es reasoning model oculto
5. Gemma 4 necesita max_tokens >= 2048

### E1 observaciones (27)
Ver archivo de datos completo en results.csv

## Impacto en el laboratorio

- Se creo la skill prompt-engineering con los hallazgos
- Qwen 3.5 9B eliminado del catalogo activo
- DeepSeek R1 designado como modelo principal para razonamiento
- Gemma 4 designado para tareas creativas y codigo complejo
- Se identifico max_tokens como parametro critico en reasoning models

## Archivos asociados

- config.yaml: parametros exactos del experimento
- results.csv: datos crudos de los 35 tests
