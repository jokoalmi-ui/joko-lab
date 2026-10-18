---
title: "Análisis — \"FreeToken: El Nuevo Motor de IA Local que Podría Dominar en 2027\" (CodeSimple, 25-ago-2026)"
type: research
---

# Análisis — "FreeToken: El Nuevo Motor de IA Local que Podría Dominar en 2027" (CodeSimple, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/0T3Rvz4eidA (CodeSimple, 9 min, 2.219 views)
**Método:** metadatos + subtítulos ES (74 KB → 7.9K chars limpios, lectura completa)

## Qué es FreeToken
Nuevo motor de inferencia local para **modelos MoE (mezcla de expertos)**. La idea central:
- **llama.cpp** (el motor que ya usas) resuelve la memoria con **partición fija por capas**: decides antes de arrancar cuántas capas van a GPU y cuántas a CPU; ese número no cambia. Problema: el router de un MoE cambia de expertos palabra a palabra, así que la partición fija es ciega al patrón real.
- **FreeToken apuesta por caché adaptativa consciente de rutas del router**: deja que el patrón de uso decida qué expertos viven en la caché de la GPU.

## Números del paper (del propio equipo — no independientes)
| Métrica | FreeToken | llama.cpp | Otro |
|---|---|---|---|
| Fallos de acceso al experto correcto (5090) | **16/100** | 62/100 | — |
| 5090 + 35B MoE | 77-83 tok/s | — | — |
| DeepSeek V0.4 Flash | 22-25 tok/s | — | casi el doble |
| GLM (workstation) | **14,9 tok/s** | 7,3 tok/s | — |
| **Peor latencia de turno** | **<44 s** | >232 s | 946 s (~16 min) |

El dato clave: la **cola de latencia** (peor turno). Muchos agentes de código matan el proceso si la respuesta tarda >2 min → FreeToken sobrevive donde llama.cpp muere.

## La crítica honesta del vídeo (importante)
1. **Números del propio equipo** que escribió el motor — no es medición independiente.
2. **El gráfico principal infla la ventaja**: comparan sus barras (77+) contra una línea de "agente en producción 33 tok/s" que **incluye tiempo hasta la primera palabra + razonamiento intermedio**. La cifra comparable de generación pura es **61,3 tok/s** → la ventaja real es **~1,3x, no 2,4x**. No es mentira (ambos números citados correctamente) pero el punto de referencia infla casi al doble.
3. **Solo Linux + Nvidia**: no hay build para Mac ni Apple Silicon; las 8 issues más votadas = soporte tarjetas viejas, doble GPU, Docker, Windows, Apple Silicon.
4. **Proyecto pequeño**: 2 mantenedores, 30 commits, 408 estrellas vs **446 colaboradores de llama.cpp** y 25.000 descargas nocturnas.
5. **Coste real**: 5090 ~$4.000 (verano 2026, doble de precio de lista) = ~500 sesiones de agente en nube o 1.000-40.000 sesiones a precio DeepSeek. La tarjeta no es gratis; el argumento real es privacidad + control + no dependencia.

## 🔴 Aplicación al LAB — VALOR MEDIO-BAJO (vigilar, no instalar)

| Ángulo | Veredicto |
|---|---|
| **¿Instalar FreeToken?** | ❌ NO hoy: el lab tiene **RTX A2000 12 GB** (FreeToken apunta a 5090/32GB+); solo Linux+Nvidia (ok) pero proyecto de 408★ con 2 mantenedores; llama.cpp sigue ganando por compatibilidad |
| **La idea (caché adaptativa)** | 🟡 **Vigilar**: si llama.cpp absorbe la idea (predicción del propio vídeo para 2027), el lab la obtendrá gratis vía LM Studio/Ollama (que usan llama.cpp) |
| **Lección de la cola de latencia** | 🟢 Aplicable al lab: los timeouts de agente (2 min) matan procesos — el lab ya gestiona timeouts en scripts/crons; tener en cuenta en el pipeline LLM |
| **Material TFM/LinkedIn** | 🟢 El análisis crítico de benchmarks (1,3x vs 2,4x) es buen ejemplo de "cómo leer un paper de IA" |

**Señal de activación**: cuando FreeToken pase ~10.000★, llegue a Apple Silicon o el lab tenga GPU >16 GB. Hasta entonces, llama.cpp (vía LM Studio) sigue siendo el motor correcto.

## Conclusión
VALOR MEDIO-BAJO: interesante técnicamente (caché adaptativa para MoE) pero inmaduro (408★, solo Linux+Nvidia, benchmarks del propio equipo con punto de referencia inflado). El lab no cambia nada hoy. La lección de la cola de latencia y el análisis crítico de benchmarks sí tienen valor.
