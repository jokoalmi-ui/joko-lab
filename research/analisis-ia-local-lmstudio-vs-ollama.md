---
title: "Análisis — Vídeo: IA local en el PC (Gemma 4 + LM Studio vs Ollama)"
type: research
---

# Análisis — Vídeo: IA local en el PC (Gemma 4 + LM Studio vs Ollama)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://youtu.be/01yM-yqG5qY (divulgativo español)
**Tema:** Romper la dependencia de la nube ejecutando modelos locales (Gemma 4, Qwen 3) con herramientas de un clic

---

## Qué dice el vídeo

- La IA local ha dejado de ser para informáticos expertos: **con 16 GB RAM + una GPU
  normal se monta un centro de IA privado**
- Modelos protagonistas: **Gemma 4** (Google DeepMind, multimodal, optimizado para
  hardware doméstico) y **Qwen 3**
- Herramientas de un clic: **LM Studio** y **Ollama** ("Oyama" en el vídeo)
- Ventajas: sin cuotas, sin límites, sin colas, latencia baja, **datos que nunca
  salen del disco**
- Uso con archivos propios: carpetas de PDFs/notas/BD financieras → resúmenes,
  búsquedas, análisis **100% sin internet**

## La prueba (mismo modelo Gemma 4, mismo prompt estricto)

- Examen de lógica (acertijo 3 cajas) + formato JSON obligatorio + restricción de
  vocabulario (sin "imposible" ni "obviamente")
- **LM Studio: 49 segundos**
- **Ollama: 12 segundos**
- Gemini evaluó ambas: **empate técnico en calidad** (misma lógica, misma estructura,
  mismas restricciones cumplidas). Ollama más conciso; LM Studio más detallado

### Conclusión del autor (Windows)

| Gana | Cuándo |
|---|---|
| **Ollama** | Velocidad pura, menor RAM en background, flujo por consola, API local |
| **LM Studio** | Interfaz gráfica completa (temperatura, contexto), descargar cuantizaciones de HF |

---

## 🔗 Aplicación al LAB (lo interesante)

El lab ya eligió LM Studio (2026) — este vídeo es divulgativo y NO cambia esa
decisión, pero el dato de **Ollama 12s vs LM Studio 49s** merece análisis honesto:

| Pregunta | Respuesta honesta |
|---|---|
| ¿Es justa la comparativa? | 🟡 Parcial — mismo modelo, mismo prompt, pero sin control de parámetros (KV cache, contexto, cuantización) en LM Studio; la diferencia de 4x huele a configuración (LM Studio sin optimizar / contexto enorme / sin cache) |
| ¿Debe el lab cambiar a Ollama? | ❌ No — el lab ya tiene LM Studio funcionando + script headless + GLM visión cargado; cambiar de motor rompe el stack |
| ¿Vale como dato? | 🟡 Sí, para el estudio comparativo de motores: **medir en el lab con la A2000** cuál es el rendimiento real (los 49s vs 12s pueden ser configuración) |
| ¿Gemma 4 es relevante? | ✅ Sí — para el estudio comparativo de modelos pequeños (es candidato: multimodal, optimizado doméstico) |

**Lección real para el lab:** cuando se compare motores (LM Studio vs Ollama vs
llama.cpp), **controlar los parámetros** (misma cuantización, misma KV cache, mismo
contexto) — si no, la diferencia de velocidad es configuración, no motor.

---

## Veredicto

Vídeo divulgativo correcto para público general (confirma la tendencia local-first
que el lab ya vive). Único dato aprovechable: la comparativa de velocidad, que
queda como referencia para el estudio de motores con control de parámetros.
