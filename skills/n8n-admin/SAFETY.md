# n8n-admin — Seguridad

## Reglas obligatorias

1. **n8n es zona protegida.** No reiniciar, parar, recrear, actualizar ni modificar nada de n8n sin confirmación explícita.

2. **No modificar datos, credenciales, workflows ni volúmenes de n8n sin autorización.** Esto incluye:
   - Workflows activos (actualmente: ENVIO WHATSAPP)
   - Credenciales (API keys, tokens de servicios externos)
   - Archivos de configuración dentro de /home/node/.n8n
   - Exportaciones en /mnt/ssd_ia_datos/exports (2.9 GB)

3. **No tocar las rutas protegidas sin confirmación explícita:**
   - `/mnt/ssd_ia_datos/n8n` (401 MB — datos persistentes)
   - `/mnt/ssd_ia_datos/exports` (2.9 GB — archivos importados/exportados)
   - `/mnt/ssd_ia_datos/backups` (419 MB — backups existentes)

4. **No usar comandos globales de Docker** que puedan afectar a n8n:
   - `docker compose stop` (sin especificar servicio)
   - `docker compose down` (para todo el stack)
   - `docker system prune`
   - `docker volume prune`

5. **Antes de actualizar n8n**, debe hacerse backup del volumen de datos y verificar compatibilidad de los workflows existentes.

## Problemas conocidos con riesgo

| Problema | Riesgo | Acción recomendada |
|----------|--------|--------------------|
| N8N_RUNNERS_ENABLED=true (deprecated) | Bajo — no afecta funcionamiento | Eliminar variable en `docker-compose.yml` |
| Python Task Runner no disponible | Medio — workflows Python no funcionan | Configurar runner externo si se necesita |
| Sin curl en contenedor | Bajo — diagnóstico limitado | Usar docker exec con wget o instalar curl |

## Comandos prohibidos sin confirmación explícita

- `docker compose restart n8n`
- `docker compose stop n8n`
- `docker compose up -d n8n` (si está parado)
- `docker compose pull n8n` (actualización de imagen)
- Cualquier `rm`, `mv`, `chmod`, `chown` en /mnt/ssd_ia_datos/n8n/
- Cualquier modificación de archivos dentro del contenedor n8n

## Paso seguro ante cualquier petición sobre n8n

1. Explicar que n8n es zona protegida.
2. Explicar el impacto de la acción solicitada.
3. Proponer primero un comando de solo lectura.
4. Esperar confirmación explícita antes de cualquier cambio.
