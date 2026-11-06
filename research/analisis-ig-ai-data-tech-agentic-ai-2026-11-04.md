# Análisis — póster «Agentic AI: A Complete Framework» (@ai.data.tech)

**VERACIDAD:** [VERIFICADO] — texto de la imagen transcrito del JPEG original (1216×1296, descargado del CDN de Instagram); metadatos leídos de `og:title`/`og:description` y del JSON embebido. El contenido del póster es **una lista de conceptos sin fuente**, no un hallazgo verificado: aquí se archiva como referencia, no como conocimiento validado.
**Fecha del análisis:** 2026-11-04 17:32 CET (`date`).
**Disparador:** `https://www.instagram.com/p/DfU3z1-u7fb/` — `@ai.data.tech`, publicado 2026-11-04 (~17:20 CET), 0 comentarios, etiquetado por Instagram como **«Contenido generado con IA»**.
**Método:** navegador → `og:title`/`og:description` + extracción de `candidates` del JSON embebido → descarga única (`t51.82787-15`, variante `stp=dst-jpg_e35_tt6`) → transcripción visual completa. **No se ha ejecutado nada más**: es verificación documental, no medición.
**Estado previo:** el shortcode `DfU3z1-u7fb` no aparecía en ningún fichero de `joko-lab` → post nuevo, no re-analizado.

## Qué es

**Una sola imagen**, no un carrusel: 16 URLs `t51.82787-15` en el HTML son variantes de tamaño del mismo archivo. Póster con 5 anillos concéntricos y ~52 etiquetas:

1. **AI & ML** — «Turn your data into decisions»: NLP, razonamiento, supervisado, refuerzo, no supervisado.
2. **Deep Learning** — atención, transfer learning, LLMs, DBN, RNN/LSTM, transformers, CNN.
3. **Gen AI** — «Create New Content»: personalización, multimodal, mitigación de alucinaciones, tool use, prompt engineering, RAG, TTS/ASR, audio, vídeo, imagen, código, runtimes, validación de salida.
4. **AI Agents** — «Autonomous Tasks»: descomposición de objetivos, orquestación de tools, gestión de contexto, human-in-the-loop, memoria corto/largo plazo, autorreflexión, ejecución autónoma.
5. **Agentic AI** — «Automate entire processes»: 20 etiquetas (planificación ReAct/CoT/ToT, coordinación multi-agente, state persistence, rollback, observabilidad y tracing, guardrails, gestión de coste, protocolo de delegación, recuperación de fallos, marketplaces de agentes…).

Cuatro bloques laterales (Key Technologies, Agent Capabilities, Agent Management, Outputs & Interfaces, Governance & Future) que **solo llevan rótulo, sin viñetas**: están vacíos en la imagen.

## Veredicto

**Referencia, no material de trabajo.** Cero técnica, cero repo, cero cifra, cero fuente. El título («A Complete Framework») promete un marco y entrega una taxonomía dibujada por IA: no define ninguno de los 20 conceptos ni dice cómo se implementa.

Lo único aprovechable es su uso como **checklist de auditoría** del lab, y el resultado de ese cruce es que el póster presenta como «futuro» cosas que aquí llevan meses funcionando.

## Cruce con el lab — los 3 huecos reales

| Etiqueta del póster | Estado en el lab | Evidencia |
|---|---|---|
| Multi-agente, delegación, handoff | **Cubierto** | `graph-lab`, `delegacion-subagentes` |
| Observabilidad y tracing | **Cubierto** | `observabilidad-pipeline`, `observabilidad-pipeline-llm` |
| Guardrails, mínimo privilegio, veracidad | **Cubierto** | `least-privilege-lab`, `gate-veracidad`, `avisos-con-acuse-lab` |
| Planificación (ReAct/CoT/ToT) | **Cubierto** | `plan`, `grill-idea`, `refactor-seguro` |
| State persistence | **Cubierto** | `state.db`, `recuperacion-state-db`, `state-verification-pattern` |
| **Rollback / replanificación** | **Hueco** | `joko-git-recibos` protege commits, pero no existe mecanismo para deshacer una tarea del agente a mitad |
| **Gobierno y retención de memoria** | **Hueco** | hay poda manual de `MEMORY.md`; no hay política con fechas ni caducidad automática |
| **Coste/recursos por tarea** | **Hueco parcial** | el criterio ventana barata/cara vive en memoria y en `ai-router`, pero no hay contador de gasto por ejecución |

Los tres huecos no se abren aquí: quedan anotados como candidatos a HYP, no como deuda aceptada.

## Qué NO es

- No es un framework pese al título: es una infografía.
- No cita fuentes ni autores; la cuenta está marcada por Instagram como generadora de contenido con IA.
- No aporta nada conceptual nuevo al lab: 52 etiquetas, todas ya usadas aquí con implementación real detrás.
- No sirve como material de entrevista ni como guion: no hay explicación que reutilizar.

## Ficheros

- Imagen original preservada: `research/analisis-ig-DfU3z1-u7fb/post-1216x1296.jpg` (525.474 bytes) — misma convención que `analisis-ig-DfPvtS7iIZ0/`.
- Este documento: `research/analisis-ig-ai-data-tech-agentic-ai-2026-11-04.md`.
- Copia temporal de trabajo: `/tmp/ig_post_big.jpg` (se puede borrar).
