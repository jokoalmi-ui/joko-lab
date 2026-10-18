---
title: "Análisis: Prompt Tuning vs Prefix Tuning (shiva.bytes)"
type: research
---

# Análisis: Prompt Tuning vs Prefix Tuning (shiva.bytes)
**VERACIDAD:** [VERIFICADO]

- **Fuente**: Instagram @shiva.bytes (Shiva Tech Bytes / Sivasankar Natrajan), reel 11-ago-2026
- **URL**: https://www.instagram.com/reel/Db5szCIDrCj/
- **Tipo**: reel de 7 s + infografía estática (misma pieza, verificada en 7 frames)
- **Método**: caption del reel + imagen local pegada por el usuario (clip_20260811_190105_1.png)
  analizada con GLM 4.6V + vídeo descargado (MP4 306 KB) y 7 frames verificados con GLM
- **Fecha análisis**: 11-ago-2026

## Qué es

Infografía "WHY TRAIN BILLION PARAMETERS WHEN YOU CAN TRAIN JUST A FEW WITH
PREFIX TUNING" (¿por qué entrenar miles de millones de parámetros cuando puedes
entrenar solo unos pocos con prefix tuning?) — dos técnicas PEFT (Parameter
Efficient Fine-Tuning) para adaptar LLMs sin reentrenar todos los pesos.

## Contenido (verificado con GLM en la infografía)

1. **PROMPT TUNING (overview)**: congela los pesos del LLM, solo se entrenan
   "prompts" aprendibles (tokens virtuales). Útil para: few-shot learning,
   tareas simples (clasificación, resumen).
2. **PREFIX TUNING (overview)**: congela los pesos, se entrenan "prefixes"
   (vectores) que se inyectan en CADA capa del transformer. Útil para:
   tareas zero-shot, generación fuerte y control más profundo.
3. **PROMPT TUNING vs PREFIX TUNING** (tabla): mismos tokens de entrada/salida;
   prompt tuning entrena solo prompts (menos parámetros); prefix tuning entrena
   prefixes por capa (más parámetros que prompt, menos que fine-tune completo).
4. **CÓMO FUNCIONA PREFIX TUNING**: Input tokens → prefijo inyectado en capas
   del transformer → Output tokens. El prefijo "guía" cada capa, no solo la entrada.
5. **CUÁNDO USARLO**: memoria limitada, adaptación rápida, reduce riesgo de overfitting.
6. **HIPERPARÁMETROS COMUNES**: número de tokens prompt/prefix, capas donde
   aplicar prefix tuning, learning rate para prompts/prefixes.
7. **BEST PRACTICES**: ajustar número de tokens, capas y learning rate.

## Caption del reel (aporte del autor)

- Experiencia real: "solía hacer full fine-tune. 8 GPUs. 3 días. ~$2k en compute.
  Luego prefix tuning me dio resultados similares en 1 GPU en 4 horas."
- Prompt tuning = aprender QUÉ decirle al modelo (tokens que actúan como
  instrucciones perfectas).
- Prefix tuning = aprender CÓMO dirigir el modelo en cada capa (prefijos pequeños
  que guían la generación, no solo la entrada).
- Regla práctica: prompt tuning para tareas simples (clasificación, resumen);
  prefix tuning cuando necesitas generación fuerte y control más profundo.

## 🎧 AUDIO DEL REEL (transcrito con faster-whisper, 13-ago — NO estaba en el
análisis visual del 11-ago)

> **"Stop burning GPUs for bragging rights. You rarely need a full fine-tune.
> Tiny adapters give you 90% of the value almost free."**

La frase hablada del autor refuerza el mapeo al lab: los adaptadores pequeños
(PEFT/LoRA) dan el 90% del valor "casi gratis" — valida que el lab NO necesita
full fine-tune (inviable en A2000 12GB) y que si algún día adapta un modelo,
la vía es LoRA/adaptadores, no entrenamiento completo. Esto refuerza la
conclusión del 05-ago y del estudio fine-tuning (LoRA futurible post-i9).

## Mapeo al lab

**Conecta directamente con la línea de eficiencia local del lab:**
- El lab opera LM Studio/llama.cpp en una A2000 12 GB: PEFT (prompt/prefix tuning)
  es exactamente la familia de técnicas para adaptar un modelo a una tarea con
  recursos mínimos (vs fine-tune completo inviable en 12 GB).
- Los futuribles de modelos locales (Gemma 26B A4B, Qwen 35B A3B, Meta Muse
  Glimmer 30B) son sobre ELEGIR modelo; este material es sobre ADAPTAR un modelo
  ya elegido sin reentrenarlo.

**Utilidad práctica hoy: NINGUNA acción inmediata.** El lab no fine-tunea modelos;
usa modelos ya entrenados (R1-14B, GLM 4.6V, DeepSeek cloud). La técnica solo
cobraría valor si algún día el lab quiere adaptar un modelo local a una tarea
específica (p.ej. entonar R1-14B para el router) — con 12 GB VRAM, prompt/prefix
tuning es la vía realista (vs LoRA, que también es PEFT pero entrena más pesos).

**Material TFM**: PEFT (prompt/prefix tuning, LoRA, adapters) es un tema central
de eficiencia en LLMs — útil como sección/evidencia para el TFM.

## Veredicto

**VALIDA la dirección + material de referencia (PEFT para 12 GB).** Reel con
componente de experiencia práctica (autor pagó ~$2k en compute por full fine-tune
antes de descubrir prefix tuning). NADA accionable hoy: el lab no adapta modelos.
Guardar como referencia para TFM y para cuando el lab decida adaptar un modelo
local (entonces prompt/prefix/LoRA será la vía, no full fine-tune).
