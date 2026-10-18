---
title: "Análisis — WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution (arXiv 2608.27454v1)"
type: research
fecha: 2026-09-17
---

# Análisis — «WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution»

**VERACIDAD:** [VERIFICADO]

**Fuente:** arXiv `2608.27454v1` [cs.AI], 27-ago-2026, licencia **CC BY 4.0** — https://arxiv.org/html/2608.27454v1 (HTML consultado por texto hoy 17-sep-2026). Autores: **Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan** (Google Research) y **Tu Vu** (Google Research / Virginia Tech); contactos declarados `lytang@google.com`, `ttvu@google.com`. Origen del hallazgo: carrusel de Instagram `Dcy01bglqFs` de `chris.enprod` (2-sep-2026), que **difunde** el paper sin aportar técnica propia (triaje de hoy 09:12 en `04-operations/backlogs/pendientes.md`).

**Nota de ruta:** la instrucción pedía `01-knowledge/research/analisis-wikiskill-2026-09-17.md`; ese directorio **no existe** (`ls` literal: `ls: no se puede acceder a '01-knowledge/research': No existe el archivo o directorio`). Se escribe en el directorio canónico `research/` de `joko-lab`, que es donde viven los análisis y el que escanea `tools/verificar_research.py`. El nombre de fichero pedido se conserva literalmente.

**Método y material:** volcado de texto del HTML de arXiv hecho hoy 09:05 (`document.body.innerText` con navegador real) → `/tmp/paper_wikiskill.txt`, **87.808 B** (no 85.769 chars como estimaba la nota previa), md5 `6fd6620605d1b08d36d4262ad64100a1`, 2.242 líneas, leído íntegro por tramos y filtrado con `grep -n`. Verificación cruzada contra la **fuente viva** hoy 12:2x: `curl` a la misma URL → `http_code=200 size=821003` (HTML) y 4 coincidencias de «Karpathy» (ver sección de correcciones). Todo sin GPU, sin descargar modelos, sin tocar servicios.

## Qué es

Framework de **auto-evolución de skills de agente** cuyo añadido frente a Trace2Skill, EvoSkill y SkillOpt es una **base de conocimiento persistente (el «wiki») que se compila entre iteraciones y no se resetea**. Lo que el agente aprende deja de estar disperso por los artefactos de cada iteración (histórico de propuestas, logs) y pasa a ser una capa propia. Frase de la introducción, literal: *«Inspired by Karpathy (2026)'s perspective on LLM Wiki, which advocates compiling experience into persistent, compounding knowledge»*.

No entrena pesos: las skills evolucionadas **se inyectan en el prompt** del agente de inferencia (Table 1: *«evolved skills are injected into the Inference Agent's prompt at inference time»*); la premisa del paper es que una skill captura conocimiento procedimental *«without updating model parameters»*.

## Arquitectura: tres capas (nombres de fichero reales)

- **`raw/`** — trazas de ejecución inmutables de cada iteración (razonamiento, llamadas a herramienta, salidas, respuesta final). *«To preserve the raw history, this layer is immutable.»* Las trazas viven aquí, pero el entorno resuelve el alias `traces/<task_id>` para los agentes que las leen.
- **`wiki/`** — conocimiento estructurado y acumulativo, mantenido durante toda la evolución: `patterns/` (un `.md` por patrón: modos de fallo y estrategias con workarounds), `index.md` (catálogo de una línea por patrón), `logs.md` (evolution log, lo actualiza el Wiki Maintainer) y **`skill-impact.md`** (lo escribe **programáticamente el harness** tras el gating: metadata de la propuesta, skill objetivo, **diff unificado**, puntuación de validación y veredicto aceptado/rechazado). *«The wiki is not reset between iterations, but rather accumulates and compiles knowledge continuously throughout the evolution process.»* Detalle verificado: el nombre del evolution log aparece como `logs.md` en §3.1 y como `wiki/log.md` en el prompt del Wiki Maintainer; el volcado conserva ambas formas.
- **`skills/`** — skills activas: `SKILL.md` (contenido completo, frontmatter YAML, *When to Apply / When NOT to Apply*) y **`PURPOSE.md`** (*«maps the skill back to the motivating Wiki patterns that inspired its creation or modification»*: Origin + Patterns Addressed + Evolution History).

## El bucle (4 componentes, §3.2)

1. **Inference Agent** ejecuta las tareas con las skills activas → trazas en `raw/`. **Sin acceso al wiki durante los rollouts de entrenamiento** (ver hallazgo).
2. **Wiki Maintainer** analiza trazas + wiki, diagnostica fallos, extrae estrategias que funcionaron y actualiza `patterns/`, `index.md` y `logs.md` con edición incremental (append/replace/insert_after).
3. **Skill Proposer** (agente ReAct multi-turno con `read_file`) lee el wiki, exige leer **≥4 trazas de ejecución** antes de proponer, prefiere **parchear** a crear, y entrega la propuesta con `finish(proposal)` (`create` con `skill_md` + `purpose_md`, `patch` con ediciones, o `no_action`).
4. **Gating & rollback** evalúa la propuesta sobre un split de validación: si no mejora, se **descarta** y las skills vuelven a la última configuración buena. El **wiki nunca se revierte**: *«the wiki W_k is never rolled back regardless of the acceptance decision»*. Si la validación llega al máximo (1.0) hay parada temprana.

## Cifras (verificadas con el volcado)

**Table 1** (§4.2, media de **3 runs independientes** del proceso completo de evolución, 5 benchmarks: LiveMath, SealQA, SpreadSheet, OfficeQA, ALFWorld):

| Modelo (sin skills) | mejor baseline | WikiSkill | Δ vs mejor baseline |
|---|---|---|---|
| Gemini-3.5-Flash 49,5 | EvoSkill 56,1 | **68,1** | +12,0 |
| Qwen-3.6-27B 39,4 | EvoSkill 53,3 | **63,3** | +10,0 |
| Gemma-4-31B 41,3 | SkillOpt 49,1 | **54,9** | +5,8 |
| Qwen-3.5-9B 29,9 | EvoSkill 42,3 | **47,4** | +5,1 |
| Qwen-3.5-4B 26,2 | SkillOpt 35,2 | **38,5** | +3,3 |

Cifras por benchmark de WikiSkill: Gemini-3.5-Flash pasa de 33,0→**72,6** en LiveMath, 50,5→**76,6** en SpreadSheet y 48,6→**60,7** en OfficeQA (en ALFWorld se queda en 85,9 = baseline, porque ya sacaba 100 % en validación y hubo parada temprana); Qwen-3.6-27B sube SpreadSheet 40,8→**81,7**, ALFWorld 52,8→**77,6**, LiveMath 33,9→**61,9**, SealQA 27,5→**41,6** y OfficeQA 42,1→**53,7**. Ganancias crecientes con el tamaño dentro de la familia Qwen: +12,3 / +17,5 / +23,9 puntos en 4B/9B/27B. Skills evolucionadas **compensan escala**: Qwen-3.5-9B con skills (47,4) supera a Qwen-3.6-27B sin skills (39,4).

**Table 3** (§5.1, ablación con Gemini-3.5-Flash sobre 4 benchmarks — sin ALFWorld—). El mapeo de cada fila a su configuración es **deducido de la prosa de §5.1** (las celdas Sí/No de "Wiki Access" no se conservan en el volcado de texto):

| Configuración | Media |
|---|---|
| Sin skills | 40,4 |
| Inference Agent con wiki **+** Skill Proposer sin wiki (sin Wiki Maintainer) | 45,3 |
| Inference Agent sin wiki **+** Skill Proposer sin wiki | 48,7 |
| Inference Agent con wiki **+** Skill Proposer con wiki | 60,9 |
| **Inference Agent sin wiki + Skill Proposer con wiki (configuración por defecto)** | **63,7** |

**El hallazgo que el post no cuenta (dos frases literales del §5.1):**

- Dar el wiki al **proponente** y ninguno al ejecutor: *«providing the Skill Proposer with access to the persistent wiki increases average benchmark performance from 48.7% to 63.7% (+15.0%), with substantial gains on LiveMath (51.3% to 72.6%) and SpreadsheetBench (49.9% to 76.6%)»*.
- Dar el wiki **también al ejecutor durante los rollouts EMPEORA**: *«reduces average benchmark performance from 63.7% to 60.9%, with a substantial drop on LiveMath from 72.6% to 64.8%»*. Hipótesis de los autores: si el ejecutor resuelve desde el wiki en vez de desde la skill, las trayectorias son **menos informativas** para desarrollar skills.

Otros datos de §5.2/§5.3: las skills de Qwen ocupan 118,9–128,6 líneas frente a 45,1 de Gemma-4-31B y 81,2 de Gemini-3.5-Flash; se crean 6,3–8,9 patrones y se editan 7,0–18,4 por modelo; SpreadSheet produce las skills más largas (142,5 líneas) y más patrones (9,8), LiveMath las más cortas (84,6) y menos (4,4). El caso de estudio (ALFWorld, Qwen-3.6-27B) muestra el mecanismo: en la iteración 0 una propuesta es **rechazada**, `skill-impact.md` **preserva el diff y el rechazo**, y en la iteración 1 el proponente sintetiza la actualización aceptada teniendo en cuenta ese rechazo. Table 5 (apéndice): el 39–52 % de las actualizaciones aceptadas llegan en las iteraciones 0–1 y el resto sigue en las fases media y tardía (el refinamiento no se agota al principio). Table 2 (transferencia entre modelos): las skills de Qwen-3.6-27B mejoran a Qwen-3.5-9B hasta 50,5 en SpreadSheet (vs 24,3 sin skills y 33,6 con las suyas), y hay **transferencia negativa** documentada: las skills de Qwen-3.5-4B hunden a Gemini-3.5-Flash en SpreadSheet de 50,5 a **18,1** porque codifican workarounds de bajo nivel que limitan a un modelo fuerte.

## Límites declarados por el paper (§Limitations)

1. **No evalúa retrieval ni triggering**: inyecta las skills completas en el prompt para aislar la calidad de la skill (*«eliminating skill triggering or retrieval failures as confounding variables»*), y admite que el retrieval *«becomes important as the number of available skills grows»*.
2. El gating exige **mejora estricta** en validación, así que **excluye propuestas neutras** que preservan el rendimiento inmediato pero podrían rendir después.
3. **No tiene mecanismo automático de poda del wiki**: patrones, logs y diffs se acumulan sin límite (*«Such pruning may become necessary as knowledge accumulates over longer evolution runs»*).
4. No cubre **horizontes muy largos** (cientos de acciones de entorno o varias horas).

## Aplicabilidad al lab local

**(a) El lab ya tiene la arquitectura equivalente, pero a mano.** `skills/` ↔ `~/.hermes/skills` (**206 ficheros `SKILL.md`** contados hoy). `wiki/` ↔ `01-knowledge/objects/` (17 `RULE-*.yaml`, 64 objetos en total) + `04-operations/backlogs/` (backlog activo **708.344 B / 2.358 líneas** medidos hoy) y los ledgers de `04-operations/metrics/` (`lecciones_ledger.jsonl`, `mel_ledger.jsonl`, `operations_ledger.jsonl`, `evolution.jsonl`, `knowledge_health.jsonl`). `raw/` ↔ `04-operations/metrics/sesiones/sesiones-*.jsonl` (**83 ficheros**) más `pipeline_obs.jsonl`. La diferencia real: el lab **no** auto-evoluciona skills; cada cambio de skill pasa por decisión humana.

**(b) Lo que falta de verdad, y es pequeño:** **`PURPOSE.md` por skill** (0 ficheros en `~/.hermes/skills`) y un **`skill-impact.md`** (0 ficheros en `/home/jokoalmi` hasta profundidad 6). El lab registra el resultado de sus *evoluciones del sistema* en `evolution.jsonl` y lecciones en `lecciones_ledger.jsonl`, pero no tiene, por skill, el diff de la propuesta + veredicto + motivo en un sitio que el «proponente» lea antes de proponer. `PURPOSE.md` en cambio sería barato y encaja con la regla del lab de no crear bloques aditivos: mapear cada skill a las RULE/backlog que la motivaron es exactamente la traza que hoy hay que reconstruir a mano.

**(c) La regla medida — conocimiento al proponente, no al ejecutor.** El lab inyecta hoy RULE + memoria + índice de skills en el system prompt del **ejecutor** (Hermes en sesión). Según Table 3 eso **no rompe nada en el lab tal como está**, porque el ejecutor del lab no genera trazas de entrenamiento para evolucionar skills (el ciclo de skills tiene al usuario en medio). Pero si algún día se automatiza la evolución de skills, el orden importa y es contraintuitivo: **durante los rollouts de aprendizaje, el ejecutor no debe recibir el material del wiki** (RULE, backlog, lecciones), porque resolverá desde ahí y las trayectorias dejarán de informar sobre la skill. Es el mismo eje que la lección ya anotada de F1 (contexto fijo = dinero y atención): aquí además, **contexto de más en el ejecutor degrada la calidad del aprendizaje**.

**(d) El hueco de poda del wiki es el problema real del lab, y el paper lo declara pero no lo resuelve.** Backlog activo 708 KB / 2.358 líneas, `pendientes.md` 30.593 B, ledgers de métricas creciendo; el paper dice que su wiki acumula sin poda automática y que hará falta. Dato de enganche con lo ya medido en el lab (informe F1, 16-sep): el `index.md` «es la parte MÁS importante del wiki porque determina si los agentes leerán las páginas completas» — y en el lab el índice de skills pesa 4.020 tok de fijo con techo de poda ≈ −10 %, mientras que la palanca real eran las tools nativas (43,9 %). Conclusión honesta: **el paper valida que el problema existe y que es de la capa de conocimiento, no de la capa de ejecución**; no aporta el algoritmo de poda.

## Verificado / inferido / no verificado

- **Verificado contra fuente primaria** (volcado + fuente viva): identidad del paper (título, autores, fecha, licencia, URL HTTP 200), las tres capas con sus nombres de fichero, los cuatro componentes del bucle, la inmutabilidad de `raw/`, la no-reversión del wiki, los números de Table 1 y Table 3, la cita de Karpathy, los cuatro límites declarados, la inyección de skills en el prompt (sin entrenar pesos) y la ausencia de enlace a código en el texto leído.
- **Inferido** (deducido, no literal): el mapeo fila↔configuración de Table 3 (las celdas Sí/No no están en el volcado de texto; el mapeo sale de las frases de §5.1 que citan 48,7 / 63,7 / 60,9); la equivalencia capa-a-capa con el lab (`rails` del lab = capas del paper) es analogía mía, no afirmación del paper; la lectura de que Table 3 **no obliga a cambiar nada hoy** en el lab.
- **No verificado / no disponible**: el **«kit» del autor** que se promete en el post de Instagram a quien comente BRAIN — **el lab no tiene acceso al DM de Instagram**, así que no hay forma de analizarlo hasta que lo traiga el usuario (si llega, contrastarlo con el paper). Tampoco hay en el paper enlace a repo/código ni cifras de coste en dólares.

## Corrección de un dato del triaje previo

La nota de triaje de las 09:12 afirmaba: *«la atribución "inspirado en el LLM Wiki de Karpathy" (Karpathy no aparece en el paper)»*. **Es incorrecto**: el paper SÍ lo cita y lo declara como inspiración. Literal de la introducción (§1): *«Inspired by Karpathy (2026)'s perspective on LLM Wiki, which advocates compiling experience into persistent, compounding knowledge»*, y en la bibliografía (referencia `Karpathy (2026) A. Karpathy LLM Wiki. Note: GitHub Gist`, marcada *Cited by: §1*). Confirmado además contra la fuente viva (4 coincidencias de «karpathy» en el HTML servido por arXiv hoy). La atribución del post de Instagram, por tanto, **es correcta**; el dato erróneo era la comprobación previa (probablemente por buscar sobre un volcado parcial). Queda corregido aquí y en la entrada del backlog; la línea de `pendientes.md` conserva su texto original íntegro y lleva añadido el marcador de HECHO con la corrección.

## Fuentes y fechas

- Paper (primaria): arXiv `2608.27454v1` [cs.AI], 27-ago-2026, CC BY 4.0, https://arxiv.org/html/2608.27454v1 (consultado 17-sep-2026 por la mañana; re-verificado HTTP 200 al mediodía).
- Origen del hallazgo: carrusel de Instagram `Dcy01bglqFs` de `chris.enprod` (2-sep-2026), solo difusión; triaje en `04-operations/backlogs/pendientes.md` (entrada 2026-09-17 09:12).
- Datos del lab citados: `04-operations/backlogs/2026-07-31-backlog.md` y `pendientes.md` (`stat -c '%s %y'` de hoy), `04-operations/metrics/` y `~/.hermes/skills` (contajes de hoy).

**Registro de escritura:** fichero nuevo creado hoy 17-sep-2026 (no había versión previa, por lo que no procede backup). Las medidas publicadas (bytes y md5) son las del fichero **después** de pasar `tools/verificar_research.py --archivo research/analisis-wikiskill-2026-09-17.md` (sin `--juez`/`--llm`, para no cargar modelos), y van en la entrada del backlog activo y en el reporte: esta misma sección no puede contener el hash del fichero que la contiene.
