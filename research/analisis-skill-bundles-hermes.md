---
title: "Análisis — Skill Bundles en Hermes (Daily Dose of Data Science, 20-ago-2026)"
type: research
---

# Análisis — Skill Bundles en Hermes (Daily Dose of Data Science, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/dailydoseofds_/p/DcQH2I-E-VB/ (19-ago)
**Método:** alt oficial IG + verificación web (docs oficiales Hermes + PR #28373)
**Veredicto:** [VERIFICADO] — feature REAL, disponible en el lab AHORA

## Qué es (verificado en docs oficiales)

`hermes bundles` agrupa varias skills bajo UN comando `/`:

```bash
hermes bundles create <nombre> --skill s1 --skill s2 --skill s3
# Luego: /<nombre> → carga TODAS las skills a la vez
```

- Almacenamiento: `~/.hermes/skill-bundles/*.yaml`
- Comandos: `list`, `show`, `create`, `delete`, `reload`
- Uso: "útil cuando una tarea concreta siempre se beneficia del mismo conjunto de skills juntas" (docs)
- PR #28373 (teknium1) — feature reciente, ya en la versión del lab

## Verificación en el lab (20-ago)

```bash
hermes bundles --help  → OK, comando existe
hermes bundles list   → "No bundles installed yet"
```

**Hermes 0.17.0 del lab YA lo soporta** — no hace falta esperar a 0.21.0.

## 🎯 Aplicación al LAB (accionable HOY)

| Bundle | Skills | Para qué |
|---|---|---|
| `/perfume-dia` | perfume-del-dia | Flujo completo del perfume del día |
| `/vigilar-ig` | instagram-monitor + instagram-carruseles-analisis | Vigilancia + análisis IG |
| `/lab-diag` | diagnostico-stack-local + watchdog-salud-sistema | Diagnóstico del stack |
| `/bolsa` | bolsa-autonoma | EXP-002 |

**Beneficio**: las tareas recurrentes cargan el set completo de skills de una vez, sin re-cargar manualmente ni gastar contexto buscando el skill.

## Nota honesta

La imagen del post no se pudo descargar (CDN de IG bloquea urllib y canvas; el b64 del fetch quedó en memoria sin persistir). El análisis se basa en el alt oficial de IG + documentación oficial real de Hermes — contenido verificado, no inventado.

## Futurible inmediato — IMPLEMENTADO (20-ago-2026, verificado con salida real)

Los 4 bundles propuestos están CREADOS y verificados (`hermes bundles list` → 4):

| Bundle | Skills | Estado |
|---|---|---|
| `/lab-diag` | diagnostico-stack-local + watchdog-salud-sistema + nvidia-linux-suspend | ✅ (creado por sesión paralela; verificado 20-ago) |
| `/perfume-dia` | perfume-del-dia | ✅ (creado por sesión paralela; verificado 20-ago) |
| `/vigilar-ig` | instagram-monitor + instagram-carruseles-analisis | ✅ (creado por sesión paralela; verificado 20-ago) |
| `/bolsa` | bolsa-autonoma | ✅ CREADO 20-ago (completaba la propuesta original) |

Directorio: `~/.hermes/skill-bundles/*.yaml`. Uso: `/<bundle>` en CLI o gateway
carga todas las skills del bundle a la vez. Nota: el lab-diag añadió
`nvidia-linux-suspend` (no estaba en la propuesta original pero es coherente
con el diagnóstico del stack).
