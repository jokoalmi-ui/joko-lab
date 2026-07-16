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

GLM-4.7-Flash se evaluó específicamente como posible **suplente de
Gemini 3.1 Flash-Lite** en el sistema, no como sustituto de DeepSeek.

El nicho sería el mismo que ocupa Gemini hoy: proveedor cloud secundario
para la franja nocturna (03:00-12:00, según `horario.yaml`), o fallback
cuando DeepSeek no esté disponible.

Ventaja potencial de GLM frente a Gemini:
- **Coste cero** (tier free de Zhipu) vs **$0.25/$1.50 por M tokens** de
  Gemini 3.1 Flash-Lite (precios estimados de Google).

Sin embargo, el ahorro real respecto a la configuración actual es
**marginal (~$0.04/día)**, porque DeepSeek ya es extremadamente barato
para el volumen actual de uso, y GLM solo ocuparía una franja de 9h.

## Falta de comparativa pública directa GLM-4.7-Flash vs Gemini 3.1 Flash-Lite

No existe ninguna comparativa pública directa entre estos dos modelos.
Verificado el 2026-07-16 en:

| Fuente | Resultado |
|---|---|
| Artificial Analysis | No tienen el par GLM-4.7-Flash vs Gemini 3.1 Flash-Lite |
| LLM Stats | No tienen el par. Lo más cercano es GLM-4.7-Flash vs Gemini 3 Flash (no Lite) |
| BenchLM | Tienen fichas individuales de cada uno, sin comparativa directa |
| SourceForge | Página listando ambos modelos sin datos comparativos reales |

Lo que sí existe son comparativas parciales:
- **GLM-4.7-Flash vs Gemini 3 Flash Preview** (modelo anterior, no Lite):
  Gemini gana en 5 benchmarks (AIME, GPQA, SWE-Bench, Terminal-Bench);
  GLM es ~7.4x más barato. Pero no es el modelo que tenemos configurado.
- **Gemini 3.1 Flash-Lite individual**: 46/100 en BenchLM, MMLU-Pro 83%,
  BFCL v3 (function calling) 76.5%, velocidad 276.7 tok/s.
- **GLM-4.7-Flash individual**: ~31.2B params, 3B activos en inferencia.
  Benchmarks de tool-calling/agentes por debajo de DeepSeek.

**Conclusión:** sin datos externos en los que apoyarse, la decisión
entre GLM-4.7-Flash y Gemini 3.1 Flash-Lite requiere obligatoriamente
una prueba de calidad manual con tareas reales de Joko Lab antes de
cualquier cambio en `horario.yaml`. No se debe decidir por especulación.

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
