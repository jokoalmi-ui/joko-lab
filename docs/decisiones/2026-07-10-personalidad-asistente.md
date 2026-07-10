# Decisión Técnica: Personalidad del Asistente en Joko Lab

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Configuración del Agente (Hermes)

## Contexto
El asistente Hermes requiere un comportamiento base explícito (definido en `display.personality`) que esté 100% alineado con las reglas de seguridad descritas en `HERMES.md`.

## Problema
Evitar que la IA asuma un rol excesivamente proactivo que intente ejecutar acciones, explorar el sistema o listar directorios sin el consentimiento previo del usuario, lo que violaría la política de ejecución no automática.

## Alternativas descartadas
- Mantener la personalidad por defecto (podría llevar a ejecuciones autónomas indeseadas).
- Configurar reglas complejas a nivel de LLM en lugar de fijar el comportamiento en el `config.yaml`.

## Decisión
Se añade explícitamente el siguiente bloque a la configuración de Hermes (`display.personality`):
> "Eres un asistente que ayuda al usuario en el laboratorio Joko Lab. Siempre propones acciones antes de ejecutarlas y esperas confirmación. Si el usuario pide listar archivos, sugiere el comando `ls -la` y espera a que el usuario lo ejecute o te autorice."

## Motivos
- Refuerza la regla absoluta de Joko Lab: "No ejecutar comandos automáticamente".
- Garantiza que la interacción con el sistema de archivos (ej. lecturas de directorios) ocurra siempre bajo un modelo de sugerencia → autorización explícita.
- Consolida el flujo de "Comprender antes de actuar".

## Consecuencias
- Las interacciones requerirán un paso extra de confirmación para tareas simples de exploración, favoreciendo la seguridad sobre la rapidez.
- Se mantiene coherencia total con la configuración `approvals.mode: manual`.

## Referencias
- `HERMES.md` (Principios del laboratorio y Reglas de seguridad).
- `~/.hermes/config.yaml` (Archivo de configuración local).