# Roadmap del laboratorio Joko Lab

Última actualización: 2026-07-14.

## Visión

Roadmap general que coordina el desarrollo del laboratorio. Las skills individuales pueden tener sus propios roadmaps detallados, pero este es el plan global.

## Estado actual del laboratorio (julio 2026)

El laboratorio ha completado la migración desde un diseño basado en scripts que
reescribían `config.yaml` hacia un **Decision Engine** con estado y políticas.
El Sprint 3 (en curso) consolida esta arquitectura en un **Runtime Agéntico**.

Arquitectura actual simplificada:

```
cron → apply-decision.sh → Decision Engine → state.json → provider activo
```

Arquitectura objetivo (Sprint 3):

```
Runtime
├── State Manager
├── Policy Engine
├── Capability Registry
└── Decision Engine
→ consultado bajo demanda, sin cron decisor
```

## Sprint 3 — Consolidación del Runtime (en curso)

Inicio: 2026-07-14. Prioridad máxima.

**Objetivo:** Transformar el laboratorio de un conjunto de automatizaciones a
un Runtime Agéntico estable, desacoplado y gobernado por contratos.

**Restricciones del Sprint:**
- No añadir nuevos modelos, skills, prompts, cron, ni capas.
- Contract-first: contrato → tests → implementación.
- Una única fuente de verdad (state.json).

**Entregables:**
1. `runtime/CONTRACT.md` — Constitución del Runtime
2. Runtime API (contrato)
3. Eliminación del provider global
4. Eliminación del cron decisor
5. Limpieza del Decision Engine
6. Tests obligatorios (unitarios e integración)
7. Logging estructurado

Detalle completo en `docs/decisiones/2026-07-14-sprint-3-consolidacion-runtime.md`

## Prioridades actuales

### Sprint 3 (consolidación, julio 2026)

| # | Tarea | Depende de |
|---|-------|------------|
| 1 | Definir contrato del Runtime (`runtime/CONTRACT.md`) | — |
| 2 | Implementar State Manager unificado | Contrato |
| 3 | Implementar Policy Engine | Contrato |
| 4 | Implementar Capability Registry | Contrato |
| 5 | Limpiar Decision Engine (eliminar duplicados, logs) | — |
| 6 | Eliminar provider global (dejar de depender de config.yaml) | State Manager |
| 7 | Eliminar cron decisor | Runtime API |
| 8 | Tests unitarios | Cada módulo |
| 9 | Tests de integración (10 casos) | Todos los módulos |

### Media (post-Sprint 3)

| # | Tarea | Depende de |
|---|-------|------------|
| 1 | Verifier / Evaluator | Runtime consolidado |
| 2 | Director Estratégico (Fase 2) | Runtime consolidado |
| 3 | Poblar skill betterbird | — |
| 4 | Auditoría global del laboratorio | Runtime consolidado |

### Baja (próximas semanas)

| # | Tarea | Depende de |
|---|-------|------------|
| 1 | Poblar skill perfumes | — |
| 2 | Poblar skill evolution | — |

## Estado de las skills del laboratorio

```
Maduras (etapa 3-4):     docker-admin, n8n-admin, ai-router, hermes-expert
En desarrollo (etapa 2): lab-manager
Vacías:                   betterbird, perfumes, evolution
```

## Dependencias entre skills

```
Ninguna skill depende de betterbird, perfumes o evolution.
ai-router, n8n-admin, docker-admin pueden evolucionar independientemente.
lab-manager necesita que las skills estén pobladas para monitorizarlas.
```

## Criterios para avanzar de etapa

1. Una skill pasa a etapa 2 cuando tiene scripts de diagnóstico funcionales.
2. Una skill pasa a etapa 3 cuando tiene scripts de acción (con confirmación).
3. Una skill pasa a etapa 4 cuando está auditada y optimizada.
4. lab-manager pasa a etapa 2 cuando detecta automáticamente incoherencias.
