---
title: "Analisis -- atareao 833: Workflows de IA, automatiza tu dia con Ollama y Docker (21-sep-2026)"
type: research
---

# Analisis -- atareao 833 «Workflows de IA, automatiza tu dia con Ollama y Docker»

**VERACIDAD:** [VERIFICADO]
completo descargado (30.452 chars); cifras re-verificadas una a una contra ese texto.
**VEREDICTO = ALCANCE INTERNO** (juicio del lab sobre contenido externo).
**Fuente:** https://youtu.be/l9fdzL8sOFs (atareao, canal `UCP8dTCaLNJFxfklb_GNqe6A`, episodio 833,
subido 2026-09-21, 1.823 s, 151 vistas al consultar) + articulo https://atareao.es/podcast/833
(ahi va el codigo completo de los 4 workflows; **no hay repo del episodio**).
**Consulta:** 2026-09-21 21:48:16 CEST · **Metodo:** metadatos + articulo + codigo del articulo + conteos medidos en
`research/` y en el lab. Coste 0: sin GPU, sin transcribir, sin descargar modelos, sin ejecutar nada.

**Veredicto en una linea:** **VALIDACION (sin entrada)** -- es el capitulo siguiente de una serie que
el lab ya sigue (7 ficheros de atareao en `research/`), y sus 4 workflows **ya existen en el lab de
otra forma**. Lo unico nuevo son **2 patrones** (abajo, con senal de activacion) y el **censo de sus
5 repos**, que se registra por la excepcion de la skill `triaje-contenido-externo` («el post no entra
pero sus fuentes si aportan»). El usuario pidio expresamente esta ficha el 21-sep-2026.

## 1. Que es (verificado)

Episodio de arquitectura y opinion, sin demo de codigo en el video: su tesis es la **«IA hibrida»**
-- *«no uses un LLM para todo; usalo solo donde aporta valor»*, con checks deterministas para lo
determinista (disco, servicios, memoria) y LLM solo donde interpreta (logs, clasificacion, resumen,
busqueda). Compara su reescritura en **Rust** de 4 automatizaciones que antes tenia en **Bash**:
**520 lineas / 11 scripts** (deps: `curl`, `jq`, `xmlstarlet`, `html2text`, `python3`, `pip`) frente a
**1.750 lineas / 38 ficheros / 15 tests** en Rust, **binarios estaticos de 5-8 MB**, 0 dependencias
del sistema. Stack declarado: Ollama (`llama3.2:3b` ~2 GB + `bge-m3` 1,2 GB / 1024 dim / «100+
idiomas»; alternativa ligera `qwen2.5:1.5b` ~1 GB), SQLite con WAL, SearXNG, Docker/Podman o
systemd, `just`. Minimos declarados: **3,2 GB de disco / 4 GB de RAM**, y dice que funciona con 8 GB.

## 2. Posicion en la serie (por que NO es novedad)

La skill de triaje obliga a comprobar si es capitulo de serie y a decir **que anade y que repite**.
En `research/` hay **7 ficheros de atareao** (`analisis-atareao824-fd-rg-pipelines.md`,
`analisis-atareao831-mcps-2026-09-17.md`, `analisis-atareao-gpu-3000-local-lab.md`,
`analisis-atareao-hermes-searxng-invidious.md`, `analisis-opencode-orquestador-agentes-atareao.md`,
`analisis-serie-atareao-ia-local.md` y `analisis-atareao-graphrag-20260921.md` de hoy). El 833 es
**el capitulo siguiente al 831** (MCPs, analizado el 17-sep) y el propio autor lo situa como
continuacion del 829 (skills) y el 831.

El video no esta cubierto por el monitor de YouTube del lab
(atareao no esta entre los 7 canales vigilados): llego porque el usuario paso la URL.

- **QUE REPITE**: los 4 workflows completos (los 4 ejes ya estan cubiertos, ver §4), el patron
  «timeouts + JSON estricto + idempotencia» y la conclusion «local-first y sin dependencias».
- **QUE ANADE**: (a) el par **rate-limiting de alertas + modo dry-run** en monitorizacion; (b) el
  **formato de empaquetado** (un binario Rust unico con servidor MCP propio) pensado para maquinas
  sin GPU; (c) el **censo de sus repos** (§7), con 2 proyectos suyos activos el 19-sep.

## 3. Los 4 workflows (codigo real del articulo)

1. **noticias-bot** -- RSS -> filtro por keywords **antes** de llamar al LLM -> resumen <20 palabras ->
   Telegram. Dedup por **SHA256 + `UNIQUE`** e `INSERT OR IGNORE`. **`timeout` de 30 s** en la llamada
   a Ollama («si el LLM se cuelga, el workflow sigue con el siguiente articulo»).
2. **tareas-bot** -- Telegram long polling -> clasificacion GTD a **JSON estricto** -> SQLite
   (`bot_state`, `tasks`, `processed_messages`). Guardrails: confirmacion con `reply_to_message_id`,
   **offset persistido** (no pierde mensajes al reiniciar) y extractor «primer `{` ... ultimo `}`»
   para cuando el modelo se desvia del formato.
3. **monitor-bot** -- **IA hibrida**: 3 checks deterministas (`df -h`, `systemctl --failed`,
   `free -m`) + 2 con LLM (`journalctl`, `docker`). Trae **remediacion automatica**
   (`journalctl --vacuum-time=7d`, `docker system prune`, `apt clean`) con **modo dry-run**, y
   **rate limiting: 1 alerta cada 15 minutos por cada tipo de check**.
4. **investigacion-bot** -- Ollama genera **3 queries distintas** -> SearXNG -> descargas **en
   paralelo** (`tokio::join_all`) -> chunks de **1024 con 128 de solape** -> `bge-m3` -> similitud
   coseno -> **top-5** -> respuesta citando fuentes.

## 4. Cobertura previa del TEMA en el lab (medida hoy 2026-09-21 21:48:16 CEST)

`research/` tiene **431 ficheros `.md`** (432 con este). Ficheros que mencionan cada termino:
**ollama 45** · **telegram 56** · **watchdog/monitor 69** · **workflow 50** · **MCP 90** ·
**bge-m3 48** · **sqlite 30** · **rust 8** · **searxng 2** · **RSS 4** · **graphrag 4**.
Estado del lab hoy: **206 SKILL.md** · **18 RULE-*.yaml** · **301 ficheros en `tools/`** · RAG
LanceDB `joko_notes` = **44.531 filas** (el `mapa-capacidades-lab-20260824.md` declaraba
«| RAG LanceDB | **43.951 fragmentos** · 4,9 GB · recall@5 = 100% |» -> frente a las **44.531 filas** de hoy (**+580, +1,3%**): el mapa esta casi al dia. La equivalencia 'fragmentos' <-> 'filas' NO esta verificada; el delta si es coherente.

- **noticias-bot** -> el lab ya lo tiene: `rss-feeds`, `blogwatcher` y los crons de vigilancia que
  entregan informes por Telegram. **Validacion.**
- **tareas-bot** -> `telegram-inbox` (clasificar OBS/HYP/EXP/DEC con guardrails y persistencia) es el
  mismo diseno, con las mismas soluciones (JSON estricto + extractor + offset). **Validacion.**
- **monitor-bot** -> `watchdog-salud-sistema` + `detectar-sin-uso` + crons. Aqui el lab tiene una
  **norma opuesta** a proposito: prohibido ejecutar comandos o tocar servicios sin OK, asi que su
  `docker system prune` / `apt clean` automaticos **no son adoptables tal cual**. **Validacion + 1 matiz.**
- **investigacion-bot** -> `agentic-rag` + LanceDB (44.531 filas) + `deep-research-lab` +
  `investigacion-web`. El suyo es RAG **efimero por consulta**; el del lab es **persistente**.
  **Validacion.**

## 5. Aplicacion al lab

| Elemento | Veredicto |
|---|---|
| Los 4 workflows | ⚪ Validacion: los 4 ejes ya estan cubiertos (Python/cron, no Rust) |
| Remediacion automatica | 🔴 **No adoptable**: contradice la norma del lab (nada sin OK, `n8n` intocable, sin `sudo`) |
| **Rate-limit 1/15 min por check** | 🟢 **Adoptable**: no ejecuta nada, solo limita el ruido de alertas. Encaja en `watchdog-salud-sistema` |
| **Dry-run declarado** | 🟢 **Adoptable como principio**: ya es la norma del lab (diagnostico primero); util como etiqueta explicita en los informes |
| Binario Rust unico + MCP stdio | 🟡 **Futurible con senal**: aplicable a `despliegue-ia-local-clientes` |
| `llama3.2:3b` / `bge-m3` | ⚪ Ya cubierto: `bge-m3` aparece en 48 ficheros; el lab tiene modelos mejores para su GPU |
| Rust en el lab | ✅ `cargo 1.93.1` / `rustc 1.93.1` instalados; `nvim` NO instalado |

## 6. Los 2 patrones con senal de activacion

1. **Rate-limiting de alertas en el watchdog** (1 alerta / 15 min / tipo de check) -- aplicar
   **cuando** se retome el informe de salud o si el usuario se queja de ruido de alertas. Es el unico
   elemento del episodio que mejora algo del lab **sin** chocar con la norma de no-remediacion.
2. **Empaquetado «binario estatico + MCP por stdio»** -- aplicar **cuando** haya que entregar algo a
   un cliente con hardware minimo (sin Python, sin GPU, 8 GB de RAM).

## 7. Censo de repos citados por el episodio (verificado hoy, fuente: GitHub API)

| Repo | ★ | Licencia | Creado | Ultimo push | Lenguaje | Nota |
|---|---|---|---|---|---|---|
| `atareao/watchbeat` | 2 | **no detectada** | 2026-08-23 | **2026-09-19** | Rust | 128 MB; monitor de uptime -- **tema del episodio 832, NO analizado en `research/`** |
| `atareao/populatrs` | 7 | **no detectada** | 2026-02-22 | **2026-09-19** | Rust | publicador por RSS; tema del episodio 830 |
| `atareao/anacleto` | 3 | MIT | 2026-08-03 | 2026-08-23 | Rust | motor de agentes (skills/tools/MCP/permisos) -- eje Hermes |
| `atareao/crypta` | 3 | MIT | 2026-01-25 | 2026-08-29 | Rust | gestion de secretos (SOPS) |
| `atareao/graphrag` | 0 | **no detectada** | 2026-08-30 | 2026-08-30 | Rust | **ya tiene ficha propia**: `analisis-atareao-graphrag-20260921.md` |

Ninguno supera 7 estrellas: es **obra de un solo autor, reciente y poco adoptada**. Dos de ellos
(`watchbeat`, `populatrs`) **sin licencia detectable** por la API -> no son adoptables aunque el
codigo guste. `anacleto` (MIT) es el unico con licencia que podria mirarse algun dia, y esta parado
desde el 23-ago.

## 8. Incoherencias detectadas y no verificado

- Dice «sin conexion a internet» cuando el investigador usa SearXNG, web y Telegram: **contradiccion
  interna** del propio material.
- El articulo dice **`Podman 5`** y la descripcion del video dice **`Podman 6`**: incoherencia entre
  guion y demo.
- «`nomic-embed-text` solo funciona en ingles» es un matiz discutible: el modelo tiene soporte
  multilingue limitado, pero la afirmacion absoluta no se sostiene (no verificado en su fuente).
- **[NO CONTRASTADO]** las cifras de su comparativa (520 lineas vs 1.750, 3,2 GB / 4 GB de RAM,
  0,08 ficheros/s): son del autor, sin metodologia de medicion.
- **[NO VERIFICADO]** que el codigo del articulo funcione; no se ha copiado ni ejecutado nada.

## 9. Veredicto y estado del lab

**Validacion: sin entrada.** Recomendacion: **no** adoptar los workflows (ya existen en el lab) ni la
remediacion automatica (prohibida por norma). Si se quiere aprovechar algo, es el **rate-limit del
watchdog** (patron 1) y el **formato de empaquetado** (patron 2). El episodio 832 (`watchbeat`) sigue
**sin analizar** y es el que mas solapa con el watchdog del lab.

- **Nada tocado**: sin GPU, sin descargas, sin instalar, sin ejecutar. Alcance 0.
- **Este fichero** es la unica escritura (usuario, 21-sep-2026). No se toco el backlog (congelado por
  la dieta IG hasta 03/04-oct) ni el ledger de aplicabilidad (`entra`/`no_entra`): esa es **otra
  escritura** que no se autorizo.
