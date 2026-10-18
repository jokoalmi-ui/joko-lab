---
title: "Investigación — Orquestación de agentes: nivel más alto de Emowe, qué dice la industria y hasta dónde en el LAB"
type: research
---

# Investigación — Orquestación de agentes: nivel más alto de Emowe, qué dice la industria y hasta dónde en el LAB
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 2026-09-01 22:10 CEST (verificada con `date`)
**Petición del usuario:** investigar el nivel más alto del marco de Emowe (Marcos) — la orquestación de agentes — en foros de expertos, y determinar hasta dónde implementar en el LAB.

## 1. El marco de Emowe (nivel 4, de la transcripción de hoy)

Emowe describe el nivel 4 como: **equipo de agentes sincronizados** con arneses distintos (Claude Code, Hermes, Antigravity), cada agente con modelos distintos según tarea (Opus potente, Haiku sencillo, IA local por seguridad), y una **jerarquía**: trabajadores (agentes atómicos que ejecutan tareas) → directores (descomponen proyectos en tareas) → CEOs (visión del negocio descompuesta en proyectos).

## 2. Qué dice la industria (foros de expertos + artículos técnicos, verificado 01-sep)

### 2.1 r/LocalLLaMA — el "dispatch gap" (3 hilos reales)

**Hilo A — "the hardest part isn't the agents, it's coordinating them"** (autor con 3 agentes nocturnos → 19 workflows en producción):
- **El problema real NO son los agentes, es la coordinación.** Pasaron de 3 agentes especializados (cada uno bueno en lo suyo, 62%→86% de éxito) a 19 workflows y "el problema de coordinación EMPEORÓ"; tuvieron que construir **una capa de dispatch** para gestionar quién hace qué y dónde está cada agente.
- Comentarios clave:
  - *"los agentes son fáciles, hacer que hablen entre sí sin caos es la pesadilla"*
  - **Contra-opinión (OpenTulpa, 5B+ tokens/mes):** *"no necesitas múltiples agentes; necesitas UN agente persistente"* — un solo agente fuerte con estado puede cubrir el trabajo de muchos (mismo tema que gpt-oss interleaved thinking abajo).
  - *"Routing es solo la mitad del problema. Pub/sub resuelve 'quién habla con quién', pero no 'qué ya está comprometido'. Lo que funcionó: hacer cada paso durable con execution_id + estado por paso, separando resume de replay."* ← **exactamente el modelo del kanban nativo (estado en SQLite).**
  - *"Los agentes no necesitan conocerse entre sí"* (analogía del supermercado) — el sistema nativo coordina; los agentes solo trabajan contra el tablero/estado compartido.

**Hilo B — "local multi agent systems":**
- **gpt-oss-120b con interleaved thinking**: un solo modelo fuerte que hace tool calls ENTRE pensamientos "se siente como multi-agente" sin serlo — la frontera entre mono y multi-agente es difusa; un agente potente puede bastar.
- **voratiq** (OSS): orquestador para ejecutar agentes de código EN PARALELO sobre la misma tarea (que "compitan").
- Patrón repetido: los que de verdad ejecutan en paralelo hacen **scraping/hypothesis exploration**, no "chats entre agentes".

**Hilo C — "is everyone just running a bunch of terminals?":**
- **El estado del arte real = 6 terminales de Claude Code abiertas**, cambiando entre ellas a mano. Las UIs vistosas ("agentes que aparecen como personajes de videojuego") no son útiles en producción.
- Lo que SÍ funciona (comentarios de producción):
  - **un worktree/container por tarea** + resumen de archivos tocados + log de tests + nota "bloqueado/necesita humano" (el "packet" de la tarea)
  - **el coordinador es "solo una cola"** — no un cerebro
  - **GitLab self-hosted como plataforma de coordinación**: épicas/issues/tareas/milestones/**kanban**/git — los agentes como "equipo real"
  - **reviewability > número de agentes**: "sin ese packet, los agentes paralelos son solo trabajo de limpieza en paralelo"
  - orquestador principal que dispara workers como CI workflows (gitea) con logs OOB

### 2.2 Artículo técnico (glukhov.org, "Multi-Agent Orchestration Patterns: A Practical Guide")

**Dato duro: 40% de los pilots multi-agente fallan en 6 meses** — no porque no funcionen, sino porque eligen el patrón equivocado o no saben cómo se rompe.

**Los 6 patrones canónicos** (cada uno con cuándo usarlo/cómo falla/mitigación):

| Patrón | Cuándo | Cómo falla | Coste vs single |
|---|---|---|---|
| Orchestrator-Worker | Descomposición clara, especialistas | SPOF, context overflow ≥4 workers, coste 2-3x | 2-3x |
| Sequential Pipeline | Flujo fijo (documentos) | Error se propaga sin backtracking, +950ms overhead, 3x tokens | 3-4x |
| Fan-Out/Fan-In | Subtareas independientes paralelas | Rate limits colectivos, race conditions N(N-1)/2, **aggregation hallucination** (el sintetizador inventa consenso) | 4-5x |
| **Hierarchical** | **20+ agentes, multi-dominio** | Latencia acumulada (3 niveles = 6-12s min), pérdida de info entre niveles, ramas contradictorias | 3-5x |
| **Swarm** | Exploración, espacio de búsqueda desconocido | **Debugging nightmare** (sin control flow central), sin garantías transaccionales, condiciones de terminación | 2-10x |
| Mesh | Refinamiento colaborativo, pares | Conexiones N(N-1)/2, dependencias circulares, debugging no determinista | 3-6x |

**MAST Taxonomy (NeurIPS 2025, 1.600+ traces, 7 frameworks):** los fallos se reparten en **3 categorías de 33%**:
1. **Specification Ambiguity** — roles subespecificados → esquemas JSON/Pydantic, no lenguaje natural
2. **Coordination Breakdowns** — protocolos no estructurados → mensajes tipados, acuses, condiciones de terminación
3. **Verification Gaps** — nadie valida la salida de los agentes → **maker-checker pattern** (validador independiente)

**Decision framework:**
- Step 1: caracterizar el problema → patrón (tabla de arriba)
- Step 2: restricciones (latencia <2s → NO jerárquico/mesh; presupuesto → NO fan-out; debugging complejo → NO swarm/mesh)
- Step 3: **empezar single-agent** — escalar a multi-agente SOLO cuando la medición diga: (a) ventana de contexto insuficiente, (b) paralelismo real necesario, (c) especialización con mejora medible, (d) el coste single supera al multi. *"La mayoría sobre-arquitecta hacia multi-agente antes de agotar el single."*
- **Cost control**: modelos baratos para workers (el orquestador razona, los workers son baratos), presupuestos por agente, early termination, **prefix caching** (no recomputar system prompts), coste POR AGENTE.
- **Kanban-style dispatchers** como patrón de rate-limit/concurrencia para swarm self-hosted.

## 3. Contraste con el marco de Emowe

| Emowe (nivel 4) | Patrón real de la industria |
|---|---|
| CEOs (visión) → directores (proyectos→tareas) → trabajadores (tareas) | = **Hierarchical** (patrón 4) con orchestrator-worker en la base |
| "Agentes sincronizados entre sí" | Los expertos lo matizan: los agentes NO necesitan conocerse entre sí; se coordinan contra el ESTADO COMPARTIDO (tablero/cola), no hablándose |
| "Cada agente con su arnés y su modelo" | ✅ Correcto: orquestador con modelo potente, workers con modelos baratos (cost control estándar) |
| "IA local por seguridad" | ✅ Correcto y avanzado: los datos sensibles no salen (práctica recomendada en producción) |
| "El salto es mental, no técnico" | ⚠️ Parcial: la industria dice que el 40% de los pilots FALLAN — el salto es técnico en coordinación/verificación, no en crear el primer agente (eso sí es fácil: 1-2 h) |

**El marco de Emowe es válido como pedagogía, pero la industria coincide en que el problema REAL es el "dispatch gap"** (coordinación + durabilidad + verificación), no la jerarquía en sí.

## 4. Hasta dónde implementar en el LAB — VEREDICTO CON EVIDENCIA

### 🟢 YA IMPLEMENTADO (el lab ya es nivel 4 del marco, con evidencia)

| Capacidad del lab | Patrón industrial equivalente | Evidencia |
|---|---|---|
| **Kanban nativo de Hermes** (`hermes kanban`, SQLite, dispatcher) | Swarm con kanban-style dispatcher + coordinación por estado compartido | Piloto swarm 01-sep: **6/6 cards done** en ~15 min, 16 fuentes reales (14 HTTP 200), workers→verifier→synthesizer |
| **Verifier en el kanban** (gate pass) | Maker-checker pattern (verification gap del 33% de MAST) | Verifier independiente que valida antes de pasar a synthesizer |
| **Modelo cloud para factuales** (perfil default) | Orquestador potente + workers baratos | Piloto F1 manual (local) falló con URLs inventadas; swarm (cloud) funcionó |
| **Gates fail-closed** (verificar_dataset.py) | Specification schemas (MAST 1) | F1: "FALLA: no existe investigacion.json → exit 1" a coste 0 |
| **Router local-cloud + cache hit 99,4%** | Cost control + prefix caching | Medido con pipeline_proxy (hoy: 90.752/91.284 tokens = 99,4%) |
| **Observabilidad** (pipeline_obs.jsonl, TTFB/tokens/coste) | Coste por agente / observabilidad | Ledger real desde 06-ago, validado con CSVs DeepSeek |

### 🟡 IMPLEMENTABLE AHORA (fácil, ya existe en la CLI)

**Jerarquía CEO→director→trabajador con el kanban nativo** (el lab tiene `hermes kanban create` + `link` + `assign` + `decompose`):
1. Card raíz = CEO (visión/objetivo) → `decompose` en subtareas = directores → `link` dependencias → `assign` a workers (perfil cloud para factuales)
2. Presupuestos por card (tokens/pasos) = cost control del artículo
3. **Probar con 2 niveles** (no 3): la latencia acumulada del jerárquico (6-12s mínimo por nivel) penaliza en el lab; 2 niveles = coordinador→workers es el punto dulce

### 🔴 NO IMPLEMENTAR (recomendación con evidencia)

| Propuesta | Por qué NO |
|---|---|
| Swarm libre sin supervisión | Debugging nightmare (MAST): sin control flow central es imposible depurar; el lab usa watchdog por una razón |
| Mesh/A2A entre servicios | El lab es 1 proceso (Hermes) + Docker; no hay múltiples servicios que coordinar entre sí — sería over-engineering (el artículo: "stay in-process with MCP alone" hasta tener razón concreta) |
| >2 niveles de jerarquía | Latencia acumulada + pérdida de info entre niveles (jerárquico 3-5x coste) |
| Delegación de factuales con modelos locales | 2 evidencias propias (31-ago F1, 01-sep repetición): r1-distill-qwen-14b inventa URLs y autoinforma "éxito" con archivo inexistente. Regla del lab vigente |
| Emular a Emowe con su club | El lab ya tiene TODO el nivel 4 de forma local y gratuita; el club vende lo que el lab ya corre |

### 📌 ACCIÓN CONCRETA PROPONIBLE (pendiente de tu OK)

**Probar la jerarquía de 2 niveles del kanban nativo en un caso real**: un objetivo del lab (p.ej. "investigar X para LinkedIn") → card raíz → 2-3 workers factuales (cloud) → verifier → synthesizer, con `--workspace dir:/ruta` (pitfall 2: scratch es efímero). Eso validaría en el lab el patrón Hierarchical de la industria SIN construir nada nuevo (todo existe en `hermes kanban`).

## 5. Actualización del mapa de capacidades (pendiente)

El mapa-capacidades-lab-20260824.md NO menciona orquestación/kanban (se creó 24-ago, antes del kanban nativo del 01-sep). Añadir dominio "ORQUESTACIÓN MULTI-AGENTE": kanban nativo (SQLite, dispatcher 60s, swarm workers→verifier→synthesizer), delegate_task (subagentes), 3 MCPs. La regla del mapa: si no está, las novedades externas parecen futuribles cuando ya son validación.

## Fuentes (todas verificadas 01-sep-2026)

- r/LocalLLaMA: hilo "hardest part is coordinating them" (1rc8yeu) · "local multi agent systems" (1plohsn) · "bunch of terminals" (1u99w8w) — leídos vía API JSON (browser)
- glukhov.org "Multi-Agent Orchestration Patterns: A Practical Guide" (6 patrones + MAST NeurIPS 2025 + decision framework) — leído completo vía browser
- Emowe "Test de nivel de evolución IA" (uyJa3yb9CUc) — transcripción de hoy
- Capacidades del lab: kanban nativo verificado con `hermes kanban --help` + piloto swarm 01-sep (skill delegacion-subagentes) + pipeline_proxy (cache hit 99,4% hoy)
