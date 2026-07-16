# Evaluación de GLM-4.7-Flash (Zhipu AI) — 2026-07-16

## Datos del modelo

| Característica | Valor |
|---|---|
| Proveedor | Zhipu AI (智谱 AI) |
| Modelo | GLM-4.7-Flash |
| Precio | Gratuito (tier free) |
| Contexto | 200K tokens |
| Requiere API key | Sí |
| Benchmarks públicos | Tool-calling/agentes por debajo de DeepSeek; latencia inicial y escritura competitivos |

## Relevancia para Joko Lab

GLM-4.7-Flash podría ocupar el mismo nicho que Gemini en el sistema:
un proveedor cloud secundario para franjas de bajo coste o fallback
cuando DeepSeek no esté disponible.

Sin embargo, el ahorro estimado respecto a la configuración actual es
**marginal (~$0.04/día)**, porque:
- DeepSeek ya es extremadamente barato para el volumen actual de uso
- El salto de precio entre DeepSeek y un modelo gratuito apenas se nota
  a menos que el volumen de tokens se multiplique por 10x

## Pendientes antes de decidir integración

1. **Prueba de calidad real**: ejecutar las 4 tareas representativas
   (lectura de log, diagnóstico propuesto, resumen de documento,
   tool-calling simple) en una sesión aislada con GLM y comparar
   resultado contra DeepSeek.
2. **Integración en el sistema**: si la prueba es positiva, habría que:
   - Crear `custom_providers` en `config.yaml` para Zhipu AI
   - Guardar la API key en `secrets/` con permisos 600
   - Añadir validación en `apply-decision.sh` (mismo patrón que deepseek/gemini)
   - Actualizar `policies/disponibilidad.yaml` y `capabilities/cloud.yaml`
3. **Decisión**: integrar como fallback, alternativa en franja pico, o
   descartar.

## Estado actual

- Sin urgencia. No se ha creado cuenta ni API key todavía.
- No hay configuración de Zhipu/GLM en ningún archivo del sistema
  (ni `config.yaml`, ni `secrets/`, ni `policies/`, ni `capabilities/`).
- La prueba de calidad real queda pendiente para cuando se decida
  priorizar esta integración.
