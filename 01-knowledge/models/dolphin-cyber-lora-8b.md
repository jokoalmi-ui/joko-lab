---
id: dolphin-cyber-lora-8b
name: Dolphin Cyber LoRA 8B
version: "2.8"
quantization: LoRA
engine: LM Studio
added: 2026-07-26
status: activo
personalidad: Charlatan directo
---
# Dolphin cyber lora 8b



## Fortalezas
- Rapidisimo (3-10s por tarea)
- Responde en texto directo, no function calls
- Razonamiento correcto sin formato estructurado
- JSON valido aunque prefiere texto
- Codigo funcional para tareas ligeras

## Debilidades
- JSON no es su fuerte (prefiere texto)
- No apto para tareas que requieren tool-use nativo
- Codigo solo para tareas ligeras

## Parametros recomendados
- max_tokens: 1024 (suficiente, es rapido)
- temperature: 0.7
- Formato conversacional, no estructurado

## Prompts ideales
- Chat directo y conversacional
- Preguntas de conocimiento general
- Tareas simples de codigo
- Creatividad rapida

## Prompts que fallan
- JSON como instruccion principal (Alta - responde texto)
- Function calling o tool-use (no entrenado para ello)

## Benchmarks
- EXP-20260726-001: 5/5 tests, 3-36s por tarea
- E1: Charlatan versatil, el mas rapido del laboratorio

## Anti-patrones
- JSON como instruccion principal → texto en lugar de JSON (Alta)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
