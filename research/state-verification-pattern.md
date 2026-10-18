---
title: "SVP v2 — State Verification Pattern (Gate-001)"
type: research
---

# SVP v2 — State Verification Pattern (Gate-001)
**VERACIDAD:** [ALCANCE INTERNO]

**Clase:** Procedural Gate obligatorio (no recomendación)
**Estado:** OBS → HIP → EXP pendiente. Origen: fallo 06-ago-2026 (revisión de analisis-hermes-quicksilver.md sin contrastar el estado real)
**EVF:** evolution_id SVP-001 — ficha en 04-operations/metrics/evolution.jsonl; validación según research/evolution-validation-framework.md (5 niveles)

**state_sources (SVP Fase 2):**
- hermes-lab/docs/pendientes.txt
- 04-operations/metrics/svp_exp.jsonl
- research/evolution-validation-framework.md
**last_state_check:** 2026-08-06

## Principio

Ningún documento con conocimiento de estado puede darse por revisado sin demostrar que ha consultado la fuente de verdad. Sin SVP REPORT, la revisión NO EXISTE.

## Fase 1 — Clasificación (obligatoria)

Al abrir un documento, responder antes de continuar:

```
¿Contiene conocimiento de estado?
[ ] NO   → revisión normal
[ ] SI   → SVP obligatorio
```

Estado = versiones, decisiones, políticas, configuración, modelos, cron, despliegues, rutas activas, reglas vigentes. No se continúa hasta responder.

## Fase 2 — Declaración de fuentes (obligatoria)

Frontmatter del documento:

```yaml
state_sources:
  - hermes-lab/docs/pendientes.txt
  - joko-lab/04-operations/proposals/
  - lab-state/logs/decision.log
  - ~/.hermes/shared-events.jsonl
last_state_check: 2026-08-06
```

Si un documento tiene estado y no declara fuentes → SVP FAIL. No puede revisarse. El documento declara qué debe consultarse; no depende de la memoria del revisor.

**Exención de Fase 2 (hallazgo EXP SVP-001, 06-ago):** la obligación de state_sources aplica a documentos cuyo estado NO está ya gobernado por otro mecanismo. Quedan exentos (no duplicar gates):
- KOs con Evidence Contract (Gate-002): su `evidence` con orígenes ya cumple la función
- Banco de evaluación: su regla interna obliga a `fuente` por item
- Fuentes canónicas mismas (pendientes.txt, decision.log): son la fuente, no la declaran

## Fase 3 — Detección automática

Buscar marcadores antes de revisar: `?`, `TODO`, `FIXME`, `XXX`, `pendiente`, `confirmar`, `verificar`, `sin confirmar`, `por decidir` (+ los que se definan).

Si existe uno → SVP entra en modo RESOLVER (no modo revisión). No existe revisión: existe una tarea de resolución.

## Fase 4 — Contraste con trazabilidad

Cada marcador obliga a escribir:

```
Marcador:       0.19?
Fuente:         pendientes.txt
Resultado:      0.17.0 instalado; esperar 0.20.1
Acción:         documento actualizado
```

No basta escribir "consultado" — la trazabilidad es el requisito.

## Fase 5 — SVP REPORT (evidencia de cierre)

```yaml
SVP REPORT
Documento:          analisis-hermes-quicksilver.md
Tipo:               Estado
Fuentes consultadas: [x] pendientes.txt [x] decision.log [ ] shared-events.jsonl
Marcadores encontrados: 3
Marcadores resueltos:    3
Marcadores pendientes:   0
Resultado:              PASS
```

Sin este bloque, la revisión no existe (SVP FAIL). La evidencia es el bloque escrito por el revisor, NO la salida de un detector automático: TD-001 da falsos negativos y no es fiable como mecanismo de cierre (mismo patrón que los verifiers ad-hoc del lab).

## Observación Goodhart (integrada en el diseño)

Medir solo "marcadores pendientes = 0" incentivaría dejar de escribir marcadores (la incertidumbre desaparece del documento, no del razonamiento). Por eso se miden dos variables independientes:

- **SVP-A:** marcadores DECLARADOS — vigilar caída brusca tras implantar SVP = posible ocultación de incertidumbre
- **SVP-B:** marcadores RESUELTOS / declarados — objetivo 100%

Solo con ambas se distingue mejora real de ocultación.

## Plan de validación (EXP)

- Aplicar SVP a las próximas 10 revisiones de documentos con estado (o 1 semana)
- Éxito: 0 revisiones aprobadas con marcadores sin resolver; 100% fuentes consultadas; SVP-A estable (sin caída brusca de marcadores declarados)
- Si cumple → promover a RULE (OBS→HIP→EXP→DEC→RULE)

### Métricas de la EXP (ampliadas, alimentan MEL)

| Métrica | Qué mide | Objetivo |
|---|---|---|
| Documentos revisados | volumen | registro continuo |
| Documentos con estado | clasificación correcta | 100% correcta |
| Marcadores encontrados | honestidad (SVP-A) | estable, sin caída brusca |
| Marcadores resueltos | eficacia (SVP-B) | 100% de los declarados |
| Fuentes realmente consultadas | cumplimiento | 100% declaradas |
| Tiempo de resolución | coste | registrar (baseline, sin umbral a priori) |
| Reaperturas posteriores | calidad | 0 |

### Registro de la EXP (operativo)

Cada revisión de un documento con estado escribe UNA línea en:
`04-operations/metrics/svp_exp.jsonl`

Esquema fijo (JSONL, una línea por revisión):

```
{"date": "YYYY-MM-DD", "doc": "<ruta>", "tipo": "estado|descriptivo",
 "clasificacion_ok": true|false, "marcadores": N, "resueltos": N,
 "pendientes": N, "fuentes_declaradas": N, "fuentes_consultadas": N,
 "tiempo_s": N|null, "resultado": "PASS|FAIL", "reapertura": true|false,
 "new_defect_found": true|false, "defect": "<tipo>|null"}
```

- `tipo` = clasificación de la Fase 1 (estado o descriptivo)
- `clasificacion_ok` = si la clasificación fue correcta
- `marcadores` = encontrados (SVP-A) · `resueltos` = resueltos (SVP-B) · `pendientes` = no resueltos
- `fuentes_declaradas` = state_sources del documento · `fuentes_consultadas` = realmente consultadas
- `tiempo_s` = tiempo detectar→resolver (null si no hubo marcadores). **Operativo desde 06-ago:** en las revisiones futuras se rellena con segundos reales medidos en la sesión (el gap del baseline era null por diseño; a partir de ahora se registra para completar la métrica de coste del EVF)
- `resultado` = PASS solo si pendientes=0 y fuentes_consultadas>=declaradas
- `reapertura` = si el documento se reabrió tras darse por revisado
- `new_defect_found` / `defect` = si la revisión descubrió un defecto que había pasado desapercibido (missing_state_sources, obsolete_reference, unresolved_marker, ...). Es la métrica de UTILIDAD del procedimiento, no de estabilidad.

Baseline registrado 06-ago-2026 (incidente original + su corrección) para que la EXP arranque con punto de partida real, no en blanco.

### Detection Yield (DY) — métrica de utilidad

```
DY = defectos descubiertos (clases únicas) / revisiones realizadas
```

Mide la **capacidad del procedimiento para descubrir defectos**, no solo cuántos PASS produce. Un procedimiento que nunca encuentra nada puede ser simplemente innecesario. DY parcial de la EXP (06-ago): 1 clase única (missing_state_sources) / 7 revisiones = 0,14.

### Criterio de promoción a RULE (dos condiciones, ambas necesarias)

- **Condición A (estabilidad):** el benchmark pasa — 10 revisiones, 0 marcadores abiertos.
- **Condición B (utilidad):** durante la EXP se detectó al menos un defecto real (missing_state_sources, obsolete version, missing source declaration, ...).

Sin la condición B, un SVP con 10/10 PASS pero que nunca encontró nada no demuestra valor: podría ser un procedimiento innecesario.

## Casos que motivan el patrón (verificado 06-ago)

| Caso | Capa | Evidencia |
|---|---|---|
| 1. Documento antiguo recuperado antes que el vigente | RAG | pendientes.txt: "vigencia OKF Fase B pendiente"; retrieval por defecto no aplica vigencia |
| 2. Campos expires/superseded_by/status existían, pipeline no los usaba | KOs | search.py: --status es filtro OPCIONAL (solo si el revisor lo pide); expires no participa en absoluto |
| 3. Marcador "0.19? — verificar versión" sin contrastar | Revisión documental | Incidente 06-ago: pendientes.txt decía 0.17.0/esperar 0.20.1 |

Patrón común: **la información de estado existe pero no participa obligatoriamente en la decisión.**

## Clase de defecto adicional descubierta (06-ago, tras la EXP)

| Clase | Descripción | Cómo se detectó | ¿La cubre el gate? |
|---|---|---|---|
| `referencia_ko_no_verificada` | Un ID de KO mencionado en prosa (p. ej. "RULE-CONF-001") no resuelve a un fichero real | Manualmente, al revisar DEC-004 (el revisor notó que el KO citado no existía) | NO — SVP-001 solo caza missing_state_sources; KVC-001 no verifica integridad referencial de IDs citados |

**Lección (importante):** la transparencia del revisor (declarar el hallazgo) no equivale a que el gate lo detecte. Este defecto NO habría sido cazado por SVP-001/KVC-001 tal como están definidos: ninguno comprueba que los IDs referenciados (en campos estructurados o en prosa) resuelvan a un fichero real — es integridad referencial, tipo foreign key, una clase distinta.

**RESUELTO (07-ago-2026):** extendido el SVP con comprobación de integridad
referencial (FK), tras el EVF completo (ficha `research/fk-integridad-referencial-evf.md`,
EXP-FK-001 con DY positivo). Ver sección al final. Corregido en DEC-004 (06-ago):
referencia falsa eliminada.

## Limitación conocida (Gate-005 pendiente)

SVP cubre la revisión de DOCUMENTOS. El Caso 1 (retrieval) no es un documento con marcador: es una consulta que ignora vigencia. Eso requiere un Gate-005 de retrieval (la vigencia participa por defecto en toda consulta RAG), no SVP. Diseño pendiente.

## Integridad referencial (FK) — gate ADOPTADO (07-ago-2026)

El SVP incluye desde el 07-ago la comprobación de integridad referencial para
la clase de defecto `referencia_ko_no_verificada` (un ID de KO citado que no
resuelve a un fichero real).

Reglas del gate:
- BLOQUEANTE: campos estructurados de KOs (`dependencies`, `superseded_by`,
  `contradicts`) con ID de KO inexistente.
- BLOQUEANTE: wikilinks `[[ID]]` en documentos que no resuelven a un
  KO/observación/hipótesis real.
- AVISO (no bloquea): menciones sueltas en prosa (pueden ser históricas o
  ejemplos de diseño; caso DEC-004/RULE-CONF-001).

Instrumento: `tools/verificar_fk_kos.py --gate` (exit 1 si hay bloqueantes).
IDs válidos: `objects/*.yaml` + `observations/*.md` + `hypotheses/*.md`;
excluye `.bak-*`. Verificado 07-ago: corpus limpio (0 bloqueantes, exit 0).
