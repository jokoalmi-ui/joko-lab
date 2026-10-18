---
title: "Análisis — @datastreakofficial: infografía «AI Agent vs AI Workflow» (17-oct-2026)"
type: research
---

# Análisis — @datastreakofficial: «AI Agent vs AI Workflow»

**VERACIDAD:** [VERIFICADO] — datos leídos del JSON embebido de la página y de la imagen descargada; transcripción literal por OCR (GLM-4.6V-Flash).

**Fuente:** https://www.instagram.com/p/DemBa3VBeZ8/ (shortcode `DemBa3VBeZ8`)
**Autor:** @datastreakofficial (verificada, «DataStreak») — canal **NO vigilado**
**Fecha del post:** 17-oct-2026 13:40 CEST · **Métricas:** 20 me gusta / 0 comentarios
**Etiqueta de Instagram:** «Contenido generado con IA» (`ai_label_info.attribution_label_text`)
**Formato:** **una sola imagen**, `media_type 1`, 1440×1470. NO es carrusel: el JSON de la página incluye un feed lateral (`polaris_ordered_timeline_connection`) con carruseles de 6/10/13 láminas que son otros posts — dato que se presta a confusión si se lee sin filtrar.
**Método:** navegador (sesión local) → `og:*` + script `ScheduledServerJS` a `/tmp/ig_dem_embedded.json` → parseo con Python (objeto `xig_polaris_media.if_not_gated_logged_out`) → imagen full-size recuperada con `fetch` desde la pestaña (el CDN da 403 fuera del navegador) → OCR/estructura con GLM (`lms load glm-4.6v-flash --context-length 32768`) → VRAM devuelta a su estado previo (gpt-oss-20b, 8.876/12.282 MiB).

## Contenido de la infografía (transcripción)

- **Título:** AI Agent vs. AI Workflow.
- **Subtítulo:** los agentes deciden y actúan de forma autónoma; los workflows siguen pasos predefinidos para completar la tarea de forma fiable.
- **1 Concepto** — Agente: sistema que percibe, razona, decide y usa herramientas hacia un objetivo de forma autónoma. Workflow: secuencia predefinida de pasos donde LLM o herramientas se ejecutan en orden fijo.
- **2 Arquitectura** — Agente: `User Goal` → `AI Agent (Planner + Reasoner)` con `Memory (corto/largo plazo)` y `Tools` (APIs, bases de datos, código/CLI, búsqueda web). Workflow: `Workflow Orchestrator (LangChain, Airflow, Step Functions)` → `Step 1..N` → `Output`.
- **3 Execution flow** — Agente: `Percibir → Planificar → Actuar → Observar` (bucle). Workflow: `Trigger → Paso 1 → Paso 2 → Paso N → Salida final`.
- **4 Runtime** — Agentes: LangChain, LangGraph, AutoGen, CrewAI (estado, memoria, acceso a herramientas, autonomía). Workflows: LangChain (Chains), Apache Airflow, AWS Step Functions, Prefect (pasos fijos, determinista, reintentos, planificación).
- **Rule of thumb:** agente si la tarea es compleja, abierta y exige decidir y usar herramientas.
- **Together:** workflow para la estructura, agente para las decisiones dinámicas; combinarlos da sistemas potentes y fiables.

## Origen del marco

Reempaqueta la taxonomía de **Anthropic, «Building effective agents» (19-dic-2024)**: *workflows = LLMs y herramientas orquestados mediante rutas de código predefinidas; agentes = el LLM dirige su propio proceso y el uso de herramientas*. La conclusión híbrida («Together») también es la de Anthropic.

## Aciertos

- La distinción de fondo es correcta: **quién controla el flujo** (código vs modelo).
- El bucle coincide con ReAct (`pensar → actuar → observar`).
- El consejo híbrido es el correcto para producción.

## Errores e imprecisiones (cotejado con Anthropic 2024 y con el estado 2026)

1. **«Deterministic» mal aplicado:** un paso ejecutado por un LLM no es determinista (temperatura, versión del modelo, prompt). Lo determinista es el **grafo de control**, no el paso.
2. **Orquestadores de datos metidos como «workflow LLM»:** Airflow, Prefect y Step Functions son planificadores de DAG (ETL), no frameworks de orquestación de LLM.
3. **«LangChain (Chains)» desfasado como runtime:** las chains clásicas quedaron en segundo plano; lo que hoy se usa para grafos es LangGraph, que la propia lámina coloca en la columna de agentes.
4. **Falta lo que decide en producción:** coste y latencia por paso, tope de iteraciones y condición de parada, permisos e idempotencia de herramientas, trazas, evaluación y aprobación humana en acciones irreversibles.
5. **Falta el consejo central de Anthropic:** empezar por lo simple; muchas veces una llamada con buen contexto basta.
6. **Memoria como caja obligatoria** cuando es una decisión de producto, no un default.

## Cruce con el LAB

- El lab **es el caso «Together» real**: cron y n8n aportan el grafo determinista; Hermes aporta el bucle; los tools van con mínimo privilegio, gate de veracidad y RULE-021.
- Ya documentado y más fino en el propio lab:
  - `research/analisis-agentic-ai-handbook.md` — espectro de autonomía (script/RPA → chatbot → tool-calling → agentic workflow → multi-agente).
  - `research/infografias/serie-ia-agentes/leccion-3-el-agente-el-bucle/` — el bucle, ReAct, memoria corto/largo plazo.
  - `research/analisis-managed-agents-anthropic-2026-09-17.md` — principio «separar cerebro (bucle) de manos (ejecución de herramientas)», que esta lámina no recoge.

## Veredicto (17-oct-2026)

**No aporta nada que mejore el LAB.** Sin técnica, patrón, herramienta ni dato nuevos; sin medición alguna. Coste real: minutos de GPU (descarga + OCR), cero escrituras en el sistema, VRAM restaurada.

**Único residuo con valor potencial —para marca, no para el sistema:** una pieza «workflow o agente: cómo decidir», con criterio y umbrales medidos (coste por tarea resuelta, pasos por tarea, latencia). No existe hoy como entrega propia en la serie de LinkedIn ni en el material del TFM. No se ha creado: a la espera de decisión del usuario.
