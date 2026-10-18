---
type: candidate_pattern
id: CP-015
status: incubating
created: 2026-10-16
confidence: E0 (3 ocurrencias: 15 corridas sin artefacto + 2 falsos ok del vigía + 1 registro de punto ciego del usuario)
domain: automatizacion-del-lab / observabilidad
---

# CP-015 · La corrida que muere antes de escribir no deja artefacto: el vigía que solo lee artefactos no la ve

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-16
> **Origen:** Ciclo semanal LPA, ventana 09→16-10-2026 (acta `incidentes/revision-fallos-2026-10-16.md`, decisión D3). El caso del vigía fue detectado y registrado por el usuario ese mismo día (`pendientes.md`, «PUNTO CIEGO 3»).
> **Nivel de confianza:** E0 (mecanismo medido con evidencia dura, pero **un solo job silencioso** y un solo vigía)

---

## 1. Patrón candidato

Un **vigía** cuya señal de «¿falló este job?» es el **artefacto que el job escribe** (informe, log, resumen) tiene un hueco estructural: los modos de fallo que **matan la corrida antes de escribir** — OOM por cgroup, `SIGKILL`, corte de energía — son exactamente los que **borran la señal que el vigía sabe leer**. El resultado no es un falso negativo ruidoso, es **silencio**: no hay informe que abrir, y «no hay informe» no se distingue de «no había job».

Formulación operativa: **un vigía que decide leyendo el producto mide la producción, no la ejecución**. Para ver la corrida que murió antes de producir, necesita una segunda fuente que exista aunque el job no escriba nada (estado del job, registro de incidencias, o el contador de corridas esperadas vs informes presentes).

Formulación complementaria (borde del patrón): el mismo vigía también puede producir un **falso ok** si el formato de fallo cambia — sigue leyendo informes, pero no reconoce la señal que el informe trae.

## 2. Contextos / dominio(s)

Automatización del lab (Hermes cron), dos vigías distintos y dos jobs distintos:

1. **Vigía de informes** (`watchdog-informes-cron`, `~/.hermes/scripts/watchdog-informes-cron.py`) sobre los informes de salida de los jobs de cron.
2. **Job silencioso** (`9474f6f3d224`, `consolidador-sesiones`, `30 22 * * *`, `no_agent`).
3. **Job con informe fallido mal clasificado** (2 informes del 15-10, de `67d5fcc5b69e` y `210486645f20`).

## 3. Evidencia (ocurrencias)

Toda la evidencia es de solo lectura y verificada el **16-10-2026**:

- **(1) 15 corridas sin artefacto, invisibles para el vigía.** `~/.hermes/cron/output/9474f6f3d224/` tiene **47 ficheros** y el más reciente es `2026-09-30_22-31-54.md`: **las 15 corridas del 1 al 15-oct no dejaron ningún informe** (coincide con `failure_streak: 15`). La causa de la del 15-10 está en el kernel, verbatim: `hermes invoked oom-killer … oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/hermes-worker-cron-9474f6f3d224-exec-a0b9fd49024a4930a54f09fc0eefed27.scope … Killed process 1490413 (hermes) total-vm:5725872kB, anon-rss:4057072kB`. Una corrida muerta por OOM **no llega a escribir**: el vigía de informes no puede verla porque su señal es el informe ausente.
- **(2) Falso ok por cambio de formato.** El barrido que el vigía importa (`~/.hermes/skills/software-development/hermes-cron-jobs/scripts/barrido-informes-fallidos.py`) reconocía **dos** señales (`(FAILED)` en cabecera, `## Error` en cola) y el formato de fallo actual de Hermes es `**Status:** script failed`. Los dos informes fallidos del 15-10 (`cron/output/67d5fcc5b69e/2026-10-15_09-01-35.md`, 363 B, y `cron/output/210486645f20/2026-10-15_12-01-37.md`, 359 B) llevan esa cadena y **pasaron como ok** (el vigilante corrió a las 12:00:37 del 15-10, después del fallo de las 09:01, y no avisó). Arreglado el **16-10 07:48** (3ª señal + `CABECERA` de 200→600 B, con la medición de que el fallo no era el tamaño de la ventana sino la señal que no se miraba).
- **(3) El hueco está reconocido por el propio lab.** Registrado por el usuario en `pendientes.md` el **16-10 07:36:35** como «PUNTO CIEGO 3: la corrida que muere por OOM no deja informe, y el vigilante solo lee informes». Es la etiqueta «3» de una serie; en el fichero solo aparece esa entrada con esa etiqueta literal.
- **Contraste que acota el patrón (lo que SÍ existe aunque no haya informe):** la misma corrida del consolidador **sí** dejó rastro en dos fuentes que no dependen del artefacto — `executions` (fila `status: unknown`, 15-10 22:30:35 → 22:31:09) y `cron_incidents` (fila `9474f6_807bf8724760`, `detected`, abierta desde el 01-10). Es decir: **el hueco no es del sistema, es del vigía elegido**: hay señales disponibles, pero el vigía no las lee.

## 4. Mecanismo propuesto

El vigía se diseñó con la señal más cómoda (el informe ya escrito, con formato conocido) y esa señal es **correlativa, no exhaustiva**: existe solo si la corrida llegó al final. Los modos de fallo más graves (OOM, kill, corte) ocurren por definición antes de ese punto, así que **el vigía es ciego justo a los fallos más severos** — el sesgo es estructural, no un bug de implementación. El segundo modo (falso ok por formato) es el mismo sesgo por otra puerta: el vigía lee el artefacto correcto, pero su criterio de «fallo» está codificado contra una versión antigua del formato.

## 5. Condición de falsación

Sería **FALSO** si, sobre **N=10 corridas** del lab que terminan sin escribir su artefacto y durante **2 ciclos LPA consecutivos**, **8 o más** son detectadas igualmente por el vigía (o por el ciclo) **desde una segunda fuente independiente** antes de que un humano las note. También lo falsaría que la ausencia de artefacto no fuera señal de fallo sino de «job que no debía producir ese día» en ≥8 de los 10 casos (es decir: que «sin informe» casi siempre signifique «nada que informar»).

## 6. Antídoto propuesto (sin medir)

1. **Cruzar dos fuentes independientes del artefacto:** `failure_streak` / `last_run_at` de `~/.hermes/cron/jobs.json` y las filas no sanas de `executions` + `cron_incidents` (una corrida muerta deja fila aunque no deje informe).
2. **Contar corridas esperadas vs informes presentes** por carpeta de job, y alertar por diferencia (no solo por contenido de informe).
3. **Declarar el formato de fallo como contrato con fecha:** las señales del barrido se validan contra el formato de la versión de Hermes instalada; un cambio de formato invalida el vigía en silencio.
4. **Etiquetar el fallo por origen** cuando la única señal es la ausencia (`sin_artefacto`), en vez de dejarla indistinguible de «no había job».

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1 (falta: un segundo job silencioso y un segundo vigía independientes)
- [ ] Asciende a procedures/ como procedimiento LPA (el cruce de fuentes todavía no está instrumentado)
- [x] Sigue en incubación
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (**relación declarada, sin fusión:** **CP-012** — «el `unknown` se resuelve en el artefacto» — es la cara complementaria y **no queda falsado**: cuando el artefacto no existe, «efectos NO» sigue siendo el veredicto correcto sobre el EFECTO; CP-015 añade lo que ese veredicto no dice: **por qué** murió, y que el vigía que solo mira artefactos no lo verá. **CP-010** comparte «el medidor no mide lo que su etiqueta declara» (aquí: el vigía se llama «informes fallidos» y mide «informes presentes y reconocibles»)).

**Fecha de revisión:** 2026-10-23 (ciclo semanal siguiente) y 2026-11-02 (mensual).
**Justificación:** 3 ocurrencias (15 corridas sin informe con causa OOM verbatim; 2 falsos ok del mismo vigía; el punto ciego reconocido en el backlog el mismo día), en un instrumento de vigilancia del lab. El sesgo es estructural y explicable, lo que lo hace prometedor, pero la evidencia es de un solo job silencioso y un solo vigía → E0.
