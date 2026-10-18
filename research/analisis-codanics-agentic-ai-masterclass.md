---
title: "Análisis — LLMs & Agentic AI Masterclass: RAG, Skills, MCP & Loop Engineering (Codanics, 23-ago-2026)"
type: research
---

# Análisis — LLMs & Agentic AI Masterclass: RAG, Skills, MCP & Loop Engineering (Codanics, 23-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=KchhsWO1zpU (Codanics, 13-07-2026, 1:13:35, 2.230 views)
**Método:** subtítulos EN (ES dio 429 ×2 → EN 561 KB) → deduplicados (179K→77K chars) → análisis de secciones temáticas
**Nota honesta:** canal con acento fuerte y transcripción ASR ruidosa; el análisis se basa en el contenido técnico extraído, no en transcripción literal perfecta.

## El vídeo en 1 párrafo

Masterclass de Codanics sobre los **3 building blocks de la IA agéntica** (RAG, Skills, MCP) + **Loop Engineering**. La tesis central: la era de los chatbots simples terminó; en 2026 el foco es que los agentes no solo hablen, sino que **hagan cosas** — y eso se construye con esos 3 bloques + bucles autónomos.

## Los 3 building blocks (según el vídeo)

| Bloque | Qué es | Dato clave |
|---|---|---|
| **RAG** | Contexto + prompt → LLM → respuesta basada en el documento (no en la memoria del modelo) | Reduce **alucinaciones**; ratio ~20% memoria del modelo / ~80% del documento; **privacidad**: datos privados sin filtrar al modelo — "must be local" |
| **Skills** | Capacidades accionables que se añaden al LLM | Habilidad + acción; el nivel del resultado sube ("Babar Azam" como analogía de nivel superior) |
| **MCP** | Model Context Protocol — protocolo estándar para conectar herramientas | 68 menciones en el vídeo; es el conector estándar entre LLM y herramientas |

## Loop Engineering (la parte más valiosa)

**Define**: reemplaza el ciclo manual *type-read-check* (escribir → ver error → volver a preguntar → repetir 100×) por un **sistema autónomo**:

```
Agente → ejecuta en terminal → error → vuelve al LLM → corrige → re-ejecuta
→ otro agente maneja el error → bucle hasta que el código pasa sin errores
```

**Pilares del loop**:
1. **Automatización con termination goals** — metas claras y finitas (ej: "pasar todos los unit tests", no "hasta que me parezca bien")
2. **Agentes observan resultados e iteran de forma independiente** — hasta que el objetivo se cumple
3. **Reflect & revise** — el agente se revisa a sí mismo en cada vuelta

**Conclusión del vídeo sobre el empleo**: el rol de *data scientist* está migrando a **AI Engineer** (integración de modelos, pipelines, loop engineering, despliegue) — el que combine método científico + dominio + IA tiene el potencial.

## Mapeo contra el LAB — 🔴 VALIDACIÓN FUERTE

| Componente del vídeo | En el lab |
|---|---|
| RAG local con privacidad | ✅ **EXACTO**: LanceDB + reranker + BGE-M3, 100% local, "must be local" es literalmente el diseño del lab |
| Skills accionables | ✅ Sistema de skills de Hermes (40+ skills, bundles) |
| MCP | ✅ 3 MCPs en producción (lab-db, lancedb, animation-server) |
| Loop engineering (termination goals) | ✅ **Gate de veracidad + revisor + verificar_research** = el lab YA itera con objetivos finitos (esperar "Procesados: 1 \| Fallos: 0") |
| Agente que re-ejecuta hasta pasar tests | ✅ TDD + suite 219 tests + refactor-seguro |

## Veredicto: VALOR MEDIO-ALTO (validación del stack completo)

1. **El lab implementa el 100% de lo que el vídeo enseña** — y con más profundidad (el lab tiene gate de veracidad que el vídeo ni menciona; el vídeo es de nivel introductorio-medio).
2. **El concepto "termination goals" valida la regla del lab**: "no describir como completado sin salida real de verificación" — es literalmente un termination goal.
3. **Sin futuribles nuevos** — es un masterclass para quien empieza; el lab está por encima en todo.
4. **Único dato reutilizable**: la frase del cierre sobre empleo ("de data scientist a AI engineer") sirve como material para LinkedIn Lab / TFM (vocabulario de la transición profesional del usuario).

**Sin acción**. Registrado como validación del diseño del lab (RAG local + skills + MCP + loops con objetivos finitos = la arquitectura que la industria enseña).
