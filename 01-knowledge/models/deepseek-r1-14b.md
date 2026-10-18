---
id: deepseek-r1-distill-qwen-14b
name: DeepSeek R1 Distill Qwen 14B
version: "1.0"
quantization: Q4_K_M (unsloth)
engine: LM Studio
added: 2026-07-26
status: activo
personalidad: Pensador del laboratorio
---
# Deepseek r1 14b



## Fortalezas
- Razonamiento paso a paso estructurado
- JSON impecable y estructurado
- Codigo completo con type hints
- Consistente en todas las tareas (5/5)

## Debilidades
- Lento (106s para codigo completo)
- Consume todo el presupuesto de tokens si max_tokens < 2048
- Temperatura alta (>0.8) degrada la calidad

## Parametros recomendados
- max_tokens: 2048 (minimo para trabajo real)
- temperature: 0.2-0.5
- top_p: 0.9

## Prompts ideales
- Razonamiento paso a paso con estructura explicita
- JSON estructurado
- Codigo Python con type hints

## Prompts que fallan
- Prompts con max_tokens < 1024 (se come el presupuesto en reasoning)
- Temperatura > 0.8 para tareas tecnicas

## Benchmarks
- EXP-20260726-001: 5/5 tests, 21-106s por tarea
- Pendiente de E3: solo 1 condicion (temp=0.7). Ver nota abajo.

## Clasificacion LPA
- E2 (hipotesis): "Pensador del laboratorio"
- Pendiente para E3 (requiere 3+ condiciones distintas):
  * Repetir tests con temperature=0.3 (codigo) y temperature=0.5 (creatividad)
  * Probar con max_tokens=2048 vs 4096
  * Probar con tipos de tarea adicionales (extraccion, clasificacion)

## Anti-patrones
- max_tokens < 2048 → content vacio (Fatal)
- temperatura alta en tareas tecnicas (Alta)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
