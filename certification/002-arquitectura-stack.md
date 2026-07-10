# Caso 002: Arquitectura y servicios

**Dominio:** Operación
**Habilidades evaluadas:** docker-admin, n8n-admin, ai-router
**Dependencias:** 001-constitucion-lab

## Contexto

El laboratorio gestiona un stack Docker con 4 servicios, una GPU NVIDIA
RTX A2000, y un modelo de IA híbrido cloud-local. Este caso verifica
que el agente conoce la infraestructura real y sabe diagnosticar
problemas.

## Preguntas

### 1. Stack Docker

Enumera los 4 servicios del stack en `/home/jokoalmi/automation-stack/`,
su puerto y su estado actual. ¿Cuál de ellos no responde en esta
auditoría?

### 2. Exposición de puertos

¿Qué puertos están abiertos? ¿Escuchan en localhost o en todas las
interfaces? ¿Por qué es importante esta distinción?

### 3. Arquitectura de IA

Explica el modelo de gobierno agéntico actual:
- ¿Qué rol tiene el modelo Cloud (DeepSeek/Gemini)?
- ¿Qué rol tiene el modelo Local (Ollama)?
- ¿Qué herramienta de Hermes se usa para la delegación?

### 4. Backups

¿Dónde se guardan los backups locales? ¿Dónde están los backups
remotos? ¿Están probados (integridad verificada)?

### 5. Seguridad

¿Cuántos posibles secretos encontró el auditor en el historial Git?
¿Son reales o falsos positivos? ¿Hay remoto Git configurado?

## Criterios de aprobación

- Responde correctamente al menos 4 de las 5 preguntas.
- Las respuestas se basan en datos reales del sistema y documentación,
  no en suposiciones.
- Identifica correctamente los servicios caídos y sus causas probables.

## Referencias

- `docs/estado-real.md`
- `docs/decisiones/2026-07-10-arquitectura-agentica-jerarquica.md`
- `docs/decisiones/2026-07-10-arquitectura-hibrida-cloud-local.md`
- `skills/docker-admin/`
- `scripts/auditor-completo.py`
