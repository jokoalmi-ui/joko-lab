# joko-lab — COMMANDS

Órdenes para consultar el contexto del laboratorio.

---

## Consultar contexto del sistema

```bash
# Resumen rápido del laboratorio
cat ~/hermes-lab/skills/joko-lab/SKILL.md

# Organización completa
grep -A 20 "Organización" ~/hermes-lab/skills/joko-lab/SKILL.md

# Hardware
grep -A 5 "Contexto del laboratorio" ~/hermes-lab/skills/joko-lab/SKILL.md

# Servicios
grep -A 10 "Stack de servicios" ~/hermes-lab/skills/joko-lab/SKILL.md
```

---

## Actualizar contexto

Cuando cambie la infraestructura (nuevo servicio, cambio de hardware,
nueva skill), actualizar SKILL.md:

1. Editar las secciones correspondientes.
2. Actualizar CHANGELOG.md.

```bash
# Ver secciones de SKILL.md
grep "^#" ~/hermes-lab/skills/joko-lab/SKILL.md
```

---

## Referencias

- HERMES.md — constitución del laboratorio
- docs/arquitectura.md — descripción técnica del entorno
- docs/decisiones/ — decisiones de arquitectura
