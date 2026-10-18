---
id: llama-3.1-instruct-8b
name: Llama 3.1 Instruct 8B
version: "3.1"
quantization: Q4_K_M
engine: LM Studio
added: 2026-07-26
status: retirado
personalidad: Tool-call nativo rígido
superseded_by: granite-4.1-8b
retired: '2026-08-06'
motivo_retirada: "Bateria modelos 06-ago: 4/7 (peor del lab), responde en formato tool-call nativo incluso a preguntas de razonamiento. granite-4.1-8b lo supera en la misma clase (7/7). GGUF eliminado del disco."
---
# Llama 3.1 instruct 8b



## Fortalezas
- Rapido (2-5s por tarea)
- Function calling nativo entrenado
- Responde con tool calls estructurados siempre
- Incluso creatividad la entrega como function call
- Codigo funcional con pandas

## Debilidades
- NO responde en texto directo. Siempre usa function calls.
- No sirve como chat directo normal
- Hay que tratarlo como backend de agente, no como asistente

## Parametros recomendados
- max_tokens: 1024
- temperature: 0.3
- Usar via function calling, no como chat

## Prompts ideales
- Backend de agentes con tool-use
- Tareas tecnicas (codigo, JSON)
- API calls estructuradas

## Prompts que fallan
- Preguntas abiertas tipo chat (Alta - responde con function calls)
- Esperar texto plano como respuesta (Alta)

## Benchmarks
- EXP-20260726-001: 5/5 tests, 2-5s por tarea
- E2: Agente tool-use nativo. No es chat.

## Anti-patrones
- Esperar texto de Llama 3.1 Instruct → function calls (Fatal)
- Usarlo como chat directo (Alta)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
