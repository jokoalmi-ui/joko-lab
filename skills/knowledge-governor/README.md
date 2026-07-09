# knowledge-governor — README

Skill de control de calidad del conocimiento documentado de Joko Lab.

---

## Instalación

No requiere instalación. Los scripts están en `scripts/`.
Dependencias: bash, grep, find, diff (todas presentes en cualquier Ubuntu).

## Uso básico

```bash
cd ~/hermes-lab/skills/knowledge-governor

# Ejecutar todas las comprobaciones
bash scripts/governor-check.sh --all

# Ejecutar una comprobación específica
bash scripts/governor-check.sh --rotos
bash scripts/governor-check.sh --duplicados
bash scripts/governor-check.sh --decisiones-pendientes
bash scripts/governor-check.sh --skills-huérfanas
bash scripts/governor-check.sh --changelogs
bash scripts/governor-check.sh --certificaciones

# Ver ayuda
bash scripts/governor-check.sh --help
```

## Salida

Los informes se generan en `/tmp/knowledge-governor/` y se muestran
también en terminal. Cada comprobación produce:

- Un resumen de hallazgos.
- Solo los problemas detectados (lo correcto no se informa).
- Severidad: ALTA / MEDIA / BAJA / INFO.

## Estado actual

**Etapa 1 — Comprender.**

La skill está definida pero aún no tiene scripts operativos.
El primer script (governor-check.sh) está en desarrollo.
