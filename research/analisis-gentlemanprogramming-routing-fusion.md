---
title: "Análisis — Model Routing vs Model Fusion (Gentleman Programming, 22-ago-2026)"
type: research
---

# Análisis — Model Routing vs Model Fusion (Gentleman Programming, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/zypreQ8hJmI (Gentleman Programming, 20-08-2026, 11:49 min)
**Método:** subtítulos ES descargados (114 KB) + extracción de fragmentos clave

## Contenido: 2 conceptos que mueven la industria

**La idea central**: "pasó de cuál es el mejor modelo a quién decide qué modelo usar en cada momento".

1. **Model Routing** = capa que analiza tu pedido ANTES de mandarlo, lo clasifica y elige el modelo:
   - Tarea simple → modelo rápido y barato ("un refactor rápido de una función, un modelo chico y veloz te sobra")
   - Tarea compleja → modelo de razonamiento ("decisión de arquitectura con trade-offs")
   - Metáfora: "es como un jefe de cocina — no pone al chef para todo"
   - Soluciones: OpenRouter (API que rutea entre cientos de modelos), LiteLLM, etc.

2. **Model Fusion** = combina DESPUÉS: varios modelos (los "4 grandes": GPT, Claude, Gemini, Grok) hacen su propia revisión → cada uno pasa su veredicto → jueces (juez 1, juez 2...) evalúan → resultado consensuado.
   - "para no casarme con la opinión de un solo modelo, con mis propios jueces en la terminal"

**La frase que lo resume**: "El routing elige antes, Fusion combina después. Uno optimiza el costo y el otro optimiza la calidad."

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (VALIDA la arquitectura del lab)

| Concepto | En el lab |
|---|---|
| **Model Routing** | ✅ `llvm-router.sh` (cloud antes 12:00 / local después) + ai-router (enrutamiento cloud-local) — EXACTO |
| **Model Fusion con jueces** | ✅ `llm_as_judge.py` (implementado hoy por el usuario): GLM + gpt-oss como 2 jueces independientes |
| "No casarme con un solo modelo" | ✅ Mismo principio (batería de evaluación + jueces + verificación) |
| OpenRouter como ejemplo | ✅ El lab conoce OpenRouter (pero usa DeepSeek + local, más barato) |

**La validación clave**: el lab ya implementa la respuesta del vídeo:
- **Routing** (elige antes, optimiza costo): llvm-router.sh ✅
- **Fusion** (combina después, optimiza calidad): llm_as_judge con 2 modelos ✅

**Futurible DÉBIL (documentado)**: ampliar el juez a "fusion" real — en vez de solo 2 jueces puntuales, ejecutar 2-3 modelos que respondan y que los jueces voten el mejor (patrón escritor+revisor del vídeo). Señal de activación: cuando se necesite máxima calidad en textos importantes (fichas, informes). El lab ya tiene la base (llm_as_judge) — sería una extensión.

**Conclusión**: vídeo que VALIDA la arquitectura de enrutamiento y evaluación del lab. El lab ya hace routing (coste) + jueces (calidad). Sin cambios necesarios; el futurible de "fusion total" queda anotado como mejora opcional.
