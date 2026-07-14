# Configuración de la arquitectura de IA

## Configuración de Hermes (config.yaml)

El archivo `~/.hermes/config.yaml` define el proveedor principal de Hermes.

### Estructura actual recomendada

```yaml
# === PROVEEDOR PRINCIPAL ===
# Define qué modelo usa Hermes como Director
model:
  default: deepseek-v4-flash     # o gemini-3.1-flash-lite según franja
  provider: deepseek             # o gemini según franja
  base_url: https://api.deepseek.com/v1  # o https://generativelanguage.googleapis.com/v1beta

# === PROVEEDORES PERSONALIZADOS ===
# Define endpoints locales que Hermes puede usar
custom_providers:
  - name: local
    base_url: http://localhost:11434/v1

# === CADENA DE FALLBACK ===
# Se activa cuando el principal falla con error
fallback_providers:
  - provider: custom
    model: qwen2.5:7b
    base_url: http://localhost:11434/v1

# === MODO DE APROBACIÓN ===
approvals:
  mode: manual         # Obligatorio para Joko Lab

# === PERSONALIDAD ===
display:
  personality: >
    Eres el Arquitecto Técnico (Cloud) de Joko Lab. Tienes a tu cargo un
    Ingeniero de Ejecución local (Ollama) accesible mediante la herramienta
    'delegate_task'. Para tareas mecánicas, lecturas de logs o trabajo
    repetitivo, NUNCA uses las herramientas directamente: delega la tarea
    en él y evalúa su resumen. Regla estricta: Siempre propones acciones
    antes de ejecutarlas y esperas confirmación.

# === DELEGACIÓN ===
delegation:
  provider: custom:local
  model: qwen2.5:7b
  max_spawn_depth: 1
```

### Claves de configuración

| Clave | Valor | Obligatoria | Descripción |
|-------|-------|-------------|-------------|
| `model.default` | deepseek-v4-flash | Sí | Modelo activo |
| `model.provider` | deepseek / gemini | Sí | Proveedor activo |
| `model.base_url` | URL de la API | Sí | Endpoint del proveedor |
| `approvals.mode` | manual | Sí | Seguridad: requiere confirmación |
| `display.personality` | texto | No | Personalidad del agente |
| `delegation.provider` | custom:local | No | Proveedor para delegación |
| `custom_providers` | lista | No | Proveedores adicionales |
| `fallback_providers` | lista | No | Fallback automático |

### ⚠️ PITFALLS CONOCIDOS

**1. El trío completo es obligatorio**
`model.provider`, `model.default` y `model.base_url` deben cambiarse SIEMPRE juntos. Cambiar solo provider y default sin base_url produce combinaciones imposibles (Gemini llamando a DeepSeek API).

**2. `model.*` vs `models.main.*`**
Hermes lee de `model:`, NO de `models:`. La sección `models.main.*` es ignorada por Hermes.

```yaml
# ✅ Hermes LEE de aquí
model:
  default: deepseek-v4-flash
  provider: deepseek

# ❌ Hermes IGNORA esto
models:
  main:
    default: deepseek-chat
    provider: deepseek
```

**3. No editar config.yaml directamente**
El motor de Hermes bloquea herramientas de edición directa sobre `~/.hermes/config.yaml`. Usar siempre:
```bash
hermes config set model.provider "deepseek"
hermes config set model.default "deepseek-v4-flash"
hermes config set model.base_url "https://api.deepseek.com/v1"
```

**4. Los cambios no afectan a la sesión activa**
`hermes config set` modifica el archivo para nuevas sesiones. Para cambiar en caliente: `/model deepseek` dentro de la sesión.

## Variables de entorno (.env)

El laboratorio usa variables de entorno para las API keys. Se almacenan en archivos seguros:

| Variable | Propósito | Dónde se guarda |
|----------|-----------|-----------------|
| `DEEPSEEK_API_KEY` | Autenticación DeepSeek | Archivo seguro (no documentar aquí) |
| `GEMINI_API_KEY` | Autenticación Gemini | Archivo seguro (no documentar aquí) |
| `N8N_API_KEY` | Autenticación n8n | Archivo seguro (no documentar aquí) |

**Regla:** NUNCA guardar API keys en este documento ni en ningún archivo del repositorio. Son secretos del usuario.

## Cómo añadir un nuevo modelo

### Modelo cloud

1. Obtener API key del proveedor
2. Verificar el endpoint base_url del proveedor
3. Probar conectividad:
   ```bash
   curl -s -H "Authorization: Bearer $API_KEY" https://api.proveedor.com/v1/models
   ```
4. Configurar en Hermes:
   ```bash
   hermes config set model.provider "proveedor"
   hermes config set model.default "modelo-nuevo"
   hermes config set model.base_url "https://api.proveedor.com/v1"
   ```
5. Documentar en MODELS.md
6. Actualizar ROUTING.md si aplica

### Modelo local (Ollama)

1. Descargar el modelo:
   ```bash
   docker exec -it ollama ollama pull modelo:dimensión
   ```
2. Verificar que carga en GPU:
   ```bash
   docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs ollama
   nvidia-smi
   ```
3. Probar conectividad:
   ```bash
   curl http://localhost:11434/api/generate -d '{"model":"modelo:dimensión","prompt":"test"}'
   ```
4. Documentar en MODELS.md
5. Si se usa para delegación, actualizar `delegation.model` en config.yaml

### Modelo local (LM Studio)

1. Cargar el modelo en la interfaz de LM Studio
2. Activar API Server
3. Probar conectividad:
   ```bash
   curl http://localhost:1234/api/v0/models
   ```
4. Documentar en MODELS.md

## Verificación de configuración

```bash
# Verificar modelo activo
grep -A2 "^model:" ~/.hermes/config.yaml

# Verificar proveedores personalizados
grep -A2 "custom_providers:" ~/.hermes/config.yaml

# Verificar fallback
grep -A3 "fallback_providers:" ~/.hermes/config.yaml

# Verificar delegación
grep -A2 "delegation:" ~/.hermes/config.yaml

# Verificar approvals
grep "approvals.mode:" ~/.hermes/config.yaml
```
