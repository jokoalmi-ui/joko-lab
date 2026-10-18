---
type: candidate_pattern
id: CP-014
status: incubating
created: 2026-10-16
confidence: E0 (4 filas de incidencia / 3 jobs / 1 evento raíz, en una sola ventana)
domain: automatizacion-del-lab / cadenas-de-jobs
---

# CP-014 · El fallo de una cadena de jobs se registra en el consumidor, no en el origen

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-16
> **Origen:** Ciclo semanal LPA, ventana 09→16-10-2026 (acta `incidentes/revision-fallos-2026-10-16.md`, decisión D2)
> **Nivel de confianza:** E0 (mecanismo claro y medido, pero **procede de un solo evento raíz**; las 4 filas son 2 jobs consumidores + 1 reintento triple)

---

## 1. Patrón candidato

Cuando un job **consume el producto** de otro job, y ese producto no existe, el fallo aparece en el registro **a nombre del consumidor**: la fila de incidencia pertenece al job que se queja, su `failure_type` es el del consumidor (`script`) y el conteo crece con cada reintento. Un solo evento aguas arriba se convierte en **N filas de incidencia y en «N fallos»** para quien cuente filas.

Matiz medido que acota el patrón: **el registro no es ciego al origen**. El texto del error nombra el producto ausente con su ruta completa (`fuente_ausente: no existe …/20261015-informe-local.txt`). Lo que no distingue es la **atribución**: la fila es del consumidor, el tipo es «fallo de su script», y el diagnóstico correcto exige mirar aguas arriba. Formulación operativa: **ante el fallo de un job que depende de otro, la primera pregunta no es «¿qué le pasa a este job?» sino «¿existe el producto del que depende?»**.

## 2. Contextos / dominio(s)

Automatización del lab (Hermes cron). Un productor y dos consumidores de propósito y cadencia distintos:

1. `67d5fcc5b69e` — **informe-diario-joko-lab (LOCAL gpt-oss)**, `0 9 * * *` (productor).
2. `210486645f20` — **Orquestador batch diario (local-first)**, `1 12 * * *` (consumidor, 1 intento registrado).
3. `380a80273240` — **Orquestador recuperacion horaria**, `15 * * * *` (consumidor, 2 intentos registrados el mismo día).

## 3. Evidencia (ocurrencias)

Medido en solo lectura sobre `~/.hermes/cron/executions.db` (`cron_incidents`, 19 filas) el **16-10-2026**. Las cuatro filas son de la jornada del 15-10:

| fila | job (tipo) | hora | texto literal (recortado) | intento |
|---|---|---|---|---|
| `67d5fc_dbacfe302a08` | informe-diario (productor) | 15-10 09:01:35 | `Script exited with code 1 · stderr: ⚠️ resumen inválido (razonamiento o error de motor) → degradado · informe-diario-local.sh: línea 60: $2: variable sin asignar` | — |
| `210486_ede8adb4a5b0` | Orquestador batch diario (consumidor) | 15-10 12:01:37 | `orquestador-batch: FALLO (fuente_ausente: no existe …/20261015-informe-local.txt) en 'informe-json' · intento 1/3` | 1/3 |
| `380a80_98511e9854f8` | Orquestador recuperación horaria (consumidor) | 15-10 13:15:37 | idem · `intento 2/3` | 2/3 |
| `380a80_40b200f10c09` | Orquestador recuperación horaria (consumidor) | 15-10 14:15:37 | idem · `intento 3/3` | 3/3 |

- **1 causa → 4 filas en 3 jobs.** La causa raíz fue una sola: un bug del productor (variable sin asignar en la línea 60 de `joko-lab/tools/informe-diario-local.sh`), que no dejó el informe diario del 15-10.
- **Los consumidores nunca estuvieron rotos**: al cerrarse el caso siguen en `last_status: ok` / `failure_streak: 0` **sin haber sido tocados**. El arreglo fue del productor (mtime del script 15-10 15:47) y se regeneró el producto a mano (15:49).
- **Los reintentos del mismo fallo cuentan como filas distintas**: la escalera `1/3`, `2/3`, `3/3` son tres filas del mismo error en el mismo archivo ausente. El conteo de incidencias de la ventana (5 nuevas) incluye 3 filas que son **un** problema.
- **Los cierres se reparten**: las dos filas del orquestador horario se cerraron a la vez (`closed_at` 15-10 15:15:37) y la del batch diario **al día siguiente** (`closed_at` 16-10 12:02:41, en su primera corrida sana) → el cierre mide «hubo una corrida sana después», no «la causa está reparada» (ver CP-010).
- **Coste real del efecto de atribución:** el productor se detectó y arregló en 6 h 45 min (09:01 → 15:47), mientras las incidencias del consumidor seguían abriendo filas nuevas cada hora con el mismo texto.

## 4. Mecanismo propuesto

Una cadena de jobs acopla dos contratos asimétricos: el consumidor verifica la EXISTENCIA del producto (lo hace bien: falla ruidosamente y nombra la ruta), pero el registro de incidencias es **por job ejecutado**, no por relación de dependencia. Como consecuencia: (a) el sujeto de la fila es el consumidor, (b) el `failure_type` describe el modo en que el consumidor murió (script/exit 1), no la causa, y (c) cada reintento abre o actualiza una fila con firma propia. El operador que cuenta filas o filtra por `job_id` obtiene una imagen del efecto, no de la causa; y el job que realmente hay que arreglar (el productor del producto ausente) aparece en el registro con una única fila que a menudo pasa desapercibida contra el ruido de sus N consumidores.

## 5. Condición de falsación

Sería **FALSO** si, sobre **N=10 fallos de jobs que consumen el producto de otro job**, en **2 ciclos LPA consecutivos**, **8 o más** tienen como causa raíz el propio consumidor (su script, sus permisos, su configuración) y no el producto aguas arriba, o si el registro resolviera la cascada por sí solo (**1 fila por causa**, con el productor como sujeto de la incidencia). Es decir: si el fallo en cadena fuera la excepción, o si el instrumento ya contara causas en vez de efectos, el patrón no se sostiene.

Segunda vía: si en la próxima ocurrencia el conteo de incidencias de la ventana coincide con el número de causas raíz (0 filas infladas por reintentos), la parte «conteo» de este patrón queda falsada y solo sobrevive la de atribución.

## 6. Antídoto propuesto (sin medir)

1. **Producto aguas arriba primero:** ante el fallo de un job que depende de otro, comprobar la existencia/fecha del producto del que depende **antes** de leer el estado del consumidor.
2. **Contar causas, no filas:** al medir una ventana, agrupar las filas de `cron_incidents` por causa raíz (producto ausente + texto de error normalizado); los reintentos (`intento n/N`) del mismo texto son 1 causa.
3. **Registrar la dependencia en la fila:** el consumidor ya nombra la ruta ausente; el paso siguiente (no implementado) es etiquetar la fila con el job productor para que el conteo por causa sea automático.
4. **Que el productor tenga su propia comprobación:** si el producto de un job alimenta a otros, su ausencia debe ser una incidencia de P0 en el productor (aquí el productor se arregló a mano 6 h 45 min después, mientras los consumidores seguían abriendo filas).

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1 (falta: el mismo mecanismo en ≥2 eventos raíz independientes, y un segundo dominio)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto «producto aguas arriba primero» **ya se aplica** en el ciclo desde esta ventana, pero sin documento propio)
- [x] Sigue en incubación
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-013** — la ventana de apagado desplaza el producto del día y dispara cadenas de consumidores, aunque aquí el desplazamiento no fue la causa; y **CP-010** — el cierre repartido entre consumidor y productor mide «corrida sana después», no causa reparada)

**Fecha de revisión:** 2026-10-23 (ciclo semanal siguiente) y 2026-11-02 (mensual).
**Justificación:** el mecanismo está medido con texto literal y con los cierres repartidos, y supera el umbral de 2 ocurrencias (4 filas / 3 jobs); pero **las 4 filas nacen de un solo evento raíz**, así que la evidencia de generalidad es débil por definición. Se declara E0 y se fija reexamen corto para buscar un segundo evento raíz independiente.
