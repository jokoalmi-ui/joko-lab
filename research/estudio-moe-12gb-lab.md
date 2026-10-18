---
title: "Estudio — ¿Puede Gemma 26B A4B (y MoE grandes similares) funcionar en el LAB?"
type: research
---

# Estudio — ¿Puede Gemma 26B A4B (y MoE grandes similares) funcionar en el LAB?
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 10-ago-2026
**Motivación:** Tras el vídeo de Nichonauta (Gemma 26B A4B a 43 tok/s en RTX 3060 12 GB),
estudiar si es viable en el lab (RTX A2000 12 GB) y qué otros MoE grandes funcionan.

---

## 1. ¿Es viable Gemma 26B A4B en el LAB?

### Datos técnicos (verificados)

| Dato | Valor |
|---|---|
| Arquitectura | MoE: 128 expertos, 8-9 activos por token (~3.8B activos de 26B totales) |
| Tamaño GGUF Q4_XL | ~14.3 GB (solo modelo; +mmproj ~1 GB + MTP ~1 GB) |
| Peso total en disco | ~16 GB |
| VRAM con técnicas | **~11 GB** (con cmoe/nmoe + KV Q8) según Nichonauta |
| VRAM en 3060 12GB | 6.4 GB (cmoe total) → 10.8 GB (nmoe 19) → 10.2 GB (KV Q8) |
| Velocidad | 23 → 43 tok/s según configuración |
| Backend requerido | **llama.cpp** (las flags --cmoe/--nmoe NO existen en LM Studio para Gemma) |
| Licencia | Apache 2.0 ✅ |

### ⚠️ PROBLEMA CLAVE para el LAB

**LM Studio NO expone --cmoe/--nmoe para Gemma.** El vídeo usó llama.cpp puro.
El lab usa LM Studio (arranque autónomo autorizado, skill lm-studio).

**PERO** — el artículo de Habr (RTX 4070 12 GB) demostró que **LM Studio SÍ tiene
"Number of layers for MoE onto CPU" (ncmoe)** para **Qwen 3.6 35B A3B**:
- ngl=40 (todo a GPU) + ncmoe=40 (MoE a CPU) → **solo 6.2 GB VRAM**
- **42 tok/s** de generación
- Configuración desde el GUI de LM Studio, sin llama.cpp puro

**Conclusión: Gemma 26B A4B NO es viable en LM Studio (faltan flags MoE).
Pero Qwen 3.6 35B A3B SÍ lo es — con la GUI de LM Studio que ya usamos.**

---

## 2. La familia de MoE grandes que SÍ funcionan en 12 GB

### El rey para el lab: **Qwen 3.6 35B A3B**

| Dato | Valor |
|---|---|
| Arquitectura | MoE: 256 expertos, 8 routed + 1 shared (~3B activos de 35B totales) |
| Tamaño Q4_K_M | ~22 GB en disco |
| VRAM en 12 GB | **~6.2 GB** (con ncmoe=40 en LM Studio) |
| Velocidad real (RTX 4070 12GB) | **42 tok/s** |
| SWE-bench Verified | **73.4%** |
| GPQA Diamond | 86.0% |
| Terminal-Bench | 51.5% |
| Comparativa vs Gemma 26B | **Superior**: 21.4 vs 8.7 en HLE (2.5x) — mejor en agentic reasoning |
| Backend | ✅ **LM Studio** (ncmoe en GUI) |
| Licencia | Apache 2.0 ✅ |
| Contexto | 131K/256K |

**Ventaja extra para el lab:** el artículo de Habr lo usó como asistente de
código con **opencode** (exactamente el patrón del lab: OpenCode como worker).

### Otros MoE del rango (para contexto)

| Modelo | Tamaño | ¿Cabe en 12 GB? | Nota |
|---|---|---|---|
| **Qwen 3.6 35B A3B** | 35B/3B activos | ✅ 6.2 GB VRAM (ncmoe) | **El mejor para el lab** |
| **Gemma 26B A4B** | 26B/3.8B | 🟡 Sí, pero solo llama.cpp (no LM Studio) | Inferior a Qwen en agentic |
| **Qwen 30B A3B** | 30B/3B | ✅ (ncmoe) | Anterior, superado por 35B |
| **Qwen 3.6 27B (dense)** | 27B denso | ❌ 16.8 GB weights → 24 GB VRAM | No cabe en 12 GB |
| **Gemma 31B** | 31B denso | ❌ Requiere 24 GB | No cabe |
| **Llama 4 Scout** | 109B/17B | ❌ | Fuera de rango |

### Patrón identificado (respuesta a la pregunta del usuario)

**SÍ — hay una familia entera de MoE ~30-35B con ~3B activos que funcionan en
12 GB gracias a descargar los expertos a CPU (ncmoe).** Son:
- Qwen 3.6 35B A3B (el estándar actual, el mejor)
- Qwen 30B A3B (predecesor)
- Gemma 26B A4B (competidor de Google, requiere llama.cpp)
- Y probablemente futuros MoE de Alibaba/Google con la misma estrategia (A3B/A4B)

**El patrón "total grande + activos pequeños + expertos en CPU" es la nueva
normalidad para GPUs de 12 GB.**

---

## 3. Viabilidad concreta en el LAB (A2000 12 GB)

### Requisitos del lab

| Requisito | Estado |
|---|---|
| VRAM libre | 12 GB totales — GLM ocupa 7.4 GB, R1 8.5 GB |
| Disco | ~22 GB libres para el Q4_K_M (hay 226 GB) |
| RAM | 30 GB totales (el artículo usó 32 GB con 22 GB de modelo → cabe) |
| CPU | i5-9500 6C/6T — el ncmoe usa CPU para expertos; más lento que el 12-core del artículo pero funcional |
| Backend | ✅ LM Studio (GUI, ncmoe disponible para Qwen) |

### El trade-off de VRAM (decisión clave)

| Configuración | Ocupa | Nota |
|---|---|---|
| **Qwen 35B A3B solo** | ~6.2 GB VRAM | ✅ Podría convivir con GLM (7.4 GB) — ¡juntos = 13.6 GB, NO caben! |
| Qwen + GLM | 6.2 + 7.4 = 13.6 GB | ❌ No caben en 12 GB |
| Qwen solo + swap a GLM | — | ✅ Patrón actual de swap |

**Realidad: sigue siendo UN modelo grande a la vez + swap para visión.** Pero
Qwen 35B (6.2 GB) deja más margen que R1 (8.5 GB) o GLM (7.4 GB).

### Rendimiento esperado en la A2000 vs R1-14B actual

| Métrica | R1-14B (hoy) | Qwen 35B A3B (esperado) |
|---|---|---|
| Velocidad | 11 tok/s | **~30-42 tok/s** (3-4x) |
| Calidad | Buena | **Mucho mejor** (73% SWE-bench vs ~40-50% R1-14B) |
| VRAM | 8.5 GB | ~6.2 GB (¡menos!) |
| Coste | 0 € | 0 € |

**La A2000 es comparable a la 4070 12 GB en VRAM pero con menos ancho de banda
(288 vs 504 GB/s)** — la velocidad real será menor que los 42 tok/s del
artículo, pero el 3-4x sobre R1 se mantiene.

---

## 4. CONCLUSIÓN

### Sí, es viable — y hay algo MEJOR

1. **Gemma 26B A4B**: viable pero NO en LM Studio (requiere llama.cpp puro para
   cmoe/nmoe). Cambiar de runtime es una decisión grande.

2. **Qwen 3.6 35B A3B**: **EL GANADOR para el lab**. Funciona en LM Studio
   (el runtime actual), ~6.2 GB VRAM (menos que R1), ~3-4x más rápido, y
   supera a Gemma en agentic coding (que es lo que el lab hace con OpenCode).

3. **La familia existe**: Qwen 30B/35B A3B + Gemma 26B A4B + futuros MoE
   "A3B/A4B" seguirán el mismo patrón → la A2000 de 12 GB tiene vida larga.

### Recomendación

**Experimento prioritario: descargar Qwen 3.6 35B A3B Q4_K_M (~22 GB) y probarlo
en LM Studio con ncmoe=40.** Si rinde ~30+ tok/s en la A2000 (probable), se
convierte en el modelo local de referencia del lab (batch + quizás código
vía OpenCode local), superando a R1-14B.

**Pasos** (cuando se autorice):
1. `lms get qwen/qwen3.6-35b-a3b` (descarga ~22 GB)
2. Cargar con ngl=40 + ncmoe=40 (GUI de LM Studio o CLI)
3. Benchmark: misma prueba que R1 (resumen, clasificación, JSON)
4. Comparar y decidir

### Riesgos honestos

- **RAM**: el modelo completo va a RAM (22 GB) + KV cache → con 30 GB totales
  hay margen pero hay que vigilar (el artículo usaba 32 GB)
- **CPU**: i5-9500 (6C/6T) es más débil que el 12-core del artículo — los
  expertos en CPU serán el cuello de botella; velocidad real por confirmar
- **Ancho de banda GPU**: A2000 = 288 GB/s vs 4070 = 504 GB/s → menos tok/s
- **LM Studio + ncmoe para Qwen**: verificado en el artículo (4070 12 GB)

## Fuentes

- Vídeo Nichonauta: Gemma 26B A4B (43 tok/s, RTX 3060 12 GB)
- Habr (rAnto): Qwen 3.6 35B A3B + opencode en RTX 4070 12 GB (42 tok/s, 6.2 GB VRAM, ncmoe en LM Studio)
- Knightli: guía VRAM Gemma 4 (12 GB → E4B/12B Q4; 26B requiere offload)
- DeepResearch Ninja (mayo 2026): análisis Qwen3.6 vs Gemma 4 vs DeepSeek V4
  (Qwen 35B A3B > Gemma 26B A4B en agentic; Qwen 27B dense no cabe en 12 GB)
- BestLLMfor: Qwen3 30B A3B "Model of the Month" mayo 2026
