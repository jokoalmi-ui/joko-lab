---
type: EXP
subtype: experiment
status: index
tags: [knowledge, experiment]
created: 2026-07-28
---
# EXP-20260728-002: Ciclo manual — Granite 4.1 8B
====================================================

Fecha: 2026-07-28
Autor: jokoalmi
Estado: COMPLETADO
Tipo: Ciclo manual de validacion

## Objetivo

Probar el ciclo completo de inferencia de forma manual antes
de automatizarlo: seleccion de modelo, ejecucion de tests,
evaluacion de resultados, actualizacion de ficha, registro de
decision. Este ciclo es la prueba de concepto del motor antes
de construir la automatizacion (Fase 4).

## Metodologia (ciclo manual)

  1. SELECCION: Granite 4.1 8B (unsloth/granite-4.1-8b)
  2. EJECUCION: 5 tests identicos a EXP-20260726-001
  3. EVALUACION: por observacion directa de cada salida
  4. FICHA: actualizar ~/joko-lab/01-knowledge/models/granite-4.1-8b.md
  5. DECISION: registrar en 04-operations/decisions/ si aplica
  6. APRENDIZAJE: documentar que se aprendio

## Condiciones

- GPU: NVIDIA RTX A2000 12GB (755MB usados, 44°C)
- Engine: LM Studio
- Modelo: unsloth/granite-4.1-8b
- Temperature: 0.7
- max_tokens: 1024
- Compiler version: 1.0.0-manual (template: benchmark-estandar-v1)

## Resultados

| Test | Tipo | Tokens out | Resultado | Notas |
|---|---|---|---|---|
| T1 | Conocimiento SQL | 664 | ✅ | Explicacion clara, bien estructurada, usa markdown |
| T2 | Razonamiento Monty Hall | 592 | ✅ | Paso a paso, probabilidades correctas, conclusion: switch |
| T3 | JSON recetas | 235 | ⚠️ | JSON valido pero envuelto en ```json markdown |
| T4 | Codigo Python CSV | 174 | ✅ | Type hints + docstring + ejemplo. Solido. |
| T5 | Creatividad relato | 84 | ✅ | 3 oraciones exactas, coherente, "I exist." |

**Puntuacion: 4/5** (T3: JSON valido pero requiere post-procesado)

## Evaluacion detallada

### T1 (Conocimiento SQL) — ✅
Explicacion completa y bien estructurada. SQL injection, tipos,
ejemplos, peligros. Markdown con headers y listas. Comparable
a Dolphin en calidad pero mas estructurado.

### T2 (Razonamiento Monty Hall) — ✅
Razonamiento paso a paso con probabilidades iniciales y
actualizadas. Llega a la conclusion correcta (switch da 2/3).
Mejor que la mayoria de modelos de 8B en este test.

### T3 (JSON recetas) — ⚠️
El contenido es JSON valido y bien formado, pero el modelo
lo envuelve en bloques de codigo markdown (```json ... ```).
Esto rompe la instruccion "ONLY a valid JSON, no markdown".
Similar a Dolphin: sabe generar JSON pero prefiere formatearlo.
Mitigacion: post-procesado para extraer JSON del markdown.

### T4 (Codigo Python CSV) — ✅
Funcion completa con:
- Import csv y typing
- Type hints (str → List[dict])
- Docstring con Args y Returns
- Uso de csv.DictReader
- if __name__ == "__main__" con ejemplo
Sin errores. Comparable a DeepSeek R1 en calidad.

### T5 (Creatividad relato) — ✅
Exactamente 3 oraciones. Tema: consciencia en martes.
Coherente, tono adecuado, final potente ("I exist.").
Menos elaborado que Gemma 4 pero mas contenido que Dolphin.

## Perfil preliminar de Granite 4.1

- Personalidad: Tool-use nativo con formato limpio
- Puntos fuertes: codigo, razonamiento estructurado
- Debilidades: JSON con markdown envolvente
- Velocidad: respuesta en ~5-15s (mas rapido que Gemma/DeepSeek)
- Similar a: Llama 3.1 Instruct (tool-use) pero con mejor formato

## Aprendizaje del ciclo (doble beneficio)

### ¿Que hemos construido?
Un perfil preliminar de Granite 4.1 con 5 tests comparables
al benchmark estandar. Primera ficha con datos reales.

### ¿Que hemos aprendido?

1. El ciclo manual FUNCIONA y aporta valor. En 10 minutos
   tenemos un perfil de modelo que antes no existia.

2. Granite 4.1 es un modelo solido para tool-use y codigo.
   Su punto debil es el JSON con markdown (mitigable).

3. El tiempo por test (5-15s) permite ciclos rapidos.
   No necesita la gestion de tokens de los reasoning models.

4. La evaluacion manual es viable para 5 tests pero no
   escala a 50. Confirmado: la automatizacion es necesaria
   para comparativas grandes.

### Clasificacion LPA
- E1 observado: Granite 4.1 envuelve JSON en markdown
- E2 hipotesis: es un modelo entrenado para tool-use que
  formatea la salida como si fuera para consumo humano
- E3: pendiente de confirmar en mas condiciones

## Archivos asociados

- config.yaml: parametros exactos del experimento
- Este README

## Referencias

- Ficha actualizada: ~/joko-lab/01-knowledge/models/granite-4.1-8b.md
- Decisión: no tomar decision nueva (modelo apto para tool-use)
- EXP-20260726-001: comparativa original con 7 modelos
