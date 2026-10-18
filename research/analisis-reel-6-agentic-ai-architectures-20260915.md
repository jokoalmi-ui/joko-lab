# Análisis del reel «6 Agentic AI Architectures» (@ai.data.tech) — 2026-09-15
**VERACIDAD:** [VERIFICADO]

Fuente: https://www.instagram.com/reel/DdKHNTOlCSg/
Autor: cuenta **ai.data.tech** (nombre mostrado «Data Science Hub»). Publicado **11-sep-2026**.
Tipo: reel vertical 720×1280 · **10,12 s** · 622.799 B. **Audio sin voz** (crédito de plantilla
«Subtítulos en español de Amara.org») → el contenido está SOLO en la imagen.
Método: descarga del MP4 desde `video_versions` del JSON embebido → frames a 1 fps (10) →
análisis con **GLM-4.6V** (LM Studio :1234) → 2 pases (texto literal + diseño).
Ficheros: `research/reel-DdKHNTOlCSg/reel.mp4`, `frame_01..10.jpg`, `reel_transcripcion.txt`.

## Contenido literal (transcrito por visión, no inventado)

Título de la pieza: **«6 Agentic AI Architectures — From Chatbot To Enterprise Agent»**.
Cada nivel añade UN componente (escalera):

1. **Level 01 · Simple Chatbot** (+1 Component)
   User → Prompt → LLM API (System Prompt + User Query) → Response → Answer
   *No memory · no tools · no data.* Tools citadas: Claude, GPT-4o, Gemini.
2. **Level 02 · RAG Application** (+ Data Layer)
   Ingestion (offline) → Embed Query → Vector DB (Top-K semantic match) → Reranker (best chunks) →
   Context → LLM (grounded answer + citations). Tools: Pinecone, Qdrant, LangChain, Cohere.
3. **Level 03 · Single AI Agent** (+ Reasoning Loop)
   User Goal → Planner (break goal → steps) → Think (LLM reasoning + tool selection) → Act
   (web search / code runner) → Memory (session + long-term). Tools: Claude Code, LangChain, OpenAI SDK.
4. **Level 04 · Multi-Agent System** (+ Orchestration)
   User Task → Orchestrator (decompose, routes, RBAC, rate limits) → Delegate → Coder (code runner) /
   Reviewer (critique loop) → Shared State (message bus + shared memory) → Merge/Aggregator.
5. **Level 05 · Autonomous Workflow** (+ Self-Correction)
   Triggers (webhook / event / cron) → Planner (DAG + task queue) → Executor (parallel runs) →
   Validator (checks output) → **HITL Gate (approve/reject)** → Output (notify + log); fail → retry.
6. **Level 06 · Enterprise AI Agent** (+ Governance)
   SSO → AI Gateway (guardrails: PII filter, prompt-injection defense) → Routes → Agent Runtime
   (multi-agent orchestration + model router) → Ground → **MCP Connectors** (CRM/ERP) →
   Memory store (per tenant) → Cost tracking → Audit logs → Observability → Evals → feedback loop.

## Diseño (para replicar formato)

- **Colores:** una franja/color por nivel (verde oscuro, azul, morado, teal, celeste, morado claro);
  títulos grandes en negrita, texto de proceso en regular.
- **Layout:** lienzo vertical único (no carrusel). Cada nivel = una fila de 2 columnas:
  izquierda título + «+componente», derecha la cadena de cajas unidas por flechas.
- **Gráficos:** cajas con iconos (usuario, LLM, vector DB), flechas entre pasos, logos de herramientas.
- **Densidad:** alta en las cadenas de proceso, baja en la columna izquierda.
- **Formato de consumo:** el reel es un scroll vertical sobre ese lienzo (10 s) → en LinkedIn el
  equivalente es **un documento/PDF vertical o una imagen alta**, no un carrusel de slides.

## Comparación con NUESTRO curso (6 niveles)

| Nuestro nivel | Equivalente en el reel |
|---|---|
| 0 Fundamentos | Level 01 (Simple Chatbot) |
| 1 Instrucciones / prompting | **no aparece como nivel** (el prompt vive dentro del Level 01) |
| 2 Datos y herramientas (RAG, tools, MCP, CoT) | Level 02 (RAG) + parte del 03 (tools) |
| 3 El agente: el bucle (ReAct, memoria) | Level 03 (Single AI Agent, + Reasoning Loop) |
| 4 De uno a muchos | Level 04 (Multi-Agent System) |
| 5 Producción (evals, verificación, permisos, coste) | **se divide en dos**: Level 05 (autonomía + HITL) y Level 06 (gobernanza empresarial) |

Coincide en el eje chatbot → RAG → agente → multiagente → producción. Dos diferencias reales:
1. El reel es una escalera de **arquitecturas** (lo que el sistema *tiene*); el nuestro, de
   **capacidades/aprendizaje** (lo que tú *sabes hacer*). Complementarios, no intercambiables.
2. El reel separa la producción en dos niveles (autonomía y gobernanza) y no dedica nivel al prompt;
   nosotros al revés (el prompt sí es un nivel y la producción va en uno).

## Lo que merece la pena copiar

- **La escalera «+1 componente»**: cada nivel añade UNA pieza y se ve en el dibujo. Recurso didáctico
  fuerte y barato de aplicar a nuestra serie.
- **Un color por nivel** como sistema visual de la serie (identidad reconocible entre piezas).
- **La pieza vertical única** cuando el tema es un mapa completo (frente a 7 slides).
- **Recorrido guiado**: el reel enseña el mapa haciendo scroll; en una imagen fija se sustituye por
  numeración clara y un orden de lectura evidente.

## Pendientes / límites

- Reel descargado y analizado; **no se ha publicado ni replicado nada**.
- El nombre de la cuenta aparece como `ai.data.tech` en og:description y «Data Science Hub» en og:title:
  cuenta con dos etiquetas; no verificado cuál es el handle exacto.
- No se han consultado métricas del post (likes/comentarios): no disponibles sin sesión.
- Si se replica como infografía: aplica la regla del lab (arte con ComfyUI/SDXL, no degradar).


---

## ANOTACIÓN 2026-09-15 18:01 CEST — ¿válida para las infografías? ¿útil para el LAB?

### 1) Veredicto para las infografías de LinkedIn: **VÁLIDA**

- El formato del reel es una extensión directa de nuestro sistema de paneles (estilo MAURYS), no otra cosa.
- Se adopta: (a) la etiqueta **«+1 componente»** por nivel, (b) **un color por nivel** como identidad de la serie,
  (c) **pieza vertical única** cuando el tema es un mapa completo (en LinkedIn: documento/PDF vertical o imagen alta).
- No se copia el texto ni las herramientas citadas: se reescribe con el stack real del lab (Ollama, LM Studio,
  n8n, LanceDB, MCP) y, si se maqueta como infografía, el arte va con ComfyUI/SDXL (regla del lab: no degradar).

### 2) ¿Hay algo útil para el LAB? Sí — verificado contra el lab, no supuesto

**CONFIRMA lo que ya está montado** (el mapa de 6 niveles coincide con piezas existentes):
- Level 05 (validación + puerta humana + reintento) ≈ `04-operations/metrics/operations_ledger.jsonl`, cuyos campos
  son exactamente `operation_id, required_gates, executed_gates, bypass, exemption, result` → el lab ya registra
  la puerta humana como caja del flujo. También: gate-veracidad, juez de alucinaciones.
- Level 06 (model router) ≈ `local_cloud_ledger.jsonl` (`escalo_cloud`, `motivo`, `intento_local`) = ai-router;
  (conectores) ≈ MCP lab-db / lancedb / animation-server; (guardrails/permisos) ≈ least-privilege-lab;
  (evals) ≈ alucinaciones_ledger + llm_judge_veredictos.db. Son 16 ledgers en `metrics/`.

**HUECO real detectado (2, ninguno inventado):**
1. **Coste por ejecución**: `local_cloud_ledger.jsonl` guarda `latencia_s` pero **ningún campo de coste ni tokens**.
   Es el único eje del Level 06 que el lab no mide, y es justo el que decide si compensa escalar a cloud.
2. **Reranker en el RAG**: no hay script de reranker en `tools/` (solo aparece en informes de agosto: 
   `2026-08-05-analisis-rag-atareado.txt`). El Level 02 lo lista como la pieza que separa recuperar de responder bien.

**OPORTUNIDAD (negocio, no técnica):** la escalera de 6 niveles es un **catálogo de servicios** listo para
`despliegue-ia-local-clientes`: permite decir al cliente «estás en el nivel N» y vender el salto al N+1.
El lab tiene piezas hasta el 5-6 pero no las presenta como oferta escalonada.

### 3) Estado

Anotado el 2026-09-15. **Nada replicado, nada publicado, ningún cambio en el lab.** Los dos huecos quedan como
candidatos (OBS), sin abrir experimento ni tocar código.


═══════════════════════════════════════════════
CORRECCION 2026-09-15 2026-09-15 18:15 CEST
═══════════════════════════════════════════════
Este informe decia, en su apartado de huecos del LAB, que el lab NO tiene
reranker. Es FALSO. Verificado el 2026-09-15 con salida real:

  - tools/reranker_daemon.py existe (CrossEncoder, BAAI/bge-reranker-v2-m3).
  - Esta ACTIVO: LISTEN 127.0.0.1:8765 (python3, pid 2526).
  - tools/rag_telemetry.py mide el paso (campo rerank_s).
  - El informe 2026-08-05-analisis-rag-atareado.txt (l. 31 y 89) ya lo describe
    como pieza del lab: "Embedding + reranker (BGE-M3 cross-encoder)".
  - Hay evaluacion formal: tools/evaluar_rag.py -> recall@5 100% con 8 consultas
    (12-ago, OP-007) + tools/evaluar_rag_adversarial.py (18-ago).

Causa del error: el grep de comprobacion se trunco con head, los .py quedaron
fuera de la salida y se concluyo una ausencia sin ver la lista completa.

Lo que SI queda en pie, ya con otra forma:
  - COSTE: sigue faltando, matizado y con evidencia -> OBS-104
    (el ledger del router no guarda coste ni tokens; el orquestador solo tiene
    "coste_estimado" como texto de consola; los tokens si estan en
    pipeline_obs.jsonl pero sin precio).
  - RERANKER: el hueco no es "no existe" sino "no es medible hoy" -> OBS-105
    (recall@5 100% con 8 consultas = metrica saturada, no discrimina con/sin
    reranker).

Registrado en:
  01-knowledge/observations/OBS-104-coste-no-unido-al-escalado-2026-09-15.md
  01-knowledge/observations/OBS-105-metrica-rag-saturada-y-reranker-2026-09-15.md
  01-knowledge/hypotheses/HYP-002-coste-por-ejecucion-y-escalado-local-cloud.md
  01-knowledge/hypotheses/HYP-003-aporte-del-reranker-hoy-no-medible.md
