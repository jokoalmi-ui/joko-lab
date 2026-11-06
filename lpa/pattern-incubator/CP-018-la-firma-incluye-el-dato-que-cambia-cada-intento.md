---
type: candidate_pattern
id: CP-018
status: incubating
created: 2026-10-30
confidence: E0 (6 ocurrencias en 2 jobs distintos + 2 contrastes medidos en el mismo registro)
domain: gobernanza-del-conocimiento / observabilidad
---

# CP-018 · La firma de la incidencia incluye el dato que cambia en cada intento: el mismo fallo se registra como N incidencias y no acumula historia

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-30
> **Origen:** Ciclo semanal LPA, ventana 23→30-10-2026 (acta `incidentes/revision-fallos-2026-10-30.md`, decisión D1). Medido en solo lectura sobre `~/.hermes/cron/executions.db` (`cron_incidents`) y sobre `~/.hermes/hermes-agent/cron/incidents.py`.
> **Nivel de confianza:** E0 (dos jobs distintos y dos contrastes en el mismo registro; pero **un solo motor de incidencias** y el antídoto no está aplicado)

---

## 1. Qué ocurrió

Hermes cron deduplica incidencias con una firma calculada sobre el **texto del error**:

```python
# ~/.hermes/hermes-agent/cron/incidents.py
_MAX_SIGNATURE_ERROR_CHARS = 200                                    # línea 43
def _error_signature(job_id: str, error: str) -> str:                # línea 131
    normalized = _DURATION_RE.sub("#s", _normalize_error(error))[:_MAX_SIGNATURE_ERROR_CHARS]
    return hashlib.sha256(job_id.encode() + normalized.encode()).hexdigest()[:12]
```

`_DURATION_RE` normaliza **solo duraciones**. Todo lo demás —fechas, rutas, contadores, ids— entra tal cual en los primeros 200 caracteres. Si el error nombra un fichero con la fecha en el nombre, el mismo fallo produce una firma distinta cada día y el registro abre **una incidencia nueva por día** en vez de acumular en una sola.

Consecuencia medida: la incidencia diaria del `informe-diario` lleva **4 filas abiertas** (27, 28, 29 y 30-10) para **un solo defecto**, cada una con `first_seen_at == last_seen_at`. El registro no puede responder «¿desde cuándo falla?» ni «¿cuántas veces ha fallado?»: eso es exactamente lo que el registro existía para conservar. Y la métrica de salud empeora visualmente: 4 abiertas donde hay 1 problema.

## 2. Evidencia que lo respalda

**(1) `informe-diario-joko-lab` (`67d5fcc5b69e`): 4 filas por 1 defecto, y la única diferencia es la fecha de la ruta.**

| id | `first_seen_at` | `state` | texto (60 c) |
|---|---|---|---|
| `67d5fc_74c14f4af0d6` | 2026-10-27T09:04:35 | detected | `Script exited with code 3 stderr: FALLO: informe sin resumen` |
| `67d5fc_8bfe3bf75670` | 2026-10-28T09:04:37 | detected | ídem |
| `67d5fc_2b5c43c6a8c3` | 2026-10-29T09:04:36 | detected | ídem |
| `67d5fc_1e374c70107a` | 2026-10-30T09:04:20 | detected | ídem |

Error literal de la última (una sola escritura, texto continuo):

```text
Script exited with code 3
stderr:
FALLO: informe sin resumen verificado (GATE_OMITIDO) — revisar /home/jokoalmi/joko-lab/04-operations/reports/20261030-informe-local.txt
stdout:
Informe guardado: /home/jokoalmi/joko-lab/04-operations/reports/20261030-informe-local.txt
```

La ruta con la fecha (`20261027`…`20261030`) cae dentro de los primeros 200 caracteres. Misma causa, cuatro firmas.

**(2) `orquestador-batch` (`380a80273240`): 2 filas en la misma hora, y la única diferencia es el contador de intento.**

- `380a80_98511e9854f8` · `2026-10-15T13:15:37` · `… FALLO (fuente_ausente: no existe …/20261015-informe-local.txt) en 'informe-json' · intento 2/3`
- `380a80_40b200f10c09` · `2026-10-15T14:15:37` · `… FALLO (fuente_ausente: no existe …/20261015-informe-local.txt) en 'informe-json' · intento 3/3`

Mismo fichero, mismo día, mismo fallo, **una hora de diferencia y `intento 2` → `intento 3`**. Dos incidencias. Es el caso más limpio: el único dato que cambia es un contador interno.

**(3) Contraste donde la firma funciona: `empleo-pipeline` (`bbc1d841e8a7`).** Cuatro días seguidos de fallo (24→27-10, credencial OAuth revocada) → **una sola fila** (`bbc1d8_a5731c9ceec0`, `last_seen_at` avanzando hasta el 27-10 18:01). Su texto no contiene datos variables en el prefijo: la firma acumula como debe.

**(4) Contraste donde varias filas son legítimas: `rag-reindex-daily` (`da39a2148b34`).** 3 filas en 45 días (`fae8` timeout, `d27e` worker `-15`, `5636` timeout) = **tres causas distintas**, no un fallo repetido. Aquí el registro hace lo correcto.

**(5) Contexto del mismo registro:** 25 filas totales hoy — 21 `resolved`, 4 `detected`; **las 4 `detected` son las 4 filas de (1)**, es decir el 100 % de lo que el registro declara «abierto» es un solo defecto contado cuatro veces.

## 3. Contradicciones o limitaciones

- **Un solo motor de incidencias.** Los cuatro casos viven en Hermes cron; no hay un segundo sistema de registro donde comprobar la generalidad. La evidencia es de dos jobs del mismo lab y del mismo motor.
- **La semántica puede ser deliberada.** Deduplicar por texto exacto es defendible: «pisa el mismo error, no otro». El patrón no dice que la firma esté mal escrita; dice que **firma el texto cuando debería firmar la plantilla**, y que el efecto medido (4 abiertas por 1 defecto, cero acumulación de historia) contradice el uso que el lab hace del registro en sus actas.
- **El daño es de historia, no de detección.** Las 4 filas detectan el fallo perfectamente. Lo que se pierde es la serie temporal y la continuidad; el `failure_streak` de `jobs.json` (hoy 4) sí lo conserva por otra vía, lo que hace que el defecto sea fácil de no ver.
- **El antídoto toca el núcleo de Hermes** (`~/.hermes/hermes-agent/cron/incidents.py`). Aplica RULE-016 (no tocar Hermes sin 5 días de incidencias tras publicación) y requiere autorización explícita: **no se aplica en este ciclo**.
- **Frontera con CP-017** (el `resolved` que no significa reparado): comparten registro y familia —«el instrumento no mide lo que su etiqueta dice»—, pero el objeto es distinto: CP-017 es el criterio de **cierre**, CP-018 es la regla de **identidad** de la incidencia. Si CP-018 se reparase, CP-017 seguiría en pie (y al contrario).
- **No medido:** cuántas de las 25 filas nacieron de este mecanismo. Requeriría recalcular firmas normalizadas sobre los textos guardados, que es justo lo que el antídoto propone.

## 4. Principio que parece emerger

> Una firma de deduplicación debe calcularse sobre la **plantilla** del error, no sobre su texto. Si el prefijo firmado contiene datos que cambian en cada intento —fecha, contador de reintento, id de ejecución, ruta temporal— el mismo fallo se registra como N incidencias distintas y se pierde precisamente la información que el registro existía para conservar: **cuántas veces y desde cuándo**.
>
> Corolario de la métrica: un registro que se duplica por datos variables no solo pierde historia, **infla el indicador de salud**. Cuatro incidencias abiertas donde hay un defecto convierten una lectura de estado en una lectura falsa.

## 5. ¿En qué otros proyectos podría aplicarse?

- Agregadores de errores con *fingerprinting* (Sentry y equivalentes): es el mismo problema, y la solución comercial es exactamente la del antídoto — reglas de normalización antes de agrupar.
- Deduplicación en ETL/ingesta: claves calculadas sobre el mensaje completo duplican la carga cuando el mensaje lleva marca de tiempo.
- Auto-creación de tickets desde alertas (Jira/Linear): un contador en el mensaje convierte una alerta en diez tickets.
- Agrupación de alertas (Alertmanager/Grafana): sin normalización, el agrupado por etiqueta exacta falla igual.
- Cualquier tabla de incidencias propia: la identidad de un fallo debe ser (productor + causa), no (productor + texto literal).

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **10 fallos del mismo job cuya única diferencia esté dentro del prefijo firmado** (fecha, contador, id), en **8 o más** el registro acumula **una sola fila** con `last_seen_at` avanzando (en vez de N filas con `first_seen_at == last_seen_at`).

Falsación auxiliar del mecanismo: si al normalizar esos datos variables en los textos guardados el número de filas resultante **no cambia**, entonces la duplicación no la causa la firma y este patrón no explica lo observado.

También lo debilitaría (no lo falsa) que las 4 filas de (1) respondieran a causas distintas —hoy no es el caso: el error literal es el mismo salvo la fecha de la ruta.

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1 (falta: un segundo registro/motor, o el antídoto aplicado y medido)
- [ ] Asciende a procedures/ como procedimiento LPA (el criterio «normalizar antes de firmar» **ya se aplica en las actas** al leer el registro, pero no está documentado como procedimiento)
- [x] Sigue en incubación
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-017**, misma familia de instrumento; objetos distintos)

**Fecha de revisión:** 2026-11-02 (mensual). Se adelanta la revisión porque el antídoto requiere decisión sobre el núcleo de Hermes (RULE-016).
**Justificación:** 6 ocurrencias medidas en 2 jobs, más 2 contrastes en el mismo registro que aíslan la causa (una fila cuando el texto es estable; varias cuando las causas son distintas). Supera el umbral de 2, pero el registro afectado es único y el antídoto no está aplicado → E0.

**Antídoto propuesto (no aplicado; toca el núcleo de Hermes, requiere autorización explícita y RULE-016):**
1. Normalizar antes de firmar: fechas (`\d{4}-?\d{2}-?\d{2}`) → `{fecha}`, contadores de intento (`intento N/M`) → `{intento}`, ids de ejecución y rutas temporales → `{id}` / `{path}`.
2. Añadir a la fila un campo de ocurrencias (`occurrence_count`) que se incremente al reencontrar la firma, para que el historial sobreviva a la normalización.
3. Mientras no se toque el núcleo: **leer el registro contando firmas del mismo job + misma causa**, no contando filas (es lo que hace el acta del 30-10).


---

## Actualización 2026-11-06 (ciclo semanal LPA, ventana 30-10 → 06-11)

- **Nueva ocurrencia (7ª):** `67d5fc_438985bd1afe`, job `67d5fcc5b69e`, `first_seen` 2026-11-02 09:00:58, cerrada 2026-11-03 09:02:05. Error real: `exit 3 — FALLO: informe sin resumen verificado (GATE_OMITIDO)`.
- **Dato acumulado:** el job acumula **7 incidencias con 7 firmas distintas** (`count(*)=7`, `count(distinct error_sig)=7`), es decir el 100 % de las firmas son únicas para un único defecto.
- **Cierre en bloque:** las 4 filas del 27, 28, 29 y 30-10 se cerraron todas a la misma hora, `2026-10-31 09:03:06`, lo que confirma que se cierran por producto y no por causa.
- **Falsación (recordatorio):** si una firma deja de crear fila nueva con la fecha cambiada, el patrón deja de aplicar en ese job.
- **Acta:** `incidentes/revision-fallos-2026-11-06.md` (F1, D1). Backup de este expediente: `.bak-20261106`.
