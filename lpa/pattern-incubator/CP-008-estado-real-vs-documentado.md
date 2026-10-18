---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-02
---
# CP-008: Estado real ≠ estado documentado (auditar contra el sistema)

**ID:** CP-008
**Fecha:** 2026-09-02
**Estado:** E0 — Candidate Pattern
**Origen:** Auditoría punto por punto del lab (02-09) — 8 divergencias encontradas el mismo día

---

## 1. Qué ocurrió

El 02-09 se auditó el lab componente por componente (14 bloques, todo con salida real) por la sospecha de "cosas desconectadas/desfasadas". Resultado: 8 divergencias entre el estado DOCUMENTADO/REGISTRADO y el estado REAL, en dominios distintos:

- **Servicio roto 13 días sin aviso:** joko-backup.service fallaba cada noche desde el 20-08 ("refspec inválido") y ningún watchdog avisó; el doc de decisión (2026-07-10) seguía pareciendo vigente.
- **Documento afirmando lo contrario de la realidad:** el doc de revisión generado el 01-09 a las 23:50 decía "kanban VACÍO — nunca usado", cuando a las 22:02-22:14 ya había 2 pilotos kanban completados (11 tareas done).
- **Fuente canónica caducada:** pendientes.txt (la fuente de verdad del lab) tenía cabecera "Actualizado 06-08" y la línea HERMES UPGRADE decía "0.21.0 SIGUE SIN SALIR" cuando v0.21.0 se ejecutó el 01-09.
- **Métrica de salud en 0 sin que nadie lo notara:** KNOWLEDGE HEALTH 0/100 (24 observaciones de telemetría mal clasificadas como DEC por una subcadena en el nombre) — nadie ejecuta el health periódicamente.
- **Código activo sin versionar:** pipeline_proxy.py llevaba +2 líneas (cache tokens) modificadas el 01-09 sin commitear; el servicio corría el cambio pero el repo y los bundles no lo tenían.
- **Escritura de memoria perdida:** a las 09:46 una operación batch de memoria falló (la entrada a borrar ya no existía — carrera entre sesiones); con MEMORY/USER al 99% es esperable que se repita.
- **Config que no hace lo que dice:** web.extract_backend=ddgs (backend solo-búsqueda) — cualquier sesión que intente extraer URLs falla (ocurrió a las 11:32).
- **Logs con avisos ignorados:** el errors.log registraba los fallos del día (sanitizer, curator, extract) sin que nadie los leyera hasta la auditoría.

**Ampliación 2026-09-18 (ciclo semanal LPA; ventana 14→18 sep) — 2 divergencias más, verificadas, en dominios nuevos:**

- **Una cadencia documentada que no es la del motor.** La consolidación `revision-fallos-2026-09-14.md` cierra con «Semanal: 2026-09-21 (lunes)», pero el job real (`lpa-revision-incidentes-semanal`, leído en `~/.hermes/cron/jobs.json`) tiene expresión `30 14 * * 5` → **viernes** 14:30, con `next_run_at` 2026-09-25. El documento de gobernanza declaraba mal su propio disparador; hoy (viernes 18-09) el motor ha vuelto a ejecutarlo, confirmando la cadencia del motor. Sin saber qué se editó primero, el criterio es el del motor: es la fuente de verdad.
- **Estado de negocio ≠ estado registrado.** El pipeline diario de fichas genera y envía la ficha, pero la fila del registro (`uso_diario`) falta para 5 fichas de la ventana: 10, 11, 12, 13 y 15-sep (el 15-sep ya constaba como «Pendiente: confirmación del usuario para registrar el uso»). Además, el 08-sep la carpeta del día dice `Perseus` y el registro dice otra cosa (nombre discordante). Decisión del usuario (18-09): NO corregir la BD hacia atrás → divergencia **conocida y aceptada**, que deja de ser incidente abierto pero sigue siendo ejemplo canónico del patrón.

**Ampliación 2026-09-25 (ciclo semanal LPA; ventana 18→25 sep) — 2 divergencias más, esta vez entre el registro DECLARADO y el registro que realmente se escribe:**
- **Dos registros de lo mismo, y el declarado es el que no crece.** `04-operations/metrics/lecciones_ledger.jsonl` (el registro de lecciones que este ciclo alimenta): **9 líneas / 7.987 B, mtime 18-sep 14:40**, sin un solo cambio en 7 días. El registro que SÍ recibe las lecciones del lab en la misma ventana: `~/.hermes/skills/.curator_ledger.jsonl`, **1.282 líneas**, con actividad todos los días de la ventana y **36 entradas `actor: curator` solo el 25-09**. El propio acta del 24-sep lo dice con todas las letras («Lecciones en skills: NO se escriben aquí […] Traza: `.curator_ledger.jsonl`, ids `4a55249e29b0`, `4fa91bace86c`, `e03e1576f508`»). Un lector que consulte el registro declarado concluye que el lab no ha aprendido nada en una semana; el que consulte el otro, lo contrario.
- **El resumen de estado del propio gobernador no refleja lo que escribe.** `hermes curator status` (medido el 25-09 a las 14:3x) → **`curator: PAUSED`**, `runs: 13`, `last report: ~/.hermes/logs/curator/20260923-170843` (23-sep), mientras su ledger registra **36 entradas `actor: curator` del 25-09**, de 05:47:50 a 11:34:35 UTC. El campo de estado (pausa programada) y el registro de actividad (mutaciones que escribe cada sesión) describen cosas distintas con la misma palabra «curador», y el desfase se lee como contradicción. No se establece cuándo ni quién lo pausó (el último informe del curador es del 23-sep): se registra la divergencia medida, no una causa.

## 2. Evidencia que lo respalda

- 8 ocurrencias el MISMO día (02-09) en dominios distintos: systemd, kanban, docs canónicos, health del conocimiento, repo git, memoria, config, logs.
- Reglas previas del lab que ya apuntaban a esto: SVP (state-verification-pattern, 06-ago) — "ningún documento con estado puede darse por revisado sin consultar la fuente de verdad"; y el backlog como documento con estado corregido 4 veces (14/21/25-ago).
- Las 4 correcciones del backlog (14, 21 y 25-ago) son la MISMA divergencia: documentos escritos con el conocimiento del día que no se actualizan solos.
- Ampliación 18-09: `~/.hermes/cron/jobs.json` → job `lpa-revision-incidentes-semanal`, expresión `30 14 * * 5`, `next_run_at` 2026-09-25, frente al «2026-09-21 (lunes)» de `revision-fallos-2026-09-14.md` (§6, Próxima revisión); `04-operations/backlogs/pendientes.md` líneas 82-85 (18-sep 08:02) para las 5 fichas sin fila en `uso_diario` y la decisión de no corregir la BD.
- Ampliación 25-09: `wc -l` + `stat` de `04-operations/metrics/lecciones_ledger.jsonl` (9 líneas, 7.987 B, mtime 18-sep 14:40; backup propio `.bak-20260925` antes de escribir en él) frente a `wc -l` de `~/.hermes/skills/.curator_ledger.jsonl` (**1.282 líneas**; conteo por actor y fecha: **36 entradas `actor: curator` del 25-09**, ts mínimo 05:47:50.448327+00:00, máximo 11:34:35.343375+00:00). `hermes curator status` literal (`curator: PAUSED`, `runs: 13`, `last report: ~/.hermes/logs/curator/20260923-170843`). `pendientes.md` 24-sep (líneas 290-302) para la traza de las 3 lecciones escritas en skills y el «no se escriben aquí».

## 3. Contradicciones o limitaciones

- Auditar TODO contra el sistema en cada afirmación es costoso (tiempo, comandos) e inviable en conversación fluida.
- No toda divergencia es dañina (algunas son cosméticas: cabecera sin actualizar); el daño aparece cuando se ACTÚA sobre el dato viejo (decisiones, promociones, commits).
- El watchdog perfecto no existe: las divergencias de contenido (un doc dice X, el sistema dice Y) no se detectan por tamaño/fecha, requieren semántica.

## 4. Principio que parece emerger

> La fuente de verdad es el SISTEMA (disco, servicios, versión instalada, salida real, estado del repo), no el documento, el registro ni la memoria. Todo documento con estado caduca por defecto; antes de afirmar o actuar sobre un dato de estado hay que contrastarlo contra el sistema. Y las métricas de salud solo sirven si alguien las ejecuta periódicamente y actúa sobre ellas: una métrica en 0 que nadie mira equivale a no tener métrica.

## 5. ¿En qué otros proyectos podría aplicarse?

- Todo lab/operación con documentación de estado (versiones, servicios, config, cron).
- Pipelines con health checks que no se ejecutan en CI/watchdog.
- Repos donde el código activo puede divergir del versionado (falta de disciplina de commit o de CI).
- Cualquier sistema multi-sesión donde varias sesiones escriben el mismo estado (memoria, pendientes, backlog).

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería FALSO si: durante 2 ciclos LPA consecutivos (2 meses), un muestreo de 10 afirmaciones de estado extraídas de documentos del lab contra su fuente real NO encuentra ninguna divergencia relevante (que hubiera llevado a una acción incorrecta de haber actuado sobre el documento).

## 7. Decisión

Incubar (E0). Primera revisión en la revisión periódica del ciclo LPA (mensual).

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [x] Sigue en incubación (falta evidencia) — **revisado el 2026-10-02**: sigue, con **+1 ocurrencia** en la ventana 25-09→02-10. `hermes curator status` declaraba `PAUSED` mientras el ledger del curador sumaba 703 operaciones en 7 días (el documento de estado y la fuente real divergen), y D9 del acta 25-09 ya había corregido la fecha de esta revisión (doc: «lunes» / motor: viernes 14:30). Su antídoto (muestreo periódico documento↔fuente) sigue siendo distinto del de CP-009 (disparador) y CP-010 (etiqueta de validez) → **no se fusiona**
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón (candidato: SVP / CP-007 audit-before-acting / **CP-009 instrumento-sin-forzado** — solape parcial: CP-008 cubre la divergencia documento↔sistema, CP-009 cubre el mecanismo que nadie dispara. **Añadido 18-09: CP-010 instrumento-no-validado-miente** — CP-008 compara documento↔sistema; CP-010 dice que el MEDIDOR que produce el número también puede estar roto)

**Fecha de revisión:** 2026-11-02 (próxima mensual)
**Última revisión:** 2026-10-02 — sin ascenso: 13 ocurrencias pero **un solo experimento** y el antídoto sin medir (D10 del acta `revision-fallos-2026-10-02.md`).
**Justificación:** 8 ocurrencias en un solo día (02-09) + 2 verificadas el 18-09 (cadencia doc vs motor; BD vs registro) + **2 nuevas el 25-09** (el registro de lecciones declarado vs el que realmente recibe; el resumen de estado del curador vs su ledger de actividad) + 4 correcciones previas del backlog (mismo patrón) + regla SVP vigente = **12 ocurrencias**. Requiere validar el antídoto: watchdog periódico del estado (health, repo sucio, servicios failed).
