---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, coste, router, escalado]
created: 2026-09-15
---
# OBS-104: El coste no esta unido a la decision de escalado local->cloud
===============================================

## Datos basicos
  ID: OBS-104
  Fecha: 2026-09-15
  Origen: inspeccion directa de ledgers y de tools/local_cloud_orchestrator.py
          (sesion 2026-09-15, al analizar el reel DdKHNTOlCSg)

## Observacion

El router local->cloud decide si escala, pero no decide por dinero: el coste
no existe como dato junto a la decision. Evidencia literal recogida el 15-sep:

1) El ledger del router, 04-operations/metrics/local_cloud_ledger.jsonl
   (5 lineas), tiene estos campos y ninguno mas:
   ts, tarea, tipo, motor, intento_local, local_ok, escalo_cloud, motivo, latencia_s.
   No hay campo de coste ni de tokens.

2) tools/local_cloud_orchestrator.py SI calcula un coste, pero como TEXTO y
   solo para consola (l. 283):
       "coste_estimado": "0 USD (local)" if motor == "local" else "cloud flash"
   y lo imprime (l. 293, 335). El campo no se escribe al ledger: la escritura
   (l. 240) vuelca el diccionario cuyo contenido real es el de (1).

3) Los tokens SI se registran, pero por otra via y sin precio:
   04-operations/metrics/pipeline_obs.jsonl (31.633 lineas) guarda por llamada
   prompt_tokens, completion_tokens, prompt_cache_hit_tokens,
   prompt_cache_miss_tokens, ttfb_ms, total_ms (ultima linea: 2026-09-15T18:13:10,
   provider deepseek, prompt_tokens 660, completion_tokens 76).
   Falta el precio (EUR/1M tokens) para convertir eso en EUR.

4) 04-operations/metrics/respuestas_hel.jsonl tiene campo coste_tokens, pero en
   su ultima linea (2026-09-14) vale null.

Consecuencia observada: no se puede responder "cuanto costo esta tarea" ni
"que porcentaje del escalado a cloud no compenso" con los datos actuales.
El unico eje de la escalera de 6 niveles que el lab no tiene instrumentado.

## Relacionados
  - HYP-002 (coste por ejecucion y escalado local->cloud)
