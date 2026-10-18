---
title: "Análisis — Vídeo: Liquid LFM 2.5 2.6B (prueba práctica)"
type: research
---

# Análisis — Vídeo: Liquid LFM 2.5 2.6B (prueba práctica)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://youtu.be/bq7sJ3hOpbk (canal técnico español — nichonauta.com)
**Transcripción:** 2026-08-06-transcripcion-youtube5.txt

---

## Qué es

Liquid LFM 2.5, **variante 2.6B** (nueva de la colección 2.5: 0.23B, 1.2B, 2.6B, 8B MoE).
- **Solo texto** (sin visión)
- **Pocos lenguajes** (español e inglés incluidos)
- **Ventana 128K** (literalmente 128,000, no 131,072)
- GGUF oficial disponible (Q8 ≈ 2.87 GB)
- Promoción: muy bueno en **uso agéntico** (tool calling)

## Pruebas reales del autor (llama.cpp + OpenCode)

| Prueba | Resultado |
|---|---|
| Chat básico ("¿por qué el cielo es azul?") | ✅ Respuesta correcta, razonamiento eficiente |
| Código (Tetris HTML one-shot) | ❌ Peor que Gemma 4 E2B / Qwen 3.5 2B |
| Corregir código | 🟡 Aceptable (como Gemma, no sobreentrenado) |
| **Tool calling (OpenCode + MCP)** | ✅ **EXCELENTE** — Brave Search, Playwright (navegador), Context7, escritura de archivos |
| Español | ✅ Bien |
| Procesamiento de input | ✅ Muy rápido (5000+ tok/s al inicio) |
| Generación | 🟡 Sin MTP → ~80 tok/s (menos que rivales) |

## Comparativa real (datos del vídeo)

| Modelo | Tamaño real | VRAM | Notas |
|---|---|---|---|
| **LFM 2.5 2.6B** | 2.6B | ~4.9GB RAM (2GB KV cache @128K) | Solo texto, sin MTP |
| **Gemma 4 E2B** | 2B texto (5.1B total) | **<3GB @4bits** (QAT) | Vision + MTP, mejor VRAM |
| Qwen 3.5 2B/4B/9B | — | — | MTP + visión, 262K ctx |

**Conclusión del autor:** no es el mejor en código ni el más ligero en VRAM (Gemma 4 E2B gana), pero **el tool calling / uso agéntico es muy bueno** — "una alternativa posible a revisar dentro de este tamaño". Al final del vídeo: *"quién sabe qué tal funcione dentro de cosas como Hermes"*.

---

## 🔗 Aplicación al lab

| Aspecto | Análisis honesto |
|---|---|
| ¿Probar LFM 2.6B en el lab? | 🟡 **Candidato solo si** se busca un modelo de tool calling ligero para tareas de enrutamiento/agentes. El lab ya tiene Dolphin 3.0 8B (chat gabinete) + GLM (visión) + DeepSeek (cloud) |
| ¿Ventaja sobre lo actual? | El lab NO tiene un modelo local pequeño dedicado a tool calling puro. Podría probarse en LM Studio como complemento, no sustituto |
| VRAM | 2.6B cabe fácil en la A2000 (12GB) — no es problema |
| Rival directo | Gemma 4 E2B es mejor en VRAM/código; Qwen 3.5 2B mejor en contexto/MTP. El LFM destaca en **uso de herramientas** |

**Veredicto:** interesante como experimento (un modelo pequeño especializado en tool calling para agentes), no como reemplazo de nada existente. El lab ya tiene 4 cerebros; este sería un 5º candidato solo si se busca esa especialización.

**Nota metodológica:** el autor es claro en que los benchmarks del fabricante están elegidos para favorecer al modelo; las pruebas reales del vídeo son la referencia.
