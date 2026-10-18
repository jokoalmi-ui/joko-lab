---
okf_version: "0.2"
---
# Joko Lab — índice raíz del bundle (OKF v0.2)

Bundle de conocimiento del Joko Lab. La identidad de cada documento es su ruta dentro del
bundle; `type` es la única clave de frontmatter siempre obligatoria. Este es el índice de la
raíz y, por eso, el único del árbol que declara `okf_version`.

## Punto de entrada

- `GUIA-JOKO-LAB.md` — guía general del lab (índice maestro, mantenido a mano)
- `README.md` — presentación del repositorio
- `lpa/constitucion/normas-jl.md` — normas constitucionales (JL-xxx) y su autoría

## Objetos de conocimiento

- `01-knowledge/objects/` — `RULE-*.yaml` (reglas), `DEC-*.yaml` (decisiones), `PATTERN-*.yaml`, `EXP-*.yaml`

## Capas del lab

- `01-knowledge/` — conocimiento: objetos, patrones, modelos, experimentos
- `02-infrastructure/` — infraestructura y recuperación
- `03-automation/` — automatización (n8n, workflows)
- `04-operations/` — operación: backlogs, métricas, informes, decisiones
- `05-inference/` — inferencia local: compilador de prompts, validadores
- `docs/`, `research/`, `tools/`, `verification/`, `instruments/`, `reports/`, `tests/`

## Sub-índices (reservados: sin frontmatter)

- `docs/index.md`
- `04-operations/decisions/index.md`
- `01-knowledge/patterns/index.md`
- `01-knowledge/experiments/index.md`

## Convenciones de este bundle

- Todo `.md` no reservado lleva frontmatter YAML parseable, con `type` no vacío.
- `index.md` y `log.md` son nombres reservados: no llevan frontmatter.
- Ciclos de vida en ISO 8601 UTC; la confianza se infiere de `sources` y `verified`, no de un score.
- Los objetos de `01-knowledge/objects/` son YAML, no documentos OKF: se comparan por semántica de claves.
