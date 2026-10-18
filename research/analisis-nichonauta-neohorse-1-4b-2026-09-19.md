---
title: "Análisis — NeoHorse-1-4B (TokenRhythm): el vendor dice +5,93, la prueba real dice que no mejora (Nichonauta, 18-sep-2026)"
type: research
fecha: 2026-09-19
---

# Análisis — NeoHorse-1-4B (TokenRhythm): el vendor dice +5,93, la prueba real dice que no mejora (Nichonauta, 18-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/HahjBkz-0eY — **[Nichonauta] «NeoHorse-1-4B es prometedor 🤖 ¿Realmente mejora al Qwen 3.5 4B?»**, **21:02 min**, publicado **18-sep-2026** (4.077 vistas, 95 likes). Transcripción ES auto-generada, limpia+dedup **20.075 chars / 3.591 palabras** (leída íntegra). Análisis: **19-sep-2026, 17:39 CEST** (`date`, RULE-012).

**Modelo (capa vendor / model card — NO reproducido en el lab):**
- **TokenRhythm/NeoHorse-1-4B**, post-entrenado desde **Qwen3.5-4B** (Apache 2.0, aviso de copyright de Alibaba conservado). Existe hermano **NeoHorse-1-9B** (base Qwen3.5-9B).
- Se presenta como **«initial prototype on the path toward recursive self-improvement (RSI)»**. Método declarado: **routing-guided agentic post-training** — un «routing harness» reparte tareas entre un pool heterogéneo de modelos, registra interacciones y resultados de herramientas, estima la demanda de capacidad y **realimenta la mezcla de entrenamiento** (curriculum SFT + on-policy distillation), con deduplicación, descontaminación y evaluación semántica de 6 dimensiones.
- Contexto **262.144 nativo** (extensible a 1.010.000). GGUF sin MTP draft head, con chat template: BF16 8,42 GB · Q8_0 4,48 GB · Q5_K_M 3,07 GB · **Q4_K_M 2,71 GB**.
- Benchmarks declarados (10 pruebas, contra Qwen3.5-4B, Gemma-4-E4B-it, Nanbeige-4.2-3B, Agents-A1-4B, Spark-X2.5-4B): **macro 64,87 vs 58,94 del base (+5,93)**; mayores subidas en VitaBench (+10,50), WorkBuddy Bench (+9,79), HumanEval (+9,75), QwenClawBench (+6,21); tau2-Bench **88,46** (mejor del grupo).

**Lo medido por Nichonauta (RTX 3060 12 GB, Q4_K_M = 2,71 GB):**
- Config: 262K de contexto con **KV cache Q8** → **8,2 GB de VRAM**, **76 tok/s**. Parámetros que muestra: `temp 1.0 · top_p 0.95 · top_k 20 · min_p 0.0 · presence_penalty 1.5 · repetition_penalty 1.0`. **Sin MTP** → el flag de decodificación especulativa falla; la GPU calienta más sin él.
- **Chat:** la cadena de razonamiento es **más corta** y las respuestas finales más cortas → «perdió mucho de modelo asistencial/chat» frente al original.
- **Código one-shot** (landing, calculadora, reloj, simulador de fluidos): estilo de código distinto, pero **el JavaScript nunca queda conectado con el resto** en los cuatro casos (calculadora sin resultado ni historial, reloj sin manecillas, fluidos que no se dibujan).
- **Agéntico (OpenCode, MCPs desactivados para no inflar el contexto):** «por lo menos el uso de la herramienta no está roto» y el JS funcionó por primera vez; la sesión consumió **más de 40.000 tokens**. Al pedirle «analiza todos los errores y corrígelo», reescribió el archivo y quedó **igual** (solo centró unos números) → **iteración de corrección = tiempo perdido**.
- **Veredicto (verbatim, limpio):** «En ninguna de las pruebas lo vi mejor que el modelo original. Por lo menos a mí me sigue funcionando mejor el modelo original.»

## 🔴 Mapeo contra el lab

| Aspecto | Veredicto |
|---|---|
| ¿Aporta al lab como modelo? | **NO.** El lab ya cubre el tramo 4B: LFM 2.6B (interactivo) y gpt-oss-20b (razonamiento/batch). Un 4B que «no mejora al Qwen 3.5 4B» no entra. |
| 2,71 GB en Q4_K_M, 8,2 GB con 262K + KV Q8 | ✅ Confirma la técnica ya registrada: **KV cache Q8 = mitad de VRAM** sin degradar apenas (analizado el 24-ago y el 20-ago). |
| Claim del vendor **+5,93 macro** vs prueba práctica | **CONTRADICCIÓN directa.** Refuerza la lección ya asumida por el lab («probar, no fiarse de benchmarks», midudev 20-ago) y valida la batería de PRODUCCIÓN del lab frente a benchmarks sintéticos. |
| Concepto **RSI / routing-guided post-training** | **NUEVO como idea**, no como herramienta: usar un pool de modelos para medir la *demanda de capacidad* de cada tarea y reorientar los datos de entrenamiento. Es materia de arquitectura, sin acción hoy. |
| Coste real de la sesión agéntica | **40.000+ tokens** para una tarea de landing → mismo eje de medida que el caso Bonsai: tokens y minutos por tarea, no tok/s. |

## Veredicto: **VALOR BAJO — validación + un concepto, sin entrada como futurible**

1. **NO se da entrada al modelo**: prueba práctica negativa (no mejora al base), y el tramo 4B del lab ya está cubierto.
2. **Sí queda registrado** por dos motivos: (a) es un caso limpio de **claim de vendor (+5,93) desmentido por prueba real** — material directo para el criterio del lab de no publicar cifras sin fuente y de medir con la batería de producción; (b) introduce el concepto **RSI / routing-guided curriculum**, que el lab no tenía nominado.
3. **Sin acción.** No se descarga (2,71 GB) ni se prueba.

*Nota honesta: transcripción auto-generada con deformaciones («Neohorse 14B» = NeoHorse-1-4B; «Qen» = Qwen; «Gema 4E4B» = Gemma-4-E4B-it; «Agents A1» = Agents-A1-4B; «Nan Big 4.2» = Nanbeige-4.2-3B; «Spark X 2.5» = Spark-X2.5-4B). La descripción del propio canal dice «Qwen 2.5 4B» mientras el título y la model card dicen **Qwen3.5-4B** — se resuelve a favor de la model card de HF. Benchmarks del vendor: cifras declaradas, no reproducidas.*
