# docker-admin — Seguridad

## Reglas obligatorias

1. **n8n es zona protegida.** No parar, reiniciar, recrear ni modificar n8n sin confirmación explícita.
2. **No ejecutar comandos automáticamente.** Proponer primero diagnóstico de solo lectura.
3. **No usar `sudo` sin autorización explícita.**
4. **No limpiar Docker** (`docker system prune`, `docker volume prune`) sin explicar el riesgo y esperar confirmación.

## Comandos prohibidos sin confirmación explícita

- `docker compose stop` / `restart` / `down` / `up -d` — solo sobre un servicio concreto y con permiso
- `docker system prune` — puede borrar volúmenes, redes e imágenes no usadas
- `docker volume prune` — puede borrar datos persistentes
- `kill` / `pkill` / `kill -9` — sobre procesos Docker

## Paso seguro ante cualquier petición

1. Explicar qué servicio se va a tocar.
2. Explicar el impacto.
3. Verificar si afecta a n8n.
4. Proponer comando de solo lectura primero.
5. Esperar confirmación explícita.
