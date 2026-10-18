---
type: knowledge
subtype: pattern
status: active
tags: [knowledge, pattern]
created: 2026-07-28
---
# Pattern: Atomic Prompt para GLM
====================================

## Proposito

Los modelos GLM (especialmente GLM 4.6V Flash) fallan cuando
reciben multiples instrucciones en un mismo prompt. Este patron
describe como dividir tareas complejas en prompts atomicos.

## Entrada esperada

  - Tareas que requieren multiples pasos
  - Preguntas con varias partes
  - Instrucciones compuestas

## Salida esperada

  - N prompts independientes, uno por instruccion
  - Cada prompt con max_tokens >= 2048
  - Resultados individuales que se combinan al final

## Riesgos conocidos

  - Prompt con 3+ instrucciones → content vacio (FATAL)
  - max_tokens < 2048 → finish=length

## Mitigaciones

  - Una sola instruccion por prompt
  - Dividir manualmente antes de enviar
  - max_tokens siempre >= 2048

## Modelos compatibles

  | Modelo | Afectado | Gravedad |
  |---|---|---|
  | GLM 4.6V Flash | Si | FATAL |
  | Otros modelos | No | — |

## Experimentos de validacion

  - EXP-20260726-001: Tests T1-T5 con GLM
  - Sesion vision: prompt con 7 preguntas → vacio; 7 prompts OK

## Ejemplo

  Mal:
    "Analiza esta imagen. Donde esta la fuente de luz?
    Que colores predominan? Que texturas se aprecian?
    Esta sobreexpuesta?"

  Bien:
    Prompt 1: "Analiza esta imagen. Donde esta la fuente de luz?"
    Prompt 2: "Analiza esta imagen. Que colores predominan?"
    Prompt 3: "Analiza esta imagen. Que texturas se aprecian?"
    Prompt 4: "Analiza esta imagen. Esta sobreexpuesta?"
