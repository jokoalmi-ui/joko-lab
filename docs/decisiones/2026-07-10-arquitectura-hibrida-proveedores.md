# Decisión: Arquitectura Híbrida de Proveedores para Joko Lab

## Estado
**OBSOLETA (14 de julio de 2026)** — DeepSeek V4 Flash es 13x mas barato que Gemini 2.5 Flash. El router horario queda desactivado. Ver `docs/decisiones/2026-07-09-router-horario-cron.md` para la correccion completa.

## Contexto

Joko Lab necesita un sistema de enrutamiento de proveedores de IA que permita
alternar entre DeepSeek (online, con coste) y Ollama (local, gratuito) según
la hora del día, sin tener que editar configuraciones manualmente en cada sesión.

El sistema actual (router-cron.sh, provider-detect.sh, model-router.sh) tenía
dos problemas:
1. El cron no modificaba config.yaml, solo escribía un archivo txt que nadie leía
2. Cuando sí modificaba config.yaml, olvidaba el base_url, dejando combinaciones
   imposibles (Gemini llamando a DeepSeek y viceversa)

## Investigación previa

Se consultó la documentación oficial de Hermes Agent:
- https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
- https://hermes-agent.nousresearch.com/docs/integrations/ai-providers

Hallazgos clave de la documentación oficial:

1. **custom_providers:** — permite definir múltiples endpoints personalizados
   (Ollama, LM Studio, etc.) que conviven en config.yaml.

2. **fallback_providers:** — sistema de resiliencia oficial con tres capas:
   credential pools (misma API key rotada), primary model fallback (otro proveedor
   cuando el principal falla), auxiliary task fallback (visión, compresión).

3. **/model** — comando interno de Hermes para cambiar de proveedor en mitad
   de una conversación: /model deepseek, /model custom:local, etc.

4. **hermes config set** — cambia el proveedor/modelo/base_url de forma
   persistente en config.yaml (afecta a nuevas sesiones).

5. **No existe un planificador horario nativo** en Hermes. Esa lógica la
   implementa Joko Lab con ai-router.

## Problema

El ai-router actual no funciona porque router-cron.sh fue refactorizado a un
"Modo Combinado" que escribe en /tmp/current-provider.txt, pero nadie lee ese
archivo para cambiar la configuración real de Hermes.

## Alternativas consideradas

### Alternativa A: router-cron.sh vuelve a modificar config.yaml (elegida)

El cron ejecuta `hermes config set` con el trío completo (provider, model,
base_url). Esto persiste en config.yaml y las nuevas sesiones de Hermes
arrancan con el proveedor correcto.

Ventajas:
- Usa la API oficial de Hermes (hermes config set)
- El cambio es persistente entre sesiones
- Elimina la capa de indirección de /tmp/current-provider.txt
- Funciona para cualquier modo de acceso (CLI, TUI, gateway)

Desventajas:
- No cambia el proveedor en una sesión activa
- Solo afecta a nuevas sesiones

### Alternativa B: provider-detect.sh se sourcea al inicio de cada sesión

Un script que detecta la hora y exporta variables que Hermes usaría
para determinar el proveedor.

Ventajas:
- Cambio en caliente

Desventajas:
- Hermes no tiene un mecanismo oficial para leer variables de entorno
  como fuente de proveedor
- No está documentado en la API oficial

### Alternativa C: Usar solo fallback_providers

Configurar DeepSeek como principal y Ollama como fallback automático.

Ventajas:
- Sin necesidad de cron
- Hermes gestiona el cambio automáticamente

Desventajas:
- No controla cuándo se usa cada uno (solo falla cuando hay error)
- No ahorra costes: DeepSeek se usaría siempre hasta que fallara

## Decisión

**OBSOLETA (14 de julio de 2026)** — Ver correccion en `docs/decisiones/2026-07-09-router-horario-cron.md`. DeepSeek V4 Flash es 13x mas barato que Gemini 2.5 Flash, por lo que no tiene sentido cambiar a Gemini ni a local por motivos de coste. El router horario queda desactivado.

Se adopta la Alternativa A: router-cron.sh modificará config.yaml usando
`hermes config set` con el trío completo de valores (provider + model + base_url).

Además se añadirán:
- `custom_providers:` con Ollama como proveedor local nombrado
- `fallback_providers:` con Ollama como respaldo automático si DeepSeek falla

El sistema legacy (provider-detect.sh, model-router.sh, /tmp/current-provider.txt)
se eliminará o archivará.

## Arquitectura final

### Config.yaml

```yaml
# Proveedor principal
model:
  default: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1

# Proveedor local (siempre disponible para cambio manual o fallback)
custom_providers:
  - name: local
    base_url: http://localhost:11434/v1

# Fallback automático si el principal falla
fallback_providers:
  - provider: custom
    model: mistral-nemo:12b
    base_url: http://localhost:11434/v1
```

### Router horario (router-cron.sh modificado)

```bash
# A las 03:00 → modo local (evitar coste DeepSeek en franja cara)
hermes config set model.provider custom:local
hermes config set model.default mistral-nemo:12b
hermes config set model.base_url http://localhost:11434/v1

# A las 12:00 → modo online (DeepSeek, franja normal)
hermes config set model.provider deepseek
hermes config set model.default deepseek-v4-flash
hermes config set model.base_url https://api.deepseek.com/v1
```

### Cambio manual en sesión

Dentro de una conversación de Hermes se puede usar:

```
/model deepseek                → volver a DeepSeek
/model custom:local            → ir a Ollama local
/model custom:local:mistral-nemo:12b  → modelo específico local
```

## Consecuencias

Positivas:
- El ai-router vuelve a funcionar realmente
- Se elimina la capa de indirección rota
- Coherente con la API oficial de Hermes
- DeepSeek como principal, Ollama como fallback automático
- Menos scripts que mantener

Negativas:
- El cambio de proveedor solo afecta a nuevas sesiones, no a las activas
- Dependencia del cron funcionando correctamente

## Archivos afectados

- ~/.hermes/config.yaml → añadir custom_providers y fallback_providers
- /home/jokoalmi/hermes-lab/scripts/router-cron.sh → reescribir para usar hermes config set
- /home/jokoalmi/hermes-lab/scripts/provider-detect.sh → eliminar o archivar
- /home/jokoalmi/hermes-lab/scripts/model-router.sh → mantener (solo terminal interactiva)

## Referencias

- Documentación oficial de Hermes: Fallback Providers
- Documentación oficial de Hermes: AI Providers (Custom & Self-Hosted)
- Skill ai-router: COMMANDS.md, KNOWLEDGE.md, references/check.md
- Bug documentado: references/2026-07-10-base_url-bug.md
