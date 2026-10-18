<!-- metadatos pre-OKF (conformidad OKF v0.2, 25-sep-2026; frontmatter retirado): type: knowledge · subtype: pattern · status: index · tags: [knowledge, pattern] · created: 2026-07-28 -->
# Pattern Library — Joko Lab
===============================

Un patron es conocimiento reutilizable y transversal que describe
como resolver un tipo de problema de forma optima. A diferencia de
una ficha de modelo (especifica de un modelo) o un experimento
(especifico de una fecha), un patron aplica a multiples modelos,
herramientas o contextos.

## Estructura

```
patterns/
├── prompt-patterns/       Patrones de prompt transversales
├── workflow-patterns/     Patrones de diseno de workflows
├── docker-patterns/       Patrones de infraestructura Docker
├── recovery-patterns/     Patrones de recuperacion del sistema
├── inference-patterns/    Patrones de estrategia de inferencia
└── anti-patterns/         Lo que NO debe hacerse
```

## Ciclo de vida de un patron

  1. Se observa un comportamiento recurrente (E1)
  2. Se hipotetiza que es un patron general (E2)
  3. Se valida en modelos/contextos distintos (E3)
  4. Se formaliza como patron en esta libreria
  5. Se referencian los experimentos que lo validaron

## Relacion con otros componentes

  - Los patrones de prompt alimentan 05-inference/compiler/rules/
  - Los anti-patrones alimentan 05-inference/validators/
  - Los patrones de recuperacion alimentan 02-infrastructure/recovery/
  - Los experimentos en 01-knowledge/experiments/ validan patrones

## Como usar un patron

  Cada patron tiene:
  - Nombre y proposito
  - Entrada esperada
  - Salida esperada
  - Riesgos conocidos
  - Modelos compatibles
  - Experimentos de validacion
  - Ejemplos de uso
