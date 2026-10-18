---
id: glm-4.6v-flash
name: GLM 4.6V Flash
version: "4.6V"
quantization: FP16
engine: LM Studio
added: 2026-07-26
status: activo
personalidad: Atomico
---
# Glm 4.6v flash



## Fortalezas
- Excelente con prompts atomicos (1 instruccion)
- JSON valido y rapido
- Creatividad OK con tokens suficientes

## Debilidades
- Prompt con mas de 3-4 lineas → content vacio
- Codigo no es su especialidad (finish=length)
- No tolera instrucciones multiples

## Parametros recomendados
- max_tokens: 2048
- temperature: 0.1-0.3
- Una unica instruccion por prompt

## Prompts ideales
- Una sola pregunta concreta
- JSON estructurado
- Clasificacion o extraccion simple

## Prompts que fallan
- Multiples instrucciones en un solo prompt (Fatal)
- Razonamiento largo y complejo (Alta)
- Codigo extenso (Media)

## Benchmarks
- EXP-20260726-001: 4/5 tests, 21-80s por tarea
- E2: Funciona con prompts atomicos y max_tokens alto

## Anti-patrones
- Prompt multi-instruccion → content vacio (Fatal)
- max_tokens < 2048 → finish=length (Alta)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
