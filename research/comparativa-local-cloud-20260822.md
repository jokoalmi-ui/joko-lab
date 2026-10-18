---
title: "Comparativa Local vs Cloud — gpt-oss-20b vs deepseek-v4-flash (batería de producción + juicio ciego)"
type: research
status: veredicto
created: 2026-08-22
---

# Comparativa Local vs Cloud — 22-ago-2026

**VERACIDAD:** [ALCANCE INTERNO]
**Objetivo:** responder con datos a "¿puede un modelo local igualar la calidad de las respuestas del cloud?" y decidir si el orquestador local-first (propuesta evaluada 10-ago) tiene sentido con el motor batch actual (gpt-oss-20b).

## Metodología

- Batería de producción existente (`lm-studio/scripts/bateria-produccion.py`): 5 tareas REALES del lab × 5 repeticiones, mismo prompt, mismo número de ejecuciones para ambos motores.
- T1 informe ejecutivo (estado real de 89 chars), T2 resumen OBS-049, T3 extracción JSON, T4 clasificación OBS/HYP/EXP/DEC, T5 razonamiento con 5 trampas.
- Evaluación: determinista en T3/T4/T5 + juicio CIEGO del usuario en T1/T2 (salidas A/B sin etiquetar).
- Condiciones: temperature 0.2 ambos. Presupuesto: local 2000; cloud probado a 2000 y a 4000 (el corte a 2000 era presupuesto, no capacidad).
- Cloud vía proxy :9911 (deepseek-v4-flash), key desde ~/.hermes/.env.
- Datos crudos: /tmp/local_gptoss_*.json, /tmp/cloud_ds_*.json (2000), /tmp/cloud_ds_4k_*.json (4000), /tmp/juicio_ciego_*.txt.

## Resultados

| Tarea | Local gpt-oss (2000) | Cloud DeepSeek (2000 → 4000) | Ganador |
|---|---|---|---|
| T3 JSON | 5/5 | 4/5 → 5/5 | Empate |
| T4 Clasificación | 5/5 | 5/5 | Empate |
| T5 Razonamiento trampas | 24/25, 0 cortes | 5/25 (4 cortes content vacío) → 25/25 | Empate técnico; local más robusto a presupuesto bajo |
| T1 Informe (ciego) | Alucina datos (2ª GPU, CPU 92%, 47 MiB) | Fiel al dato | Cloud |
| T2 Resumen (ciego) | Relleno formal, sin interpretación | Conciso + interpretación | Cloud |
| Latencia | 15-16 tok/s (9-48s/tarea) | 100+ tok/s (1.5-29s/tarea) | Cloud (5-10x) |

Juicio ciego: el usuario identificó correctamente que las variantes A (gpt-oss) "no daban los resultados esperados" en T1/T2. Revelado: A = gpt-oss local, B = DeepSeek.

## Hallazgos verificados

1. **Id del proxy :9911**: ids válidos `deepseek-v4-pro`, `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp` — SIN prefijo `deepseek/`. El `ejecutar_cloud()` del orquestador usa un id inválido (400).
2. **DeepSeek necesita >=4000 tokens** en razonamiento: a 2000 se corta (content vacío, finish=length); a 4000 resuelve 25/25 sin cortes. El router cloud con presupuestos 400/1200 cortaría.
3. **gpt-oss alucina en informes con estado corto**: inventa datos no presentes. El verifier determinista (JSON válido / contenido no vacío) NO detecta alucinación: T1-A pasaba el gate con contenido largo.
4. **La key de DeepSeek está en ~/.hermes/.env** (`DEEPSEEK_API_KEY`), NO en Bitwarden (bitwarden desactivado desde 06-jul-2026). El pitfall 8 de ai-router (11-ago) quedó obsoleto.
5. **Error recurrente de pegado del usuario con comandos largos** → patrón confirmado: scripts en /tmp (bash /tmp/x.sh) para cualquier comando multilínea o con variables.

## Veredicto

- **Batch estructurado (JSON, clasificación, razonamiento verificable): el local IGUALA al cloud** con presupuesto suficiente y sin coste. El orquestador local-first es viable para ESTAS tareas: trabajador local + verifier determinista + escalada a cloud solo en fallo.
- **Redacción abierta con datos delante (informe, resumen): el local NO iguala** — alucina y rellena. El cloud gana en fidelidad al dato e interpretación. Si se quiere local para redacción, el verifier de tareas abiertas (pendiente del diseño: LFM 2.5 revisor o rúbrica de fidelidad) es requisito, no opción.
- **Latencia interactiva: cloud siempre.** Local solo para batch donde la espera no importa.
- El cloud es el modelo principal para razonamiento complejo/conocimiento; el local para batch repetitivo — la arquitectura híbrida actual queda confirmada con datos.

## Pendientes (estado 22-ago-2026, sesión cerrada)

- [x] Corregir `ejecutar_cloud()`: id `deepseek-v4-flash` (sin prefijo) + max_tokens 4000 + key desde ~/.hermes/.env + header por partes. VALIDADO con prueba real (DeepSeek respondió "A es el mayor." en 2.28s). Micro-mejoras: la rama cloud imprime la salida; verifier rechaza JSON vacío.
- [x] Verifier de tareas abiertas: DECISIÓN — redacción abierta se queda en cloud (donde gana, juicio ciego T1/T2). El verifier de tareas abiertas (LFM 2.5 revisor o rúbrica) queda como MEJORA FUTURA condicionada a que se quiera mover redacción a local. El verifier determinista reforzado (JSON vacío rechazado) cubre el batch estructurado, que es donde opera el orquestador.
- [x] Línea base: esta batería.
- [ ] Integración del orquestador como herramienta/skill de Hermes (pendiente del diseño, fase 2).
