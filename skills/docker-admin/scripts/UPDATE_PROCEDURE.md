# docker-admin — Procedimiento de actualización segura

> Cómo actualizar un servicio del stack Docker sin riesgo de pérdida de datos.

## Principio

Siempre: **backup → pull → up → verificar**

Nunca actualizar sin verificar que el servicio responde después.

## Paso a paso

### 1. Identificar qué servicio actualizar

Servicios con imágenes externas (actualizables con `pull`):

| Servicio | Imagen | Se puede actualizar |
|---|---|---|
| n8n | docker.n8n.io/n8nio/n8n:latest | Sí |
| ollama | ollama/ollama:latest | Sí |
| stirling-pdf | frooodle/s-pdf:latest | Sí |
| pdf-cleaner | pdf-cleaner:latest (build local) | No (se rebuildtea) |

### 2. Hacer backup del volumen (si aplica)

Si el servicio tiene datos persistentes (n8n, ollama), ejecutar backup antes:

```bash
bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh <servicio>
```

### 3. Descargar nueva imagen

```bash
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml pull <servicio>
```

Esto descarga la nueva versión **sin parar el servicio actual**.

### 4. Recrear el contenedor

```bash
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d <servicio>
```

Docker Compose detecta que la imagen ha cambiado y recrea el contenedor automáticamente.

### 5. Verificar que responde

```bash
bash ~/hermes-lab/skills/docker-admin/scripts/healthcheck.sh
```

El servicio debe aparecer como `Up` y el healthcheck HTTP debe devolver 200.

### 6. Verificar logs por si hay errores

```bash
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=30 <servicio>
```

## Caso especial: pdf-cleaner (build local)

No usa `pull`. Se rebuildtea con:

```bash
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d --build pdf-cleaner
```

## Caso especial: n8n (zona protegida)

n8n no se actualiza sin confirmación explícita. Antes de cualquier actualización:

1. Hacer backup completo: `bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh n8n`
2. Esperar confirmación del usuario
3. Proceder con pull + up -d

## Rollback (volver atrás)

Si la nueva versión falla:

1. Parar el servicio: `docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml stop <servicio>`
2. Restaurar backup si hay datos: `bash ~/hermes-lab/skills/docker-admin/scripts/restore-volumen.sh <servicio> <fecha>`
3. Forzar uso de la imagen anterior: `docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d <servicio>`
   (si la imagen anterior aún está en caché, se usará automáticamente)
