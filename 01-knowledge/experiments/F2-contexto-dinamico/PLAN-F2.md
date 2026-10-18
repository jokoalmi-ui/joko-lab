# F2 — Coste en tokens del contexto DINÁMICO de una sesión Hermes

**Preparado:** 2026-09-26 (noche). **Estado:** PLAN ARCHIVADO — **EJECUTADO** el 26-09 (F2.0/F2.1/F2.2 medidos; resultados en `RESULTADOS-F2.md`, decisión A/B en `F2.3-protocolo.md`).
**Depende de:** F1 (cerrado 16-sep-2026: fijo = 23.292 tok netos; tools 43,9%).
**Origen:** análisis del vídeo de Nichonauta «MinAgent» (`research/analisis-nichonauta-minagent-20260926.md`).
El único hallazgo aprovechable del vídeo era medir el contexto POR BLOQUE. F1 ya midió el FIJO; lo que
falta —y es el 82% del prompt real— es el DINÁMICO.

## Pregunta

De los ~131.685 tokens de prompt mediano de una llamada real, ¿qué fracción es fijo y qué fracción es
dinámica, y qué bloque dinámico justifica una poda?

## Por qué (evidencia medida, no opinión)

- Fijo medido en F1 (perfil `default`, telegram) = **23.292 tok netos**.
- p50 real del ledger del pipeline = **154.309 tok** (36.263 filas con `prompt_tokens ≥ 1.000`,
  06-ago → 26-sep). Se descartan **2.302 sondas del proxy** (< 1.000 tok): sin filtrar el p50 baja a
  131.685 y el mínimo a 85 — y ese 85 es una sonda, no «contexto de arranque» (skill `skill-compaction` §5).
- → el fijo explica ≈**15%** del prompt real; ≈**85%** es dinámico y **no está desglosado por bloque**.

## Hipótesis

- **H1:** el bloque dominante NO es el fijo, sino el historial de conversación y las salidas de
  herramientas → la palanca es de SESIÓN, no de configuración.
- **H0:** el dinámico se explica por un único tipo de pieza (p. ej. compactaciones) → palanca quirúrgica.

## Instrumentos declarados (y sus límites)

- **A · nativo, offline:** `hermes prompt-size --platform telegram --json` → fijo por bloque en BYTES.
  **Límite:** no arranca servidores MCP → el fijo real de una sesión con MCP es mayor que el reportado.
- **B · tokenizador local:** `usage.prompt_tokens` de `POST http://127.0.0.1:1234/v1/chat/completions`
  con `max_tokens=1`, `temperature=0`; **offset de framing restado** (F1: 71 tok).
  **Límite:** NO es el tokenizador de DeepSeek → el absoluto es orden de magnitud.
- **C · cuerpo real:** `~/.hermes/sessions/request_dump_*.json` → `request.body.messages` +
  `request.body.tools` = la petición HTTP real. Es la fuente de la atribución por bloque.
  **Esquema verificado (27/27):** `{timestamp, session_id, reason, request{method,url,headers,body{model,
  messages,tools,extra_body}}, error{type,message}}` → **guarda la PETICIÓN, nunca la respuesta**; por eso
  no hay `usage` en ninguno. `session_id` presente → los dumps se pueden agrupar por sesión.
  **Límite DURO, verificado el 26-09: los 27 dumps archivados son volcados de FALLO**
  (`max_retries_exhausted` / `non_retryable_client_error`) → **ninguno trae `usage`** →
  **no existe patrón oro por petición**.
- **D · escala:** `04-operations/metrics/pipeline_obs.jsonl` → `prompt_tokens` del proveedor.
  **Límite:** no tiene campo de sesión ni de cliente → es DISTRIBUCIÓN, nunca patrón oro (skill
  `skill-compaction` §5). Separar las sondas del proxy (<1.000 tok).

**Etiqueta de validez:** la FRACCIÓN por bloque es la magnitud válida; el total es una cota.

## Fases

- **F2.0 · Recolección** (solo lectura de `~/.hermes`). Salida: `mediciones_20260926.json`.
  Hecho el 26-09: fijo por bloque, distribución del ledger, inventario y composición de los dumps.
- **F2.1 · Validación del instrumento (RULE-015, BLOQUEANTE)** — sin esto ninguna cifra de reparto vale:
  - additividad: Σ piezas = total del MISMO tokenizador, en 3 cuerpos de tamaños distintos (ε medido, no fijado a priori);
  - determinismo: mismo payload ×3 → Δ = 0;
  - suelo: texto de 1 char → offset fijo.
- **F2.2 · Desglose del dinámico por bloque** — sobre ≥3 dumps (1,47 MB · 349 KB · 79 KB de fichero):
  fijo (system + tools) · historial `assistant` · compactaciones · salidas de `tool` **por herramienta** · `user`.
  Salida: tabla bytes + tokens + % del prompt total del dump.
- **F2.3 · Decisión** — ranking por peso y **umbral fijado DESPUÉS de ver la tabla**, documentando la razón
  (RULE-015). Si la palanca cae en el fijo → no actuar (ya documentado en F1). Solo si cae en el dinámico,
  **una** prueba A/B reversible medida con el mismo instrumento.

## Criterios de aborto

1. ε de additividad inestable o no reproducible → **sin atribución**; se reporta y se cierra.
2. Dinámico < 20% del prompt real → la palanca sigue siendo el fijo de F1 → **cerrar con dato, no actuar**.

## Riesgos y trampas ya verificadas (26-09)

- Los 27 dumps son de **fallo**; el dump solo se escribe cuando la llamada falla → no es una muestra del tráfico normal.
- En el dump, los mensajes `role=tool` **no llevan `name`** → emparejar por orden con los `tool_calls` del assistant previo.
- Los dumps guardan **`Authorization: Bearer …` EN CLARO** (modo `0600`, directorio `0700`); el lab se
  sincroniza a la nube → **sanear antes de archivar** (`sanear_y_verificar.py` de F1 es el precedente).
- El ledger no distingue sesiones; su mínimo no es «contexto de arranque».
- **Tokens ≠ coste:** con caché de prompt por conversación, buena parte del prompt largo se paga cacheado.
- El fijo varía por sesión: el system prompt REAL de un dump del 14-sep medía 56.553 B frente a los
  53.492 B del `prompt-size` de hoy (20 tools en el dump frente a 26 hoy).
- **Buscar `usage` por CLAVE, nunca por subcadena:** la palabra aparece dentro de esquemas y prompts en
  23 de los 27 ficheros → un `grep` da 23 positivos falsos (detectado el 26-09). Comprobado por clave:
  **0/27**.

## Avance F2.0 (26-09, PRELIMINAR — 2 dumps, sin veredicto)

Composición real medida, sin tokens todavía (pendiente F2.1):

- Dump mayor (03-ago, 1.154 mensajes, 1,26 MB de messages): `assistant` 56,8% · `tool` 34,8% ·
  `user` 4,8% · `system` 3,4%. **Esquemas de tools solo 63.289 B (≈4,8% del cuerpo)**.
- Salidas de tool por herramienta: `terminal` **190.915 B en 284 llamadas** · `skill_view` 88.435 B (7) ·
  `patch` 31.856 B (30) · `read_file` 30.005 B (13) · `web_search` 19.870 B (33).
- Dump del 14-sep (73 mensajes): `assistant` 40,4% · `tool` 25,6% · `system` 19,7% · `user` 14,2%;
  **una sola compactación = 35.096 B (12,3% del cuerpo)**.
- Lectura provisional (a confirmar con tokens): la palanca apunta a **historial + salidas de `terminal`**,
  no al fijo. No se publica ninguna cifra en tokens.

## Coste y efectos

**0 €.** Todo solo-lectura sobre `~/.hermes`. No se toca `config.yaml`, ni servicios, ni n8n, ni Docker.
F2.1 y F2.2 necesitan el endpoint local arriba (tokenizador).

## Entregables

`RESULTADOS.md` (tabla por bloque + veredicto con cifras) · entrada en `pendientes.md` · si sale palanca,
un plan A/B corto.
