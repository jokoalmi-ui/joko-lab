---
title: "Análisis — Qwen 3.8 27B local vs Google/Anthropic (Xavier Mitjana, 23-ago-2026)"
type: research
---

# Análisis — Qwen 3.8 27B local vs Google/Anthropic (Xavier Mitjana, 23-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/ZqkljdI1HT0 (Xavier Mitjana, 23-08-2026, 19:36 min, ~16.5K likes)
**Método:** subtítulos ES descargados (189 KB VTT) → deduplicados (solapamiento triple, 61K→20.7K chars) → análisis completo

## El vídeo en 1 párrafo

Qwen 3.8 27B (17 GB, open source, Apache 2.0) ya se ejecuta en una GPU de consumo y, según el índice de **Georgi Gerganov** (creador de llama.cpp), puntúa 52 vs 38 de la versión anterior (+14 puntos) — **la primera vez que un modelo local alcanza vanguardia**. No supera en inteligencia general a DeepSeek/GLM/Opus 4.7/Gemini Flash, **pero SÍ gana en el índice de AGENTES (herramientas/trabajo)**. Aun así, lo top de Anthropic (Opus 5, Fable 5) sigue por encima.

## La prueba práctica (su proyecto vs Google)

Le encargó el mismo proyecto al modelo local y al mejor modelo de Google. Conclusión del vídeo: **si mañana Google/Anthropic cortaran el grifo, podría seguir trabajando solo con IA local** — con pérdidas de agilidad, pero casi nada se quedaría sin hacer y con calidad similar.

## 4 avisos de configuración (dato práctico útil)

1. **Viene mal configurado de fábrica**: razonamiento al MÁXIMO por defecto (Simon Willison: dibujo → 21 min y 22.000 palabras pensando; con razonamiento apagado → 2 min). → Bajar a bajo/desactivado y subir solo si hace falta.
2. **En LM Studio, subir la ventana de contexto al cargarlo** — la de defecto se la come solo pensando.
3. **Lento por defecto**: 15-30 tok/s en configuración estándar; con la cuantización que trae de serie → **hasta 70 tok/s en una 4090 con visión y 100K contexto** (el dato del vídeo comparando con nube quedó confuso en la transcripción ASR — "1,74" no es verificable, NO usar ese número).
4. **El conocimiento técnico de configuración sigue siendo la barrera de entrada** a la IA local.

## ⚠️ Análisis crítico: dónde el vídeo EXAGERA (no inventa, pero infla)

| Afirmación del vídeo | Matiz real (del propio vídeo) | ¿Exageración? |
|---|---|---|
| Título: "La IA de tu PC **ya supera a Google**" | El propio contenido dice: NO supera en inteligencia general a DeepSeek/GLM/Opus 4.7/Gemini Flash; solo gana en **AGENTES** | ⚠️ **SÍ, hipérbole del titular** |
| "Puntúa por delante de Claude Opus 4.8, QV4 Pro, GPT 5.6" | Verdad, pero solo en el **índice específico de Gerganov** (llama.cpp), no en todos los benchmarks | ⚠️ Parcial: depende del índice |
| "Primera vez que un modelo local alcanza vanguardia" | Es la afirmación de **Gerganov** (creador de llama.cpp) — parte interesada en que los modelos locales funcionen | ⚠️ Interés declarado del autor |
| "Podría seguir trabajando solo con IA local si cortan el grifo" | Él mismo matiza: "sufriendo dolores de muelas, perdería agilidad, volver a flujos de hace meses" | ⚪ Matizado en el propio vídeo |
| No supera a Opus 5/Fable 5 (lo top actual de Anthropic) | Dicho explícitamente | ❌ No exagera — es honesto |

**Veredicto sobre la veracidad**: el vídeo NO inventa datos (los números de índice son reales y cita a Gerganov), pero el **titular es hipérbole** — "supera a Google" es falso en inteligencia general, solo cierto en el subíndice de agentes y en un índice concreto. El contenido matizado es honesto; el empaque es clickbait.

## La frase clave (alineada con el lab)

> "¿Para qué pagar un cohete si necesitas un utilitario? Si mañana cortara el grifo, ¿cuánto de tu trabajo se pararía de verdad? Lo que no se para es lo que pagas por costumbre."

## Mapeo contra el LAB

| Aspecto | Estado |
|---|---|
| Filosofía local-first (no pagar por costumbre) | ✅ **El lab ES esto** — router local/cloud, coste 0 tras 12:00, RULE-003 |
| Modelo pequeño que iguala a grandes en tareas reales | ✅ gpt-oss-20b validado 7/7 (batch), LFM 2.6B — misma lógica |
| **Qwen 3.8 27B ejecutable** | ❌ **Requiere ~24 GB VRAM** (17 GB modelo + contexto) — la A2000 (12 GB) NO puede. Es el mismo muro de siempre |
| Configuración como barrera (razonamiento/contexto) | ✅ Lección aplicable a GLM/gpt-oss: effort MAX→HIGH ya anotado (20-ago) |

## Veredicto: VALOR MEDIO-ALTO (validación + refuerza futurible existente)

1. **Refuerza el futurible F6 ya anotado (20-ago)**: Qwen 3.8/Muse Glimmer si la GPU se actualiza a 24 GB. Este vídeo es la validación práctica de por qué valdría la pena.
2. **Valida la dirección del lab**: la conclusión del vídeo ("trabajar solo con local si cortan el grifo") es EXACTAMENTE el diseño del lab (local-first con escalada cloud).
3. **Sin acción nueva hoy**: la GPU de 12 GB no puede ejecutar Qwen 3.8. El techo de VRAM vuelve a ser el factor limitante (misma conclusión de la sesión).
4. **Dato reutilizable**: los 3 avisos de configuración (razonamiento bajo por defecto, contexto alto en LM Studio, cuantización → 70 tok/s) aplican al lab cuando llegue un modelo local grande.

**Sin futuribles nuevos** (F6 ya existe). El vídeo es más validación de filosofía que novedad técnica accionable con el hardware actual.
