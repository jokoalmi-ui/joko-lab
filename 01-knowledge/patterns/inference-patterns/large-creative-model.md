---
type: knowledge
subtype: pattern
status: active
tags: [knowledge, pattern]
created: 2026-07-28
---
# Pattern: Large Creative Model
==================================

## Proposito

Modelos grandes (>10B parametros) optimizados para tareas que
requieren creatividad, razonamiento profundo y generacion de
contenido estructurado. Sacrifican velocidad por calidad.

## Entrada esperada

  - Tareas con objetivos abiertos o semi-abiertos
  - Problemas que requieren multiples enfoques
  - Generacion de contenido con estructura narrativa
  - Codigo completo con alternativas de implementacion

## Salida esperada

  - Texto creativo de alta calidad
  - Codigo completo con 2+ versiones (ej: pandas + stdlib)
  - Explicaciones detalladas y razonadas
  - JSON estructurado correctamente

## Riesgos conocidos

  - Lentitud: hasta 2-3 minutos por respuesta completa
  - max_tokens < 2048: content vacio o finish=length
  - Temperatura > 0.8: degradacion del razonamiento
  - Prompt multi-instruccion: confusion y perdida de contexto
  - Semilla no fijada: resultados no reproducibles entre ejecuciones

## Mitigaciones

  - max_tokens siempre >= 2048 (400 como minimo absoluto)
  - Temperature: 0.2-0.3 para codigo, 0.5-0.7 para creatividad
  - Prompts atomicos si el modelo es GLM
  - Fijar seed cuando se requiera reproducibilidad exacta

## Modelos compatibles (verificado en Joko Lab)

  | Modelo | Creatividad | Codigo | Velocidad | Tokens/s |
  |---|---|---|---|---|
  | Gemma 4 12B | Excelente | Excelente (2 versiones) | Lento (151s) | ~15 |
  | DeepSeek R1 14B | Buena | Completo (type hints) | Lento (106s) | ~20 |
  | GLM 4.6V Flash | Buena | Limitado | Medio (80s) | ~30 |

## Experimentos de validacion

  - EXP-20260726-001: Tests T4 (codigo) y T5 (creatividad)
  - Resultados: Gemma 4 5/5, DeepSeek R1 5/5, GLM 4.6V 4/5

## Ejemplo de uso

  Objetivo: Escribir una funcion que lea CSV y filtre por edad
  Modelo recomendado: Gemma 4 12B
  Config: max_tokens=2048, temperature=0.2, seed=42
  Resultado: 2 versiones (pandas + stdlib), ambas funcionales

## Referencias

  - ~/joko-lab/01-knowledge/models/gemma-4-12b.md
  - ~/joko-lab/01-knowledge/models/deepseek-r1-14b.md
  - ~/joko-lab/01-knowledge/experiments/EXP-20260726-001/
  - ~/joko-lab/01-knowledge/patterns/anti-patterns/catalogo.md
