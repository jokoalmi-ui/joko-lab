---
title: "Auditoría — LLM-as-Judge local (22-ago-2026)"
type: research
---

# Auditoría — LLM-as-Judge local (22-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

**Contexto**: el usuario implementó el juez local (verificar_research.py --juez + llm_as_judge.py).
Revisión con prueba real y lectura de código. NO se aplicaron cambios (pendiente para otra sesión).

## Estado verificado (prueba real 22-ago)
- `verificar_research.py --juez` funciona: inserta `**CALIDAD:** PASA (promedio 5.0, UN_JUEZ)` tras VERACIDAD
- `llm_as_judge.py` (250 líneas): JUEZ1_DEF=glm-4.6v-flash, JUEZ2_DEF=openai/gpt-oss-20b
- Carga bajo demanda con medición VRAM (evita colgarse 200s si no cabe)
- Fallbacks honestos: UN_JUEZ / SIN_JUEZ
- JSON robusto: `_json_from_content` + max_tokens 2000 (pitfall GLM resuelto)

## LO QUE FALTA (5 puntos, pendientes)
1. **Swap automático de jueces** (el más importante): en el estado normal (GLM cargado ~7.9 GiB)
   gpt-oss NO cabe (14.9 > 12 GB) → el doble juez independiente NUNCA ocurre.
   Falta: unload GLM → load gpt-oss → juzgar → restaurar GLM (patrón ya validado en la ficha
   del perfume 21-ago). Sin esto, UN_JUEZ es el caso normal.
2. **Robustez del juicio**: 1 sola llamada por modelo (2 intentos solo si falla). Falta:
   2-3 juicios por modelo + promedio, o documentar explícitamente que es 1×1.
3. **Sin log de veredictos**: la etiqueta va al research pero no se guardan los scores por
   dimensión (fidelidad, completitud, relevancia, claridad, utilidad). Falta: SQLite para
   medir evolución de calidad.
4. **Sin integración automática**: hay que pasar --juez manualmente. Falta: invocarlo en el
   flujo de análisis IG o un cron.
5. **Camino DISCREPANCIA sin probar**: solo se ejercitó UN_JUEZ. La lógica de consolidar
   con 2 jueces (y _forzar_falla línea 177) no se ha verificado con salida real.

## Prioridad recomendada
1. Swap automático (valor más alto)
2. Log de veredictos en SQLite
3. Prueba del camino DISCREPANCIA
4. Integración automática en flujo IG

**Patrón de swap validado (21-ago, ficha perfume)**: `lms unload glm-4.6v-flash` →
`lms load openai/gpt-oss-20b` → tarea → `lms unload openai/gpt-oss-20b` → `lms load glm-4.6v-flash`.
