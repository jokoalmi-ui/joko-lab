---
title: "Investigación — Múltiples sesiones en un mismo PC: sincronización instantánea"
type: research
---

# Investigación — Múltiples sesiones en un mismo PC: sincronización instantánea
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 05-ago-2026
**Motivo:** El lab tiene sesiones independientes (Telegram, CLI, cron) sin estado
compartido en tiempo real. `shared-state.json` + `session-state.sh` + heartbeat
es la solución actual (unidireccional, bajo demanda). Se investiga cómo lo
resuelven otros.

---

## 1. El problema (confirmado por la comunidad Hermes)

**Issue #28690** (hermes-agent, 19-may-2026) describe EXACTAMENTE el caso del lab:

> "Hermes ya soporta múltiples contextos: CLI, gateway, cron, spawned workers,
> Kanban. En la práctica hay varios agentes vivos a la vez... que no se conocen
> entre sí salvo que el usuario relate el contexto manualmente."

**Problemas que esto causa (textuales del issue):**
- Trabajo duplicado en la misma tarea
- Ediciones conflictivas en el mismo repo/worktree
- Acciones externas repetidas (una sesión no sabe que otra ya las hizo)
- Handoffs perdidos entre sesiones
- Dificultad para responder "¿qué están haciendo mis agentes ahora?"

**El UX objetivo:** "debe sentirse como un pequeño equipo de agentes
coordinado, no como terminales aislados."

---

## 2. Solución propuesta por la comunidad: "Session Mesh" (#28690)

Capa de coordinación local por sesión con:

| Componente | Función |
|---|---|
| **1. Registro activo de sesiones** | Heartbeat periódico a un registro compartido (scoped por profile) |
| **2. API de consulta/mensajería** | `session_list_active()`, `session_query(id, q)`, `session_send(id, msg)`, `session_broadcast(msg)`, `session_claim_resource(resource)` |
| **3. Comandos de usuario** | `/sessions active`, `/sessions ask <id>`, `/sync`, `/handoff <id>` |
| **4. Sincronización** | Aviso antes de editar un repo reclamado por otra sesión; handoff explícito |

**Campos del heartbeat sugeridos:**
```
session id, profile, platform/source, model/provider
process id / host / start time / last heartbeat
tarea actual visible al usuario
cwd / repo / git branch / worktree
recursos reclamados: rutas, puertos, crons, cuentas
estado: idle | thinking | tool-running | blocked | waiting-user | done | errored
```

**Advertencias de diseño:** sin locks duros al principio (advisory); scope por
profile; sin exponer transcripciones completas (solo resúmenes auto-reportados);
evitar deadlocks y bucles agente-a-agente (timeouts, presupuestos de mensajes);
desactivable en config.

**Minimal first version:** heartbeat table + `/sessions active` + herramienta
`session_list_active` + consulta manual + avisos de conflicto por cwd/repo.

---

## 3. Solución alternativa: "Domain-Owned File Bus" (#4529)

**Validado en producción real** (agentes Hermes en LXC aislados, Proxmox):

> "Scope bleed es el modo de fallo principal de los diseños un-agente-hace-todo.
> La pérdida de contexto entre sesiones se resuelve leyendo estado compartido
> al arrancar."

**El modelo:**
- Directorio compartido: `~/.hermes/team-context/`
- **Un archivo markdown por dominio, cada uno propiedad de UN agente**
- **Todos los agentes leen todos los archivos; cada uno escribe solo el suyo**
- Sin protocolo de locking — la propiedad se impone por convención

**Esquema de archivo:**
```markdown
## health.md (propiedad: health-agent)
---
owner: health-agent
last_updated: 2026-04-02
---
sleep_quality: poor
energy_level: low
recommendation: reduce cognitive load today
```

**Por qué markdown y no SQLite:** los archivos markdown son directamente
legibles en el contexto del agente; SQLite añade dependencia y es más difícil
de inspeccionar/razonar para un LLM.

**Comparación con alternativas:**
| Alternativa | Por qué NO |
|---|---|
| Filesystem sin reglas (workaround actual) | Frágil: sin esquema, sin propiedad, sin convención de nombres |
| Agente padre como relé | Quema tokens, pierde info por resumir, no sirve para equipos sin padre |
| #377 Shared Memory Pools | Temporal (flujo de trabajo), se limpia al terminar — no persiste entre sesiones |
| SQLite compartido | Más pesado de lo necesario, dependencia, menos legible para el agente |

---

## 4. Patrón del sector: Redis como capa de memoria

Redis (y su `agent-memory-server` de 2026) propone una **capa de memoria
centralizada** para agentes:

| Necesidad | Solución Redis |
|---|---|
| Estado de sesión (working memory) | Claves por sesión (`session:<id>:messages`) |
| Memoria a largo plazo | Vectores + búsqueda semántica |
| Cross-session / load-balanced | ✅ Estado compartido entre instancias |
| Checkpoints | Persistencia de hilos |

**Limitación señalada por el propio Redis:** una vector DB standalone indexa
memoria semántica pero no cubre el estado de sesión en marcha ni el log de
acciones ordenado; y añadir un servicio en el hot path del agente añade
latencia que se acumula en bucles multi-paso.

**Veredicto para el lab:** Redis es la opción "enterprise" — potente pero
más pesada de lo que necesita un lab local de 2-3 sesiones. La lección
transferible es la SEPARACIÓN de planos: working memory (sesión) vs long-term
(knowledge) vs cross-agent (estado compartido).

---

## 5. Patrón del sector: estado externo compartido + sincronización explícita

El artículo "Parallel Agents Are Just Multithreading" (may-2026) aporta el
marco teórico:

> "Los agentes paralelos operan sobre estado externo compartido: bases de
> datos, colas, archivos, knowledge stores. La coordinación requiere
> sincronización EXPLÍCITA: protocolos de claim, contratos de esquema, buses
> de eventos y barreras."

**Los 4 mecanismos de sincronización que nombra:**
1. **Claim protocols** — reclamar un recurso antes de usarlo (advisory lock)
2. **Schema contracts** — acordar el formato del estado compartido
3. **Event buses** — notificar cambios (no solo estado estático)
4. **Barriers** — puntos de espera para coordinar fases

**Aplicación al lab:**
- Claim protocol = `session_claim_resource` (el lab NO lo tiene — las sesiones
  tocan archivos sin avisar)
- Schema contract = el YAML/JSON de shared-state (el lab SÍ lo tiene)
- Event bus = heartbeat/eventos (el lab lo tiene a medias — `shared-events.sh`)
- Barriers = handoffs explícitos (el lab no los tiene)

---

## 6. Multi-agent orchestration: memoria compartida + comunicación estandarizada

La guía de orchestration 2026 (lyzr, codebridge) coincide en las decisiones
arquitecturales clave:

1. **Shared memory / state management** — preservar continuidad entre sesiones
2. **Standardized tool/API integration layer** — que todos hablen el mismo idioma
3. **Communication protocols** — prevenir "coordination overload"
4. **Modelo de coordinación**: centralizado / descentralizado / jerárquico

**Modelos de coordinación:**
| Modelo | Cuándo |
|---|---|
| Centralizado (orquestador) | Un agente dirige a los demás — fácil de gobernar, cuello de botella |
| Descentralizado (peer) | Agentes se hablan directamente — escalable, más complejo |
| Jerárquico | Niveles de delegación — equilibrio |

**El lab hoy:** centralizado de facto (Hermes orquesta; las sesiones no se
hablan entre sí, pasan por shared-state).

---

## 7. Sincronización técnica instantánea (mecanismos OS)

Para que el estado sea "lo más instantáneo posible" (pedido del usuario):

| Mecanismo | Latencia | Para qué |
|---|---|---|
| **File watcher (inotify)** | ms | Detectar cambios en shared-state al momento |
| **Polling de archivo** (actual) | 10 min | Heartbeat — barato pero lento |
| **Unix socket / named pipe** | ms | Comunicación agente-agente directa |
| **Redis pub/sub** | ms | Eventos en tiempo real |
| **Mmap compartido** | µs | Estado en memoria compartida |

**Recomendación realista:** inotify (o polling corto de 5-10s) sobre el
directorio `team-context/` — da "casi instantáneo" sin añadir servicios.

---

## 8. Comparativa de soluciones para el lab

| Solución | Complejidad | Instantaneidad | Encaje |
|---|---|---|---|
| **File bus + polling corto** (evolución del actual) | Baja | ~10s | ✅ MEJOR OPCIÓN |
| **File bus + inotify** | Baja-media | ms | ✅ Ideal |
| **Redis pub/sub** | Media (servicio nuevo) | ms | ⚠️ Sobredimensionado |
| **Unix socket** | Media | ms | ⚠️ Requiere código |
| **Session Mesh (issue #28690)** | Alta (nativo Hermes) | — | ⏳ Si Hermes lo implementa |

**Veredicto:** la evolución natural del lab es el **Domain-Owned File Bus**
(#4529): cada dominio con su archivo, todos leen, uno escribe por archivo,
más un **file watcher corto** (o polling 5-10s) para acercarse a tiempo real.

---

## 9. Conclusión práctica para Joko Lab

**Lo que el lab YA tiene** (y coincide con el sector):
- `shared-events.sh write/read` — evento bus básico ✅
- `session-state.sh` + heartbeat 10 min — registro de sesiones ✅
- `shared-state.json` — schema contract ✅

**Lo que FALTA** (según las mejores prácticas):
1. **Dominios por archivo** — separar el estado por dominio (biohacking,
   perfume, lab, docker) en vez de un solo shared-state.json
2. **Ownership** — cada sesión escribe solo en su dominio
3. **Latencia** — bajar de 10 min a ~10s (polling corto) o ms (inotify)
4. **Claim protocol** — que una sesión avise antes de tocar un recurso que
   otra usa (git repo, puerto, archivo)
5. **Handoff explícito** — notas de traspaso entre sesiones

**Nota estratégica:** el issue #28690 (Session Mesh) está ABIERTO en Hermes.
Si Nous lo implementa, será la solución nativa. El file bus del lab es el
puente — compatible y sin esperar.

---

## Fuentes

- GitHub NousResearch/hermes-agent issue #28690 (Session Mesh) — 19-may-2026
- GitHub NousResearch/hermes-agent issue #4529 (Domain-Owned File Bus) — 02-abr-2026
- Redis Agent Memory docs — redis.io/docs (2026)
- "Parallel Agents Are Just Multithreading" — Medium, may-2026
- Multi-Agent Orchestration Guide — lyzr.ai / codebridge.tech (2026)
- Hermes multi-agent workflows — hermes-agent.ai (may-2026)
