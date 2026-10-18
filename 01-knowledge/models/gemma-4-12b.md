---
id: gemma-4-12b-qat
name: Gemma 4 12B QAT
version: "4"
quantization: QAT
engine: LM Studio
added: 2026-07-26
status: activo
personalidad: Director Creativo
---
# Gemma 4 12b



## Fortalezas
- Razonamiento profundo y explicaciones detalladas
- Creatividad excelente (mejor relato del laboratorio)
- Codigo con 2 versiones (pandas + stdlib)
- JSON valido

## Debilidades
- El mas lento del laboratorio (151s para creatividad)
- max_tokens < 400 → se come el presupuesto en reasoning
- Lento pero fiable

## Parametros recomendados
- max_tokens: 2048 (minimo)
- temperature: 0.7 (creatividad), 0.2 (codigo)
- context_length: maximo disponible

## Prompts ideales
- Tareas complejas multi-paso
- Codigo con alternativas (pandas + stdlib)
- Creatividad literaria

## Prompts que fallan
- max_tokens < 400
- Preguntas que requieren respuesta inmediata (es lento)

## Benchmarks
- EXP-20260726-001: 5/5 tests, 35-151s por tarea
- Pendiente de E3: solo 1 condicion (temp=0.7). Ver nota abajo.

## Clasificacion LPA
- E2 (hipotesis): "Director Creativo"
- Pendiente para E3 (requiere 3+ condiciones distintas):
  * Repetir tests con temperature=0.2 (codigo) y temperature=0.5 (creatividad)
  * Probar con max_tokens=2048 vs 4096
  * Evaluar con tareas de razonamiento puro (sin componente creativo)

## Anti-patrones
- max_tokens < 400 → content vacio (Fatal)
- Esperar respuesta rapida (Baja - es lento por diseno)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
