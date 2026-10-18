# F2 — Archivo del experimento: coste del contexto DINÁMICO

**Preparado:** 2026-09-26 17:59 CEST · **Estado:** PLAN ARCHIVADO — NO EJECUTADO
**Predecesor:** `F1-contexto-fijo` (cerrado 16-sep-2026: fijo = 23.292 tok netos)
**Coste hasta ahora:** 0 € · **`~/.hermes` modificado:** no (todo solo-lectura)

## Qué añade sobre F1

F1 midió el FIJO (23.292 tok). El p50 real del ledger es **154.309 tok** (36.263 filas ≥1.000 tok, tras
descartar 2.302 sondas del proxy) → **el fijo explica ≈15%**; el **≈85%** restante es contexto dinámico y
no estaba desglosado por bloque. Eso es lo que mide F2.

## Material

- `PLAN-F2.md` — diseño: pregunta, hipótesis, instrumentos con sus límites, fases F2.0–F2.3,
  criterios de aborto y riesgos verificados.
- `mediciones_20260926.json` — evidencia cruda recogida el 26-09 (fijo por bloque, distribución del
  ledger, inventario y composición de los dumps).
- `prompt_size_telegram_20260926.json` — salida nativa de `hermes prompt-size` (solo métricas).
- `analizar_dumps.py` — instrumento C: composición por rol y por herramienta de un dump (solo lectura).
- `leer_ledger_f2.py` — instrumento D: distribución de `prompt_tokens` del ledger.

## Estado por fase

| fase | estado |
|---|---|
| F2.0 recolección | HECHO 26-09 (fijo, ledger, dumps) |
| F2.1 validación del instrumento | PENDIENTE (bloqueante) |
| F2.2 desglose del dinámico | PENDIENTE |
| F2.3 decisión | PENDIENTE |

## Qué NO está aquí, y por qué

- **Los cuerpos de los dumps no se copian**: contienen el system prompt completo, conversación y
  **`Authorization: Bearer` en claro**. Se analizan en su sitio (`~/.hermes/sessions/`), solo lectura.
- No hay cifras de tokens del dinámico porque F2.1/F2.2 no se han ejecutado: **no se publica ninguna
  estimación** (el ratio chars/token solo sirve para ±30%, skill `skill-compaction` §4).

## Resultados

- **RESULTADOS-F2.md** — F2.1/F2.2 ejecutadas 26-sep-2026: instrumento validado (offset, aditividad, framing), composición en tokens por bloque, régimen real del ledger (semanal + caché) y línea base congelada para F2.3.
- Instrumentos: `linea_base_f2.py` (régimen del ledger) · `leer_ledger_f2.py` · `analizar_dumps.py`.
- **F2.3 abierto** (26-sep 19:22): `F2.3-protocolo.md` + `ab_f2.py` + `linea_base_20260926.json`.
  Ventana de intervención **27-sep → 4-oct-2026**. Umbral derivado de la banda natural, no a priori.
