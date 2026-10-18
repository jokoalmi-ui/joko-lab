---
id: openai-gpt-oss-20b
name: OpenAI gpt-oss-20b (MXFP4)
version: "1.0"
quantization: MXFP4 nativo (MoE 21B total / 3.6B activo)
engine: LM Studio
added: 2026-08-19
status: activo
personalidad: Razonador rápido del laboratorio
---
# OpenAI gpt-oss-20b

Modelo MoE de razonamiento (21B totales / 3.6B activos), MXFP4 nativo.
GGUF 12.11 GB. **VALIDADO 19-ago-2026 como sustituto de R1-14B** en razonamiento
batch (RULE-003). Batería de producción 5 tareas × 5 reps vs R1-14B:
24/25 (96%) vs 11/25 (44%) en razonamiento duro, 0 cortes vs 4/5 cortes,
3-15x más rápido según tarea. Juicio ciego del usuario: redacción equivalente o mejor.

## Fortalezas
- Razonamiento duro con trampas: 96% aciertos (vs 44% de R1-14B)
- Nunca se corta (0/25 finish=length; R1 se cortaba 4/5 con content vacío)
- Rápido: 13.7-16.4 tok/s reales en A2000 (i5-9500, PCIe 3.0)
- T1 informe 14.8s vs 47.7s · T4 clasificación 2.1s vs 31.4s (15x)
- JSON, tool calling, español, consistencia: 5/5 en batería exigente
- Acierta la trampa del billete falso (80€) que R1 falla siempre (180€)

## Debilidades
- Offload parcial OBLIGATORIO: 12.0 GB modelo + 2.7 GB buffers > 12 GB VRAM
- NO carga junto con GLM-4.6V (compiten por VRAM: 11.28 vs 7.41 GiB)
- Razonamiento encubierto: LM Studio lo expone en message.reasoning (no
  reasoning_content); con max_tokens < 2048 → content vacío + finish=length
- PCIe 3.0 penaliza: 13-16 tok/s vs 53-67 del benchmark llama.cpp en RTX 3060
- Variabilidad puntual: en la batería falló P1 una vez (dio 150€)

## Parametros recomendados
- max_tokens: 2048+ (minimo para razonamiento real)
- temperature: 0.2-0.3 (0.3 en router)
- presupuesto batch router: 400-800 (subir a 1200+ para informes de usuario)

## Prompts ideales
- Razonamiento paso a paso con respuesta verificable
- Informes ejecutivos del estado del lab
- JSON estructurado, clasificación, resumen de observaciones

## Prompts que fallan
- max_tokens < 2048 en tareas de razonamiento (content vacío)
- Peticiones que exigen NO razonar en voz alta (razona igual, como R1)

## Benchmarks
- EXP-20260819-001: benchmark trampas 4 ejecuciones 12/12 (100%), 49.6s media
- EXP-20260819-002: batería exigente 7/7 (ver research/validacion-gpt-oss-bateria-exigente.md)
- EXP-20260819-003: batería producción 5x5 — T5 24/25, 0 cortes (ver
  research/validacion-gpt-oss-20b.md)

## Clasificacion LPA
- E3 (validado): modelo de razonamiento batch del lab (RULE-003)
- Sustituye a: deepseek-r1-distill-qwen-14b (retirado del rol batch)

## Anti-patrones
- max_tokens < 2048 → content vacio (Fatal)
- Esperar que cargue junto con GLM-4.6V (no cabe en 12GB)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
- [[RULE-003]] — modelo de razonamiento del lab
- [[lm-studio]] — motor de inferencia local
