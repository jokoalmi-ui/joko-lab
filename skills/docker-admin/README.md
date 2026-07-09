# docker-admin

Skill para gestionar el stack Docker de Joko Lab.

## ¿Qué permite?

- Diagnosticar el estado de los contenedores (n8n, ollama, stirling-pdf, pdf-cleaner)
- Leer logs de servicios concretos
- Verificar configuración del docker-compose.yml
- Comprobar uso de recursos (CPU, RAM, GPU) por contenedor

## ¿Qué NO permite?

- No modificar configuraciones sin confirmación explícita
- No reiniciar servicios sin autorización
- No tocar n8n sin protección especial

## Dependencias

- Docker y Docker Compose v2 instalados
- Stack en `/home/jokoalmi/automation-stack/docker-compose.yml`

## Documentación relacionada

- `HERMES.md` — filosofía y normas del laboratorio
- `docs/arquitectura.md` — detalles técnicos del stack
