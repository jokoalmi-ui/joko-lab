---
title: "Análisis — \"Probé GLM 5.3: ¿realmente compite con Kimi 3 y Qwen 3.8?\" (Fazt Code, 24-ago-2026)"
type: research
---

# Análisis — "Probé GLM 5.3: ¿realmente compite con Kimi 3 y Qwen 3.8?" (Fazt Code, 24-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=Boz0W0tTgUU (Fazt Code, 22-08-2026, 15:14 min, 4.879 views)
**Método:** subtítulos ES (179 KB) → deduplicados (57.8K→19.4K chars) → análisis completo
**Categoría:** estudio de modelos cloud/locales mejores/baratos para el LAB (petición del usuario)

## ⚠️ Nota de veracidad

Vídeo con sponsor (Hostinger, ~4 min iniciales — descartado). Las pruebas reales son auténticas (las ejecuta en vivo con Command Code). Los benchmarks citados son de Artificial Analysis y Cybergin (no son de Fazt — fuentes externas).

## Qué es GLM 5.3 (datos del vídeo + benchmarks externos)

| Dato | Valor |
|---|---|
| Empresa | Zhipu (ZII) — china |
| Base | Reentrenamiento de GLM 5.2 (misma arquitectura) |
| Posicionamiento | **A la par de Kimi 3 y Qwen 3.8** — el "trío chino" competitivo |
| Comparación con frontier | No vende "a nivel Opus 5" — se posiciona como alternativa directa a Kimi 3 |
| Modalidad | **SOLO texto** (no multimodal, a diferencia de GPT) |
| Contexto | 1M tokens |
| Precio | **Más barato que Grok 4.6** · similar/menor que Kimi 3 · ~1/3 de Opus 5 |
| Ciberseguridad | Benchmark Cybergin: casi a la par de Tropic/GPT (mejor que la mayoría de chinos) |
| Velocidad | Respuesta más veloz que Grok 4.6 (según Fazt) |

## 🔴 La parte honesta: las pruebas reales NO respaldan los benchmarks

Fazt probó 3 tareas reales con Command Code (harness):

| Tarea | Resultado real |
|---|---|
| **Juego 3D (Resident Evil cabaña)** | 🔴 **FALLÓ al primer intento** — entró en loop de planificación; hubo que simplificar el prompt; tardó ~10 min en empezar a escribir código; resultado mediocre |
| **E-commerce Next.js + Stripe** | 🔴 **Mediocre** — 20 min, usó Next 14 (versión antigua), error de variable de entorno al ejecutar; "no es tan sorprendente" |
| **Landing page agencia marketing** | 🟡 Aceptable — diseño no típico (parecía interfaz de música), no es "UI slop" |

**La frase clave de Fazt**: *"he probado esto con Qwen y con DeepSeek, e irónicamente esos modelos responden mucho mejor a pesar de que están muy por detrás de los benchmarks."*

**Lentitud**: ~10 min de planificación antes de implementar (modelo o harness — no lo sabe).

## 🎯 Aplicación al LAB (estudio de modelos cloud/locales)

### Lo que aporta a tu estudio

1. **El "trío chino" (Kimi 3, GLM 5.3, Qwen 3.8) está a la par** — ya casi no hay diferencia entre modelos chinos; todos llegan al mismo nivel (cita de Fazt: "ahora casi todos están llegando al mismo nivel")
2. **GLM 5.3 es el más barato del trío** — pero solo texto (el lab necesita visión → GLM 4.6V local para eso, o cloud multimodal)
3. **⚠️ Lección CRÍTICA para el lab**: los benchmarks dicen "a la par", pero **en la práctica DeepSeek/Qwen funcionaron MEJOR** en las mismas tareas. **Confirma la regla del lab: validar con pruebas reales (batería 5x5), no con benchmarks.** El lab ya hace esto (juicio ciego CLI).

### Mapa con el stack actual del lab

| Modelo | Rol en el lab | Estado |
|---|---|---|
| **DeepSeek (cloud)** | Modelo principal (DeepSeek API en .env) | ✅ Ya en uso — y según Fazt, responde mejor en la práctica que GLM 5.3 |
| **GLM 4.6V-Flash (local)** | Visión local (LM Studio) | ✅ No confundir con GLM 5.3 (cloud, texto-only) — son modelos distintos |
| **gpt-oss-20b (local)** | Razonamiento local | ✅ |
| **LFM 2.5 (local)** | Ligero | ✅ Futurible QAD |
| **GLM 5.3 (cloud)** | ¿Alternativa barata? | ⚪ **No aporta al lab**: solo texto (el lab ya tiene DeepSeek texto), y las pruebas reales de Fazt muestran que es lento y mediocre vs DeepSeek/Qwen |

### Conclusión honesta para el estudio de modelos

**GLM 5.3 NO entra al stack del lab**: el lab ya tiene DeepSeek (cloud, texto) que en las pruebas reales de Fazt responde mejor; GLM 5.3 es solo texto (el lab necesita visión aparte); y es lento en la práctica. **El dato útil es el patrón**: los modelos chinos están convergiendo (misma calidad, precios a la baja) — la regla de decisión del lab (validar con batería real, no benchmarks) es exactamente la correcta para este mercado.

## Veredicto: VALOR MEDIO-BAJO para el lab

- ✅ **Valida la regla del lab**: benchmarks ≠ realidad; pruebas reales mandan (batería 5x5 + juicio ciego)
- ✅ **Dato del mercado**: el trío chino converge; DeepSeek sigue siendo opción sólida
- ❌ **GLM 5.3 no se añade** (solo texto, lento en pruebas, redundante con DeepSeek)
- ⚪ Sin futuribles nuevos — refuerza la metodología de evaluación existente

**Material LinkedIn/TFM**: "cuando los benchmarks dicen que tres modelos están a la par, la práctica real los separa" — ejemplo de por qué el lab valida con baterías reales, no con gráficas.
