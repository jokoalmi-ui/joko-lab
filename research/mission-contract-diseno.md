---
title: "Mission Contract — diseño (PROPUESTA, sin adoptar)"
type: research
---

# Mission Contract — diseño (PROPUESTA, sin adoptar)
**VERACIDAD:** [ALCANCE INTERNO]

- Estado: PROPUESTA pendiente de revisión (revisar 07-ago-2026)
- Origen: análisis externo (sesión 2, 07-ago-2026) sobre el hueco entre
  Graph Engineering y la ejecución real de misiones multi-fase.
- Fecha (España): 2026-08-07.
- Relación: extiende graph-engineering (shared state, nodos, aristas) y
  ai-router (límite declarado: "el Router no puede orquestar pipelines de
  múltiples fases; hace falta una capa de ejecución con estado, progreso y
  reutilización de resultados intermedios"). Es una pieza de la CAPA 2/3
  (recuperación/ejecución), distinta del gate cognitivo H-HEL-001 (CAPA 4),
  aunque comparten el principio: activación deliberada antes de ejecutar.
- Precedente de contrato en el lab: runtime/CONTRACT.md v1.0 (enrutamiento).
  Este contrato es de otro dominio (ejecución de misiones), por eso merece
  entidad propia y no una sección dentro del CONTRACT.md del router.

---

## 1. Qué es una misión

Una misión es una unidad de trabajo que persigue un objetivo concreto, se
ejecuta en varias fases (no necesariamente muchas) y deja evidencia
verificable de que el objetivo se cumplió o de por qué no se cumplió.

Una misión NO es una conversación. No es un prompt. No es una tarea de una
sola fase que se resuelve con una llamada. Es trabajo encadenado donde el
resultado de una fase alimenta a la siguiente, y donde el sistema necesita
saber, en cualquier momento, en qué punto está y qué ha pasado antes.

La distinción con el pipeline lineal actual del lab es que una misión
puede volver atrás, reintentar, ramificarse o paralelizarse. El pipeline
lineal actual pasa datos por archivo o tubería, en orden fijo, y no sabe
responder a preguntas como "¿qué fase falló?", "¿se puede reintentar sin
rehacer todo?" o "¿qué evidencia dejó la fase 2?".

## 2. Qué estado mantiene una misión

El estado de una misión es la respuesta a la pregunta: "¿en qué punto está
y qué necesita para continuar?". Se define con estos campos:

- id: identificador único de la misión (ej: M-2026-08-07-001).
- goal: el objetivo, expresado como resultado verificable.
- status: el estado de ciclo de vida (ver sección 4).
- current_node: la fase o nodo en el que está la ejecución ahora mismo.
- completed: lista de fases terminadas con su resultado.
- pending: lista de fases pendientes.
- retries: contador de reintentos por fase, con el motivo de cada uno.
- inputs: datos de entrada de cada fase.
- outputs: datos de salida de cada fase.
- evidence: ruta o referencia de la evidencia que deja cada fase (log,
  artefacto, resultado de verificación).
- checkpoints: puntos de estado guardados desde los que se puede reanudar.
- shared_state: el estado compartido entre nodos. Aquí "estado" NO es la
  memoria del sistema (policy de privacidad del lab). Es el acumulador de
  datos intermedios que fluye entre fases, como el state de LangGraph.

Nota terminológica: no llamar a shared_state "memory". En el lab "memoria"
tiene otro significado (memory policy, privacidad, contexto). El estado de
una misión es shared_state.

## 3. Qué transiciones puede sufrir

Una misión nace, se ejecuta y termina. Las transiciones de estado son:

- pendiente -> en_ejecucion (cuando el Runner la toma).
- en_ejecucion -> en_espera (cuando una fase espera un input externo, un
  humano, o un servicio que no responde).
- en_espera -> en_ejecucion (cuando el input llega).
- en_ejecucion -> reintentando (cuando una fase falla y el reintento está
  permitido por la configuración de la misión).
- reintentando -> en_ejecucion (reintento en curso) o -> fallida (cuando se
  agotan los reintentos).
- en_ejecucion -> completada (cuando todas las fases terminaron y la
  evidencia está registrada).
- en_ejecucion|reintentando|en_espera -> cancelada (cuando un humano o una
  política la detiene; el estado conserva lo que ya se hizo).
- cualquiera -> fallida (error no recuperable).

Regla: una misión nunca desaparece. Completada, fallida o cancelada,
conserva su registro con evidencia. Eso es lo que permite a MEL medir la
evolución y a PIL verificar que los gates se ejecutaron.

## 4. Qué eventos genera

Cada transición genera un evento, que se registra en un ledger (el lab ya
tiene el patrón: decision-ledger, activation-ledger, rag-query-ledger).
Eventos mínimos:

- mission.created (con goal y plan de fases).
- phase.started (con current_node e inputs).
- phase.completed (con outputs y evidence).
- phase.failed (con motivo y nº de reintento).
- mission.retrying (con contador y política de reintento).
- mission.completed (con evidencia final y estado de cada fase).
- mission.failed (con la fase que falló y el motivo).
- mission.cancelled (con el punto en el que se detuvo).

El ledger es append-only y la instrumentación es defensiva: si falla el
registro, la misión sigue (mismo patrón que la telemetría F1/F2 del lab).

## 5. Qué evidencia deja

Cada fase debe poder responder "¿cómo demuestro que hice lo que hice?".
Evidencia mínima por fase: inputs usados, outputs producidos, comando o
llamada ejecutada (con timestamp), y resultado de la verificación si la
fase la tiene (contrato de evidencia del lab: dependencias no son
evidencia). Al terminar, la misión deja un resumen con el goal, el estado
final, las fases y las evidencias, en el formato que el lab ya usa para
EXP/DEC (frontmatter + cuerpo), para que sea indexable por el RAG.

## 6. Cuándo termina

Termina cuando alcanza un estado terminal: completada (objetivo cumplido y
evidencia registrada), fallida (error no recuperable o reintentos agotados)
o cancelada (decisión humana o política). No hay estado "en ejecución"
indefinido: toda misión tiene un timeout o una política de cancelación.

## 7. Cuándo activar el Mission Runner (árbol por propiedades)

El criterio NO es el número de fases. Es si la misión exige propiedades de
ejecución que un pipeline lineal no puede dar. El árbol:

¿La misión requiere estado compartido entre fases (una fase necesita el
resultado de otra que ya pasó, y eso debe conservarse explícitamente)?
  SI -> Mission Runner

¿La misión puede volver atrás (una fase posterior invalida el resultado de
una anterior y hay que rehacerla sin rehacer todo)?
  SI -> Mission Runner

¿La misión exige reintentos semánticos (reintentar no es repetir la misma
llamada; es reintentar con conocimiento del fallo anterior)?
  SI -> Mission Runner

¿La misión tiene ramas condicionales (el siguiente paso depende del
resultado de la fase actual)?
  SI -> Mission Runner

¿La misión tiene paralelismo real (fases independientes que deben ejecutarse
a la vez)?
  SI -> Mission Runner

¿La misión exige checkpoints (poder reanudar desde un punto intermedio si
se interrumpe)?
  SI -> Mission Runner

Matiz crítico: la pregunta es "¿lo REQUIERE la lógica de negocio?", no
"¿podría tenerlo?". Toda misión podría tener retries; pocas lo exigen. Si
el árbol se responde con "podría", todo termina en Mission Runner y el
árbol no discrimina. La validación del criterio se hace contra misiones
reales del lab (candidato inmediato: el caso judicial de 4 fases de
ai-router, extraer -> clasificar -> puntuar -> redactar), nunca a priori.

Si ninguna propiedad se requiere, la misión es un pipeline lineal y se
ejecuta con el mecanismo actual (script encadenado o workflow simple), sin
Runner. Eso respeta el principio del artefacto mínimo: no añadir un motor
stateful donde no hace falta.

## 8. Relación con el motor (motor-agnóstico)

El contrato NO depende del motor. Una misión definida con este contrato
puede ejecutarse con:

- n8n (ya es un orquestador stateful en el lab; para misiones visuales o
  que ya viven en workflows existentes).
- Python (para misiones que necesitan LM Studio, RAG, delegación o lógica
  que n8n no expresa bien).
- LangGraph, Temporal, Prefect, Airflow u otro (si algún día hace falta).

El contrato permanece; el motor es intercambiable. En el lab, la regla
práctica: si la misión ya tiene forma de workflow n8n, se ejecuta en n8n;
el Runner Python solo cubre lo que n8n no puede. No duplicar motores.

## 9. Integración con el flujo existente

```
Solicitud
  -> Router (decide si es misión o tarea simple)
  -> Clasificación de misión (árbol de la sección 7)
  -> Pipeline lineal (si no requiere propiedades) | Mission Runner (si las requiere)
  -> Graph Execution (fases con estado y evidencia)
  -> PIL (verifica que los gates se ejecutaron)
  -> MEL (aprende del ledger de misiones)
```

El Router decide. El Runner ejecuta. PIL verifica. MEL aprende. Las
responsabilidades quedan separadas, igual que en la arquitectura v3 del
lab (el Decision Engine decide, el runtime ejecuta, la gobernanza vigila).

## 10. Siguientes pasos (propuesta, sin ejecutar)

1. Revisar este borrador con Joseba. HECHO (07-ago-2026).
2. Validar el contrato contra la misión real de 4 fases del caso judicial
   (¿el esquema cubre lo que esa misión necesitaba? ¿qué faltaría?).
   HECHO (07-ago-2026): validado contra caso Indra 2026 — 6/6 propiedades
   requeridas, 3 ajustes derivados (waiting_on, evidence como archivo,
   nodo humano). Ver sección 12.
3. Cuando el esquema esté estable, formalizarlo como mission.schema.json
   (o YAML) en lpa/contracts/, siguiendo el patrón contract-first del lab.
   HECHO (07-ago-2026): lpa/contracts/mission.schema.json — JSON Schema
   draft 2020-12, validado con jsonschema contra ejemplo del caso Indra
   (salida: "VALIDACION OK"). Pendiente de decisión sobre adopción.
4. Decidir el motor por misión (n8n vs Python), no un motor global.
   HECHO (07-ago-2026): confirmado por Joseba — n8n para misiones que ya
   viven en workflows existentes (12 workflows); Python solo para lo que
   n8n no cubre (LM Studio, RAG, delegación, archivos). Caso Indra: Python.
   Ver sección 13.
5. Convertir el árbol de activación en una RULE con el formato de
   01-knowledge/objects (type=RULE, tipo_tarea=orquestacion), con el
   matiz "requiere, no puede" y la validación contra misiones reales.
   HECHO (07-ago-2026): RULE-010 ADOPTADA como KO activo (KVC de Joseba),
   01-knowledge/objects/RULE-010.yaml, gate FK exit 0. Ver sección 13.

## 11. Qué falsearía este diseño

- Si una misión real del lab con estado compartido, ramas o reintentos se
  ejecuta correctamente con un pipeline lineal simple: el contrato es
  innecesario para ese caso y el árbol sobra.
- Si el coste de mantener el estado (ledger, checkpoints) supera el
  beneficio en las misiones reales del lab (que hoy son pocas): el contrato
  queda como referencia conceptual, no como pieza operativa.
- Si n8n cubre el 100% de las misiones stateful que el lab necesita: el
  Runner Python no debe construirse; el contrato sirve igual para
  documentar el estado de los workflows n8n.

---

## 12. Validación contra el caso real (caso Indra 2026)

Contraste del esquema contra la misión documentada en
forense-digital/references/caso-indra-2026.md (pipeline de 4 fases que
motivó la necesidad del Mission Runner en ai-router). Los datos que siguen
vienen de la referencia del caso, no de memoria.

### La misión real

- goal: dossier probatorio para reclamación de categoría profesional
  (Grupo D oficial -> Grupo C/B reclamado), trabajador con 18 años de
  antigüedad.
- Fases reales del protocolo forense:
  1. Extracción (barrido amplio, regex por función) -> 8.545 correos,
     2.681 evidencias en evidencias_raw.json.
  2. Puntuación y selección (top 1%, 0-100 por factor) ->
     top40_evidencias.json.
  3. Construcción del caso (organizar por FUNCIONES, 4 preguntas
     obligatorias por función) -> caso-judicial.txt/PDF.
  4. Preparación para el juicio (informe ejecutivo + dossier + CSV) ->
     para-abogado.zip.

### Contraste campo a campo

- id: NO existía. La misión se identificaba informalmente ("caso Indra").
- goal: existía implícito; nunca declarado como resultado verificable.
- status/current_node: NO existían. Durante la ejecución no se sabía
  formalmente en qué fase se estaba; se sabía por conversación.
- completed/pending: NO declarados. Se sabía informalmente.
- retries: SÍ hubo reintentos reales (corrección del nombre del
  trabajador, revisión conjunta que amplió funciones) pero manuales, sin
  registro de motivo.
- inputs/outputs: cada fase los tenía de facto (evidencias_raw.json ->
  top40 -> caso) pero no declarados como contrato.
- evidence: SÍ. Archivos generados por fase (JSON, CSV, PDF, ZIP). El caso
  dejó evidencia real y verificable.
- checkpoints: NO existían. Si el proceso se interrumpía, se rehacía la
  fase. Los archivos intermedios actuaban de estado de facto, sin
  reanudación declarada.
- shared_state: existía de facto (archivos intermedios entre fases), pero
  sin contrato ni garantía de integridad.

### Propiedades de ejecución que el caso REQUERÍA (árbol sección 7)

- Estado compartido entre fases: SI (output de cada fase = input de la
  siguiente). -> Mission Runner
- Backtracking: SI (la revisión humana podía invalidar partes de la fase 3
  y obligar a buscar más pruebas en fases 1-2). -> Mission Runner
- Retries semánticos: SI (reintentar la extracción con patrones nuevos al
  descubrir una pista, p.ej. ServiceNow logs). -> Mission Runner
- Ramas condicionales: SI (la selección "10 incontestables > 40 buenas"
  es una decisión condicional sobre el resultado de la fase 2). ->
  Mission Runner
- Paralelismo: SI potencial (los 3 buzones, 5.285+1.743+1.517 correos,
  podían extraerse en paralelo). -> Mission Runner
- Checkpoints: SI (8.545 correos; interrumpir y rehacer la extracción
  entera era inaceptable). -> Mission Runner

Resultado: el caso requiere Mission Runner por 6/6 propiedades del árbol.
El pipeline lineal actual funcionó, pero sin estado declarado: cada script
releía archivos intermedios, no había registro de fase, no había
reanudación y los reintentos eran manuales. Esto confirma que el hueco que
motivó el contrato es real y que el esquema lo cubre.

### Qué revela el caso que el esquema NO contemplaba

1. Nodos humanos explícitos: la revisión con el trabajador (roleplay
   judicial) fue un nodo humano obligatorio entre fases. El contrato tiene
   la transición en_espera, pero conviene declarar "input humano" como un
   tipo de espera explícito (esperando: humano | servicio | recurso).
2. Evidencia por fase como archivo físico: la evidencia del caso era un
   artefacto por fase (JSON, CSV, PDF, ZIP). El contrato debe permitir que
   evidence apunte a rutas de archivo, no solo a texto.
3. La selección no era solo por score: la puntuación (fase 2) alimentaba
   una decisión cualitativa (fase 3) con criterio humano. El contrato debe
   soportar que un nodo humano consuma el output de un nodo determinista.

### Ajustes al esquema derivados de la validación

- Añadir al estado: `waiting_on` (humano | servicio | recurso) para
  distinguir el tipo de espera en la transición en_espera.
- Añadir al contrato: evidence puede ser ruta de archivo o texto.
- Declarar explícitamente que un nodo puede ser humano (revisión,
  validación) y que su input/output se registra igual que el de un nodo
  determinista.

Con estos tres ajustes, el contrato cubre el caso Indra 2026 sin forzar
nada. El siguiente paso natural es formalizar el esquema ajustado como
mission.schema.json en lpa/contracts/ y decidir el motor (n8n para lo
visual, Python para lo que n8n no cubre).

---

## 13. Decisión de motor y borrador de la RULE de activación (07-ago, propuesta sin adoptar)

### 13.1 Motor por misión (paso 4)

Regla práctica confirmada (ya estaba en la sección 8, ahora explicitada):

- n8n: misiones que YA viven en workflows existentes del lab (12 workflows)
  o que son visuales por naturaleza. El contrato documenta su estado.
- Python (Mission Runner Python): solo lo que n8n no cubre — LM Studio,
  RAG, delegación a subagentes, lógica con archivos por fase.
- Caso Indra 2026 (primer candidato real): motor PYTHON (necesita RAG,
  LM Studio para la puntuación, archivos intermedios JSON/CSV/PDF/ZIP y
  potencial delegación). n8n no lo cubre sin forzar nodos.

### 13.2 Borrador RULE-010 (paso 5) — "Activar el Mission Runner solo si la misión lo REQUIERE"

Formato 01-knowledge/objects, propuesta sin adoptar (no es KO activo aún):

```yaml
id: RULE-010
type: RULE
status: draft
version: 1
created: 2026-08-07
last_validated: 2026-08-07
next_review: 2026-11-07
expires: 2027-02-07
title: "Activar el Mission Runner solo cuando la misión lo REQUIERA"
desc: >
  Ante una solicitud de tipo orquestacion (pipeline, misión, caso
  multi-fase), decidir el motor de ejecución por PROPIEDADES de la misión,
  no por número de fases. El Mission Runner solo se activa si la misión
  REQUIERE al menos una de: estado compartido entre fases, backtracking,
  reintentos semánticos, ramas condicionales, paralelismo real o
  checkpoints. Si ninguna se requiere, la misión es un pipeline lineal y se
  ejecuta con el mecanismo actual, sin Runner.
confidence: 0.8
confidence_label: ALTA
evidence: [research/mission-contract-diseno.md]
dependencies: [RULE-001]
contradicts: []
superseded_by: null
domain: ai-architecture
scope: todo_joko_lab
monitoring:
  metric: misiones_que_requieren_runner_vs_activas
  baseline: null
  current: null
  last_checked: null
history:
  - date: 2026-08-07
    event: created
    note: >
      Borrador propuesto (paso 5 de mission-contract-diseno); sin adoptar.
      Matiz "requiere, no podría" validado contra el caso Indra 2026 (6/6
      propiedades requeridas). Motor propuesto: Python para el caso Indra.
legacy_fields:
  condicion:
    tipo_tarea: [orquestacion]
    keywords: [misión, pipeline, fases, caso, orquestar]
  accion:
    accion: decidir_motor_por_propiedades
    params:
      runner_requerido: [estado_compartido, backtracking, retries_semanticos,
        ramas_condicionales, paralelismo, checkpoints]
      matiz: "la misión lo REQUIERE, no 'podría tenerlo'"
  prioridad: 80
  canal: no_engine
  canal_nota: >
    Regla de gobernanza de ejecución; su canal es la decisión del
    Router/clasificador de misiones, no el Activation Engine de modelos.
```

Pasos 4-5 CERRADOS (07-ago): motor confirmado y RULE-010 adoptada
(01-knowledge/objects/RULE-010.yaml, OP-20260807-030). El Mission Runner en
sí se construirá cuando exista una misión real que lo requiera (la sección
11 define qué lo falsearía); el contrato, el esquema y la regla ya están.
