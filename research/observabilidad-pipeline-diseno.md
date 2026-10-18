---
title: "Diseño — Subsistema de Observabilidad del Pipeline"
type: research
---

# Diseño — Subsistema de Observabilidad del Pipeline
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Estado:** ESPECIFICACIÓN DE DISEÑO — prioridad declarada por Joseba; NO implementar sin OK explícito
**Origen:** crítica metodológica al test de velocidad Telegram vs CLI (04-ago). Prioridad: no optimizar canales; observar el pipeline.

---

## 1. Motivación

El test de velocidad (3 muestras) respondió "¿hay diferencia observable?" → sí, ~5.8s.
Pero NO responde "¿dónde está la diferencia?" ni "¿qué optimizar?". Tres muestras
detectan una señal; no caracterizan el comportamiento. El indicador que importa
para la experiencia es p95, no la media.

El siguiente paso de mayor retorno NO es repetir el test con más muestras, sino
convertir las mediciones puntuales en observabilidad del pipeline: registrar
CADA consulta con su descomposición temporal. Ese histórico alimenta KEL y el
futuro motor metacognitivo, y permite detectar regresiones y justificar cambios
de arquitectura con datos.

## 2. Distribución temporal del pipeline (t0-t6)

```
t0 usuario
 ↓
t1 prompt construido        → Construcción de contexto (RAG, skills, memoria)
 ↓
t2 petición HTTP            → Negociación TLS, envío
 ↓
t3 primer byte              → TTFB del proveedor
 ↓
t4 respuesta completa       → Inferencia (DeepSeek/otro)
 ↓
t5 postproceso              → Parseo, validación, tools
 ↓
t6 respuesta enviada        → Render/entrega (gateway o CLI)
```

## 3. Registro por consulta (OBS)

Cada consulta genera una observación con:

```yaml
OBS:
  timestamp: 2026-08-04T15:00:00
  channel: telegram            # telegram | cli
  model: deepseek-v4-flash
  prompt_tokens: 2400
  completion_tokens: 180
  context_chars: 12000
  tools: []                    # herramientas invocadas
  fases_ms:
    t0_t1_contexto: 2100
    t1_t2_http: 320
    t2_t3_ttfb: 4800           # inferencia hasta primer byte
    t3_t4_completado: 850
    t4_t5_postproceso: 210
    t5_t6_entrega: 95
  total_ms: 8375
```

## 4. Preguntas que responde tras ~500 consultas

- ¿Qué % del tiempo es RAG/contexto vs inferencia vs entrega?
- ¿Influye el tamaño de contexto (context_chars) en el TTFB?
- ¿Influye el número de herramientas en postproceso?
- ¿Cuándo aparece cola del proveedor (TTFB anómalo)?
- ¿Regresiones por cambio de versión/política?

## 5. Experimento de caracterización (para cuando se implemente)

- 30 consultas por canal
- Condiciones cruzadas: contexto nuevo / largo, sin/herramientas, RAG off/on
- Estadísticos por condición: media, mediana, desviación estándar, p95, mínimo, máximo
- El p95 (consultas más lentas) es el indicador de experiencia, no la media

## 6. Integración (sin acoplar)

- Alimenta KEL (observaciones como OBS-* reutilizables)
- Alimenta el futuro Metacognitive Engine (señales por decisión)
- NO toca el decision-ledger actual (frontera con Loop Engineering preservada)
- Dónde viviría: hermes-lab/observability/ (o equivalente) — por decidir en la sesión de implementación

## 7. Fronteras (lo que NO es)

- NO es benchmarking de modelos (eso es medir_p1 y la batería de LM Studio)
- NO es Loop Engineering (ese observa reglas; este observa tiempos)
- NO es optimización de Telegram/CLI — es la base de datos para decidir DÓNDE optimizar

## 8. Verificación del diseño

- [x] Distingue fases medibles (t0-t6)
- [x] Define OBS por consulta con campos accionables
- [x] Propone experimento con p95 (no solo media)
- [x] Alimenta KEL + metacognición sin acoplar a Loop Engineering
- [x] Prioridad declarada: observabilidad > optimización de canales
