---
id: qwen-3.5-9b
name: Qwen 3.5 9B
version: "3.5"
quantization: Q4_K_M
engine: LM Studio
added: 2026-07-26
status: descartado
personalidad: DESCARTADO
razon_descarte: "0/5 tests utiles. Reasoning model que consume todo el presupuesto de tokens."
---
# Qwen 3.5 9b



## Fortalezas
- Ninguna identificada en el laboratorio

## Debilidades
- Content vacio en 3/5 tests
- finish=length en los 2 restantes
- 0/5 tests utiles

## Parametros recomendados
- NO USAR. No se ha encontrado configuracion que funcione.

## Prompts que fallan
- TODOS. Cualquier tarea no trivial → content vacio o finish=length

## Benchmarks
- EXP-20260726-001: 0/5 tests
- E3 validado: Descartado del laboratorio

## Anti-patrones
- Usar Qwen 3.5 9B para cualquier tarea (Fatal)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
