# Estado real de Joko Lab

Última actualización: 2026-07-09 (Git init, principios, smoke tests)

## Hardware

| Componente | Estado | Detalle |
|---|---|---|
| CPU | ✓ | Intel Core i5-9500 |
| GPU | ✓ | NVIDIA RTX A2000 12 GB VRAM |
| RAM | ✓ | 32 GB |

## Software base

| Componente | Estado | Detalle |
|---|---|---|
| Sistema | ✓ | Ubuntu, kernel 7.0.0-27-generic |
| Python | ✓ | 3.14.4 |
| Docker | ✓ | Instalado, Docker Compose v2 |
| Git | ✓ | v2.53.0, repo iniciado (142 archivos, rama master) |
| Hermes Agent | ✓ | En ejecución, perfil default |

## Servicios del stack (`automation-stack`)

| Servicio | Puerto | Estado |
|---|---|---|
| n8n | 5678 | ✓ Up. v2.27.4, límite RAM 2G, 305 MiB en reposo. JS Runner activo. Workflow ENVIO WHATSAPP activo. Healthcheck 5/5. Cron cada 30 min. Puerto restringido a localhost (127.0.0.1). |
| Ollama | 11434 | ✓ Funcionando. Modelos: qwen2.5:7b, llama3.1:8b, llama31-8b-64k |
| Stirling-PDF | 8081 | ✓ Funcionando |
| pdf-cleaner | 8000 | ✓ Funcionando (build local) |

## Proveedores de IA

| Proveedor | Tipo | Endpoint | Estado |
|---|---|---|---|
| DeepSeek (v4-flash) | Principal (Hermes) | v4-flash | ✓ Funcionando |
| Ollama | Local | localhost:11434 | ✓ Funcionando |
| LM Studio | Local | localhost:1234 | ✓ API Server activo |

### Modelos disponibles en LM Studio

google/gemma-4-e4b, google/gemma-4-12b-qat, google/gemma-4-12b, glm-4.6v-flash, qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5

### Árbol de decisión (ai-router)

```
¿Datos privados? → Ollama
├── ¿Multimodal? → LM Studio (VLM local)
│  └─ (si no cargado) → Gemini (externo)
└── ¿Razonamiento complejo? → DeepSeek
   └─ ¿Consulta simple? → Ollama llama31-8b-64k
```

## Datos y backups

| Componente | Ruta | Estado |
|---|---|---|
| Datos n8n | /mnt/ssd_ia_datos/n8n | ✓ |
| Exports | /mnt/ssd_ia_datos/exports | ✓ |
| Backups | /mnt/ssd_ia_datos/backups | ✓ Backup n8n realizado (419 MB) |
| Backup automático | Cron diario 3:00 (n8n), 3:30 (ollama) | ✓ Instalado |

## Automatización

| Componente | Estado | Detalle |
|---|---|---|
| Healthcheck automático | ✓ | Cada hora (minuto 5), notifica si falla |
| Backup automático | ✓ | Diario 3:00 n8n, 3:30 ollama |
| Healthcheck n8n específico | ✓ | Cada 30 min, 5 tests, notifica si falla |
| Auditoría integrada | ✓ | Docker + Hermes + disco + GPU |

## Skills de Hermes — Jerarquía

Las skills se organizan en una jerarquía de 4 niveles que responde a la pregunta:
**¿Quién manda sobre quién?**

```
               ┌─────────────────────┐
               │      HERMES.md      │
               │   (Constitución)    │
               │  No es una skill.   │
               │  Todas lo respetan. │
               └─────────────────────┘

                      Nivel 1
                  Identidad

               ┌─────────────────────┐
               │      joko-lab       │
               │  Identidad y con-   │
               │  texto del lab.     │
               │  No administra.     │
               └─────────────────────┘

                      Nivel 2
                 Arquitectura

               ┌─────────────────────┐
               │    lab-manager      │
               │  Arquitecto técnico │
               │  Coordina, no       │
               │  ejecuta. Consulta  │
               │  a niveles 3 y 4.   │
               └─────────────────────┘

                      Nivel 3
               Especialistas

     ┌──────────┼──────────┬──────────────┐
     │          │          │              │
 hermes-    docker-     n8n-        ai-router
 expert     admin       admin

                      Nivel 4
                Aplicaciones

     ┌──────────┬──────────────┐
     │          │              │
 betterbird  evolution    perfumes
```

### Roles y responsabilidades

| Nivel | Skill | Rol | Qué hace |
|---|---|---|---|
| — | HERMES.md | Constitución | Define principios, normas y organización. Ninguna skill lo modifica. |
| 1 | joko-lab | Identidad | Aporta contexto global: qué es Joko Lab, su infraestructura, sus objetivos. |
| 2 | lab-manager | Arquitecto técnico | Audita, detecta incoherencias, prioriza trabajo, revisa documentación. Consulta a especialistas pero no ejecuta. |
| 3 | hermes-expert | Especialista en Hermes | Configura, instala y optimiza Hermes Agent. |
| 3 | docker-admin | Especialista en Docker | Gestiona contenedores, volúmenes, redes y healthchecks. |
| 3 | n8n-admin | Especialista en n8n | Gestiona workflows, exportaciones y estado de n8n. |
| 3 | ai-router | Especialista en IA | Decide qué modelo usar según la tarea. Gestiona Ollama y LM Studio. |
| 4 | betterbird | Especialista en Betterbird | Opera el cliente de correo. |
| 4 | evolution | Especialista en Evolution | Opera el cliente PIM. |
| 4 | perfumes | Especialista en perfumes | Gestiona la colección personal. |

### Madurez técnica (0-7)

Independientemente de la jerarquía, cada skill tiene un nivel de madurez que mide
su desarrollo técnico (ver escala completa en HERMES.md §5).

| Skill | Etapa | Madurez | Versión |
|---|---|---|---|---|
| joko-lab | — | 1 | — |
| docker-admin | 4 — Optimizar | 5 | v0.4.0 |
| hermes-expert | 4 — Optimizar | 5 | v0.3.0 |
| n8n-admin | 3 — Actuar | 3 | v0.3.0 |
| ai-router | 3 — Actuar | 3 | v0.4.0 |
| lab-manager | 3 — Razonar | 5 | v0.3.0 |
| betterbird | — | 3 | — |
| perfumes | — | 2 | — |
| evolution | 1 — Comprender | 3 | v0.1.0 |

| Skill | Scripts | Tests | Auditada | Docs | Madurez |
|---|---|---|---|---|---|---|
| docker-admin | ✅ | ❌ | ✅ | Completa | 5 |
| hermes-expert | ✅ | ❌ | ✅ | Completa | 5 |
| lab-manager | ✅ | ❌ | ❌ | Completa | 5 |
| n8n-admin | ✅ | ❌ | ❌ | Completa | 3 |
| ai-router | ✅ | ❌ | ❌ | Completa | 3 |
| betterbird | ❌ | ❌ | ❌ | Instrumentada | 3 |
| perfumes | ❌ | ❌ | ❌ | Documentada | 2 |
| evolution | ❌ | ❌ | ❌ | Instrumentada | 3 |
| joko-lab | ❌ | ❌ | ❌ | Básica | 1 |

## Documentación

| Archivo | Estado |
|---|---|
| HERMES.md | 5/11 secciones completas |
| docs/estado-real.md | ✓ Este archivo (actualizado 2026-07-07) |
| docs/arquitectura.md | ✓ Completo (156 líneas) |
| docs/hermes-internals.md | Con contenido |
| docs/hermes-notes.md | Con contenido antiguo |
| docs/joko-lab-principles.md | Vacío |
| docs/decisiones/ | 10 archivos: 6 completadas, 4 activas |

### Decisiones de arquitectura registradas

| Decisión | Archivo | Estado |
|---|---|---|
| Memoria persistente | 2026-07-05-memoria-persistente.md | Completada |
| Estructura documentación | 2026-07-05-estructura-documentacion.md | Completada |
| Registro de decisiones | 2026-07-05-registro-decisiones.md | Completada |
| docker-compose sin guion | 2026-07-05-docker-compose.md | Completada |
| Mejora continua | 2026-07-05-mejora-continua.md | Completada |
| Estructura Hermes Lab | 2026-07-06-estructura-hermes-lab.md | Completada |
| Enrutador de modelos IA | 2026-07-08-ai-router.md | Activa |
| Regla justificación mejoras | 2026-07-07-regla-justificacion-mejoras.md | Activa |

## Próximos pasos recomendados

1. ~~Verificar Git e iniciar repo~~ ✔ Hecho
2. ~~Redactar docs/joko-lab-principles.md~~ ✔ Hecho
3. ~~Crear smoke tests~~ ✔ Hecho (scripts/smoke-test.sh, 6/8 pasan)
4. Arrancar LM Studio API Server cuando se necesite
5. Poblar skill betterbird (nivel 0→1)
6. n8n-admin a nivel 5: auditoría global, CHANGELOG completo
7. ai-router a nivel 5: auditoría, CHANGELOG completo
8. lab-manager a nivel 5: auditoría formal
9. docker-admin a nivel 6: tests automatizados
10. Revisar docs/hermes-notes.md (contenido antiguo)
