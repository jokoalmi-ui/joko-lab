# AGENTS.md — contrato para agentes que trabajan en `hermes-lab`

> **Para quién es esto.** Para cualquier agente de IA que trabaje **dentro** de este
> repositorio: el gate del `pre-commit`, Codex / opencode / Claude Code, o un subagente
> delegado. Al escribir este fichero, en este repo no existía ningún `AGENTS.md` ni
> `CLAUDE.md`.
>
> **Qué manda.** La constitución de este repo es **`HERMES.md`** (13 secciones). La
> fuente de verdad del contenido es **`docs/`**: «`docs/` es la única fuente de verdad. `certification/` verifica, no define.»
> Las reglas del lab son los **18 `RULE-*.yaml` activos** de
> `~/joko-lab/01-knowledge/objects/`. Este fichero **no sustituye a nada de eso**: es
> un enrutador. Si aquí pone una cosa y una RULE activa dice otra, **gana la RULE**.
>
> **Dos repos, un lab.** `~/joko-lab` es el lab (reglas, backlogs, investigación).
> `~/hermes-lab` es este: la casa del asistente. No se mezclan.

## 0. Quién decide

- El dueño es **Joseba**. El agente **propone**; él decide y da el veredicto final
  («Confianza solo en datos reales; veredicto final del usuario»).
- «Ok» o «vale» es un **acuse**, no una autorización. Un «sí» a una pregunta cerrada
  sí autoriza.
- Antes de cualquier escritura: **qué fichero**, **qué cambio**, **qué riesgo**,
  **cómo se revierte**. Y si el fichero no está versionado, copia previa primero
  (RULE-007).

## 1. Las 18 reglas activas (título literal) y qué te obligan aquí

Las RULE viven en `~/joko-lab/01-knowledge/objects/`. El índice maestro está en
`~/joko-lab/AGENTS.md` («## 1. Las 18 reglas activas (título literal; léelas antes de
actuar)»). Este bloque se repite aquí **a propósito**: un agente que trabaje en este
repo no debe tener que salir de él para saber qué reglas le aplican. El texto normativo
es el fichero de cada RULE, no este resumen.

**Te afectan directamente aquí (scope `hermes-lab` y `todo_joko_lab`):**

- **RULE-006** (`hermes-lab`) — «Recibo SHA obligatorio antes de commit en hermes-lab.»
  La más importante de este repo: **ningún commit entra sin recibo**. Detalle en §3.6 y §6.
- **RULE-007** (`todo_joko_lab`) — «Antes de modificar un archivo existente sin
  versionar en git, crear copia de seguridad (cp archivo archivo.bak-YYYYMMDD).»
- **RULE-008** (`todo_joko_lab`) — «El .bak-YYYYMMDD vive en la misma carpeta del
  fichero original»; «Prohibido crear .bak-* en ~/ (home) o fuera de
  joko-lab//hermes-lab/»
- **RULE-001** (`todo_joko_lab`) — «Usar Gemma 4 (google/gemma-4-12b-qat) para tareas de
  creatividad, brainstorming y código completo.»
- **RULE-002** (`todo_joko_lab`) — «Usar Granite 4.1 temp=0.3 para JSON estructurado.»
- **RULE-003** (`todo_joko_lab`) — «Usar gpt-oss-20b (LM Studio) para razonamiento paso
  a paso y tareas batch.»
- **RULE-004** (`todo_joko_lab`) — «Bloquear Qwen 3.5 — descartado (0/5 tests). Ver
  [[DEC-001]]»
- **RULE-005** (`todo_joko_lab`) — «Actualizar GUIA-JOKO-LAB.md ante cada cambio
  estructural del laboratorio, en la misma sesion. Origen: norma JL-013»
- **RULE-009** (`todo_joko_lab`) — «Usar LFM 2.5 (lfm2.5-2.6b) para tool calling y
  tareas ageneticas ligeras»
- **RULE-010** (`todo_joko_lab`) — «Activar el Mission Runner solo cuando la misión lo
  REQUIERA»
- **RULE-011** (`todo_joko_lab`) — «Escritura mínima de memoria episódica (integrada con
  RULE-009, sin duplicar)»
- **RULE-014** (`todo_joko_lab`) — «LEC: si existe skill para la tarea, EJECUTARLA (no
  improvisar desde memoria)»
- **RULE-015** (`todo_joko_lab`) — «Instrumentos de medición: validar la métrica antes
  de confiar; umbrales NO a priori»

**Gobiernan al asistente (y por tanto a ti, si eres uno):**

- **RULE-012** — «No afirmar hora/fecha sin ejecutar date primero»
- **RULE-013** — «Confianza solo en datos reales; veredicto final del usuario»
- **RULE-016** — «Nueva versión de Hermes Agent: investigar incidencias 5 días ANTES de
  actualizar en el lab»
- **RULE-018** — «Un proceso de fondo (curador de Hermes) NO escribe skills del lab sin
  OK: si una skill cambia bajo tus pies, parar y reportar»

**De vigilancia de contenido (aplican si tocas monitores o feeds):**

- **RULE-017** — «Canales de contenido NO confiables: 2 datos falsos burdos verificados
  -> excluir del monitor»

## 2. Prohibiciones por defecto: requieren OK explícito

- **Nada destructivo**: borrar, mover, `chmod`, `chown`, `sudo`, matar procesos. Primero
  diagnóstico, después acción: «Priorizar siempre comandos de diagnóstico antes que
  comandos correctivos.»
- **No tocar servicios ni contenedores** del host (stack de automatización, n8n) ni la
  configuración o el estado de `~/.hermes`. Este repo es la casa del asistente, **no**
  su configuración en caliente.
- **`/mnt/ssd_ia_datos` es solo lectura**, con una excepción: el push al bare de este
  repo (`origin`).
- **No instalar software nuevo** sin OK explícito.
- **Credenciales**: no se pegan en el chat ni se imprimen por pantalla («API Keys»);
  viven en fichero local con permisos restringidos y se leen dentro del proceso.
- **No commitear sin recibo**, y **no commitear «de paso» ficheros ajenos**: mide el
  diff y di su alcance real antes de commitear.
- **No afirmar hora ni fecha** sin ejecutar antes `date`.

## 3. Ciclo obligatorio de trabajo

1. **Leer antes de escribir.** La RULE que aplique y, en este repo, `HERMES.md` §6–§13.
   Si existe una skill para la tarea, **se ejecuta** (no se improvisa).
2. **Medir, no deducir.** La cifra manda y va con su comando o su fichero. Un recuento
   escrito por otro documento **no** es fuente: `docs/estado-real.md` iba por detrás
   («Última actualización: 2026-07-14»).
3. **Cambio mínimo y aditivo**, con copia previa en la **misma** carpeta del fichero
   (RULE-007/008).
4. **Lo mecánico va en script fail-closed**: si el estado real no es el esperado, no
   actúa. Nada de `rm`; para temporales, directorio nuevo.
5. **Verificar leyendo el otro lado**: el fichero en disco, el blob en `HEAD`, el bare
   con `ls-remote`. La impresión de haberlo hecho no es prueba.
6. **Commit solo con recibo**: generar el recibo **después** de tener el staging final,
   y commitear. Si algo cambia después de revisar, el recibo queda invalidado y se
   bloquea el commit.
7. **Cerrar el ciclo documental**: cambio estructural → decisión en
   `docs/decisiones/` + `docs/` + `CHANGELOG.md`. «Documentar siempre antes de pasar a
   la siguiente tarea.»

## 4. Mapa de este repo (medido el 2026-09-29)

- **`HERMES.md`** — constitución: identidad, principios, orden de consulta, ciclo de
  skills, flujo de desarrollo, convenciones, seguridad, certificación (13 secciones).
- **`docs/`** — única fuente de verdad. Incluye `arquitectura.md`, `estado-real.md`,
  `hermes-internals.md`, `metodologia.md`, `joko-lab-principles.md` y `decisiones/`
  (34 entradas). Subcarpetas: `auditorias/`, `benchmark/`, `hypothesis/`, `archived/`.
- **`skills/`** — 11 dominios; **10 con `SKILL.md`**. El que no lo tiene es
  `ai-architecture` (pendiente, no lo inventes).
- **`scripts/`** — 13 `.sh` (entre ellos `smoke-test.sh`, `checkpoint.sh`, `rescue.sh`,
  `fin.sh` y los `backup-*.sh`).
- **`certification/`** — 8 entradas de primer nivel; **verifica, no define**.
- **`hooks/`** — 3 ficheros: `pre-commit` (el gate), `generar_recibo.sh` (el recibo) y
  `pre-commit.bak-20260803`.
- **`tests/`** — 3 `test_*.py`: `test_contract.py`, `test_decision_engine.py`,
  `test_state_manager.py`.
- **Subsistemas**: `runtime/`, `decision-engine/`, `loop-engineering/`,
  `state-manager/`, `observability/` (con su `CONTRACT.md` donde aplica).
- **No versionado** (`.gitignore`): `logs/`, `backups/`, `recovery/` (772 entradas contando subcarpetas,
  «Puntos de recuperación (pueden ser grandes por sessions.jsonl)»), `*.bak*`. Los
  backups de ficheros del lab sí van dentro del árbol: «Backups RULE-008 (no versionar)».

## 5. Convenciones (están en `HERMES.md` §7: no las reinventes)

- **Nombres**: documentación `snake-case.md`; decisiones `AAAA-MM-DD-tema.md`; scripts
  `kebab-case.sh`; una skill por dominio, sin mezclar responsabilidades.
- **Documentación**: un tema por fichero; no duplicar lo que ya existe; no reescribir un
  documento entero sin que se pida.
- **Decisiones**: «Las decisiones técnicas van siempre en `docs/decisiones/` con el
  formato: contexto, problema, alternativas, decisión, motivos, consecuencias, estado.»
- **Commits**: `tipo: mensaje breve sin punto final`, con `feat:`, `fix:`, `docs:`
  («Cambios en documentación»), `chore:` («Mantenimiento, init, configuración»).
- **Bash**: «Los scripts en Bash usan `set +e` (el laboratorio prefiere control manual de errores).» También `--help` y el modo silencioso `--quiet`.
- **Estilo de respuesta**: «Cuando se ejecuten comandos, muestra primero la salida
  obtenida y después un resumen.»

## 6. Cómo se ejecuta, se comprueba y se mide

- **El gate**: `hooks/pre-commit`, que abre con esta cabecera literal:

  ```
  # pre-commit — Gate determinista: bloquea el commit si el árbol en
  # staging no coincide con un recibo generado tras revisión explícita.
  ```

  Falla cerrado («BLOQUEADO: no hay recibo para este árbol.») y su veredicto se
  registra en `~/.hermes/logs/joko-rdd.log`.
- **El recibo**: `hooks/generar_recibo.sh <nombre> [nota]`; el gate recalcula el árbol y
  compara. «Un solo byte cambiado invalida el recibo.» El recibo vive en
  `RECIBO_FILE="${GIT_DIR}/joko-recibo.json"`, fuera de control de versiones.
- **El mecanismo, literal de RULE-006**: «1. Congelar: hash del arbol en staging con
  `git write-tree` (nativo de Git, determinista).» … «4. Gate: el hook pre-commit
  recalcula el hash del staging; si no hay recibo o el hash diverge (se toco algo
  despues de revisar), el commit se bloquea.»
- **Kill switches** (documentados, no silenciosos): «JOKO_RDD_DISABLE=1: desactiva el
  gate una sola vez (aviso en el log del hook).» y «Fichero .joko-rdd-disable en la
  raiz del repo: desactiva para todo el repo (aviso).» «Nunca bypass implicito por
  patron de mensaje»: no hay atajo por el texto del commit.
- **Alcance del gate**: «Gate instalado en los DOS repos git del lab: hermes-lab
  (2026-08-03) y joko-lab (2026-09-29), ambos con core.hooksPath=hooks y hooks
  byte-identicos (sha256 verificado).»
- **Cierre de sesión**: `scripts/fin.sh`. Aquí es un wrapper: «La implementacion real
  esta en:» `~/joko-lab/02-infrastructure/fin/fin.sh`; si no está, «Usando fallback:
  checkpoint clasico».
- **Comprobaciones rápidas** (todas de lectura):

```bash
git rev-parse --short HEAD            # qué commit es en realidad
git status --porcelain | wc -l        # cuántos ficheros pendientes hay
git log -1 --stat --format='%H %s'    # qué entró en el último commit
```

- **Tests**: `tests/` usa `unittest` y cada fichero se lanza por sí mismo
  («unittest.main(verbosity=2)»): 3 `test_*.py` (contrato, decision-engine,
  state-manager).
- **Lo que NO existe todavía**: no hay validador automático de este fichero. Medido:
  `gga` no está instalado y `hooks/pre-commit` no contiene ninguna referencia a GGA. Hoy
  el cumplimiento lo sostienen el gate del recibo, los tests de `tests/` y la revisión
  humana.

## 7. Estado al escribir este fichero (2026-09-29 21:04 CEST)

- Rama `master`; `core.hooksPath=hooks`; en `.git/hooks` no hay hooks activos (solo
  `.sample`): el gate vive en `hooks/`, versionado.
- `hooks/pre-commit` md5 `df169c48f943f10c6a18fda6c0613b71` y
  `hooks/generar_recibo.sh` md5 `63670ea09bdbfb827f1468a7a612d0e3` — **los mismos** que
  en `joko-lab`, como declara RULE-006.
- Remotos: `origin` = `/mnt/ssd_ia_datos/hermes-lab.git` (bare **local**, mismo SSD: no
  es copia externa) y `github` = `git@github.com:jokoalmi-ui/joko-lab.git` (SSH). El
  remoto se llama `joko-lab` aunque la carpeta sea `hermes-lab`: es correcto, no un error.
- Repo: 1035 ficheros sin contar `.git` ni este fichero; 18 RULE activos, 1 de ellos con
  scope `hermes-lab` (RULE-006).
- **Los datos que caducan no se copian: se miden.** Este fichero evita a propósito
  meter a mano el commit de `HEAD` o el número de pendientes; para eso están las órdenes
  de §6.

---

Si algo de este fichero no se puede comprobar con una orden o un fichero, **no lo uses**:
mídelo y sigue la RULE que aplique.
