# Arquitectura de Joko Lab

## Objetivo

Laboratorio personal de automatización e IA, operado desde terminal.

- Hermes Agent como asistente central que orquesta todas las herramientas
- Automatización de tareas con n8n
- IA local con Ollama e IA online con DeepSeek-v4-flash
- Procesamiento de documentos (Stirling-PDF, pdf-cleaner)
- Monitorización de hardware (LM Studio monitor)
- Cliente de correo (Betterbird)
- Aprendizaje continuo sobre IA, Docker, Linux y automatización

---

## Hardware

- Equipo principal: Torre de escritorio
- CPU: Intel Core i5-9500
- RAM: 32 GB
- GPU: NVIDIA RTX A2000 12 GB VRAM
- Discos:
  - SSD principal: sistema y home
  - SSD secundario: /mnt/ssd_ia_datos (datos de n8n, backups, exports)

---

## Sistema operativo

- Ubuntu (kernel 7.0.0-27-generic)
- Usuario principal: jokoalmi

---

## Componentes principales

- Hermes Agent — agente CLI auto-mejorable (Nous Research)
- Docker + Docker Compose v2 — contenedores
- n8n — automatización low-code (zona protegida)
- Ollama — modelos de IA locales
- Betterbird — cliente de correo
- LM Studio — servidor de modelos local con API en localhost:1234
- Stirling-PDF — procesamiento de PDFs
- pdf-cleaner — limpieza de PDFs
- LM Studio Real Monitor — dashboard Flask local en localhost:5000

---

## Estructura de directorios

| Ruta | Propósito |
|---|---|
| /home/jokoalmi/hermes-lab | Proyectos, skills, documentación de Hermes |
| /home/jokoalmi/hermes-lab/skills/ | Skills instaladas de Hermes |
| /home/jokoalmi/hermes-lab/docs/ | Documentación del laboratorio |
| /home/jokoalmi/hermes-lab/docs/decisiones/ | Decisiones de arquitectura registradas |
| /home/jokoalmi/automation-stack | Stack Docker Compose principal |
| /mnt/ssd_ia_datos/n8n | Datos persistentes de n8n |
| /mnt/ssd_ia_datos/exports | Exportaciones de n8n |
| /mnt/ssd_ia_datos/backups | Backups del sistema |
| /home/jokoalmi/lmstudio_real_monitor | Proyecto monitor LM Studio (Flask) |
| ~/.hermes/ | Configuración, skills y memoria de Hermes |

---

## Docker

Todos los servicios en /home/jokoalmi/automation-stack/docker-compose.yml

Servicios:

| Servicio | Puerto | Volumen datos |
|---|---|---|
| n8n | 5678 | /mnt/ssd_ia_datos/n8n |
| Ollama | 11434 | interno |
| Stirling-PDF | 8081 | interno |
| pdf-cleaner | 8000 | interno |

Red: automation_net (red bridge personalizada definida en el compose)

## Dependencias entre servicios

| Servicio | Depende de | Llamadas a |
|----------|-----------|------------|
| n8n | — | Ollama (via API localhost:11434) |
| Ollama | — | — |
| Stirling-PDF | — | — |
| pdf-cleaner | — | — |
| Hermes Agent | DeepSeek (online) | Ollama (localhost:11434), LM Studio (localhost:1234) |
| ai-router (desde Hermes) | — | Ollama, LM Studio, DeepSeek (según árbol decisión) |

La red automation_net aísla los servicios contenerizados (n8n, Ollama, Stirling-PDF, pdf-cleaner) del resto del sistema. Hermes Agent y LM Studio corren fuera de Docker y se comunican con los contenedores via localhost.

---

## IA

### Modelos locales
- Ollama serve en localhost:11434 — modelos: qwen2.5:7b, llama3.1:8b, llama31-8b-64k
- LM Studio API en localhost:1234 — modelos: gemma-4-e4b, gemma-4-12b-qat, gemma-4-12b, glm-4.6v-flash, qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5

### Modelos online
- DeepSeek Flash (v4-flash) — proveedor online preferido

### Proveedor principal (Hermes)
- deepseek-v4-flash vía DeepSeek

### Árbol de decisión (ai-router)
```
¿Datos privados? → Ollama
├── ¿Multimodal? → LM Studio (VLM local)
│  └─ (si no cargado) → Gemini (externo)
└── ¿Razonamiento complejo? → DeepSeek
   └─ ¿Consulta simple? → Ollama llama31-8b-64k
```

---

## Flujo general (visión general)

```
Usuario
   ↓
Hermes Agent (CLI) — recibe petición, orquesta herramientas
   ↓
Docker — ejecuta servicios containerizados
   ↓
n8n — automatización de workflows (si aplica)
   ↓
Ollama / LM Studio / DeepSeek — inferencia de modelos según tarea
   ↓
Resultado devuelto al usuario
```

---

## Skills instaladas (Hermes)

| Skill | Estado | Etapa | Versión |
|---|---|---|---|
| joko-lab | Poblada | — | — |
| docker-admin | Completa | 4 — Optimizar | v0.4.0 |
| hermes-expert | Completa | 4 — Optimizar | v0.3.0 |
| n8n-admin | Completa | 3 — Actuar | v0.3.0 |
| ai-router | Poblada | 3 — Actuar | v0.4.0 |
| lab-manager | Poblada | 1 — Comprender | v0.1.0 |
| betterbird | Vacía | — | — |
| perfumes | Vacía | — | — |
| evolution | Poblada | 1 — Comprender | v0.1.0 |

---

## Documentación relacionada

- /home/jokoalmi/hermes-lab/docs/hermes-internals.md
- /home/jokoalmi/hermes-lab/docs/hermes-notes.md
- /home/jokoalmi/hermes-lab/docs/decisiones/ (8 archivos)
- /home/jokoalmi/hermes-lab/docs/roadmap.md
- /home/jokoalmi/hermes-lab/docs/joko-lab-principles.md (vacío)
- Documentación oficial: https://hermes-agent.nousresearch.com/docs/

---

## Automatización programada

| Automatización | Frecuencia | Responsable | Qué hace |
|---------------|-----------|-------------|----------|
| Healthcheck del stack | Cada hora (minuto 5) | docker-admin | Verifica contenedores activos, notifica si falla |
| Healthcheck n8n | Cada 30 min | n8n-admin | 5 tests (proceso, puerto, health, API, logs) |
| Backup n8n | Diario 3:00 | n8n-admin | Exporta workflows y datos a /mnt/ssd_ia_datos/backups |
| Backup Ollama | Diario 3:30 | docker-admin | Respaldos de modelos y datos |

Los healthchecks se ejecutan via cron del sistema. Los resultados se registran en logs y notifican al usuario si algo falla.

---

## Pendientes de arquitectura

1. docs/joko-lab-principles.md — vacío, pendiente de redactar
2. skills betterbird, perfumes — vacías, pendientes de poblar. evolution poblada (v0.1.0, etapa 1).
3. Git — pendiente comprobar si está instalado y cómo se usa en el proyecto
