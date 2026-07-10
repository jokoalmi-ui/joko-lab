# Decisión Técnica: Arquitectura Híbrida Cloud-Local para Hermes

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Modelos y Enrutamiento

## Contexto
Se necesita aprovechar la velocidad de los modelos locales (Ollama) y la capacidad de razonamiento de los modelos en la nube (DeepSeek/Gemini) sin comprometer las reglas de seguridad del laboratorio.

## Decisión
1. **El agente orquestador** (responsable de planificar y decidir herramientas) usará **DeepSeek o Gemini** (nube) por su mejor razonamiento.
2. **El modelo de ejecución** (responsable de generar respuestas finales y resumir salidas) usará **qwen2.5:7b o llama31** (local) por su velocidad.
3. **Toda ejecución de comandos** requiere **confirmación explícita del usuario** (modo `manual` en approvals), independientemente del modelo activo.
4. **El enrutamiento horario** (cron) entre modelos locales y de nube queda documentado en `docs/vision/`.

## Reglas de seguridad innegociables
- No se ejecutarán comandos automáticamente.
- Cualquier acción que afecte al sistema de archivos o a procesos externos debe ser propuesta y confirmada.
- El modelo local nunca ejecutará comandos por sí mismo; solo actuará bajo la supervisión del agente orquestador.

## Impacto (Consecuencias)
- Mayor velocidad en respuestas simples (local) y mejor razonamiento en tareas complejas (nube).
- Se mantiene el control total del usuario sobre las acciones del sistema.
- La configuración de `approvals.mode: manual` permanece inalterada.

## Alternativas descartadas
- Ejecución automática de comandos (rechazada por seguridad).
- Delegación completa al modelo local (rechazada por falta de capacidad de razonamiento).

## Referencias
- `HERMES.md` (reglas de seguridad)
- `docs/vision/` (cron y alternancia)