---
title: "Análisis — DeepSeek V4 Flash Official API (vídeo YouTube, 10-ago-2026)"
type: research
---

# Análisis — DeepSeek V4 Flash Official API (vídeo YouTube, 10-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 10-ago-2026
**Fuente:** https://youtu.be/9RNVLn8-vr4 — canal de desarrollo (comparativa de modelos)
**Tema:** Lanzamiento de la API oficial DeepSeek V4 Flash (0731) + comparativa con Kimi, Qwen 3.8 Max, Luna y GPT-5.6

---

## Contenido del vídeo

### DeepSeek V4 Flash Official API (la novedad)

| Dato | Valor |
|---|---|
| **Versión** | V4 Flash 0731 (última) |
| **Contexto** | La "Preview" salió el 24-abril; AHORA es la versión oficial |
| **Precio** | **$0.14/M input · $0.28/M output** (ridículamente barato, ~25x menos que modelos frontera) |
| **Benchmarks** | Mejores que la Pro Preview — nivel GPT-5.6 en algunos |
| **Integración** | Disponible en Codex + OpenCode (Go) + 31,000 peticiones |
| **Pesos abiertos** | Publicados (HuggingFace) — requiere ~128 GB RAM para self-host |
| **Artificial Analysis** | Subió 10 puntos; inteligencia similar a GPT-5.6 (1 punto de diferencia); por encima de MiniMax M3 y DeepSeek Pro |

### Lo que probó (comparativa ciega)
- **DeepSeek V4**: funcionó, ~52-71 TPS pero el más LENTO de los probados vía OpenRouter (le tocó el peor provider, 3 tok/s — crítica a OpenRouter por enrutar al peor servidor)
- **Kimi**: falló (errores de código)
- **Qwen 3.8 Max**: nuevo (2.4B parámetros = 2,400 millones... en realidad 2.4 T según el autor), $2/M input $6/M output, trabajo autónomo hasta 10-16 días, diseño de chip 12h autónomo, Text Arena #2 solo detrás de Fable 5, multimodal (texto/imagen/vídeo), contexto 1M tokens — pero TAMBIÉN falló en la prueba
- **Crítica del autor**: los modelos chinos de pesos abiertos tienen APIs menos estables; OpenRouter enruta al peor provider sin avisar

### Conclusión del autor
Los modelos chinos de pesos abiertos cada vez más grandes e inteligentes con calidad/precio muy atractiva — alternativa real a Anthropic. Pero los 3 que probó fallaron en el momento de máxima demanda (acaban de salir).

---

## 🎯 Aplicación al LAB

### La conexión directa: DeepSeek V4 Flash = el modelo que YA usa el lab

| Aspecto | Lab |
|---|---|
| **Modelo** | deepseek-v4-flash (config.yaml, Hermes + pipeline_proxy) |
| **Precio** | $0.077/M prompt (con cache) — el vídeo dice $0.14/M pero el lab ya lo tiene más barato con caché |
| **API oficial** | ✅ api.deepseek.com/v1 — la que usa el lab directamente |
| **Estabilidad** | El lab no pasa por OpenRouter → evita el problema del vídeo (peor provider) |

### ⚠️ Los 2 aprendizajes reales para el lab

1. **Confirmado: el lab usa la API oficial directa** — la elección correcta. El vídeo critica OpenRouter por enrutar al peor provider (3 tok/s); el lab va directo a DeepSeek → no tiene ese problema.

2. **La inestabilidad de DeepSeek es real en picos** — el vídeo muestra fallos en momentos de máxima demanda (acaban de lanzar la versión). **El lab ya tiene el fallback natural: router local/cloud** (R1-14B para batch cuando DeepSeek falla).

### 💡 El dato que refuerza la estrategia de coste

El vídeo confirma que **DeepSeek V4 Flash es de los modelos con mejor calidad/precio** (nivel GPT-5.6 a cuarta parte del coste). **La palanca del lab sigue siendo la misma: reducir contexto (99.7% del coste), no cambiar de modelo** — el modelo ya es de los más baratos del mercado.

### 📌 Futurible relacionado

Qwen 3.8 Max (2.4T, $2/$6 por M, trabajo autónomo 10-16 días, contexto 1M, multimodal) — el autor lo destaca como el próximo gran salto. **A vigilar para el lab** (candidato futuro para tareas agentic largas, aunque caro para el lab).

## Conclusión

Vídeo de novedades (DeepSeek V4 Flash official + Qwen 3.8 Max). Para el lab: **confirma que el stack actual es correcto** (API oficial directa, modelo barato con buena calidad, fallback local listo). La inestabilidad en picos refuerza el valor del router local/cloud. Sin acciones urgentes.

## Nota honesta

Los precios del vídeo ($0.14/$0.28) son los oficiales sin caché; el lab usa $0.077 prompt con caché de contexto (los precios del lab ya medidos: 62.45 USD/3d con 99.7% en prompt). El vídeo no cubre caché — el lab sí la aprovecha.
