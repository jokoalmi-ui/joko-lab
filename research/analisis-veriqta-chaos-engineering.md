---
title: "Análisis — Carrusel veriqta: Chaos Engineering Handbook (17-ago-2026)"
type: research
---

# Análisis — Carrusel veriqta: Chaos Engineering Handbook (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DcJXVYxjrZl/ (veriqta — misma cuenta del NGINX Production Handbook analizado ayer, serie "Engineering Notebook")
**Método:** browser_get_images → descarga 2 slides (1440×1901, webp) → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]
**⚠️ CARRUSEL PARCIAL**: 2 slides (portada + fundamentos); probablemente el handbook tiene más.

## CONTENIDO (lo que dice)

### Slide 1 — Portada: "CHAOS ENGINEERING HANDBOOK"
- Slogan: "BUILD RESILIENT SYSTEMS. EXPERIMENT WITH FAILURE. IMPROVE RELIABILITY."
- Campos de notebook: PROJECT / ENGINEER / DATE / VERSION
- Serie: "VERIQTA — ENGINEERING NOTEBOOK SERIES"
- Iconos: nube, servidores, monitor, cubo, BD, warning, Kubernetes

### Slide 2 — "CHAOS ENGINEERING FUNDAMENTALS"

**1. What Chaos Engineering is**: "the practice of running controlled experiments in production to find weaknesses before they cause outages... improve resilience." Diagrama: Nube → INJECT FAILURE (⚡) → OBSERVE & LEARN (✓)

**2. Reliability vs Resilience**:

| RELIABILITY | RESILIENCE |
|---|---|
| Prevents failure · fixes before | Withstands and recovers |
| Built systems that don't fail | Builds systems to recover fast |
| Measured by availability | Measured by recovery capability |

**3. Controlled Failure Experimentation**: hipótesis guiada · ejecutar en producción (con cuidado) · radio de explosión pequeña · observar comportamiento real · aprender y mejorar · repetir continuamente

**4. Chaos vs Ordinary Testing**:

| ORDINARY TESTING | CHAOS ENGINEERING |
|---|---|
| Preproducción · resultados predichos | Producción · fallas reales impredecibles |
| Confirma lo esperado · bugs antes del launch | Revela debilidades desconocidas · gaps después |
| Para cuando pasan los tests | Aprendizaje continuo |
| Enfocado en calidad de código | Enfocado en resiliencia del sistema |

**5. Production Engineering Mindset**: abrazar la falla · suponer que algo pasará · diseñar para ello · ser curioso ("¿qué puede ir mal?") · medir todo · aprender continuamente · cada experimento mejora el sistema · enfocarse en impacto

## 🎯 APLICACIÓN AL LAB — INTERESANTE (sí aplica, con matices)

| Concepto | Aplicación al lab | Valor |
|---|---|---|
| **"Experimentar con fallas en producción"** | El lab YA hace esto sin llamarlo así: watchdogs (detector de pérdida de contexto cada 4h, vigilancia de salud), pruebas de fallo (CUDA OOM de hoy → fix), gate fail-closed | ✅ VALIDA la cultura del lab |
| **Reliability vs Resilience** | El lab mide disponibilidad (uptime crons) pero NO recuperación explícita | 🟡 Concepto aislable |
| **Controlled experimentation** | El lab ejecuta experimentos controlados (Prueba 1 biohacking = experimento con hipótesis + medición + decisión) | ✅ El patrón del lab |
| **Chaos testing real** (inyectar fallos a propósito) | NO recomendado en el lab actual (infra local crítica: n8n, backups) | ⚠️ No hoy |
| **Formato notebook** (PROJECT/ENGINEER/DATE/VERSION + secciones numeradas) | Reutilizable para documentación TFM | ✅ Formato |

## Veredicto
**INTERESANTE / VALIDA + FORMATO.** El handbook formaliza lo que el lab ya
practica empíricamente: experimentación controlada, aprendizaje continuo,
"qué puede ir mal", watchdogs. NO recomendado inyectar caos real en la infra
local (n8n/backups críticos) — el lab ya tiene suficiente caos natural
(pitfall 13 ×12 hoy 😄). El formato notebook (portada con campos + secciones
numeradas con tablas comparativas) es aislable para TFM. Serie Engineering
Notebook de veriqta: NGINX (analizado ayer) + Chaos Engineering = 2º de la
colección; posible material si siguen saliendo.
