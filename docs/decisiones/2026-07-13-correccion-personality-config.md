# Decisión Técnica: Corrección de display.personality y tono neutro

**Fecha**: 2026-07-13
**Estado**: Aceptada
**Área**: Configuración del Agente (Hermes)
**Referencia previa**: 2026-07-10-personalidad-asistente.md

## Contexto
Al auditar `config.yaml` se detectó que `display.personality` (línea 245) no
coincide con el texto aprobado en la decisión 2026-07-10-personalidad-asistente.md.
El bloque actual añade un rol de "Arquitecto Técnico (Cloud) con Ingeniero de
Ejecución local a su cargo" que no fue documentado como decisión independiente.

Adicionalmente, se detectó un patrón de tono halagador/adulador en las respuestas
del agente (ej. "tu crítica es brillante", "agudeza clínica excepcional") que no
proviene de ninguna instrucción explícita en config.yaml ni en las skills
(verificado con grep sobre skills/). Se atribuye a comportamiento por defecto del
modelo cloud (gemini-3.5-flash) sin restricción de estilo.

## Problema
1. Configuración real diverge de decisión documentada (deuda de gobernanza).
2. Tono adulador reduce la fiabilidad percibida de auditorías e informes técnicos,
   especialmente en contexto de seguridad, donde el tono neutro facilita detectar
   sesgos de complacencia.

## Decisión
Se mantiene el rol de "Arquitecto Técnico (Cloud) con delegate_task" por ser
coherente con la arquitectura híbrida cloud-local ya aceptada
(2026-07-10-arquitectura-hibrida-cloud-local.md), pero se añade una instrucción
explícita de tono al final de `display.personality`:

> "Sé directo, técnico y neutro. No elogies ni valides las preguntas o críticas
> del usuario antes de responder; ve directo al análisis, al dato o a la acción
> propuesta. Evita superlativos y adjetivos valorativos sobre la calidad del
> razonamiento del usuario."

## Motivos
- Alinea la configuración real con lo documentado (cierra la deuda de gobernanza).
- Refuerza la fiabilidad de auditorías e informes técnicos generados por Hermes.
- No afecta la regla de "proponer antes de ejecutar" (approvals.mode: manual),
  que se mantiene sin cambios.

## Consecuencias
- Respuestas más secas/directas en contextos donde antes había refuerzo positivo.
- Ninguna consecuencia sobre approvals, delegación o seguridad de ejecución.

## Referencias
- `docs/decisiones/2026-07-10-personalidad-asistente.md`
- `docs/decisiones/2026-07-10-arquitectura-hibrida-cloud-local.md`
- `~/.hermes/config.yaml` (display.personality, línea 245)
