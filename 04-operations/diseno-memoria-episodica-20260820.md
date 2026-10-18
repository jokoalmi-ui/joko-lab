---
title: "Diseño — Capa de estructura mínima de Memoria Episódica (MEP-001)"
type: operations
---

# Diseño — Capa de estructura mínima de Memoria Episódica (MEP-001)

fecha: 2026-08-20
autor: agente (jokoalmi)
tipo: diseño / operaciones
estado: IMPLEMENTADO (2026-08-20) — ledger + script + [[RULE-011]] creados y verificados · RECTIFICADO 04-oct-2026: Pieza A (episodic_ledger) retirada; ver §7
origen: gap detectado en `research/analisis-memoria-agentes-3-tipos.md` +
decisión de priorización del usuario (mayor incidencia en funcionamiento del LAB)

---

## 1. Problema

Las piezas de memoria episódica EXISTEN pero son islas: cada una tiene su
formato, su ubicación y su ciclo de vida, y ninguna es consultable como
"qué pasó" de forma unificada. El síntoma diario: cada sesión arranca en
frío y hay que reconstruir el estado a mano (session_search + file bus +
backlog), con fricción y lagunas.

## 2. Auditoría real (2026-08-20, verificada en disco)

| Pieza | Ruta | Formato | Ciclo de vida | Rol episódico |
|---|---|---|---|---|
| lecciones_ledger | joko-lab/04-operations/metrics/lecciones_ledger.jsonl | LEC-id, fecha, dominio, titulo, tried, causa_raiz | persistente | Lecciones con causa raíz ✅ estructurado |
| mel_ledger | 04-operations/metrics/mel_ledger.jsonl | MEL-id, fecha, nivel, trigger, procedure, root_cause, systemic_change | persistente | Incidentes con root cause ✅ estructurado |
| operations_ledger | 04-operations/metrics/operations_ledger.jsonl | OP-id, ts, operation_type, required_gates, executed_gates, result | persistente | Operaciones con gates ✅ estructurado |
| local_cloud_ledger | 04-operations/metrics/local_cloud_ledger.jsonl | ts, tarea, tipo, motor, latencia | persistente | Telemetría router (no episódica) |
| shared-events | ~/.hermes/shared-events.jsonl (143 líneas) | ts, canal, tipo, resumen | ROTACIÓN: poda >14 días o >500 líneas | Timeline plano EFÍMERO — sin id, sin dominio, sin ref |
| file bus | ~/.hermes/team-context/*.md | dominio.md (lab, cli, telegram...) | sobrescrito por convención | Estado actual, no histórico |
| backlog | joko-lab/04-operations/backlogs/2026-07-31-backlog.md (842 líneas) | markdown priorizado | crece, con backups | Pendientes + completados |
| prospective-memory | 04-operations/prospective-memory.md | INT-NNN + deadline + fuente | gestionado por prospective.sh | Intenciones futuras (tipo 7) |
| state.db | ~/.hermes/state.db | SQLite transcript | permanente | Materia prima cruda (session_search) |

GAP real (3):
1. **No existe punto de consulta único** "¿qué pasó el día X / en el dominio Y /
   qué quedó abierto?" — hay que mirar 4+ fuentes a mano.
2. **El 90% de la actividad cotidiana** (eventos, cambios, tareas cerradas)
   solo vive en shared-events, que se PODA a los 14 días → la mayor parte de
   la memoria episódica del lab es efímera por diseño.
3. **Sin id ni dominio ni ref** en la capa cotidiana → no se puede enlazar un
   evento con su causa raíz ni con el artefacto donde quedó.

## 3. Diseño mínimo (2 piezas nuevas + 1 regla, 0 cambios a lo existente)

### Pieza A — episodic_ledger.jsonl (nuevo)

Ruta: `joko-lab/04-operations/metrics/episodic_ledger.jsonl`

Esquema mínimo (una línea JSON por evento, append-only, backups .bak como
los demás ledgers):

```json
{
  "ep_id": "EP-20260820-001",
  "ts": "2026-08-20T12:52:51+02:00",
  "dominio": "sesiones | rag | router | n8n | pipeline | proceso | ...",
  "tipo": "evento | leccion | incidente | decision",
  "evento": "qué pasó (resumen ≤200 chars)",
  "causa": "por qué (raíz; vacío si no aplica)",
  "accion": "qué se hizo / fix / decisión tomada",
  "ref": "ruta o id de la fuente (backlog, research/, sesión)",
  "estado": "abierto | cerrado"
}
```

Regla anti-duplicado (el usuario odia duplicados):
- Si el evento encaja en un ledger especializado → va ALLÁ, no aquí:
  - lección con causa raíz → `lecciones_ledger.jsonl` (LEC-*)
  - incidente con impacto sistémico → `mel_ledger.jsonl` (MEL-*)
  - operación con gates → `operations_ledger.jsonl` (OP-*)
- episodic_ledger recoge SOLO lo cotidiano sin hogar especializado: cambios
  de configuración, tareas cerradas, eventos de sesión, decisiones menores.
- Si hay duda → episodic_ledger (es el cajón general; los especializados
  son refinamiento posterior, no obligatorio).

### Pieza B — memoria-episodica.sh (nuevo, solo lectura)

Ruta: `~/.hermes/scripts/memoria-episodica.sh`

Consultas (patrón domain-bus.sh: bash puro, sin dependencias):

```bash
memoria-episodica.sh hoy                    # todo lo episódico de hoy (fecha)
memoria-episodica.sh dominio <X>            # episodios + LEC + MEL del dominio X
memoria-episodica.sh abiertos               # incidentes/eventos con estado abierto
memoria-episodica.sh buscar <texto>         # grep unificado en todas las fuentes
memoria-episodica.sh ultimo N               # últimas N líneas entre todas las fuentes
```

Qué fusiona (todas de solo lectura):
1. `episodic_ledger.jsonl`
2. `lecciones_ledger.jsonl` (LEC)
3. `mel_ledger.jsonl` (MEL)
4. `shared-events.jsonl` (solo ≤14 días — es lo que sobrevive)
5. `backlog` (pendientes activos, vía grep del último backlog)
6. opcional: `operations_ledger.jsonl` para `dominio`/`buscar`

Salida: una lista única ordenada por fecha, con la etiqueta de origen
(EP/LEC/MEL/EV/BL) para saber de dónde sale cada línea.

### Regla C — [[RULE-011]] propuesta (escritura mínima)

Integrada con [[RULE-009]] (registrar al completar), sin duplicar:

1. Al cerrar una tarea/incidente/cambio relevante: si encaja en ledger
   especializado (LEC/MEL/OP) → escribir allá (como hoy).
2. Si NO encaja → añadir UNA línea a `episodic_ledger.jsonl` con ref.
3. El shared-events se mantiene como aviso en vivo (efímero) — no es la
   memoria; el ledger es la memoria.
4. Los crons/watchdogs NO escriben en episodic_ledger (solo sesiones).

## 4. Coste y riesgo

- Nuevas piezas: 1 jsonl + 1 script bash (~80 líneas) — patrón idéntico a
  domain-bus.sh / prospective.sh ya validados.
- 0 cambios a piezas existentes → sin riesgo de regresión.
- El script es solo lectura → no requiere confirmaciones especiales.
- Primer uso: backfill NO necesario — el ledger arranca vacío y se llena
  hacia adelante (la historia ya vive en las otras fuentes, que el script
  consulta igualmente).

## 5. Criterio de éxito (verificable)

1. `memoria-episodica.sh hoy` responde en <2s y muestra TODO lo episódico
   del día fusionado (eventos + LEC + MEL + shared-events).
2. `memoria-episodica.sh dominio sesiones` muestra el incidente del handoff
   de hoy (EP/LEC) sin abrir 4 archivos.
3. `memoria-episodica.sh abiertos` lista incidentes sin cerrar.
4. Un mes después: los eventos de hoy SEGUIRÁN consultables (hoy mueren a
   los 14 días por la poda de shared-events — el ledger los conserva).

## 6. Decisión pendiente del usuario

- ¿Implementar ahora (crear ledger + script + RULE-011) o guardar el diseño?
- ¿Añadir RULE-011 como Knowledge Object (joko-lab/01-knowledge/objects/) o
  basta con la regla documentada aquí + memoria?

## 7. Rectificacion 04-oct-2026 — retirada de `episodic_ledger` (Pieza A)

MARCA: RECTIF-20261004-EPISODIC

Medido (04-oct-2026 21:12 CEST): `04-operations/metrics/episodic_ledger.jsonl` = **1 fila /
554 B**, `mtime` 2026-08-20 13:26 — el unico asiento es `EP-20260820-001` (el handoff del
mismo dia del diseno) y no ha recibido **ni una escritura en 45 dias**. Los ledgers
especializados siguen vivos: `lecciones_ledger` 16 filas (ultima 02-oct), `mel_ledger` 11
(06-ago), `operations_ledger` 114 (15-sep).

Decision (OK del usuario, 04-oct-2026): **retirar la Pieza A del MEP**. El rol que le asignaba
el diseno («cajon general» para lo cotidiano sin hogar especializado) no lo uso nadie: lo
cotidiano con causa raiz acaba en `lecciones_ledger` (LEC) y el resto simplemente no se
registra. La regla anti-duplicado funciona igual sin ella, porque los ledgers especializados
ya tienen la prioridad.

Que NO cambia: `memoria-episodica.sh` sigue siendo el punto de consulta unificado (fusiona
LEC + MEL + shared-events + backlog) y `episodic_ledger.jsonl` **no se borra ni se mueve**:
queda como historico y el script lo sigue leyendo (AGENTS.md §2: «no se borra: se archiva»).
[[RULE-011]] conserva su aserto en el `body` y lleva la rectificacion en su `history`.

Hueco que el diseno detecto y sigue ABIERTO (declarado, no resuelto): el grueso de la
actividad cotidiana solo vive en `shared-events`, que se poda a 14 dias → ese material sigue
siendo efimero, y sin `episodic_ledger` el hueco NO tiene sustituto. Si vuelve a doler, la via
no es resucitar un fichero que nadie escribe: es anadir el asiento al ledger especializado que
corresponda (LEC/MEL/OP) o proponer otro destino con su propia regla de escritura.
