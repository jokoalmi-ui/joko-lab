---
title: "PRD — Graph de delegación multi-agente del LAB (18-ago-2026)"
type: research
---

# PRD: GRAPH DE DELEGACIÓN MULTI-AGENTE DEL LAB
**VERACIDAD:** [ALCANCE INTERNO]
fuentes externas analizadas (podcast atareao 17-ago, codewithbrij 18-ago,
checklist 8 preguntas, skill delegacion-subagentes) + config real del lab.

## 0. RESUMEN EJECUTIVO

El lab está en fase **LOOP GOVERNS** (auditoría 18-ago: 7/8 checklist
cumplido). La frontera es el **GRAPH**: delegación formal multi-agente con
nodos especializados, edges con contrato y estado compartido. Este PRD
define el primer graph del lab aplicando el patrón validado del podcast
atareao (coordinador que NO ejecuta + especialistas con permisos mínimos)
y el checklist de codewithbrij (pregunta 8: contratos de edges).

**Bloqueador identificado**: `delegation.model: llama31-8b-64k` (local,
Ollama) — 4 casos reales documentados de informes pobres. El graph exige
pinar modelo cloud (o, como mínimo, un modelo local de calidad probada).

## 1. ALCANCE

**Incluye**:
- Graph de 4 nodos para el CASO DE USO PILOTO: producción de contenido
  educativo LinkedIn Lab (investigación → redacción → revisión → publicación)
- Contratos de edges (entrada/salida/estado) de cada nodo
- Política de modelos por nodo (coste/calidad)
- Mecanismo de verificación (gate existente: verificar_research + suite)
- Criterio de éxito medible

**NO incluye** (fuera de alcance v1):
- Graph de producción general (todos los tipos de tarea del lab)
- Anidación de graphs (graph dentro de graph)
- Cambio de config (solo propuesta — decisión del usuario)
- Integración con MCP del lab (futurible aparte)

## 2. EL GRAPH (caso de uso: contenido LinkedIn Lab)

```
┌─────────────────────────────────────────────────────────┐
│                    COORDINADOR (supervisor)             │
│  Modelo: deepseek-v4-flash (cloud) · temp 0.3           │
│  Permisos: task:{"*": deny, investigador: allow,        │
│           redactor: allow, revisor: allow}              │
│  NO ejecuta nada: solo delega y orquesta                │
└──────────────┬───────────────────┬──────────────────────┘
               │ edge C→I           │ edge C→R (2ª pasada)
               ▼                    ▼
┌──────────────────────┐  ┌──────────────────────┐
│    INVESTIGADOR      │  │      REDACTOR        │
│  Modelo: llama31-8b  │  │  Modelo: deepseek-v4 │
│  (local, temp 0.1)   │  │  (cloud, temp 0.7)   │
│  Toolsets: [web]     │  │  Toolsets: [] (solo  │
│  SOLO datos+fuentes  │  │  recibe investigación│
└──────────┬───────────┘  └──────────┬───────────┘
           │ edge I→R (dataset)      │ edge R→V
           ▼                         ▼
┌──────────────────────────────────────────────┐
│              REVISOR (solo lectura)          │
│  Modelo: llama31-8b (local, temp 0.2)        │
│  Toolsets: [] · Permisos: deny editar        │
│  Devuelve INFORME (no edita) → bucle:        │
│  revisor→redactor hasta OK                   │
└──────────────────────────────────────────────┘
```

## 3. CONTRATOS DE EDGES (checklist pregunta 8)

### ⚠️ MEJORAS APLICADAS 31-ago-2026 (patrón Atomic Agents de Emowe)

Dos refinamientos al flujo del graph, validados por la especificación de agentes
atómicos (research/analisis-emowe-agentes-atomicos.md):

**Mejora A — ENCADENAR POR SEÑAL, no lanzar en paralelo ("una card a la vez").**
El coordinador NO lanza los 3 subagentes a la vez: crea el investigador, espera
su resultado, y SOLO si el investigador produce un dataset válido (≥5 claims con
URL) crea el redactor; solo si el borrador existe crea el revisor. Principio de
Emowe: "si el paso 1 no produce nada, los pasos 2-3 nunca existen". Beneficio:
no se gasta cloud ni tiempo en redactar sobre un dataset vacío o inválido.

**Mejora B — WIRING SELF-CHECK del coordinador (anti "carta sorda").**
El punto frágil del graph es que un LLM (el coordinador) escribe las rutas del
estado compartido (/tmp/graph_<id>/...). Una ruta mal escrita = el subagente
siguiente no encuentra su entrada. Por eso, ANTES de lanzar cada nodo, el
coordinador re-lee el archivo de estado del nodo anterior y verifica que la ruta
existe y coincide exactamente con lo que va a pasar al siguiente. Si no existe →
bloquea el card, no inventa el paso (fail-loud, patrón Emowe).

### Edge C→I (Coordinador → Investigador)
- **Entrada**: tema + 2-3 preguntas de investigación + formato de salida (JSON: claims con URL + cita textual + fecha)
- **Salida**: dataset de claims verificables (mínimo 5, máximo 10)
- **Estado compartido**: archivo /tmp/graph_<id>/investigacion.json
- **Éxito**: ≥5 claims con URL real citada · api_calls ≥ 5 (síntoma de subagente real)
- **Fallo → retry**: 1 reintento con instrucción más acotada; si falla → escalar a coordinador

### Edge I→R (Investigador → Redactor)
- **Entrada**: dataset JSON (claims)
- **Salida**: borrador en Markdown (300-500 palabras, tono LinkedIn Lab educativo)
- **Estado compartido**: /tmp/graph_<id>/borrador.md
- **Éxito**: usa TODOS los claims del dataset · estructura título+gancho+3 secciones+CTA
- **Restricción**: NO inventa datos (solo los del dataset) · NO cita fuentes que no estén en el dataset

### Edge R→V (Redactor → Revisor)
- **Entrada**: borrador.md
- **Salida**: informe de revisión (errores factuales, sesgos, tono, estructura) — NO edita el archivo
- **Estado compartido**: /tmp/graph_<id>/revision.md
- **Éxito**: informe con ≥3 observaciones concretas · verifica que cada claim del dataset está citado
- **Bucle**: si revisor marca errores → redactor corrige → revisor re-verifica (máx 2 vueltas)

### Edge C→Final (Coordinador → Entrega)
- **Entrada**: borrador final + informe de revisión OK
- **Salida**: resumen al usuario con: ruta del borrador, nº claims usados, nº revisiones, veredicto del revisor
- **Criterio**: solo se entrega al usuario si revisor dice OK (fail-closed, patrón gate del lab)

## 4. POLÍTICA DE MODELOS POR NODO

| Nodo | Modelo | Temp | Coste | Justificación |
|---|---|---|---|---|
| Coordinador | deepseek-v4-flash (cloud) | 0.3 | tokens | Orquesta, no genera — necesita fiabilidad de decisión |
| Investigador | llama31-8b-64k (local) | 0.1 | 0 € | Búsqueda mecánica con criterio claro... ⚠️ PERO: 4 casos de fallo documentados. Opción A: dejar local y verificar con gate (api_calls ≥5); Opción B: cloud también (más fiable, más coste) |
| Redactor | deepseek-v4-flash (cloud) | 0.7 | tokens | Generación de calidad media-alta |
| Revisor | llama31-8b-64k (local) | 0.2 | 0 € | Solo lectura + informe — el más barato de pinear bien |

**Decisión pendiente del usuario**: investigador local (Opción A, gratis pero
arriesgado) vs cloud (Opción B, fiable pero con coste). El podcast atareao
usó modelo pequeño para bibliotecario porque "solo datos con fuentes" —
pero en el lab los intentos con llama31 en investigación fallaron 4 veces.
**Recomendación: Opción B para investigador en el piloto** (1ª vez),
reevaluar con datos tras el piloto.

## 5. CAMBIO DE CONFIG REQUERIDO (propuesta — NO ejecutada)

```yaml
# config.yaml — delegación global (afecta a TODO delegate_task)
delegation:
  model: deepseek/deepseek-v4-flash   # ← cambiar de llama31-8b-64k
  provider: deepseek
```

**⚠️ IMPACTO**: este cambio afecta a TODA delegación futura del lab (no solo
al graph). Alternativa más conservadora: mantener llama31 como default y
hacer el piloto con el coordinador en la sesión principal (Hermes) usando
delegate_task directamente — sin cambiar config global. **Recomendación:
piloto SIN cambiar config** (usar la sesión como coordinador), validar el
flujo, y SOLO entonces decidir si pinear cloud globalmente.

## 6. VERIFICACIÓN (gate del lab aplicado al graph)

1. **api_calls por subagente** ≥ 5 (síntoma anti-zombi de la skill)
2. **verificar_research.py** sobre el borrador final (etiqueta VERIFICADO/ALCANCE INTERNO)
3. **Cada claim del dataset** con URL + cita textual (contrastable)
4. **Diff del borrador** vs dataset: no hay datos que no vengan del investigador
5. **Suite de tests del lab**: intacta tras el piloto (no debe tocarse código)
6. **Registro en backlog** con backup (RULE-008) tras el piloto

## 7. PLAN DE IMPLEMENTACIÓN (fases)

| Fase | Qué | Criterio de salida |
|---|---|---|
| **F0** | Aprobación del PRD por el usuario | OK explícito |
| **F1** | Piloto manual: sesión = coordinador; 2 subagentes (investigador+revisor) sobre 1 tema real de LinkedIn — **con Mejora A (encadenar por señal) y Mejora B (wiring self-check)** | Informe del revisor con ≥3 observaciones · claims verificados |
| **F2** | Añadir nodo redactor (3º subagente) | Borrador usable con revisor OK |
| **F3** | Documentar el flujo en skill (graph-lab) + plantilla reutilizable | Skill creada con comando de ejecución |
| **F4** | Decidir config global (cloud vs local) con datos del piloto | Decisión documentada en backlog |

## 8. RIESGOS Y MITIGACIONES

| Riesgo | Mitigación |
|---|---|
| Subagente zombie (llama31 no ejecuta) | Gate api_calls ≥5 + retry acotado + escalar a coordinador |
| Coste de tokens cloud | Piloto con 1 tema real; medir coste real antes de decidir escala |
| Contaminación de contexto | Contexto aislado por subagente (nativo) + estado en /tmp/graph_<id>/ |
| Over-engineering (graph innecesario para tareas simples) | REGLA: graph SOLO para tareas de 3+ subpasos con verificación de fuentes; lo demás, sesión directa |
| El coordinador "hace el trabajo él mismo" (error del podcast) | Prompt con "NO HAGAS EL TRABAJO TÚ MISMO" en mayúsculas (patrón validado) |

## 9. MÉTRICAS DE ÉXITO DEL PILOTO (medibles)

- [ ] 1 artículo LinkedIn completado de principio a fin (investigación→borrador→revisión)
- [ ] api_calls por subagente ≥ 5 (sin zombies)
- [ ] Revisor detecta ≥1 error real que el redactor corrige (el gate aporta valor)
- [ ] Tiempo total < 30 min (vs ~2h si se hiciera todo en sesión)
- [ ] Coste cloud < 0,10 € por artículo (medido con las respuestas reales)

## 10. RELACIÓN CON OTROS FUTURIBLES

- **skill "grill me"** (del podcast, 17-ago): el coordinador podría preguntar
  2-3 preguntas antes de lanzar el graph → integrar en F3
- **PRD PROMPT** (patrón 17-ago): este documento ES la aplicación del patrón
- **MCP del lab**: si un día hay MCP de BD, el investigador podría
  consultarlo — fuera de alcance v1
- **least-privilege R1**: ya garantiza toolsets mínimos por nodo ✅

---

*Fin del PRD — ✅ APROBADO por el usuario el 31-ago-2026 (F0 OK, con Mejoras A/B de Emowe incorporadas). F1 piloto en curso.

## 📋 RESULTADO PILOTO F1 (31-ago-2026 23:55) — gate FUNCIONA (fail-closed)

Ejecutado el piloto F1 con tema real de LinkedIn (Spec-Driven vs Vibe Coding).
RESULTADO DEL INVESTIGADOR: **INCUMPLIÓ el contrato del edge C→I**:
- api_calls = 1 (contrato: ≥5) → no investigó, generó de memoria
- 5/5 URLs = `example.com` (INVENTADAS — el peor fallo posible)
- NO escribió `investigacion.json` en el estado compartido (incumplió Mejora B)

GATE (Mejora B) → **FALLA: "no existe investigacion.json (el investigador no entregó)"** → exit 1 → **NO se lanzó el revisor** (Mejora A funcionó: sin dataset válido, no hay revisor).

LECCIONES DEL PILOTO (valiosas — el sistema hizo su trabajo):
1. **El gate de verificación del graph FUNCIONA**: atrapó datos inventados antes de costar nada más. fail-closed correcto.
2. **La delegación LOCAL no es fiable para investigación factual** (modelo deepseek-r1-distill-qwen-14b inventó URLs). Confirma la regla del lab: "locales NO fiables; investigar en sesión".
3. **api_calls ≥ 5 como gate anti-zombi es correcto**: un investigador que hace 1 llamada no investigó.
4. El coordinador debe PODER elegir el modelo del investigador (cloud) o el nodo investigador debe usar el modelo principal, no el de delegación local.

ACCIÓN SIGUIENTE (RESUELTA el 01-sep): **el PRD graph se sustituye por el kanban nativo de Hermes** (ver sección final).

---

## 🔄 DECISIÓN FINAL 01-sep-2026: PRD GRAPH → KANBAN NATIVO DE HERMES (sustitución)

**Contexto (descubierto 01-sep, tras el comentario del usuario sobre el kanban de Emowe):** Hermes tiene un **kanban nativo integrado** (`hermes kanban`, kanban.db SQLite) que implementa EXACTAMENTE el diseño que este PRD quería construir a mano: board de cards con estado, dispatcher ciego integrado en el gateway, workers aislados, dependencias entre tasks.

### ✅ PILOTO KANBAN SWARM (01-sep-2026 10:35) — ÉXITO COMPLETO

Ejecutado `hermes kanban swarm` con el MISMO tema del piloto F1 (Spec-Driven vs Vibe Coding):

| | Piloto F1 manual (31-ago) | Piloto kanban nativo (01-sep) |
|---|---|---|
| Modelo | local deepseek-r1-distill | **cloud deepseek-v4-flash** (perfil default) |
| Fuentes | 5/5 example.com INVENTADAS ❌ | **16 reales verificadas** (14 HTTP 200 + 2 anti-bot confirmadas) ✅ |
| Estado compartido | archivo que el subagente debía escribir | **SQLite + dispatcher automático** |
| Verifier | no se lanzó (gate fail-closed) | **gate pass con evidencia suficiente** |
| Resultado | fallo (correcto, fail-closed) | **informe comparativo completo** |

Tiempo: ~15 min · 6/6 cards done (2 workers → verifier → synthesizer).

### POR QUÉ SUSTITUYE AL PRD MANUAL

1. **Estado en SQLite elimina el fallo de raíz**: la card ES el estado (no un archivo que el subagente debe recordar escribir — el fallo exacto del F1).
2. **El dispatcher hace el wiring solo**: no hay coordinador manual verificando rutas (Mejora B queda incorporada por diseño).
3. **`kanban swarm` ya tiene el patrón workers→verifier→synthesizer** que este PRD quería construir desde 18-ago.
4. **El perfil default (cloud) es el correcto para factuales** — la delegación local sigue sin ser fiable.

### PITFALLS DESCUBIERTOS (registrados en backlog)

- ⚠️ Assignee `default:verificador` / `default:sintetizador` NO se despacha (perfil inexistente en disco) → reasignar al perfil real: `hermes kanban reassign <id> default`.
- ⚠️ Workspace scratch es EFÍMERO (informes se borran al completar) → usar `--workspace dir:/ruta` para preservar salidas.

### ESTADO FINAL DEL PRD

- **V1 (manual)**: ✅ APROBADO como diseño conceptual (F0) — las Mejoras A/B de Emowe quedaron validadas por el kanban nativo (encadenar por señal + wiring).
- **Implementación**: **NO se construye el orquestador manual** → se usa `hermes kanban swarm` (o `kanban create` + assign para graphs a medida).
- **Pendientes futuros**: probar `--workspace dir:` para preservar informes; evaluar graphs a medida (más allá del patrón swarm) con `kanban create`/`link`/`assign`.

