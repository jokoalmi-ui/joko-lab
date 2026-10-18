---
title: "Análisis — \"AI Model vs Agentic Harness: What Actually Drives AI\" (IBM Technology, 25-ago-2026)"
type: research
---

# Análisis — "AI Model vs Agentic Harness: What Actually Drives AI" (IBM Technology, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/ZELPNFXJ4_o (IBM Technology, 8.5 min, 5.880 views — canal de referencia del lab)
**Método:** metadatos + subtítulos EN (ES dio 429 → fallback EN validado; 65 KB → 6.9K chars limpios, lectura completa)

## Qué dice el vídeo (concepto didáctico de IBM)

La distinción **modelo vs harness** (arnés agéntico):

1. **AI model** = la red neuronal ("cerebro en un tarro"). Solo, no puede abrir archivos, ejecutar código ni navegar.
2. **Agentic harness** = lo que envuelve al cerebro: **herramientas + memoria + bucle agéntico**.
3. **AI agent** = modelo + harness juntos.

### Los 3 componentes del harness
- **Tools**: acceso a archivos, ejecutar código (sandbox), internet, computer use (mover cursor), línea de comandos, y **MCP** para servicios externos (estándar que permite plug-and-play entre harnesses).
- **Memory**: context window = memoria de trabajo (se borra al terminar); el harness persiste con: archivos de instrucción (AGENTS.md en el proyecto, cargado al inicio), **compactación de contexto** (resumir lo anterior, podar outputs redundantes), y **búsqueda selectiva** (grep/semántica/código — no volcar todo el repo).
- **Agentic loop**: plan → acción → observar → repetir (segundos u horas). Los harnesses modernos añaden **verificación continua**: tests en marcha, screenshots, y a veces **un segundo modelo como revisor**.

### La tesis
- Los gaps entre modelos top se han estrechado a pocos puntos → **la mayoría de las ganancias recientes vienen del harness, no del modelo**.
- La pregunta útil no es "¿es buena la IA para X?" sino "¿**qué modelo** + **qué harness**?"
- La línea es fluida: capacidades que vivían en el harness (planificación de largo horizonte, auto-verificación) se están entrenando directamente en los modelos, y viceversa.

## 🔴 Aplicación al LAB — VALOR ALTO (validación directa del diseño)

| Concepto de IBM | En el lab |
|---|---|
| **Modelo = cerebro en tarro** | ✅ El lab distingue modelos (gpt-oss, GLM, LFM, r1-14b) del agente |
| **Harness = tools + memoria + loop** | ✅ **Hermes ES el harness**: tools (80), memoria persistente (MEP-001, Obsidian), bucle agéntico |
| **AGENTS.md / instrucciones persistentes** | ✅ Skills + memoria + contexto de proyecto |
| **Compactación de contexto** | ✅ El lab la usa (skills de compactación, contexto selectivo) |
| **Búsqueda selectiva** | ✅ RAG LanceDB 21.975 fragmentos (recall 100%) + search.py |
| **MCP como estándar** | ✅ 3 MCPs conectados (animation, lab-db, lancedb) + futuribles (n8n, Gemini Notebook) |
| **Verificación continua con segundo modelo** | ✅ **LLM-as-judge** (n_juicios=3, robusto desde ayer) + evaluar_rag + batería 5x5 |
| **Los gaps de modelo importan poco** | ✅ El lab eligió modelos por VRAM/contexto, no por benchmark — validado |

**Veredicto**: VALOR ALTO como **validación externa del diseño del lab** — IBM explica formalmente lo que el lab construyó empíricamente. Hermes ya es un harness completo: herramientas + memoria + loop + verificación con juez.

**Usos adicionales**:
- **Material TFM/LinkedIn**: la distinción modelo/harness es un marco conceptual excelente para explicar el lab.
- **Para el usuario**: explica por qué "el mismo modelo" rinde distinto según el harness — relevante al evaluar modelos locales (el harness LM Studio vs Ollama vs Hermes cambia el resultado).

## Conclusión
VALOR ALTO: validación directa y formal del diseño del lab (Hermes = harness completo). Sin futuribles nuevos — refuerza las decisiones ya tomadas (MCP, LLM-as-judge, RAG selectivo, memoria persistente). Ningún cambio de stack.
