---
title: "Análisis — Qwen 3.8 27B ultra-cuantizado en hardware limitado (Nichonauta, 24-ago-2026)"
type: research
---

# Análisis — Qwen 3.8 27B ultra-cuantizado en hardware limitado (Nichonauta, 24-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/k3ebeIyazBI (Nichonauta, 23-08-2026, 14:11 min, 2.319 views)
**Método:** subtítulos ES descargados (115 KB) → deduplicados (37K→12.5K chars) → análisis completo
**Contexto lab:** conecta con el análisis de Xavier Mitjana (Qwen 3.8 27B local, 23-ago) y con la limitación real de la A2000 (12 GB).

## La pregunta que responde

> **¿Conviene usar un modelo GRANDE MUY cuantizado (IQ1-S, 1 bit) en hardware limitado?**
> Respuesta de Nichonauta (probado en RTX 3060 12 GB): **NO — no sirve para nada.**

## El experimento real (RTX 3060 12 GB, Qwen 3.8 27B IQ1-S = 6.19 GB)

| Config | VRAM | Velocidad | Resultado |
|---|---|---|---|
| 32K contexto + MTP | 9.2 GB | 24-25 tok/s | OK inicial |
| 64K contexto | 11.4 GB | — | Al límite |
| KV cache Q8 | 9.7 GB | — | Calidad casi original, mitad VRAM ✅ |
| KV cache Q4 + 131K | 10.5 GB | — | Ya degrada |
| Sin MTP | 8.6 GB | 24.68 tok/s | Respuesta con sentido |
| MTP=1 | 10.2 GB | 31 tok/s (+29%) | ✅ Mejora real |
| MTP=2 | — | Pierde velocidad | ❌ |

**El test de inteligencia (generar juego Pong en HTML)**: el modelo **no sirve** — repetía las mismas frases, mezclaba cadena de razonamiento con respuesta, generaba texto sin sentido ("Pong no tiene P" — cuando sí la tiene). Tras ~2.000 tokens de razonamiento, seguía sin generar nada útil.

## La conclusión (regla práctica)

> **"El mejor modelo para una colección es el más grande que puedas cargar al menos en Q4_K_M / Q4_XL. Si un modelo solo cabe MUY cuantizado (IQ1-S, 1-2 bits), no conviene — pierde tanta calidad que un modelo más pequeño menos cuantizado funciona mejor, más rápido y con más sentido."**

Demostración inversa: Qwen 3.5 8B en Q4_K_M con visión + MTP + 262K contexto → más rápido, menos VRAM, resultados con sentido.

## 🔴 Mapeo contra el lab (A2000 12 GB)

| Pregunta | Respuesta |
|---|---|
| ¿Qwen 3.8 27B cabe en la A2000? | Solo en IQ1-S (6.19 GB) + KV cache Q8/Q4 (~9-10 GB) — **pero demuestra que no sirve** |
| ¿Conviene probarlo? | **NO** — Nichonauta ya lo probó: genera basura con esa cuantización extrema |
| ¿Qué hace el lab? | Ya sigue la regla: **LFM 2.6B, gpt-oss 20B, GLM 9.5 GB — todos en Q4 o mejor** ✅ |
| ¿Cambia el F6 (Qwen 3.8 con GPU 24 GB)? | NO — refuerza: cuando haya 24 GB, usar Qwen 27B en Q4_XL, no antes |

## Datos técnicos reutilizables (para el futurible Ngram/MTP del 20-ago)

1. **MTP (speculative decoding) con valor 1 acelera +29%** (31 vs 24 tok/s) — pero solo si el modelo base tiene calidad
2. **KV cache en Q8** = mitad de VRAM con calidad casi original — útil para GLM/gpt-oss si se necesita contexto largo
3. **KV cache en Q4 ya degrada** la calidad de respuesta — evitar
4. **MTP=2 pierde velocidad** — el valor óptimo es 1

## Veredicto: VALOR ALTO (confirma la conclusión de la sesión + 2 datos útiles)

1. **Confirma con prueba real** lo que ya sabíamos: Qwen 27B NO es viable en la A2000 — ni siquiera ultra-cuantizado. **La regla "el más grande en Q4 o mejor" valida la elección actual del lab.**
2. **Dato útil 1**: KV cache Q8 = mitad de VRAM — aplicable a GLM (9.5 GB) si el lab necesita contexto largo.
3. **Dato útil 2**: MTP=1 óptimo, MTP=2 contraproducente — matiza el futurible del 20-ago.

**Sin acción nueva.** El vídeo refuerza que la A2000 está bien servida con los modelos actuales (todos ≥Q4) y que el salto a Qwen 27B requiere la GPU de 24 GB (F6, sin fecha).
