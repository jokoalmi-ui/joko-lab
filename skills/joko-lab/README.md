# joko-lab — README

Skill de identidad y contexto global del laboratorio personal de JokoAlmi.

---

## ¿Qué es?

joko-lab es la skill raíz. Define qué es Joko Lab, qué infraestructura tiene,
cuáles son sus objetivos y cómo está organizado.

No contiene procedimientos. No se usa para diagnósticos ni operaciones.

## ¿Para qué sirve?

- Contexto base para cualquier tarea del laboratorio.
- Referencia rápida de hardware, software y servicios.
- Organización del ecosistema de skills.

## ¿Cómo se relaciona con HERMES.md?

HERMES.md es la constitución: principios, normas y reglas del laboratorio.

joko-lab es la skill que contiene el contexto operativo: qué máquina,
qué servicios, qué herramientas.

HERMES.md no cambia casi nunca.
joko-lab se actualiza cuando cambia la infraestructura.

## Organización actual

```
HERMES.md          — Constitución (principios, reglas)
docs/              — Conocimiento documentado
skills/            — Capacidades operativas (skills)
  joko-lab        — Identidad y contexto (nivel 1)
  lab-manager     — Arquitecto técnico (nivel 2)
  hermes-expert,
  docker-admin,
  n8n-admin,
  ai-router       — Especialistas (nivel 3)
  betterbird,
  evolution,
  perfumes,
  knowledge-governor — Aplicaciones y control calidad (nivel 4)
certification/    — Validación del conocimiento
scripts/          — Automatización
```
