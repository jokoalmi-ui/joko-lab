---
type: instrument
subtype: instrument
status: index
tags: [instrument]
created: 2026-07-21
---
# Critic Loop v0.1 — Instrumento científico

## Restricción constitucional

Este script **NO modifica absolutamente nada.**

- No toca HTML.
- No propone cambios.
- No escribe CSS.
- No optimiza.
- No tiene permiso para mejorar nada.

Su única misión es **observar, medir y registrar**.

## Propósito real

Validar si los principios definidos en `design-principles.yaml` producen evaluaciones consistentes:

1. ¿El mismo modelo da scores consistentes en momentos distintos?
2. ¿Modelos distintos coinciden en sus evaluaciones?
3. ¿Qué principios son demasiado ambiguos para ser evaluables?
4. ¿Qué principios nunca producen mejoras útiles?

## Evidencia acumulada (2026-07-20 → 2026-07-21)

| Fecha | Página | Modelo | Media | Tiempo | Tag |
|---|---|---|---|---|---|
| 2026-07-20 | `perfume.html` (archivo) | glm-4.6v-flash | 7.6 | 236s | v4 |
| 2026-07-20 | `localhost:5050/perfume/1055` | glm-4.6v-flash | — | — | — |

**Hallazgo 2026-07-21:** Ambos modelos (glm, qwen) hacen timeout en frío tras cargar. La primera inferencia de un modelo de visión recién cargado requiere compilación JIT de kernels CUDA y asignación de buffers. Solución: warm-up previo automático (ver v0.2).

## Uso

```bash
cd /home/jokoalmi/joko-lab/instruments/critic-loop
python3 evaluate.py /home/jokoalmi/perfume-ia/app/templates/perfume.html
```

Con modelo específico:

```bash
python3 evaluate.py perfume.html --model google/gemma-4-12b-qat --tag v1
```

## Output

JSON en `outputs/` con:

- `evaluations[]`: score, confidence, uncertainty, evidence por principio
- `aggregates`: mean_score, low_confidence_principles, flag
- `meta`: modelo usado, timestamp, paths

## Roadmap v0.2

Dos mejoras priorizadas, descubiertas durante la sesión del 2026-07-21:

### 1. Warm-up automático

**Problema:** modelos de visión recién cargados hacen timeout en la primera evaluación (compilación JIT de kernels CUDA, buffers fríos). glm-4.6v-flash y qwen3.5-9b confirmados.

**Solución:** antes de ejecutar la evaluación completa, enviar una inferencia ligera de calentamiento:

```
"Describe esta imagen en una palabra."
```

Esperar respuesta. Solo después lanzar la evaluación de 10 principios.

### 2. Recomendaciones accionables

**Problema:** el output actual es solo diagnóstico:

```
Luxury: 5/10
```

**Objetivo:** que el output incluya propuestas:

```
Luxury: 5/10

Motivos: exceso de bloques, bordes duros, falta de aire
Cambios sugeridos: reducir weights, aumentar whitespace, simplificar estructura
Impacto esperado: +1.5 puntos
Confianza: 0.84
```

Este cambio convierte el Critic Loop de instrumento de diagnóstico a herramienta de trabajo. Con esto, Hermes puede cerrar el ciclo: Versión A → Evaluar → Proponer → Versión B → Reevaluar → Comparar.

## No confundir

Esto NO es el Design Director. Es el instrumento de medida que,
si resulta fiable, permitirá construir un Design Director después.
