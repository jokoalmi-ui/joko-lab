---
id: qwen3-14b
name: Qwen3 14B
version: "3"
quantization: Q4_K_M
engine: LM Studio
added: 2026-07-26
status: retirado
personalidad: Mixto
superseded_by: deepseek-r1-distill-qwen-14b
retired: '2026-08-06'
motivo_retirada: "Bateria modelos 06-ago: 7/7 pero 12 tok/s (lento); ficha: Monty Hall fallo completo, 3/5 tests. deepseek-r1-14b lo supera en razonamiento (5/5). Sin RULE que lo seleccione. GGUF eliminado del disco."
---
# Qwen3 14b



## Fortalezas
- Funciona bien con prompts simples y JSON
- Creatividad decente
- Razonamiento basico funcional con tokens suficientes

## Debilidades
- Es reasoning model oculto: necesita max_tokens >= 2048
- Monty Hall (T2) fallo completamente incluso con tokens altos
- Codigo completo se trunca (finish=length)
- Resultados mixtos: 3/5 tests

## Parametros recomendados
- max_tokens: 2048 (minimo para tareas no triviales)
- temperature: 0.3-0.7
- Evitar tareas que requieran razonamiento multivariable

## Prompts ideales
- JSON estructurado
- Preguntas directas y simples
- Tareas de creatividad ligera

## Prompts que fallan
- Razonamiento complejo (Monty Hall) (Alta)
- Codigo extenso (Media)
- max_tokens < 1024 (Fatal)

## Benchmarks
- EXP-20260726-001: 3/5 tests
- E2: Mixto - fiable para cosas simples, falla en complejidad

## Anti-patrones
- max_tokens < 1024 → content vacio (Fatal)
- Tareas que requieren razonamiento multivariable (Alta)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
