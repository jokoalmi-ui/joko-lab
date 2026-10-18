---
title: "Análisis — Nichonauta: \"Iterar Rápido con IA — Ngram y MTP\" (20-ago-2026)"
type: research
---

# Análisis — Nichonauta: "Iterar Rápido con IA — Ngram y MTP" (20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/pe2SuSIaU8A (Nichonauta)
**Método:** transcripción VTT en español descargada y verificada (99 KB → 32.7K chars limpios)
**Veracidad:** [VERIFICADO] — técnica y números extraídos de la transcripción real

---

## QUÉ ES

Vídeo de Nichonauta (canal de IA local/open source, conocido del lab) sobre
cómo **acelerar modelos de lenguaje con speculative decoding usando Ngram y
MTP** (Multi-Token Prediction), combinado con la filosofía de "iterar rápido
con IA".

## CONTEXTO (serie previa del canal)

- Vídeos anteriores: speculative decoding con modelos borrador (modelos
  pequeños que predicen el texto del grande)
- Hallazgo previo: **no usar borrador y usar solo el contexto** daba
  velocidades **hasta 5x o más**
- Filosofía central: "un modelo más grande e inteligente con un único prompt
  puede llegar más lejos, pero **ninguno hace todo a la primera**" → hay que
  ITERAR

## TÉCNICAS EXPLICADAS

### 1. Ngram (16 menciones)
- Acelera la generación SOLO cuando escribes cosas **similares a lo anterior**
  (fragmentos repetidos del contexto/prompt)
- Útil para: código con patrones repetitivos, textos con estructura
  recurrente

### 2. MTP — Multi-Token Prediction (12 menciones)
- El modelo predice **varios tokens a la vez** en lugar de uno a uno
- Combinable con Ngram ("MTP con todo y Ngram")

## RESULTADOS DE VELOCIDAD (datos de la transcripción)

| Configuración | Velocidad |
|---|---|
| Modelo base (sin aceleración) | ~50 tok/s o poco menos |
| Con Ngram (fragmentos repetidos) | **>100 tok/s**, picos 277-306 |
| Con Ngram+MTP | **>200 tok/s promedio**, picos hasta 300, valores 195-273 |
| Tarea de razonamiento (cadena) | ~40 tok/s (poca aceleración — no hay texto repetido) |
| Tarea de código | **>200 tok/s** (sí se acelera — código es repetitivo) |
| Consumo VRAM | ~10 GB con ambos métodos |

**Observación clave**: con Ngram+MTP llegó a **86.64 tok/s** incluso en
tareas con poca repetición; en código, **200+ tok/s vs 50 del base = 4x**.

## LECTURA PARA EL LAB

| Aspecto | Relevancia |
|---|---|
| **MTP en LM Studio** | ⚠️ LM Studio no expone MTP directamente (es flag de llama.cpp) — el lab usa GLM/R1/gpt-oss |
| **Ngram en llama.cpp** | ✅ Los backends de LM Studio/Ollama SÍ soportan flags de speculative decoding (n-gram) |
| **R1-14B a 11 tok/s** | Potencial de mejora si se activa ngram para tareas repetitivas (batch/JSON) |
| **gpt-oss-20b a 15 tok/s** | Idem — el speculative decoding podría acercarlo a los 53-67 tok/s teóricos del benchmark llama.cpp |

**Veredicto**: la técnica es REAL y verificada (números de la transcripción),
pero requiere flags de llama.cpp que LM Studio expone de forma limitada.
**Futurible**: probar flags de speculative decoding (n-gram) en llama-server
del lab para tareas repetitivas (batch, JSON, código) — señal: cuando el lab
tenga una tarea batch que haga ~30-60 min diarios y valga la pena optimizar.

**Filosofía "iterar"**: valida el patrón del lab de no esperar el prompt
perfecto a la primera — iterar con verificación (gate de veracidad,
verificar_research, revisor) es exactamente el flujo del lab.

## Nota de proceso
- Transcripción: /tmp/vid_pe2.es.vtt y /tmp/pe2_limpio.txt (temporales)
- 7 menciones speculative decoding · 66 menciones velocidad/tok/s
