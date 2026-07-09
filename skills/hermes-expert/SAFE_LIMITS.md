# Límites seguros para modificar ~/.hermes/config.yaml

## Regla de oro

Nunca editar config.yaml directamente sin hacer backup primero.

```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup
```

## Secciones seguras de modificar

| Sección | Qué se puede cambiar | Riesgo |
|---|---|---|
| `model.default` | Cambiar modelo por defecto | Bajo. Hermes usará el nuevo modelo en la siguiente sesión |
| `model.provider` | Cambiar proveedor (deepseek, openrouter, etc.) | Bajo si el proveedor tiene API key configurada |
| `model.context` | Límite de contexto | Medio. Si pones demasiado, gastas más tokens |
| `model.max_output` | Límite de tokens de salida | Bajo |
| `model.temperature`, `model.top_p` | Parámetros de generación | Bajo |
| `model.streaming` | Activar/desactivar streaming | Bajo |
| `display.*` | Configuración visual TUI/CLI | Bajo |
| `fallback_providers` | Añadir/eliminar fallbacks | Bajo |
| `computer_use.*` | Configuración de uso de PC | Medio. Cambiar backend afecta cómo Hermes controla el ratón/teclado |
| `tool_approval_timeout` | Timeout de aprobación de herramientas | Bajo |

## Secciones que requieren cuidado

| Sección | Riesgo | Motivo |
|---|---|---|
| `agent.prompt`, `agent.platforms` | Alto | Cambiar el prompt del sistema altera cómo se comporta Hermes |
| `agent.describe_output`, `agent.describe_tool_results` | Medio | Afecta cuánto contexto consume cada paso |
| `memory.*` | Medio | Cambiar el proveedor de memoria externa puede perder datos |
| `terminal.*` | Medio | Timeouts e imágenes afectan cómo se ejecutan comandos |
| `computer_use.cua_driver` | Medio | Cambiar de CUA a otro backend requiere software adicional |
| `updates.pre_update_backup` | Bajo | Desactivar backups antes de actualizar puede perder cambios locales |
| `credential_pool_strategies` | Alto | Autenticación de proveedores |
| `secrets.*` | Alto | Gestores de contraseñas externos |

## Secciones prohibidas sin entenderlas

| Sección | Motivo |
|---|---|
| `lsp.*` | Configuración del servidor de lenguaje. Afecta a todo el asistente |
| `onboarding.*` | Marcar como no visto puede reiniciar el asistente de inicio |
| `plugins.spotify.auth` | Credenciales de Spotify |
| `gateway.*` | Configuración del gateway de mensajería |
| `hooks.*` | Hooks de shell que se ejecutan automáticamente |
| Cualquier `*_api_key` inline | Las claves van en `.env`, no en config.yaml |

## Procedimiento seguro para editar

### 1. Backup
```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup
```

### 2. Editar con comando oficial
```bash
hermes config edit
```
Esto abre el archivo en tu editor. Es la forma recomendada.

### 3. O bien editar directamente
```bash
nano ~/.hermes/config.yaml
```

### 4. Verificar que la sintaxis es válida
```bash
python3 -c "import yaml; yaml.safe_load(open('~/.hermes/config.yaml'))"
```

### 5. Probar que Hermes sigue funcionando
```bash
hermes doctor
```

## Recuperación

Si algo sale mal:

```bash
# Restaurar backup
cp ~/.hermes/config.yaml.backup ~/.hermes/config.yaml

# O restaurar configuración por defecto
hermes setup
```

## Notas importantes

- Hermes recarga config.yaml al iniciar cada sesión. No necesita reinicio.
- Los cambios en `.env` también se recargan en cada sesión.
- Si usas `hermes config set clave valor`, Hermes valida el cambio antes de aplicarlo.
- Siempre preferir `hermes config set` antes que editar manualmente.
