---
title: "F1 — Informe de corte: coste en tokens del contexto fijo del perfil default"
type: FUTURIBLE
fecha: 2026-09-16
estado: cerrado_con_dato
---

# F1 — Corte: coste real del contexto fijo (16-sep-2026)

Origen: futurible **F1** abierto en el análisis del vídeo de Gentleman Programming
(ventana de contexto, 16-sep-2026 22:56). Pregunta literal del backlog:
*medir el coste en tokens del contexto fijo del lab (SOUL + skills + 3 MCP + toolsets)
y decidir si algún MCP pasa a carga bajo demanda*.

## Problema original

Cada request del perfil `default` paga un contexto fijo (SOUL + guía + memorias +
índice de skills + esquemas de herramientas + los 3 servidores MCP). Nunca se había
medido. Sin baseline no se puede decidir qué mover a carga bajo demanda: cualquier
"esto pesa mucho" era una estimación, y las estimaciones chars→tokens no son fiables
(rango medido 30,2% entre prosa, JSON y código).

## Método

| fase | qué | instrumento | resultado |
|---|---|---|---|
| F1.1 | validar el instrumento ANTES de confiar en él (RULE-015) | 5 pruebas sobre `usage.prompt_tokens` de LM Studio | **VALIDADO** |
| F1.2 | reconstrucción por ficheros (cota inferior) | tokenizador local sobre las piezas | 18.383 tok |
| F1.3 | distribución de referencia | `04-operations/metrics/pipeline_obs.jsonl` | 30.079 llamadas limpias |
| F1.5 | medición real del fijo | **nativo** `hermes prompt-size` + tokenizador `gpt-oss-20b` | **23.292 tok** |
| F1.4 | coste de los 3 MCP | request HTTP real persistido + `mcp_schema_cache.json` (sin arrancar servidores) | **619 tok** |

Validación del instrumento (F1.1): V1 determinismo `[551, 551, 551]` varianza 0;
V2 linealidad +520/+520 (desviación 0,00%); V3 offset de framing 71 tok (67 nativo
con texto vacío); V4 informativo y **no bloqueante** (prosa 4,21 · JSON 3,65 · código
2,94 chars/token); V5 suelo real no-sonda 1.009 tok (las sondas del proxy dan 85 tok:
falso suelo). Todo el trabajo es local, 0 €.

## Resultados

**1. El fijo del perfil `default` = 23.292 tok netos** (23.426 brutos − 67 de framing).

| pieza | tokens | % del fijo |
|---|---|---|
| System prompt | 13.069 | 56,1% |
| — índice de skills | 4.020 | 17,3% |
| — SOUL + guía + memoria + perfil (resto) | 9.049 | 38,8% |
| Esquemas de herramientas nativas (26 tools) | 10.223 | 43,9% |
| Catálogo MCP (25 tools de 3 servidores) | 619 | 2,7% |

El índice de skills es **plano**: 163 entradas, 16.450 B, 83,9 B/entrada, máximo 99 B.
Una skill de 98 KB de `SKILL.md` ocupa 97 B en el índice. Las descripciones ya están
al límite (media 57,4 chars, tope 60): **no queda grasa barata**.

**2. Los 3 MCP YA están en carga bajo demanda.** No es una acción pendiente: el
catálogo vive dentro de la **descripción de la tool `tool_search`** (por eso los
prompts cacheados en `state.db` tienen 0 apariciones de `mcp__`: el catálogo se
inyecta en runtime). Config real: `tool_search = {enabled: auto, threshold_pct: 10}`.

- Catálogo real (25 MCP + 4 nativas): 2.697 chars → 793 tok
- Catálogo base (solo las 4 nativas): 454 chars → 174 tok
- **Coste MCP = 619 tok**
- Contraste: los 25 esquemas completos costarían 6.900 chars → 1.973 tok
- **Ahorro ya aplicado: −1.354 tok (−68,6%)**

**3. El fijo sobre una sesión auténtica** (request real del 14-sep 22:33, con MCP):
92.546 chars → **22.800 tok** — casi idéntico a los 23.292 medidos hoy sin arrancar
los servidores. El catálogo deferred es barato; lo que se paga es la lista de tools.

**4. Una sola tool pesa más que 50 skills.** Reparto por toolset: `delegation` 4.432 B
≈ **1.050 tok = 26% del índice de skills completo**; `file` 1.351 · `browser` 1.090 ·
`skills` 901 · `terminal` 843 · `memory` 824 · `code_execution` 752 · `connections` 668.

**5. Escenarios de poda cuantificados** (todos bajo el techo del índice, 4.020 tok):
A) quitar descripciones de categoría ≈ 570 tok (−2,4%) · B) colapsar el índice a
`[names only]` ≈ 2.300 tok (−10%, solo bajo `posture: focus` y a costa de
descubribilidad) · C) 40 skills muertas ≈ 840 tok (−3,6%) · D) `tts` + `browser-use`
≈ 1.342 tok (−5,8%, a costa de capacidades reales).

**6. Contraste con el ledger**: 30.079 llamadas limpias; p10 54.532 · mediana 192.799 ·
máximo 557.409 tok. El fijo es ≈ **9,5% de la mediana** y ≈ 34% del p10
(tokenizadores distintos → orden de magnitud, no igualdad). Coste unitario del fijo:
18.383 × 0,15 USD/1M = **0,00276 USD/request** contado como *miss* (EXP-007: sin
desglose de caché, nunca 0).

## Defectos del instrumento y correcciones propias

1. **Falso positivo SQL**: `like '%mcp__%'` devolvió 440 filas espurias porque `_` es
   comodín en SQL. Con búsqueda literal: **0 filas**. De ahí salió el hilo que localizó
   el catálogo en `tool_search`.
2. **La reconstrucción por ficheros sobrecuenta**: 205 `SKILL.md` en disco vs las
   **163 reales** del snapshot de runtime. La cifra nativa es la autoritativa.
3. `sessions.system_prompt` está a **NULL** en las sesiones posteriores al 02-sep: el
   prompt de la sesión viva no está persistido → no sirve como patrón oro.
4. El ledger **no identifica sesión ni cliente** → es distribución, no patrón oro.
5. `lms load --estimate-only` no es fiable (siempre 11,28 GiB).
6. V4 de mi propio validador imponía un umbral a priori (`dif <= 0.10`): violaba
   RULE-015 y el baseline lo desmintió (rango real 30,2%). Queda como informativo.
7. Bug propio en el check V5 (`min(tuplas)` comparaba por timestamp → 25.625 en vez
   de 1.009). Corregido con `key=lambda x: x[1]`.

## Coste

- Medición: **0 €**. Todo local (LM Studio `:1234` con `gpt-oss-20b` IDLE, tokenizador
  local, `hermes prompt-size` offline). Cero llamadas a DeepSeek.
- Ningún servidor MCP arrancado para medir (se usó el request real persistido).
- Nada escrito en `~/.hermes` ni en el lab durante la medición.

## Decisión

1. **F1 queda CERRADO con dato**: el fijo es 23.292 tok. No hay acción urgente.
2. **Los 3 MCP no se tocan**: ya están en carga bajo demanda (619 tok, −68,6% respecto
   a esquemas completos). Un modo `summary` ahorraría ~500 tok más (−2%): no compensa
   la pérdida de información.
3. **El índice de skills NO es la palanca** (inversión de la hipótesis inicial): techo
   ≈ −10% y a costa de descubribilidad; `delegation` sola pesa más que 50 skills.
4. **La palanca real son las tools nativas** (10.223 tok, 43,9%). Siguiente paso
   racional: instrumentar el **uso real** de tools y decidir con ese dato qué toolset
   se difiere (futurible **F1-bis**), no podar por intuición.
5. **No se aplica ninguna poda** en esta sesión.

## Futurible abierto por este corte

- **F1-bis**: medir el uso real por tool/toolset (delegation, browser, tts, file...) en
  las sesiones del lab y decidir con dato la promoción de toolsets a carga bajo demanda.
  Criterio de corte: un toolset que se use en <X% de sesiones y pese >500 tok.

## Registro

- Material completo (efímero, en `/tmp/f1-contexto/`, 6 scripts / 1.022 líneas):
  `PLAN-F1.md` (7.575 B, md5 `0a91de4a8669891d3962d690a5456827`),
  `RESULTADOS.md` (3.528 B, md5 `269fa8ef70cecdc7b6acddc5cdfc3108`),
  `mediciones.json` (1.504 B, md5 `d1995b3afbf057a2186a4e4823f615c3`),
  `mcp_real.json` (1.383 B, md5 `1c2c3caf7c969a5f982f30078f967e4d`),
  `fijo_real.json` (1.287 B, md5 `11ecb1edd9e63189b902053d3c3c9a30`),
  `fijo/system_prompt.txt` (53.489 B, md5 `7c8dd4ab4623e1d37c933d8166f6a7fb`),
  `fijo/tools.json` (43.398 B, md5 `0c6b57cb59d1ad66f8cf0b2ee8850b5e`),
  `fijo/catalogo_real.txt` (2.729 B, md5 `1d50beb625368a5a052ddac7f76b5466`),
  `fijo/mcp_completos.json` (6.951 B, md5 `295b70626ad1b5202351eb1aa59d19f2`).
- Fuentes medidas (solo lectura): `~/.hermes/SOUL.md` (20.235 chars) ·
  `~/.hermes/config.yaml` (14.439 chars) · memorias (4.342 chars) ·
  `~/.hermes/.skills_prompt_snapshot.json` (165 skills) ·
  `~/.hermes/cache/mcp_schema_cache.json` (25 tools MCP, 8.653 B) ·
  `~/.hermes/sessions/request_dump_20260914_172635_d00cc0_20260914_223309_841438.json`
  (body 343.682 B).
- Escrito: este informe (2026-09-16 23:24 CEST). Entrada de cierre añadida al backlog
  activo `04-operations/backlogs/2026-07-31-backlog.md`: 686.505 B (md5
  `45c4748d140b95d685a7b05a037e43b0`) -> 691.926 B (md5 `dcd87777ea9afef85b118f75e2436d01`),
  backup `.bak-20260916-f1-cierre`, 1 línea reescrita a propósito (futuribles F1) y 0
  líneas de contenido perdidas.
- **Archivado (2026-09-16 23:28, a petición del usuario)**: material copiado a
  `01-knowledge/experiments/F1-contexto-fijo/` — 23 ficheros, 476 KB, con `README.md`
  propio (índice, resultado, cómo reproducir, qué se excluyó). Verificación por hash:
  **20/20 ficheros copiados con md5 origen == destino, 0 desajustes**
  (`sanear_y_verificar.py`, 23:27:48 CEST).
- **Excluidos/reducidos en el archivo por datos personales** (el lab se sincroniza a
  la nube): `fijo/system_prompt.txt` (53.489 B, md5 `7c8dd4ab4623e1d37c933d8166f6a7fb`) y
  `fijo/session_prompt.txt` (51.411 B, md5 `4c49e2d3c2444440a00624bd3e52c14f`), volcados
  del system prompt con `MEMORY.md` y `USER.md` literales; y `piezas.json` (196.077 B,
  md5 `17b17a1eb5e1f857525557833ca81cbf`), del que se archivó copia con `B2_memoria` y
  `B2_user` redactadas (`_meta.archivado` declara qué se quitó). Regenerables con
  `hermes prompt-size --json` y `python3 recolectar.py` (instrucciones en el README del archivo).
