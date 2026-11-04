---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, bot-mode, hermes]
created: 2026-10-22
---
# OBS-221: message_agent inyectada, no registrada (Bot Mode)
===============================================

## Datos basicos
  ID: OBS-221
  Fecha: 2026-10-22
  Origen: prueba real de DM bot a bot en Hermes 0.22.2

## Observacion

`message_agent` NO esta en el catalogo de tools diferidas que devuelve `tool_search`: se INYECTA
en el turno cuando el protocolo Bot Mode esta activo. Cita literal del propio codigo
(`tools/bot_mode_dm.py:68`): `"""OpenAI-format schema for ``message_agent`` (injected, not registered)."""`.
El ejecutor vive aparte, en `agent/inline_tool_executors.py:260`. Consecuencia medida: un bot que
enumera sus herramientas con `tool_search` (38 disponibles en esta instalacion) NO la ve y responde
que no la tiene. Ese listado es un falso negativo, no una prueba de ausencia.

## Prueba en uso real (2026-10-22, 07:01 CEST)

- Gates que habilitan la tool: `is_bot_mode_managed(research-bot)=True`, sesion titulada exactamente
  `Bot Chat`, `ui_meta['hermes-bots']` en `profile.yaml`, roster de 3 profiles; seccion de protocolo
  de 1.630 chars con la frase "you have the `message_agent` tool".
- `research-bot` -> `@hermes`: `{"status": "queued", "delivery_id": "d151a18d1c19…", "to": "@hermes"}` a las 07:01:01.
- `default` recibe `Message from 🤖 research-bot (@research-bot): prueba de bot mode desde research-bot`
  a las 07:01:00 en la sesion `20261008_194647_5f0ad9` (su Bot Chat, vacio desde el 8-oct).
- `default` contesta con su propio `message_agent` a las 07:01:04: `delivery_id e757c931b6bc…`, `to: @research-bot`.
- `research-bot` recibe la respuesta a las 07:01:15. Ida y vuelta completa en **15 s**; el proceso de
  fondo `proc_d1c15cba2494` cierra con exit 0 a las 07:01:36.

## Lo que NO se puede afirmar

- Que un modelo local sepa usar la tool por iniciativa propia: aqui se le dio la instruccion literal.
- Que sirva para conversacion fluida entre dos bots locales: el turno medido del bot fue de 40 s
  (06:52:44 -> 06:53:24) con contexto 131.072, o sea ~80 s por intercambio.
- Que el reparto por `tool_search` sea un bug: es el diseno (`injected, not registered`).

## Referencias

- `~/.hermes/hermes-agent/tools/bot_mode_dm.py:68` (schema inyectado), `agent/inline_tool_executors.py:260` (ejecutor)
- `~/.hermes/hermes-agent/tools/tool_search_catalog.py` (0 apariciones: no es tool de catalogo)
- `~/joko-lab/04-operations/backlogs/pendientes.md` — MARCA: BOT-MODE-DM-20261022
