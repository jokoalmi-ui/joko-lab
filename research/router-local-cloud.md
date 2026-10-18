---
title: "Router Local/Cloud por tipo de tarea (09-ago-2026)"
type: research
---

# Router Local/Cloud por tipo de tarea (09-ago-2026)
**VERACIDAD:** [VERIFICADO]

## Qué es

Capa nueva sobre el AI Router existente: decide el MOTOR por TIPO DE TAREA
sin tocar config.yaml (el modelo principal de Hermes sigue siendo deepseek
cloud). Los crons/delegaciones batch usan el local; lo interactivo sigue cloud.

## Script

`~/joko-lab/tools/llm-router.sh`

| Modo | Motor | Uso |
|---|---|---|
| `batch` | R1-14B local | resumen, clasificación, extracción |
| `batch-json` | R1-14B local | JSON estricto (con fences; limpiar en consumidor) |
| `vision` | GLM 4.6V local | requiere GLM cargado |
| `check` | — | diagnóstico de qué motor tocaría cada tipo |

## Reglas de enrutamiento

- batch / resumen / clasificacion / extraccion → **LOCAL** (R1-14B)
- vision → **LOCAL** (GLM 4.6V)
- interactivo / razonamiento complejo → **CLOUD** (deepseek, config)

## Validación real (09-ago)

- R1-14B: 11.2-11.4 tok/s, calidad 90-95%, 0 coste, ~30s/tarea
- Clasificación de perfumes por temporada: ✅ correcta (Lavish→primavera,
  Afternoon Swim→verano, Alexandria II→otoño)
- JSON: ✅ con fences (```json) — consumidor debe limpiarlas
- Vision sin GLM cargado: degrada a R1 → error del API visible (no rompe)

## Pitfalls del script

1. **Id del modelo en API ≠ nombre de archivo**: el API expone
   `deepseek/deepseek-r1-distill-qwen-14b` (con prefijo), no el nombre GGUF.
2. **Endpoint de modelos**: `http://localhost:1234/api/v0/models` (NO
   `.../chat/completions/../models` — URL inexistente).
3. **R1 responde en reasoning_content**: el system prompt debe pedir
   "NO razones en voz alta, da la respuesta directa".
4. **JSON con fences**: R1 envuelve el JSON en ```json — limpiar con
   `sed 's/^```json//;s/```$//'` en el consumidor.
