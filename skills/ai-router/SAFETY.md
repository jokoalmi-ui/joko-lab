# ai-router — Seguridad

## Reglas obligatorias

1. **No enviar datos privados a proveedores externos.** Si la tarea contiene información sensible, se fuerza el enrutamiento a Ollama (local). No hay excepción aunque el modelo local no pueda resolver la tarea.

2. **No cambiar el proveedor por defecto de Hermes** sin explicar el impacto y recibir confirmación explícita. Cambiar el proveedor afecta a todas las conversaciones, no solo a tareas específicas.

3. **No modificar la configuración de Ollama, LM Studio ni Gemini** sin autorización explícita.

4. **No asumir que un modelo local está disponible** sin verificarlo primero con `curl`. Los contenedores pueden estar parados o el API Server de LM Studio puede estar desactivado.

5. **No instalar modelos nuevos en Ollama automáticamente.** Descargar modelos consume ancho de banda y espacio en disco. Requiere confirmación explícita.

6. **No enviar datos privados a Gemini aunque sea multimodal.** Si la tarea contiene datos sensibles y necesita visión, se informa al usuario de la limitación en lugar de enviarlos a un proveedor externo.

## Riesgos conocidos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Ollama parado | Tareas locales fallan con error de conexión | Verificar antes de enrutar |
| VRAM insuficiente | Modelo grande no carga o Out-of-Memory | Medir VRAM antes de decidir |
| LM Studio sin modelo cargado | Tareas de visión fallan | Verificar antes de enrutar (`curl localhost:1234/api/v0/models`) |
| Cambiar proveedor de Hermes | Afecta a todas las conversaciones | No hacerlo sin confirmación |
| DeepSeek caído | Tareas de razonamiento no disponibles | Informar, sugerir alternativa local |
| Modelo ligero no instalado | El enrutamiento a ligero falla | Verificar modelos disponibles primero |

## Límites conocidos

- **Ollama:** contexto típico de 4k-8k tokens (modelos pequeños) a 128k (modelos grandes)
- **DeepSeek:** 128k tokens de contexto, pero es externo (datos salen del equipo)
- **Gemini:** depende del plan, contexto largo pero externo
- **LM Studio:** modelos hasta lo que quepa en VRAM
