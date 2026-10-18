---
type: knowledge
subtype: observation
status: active
tags: [hermes, curador, skills, escritura, proceso, rule-018]
created: 2026-09-30
---

# OBS-154: El curador inline de Hermes edita skills del lab sin OK (30-sep: 51 operaciones sobre 7 skills) y el estado esta en `paused: true`

==============================================================================

## Datos basicos

- **ID**: OBS-154
- **Fecha de la medicion**: 2026-09-30, ventana 07:28-16:24 CEST (05:28-14:24 UTC). Cierre: `date` -> 16:24:06 CEST.
- **Origen**: hallazgo al cerrar la tarea «Las 3». El agente iba a anotar una leccion en la skill `instagram-content-extraction` (perfil `default`) y, antes de escribir, re-midio el fichero: `SKILL.md` habia cambiado bajo sus pies. Escritor: el pase de curaduria que Hermes lanza al final de un turno del agente (`actor: curator`), en la MISMA sesion.
- **Metodo**: solo lectura (`md5sum`, `sha256sum`, `ls -la --time-style=full-iso`, `read_file`, `.curator_ledger.jsonl`, `hermes curator ledger`, `agent.log`). El agente NO escribio nada en ningun fichero de skill.

## Observacion

Caso del mismo tipo que RULE-018 formalizo el 20-sep-2026, con dos hechos nuevos medidos hoy:

1. **Escala**: 51 operaciones con `actor: curator` sobre 7 skills del lab en un dia (frente a 16 en 4 h sobre 4 skills el 20-sep).
2. **El cortafuegos que cita RULE-018 no aplica**: el estado del curador lleva `paused: true` desde el 23-sep y las escrituras con `actor: curator` continuan hoy, con la sesion del propio agente como `evidence.session_id`.

Cambio concreto: a las 16:15:01 `write_file` de `references/veredicto-y-cruce-con-el-lab.md` (3077 B) y a las 16:15:08 `patch` del puntero en la linea 101 de `SKILL.md`. La seccion que el agente iba a tocar (lineas 87-97) quedo intacta, y la leccion que iba a escribir ya estaba escrita por el curador ~40 s antes, con este literal: `Nº de láminas: solo si el bloque JSON del post cuadra con la fecha de ese post`. Por el procedimiento de RULE-018 no se duplico: se reporta como ya cubierta.

## Medicion literal

**1. Quien arranca el pase** (`~/.hermes/logs/agent.log`, linea 14410):

```
2026-09-30 16:13:15,841 INFO [20260930_161100_556214] agent.turn_context: conversation turn: session=20260930_161100_556214 model=deepseek-v4-flash provider=deepseek platform=telegram history=62 msg='Review the conversation above and update the skill library. Be ACTIVE — most ses...'
```

**2. Las mutaciones sobre la skill** (`~/.hermes/skills/.curator_ledger.jsonl`, filas `3ca9cc439b60` y `cf20efc7a56a`):

```
"id": "3ca9cc439b60", "ts": "2026-09-30T14:15:01.385965+00:00", "actor": "curator", "action": "write_file", "skill": "instagram-content-extraction"
"id": "cf20efc7a56a", "ts": "2026-09-30T14:15:08.079389+00:00", "actor": "curator", "action": "patch", "skill": "instagram-content-extraction"
```

Segundo instrumento: `hermes curator ledger --skill instagram-content-extraction` lista esas mismas dos filas como las mas recientes (`cf20efc7a56a 8m ago curator patch`, `3ca9cc439b60 9m ago curator write_file`). Coinciden.

**3. Conteo del dia** (ledger completo: 1750 filas desde el 01-sep) — **51 operaciones, 7 skills**:

- `hermes-cron-jobs`: 23 patch + 3 write_file + 1 remove_file = 27
- `render-html-a-imagen`: 8 patch + 2 write_file = 10
- `edicion-aditiva-registros`: 7 patch
- `instagram-content-extraction`: 3 patch + 1 write_file = 4
- `watchdog-salud-sistema`: 1 patch
- `delegacion-subagentes`: 1 patch
- `vigilancia-canales-youtube`: 1 patch

**4. Hashes: dos instrumentos coinciden**. `sha256sum SKILL.md` = `528db3e514dd831537b909e40b402b2f75aa28fe401be7536f3d774d7cd7ab80`, igual al `after` que el propio ledger registra para la fila `cf20efc7a56a`; el `before` del ledger es `a46ea2e62ab74404013da70da66fde6ef7cf714d373a91022300726b964d72e6`. El `write_file` de la referencia: `after` = `bdec930ba7a9a8be51f5419fa1a7ae63ff83cb27f9ccae9a6b7eaa01262cd34c`, igual al sha256 medido del fichero.

**5. Estado del curador** (`~/.hermes/skills/.curator_state`):

```
"last_run_at": "2026-09-23T17:08:43.212125+00:00", "last_run_summary": "auto: 16 marked stale, 6 archived, 6 reactivated; llm: skipped (consolidation off)", "paused": true, "run_count": 13
```

**6. El criterio real es la propiedad de la skill, no `pause`**. En las user-owned se NIEGA (`agent.log`, 2026-09-30 08:32:36):

```
"Refusing background curator patch for skill 'perfume-del-dia': the skill is not curator-managed (created_by=None). User-owned skills are off-limits to autonomous curation.
```

Intentos rechazados hoy: `diagnostico-stack-local` (07:59, 08:16), `perfume-del-dia` (08:32, 09:05), `perfume-ia` (08:33). En las curator-managed (entre ellas `instagram-content-extraction`) escribe sin OK.

**7. Reversibilidad verificada** (RULE-018 la citaba sin comprobar): `~/.hermes/.curator_backups/blobs/` existe con 2709 ficheros y CONTIENE el previo exacto de `SKILL.md`, `a46ea2e62ab74404013da70da66fde6ef7cf714d373a91022300726b964d72e6`. Rollback por mutacion: `hermes curator rollback cf20efc7a56a`.

## Que confirma de RULE-018

- Un proceso de fondo (el curador de Hermes) escribe CONTENIDO de skills del lab sin OK explicito: segunda medicion independiente (20-sep y 30-sep).
- El procedimiento de la RULE se aplico tal cual: medir antes de escribir -> detectar el cambio bajo los pies -> PARAR -> leer el fichero entero -> no duplicar. Literal de la RULE: `Si el diff es consolidacion en sitio y la leccion ya esta escrita, NO se escribe nada: se reporta.`
- La atribucion por actor se sostiene: lo escrito por el curador no se atribuye al agente.
- La skill `edicion-aditiva-registros` ya recoge ese paso (releer justo antes de aplicar; el curador puede haber escrito ya la misma leccion).

## Limites / lo que NO dice

- NO se ha medido si el curador PRESERVA lo escrito a mano por el agente en una skill curator-managed (solo que escribe y que hoy reescribio una seccion).
- NO se ha probado si `hermes curator pause` detendria el pase por turno: con `paused: true` sigue escribiendo, pero el experimento (pausar y observar) no se ha hecho.
- El ledger guarda hashes antes/despues, NO el diff; el diff de hoy (una linea) se obtuvo leyendo el fichero.
- NO se ha revisado el contenido de las otras skills tocadas hoy para ver si alguna queda peor.
- El conteo es del ledger local de HOY; no se ha cruzado con `hermes curator ledger` skill por skill.

## Acciones derivadas (propuestas, ninguna ejecutada)

1. Decidir si se protegen skills concretas con `hermes curator pin <skill>` (RULE-018 dice que deja el curador vivo para el resto; ojo: pinear `instagram-content-extraction` detendria tambien lo que hoy ha sido util).
2. Corregir RULE-018 con lo medido: `pause` no cubre el pase por turno; el criterio efectivo es `created_by`.
3. Actualizar `last_validated` de RULE-018 (sigue en 2026-09-20) si se acepta esta revalidacion.

==============================================================================

## Addendum 2026-09-30 - el conteo subio DESPUES de cerrar este OBS (51 -> 55) y el pase corre POR TURNO

MARCA: obs154-addendum-drift-20260930

- **El conteo de este OBS es una FOTO de las 16:24 CEST**: re-medido a las 16:41 CEST el mismo ledger da **55 operaciones** (no 51) y sigue por encima de lo que recoge el OBS: a las 17:04 CEST son **55** operaciones de hoy repartidas en 8 nombres de skill (7 en la ventana de las 16:41) y 1757 filas en el ledger. Este OBS no se reescribe: se anade este addendum y las 95 lineas previas quedan intactas.
- **Las 4 operaciones nuevas**: 3 `patch` + 1 `write_file` del curador sobre `edicion-aditiva-registros` a las 16:27:25-29 CEST, con `evidence.session_id` = `20260930_162343_c83c97`, la sesion del turno del agente que estaba redactando y reportando ESTE hallazgo. Confirma el mecanismo ya medido: no hay un tercero escribiendo; el pase se dispara POR TURNO, al cerrar el turno del agente, dentro de su propia sesion.
- **Segundo instrumento** (recuento directo de `.curator_ledger.jsonl`, solo lectura): 1757 filas desde el 01-sep, actores `curator` 1341 / `agent` 416 -> el ledger SI distingue autor, que es lo que RULE-018 citaba.
- **`hermes curator status` (30-sep)**: `curator: PAUSED`, runs=13, last run hace 6d, interval 7d, stale 14d, archive 30d, consolidate off; curator-managed=96 (agent-created=71, bundled=25; 67 active / 29 stale), unmanaged=68 (68 foreground-created). Corrobora que el corte efectivo es la PROPIEDAD (`created_by`) y no `pause`.
- **`.curator_suppressed`** (337 B, 23-sep): 30 nombres del catalogo bundled ([airtable..xurl]), sin solape con las 8 skills del lab editadas hoy -> no es el mecanismo que protege las skills del lab.
- **`~/.hermes/.curator_backups/blobs/`**: 2716 blobs y creciendo con cada mutacion -> el rollback por mutacion (`hermes curator rollback <id>`) sigue viable.
- **RULE-018 corregida en esta misma sesion** (accion derivada 2, tras OK del usuario): `last_validated` 2026-09-20 -> 2026-09-30; el `desc` deja de dar `pause` como cortafuegos y pasa al criterio `created_by`; `evidence` 3 -> 6 asientos; `verified` gana `machine:hermes` 30-sep (la entrada `human:jokoalmi` del 20-sep NO se toca). Fichero 3184 -> 7942 B (sha256 `a4d58e105be76640c13e6152bbb6a3053de102f70b5d0f22fc244fcc834a9790`), con la cadena de backups `RULE-018.yaml.bak-20260930-cortafuegos` (3184 B) y `RULE-018.yaml.bak-20260930-figs` (6578 B) para revertir paso a paso. Dos cifras de la primera pasada salieron mal medidas (32 skills suprimidos y 2713 blobs): se rectificaron en una segunda pasada con instrumento y este OBS no las hereda.
- **La leccion ya estaba escrita por el curador** en `edicion-aditiva-registros` (11 ops hoy, 4 de ellas en este mismo turno): el criterio `created_by` con el rechazo, la advertencia de que `pause` no cubre el pase por turno y la referencia `references/auditar-y-revertir-al-curador.md`. Por RULE-018 NO se duplica.
- **Lo que NO cambia**: las cifras de la medicion original de este OBS (51 ops / 7 skills / 1750 filas / ventana 07:28-16:24 CEST) siguen siendo correctas para ESA ventana; este addendum no las sustituye.

==============================================================================

## Addendum 2 - 2026-09-30 noche: el pase sigue corriendo por turno (22:00-23:04 CEST: 28 operaciones sobre 7 skills; el dia cierra en 107 operaciones / 16 skills)

MARCA: obs154-addendum-drift-23h-20260930

- **Medido a las 23:16 CEST** (`date` -> 2026-09-30 23:16:29 CEST) sobre `~/.hermes/skills/.curator_ledger.jsonl` (1806 filas, el 100% JSON valido). El `ts` del ledger va en **UTC**: la ventana local 22:00-24:00 CEST es `2026-09-30T20:00` -> `2026-09-30T22:00` UTC.
- **Ventana 22:00-23:04 CEST: 28 operaciones, las 28 con `actor: curator`** (27 `patch` + 1 `write_file`), repartidas en **7 skills**: `serie-editorial-linkedin` 19 (13 de ellas en `references/produccion-pieza-serie.md`), `edicion-aditiva-registros` 3, `joko-git-recibos` 2, y 1 en `evaluar-alucinaciones`, `preservacion-material-sesion`, `autorizacion-escritura-lab` y `validacion-instrumentos-medicion`.
- **El bloque de las 23:03:28 CEST**: 8 `patch` sobre `references/produccion-pieza-serie.md` (ids `76d7e77f5b18`, `a1ce99f8eb33`, `a310effd5f9b`, `7f0227134fc4`, `cb3427932cb6`, `87d1b8e9fd13`, `681c158a28b4` y, a las 23:03:35, `c42a2bf087d8`). El fichero pasa de **28.911 B a 31.456 B** (mtime 23:03; sha256 en disco `aced79e7a328202e7fb2ae17d07cc1a278915723ebc96c7fc998c7cf2b35137e`). `evidence.session_id` = `20260930_224315_0ba36a`.
- **Como se detecto**: el agente iba a anotar en esa receta las dos lecciones que el usuario acababa de aprobar (revisor con huella md5 por slide y desvio de los pies 7 -> 1) y, al re-medir antes de escribir, encontro el cambio bajo sus pies (mtime 23:03, +2545 B). Por el procedimiento de RULE-018 **no se duplico**: se paro y se reporto al usuario, que decidio registrar el incidente aqui y en el backlog.
- **23:04:31 CEST**: `write_file` de `validacion-instrumentos-medicion/references/mediciones-reanudables-y-cache.md` (1718 B, fichero NUEVO).
- **El pase se dispara por turno, no por reloj**: las 28 operaciones se agrupan en 10 instantes (22:08:46, 22:19:39-40, 22:27:26, 22:27:34, 22:30:47, 22:31:59, 22:32:07, 23:03:28, 23:03:35, 23:04:31), todas con el `evidence.session_id` de una sesion del agente.
- **El dia sube a 107 operaciones / 16 skills** (UTC 2026-09-30), frente a las **51 / 7** de la foto de las 16:24 y las **55 / 8** del addendum 1 (16:41-17:04). El corte no envejece: la serie crece tras cada turno.
- **Segundo instrumento**: la ultima fila del ledger (`ea667750b3e6`, `after.sha256` de `validacion-instrumentos-medicion/SKILL.md` = `11110a81b5db4f4a4462b4a398e9f214cec4039e80c641386533cab8a61534db`) coincide con el sha256 del fichero en disco -> el ledger dice la verdad sobre el arbol. La receta se midio dos veces de forma independiente: 31.456 B / sha256 `aced79e7...`.
- **Error de instrumento corregido en esta medicion**: la primera pasada conto la ventana con el `ts` en hora local y dio 0 operaciones; el ledger sella en UTC. Corregido antes de escribir nada.
- **Limite**: no se ha medido quien crea las copias `.bak-20260930` que hay en la carpeta de la skill (`SKILL.md.bak-20260930`, 27140 B, y `references/produccion-pieza-serie.md.bak-20260930`, 27324 B, ambas mtime 22:19); se deja constancia, sin atribuirlas.
- **No cambia nada de lo anterior**: las cifras de la medicion original (51 / 7, ventana 07:28-16:24) y del addendum 1 (55 / 8) siguen siendo correctas para SUS ventanas; este addendum anade la ventana de la noche.
- **Sin OK todavia**: `hermes curator pin <skill>` / `hermes curator pause` como cortafuegos; el commit de este OBS y del bloque de backlog.

==============================================================================

## Addendum 3 - 2026-10-07: el escritor NO es el pase semanal, es la REVISION AUTOMATICA POST-TURNO (mecanismo localizado en el codigo)

MARCA: obs154-addendum-post-turno-20261007

- **Foto a las 2026-10-07 14:53:06 CEST** (`date` medido) sobre `~/.hermes/skills/.curator_ledger.jsonl` (**2116 filas, 0 invalidas**, JSON valido al 100%): **34 operaciones del actor `curator` el 07-oct sobre 11 skills** (30 `patch` + 4 `write_file`), ventana **07:28:48 -> 14:19:32 CEST**, repartidas en 8 sesiones de evidencia distintas. Un pase previo del mismo dia medido a las 14:16 daba **32 / 10**: es una foto, la serie crece tras cada turno.
- **Reparto por skill**: `lm-studio` 9, `validacion-instrumentos-medicion` 6, `recorte-figuras-producto` 4, `infografia-html` 3, `edicion-aditiva-registros` 3, `render-html-a-imagen` 2, `recuperar-mensajes-hermes` 2, `autorizacion-escritura-lab` 2, `state-verification-pattern` 1, `hermes-cron-jobs` 1, `refactor-seguro` 1.
- **Ventanas parciales de contraste**: 00:00-08:00 = 6 ops / 3 skills; 08:00-12:00 = 22 ops / 7 skills; 12:00-24:00 = 6 ops / 4 skills. El trabajo del pase se concentra en la manana.
- **Mecanismo (leido en la fuente, no inferido)**: `agent/turn_finalizer.py` (~l.763) llama a `agent._spawn_background_review(...)` **al cerrar el turno**, condicionado a que el turno tenga respuesta final, no este interrumpido y no lleve el flag `skip_background_review`, y a que toque revisar memoria **o** skills. El criterio de skills es `_should_review_skills = agent._skill_nudge_interval > 0 and agent._iters_since_skill >= agent._skill_nudge_interval and "skill_manage" in agent.valid_tool_names`: es decir, **un turno que consumio iteraciones de herramientas sin tocar skills**. Se dispara por turno, NO por reloj.
- **Por que consta como `curator`**: `tools/skill_ledger.py` (`derive_actor`) devuelve "curator" cuando esta puesto el flag de `tools/skill_provenance.py` (`is_background_review()`), y "agent" en el resto de casos; tambien hay override explicito por `set_ledger_actor`. **El nombre de actor no distingue "pase semanal" de "fork de revision de fondo".**
- **El pase semanal SI esta parado**: `~/.hermes/skills/.curator_state` = `paused: true`, `run_count 13`, `last_run_at 2026-09-23T17:08:43Z`, resumen `auto: 16 marked stale, 6 archived, 6 reactivated; llm: skipped`. Ese pase (transiciones de estado/archivado) es **el otro camino** que marca `curator` a mano: `agent/curator.py`, `_archive_as_curator` -> `set_ledger_actor("curator")` (la marca de la ~l.198).
- **Otros disparadores del mismo fork**: `/goals` (`gateway/slash_commands_goals.py`:171), `/refine` (`hermes_cli/cli_commands_mixin.py`:2245) y `agent/codex_runtime.py`:654. **Los cron NO lo disparan** (llevan `skip_background_review`).
- **Modelo del fork**: por defecto reusa el del padre (`auxiliary.background_review` = provider `auto`, `model` vacio), de ahi que las escrituras del 07-oct salgan con `deepseek-v4-flash`.
- **Interruptores, medidos pero NO aplicados (ninguno)**: (1) `auxiliary.background_review.enabled` NO esta en `config.yaml` y el cargador es **FAIL-OPEN** (`enabled=True` por defecto): para apagar el fork hay que escribir la clave explicitamente con `false`; (2) `skills.write_approval: false` y `skills.guard_agent_created: false` en la config de hoy — **semantica no verificada para este camino**, no se promete que corten el fork; (3) por skill: `hermes curator pin <skill>`.
- **Traza del 07-oct (decision de este dia)**: la nota de origen esta escrita **dentro** de `infografia-html` (bloque "Trazabilidad: parche del 07-oct-2026", con los 2 parches 08:01:03 / 08:01:10 y el sha256 del reference). Para las otras 10 skills no se toca cada fichero: la traza queda **centralizada** en este addendum y en el asiento de `04-operations/backlogs/pendientes.md` (MARCA `curador-post-turno-20261007`), que ademas evita el riesgo de que el propio fork parchee los 11 ficheros mientras se anotan.
- **Limite**: sigue sin medirse si `pause` o `enabled: false` detendrian el fork por turno (experimento pendiente desde el 30-sep, requiere OK).
- **Sin OK todavia**: los 3 interruptores y el commit de este addendum + asiento.
- **No cambia nada de lo anterior**: las cifras de la medicion original (51 / 7) y de los addenda 1 (55 / 8) y 2 (107 / 16) siguen siendo correctas para SUS ventanas; este addendum solo anade la del 07-oct.
- **Escrito por**: agente (Hermes) a peticion del usuario. Nada de este bloque es obra del fork.

==============================================================================

## Addendum 4 - 2026-10-07 noche: INTERRUPTOR 1 APLICADO en disco (background_review.enabled: false) y COMMIT del addendum 3 + asiento; el fork NO se ha probado apagado

MARCA: obs154-addendum4-fork-off-20261007

- **Orden del usuario, en serie**: «haz los 4 secuencialmente» (2026-10-07, sesion desktop). El PASO 1 de los 3 interruptores (apagar el fork) es el de este addendum; los otros 2 siguen SIN OK.
- **APLICADO en disco, con medicion doble** (2026-10-07 23:37:32 CEST): `~/.hermes/config.yaml` **618 -> 621 lineas** (+3), md5 PRE `2e08750f2528322bd44522ce14c1659d` -> POST `6388260059a914db3167714abbaca424`; `diff -u` contra el backup = **3 lineas (+) / 0 (-)**, hunk `@@ -208,6 +208,9 @@`: 2 comentarios + `enabled: false` dentro del bloque `background_review` (lineas 205..210; el bloque cierra en la 211 con `  web_extract:`) y antes de `timeout: 120`. Las 14 claves `auxiliary.*` quedan intactas (re-parseo con `yaml.safe_load`: `enabled = False`; deep-equal contra «PRE + 1 clave» = True). Backup PRE etiquetado: `config.yaml.bak-20261007-background-review-off` (14641 B en disco, mtime 2026-10-04 08:51:11).
  - Nota de numeracion (07-oct, tras el commit `e410ede`): el bloque `background_review` es AHORA 205..213 y `  web_extract:` esta en la **214**; los «205..210 / 211» citados arriba son la numeracion PRE al insert de las +3 lineas.
- **AVISO DE INSTRUMENTO (unidad mal etiquetada por el script)**: el lanzador imprimia «14509 B -> 14834 B» contando **CARACTERES**; en disco el fichero pasa de **14641 B a 14834 B**. La unidad de toda cifra publicada se RE-MIDE en disco (`stat -c %s`), no se copia del mensaje del script.
- **El cambio esta EN DISCO pero NO ACTIVO**: el proceso Hermes leyo `config.yaml` al arrancar. Hasta recargar o reiniciar Hermes, el fork puede seguir disparandose al cerrar turno.
- **EVIDENCIA medida (a favor, NO prueba)**: la ultima escritura del fork sobre `autorizacion-escritura-lab` es de las **23:28:50 CEST** (ts del ledger `2026-10-07T21:28:50Z`, sesion `20261007_232805_c527cd`) — 2 min DESPUES del commit 147d308 y 48 s ANTES del cambio —, y no hay ninguna op del actor `curator` con ts posterior al cambio. Limite: la ventana medida son minutos y el fork solo corre al cerrar turno; **no prueba** que `enabled: false` lo corte (eso exige reiniciar Hermes + una ventana larga con turnos).
- **COMMIT del addendum 3 + asiento: HECHO** el 2026-10-07 23:26:37 CEST -> `147d3081fad5c677d5988ee5e0f8bff73f31b65f`, arbol `7d681552b7afd62fe39318628cb78401cb62b69d` = `tree_sha` del recibo `.git/joko-recibo.json` (`aprobado_por: joseba`), **2 ficheros** (+35/-0). **SIN push**: `origin/master` sigue en `a3fdab59ad23ba0f2e0d87fc946b1750e63a0d33` (`rev-list --left-right --count` = `0 1`).
- **Sigue SIN OK**: (2) `skills.write_approval` y (3) `hermes curator pin <skill>`; y el commit de ESTE addendum 4 + su asiento (estado: aplicado-sin-firmar).
  - Cerrado el 07-oct 23:40:01 CEST: el commit de ESTE addendum 4 + su asiento es `e410ede6f3fad6469733202a975bf4e08662f3ee` (mismo `tree_sha` `0682d6eb36ddd505fee28f1190462e3a4d940cd9`, gate RDD OK); 2 ficheros, +28/-0; SIN push (`0 2`). Los interruptores 2 y 3 siguen SIN OK.
- **No cambia nada de lo anterior**: las cifras de la medicion original (51 / 7) y de los addenda 1 (55 / 8), 2 (107 / 16) y 3 (34 / 11 en su ventana) siguen siendo correctas para SUS ventanas; este addendum solo anade el cambio aplicado y el commit.
- **Escrito por**: agente (Hermes) a peticion del usuario («haz los 4 secuencialmente», 2026-10-07).
  - Registro: OBS-154 18289 B / 149 lineas / md5 `822dec4d45d7d6a97e367645e2785ff8` antes -> 21402 B / 165 lineas / md5 `586717a9b28ab7e092bdf285720010bb` tras el addendum (delta +3113 B, +16 lineas) | backup PRE: `OBS-154-curador-edita-skills-sin-ok-2026-09-30.md.bak-20261007-addendum4` | escrito por agente (Hermes) a peticion del usuario.

==============================================================================

## Addendum 5 - 2026-10-08: INTERRUPTORES 2 y 3 APLICADOS y VERIFICADOS EN CALIENTE (sin reiniciar); el 1 sigue pendiente de reinicio. HALLAZGO: 8 escrituras de MEMORIA del fork encoladas sin aprobar

MARCA: obs154-addendum5-interruptores-2-3-20261008

- **Orden del usuario**: «haz todos» (07-08-oct, sesion desktop) = push + interruptores 2 y 3 + reinicio + la leccion; despues «inspecciona y si» (08-oct) = volcar la cola de memoria y escribir esta traza + commit + push.
- **PUSH HECHO Y VERIFICADO (08-oct)**: `git push origin master` exit 0; `git ls-remote origin master` == HEAD local == `57c153bf82845c5a54b472e2f52519fc7df59120`; `rev-list --left-right --count origin/master...master` = `0 0`; en el bare `/mnt/ssd_ia_datos/joko-lab.git` (`findmnt -T /mnt/ssd_ia_datos` = `/dev/sda1 ext4`) `git log -1` y `ls-tree -r` listan los 2 ficheros. Subio la historia de los 3 commits que estaban SIN push (`147d308`, `e410ede`, `57c153b`).
- **INTERRUPTOR 2 APLICADO**: `hermes config set skills.write_approval true` -> `Set skills.write_approval = True`. Medido en disco: 621 lineas, `diff -u` contra el backup = **1 sola linea** (`write_approval: false` -> `true`), comentarios `#` **23 -> 23** (el escritor del CLI conserva comentarios: round-trip de ruamel, `hermes_cli/config.py`), md5 PRE `6388260059a914db3167714abbaca424` -> POST `47c1622cca9c1071661a7f4e034eea05`. Backup PRE: `config.yaml.bak-20261008-writegate`.
- **...Y ACTIVO SIN REINICIAR** (el cargador se invalida por `mtime`; `load_config` en `hermes_cli/config.py`), probado de TRES formas: (a) `hermes config get skills.write_approval` -> `true`; (b) la propia funcion del gate `tools.write_approval.write_approval_enabled('skills')` -> **True** (ejecutada con el interprete del bundle `~/.hermes/tools/python-3.14*/bin/python3` + `hermes_bootstrap`, que es quien inyecta las dependencias: el python del bundle a secas NO trae ruamel); (c) **prueba end-to-end**: un `skill_manage` real del agente devolvio `staged: true`, `pending_id 932e8db8`, «Staged for approval (skills.write_approval is on). Not yet saved»; la skill de prueba NO aparecio en disco y se limpio con `discard_pending('skills','932e8db8')` (cola de skills = 0). El gate cubre foreground Y revision de fondo (`hermes_cli/config_defaults.py:1455`).
- **Cola de pendientes (mecanica verificada en fuente)**: `~/.hermes/pending/<subsystem>/<id>.json`; se descarta con `discard_pending(subsystem, id)`; la de skills se revisa con `/skills pending`. **El nombre del comando equivalente para memoria NO esta verificado** (no se cita).
- **EFECTO COLATERAL DECLARADO**: desde ahora las escrituras de skills del AGENTE en sesion tambien quedan pendientes de aprobacion (`/skills pending` -> approve/reject). Por eso la leccion de este dia se escribio ANTES de encender el interruptor 2.
- **INTERRUPTOR 3 APLICADO**: `hermes curator pin` sobre las 11 skills de la lista del addendum 3 -> `hermes curator status` muestra `pinned (11)` y persiste en `~/.hermes/skills/.usage.json`. **PRECISION que corrige la expectativa**: `pin` = «pinned skills bypass all auto-transitions» -> protege de *stale/archivado*, **NO corta el fork de revision de fondo** (ese escribe via `skill_manage`). Lo cortan los interruptores 1 y 2. El pase semanal ya estaba `paused: true` (`~/.hermes/skills/.curator_state`).
- **INTERRUPTOR 1**: sigue **en disco `false` y NO efectivo** (addendum 4). El valor se lee en caliente por `mtime`, pero el punto de lectura del fork no se ha medido: **reiniciar Hermes queda PENDIENTE y lo hace el usuario** (el agente no se reinicia: mataria su propia sesion).
- **HALLAZGO NUEVO (medido hoy, SOLO LECTURA)**: `~/.hermes/pending/memory/` contiene **8 entradas del actor `background_review`**, de **2026-09-19 12:15 a 2026-10-06 07:48**, con **26 operaciones** (7 con `target: memory` + 1 con `target: user`), **ninguna aprobada**; hoy `write_approval_enabled('memory')` = **False**. El fork intento consolidar la memoria durante 3 semanas y **todo quedo en cola**: proponia borrar `09-09: retomar grill-idea` (3 entradas) y `Padre: cumple 24-ago`, anadir el parrafo `TG: envios sueltos ... NO llegan al DM`, la nota de `python3` del lab, una entrada nueva de perfume/piel, y varias condensaciones (Backups, Obsidian, LOCAL/qwen, RULE-016). **Causa NO verificada** (por que el gate de memoria estaba activo en esas fechas) y **cola NO tocada**: sigue intacta a la espera de decision del usuario.
- **LECCION escrita hoy** en `autorizacion-escritura-lab/SKILL.md` (lineas 125/129/130): «Cuatro defectos que han costado un run entero...»; (d) **un backup PRE por FICHERO, no por ancla** (dos anclas del mismo fichero compartian nombre de backup: asertos de unicidad de TODAS las anclas antes de escribir la primera, e inserciones de abajo arriba); y **el que escribe no se verifica a si mismo: la comprobacion posterior la hace un SEGUNDO programa de solo lectura**.
- **Estado de firma al escribir este bloque**: aplicado-sin-firmar. El commit de este asiento y del addendum 5 se hace en el mismo turno del 08-oct; el hash vive en el log del repo y NO se anticipa aqui.
- **Sigue SIN OK / pendiente**: (a) el REINICIO de Hermes (para que el interruptor 1 sea efectivo); (b) la cola de memoria (8 entradas): aprobar, descartar o dejar; (c) `skills.guard_agent_created` y `memory.write_approval` (ambos medidos `false` hoy; semantica para este camino no verificada).
- **Escrito por**: agente (Hermes) a peticion del usuario («haz todos» + «inspecciona y si», 08-oct-2026).
  - Registro: OBS-154 22257 B / 168 lineas / md5 `eae42326f2225d107461bb61ad2f1356` antes -> 28311 B / 189 lineas tras el addendum | **md5 POST: NO se publica dentro del fichero** (autorreferencia: el md5 de un fichero no puede ir en su propio contenido; se mide fuera, en el commit del 08-oct) | backup PRE: `OBS-154-curador-edita-skills-sin-ok-2026-09-30.md.bak-20261008-interruptores23` | escrito por agente (Hermes) a peticion del usuario.
