---
id: lfm2.5-2.6b
name: Liquid LFM 2.5 2.6B
version: "2.5"
quantization: Q4_K_M
engine: LM Studio
added: 2026-08-06
tested: 2026-08-06 (batería de modelos, 7/7)
status: activo
personalidad: Agente ligero
---
# LFM 2.5 2.6b

## Qué es

Modelo de Liquid AI (LiquidAI/LFM2.5-2.6B-GGUF, publicado 04-ago-2026).
2.7B parámetros, solo texto, español+inglés, ventana 128K. Descargado 06-ago
(Q4_K_M, 1.67 GB) en /mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/LFM2.5-2.6B-Q4_K_M/.

## Fortalezas (verificadas 06-ago, batería 7/7 + estudio)

- Tool calling excelente (JSON estricto, formato nativo)
- Razonamiento encubierto (reasoning_content): útil pero consume tokens
- Español correcto
- El MÁS RÁPIDO del lab: 55 tok/s (casi 2× granite, 5× los 14B)
- Cabe en 1.67 GB — VRAM mínima
- 7/7 en batería de 8 dimensiones (razonamiento ×2, código ×2, tool calling, español, consistencia)

## Debilidades

- Código one-shot peor que Gemma 4 E2B / Qwen (estudio del autor)
- Sin MTP → generación ~55-80 tok/s (el estudio decía ~80; medido 55 con razonamiento)
- Razonamiento encubierto puede agotar max_tokens y dejar content vacío
  (requiere max_tokens generoso y leer reasoning_content)
- Sin visión (solo texto)

## Parámetros recomendados

- max_tokens: 2000+ (el razonamiento encubierto consume presupuesto)
- temperature: 0.2-0.7
- Leer `reasoning_content` + `content` concatenados (content puede quedar vacío con finish_reason=length)

## Prompts ideales

- Tool calling / function calling (su especialidad)
- Tareas agénticas ligeras (enrutamiento, agentes, MCP)
- Español conversacional
- Respuestas que requieren velocidad

## Prompts que fallan

- Código one-shot complejo (Media)
- max_tokens < 800 (Fatal: se agota en razonamiento, content vacío)

## Benchmarks

- Batería 06-ago: 7/7 (A1 razonamiento, A2 restricciones, B1 código, B2 corregir, C1 tool calling, D1 español, E1 consistencia) — 55.3 tok/s
- Estudio autor (06-ago): tool calling EXCELENTE (OpenCode+MCP), código ❌, español ✅, ~80 tok/s sin MTP

## Clasificación LPA

- E2 (hipótesis): "Agente ligero" — especializado en tool calling rápido
- Pendiente para E3: uso real en tareas agénticas del lab (3+ condiciones)

## Anti-patrones

- max_tokens bajo → content vacío (Fatal)
- Esperar respuesta sin razonamiento (el modelo razona primero siempre)

## Notas

- Descargado y probado el 06-ago-2026 (batería de modelos, 7/7)
- 5º cerebro candidato: tool calling / tareas agénticas ligeras
- No sustituye a granite (estándar RAG/JSON) ni a gemma-4 (creatividad)

## Conexiones

- [[ai-router]] — ai-router: selección de modelos
