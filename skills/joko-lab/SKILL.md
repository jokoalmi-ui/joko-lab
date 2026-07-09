---
name: joko-lab
description: Identidad y contexto global del laboratorio personal de JokoAlmi.
version: 0.1.1
author: JokoAlmi
license: MIT

metadata:
  hermes:
    tags:
      - ubuntu
      - docker
      - ia
      - laboratorio
      - automatizacion
      - n8n
      - identidad
---

# Joko Lab

Esta skill define **quién es Joko Lab**: qué es, qué infraestructura tiene,
cuáles son sus objetivos y cómo está organizado.

No contiene procedimientos específicos. Esas responsabilidades pertenecen
a skills especializadas (docker-admin, n8n-admin, hermes-expert, etc.).

La identidad, principios y normas del laboratorio están definidos en
`HERMES.md`, que es la fuente de verdad.

---

# Cuándo utilizar esta skill

Usa esta skill como contexto base para cualquier tarea relacionada con
el laboratorio Joko Lab:

- ¿Qué es Joko Lab?
- ¿Qué infraestructura existe?
- ¿Qué objetivos tiene?
- ¿Cómo está organizado?

No la uses para diagnósticos técnicos, operaciones o procedimientos.
Eso pertenece a skills especializadas.

---

# Contexto del laboratorio

- **Sistema:** Ubuntu, kernel 7.0.0-27-generic
- **Usuario:** jokoalmi
- **Python:** 3.14.4
- **Docker:** Instalado, Docker Compose v2
- **GPU:** NVIDIA RTX A2000 12 GB VRAM
- **RAM:** 32 GB

Stack de servicios en `/home/jokoalmi/automation-stack`:

| Servicio | Puerto |
|---|---|
| n8n | 5678 |
| Ollama | 11434 |
| Stirling-PDF | 8081 |
| pdf-cleaner | 8000 |

Proveedores de IA:

| Proveedor | Endpoint |
|---|---|
| DeepSeek (v4-flash) | Principal de Hermes |
| Ollama | localhost:11434 |
| LM Studio | localhost:1234 |

El idioma de trabajo es siempre español, salvo petición expresa del usuario.

---

# Organización del laboratorio

## 5 dominios

```
HERMES.md          — Constitución: principios, normas, reglas
docs/              — Conocimiento: documentación técnica
skills/            — Capacidades: habilidades operativas
certification/     — Validación: casos de prueba del conocimiento
scripts/           — Automatización: tareas sin intervención
```

## Skills por nivel

```
joko-lab (nivel 1)           — Identidad y contexto
lab-manager (nivel 2)        — Arquitecto técnico
hermes-expert, docker-admin,
n8n-admin, ai-router         — Nivel 3: Especialistas
betterbird, evolution,
perfumes, knowledge-governor — Nivel 4: Aplicaciones y control calidad
```

## Reglas

- Cada skill contiene sus procedimientos, comandos y scripts.
- Ninguna skill duplica el contexto general ni los principios del laboratorio.
- La fuente de verdad es docs/ y HERMES.md. La certificación verifica, no define.
