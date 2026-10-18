---
title: "Análisis — Qwen 3.8: La IA local se acaba de poner SERIA (midudev, 20-ago-2026)"
type: research
---

# Análisis — Qwen 3.8: La IA local se acaba de poner SERIA (midudev, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/Msi1EgEx-WE (midudev, 20-08-2026, 12:16)
**Método:** transcripción ES completa (yt-dlp auto-subs, VTT limpio + dedup, 69.5K chars, leída íntegra)
**Veredicto:** [VERIFICADO] — datos del vídeo + contexto del lab (VRAM real 12 GB)

## VALOR REAL: MEDIO-ALTO (información de referencia — NO accionable hoy)

El vídeo presenta el nuevo rey de los modelos locales (Qwen 3.8), con
benchmarks al nivel de Opus 4.6 Max. PERO el requisito mínimo útil es
**24 GB VRAM** — el lab tiene **RTX A2000 de 12 GB**. Es información clave
para decidir futuros upgrades, no una acción inmediata.

## Datos verificados del vídeo

### Qwen 3.8 (Alibaba, pesos abiertos, Apache 2.0)
| Dato | Valor |
|---|---|
| Tamaño útil | **27B parámetros** (denso, multimodal: texto+imagen+vídeo) |
| Contexto nativo | **262K tokens** (expandible a **1M**) |
| Nivel | **Opus 4.6 Max** (algunos benchmarks por encima, otros por debajo) |
| Especialidad | Código real + flujos de oficina |
| Licencia | Apache 2.0 (comercial OK) |
| Punto dulce | **4-bit @ 24 GB** (4090, 3090, 7900 XTX, M4 Pro 32 GB) |
| 16 GB | Entra justo, tirones (~15 tok/s) |
| 54 GB | 100% precisión sin cuantificar |
| 5090 | **200 tok/s** (midudev real) |

### Lecciones del vídeo (no solo specs)
1. **Effort de pensamiento por defecto en MAX = piensa demasiado** → bajarlo a HIGH (lección directa aplicable a cualquier modelo con reasoning)
2. **Benchmarks no son de fiar / no todos pesan igual** → hay que PROBAR (exactamente la filosofía del lab: batería de PRODUCCIÓN, no sintética)
3. **Modelos sin censura = torpes** (le quitas el arnés/system prompt y pierde el "cómo funcionar") → el lab NO debe usar esos derivados para trabajo real
4. Contexto: Muse Glimmer (Meta 30B) fue rey 1 semana → **Qwen 3.8 lo destrona** (midudev probando ambos en local)
5. DGX Spark: 22 tok/s con Qwen 3.8 (mucha RAM, poco ancho de banda) vs 200 en 5090 — **el ancho de banda de memoria manda más que la RAM total**

## 🔴 Conexión con el LAB

| Aspecto | Veredicto |
|---|---|
| **¿Puede el lab ejecutar Qwen 3.8 hoy?** | ❌ **NO** — 12 GB VRAM < 24 GB punto dulce (a 4-bit entraría "justo con tirones" en el límite de 16 GB, y el lab tiene 12) |
| Contexto 262K nativo | ✅ **Muy relevante**: el lab maneja documentos grandes (RAG LanceDB ~19.9K filas, backlog 1041 lín.) — un modelo con 262K de contexto nativo cambiaría el pipeline |
| "Prueba, no te fíes de benchmarks" | ✅ VALIDA al 100% la batería de PRODUCCIÓN del lab (5 tareas reales + juicio ciego CLI) |
| Effort de pensamiento MAX → HIGH | ✅ Pitfall directo: GLM del lab también razona en voz alta (content:'') — misma clase de problema |
| Competencia Meta (Muse Glimmer 30B) | 🟡 A vigilar — mismo perfil que Qwen 3.8 |
| Estado de gpt-oss-20b en el lab | ⚪ Sigue siendo el mejor para 12 GB (validado 7/7) — Qwen 3.8 NO lo sustituye sin hardware nuevo |

## Futurible (registrado)

**F6: Qwen 3.8 (o Muse Glimmer) como candidato principal SI se actualiza la GPU a 24 GB** — señal de activación: upgrade de hardware (4090/5090 o equivalente). Con 12 GB actuales es inviable. También: probar el ajuste "effort de pensamiento HIGH" en GLM del lab (lección 1 del vídeo, 0 coste).

## Veredicto honesto

**Valor medio-alto como referencia de mercado.** Confirma que la frontera
local avanza rápido (Opus 4.6 en local a 24 GB), pero **no es accionable hoy**
para el lab (VRAM insuficiente). La lección transversal (probar > benchmarks)
valida el método del lab. El ajuste de effort de pensamiento sí es un
micro-experimento viable con GLM ya cargado.
