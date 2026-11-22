---
title: "Análisis — «NUEVO Harness De DeepSeek - ¡Super Agent!» (Jorge Marfil) y el estado real de las versiones de Hermes"
type: research
---

# Análisis — «NUEVO Harness De DeepSeek - ¡Super Agent!» (Jorge Marfil)

**VERACIDAD:** [VERIFICADO] contra fuente primaria: metadatos del repositorio y de la CVE por API de GitHub y NVD; tabla del benchmark leída del `README.md` de `frontier-harness-eval/eval` en la rama `main`; versiones de Hermes por `releases` de la API de GitHub y `git ls-remote`. [NO VERIFICADO] todo lo que el vídeo afirma sobre intenciones de DeepSeek, hoja de ruta o cifras propias: no hay fuente primaria que lo respalde.

**Fuente analizada:** https://youtu.be/3sGqvV-wwfw — «NUEVO Harness De DeepSeek - ¡Super Agent!», canal **Jorge Marfil** (`@Jorge_Marfil`). Transcripción automática en español, 7.525 palabras, 41.207 caracteres, guardada en `~/.hermes/cache/scratch/yt_3sGqvV.txt`.
**Método:** transcripción completa + contraste de cada afirmación con repositorio, CVE y benchmark oficiales. Nada se da por bueno por aparecer en el vídeo.

## Qué afirma el vídeo

El vídeo arranca con una escena de cuatro terminales y cuatro agentes, de los cuales tres están esperando o se han ido por donde no debían, y presenta el anuncio de DeepSeek del 31 de octubre como la solución a ese cuello de botella. El objeto del anuncio es **Super Agent**: un agente que vigila un repositorio de GitHub, lee issues y pull requests y, cuando alguien del equipo con permiso se lo pide, se va a su propia sesión, hace el trabajo y vuelve con un pull request.

Describe tres piezas: un **router** que no escribe archivos y reparte el trabajo, **workers** aislados que nunca hablan con personas, y un sistema de **reglas** que solo permite actuar si la regla lo autoriza, con modo `observe` por defecto. El propio vídeo desmonta el titular: recuerda que el repositorio es un prototipo de investigación, que no es un producto oficial de DeepSeek, que no hay fork del harness sino tres plugins sobre un `cordis.patch`, y que la seguridad no está resuelta.

## Contraste con fuente primaria

`deepseek-ai/dsh-superagent-prototype` (API de GitHub, 22-nov-2026): descripción «Towards a More Autonomous Agent System», **24.183 estrellas, 3.008 forks, 0 issues abiertos, licencia MIT, creado el 31-oct-2026, último push el 03-nov-2026 y un único commit** (`8c32a9dc`, 31-oct-2026 12:05 UTC, «feat: add the dsh-superagent research prototype»). Un prototipo de un solo commit, efectivamente.

**CVE-2026-82533** (NVD, publicada 08-09-2026): CVSS **9.6 CRITICAL**. Es un *bypass* de autenticación: la API local de control del agente acepta una cabecera `Host` de loopback enviada por el cliente en lugar de validar el origen real de la conexión TCP, de modo que un proceso confinado por las herramientas alcanza la API sin exponer ningún puerto y la usa para **escapar del sandbox**. Afecta a DeepSeek Harness anterior a `0.1.2-alpha.1`. Corrección respecto al dato dado en el chat el 22-11: la puntuación es **9.6**, no 9.4; la descripción de la CVE es de *authentication bypass* con escape de sandbox, no de un fallo aislado de sandbox.

## El benchmark: v1.1 y la posición de Hermes

El vídeo comenta FrontierHarness Eval y sostiene que el repositorio no había cambiado desde el 8 de septiembre. Eso era cierto al grabarse y **dejó de serlo el 17-11**: el commit `660291ec` («Replace v1.0 content with the v1.1 evaluation») sustituye la v1.0, y el merge del PR de release entra el 20-11 a las 18:23 UTC. La v1.1 evaluúa **5 modelos, 22 configuraciones, 62 tareas y 27.280 ensayos**, con 1.240 intentos puntuados por configuración, en Baseten y con la capa Runta.

Resultados completos, ordenados por coste por acierto (leídos del README de la rama `main`):

| Harness | Coste/acierto | Tasa de acierto | Caché | Tiempo/acierto | Versión |
|---|---|---|---|---|---|
| Codex CLI | $0,937 | 61,1 % | 93,9 % | 43m 48s | 0.164.0 |
| Pi | $0,976 | 57,7 % | 94,5 % | 54m 01s | 1.4.0 |
| OpenCode v2 | $0,978 | 57,3 % | 94,3 % | 43m 43s | 2.2.7 |
| Oh My Pi | $0,983 | 57,3 % | 93,1 % | 59m 13s | 18.12.6 |
| ZCode | $1,06 | **61,9 %** | 92,0 % | 57m 08s | 0.17.0 |
| KimiCode | $1,09 | 60,2 % | 93,3 % | 56m 04s | 2.3.1 |
| OpenCode v1 | $1,12 | 57,4 % | 94,6 % | 1h 02m | 1.19.4 |
| Maka | $1,13 | 57,7 % | 91,5 % | 57m 30s | 0.2.2-dev.92.20261019 |
| MiniMax Code | $1,14 | 56,8 % | 92,3 % | 1h 00m | 0.6.13 |
| DSH Minimal | $1,15 | 57,4 % | 95,1 % | 1h 03m | 0.2.1-rc.3 |
| **Hermes Agent** | **$1,16** | **59,9 %** | 93,0 % | 58m 26s | **0.22.5** |
| Cline CLI | $1,19 | 57,7 % | 86,4 % | 1h 01m | 3.0.73 |
| Grok Build | $1,20 | 60,0 % | 92,4 % | 1h 00m | 1.0.67 |
| Alma | $1,22 | 59,7 % | 91,0 % | 57m 08s | 0.4.212 |
| DSH Creator | $1,27 | 56,1 % | 95,5 % | 1h 07m | 0.2.1-rc.3 |
| DSH Standard | $1,27 | 55,0 % | 94,6 % | 1h 05m | 0.2.1-rc.3 |
| mini-SWE-agent | $1,29 | 58,6 % | 94,7 % | 59m 32s | 2.4.6 |
| DSH Code | $1,32 | 55,2 % | 94,5 % | 1h 06m | 0.2.1-rc.3 |
| Exo | $1,36 | 50,6 % | 91,1 % | 1h 07m | 825318306c0e |
| GitHub Copilot CLI | $1,38 | 56,9 % | 88,6 % | 1h 04m | 1.0.103 |
| Claude Code | $1,55 | 58,9 % | 94,3 % | 1h 10m | 2.1.308 |
| Antigravity CLI | $1,63 | 55,0 % | **95,6 %** | 1h 06m | 1.4.6 |

Lectura del dato: Hermes Agent queda **11 de 22 por coste** y **quinto por tasa de acierto** (por detrás de ZCode 61,9 %, Codex 61,1 %, KimiCode 60,2 % y Grok Build 60,0 %). Con el mismo modelo, el reparto de coste entre harnesses va de $0,937 a $1,63: **1,74x**, no el 17,5x que se atribuye al titular del vídeo en su propio arranque. Las cuatro configuraciones del DSH (Minimal 57,4 %, Creator 56,1 %, Standard 55,0 %, Code 55,2 %) quedan **por debajo de Hermes en acierto y por encima o igual en coste salvo Minimal**, que cuesta un céntimo menos y acierta 2,5 puntos menos.

## Qué aporta al lab

**CONFIRMA** dos cosas que ya están montadas. Primera: el banco propio de `medicion-opencode` mide lo mismo que este benchmark (coste por acierto, tasa de éxito, tiempo) con control propio; el vídeo no aporta método nuevo, aporta la existencia de una referencia externa con la que contrastar. Segunda: el reparto router ligero / worker capaz ya se ejecuta en el lab con la delegación a `gpt-oss-20b`; el vídeo le pone cifras ajenas, no una mecánica distinta.

**NUEVO y aprovechable:** que **Hermes Agent ya está medido por un tercero** y sale mejor que Claude Code en acierto (59,9 % frente a 58,9 %) y en coste ($1,16 frente a $1,55). Es el primer dato externo, reproducible y citable, de que el harness que usa el lab está en la banda alta. Sirve para LinkedIn (marca empleo/IA) y para no cambiar de harness por impulso.

**Sin entrada:** Super Agent. Un commit, un repositorio, dependencia de GitHub App propia, `tmux` y mensajería corporativa, y sus propios autores lo llaman prototipo. El harness DeepSeek ya está analizado dos veces en `research/` (`analisis-nichonauta-deepseek-harness.md`, `analisis-deepseek-harness-nichonauta.md`) con veredicto bajo. Si alguna vez se prueba, la versión mínima segura es `0.1.2-alpha.1` o superior por la CVE-2026-82533.

## Estado real de las versiones de Hermes (22-nov-2026)

- **Instalada:** `v0.22.2+8170.g2bd378e` (base 2026.9.24), instalación por git en `~/.hermes/hermes-agent`, Python 3.14.9. El binario avisa «Update available — run 'hermes update'».
- **Medida por el benchmark:** `0.22.5`. El lab corre un parche por detrás de la versión que se evaluó.
- **Estables publicadas por detrás:** 0.22.3, 0.22.4, 0.22.5, 0.22.6, 0.22.7, y **0.23.0** (05-11 21:32 UTC, «The Hearth Release»), **0.23.1** (10-11 01:42 UTC), **0.23.2** (16-11 20:59 UTC) y **0.23.3** (20-11 00:34 UTC), que es la última. Entre medias hay canary diarios, no estables.
- **RULE-016:** la última estable se publicó el 20-11; los cinco días de investigación post-publicación se cumplen el **25-11-2026**. Antes de esa fecha no se actualiza salvo análisis con OK explícito.
- **Watchdog de versiones:** ya notificó `v0.23.3` (contenido de `~/.hermes/.version-watchdog-notified`), así que el aviso llegó.
- **No verificado todavía:** `_config_version` objetivo de 0.23.3 y salto de migración desde la config actual (v52), requisito de Node de la release, y si hay bugs de migración abiertos. Sin esos tres datos no hay recomendación de actualizar: sólo hay fecha de elegibilidad.

## Lo que NO se puede afirmar

No se puede afirmar que el benchmark sea neutral: lo opera Runta, que vende la capa de ejecución con la que se mide, y el coste depende del precio del proveedor y de la caché. No se puede afirmar que el resultado de `0.22.5` represente a `0.23.3`. No se puede afirmar que Super Agent vaya a ser producto: el repositorio no tiene ni un segundo commit. Y no se puede afirmar que las cifras del titular del vídeo (17,5x) salgan de la v1.1: en la tabla publicada el rango es 1,74x.

## Fuentes

- https://youtu.be/3sGqvV-wwfw — transcripción ES, 7.525 palabras.
- https://api.github.com/repos/deepseek-ai/dsh-superagent-prototype — metadatos y commits, consultado 22-11-2026.
- https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-82533 — CVSS 9.6, publicada 08-09-2026.
- https://raw.githubusercontent.com/frontier-harness-eval/eval/main/README.md — tabla v1.1, 22 configuraciones.
- https://api.github.com/repos/NousResearch/hermes-agent/releases y `git ls-remote --tags` — versiones 0.22.x/0.23.x, consultado 22-11-2026.
