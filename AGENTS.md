# AGENTS.md — instrucciones para agentes que trabajan en joko-lab

> **Para quién es esto.** Para CUALQUIER agente de IA que trabaje DENTRO de este repo
> (el hook de revisión en el pre-commit, opencode / Codex / Claude Code, subagentes
> delegados). Medido 2026-09-29: no existía ningún `AGENTS.md` ni `CLAUDE.md` aquí.
> **Autoridad.** Las reglas del lab son los `RULE-*.yaml` de `01-knowledge/objects/` y las
> normas constitucionales JL de `lpa/constitucion/normas-jl.md`. Este fichero es un
> **enrutador**: si algo de aquí contradice una RULE activa, **manda la RULE**. Antes de
> actuar, abre la RULE aplicable; no improvises desde la memoria del modelo.

## 0. Qué es esto y quién decide

- Joko Lab es un **laboratorio reproducible** para estudiar, comparar y mejorar agentes de
  IA. No es un producto ni "un agente": es el sistema operativo para trabajar con IA.
- Dueño: **Joseba**. El agente **propone**; él **decide y autoriza**. "Ok" es un acuse, no
  una autorización; una escritura o una acción sobre servicios necesita OK directo.
- Dos repos hermanos: **`~/joko-lab`** (este, el lab) y **`~/hermes-lab`** (configuración y
  decisiones del asistente Hermes). Reglas de commit: RULE-006 (recibo SHA).

## 1. Las 21 reglas activas (título literal; léalas antes de actuar)

Ficheros: `01-knowledge/objects/RULE-0XX.yaml` — claves `title`/`desc`/`body` + `domain`,
`scope`, `confidence`, `next_review`, `expires`. `[...]` = cita recortada.

- **RULE-001** (ai-architecture / todo_joko_lab): "Usar Gemma 4 (google/gemma-4-12b-qat) para tareas de creatividad, brainstorming y código completo. […]"
- **RULE-002** (ai-architecture / todo_joko_lab): "Usar Granite 4.1 temp=0.3 para JSON estructurado. […]"
- **RULE-003** (ai-architecture / todo_joko_lab): "Usar gpt-oss-20b (LM Studio) para razonamiento paso a paso y tareas batch. […]"
- **RULE-004** (ai-architecture / todo_joko_lab): "Bloquear Qwen 3.5 — descartado (0/5 tests). Ver [[DEC-001]] […]"
- **RULE-005** (joko-lab / todo_joko_lab): "Actualizar GUIA-JOKO-LAB.md ante cada cambio estructural del laboratorio, en la misma sesion. Origen: norma JL-013 […]"
- **RULE-006** (joko-lab / **hermes-lab**): "Recibo SHA obligatorio antes de commit en hermes-lab. […]"
- **RULE-007** (joko-lab / todo_joko_lab): "Antes de modificar un archivo existente sin versionar en git, crear copia de seguridad (cp archivo archivo.bak-YYYYMMDD). Prohibido write_file (reemplazo completo) sobre archivo existente sin backup previo. […]"
- **RULE-008** (joko-lab / todo_joko_lab): backup **dentro del árbol** — "El .bak-YYYYMMDD vive en la misma carpeta del fichero original"; "Prohibido crear .bak-* en ~/ (home) o fuera de joko-lab//hermes-lab/".
- **RULE-009** (ai-architecture / todo_joko_lab): "Usar LFM 2.5 (lfm2.5-2.6b) para tool calling y tareas ageneticas ligeras […]"
- **RULE-010** (ai-architecture / todo_joko_lab): "Activar el Mission Runner solo cuando la misión lo REQUIERA"
- **RULE-011** (operaciones / todo_joko_lab): "Escritura mínima de memoria episódica (integrada con RULE-009, sin duplicar) […]" — el registro va al ledger especializado, no a la memoria del agente.
- **RULE-012** (proceso / asistente_hermes): "No afirmar hora/fecha sin ejecutar date primero"
- **RULE-013** (proceso / asistente_hermes): "Confianza solo en datos reales; veredicto final del usuario"
- **RULE-014** (proceso / todo_joko_lab): "LEC: si existe skill para la tarea, EJECUTARLA (no improvisar desde memoria)"
- **RULE-015** (proceso / todo_joko_lab): "Instrumentos de medición: validar la métrica antes de confiar; umbrales NO a priori"
- **RULE-016** (proceso / actualizaciones_hermes_agent): "Nueva versión de Hermes Agent: investigar incidencias 5 días ANTES de actualizar en el lab"
- **RULE-017** (contenido / canales_contenido_vigilados): "Canales de contenido NO confiables: 2 datos falsos burdos verificados -> excluir del monitor"
- **RULE-018** (proceso / skills_del_lab): "Un proceso de fondo (curador de Hermes) NO escribe skills del lab sin OK: si una skill cambia bajo tus pies, parar y reportar"
- **RULE-019** (ai-architecture / todo_joko_lab): "MoE que no cabe en VRAM: se lanza con la cache de expertos (--moe-cache-mib 512), nunca con 0" (alta 09-oct-2026)
- **RULE-020** (contenido / cv_entregables_ofertas): "CV para ofertas: prototipo de 2 columnas en 1 hoja A4 (Courier 7,6 pt) y el entregable de «1 hoja» es el PDF de Chrome, nunca el DOCX" (alta 10-oct-2026)
- **RULE-021** (proceso / todo_joko_lab): "El estado ok con el error descartado es un falso ok: quien invoca un binario o un motor no silencia su error, y el ok se acredita en el artefacto" (alta 12-oct-2026)

Las RULE se revalidan (clave `next_review`) y caducan (`expires`): para comprobar vencidas,
`tools/revalidar_kos.py` (solo lectura).

## 2. Prohibiciones (requieren OK explícito de Joseba; por defecto NO)

- **Servicios y contenedores.** Nada de `docker compose restart|stop|down|up`, prunes ni
  `kill`. **n8n es zona protegida**: no tocarlo sin confirmación explícita.
- **Rutas protegidas**: `/mnt/ssd_ia_datos/` y todo lo que contiene (`n8n/`, `exports/`,
  `backups/`, `ollama/`, `*.git/`, `obsidian-vault/`, `DOCUMENTACION PARA JUICIO/`,
  `SALVADO/`). El remoto de este repo es un **bare local** en ese disco.
- **Nada destructivo**: sin `rm`, `mv`, `chmod`, `chown`, `sudo`, `prune`, ni reiniciar la
  máquina. Reiniciar solo lo hace Joseba. **No se borra: se archiva** (`.archive/`, `*.bak-*`).
- **Instalar software nuevo** o añadir dependencias: necesita OK explícito.
- **Credenciales**: nunca en el repo, en el chat ni en logs. Viven en `~/.hermes/.env` o en
  ficheros `chmod 600`; al citarlas, `[REDACTED]`. No imprimas tokens, ni `Authorization`,
  ni dumps de sesión.
- **No tocar** `~/.hermes/` (config, `state.db`, skills) ni `~/automation-stack`: es el
  entorno del agente, no el contenido del lab.
- **Commits**: no se commitea sin recibo (§4). No reescribir historia (`--force`, rebase de
  ramas compartidas) sin OK.

## 3. Cómo se trabaja aquí (ciclo obligatorio)

1. **Leer la RULE aplicable** y, si existe, la skill del lab para esa tarea (RULE-014).
2. **Medir antes de afirmar.** Toda cifra se mide, y las medidas importantes con **dos
   instrumentos independientes** (RULE-015). Hora/fecha: ejecutar `date` primero (RULE-012).
   Si un dato no está en la salida real, se dice "no aparece en la salida": no se rellena.
3. **Editar al mínimo y de forma aditiva**: `patch`/append, nunca reescribir en bloque.
   Backup `.bak-YYYYMMDD` en la misma carpeta antes de tocar un fichero existente
   (RULE-007/008). Para ficheros de registro, usar la plantilla oficial del lab.
4. **Script con asertos, fail-closed**: si un dato esperado no se cumple, **abortar antes de
   escribir**. Nada a medias.
5. **Verificar leyendo el otro lado**: relee el fichero escrito, `git diff --stat`,
   `git status --porcelain`, cuenta de líneas y md5. "Hecho" = salida real, no intención.
6. **Commit solo con recibo**: `hooks/generar_recibo.sh "<quien-aprueba>" ["nota"]` y luego
   `git commit`. El hook `hooks/pre-commit` (activado con `core.hooksPath=hooks`) **aborta**
   si un solo byte en staging no coincide con el recibo. Kill switch documentado y
   trazado: `JOKO_RDD_DISABLE=1` (una vez) o `.joko-rdd-disable`; el log es
   `~/.hermes/logs/joko-rdd.log`.
7. **Si el cambio es estructural** (servicio, modelo, ruta, protocolo, skill): actualizar
   `GUIA-JOKO-LAB.md` **en la misma sesión** (RULE-005).
8. **Registrar** el cierre en el ledger que corresponda (RULE-011) y, si la lección es
   reutilizable, en la skill del lab (RULE-018: un proceso de fondo no escribe skills sin OK).

## 4. Mapa del repo

- `01-knowledge/` — lo que sabemos: `objects/` (RULE, DEC, PATTERN, EXP en YAML),
  `patterns/`, `experiments/`, `models/`.
- `02-infrastructure/` — lo que lo sostiene: `inicio/`, `fin/`, `recovery/procedures/`,
  `services/`, `docker/`, `network/`.
- `03-automation/` — lo que se ejecuta solo: `cron/`, `scripts/`, `tests/`, `workflows/`.
- `04-operations/` — lo que se registra: `backlogs/pendientes.md`, `metrics/` (ledgers
  `*.jsonl`), `reports/`, `decisions/` (DEC-*), `proposals/`, `kap/`, `inputs/`.
- `05-inference/` — lo que hacemos con lo anterior: `router/`, `compiler/`, `validators/`,
  `evaluators/`, `executors/`, `feedback/`.
- `tools/` — 176 ficheros (gates y utilidades). `tests/` — 25 `test_*.py` (unittest).
- `research/` (análisis), `verification/` (banco de evaluación), `instruments/`, `lpa/`
  (programa LPA: `constitucion/`, `contracts/`, `experiments/`, `incidentes/`, `meta/`),
  `docs/`, `reports/`, `USAGE/`, `founderz/`, `tfm/`, `assets/`, `inbox/`.
- **Puntos de entrada**: `README.md` (qué es), `index.md` (índice OKF v0.2, el único con
  `okf_version`), `GUIA-JOKO-LAB.md` (índice maestro, mantenido a mano — **puede ir por
  detrás**: comprueba sus cifras contra los ficheros (al 13-oct-2026 declara 21 RULEs).

## 5. Convenciones de contenido

- Todo `.md` no reservado lleva **frontmatter YAML parseable** con `type` no vacío
  (`index.md` y `log.md` son nombres reservados: sin frontmatter).
- Fechas **ISO 8601 UTC**. La confianza se infiere de `sources`/`verified`, no de un score.
- Los objetos de `01-knowledge/objects/` son **YAML** (se comparan por semántica de claves),
  no documentos OKF.
- Los `*.bak*` **no se versionan** (`.gitignore`); el árbol del repo es solo texto y código.
- Etiquetas de veracidad en los análisis: `[VERIFICADO]` / `[ALCANCE INTERNO]` /
  `[NO VERIFICADO]` / `[REVISAR]` (`tools/verificar_research.py`,
  `tools/verificador_alucinaciones.py` — exit 1 bloqueante —, `tools/contrastar_externo.py`).
- Informes y conclusiones **en prosa**; el material repetitivo, condensado (`.txt`).
- No dupliques una regla: se cita por su id (`RULE-0XX`) y vive en un solo sitio.

## 6. Ejecutar, comprobar y medir

- Abrir sesión: `~/joko-lab/02-infrastructure/inicio/inicio.sh` (294 líneas) → estado
  inicial y comparación con el último cierre.
- Cerrar sesión: `~/joko-lab/02-infrastructure/fin/fin.sh` (288 líneas) → estado final,
  backup si hay cambios y checkpoint de `hermes-lab` a `origin` (el bare local; el remoto
  `github` **no** se toca por defecto).
- Tests: `python3 -m unittest discover -s tests`.
- Gates de contenido: `tools/verificar_fk_kos.py --gate` (integridad referencial),
  `tools/revalidar_kos.py` (KOs vencidos), `tools/lock-backlog.sh` (lock de backlogs entre
  sesiones paralelas).
- Modelo local por tarea: `tools/llm-router.sh` y RULE-001/002/003/004/009.

## 7. Estado al escribir este fichero (2026-10-13 22:50 CEST)

- `joko-lab`: rama `master`, `core.hooksPath=hooks`; remoto `origin` =
  `/mnt/ssd_ia_datos/joko-lab.git` (bare local; **no hay remoto externo** de este repo).
- `hermes-lab`: rama `master`; remotos `origin` (bare local) y `github`
  (`git@github.com:jokoalmi-ui/joko-lab.git`, SSH).
- 21 `RULE-*.yaml` (todas `status: activo`), 176 ficheros en `tools/`, 25 `test_*.py` en `tests/`.

**Aquí no se citan HEAD ni el número de cambios pendientes**: cambian con cada commit y
quedarían falsos de inmediato. Mide los tuyos: `git log -1 --format='%h %ad'` y
`git status --porcelain | wc -l`. Las cifras de arriba son fotografía: vuelve a medirlas
antes de usarlas.
