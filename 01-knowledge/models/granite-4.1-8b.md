---
id: granite-4.1-8b
name: Granite 4.1 8B (IBM)
version: "4.1"
quantization: Q4_K_S (unsloth)
engine: LM Studio
added: 2026-07-27
tested: 2026-07-28 (ciclo manual EXP-20260728-002)
status: activo
personalidad: Tool-use con formato limpio
---
# Granite 4.1 8b



## Fortalezas
- Codigo solido: type hints, docstring, ejemplo de uso
- Razonamiento paso a paso correcto (Monty Hall)
- Explicaciones estructuradas con markdown
- Rapido (5-15s por respuesta)
- Similar a Llama 3.1 Instruct en tool-use, pero con mejor formato

## Debilidades
- JSON valido pero envuelto en bloques de codigo markdown
  (requiere post-procesado para extraer JSON puro)
- Creatividad correcta pero menos elaborada que Gemma 4
- Solo 1 variante probada (unsloth Q4_K_S)

## Parametros recomendados
- max_tokens: 1024 (suficiente para respuestas concisas)
- temperature: 0.3-0.7 (0.3 para codigo, 0.7 para creatividad)
- Formato: tool-use nativo. Esperar markdown en la salida.

## Prompts ideales
- Codigo Python con type hints
- Explicaciones tecnicas estructuradas
- Razonamiento paso a paso
- Tareas que requieren formato claro

## Prompts que fallan
- JSON puro sin markdown (Alta - siempre envuelve en ```json)
- Tareas de creatividad muy abiertas (Media - funcional pero soso)

## Benchmarks
- EXP-20260728-002: 4/5 tests (4 OK, 1 WARNING)
- Pendiente de incluir en comparativa completa (EXP-20260726-001)

## Anti-patrones
- JSON sin markdown envolvente → devuelve ```json (Alta)
- Prompt excesivamente largo → respuestas truncadas (Media, no verificado)

## Notas
- Descargado el 2026-07-27
- Primer ciclo manual completo el 2026-07-28
- Modelo recomendado para tareas de codigo y tool-use
- No recomendado para JSON raw sin post-procesado

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
