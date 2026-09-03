# DEC-2026-09-03 — Corrupción state.db en v0.21.0: causa raíz upstream + mitigación + norma de espera

**Fecha:** 2026-09-03
**Estado:** activa
**Ámbito:** Hermes Agent (state.db) + proceso de actualización del lab
**Tipo:** incidente → decisión + norma (RULE-016)

## Contexto (incidente 02-03 sep 2026)

state.db (SQLite + FTS5, ~1.3 GB, 124k mensajes) se corrompió el 02-sep 22:31
(cron Bolsa: `database disk image is malformed`) y empeoró a `file is not a
database` el 02-sep 22:57 (gateway Telegram). Reparación completa verificada
03-sep 10:16: foreign_key_check vacío, quick_check ok, 7 sesiones huérfanas
reinsertadas desde JSONL, 551 sesiones. Verificación end-to-end OK a las
10:27 (session_search resuelve, gateway activo, 0 patrones post-10:16).

## Causa raíz (investigación upstream 03-sep, fuentes oficiales GitHub)

El fallo NO es de configuración local: es una clase de corrupción conocida y
ABIERTA en NousResearch/hermes-agent, agravada en v0.21.0:

- **Issue #100313** (P1, open): corrupción de state.db en el instante en que un
  cron (cronjob action=run) se lanza desde una sesión CLI activa con escrituras.
  Entorno casi idéntico al nuestro: v0.21.0, kernel 7.0.0-30-generic, WAL,
  gateway systemd + CLI + cron en la misma BD. Síntomas idénticos: NOTADB en la
  conexión ya abierta + CORRUPT en la conexión nueva, mismo instante.
- **Causa raíz confirmada por mantenedores** (triage round-2 de #100313): el
  commit 71256df (2026-08-18, dentro de la ventana 0.21) introdujo
  `_read_sqlite_application_id`, un probe raw `open/read/close` de la state.db
  VIVA al inicio de cada escritura. En POSIX, `close()` cancela TODOS los
  advisory locks del proceso → el writer pierde su DMS lock del WAL → un opener
  nuevo puede lanzar WAL recovery/checkpoint bajo un writer a mitad de commit.
- **Fix**: PR #100519 (`_pread_db_header` + os.pread; lock-safe), mergeado
  2026-09-01 17:51 UTC. Nuestro HEAD local 5a8e8a6b (01-sep 09:32 UTC) es
  ANTERIOR al fix por 8h19m → **v0.21.0 publicada (31-ago) NO incluye el fix**.
  Confirmado: nuestro código tiene `_read_sqlite_application_id` (L4227) y NO
  tiene `os.pread`. 0.21.1 NO existe todavía (última release v2026.8.31).
- Cluster relacionado: #90837 (umbrella forensics, 11 incidentes), #85004
  (background_review fork), #100896 (precursor "5 live SessionDB handles"),
  #101064 (WAL unlink race). Fixes adicionales de la clase ya en main:
  #100958, #101000, #101081, #101085, #101092.

## Decisiones

### D1 — Esperar a v0.21.1 para actualizar (NO saltar a main)

- Criterio de salida: publicación de v0.21.1 (o parche superior) que incluya
  el fix #100519 + fixes del cluster (#100958, #101000, #101081/#101085).
- Al salir, ejecutar el análisis completo con la skill hermes-upgrade-analysis
  ANTES de actualizar (ver D3 / RULE-016).

### D2 — Mitigación puente YA aplicada: journal_mode: delete

- `database.journal_mode: delete` en ~/.hermes/config.yaml (vía `hermes config
  set`, backup previo config.yaml.bak-20260903-journaldelete).
- Efecto: elimina la superficie WAL multi-proceso (la clase de fallo de la
  corrupción). Coste: menor concurrencia de escritura (aceptable: 1 gateway +
  CLI + crons, volumen moderado). Reversible con `hermes config set
  database.journal_mode wal` + reinicio.
- OJO: el journal_mode REAL de state.db sigue `wal` hasta el próximo reinicio
  del gateway (Hermes aplica resolve_journal_mode al abrir la BD). El cambio
  efectivo requiere reiniciar el gateway en una ventana controlada (ver plan).

### D3 — NORMA (RULE-016): espera de 5 días tras publicación de nueva versión

Cuando el watchdog detecte una NUEVA versión de Hermes Agent, el lab NO
actualiza de inmediato: durante los 5 días posteriores a la publicación se
investigan incidencias derivadas de esa versión (issues/PRs del repo oficial,
foros expertos) ANTES de decidir actualizar. Ver RULE-016.yaml.

## Plan de ejecución

1. [HECHO] Investigación upstream con fuentes oficiales (issues #100313,
   #90837, #94736, #85004, #100896, #101064; PR #100519; código local).
2. [HECHO] `hermes config set database.journal_mode delete` + backup config.
3. [PENDIENTE] Reinicio del gateway en ventana controlada para que state.db
   pase realmente a journal_mode=delete. Hacerlo cuando no haya sesiones
   críticas en vuelo (preferible: mismo procedimiento que la reparación:
   verificar con ps/lsof que no hay writers antes). NO reiniciar el gateway
   desde una tool call del agente (bloqueado); vía shell externo del usuario o
   cron one-shot.
4. [HECHO] RULE-016 creada (objeto YAML) + esta decisión documentada.
5. [PENDIENTE] Actualizar GUIA-JOKO-LAB (v1.6.5) y skill hermes-upgrade-analysis
   con la norma de 5 días.
6. [VIGILANCIA] Watchdog de versiones (517fdc280d6f) sigue activo: cuando
   notifique 0.21.1, ejecutar análisis hermes-upgrade-analysis completo (con
   especial atención al fix #100519) antes de actualizar.

## Reversión de D2

```bash
hermes config set database.journal_mode wal
# + reinicio del gateway en ventana controlada
```

## Referencias

- Issue #100313: https://github.com/NousResearch/hermes-agent/issues/100313
- Issue #94736: https://github.com/NousResearch/hermes-agent/issues/94736
- PR #100519: https://github.com/NousResearch/hermes-agent/pull/100519
- Issue #90837: https://github.com/NousResearch/hermes-agent/issues/90837
- Issue #101064: https://github.com/NousResearch/hermes-agent/issues/101064
- Skill recuperacion-state-db (procedimiento + incidente completo)

---

## Addendum 03-sep-2026 (tarde) — resolución real tras la actualización

Estado a 03-sep 13:20, verificado con salida real (auditoría post-incidente):

1. **Actualización EJECUTADA (12:07-12:19) a upstream 561b053f (main), 790 commits.**
   Incumple la letra de D1 (esperar v0.21.1) pero cumple su espíritu: el commit
   INCLUYE el fix #100519. Verificado por grep en hermes_state.py (mtime 12:19):
   `_pread_db_header` (L4485) + `os.pread` (L4523); `_read_sqlite_application_id`
   ahora enrutado por `_pread_db_header` (L4531, "Safe against live databases").
   Decisión real del usuario: saltar a main para obtener el fix en lugar de
   esperar la release. RULE-016 sigue vigente para futuras versiones.

2. **D2 RESUELTA — journal_mode revertido a `wal` (03-sep 13:16, OK usuario).**
   Con el fix instalado, WAL vuelve a ser seguro (el bug del probe que cancelaba
   locks POSIX está corregido). La config pedía `delete` pero state.db y
   cron/executions.db seguían en WAL en disco (downgrade en vivo bloqueado por
   Hermes) → spam de ERROR cada ~2 min en errors.log: "database.journal_mode=delete
   is configured but the on-disk database is already WAL". Fix aplicado:
   `hermes config set database.journal_mode wal` (backup
   config.yaml.bak-20260903-journalwal). Config y disco ahora coinciden.

3. **sessions.auto_prune: true activado (03-sep 13:16, OK usuario).** El informe
   de recuperación lo daba por hecho, pero la config real estaba en false; el
   `true` visto pertenecía a la sección snapshots. Corregido y verificado.

4. **Higiene post-reparación (03-sep 13:17, OK usuario):** borrados ~17 GB de
   residuos state.db.* (14 copias de ~1.3 GB: malformed-backup-*, forensic-*,
   recover-attempt, pre-fk-repair, pre-journal, recuperada, bak4, before-restore)
   + tmpgmetwcl6.db (482 MB, residuo de update del 01-sep). Conservados: state.db
   (buena, 718 MB, quick_check ok, FK vacío, 555 ses / 124.162 msg),
   state.db.malformed-backup-20260903_115200 (evidencia) y
   state.db.repair-attempts.json (registro forense). Regla de la skill: BD buena
   + 1 backup malformado como evidencia.

5. **Crons con error tras el incidente — ninguno activo (auditoría 13:10):**
   los 7 errores de jobs.json están fechados en ventanas de corrupción
   (Bolsa EXP-002 02-sep 22:31 = detonante; vigilar-ig 03-sep 09:01) o antes
   (3 semanales del 31-ago: "interpreter shutdown"). Vigilar:
   detector-perdida-contexto (streak=2, próximo run ~15:02) y reintentos
   semanales del lunes 07-sep.
