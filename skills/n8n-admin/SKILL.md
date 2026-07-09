---
name: n8n-admin
description: Gestión, diagnóstico y mantenimiento del servicio n8n de Joko Lab.
version: 0.3.0
author: JokoAlmi
license: MIT

metadata:
  hermes:
    tags:
      - n8n
      - automatización
      - workflows
      - docker
---

# n8n-admin

Skill especializada en la gestión del servicio n8n de Joko Lab.

**Etapa actual:** 3 — Actuar (Completada)
**Siguiente:** 4 — Optimizar (parcialmente completada)

n8n es una zona protegida. Ninguna acción sobre n8n se realiza sin confirmación explícita.

Datos verificados:
- Versión: 2.27.4
- Contenedor: Up, puerto 5678
- Límites: memoria 2G máx, 512M reserva
- Workflow activo: ENVIO WHATSAPP
- JS Task Runner: ✔ registrado
- Python Task Runner: ✗ no disponible (falta Python 3)
- Conectividad con Ollama: ✔ confirmada
- Volumen de datos: 401 MB (n8n), 2.9 GB (exports), 419 MB (backup)
- Uso de recursos: CPU ~0.1%, RAM ~500 MB (24.7% del límite 2G)

Para comandos y órdenes, consultar `COMMANDS.md`.
Para riesgos y protecciones, consultar `SAFETY.md`.
