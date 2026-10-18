---
title: "Análisis — Joaquín Ruiz: «Descubrí que el harness importa más que el modelo» (17-oct-2026)"
type: research
---

# Análisis — «Descubrí que el harness importa más que el modelo»

**VERACIDAD:** mixta y declarada por bloques. **[VERIFICADO hoy 17-oct-2026]** los literales del código de Hermes que se citan (medidos con `grep -n` sobre `~/.hermes/hermes-agent`) y los metadatos de título/autor del vídeo (endpoint `oembed` de YouTube). **[NO RE-VERIFICADO en este pase]** las cifras del vídeo y de su README: se leyeron el 17-oct hacia las 20:00 desde la transcripción y el repositorio, y no se han vuelto a consultar; se publican con esa fecha y no se presentan como medidas de hoy.

**Fuente:** https://youtu.be/03n-YAm9eZ4 — «Descubrí que el harness importa más que el modelo», canal **Joaquín Ruiz — IA para Desarrolladores** (`@jokioki`), publicado el 16-oct-2026. Título y autor verificados hoy con `oembed`; la duración (763 s) viene de la transcripción leída el 17-oct y **no se ha re-medido**.

## Qué aporta (tres cosas y media)

1. **Contexto ≠ configuración.** La documentación de Claude Code dice literalmente que `CLAUDE.md`/`AGENTS.md` son *«context, not enforced configuration»*: se pueden ignorar. Para que una regla no se negocie hace falta un hook `PreToolUse` que salga con **exit 2**; cualquier código distinto de 0 o 2 cuenta como «non-blocking error». Es la distinción entre una regla escrita y una regla que se ejecuta.

2. **Una regla escrita reduce fallos, y lo midió.** Su repositorio describe 5 tickets × 3 condiciones, una sola toma por celda: condición A (sin configuración) rompió 1 regla y dejó 3/5 entregas sin suite verde; B (`AGENTS.md`) y C (plugin) con cero roturas. El fichero `.env` se leyó **3/3** en A (una vez filtró la contraseña de pega) y **0/3** en B y C. **Caveat que él mismo reconoce y que hay que repetir: 15 celdas, una sola toma por celda → dirección razonable, potencia estadística baja. No es una ley.**

3. **El plugin no compensa.** La condición C cuesta **+27 % de coste y +67 % de tiempo** frente a B sin mejorar el cumplimiento. La conclusión operativa: si se pone una capa determinista, va como **hook**, no como plugin.

4. **Media cosa: corrige a Hashimoto.** La definición de *harness* de Hashimoto **sí** incluye el prompting (`AGENTS.md`) como primera forma; el vídeo lo presenta como si no. Matiz conceptual, sin efecto práctico.

## Lo que NO se sostiene

- El **«27 % menos de coste A→B»** que se afirma en el vídeo **no aparece en el README** del experimento → **no verificado**, no se cita como dato.
- El experimento **no cubre el caso del Lab**: mide lectura de un `.env` y cumplimiento de una regla de estilo, no **escrituras en rutas protegidas**.

## Aplicación al Lab — la capa determinista SÍ existe (verificado en código)

Medido hoy sobre `~/.hermes/hermes-agent/agent/shell_hooks.py` (`grep -n`) y `~/.hermes/config.yaml`:

- Líneas 4-5 (docstring del módulo): el hook devuelve JSON `{"decision"|"action": "block"|"modify", ...}`, y **«Exit code 2 blocks a ``pre_tool_call`` even without JSON (Claude-Code / Cursor). Fail open unless ``fail_closed``»**.
- Líneas 43-44: `_BLOCKING_EVENTS = frozenset({"pre_tool_call"})` — es el **único** evento cuyo bloqueo se honra aguas abajo; exit 2 y `fail_closed` solo aplican ahí.
- Campos del spec (líneas 133-135): `matcher`, `timeout`, `fail_closed`. El `matcher` (regex) **solo se honra en los eventos de tool** (líneas 251-256 avisan de que en otros eventos se ignora).
- `~/.hermes/config.yaml` tiene **una sola** entrada en `hooks:`: `pre_llm_call` → `joko-context.py`, `timeout: 35`. **No hay `pre_tool_call`**: hoy el gate de rutas protegidas (`/mnt/ssd_ia_datos/n8n`, `exports`, `backups`) es **texto**.

**Consecuencia:** el gate de rutas protegidas puede volverse **determinista y nativo**, sin plugin — y por tanto sin el +27 % de coste ni el +67 % de tiempo que el vídeo mide en su condición C. SOUL.md y las RULE siguen siendo capa de texto; esto sería la capa que impide ejecutar.

## Límite honesto del instrumento

El hook recibe `tool_name` y `args`, así que puede inspeccionar el `command` de `terminal` (detectar `rm`, `mv`, `dd`, `docker compose down`…) y bloquearlo con exit 2 o con `{"action":"block"}`. **No puede saber qué va a escribir un script**: un `python3 /tmp/x.py` que escriba en `/mnt/ssd_ia_datos/n8n` pasa el filtro. Sirve como gate de comandos peligrosos reconocibles, **no como sandbox de rutas**. Venderlo como aislamiento total sería falso.

## Estado

- La pregunta **(c)** del recordatorio queda **resuelta**: sí se puede bloquear, de forma nativa.
- **No se ha escrito nada**: montar el hook exige tocar `config.yaml` (zona sensible), crear el script, aprobarlo en la allowlist y probarlo con `hermes hooks list | test | doctor`. Requiere autorización explícita aparte.
- No se aplica nada de lo que propone el vídeo: la lección útil es la distinción *contexto vs configuración*, y el Lab ya puede cubrirla con lo que trae Hermes.
