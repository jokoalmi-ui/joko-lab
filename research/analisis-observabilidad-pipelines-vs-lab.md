---
title: "Análisis — Observabilidad de pipelines LLM vs lab (23-ago-2026)"
type: research
---

# Análisis — Observabilidad de pipelines LLM vs lab (23-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

**Origen:** búsqueda invertida por tema "observabilidad de pipelines" (el lab ya tiene proxy :9911 + pipeline_obs)
**Fuentes:** artículos de Confident AI (3 campos de herramientas), MLflow (judge scores como span attributes), Langfuse (tracing open source), Braintrust (SDK + gateway). Sin vídeo destacado — el tema está dominado por herramientas, no por vídeos.

## El estado del arte (lo que ofrecen las herramientas estándar)

| Herramienta | Qué aporta | Modelo |
|---|---|---|
| **Langfuse** | Tracing open source: prompt exacto, respuesta, tokens, latencia, tools/retrieval en el medio | Self-hosted (Docker) |
| **MLflow** | Judge scores escritos como span attributes → correlacionan con trazas | Plataforma |
| **Braintrust** | SDK + Gateway: TTFT, latencia total, tokens/s, coste $; free tier 1 GB | SaaS/SDK |
| **Datadog/New Relic** | Tabs LLM sobre APM tradicional | SaaS |

Los 3 campos del mercado: APM tradicional + tracing AI-native (Langfuse/LangSmith) + evals.

## Qué ya mide el lab (verificado en pipeline_obs.jsonl, 19.337 entradas)

```
CAMPOS: timestamp, path, model, provider, stream, ttfb_ms, total_ms,
        status, prompt_tokens, completion_tokens, error
```

| Métrica | Lab (:9911) | Langfuse | Braintrust |
|---|---|---|---|
| TTFT (time-to-first-token) | ✅ ttfb_ms | ✅ | ✅ |
| Latencia total | ✅ total_ms | ✅ | ✅ |
| Tokens (prompt/completion) | ✅ | ✅ | ✅ |
| Modelo/proveedor | ✅ | ✅ | ✅ |
| Coste € | ❌ (no calculado) | ⚪ (con pricing) | ✅ |
| Trace con prompt exacto | ❌ (solo métricas) | ✅ | ✅ |
| Judge scores correlacionados | ⚪ (llm_as_judge separado) | ✅ | ✅ |
| UI/dashboard | ❌ (jsonl plano) | ✅ | ✅ |

## Veredicto honesto: VALOR MEDIO — el lab cubre el 80% con 2 gaps claros

### Lo que el lab YA tiene (validación)
- **19.337 entradas reales** de telemetría — el lab registra TODO desde hace semanas
- Métricas clave (TTFT, latencia, tokens, modelo) — lo esencial para el coste (de hecho alimentó el análisis del -32.1% de pruning)
- **0 coste y 0 dependencias**: jsonl plano local

### Los 2 gaps reales (si algún día importan)
1. **Sin coste € por llamada**: con DeepSeek (99% del coste es prompt) calcular `prompt_tokens × tarifa` por entrada sería trivial de añadir — pero el lab no paga nada tras las 12:00 (local), así que el coste solo importa para la parte cloud.
2. **Sin trazas del prompt exacto**: Langfuse guarda el prompt/respuesta para depurar; el lab solo guarda métricas. Para depurar una respuesta mala, hoy no puedes ver QUÉ se envió. ⚠️ PERO: guardar prompts completos = volumen grande + datos personales en disco — el diseño actual (métricas + RAG para recuperar contexto) es una elección deliberada de privacidad.

### Langfuse como opción futura
- Es self-hosted (Docker) → encaja con local-first
- Añadiría: UI web, trazas completas, judge scores integrados
- Coste: ~1 contenedor + almacenamiento de trazas
- **Señal de activación**: cuando el lab necesite DEPURAR respuestas concretas con regularidad (hoy: el gate de veracidad + revisor ya cubren la calidad; la depuración es rara)

## Conclusión

**El lab tiene observabilidad de nivel industria en métricas, sin UI ni trazas.** Para el uso actual (local-first, coste 0, gate de veracidad) es suficiente. Langfuse es el futurible si aparece la necesidad de depurar con trazas. Sin acción.

**Dato reutilizable**: el campo `prompt_tokens` ya permite calcular coste € si algún día se quiere (tarifa DeepSeek conocida). Anotado como referencia.
