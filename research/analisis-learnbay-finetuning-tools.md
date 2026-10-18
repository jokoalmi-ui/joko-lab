---
title: "Análisis — Herramientas open source de fine-tuning (Learnbay, 21-ago-2026)"
type: research
---

# Análisis — Herramientas open source de fine-tuning (Learnbay, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcLmWD1GlNQ/ (learnbayofficial, 18-08-2026, 52 likes)
**Método:** caption íntegro extraído (browser_console, sin imágenes — el caption ya lista todo)

## Contenido
Mapa de herramientas open source para fine-tuning de LLMs SIN rentar GPU cluster:

| Herramienta | Enfoque |
|---|---|
| **Unsloth** | Reduce VRAM y tiempo de entrenamiento (lo más relevante para GPUs modestas) |
| **LLaMA-Factory** | CLI + web, control entre familias de modelos |
| **PEFT** | Adaptación eficiente (LoRA, adapters) |
| **DeepSpeed** | Entrenamiento distribuido |
| **TRL** | Post-training y RLHF |
| **Axolotl, Torchtune, LitGPT, ms-swift, AutoTrain** | Distintas necesidades de entrenamiento |

Frase clave: *"La habilidad real no es conocer todas las librerías, sino saber cuál resuelve tu cuello de botella."*

## 🔴 Para el LAB — VALOR: BAJO (referencia, no accionable hoy)

| Aspecto | Análisis |
|---|---|
| ¿El lab hace fine-tuning? | ❌ NO — usa modelos listos (LFM, gpt-oss, GLM, Gemma) con prompts/skills |
| ¿Puede el lab fine-tunear? | ⚪ Técnicamente SÍ (12 GB VRAM + Unsloth podría entrenar LoRA de un modelo pequeño como LFM 2.6B), pero sin necesidad actual |
| Señal de activación | ⚠️ Cuando los prompts dejen de bastar (p.ej. formato de salida muy específico, dominio cerrado) — entonces Unsloth + LoRA de LFM es la vía local viable |

**Sin futuribles nuevos.** Referencia útil para el TFM/LinkedIn (vocabulario: PEFT, LoRA, Unsloth), pero el lab no entrena modelos hoy y la señal no está activa. El coste de mantener un pipeline de entrenamiento local (tiempo, datos, GPU) NO se justifica con la batería PRODUCCIÓN actual funcionando.
