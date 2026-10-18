---
title: "Análisis: Qwen 3.6 35B A3B, el modelo MoE más rápido y eficiente (Nichonauta)"
type: research
---

# Análisis: Qwen 3.6 35B A3B MoE (Nichonauta)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/L5CCF3IPcoY · Nichonauta (@nichonauta) · 06-sep-2026
**Vídeo**: 6:17 min · 1.176 views · Transcripción real (subs es-orig, dedup → 6.326 chars, análisis completo)
**ID**: L5CCF3IPcoY · **Estado**: [VERIFICADO] con transcripción íntegra

## Qué prueba el vídeo

Prueba práctica del **Qwen 3.6 35B A3B** (MoE, ~3B activos) en RTX 3060 **12 GB**
(misma clase que la A2000 12 GB del lab). Contexto del autor:
- Qwen 3.7 **no** está en pesos abiertos
- Qwen 3.8 es el modelo **27B denso** (27B activos): más memoria (KV cache +
  ventana larga), más lento, razonamiento largo (minutos/horas) → no apto para
  GPU de 12 GB

Configuración: llama.cpp, cuantización **MXFP4** + visión (MBF16/MBP16),
11 GB VRAM consumidos (resto en CPU/RAM).

## Resultados (pruebas en vivo, mismos prompts de la serie)

| Prueba | Resultado |
|---|---|
| Landing page (21.000 tokens, 8 min, **43,75 tok/s**) | "De las mejores respuestas que he visto" — sigue instrucciones, sin especificar dependencias |
| Calculadora HTML/CSS/JS | ✅ Funcional (suma, resta, mult, div, limpiar, historial) — solo crítica de diseño menor |
| Reloj analógico | ✅ "De las mejores, por no decir la mejor" — modo claro/oscuro |
| Simulador de fluidos (9.500 tokens, 3 min, **48 tok/s**) | ✅ Físicas OK, parámetros ajustables |

## Veredicto del autor (textual)

- Modelo **eficiente, inteligente, ejecutable en casi cualquier hardware con o
  sin GPU** (con GPU acelera la generación)
- Muchísimo más rápido y en hardware más modesto que el Qwen 3.8 27B (denso,
  KV cache grande, razonamiento lento)
- Mejor opción que el 27B cuando no hay GPU donde quepa entero o se quiere
  velocidad con 3B activos
- Sigue siendo uno de los mejores modelos "pequeñitos" en llama.cpp

## Filtro de valor para el lab (regla 20-ago)

**ALTO — candidato real a evaluar.** La GPU del lab (A2000 12 GB) es de la
misma clase que la del vídeo (RTX 3060 12 GB): un MoE de ~3B activos que carga
con visión en ~11 GB VRAM encaja en el punto dulce del lab (razonamiento
local con cuantización consciente de VRAM). Conexión directa con la batería de
evaluación del lab (evaluar-alucinaciones / mapa-capacidades: Evaluación de
modelos = batería propia, no benchmarks).

Futurible (anotar): **probar Qwen 3.6 35B A3B (MXFP4) en la A2000 del lab**
con la batería de evaluación — ver si supera a los modelos de razonamiento
actuales (gpt-oss-20b, r1-14b) a igual VRAM.

Conecta con: `analisis-nichonauta-qwen35-9b.md`, `analisis-nichonauta-qwen27b-cuantizado.md`
(serie del canal en 12 GB), mapa-capacidades (Evaluación modelos).
