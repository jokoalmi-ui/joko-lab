---
title: "Informe — Test de velocidad Telegram vs CLI"
type: operations
---

# Informe — Test de velocidad Telegram vs CLI

**Fecha del test:** 2026-08-04 (adelantado desde 05-ago)
**Modelo verificado:** deepseek-v4-flash en ambos canales (config.yaml + consulta-decision.sh, política 00:00-23:59)
**Pregunta:** "Responde en una sola línea: ¿qué modelo estás usando ahora mismo y qué hora es en España?"
**Método:** cronómetro desde envío hasta respuesta completa; CLI con sesión nueva (`hermes chat -q` + time)

## Resultados

| Canal | t1 (s) | t2 (s) | t3 (s) | media |
|---|---|---|---|---|
| Telegram (móvil) | ~8 | ~8 | ~8 | ~8.0 |
| CLI (sesión nueva) | 12.4 | 13.6 | 15.5* | 13.8 |

*El intento 3 del CLI hizo 2 llamadas a herramientas (el modelo consultó estado), inflando el tiempo.

## Conclusión

- Telegram respondió ~5.8s más rápido de media (8.0 vs 13.8s) con el MISMO modelo.
- La diferencia es real en esta medición, pero la causa no es "el canal de mensajería" en abstracto:
  1. El CLI paga el arranque del proceso (interprete + carga del system prompt completo con skills/memoria) en cada invocación; el gateway de Telegram mantiene el runtime residente.
  2. El intento 3 del CLI con tool calls añadió ~2s.
  3. Matiz de contexto: la sesión CLI era nueva (contexto mínimo); la de Telegram era el hilo habitual del día (contexto LARGO), por lo que la ventaja de Telegram es incluso más notable de lo que sugiere el número crudo — con contexto comparable nuevo, la diferencia podría ser menor.

## Interpretación honesta (reglas del lab)

- No es una falacia: Telegram respondió más rápido hoy, y no fue por modelo (verificado igual).
- Es la combinación de runtime caliente del gateway + arranque frío del CLI + variabilidad de tool calls.
- Para una comparación pura de inferencia (sin arranque), la diferencia se reduciría a la latencia de red + prefill del system prompt — ambas presentes en los dos canales.
- Limitación: 3 muestras por canal, un solo momento del día, una sola pregunta sin RAG. No extrapolar a "Telegram siempre gana".

## Niveles de conclusión (revisión metodológica 04-ago)

**[HECHO]** Con 3 muestras: Telegram ≈ 8.0s, CLI ≈ 13.8s → diferencia observada ≈ 5.8s. Resultado medido.

**[INFERENCIA]** "Runtime caliente vs arranque frío" es razonable pero NO está aislada experimentalmente. Factores no separados: inicialización del proceso Python, carga del system prompt, negociación HTTP/TLS, latencia del wrapper, serialización, herramientas cargadas, logging, planificación del SO.

**[NO AFIRMABLE]** No se puede afirmar "Telegram es más rápido" — solo "en este experimento, Telegram respondió más rápido". Con 3 muestras no se caracteriza el comportamiento (media engaña; el indicador de experiencia es p95).

**Conclusión de la revisión:** la pregunta "¿hay diferencia observable?" queda respondida (sí, 5.8s). La pregunta "¿dónde está la diferencia y cómo optimizar?" requiere observabilidad del pipeline (fases t0-t6), no más repeticiones del mismo test. Ver: research/observabilidad-pipeline-diseno.md

## Estado del pendiente

- Test realizado (adelantado). El recordatorio del cronjob 6e306eb32be6 (05-ago 10:00) queda obsoleto — propuesto eliminar.
- Próximo paso opcional: repetir la medición con pregunta con RAG (contexto real) para medir el canal con carga, o con sesión Telegram nueva para aislar el contexto.
