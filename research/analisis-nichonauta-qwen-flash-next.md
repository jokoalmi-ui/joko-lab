---
title: "Análisis — \"Mejor que DeepSeek V4 Pro en mi PC 🚀 Qwen 3.8 Flash Next es INCREÍBLE\" (Nichonauta, 01-sep-2026)"
type: research
---

# Análisis — "Mejor que DeepSeek V4 Pro en mi PC 🚀 Qwen 3.8 Flash Next es INCREÍBLE" (Nichonauta, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/RirKlGTe9fE (@nichonauta, ~10 min, transcripción completa 11 KB)
**Fecha:** 2026-09-01 22:50 CEST

## Contenido — Qwen 3.8 Flash Next (previsualización de arquitectura Qwen 4)

**Arquitectura** (según documentación oficial):
- ~180B parámetros totales (MoE: 6B activos + 51B n-gramas para predicción rápida + 4B MTP para speculative decoding + visión)
- Contexto 262.144 tokens, expandible hasta 1M (modificación del GGUF)
- Visión de imágenes (y vídeo con mmproj)

**Pruebas reales de Nichonauta** (Ryzen 5, DDR4 3200 CL16 dual channel, GPU NVIDIA ~12 GB):
| Configuración | Resultado |
|---|---|
| Q2_K_L + mmproj (74.2 GB), todo en RAM, sin CUDA | ~5 tok/s |
| Con CUDA (llama.cpp nuevo) | 6.3 GB VRAM usados, 79 GB RAM |
| 43 capas CPU / 4 capas GPU (KV cabe) | **~13 tok/s** |
| Con MTP (aún no soportado en llama.cpp estable) | estimación 30 tok/s (especulación del autor) |

**Benchmarks citados** (Qwen + Artificial Analysis): Qwen 3.8 Flash Next > DeepSeek V4 Pro 0813 (checkpoint nuevo) > GLM 5.3 Flash > Qwen 3.8 27B. El autor concluye: "en mi PC cargo algo superior a DeepSeek V4 Pro, ilimitado, privado y gratis".

**Ajuste para 12 GB GPU**: Q3 (90 GB) o UDQ4 KXL (111 GB) caben en 12 GB GPU + 128 GB RAM.

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (referencia/benchmark, NO implementable hoy)

| Ángulo | Veredicto |
|---|---|
| **¿Cabe en el lab?** | 🔴 **NO**. Verificado con `free -h`: el lab tiene **30 GB RAM** (el vídeo asume 128 GB). El mínimo Q2 son ~74 GB; Q3 ~90 GB. Con 30 GB es inviable (ni con el i9-9900K pendiente — la RAM es del sistema, no del CPU) |
| **Estado del arte local (referencia)** | 🟢🟢 El dato más valioso: el mejor modelo de pesos abiertos actual (según benchmarks externos) supera a DeepSeek V4 Pro en local. Confirma la dirección local-first del lab (la brecha cloud↔local se está cerrando) |
| **Comparativa útil para decisiones** | 🟢 Si el lab considera el i9-9900K + ampliación de RAM (futurible de hardware), este modelo es el candidato a evaluar (Q3 90 GB, 12 GB GPU + RAM ampliada) |
| **Lección de rendimiento** | 🟢 MoE con pocos activos: 13 tok/s de un 180B en un PC normal con solo 4 capas en GPU — la RAM es el cuello de botella, no la GPU |
| **MTP/NGAM** | 🟡 Recordatorio: el MTP del modelo no funciona aún en llama.cpp estable (se necesita versión experimental). No fiable hoy |

**Conclusión**: VALOR MEDIO-ALTO como **referencia de estado del arte** (qué modelo domina el local ahora, comparativa DeepSeek V4 Pro local vs cloud), pero **NO implementable en el lab**: 30 GB RAM no pueden cargar ni el mínimo Q2 (74 GB). Futurible de hardware, no de software.

## Notas de honestidad

- **Cifras de benchmark no verificadas de forma independiente** (el autor cita Qwen + Artificial Analysis; el título "mejor que DeepSeek V4 Pro" es afirmación del autor sobre benchmarks, no una prueba propia del lab).
- "Qwen 3.8 Flash Next" es el nombre real del modelo (transcripción ASR confunde con "Quen/Quen"; el autor lo dice explícitamente).
- El dato de RAM del lab (30 GB) es verificación propia de hoy (`free -h`), no del vídeo.
- El vídeo es de un canal ya en el consolidado del lab (Nichonauta, el más valioso técnicamente).
- Benchmark "Artificial Analysis" no contrastado en este análisis (no era el objetivo).
