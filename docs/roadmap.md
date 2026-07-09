# Roadmap del laboratorio Joko Lab

Última actualización: 2026-07-07.

## Visión

Roadmap general que coordina el desarrollo del laboratorio. Las skills individuales pueden tener sus propios roadmaps detallados, pero este es el plan global.

## Prioridades actuales

### Alta (urgente)

| # | Tarea | Depende de |
|---|---|---|
| 1 | Poblar skill betterbird | — |
| 2 | ~Completar docs/arquitectura.md (3 huecos)~ | **HECHO** |
| 3 | Redactar docs/joko-lab-principles.md | — |
| 4 | Comprobar Git (instalado, repo, config) | — |

### Media (esta semana)

| # | Tarea | Depende de |
|---|---|---|
| 5 | Poblar skill perfumes | — |
| 6 | ~Poblar skill evolution~ | **HECHO** |
| 7 | ai-router etapa 4: integrar en Hermes | ai-router v0.4.0 completada |
| 8 | Revisar docs/hermes-notes.md (contenido antiguo) | — |

### Baja (próximas semanas)

| # | Tarea | Depende de |
|---|---|---|
| 8 | Poblar skill evolution | skills vacías priorizadas |
| 9 | n8n-admin etapa 4: runners externos, métricas | n8n-admin v0.3.0 completada |
| 10 | Auditoría global del laboratorio | — |

## Estado de las skills del laboratorio

```
Maduras (etapa 3-4):  docker-admin, n8n-admin, ai-router, hermes-expert
En desarrollo (etapa 1): lab-manager, evolution
Vacías:                 betterbird, perfumes
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
