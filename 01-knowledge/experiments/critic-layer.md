---
type: knowledge
subtype: experiment
status: active
tags: [knowledge, experiment]
created: 2026-07-28
---
# Critic Layer — Propuesta de investigación

**Estado:** HIPÓTESIS ABIERTA
**Fecha:** 2026-07-20
**Autor:** Derivado de conversación con Hermes (sesión 2026-07-20)
**Nivel de evidencia:** E0 (observación única, un solo dominio)

## Qué es

Una capa arquitectónica que envuelve la implementación de cualquier producto LPA y la somete a evaluación automatizada contra principios de diseño formales.

No mejora el código. Evalúa el resultado.

## Por qué aparece ahora

Durante el desarrollo de Perfume IA (Carril A), Hermes genera HTML que luego no puede evaluar por sí mismo. Preguntas como "¿es elegante?" o "¿hay demasiado texto?" solo pueden responderse con criterio humano o con un modelo de visión. La Critic Layer formaliza ese segundo camino.

## Componentes propuestos

| Componente | Rol | Estado |
|------------|-----|--------|
| Design Principles YAML | Especificación formal de criterios evaluables | ✅ Creado en perfume-ia/governance/ |
| Reference Explorer | Extracción de principios desde referencias externas | Idea |
| Design Director | Orquestador: captura + visión + puntuación + informe | Idea |
| UX Relationship Reviewer | Evaluación cualitativa contra leyes de experiencia | Idea |
| Telemetry | Datos de uso real para contrastar intuiciones | Idea |

## Relación con LPA

La Critic Layer no es parte de LPA core. Es una consecuencia de aplicar LPA a un producto con interfaz visual: cuando la experiencia es parte del producto, evaluar la experiencia es parte del ciclo de vida.

## Preguntas abiertas

1. ¿Es la Critic Layer específica de productos con UI, o existe un equivalente para APIs, workflows o datos?
2. ¿Debe ser un servicio independiente del producto (reutilizable) o un componente interno de cada proyecto?
3. ¿Cuándo tiene sentido invertir en construirla? ¿Qué umbral de complejidad del producto lo justifica?

## Próximo paso

Ninguno. Esta investigación no debe ejecutarse hasta que Perfume IA tenga al menos 5 pantallas en producción y telemetría básica funcionando. Hasta entonces, mantener como hipótesis documentada.

## Conexiones

- [[HYP-001]] — HYP-001: hipótesis relacionada
