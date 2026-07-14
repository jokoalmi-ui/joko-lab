# Sprint 3 — Consolidación del Runtime de Joko Lab

**Fecha:** 2026-07-14
**Estado:** Plan aprobado, pendiente de ejecución

---

## Contexto

El Sprint 1-2 construyó un Decision Engine funcional que eliminó la dependencia
de `config.yaml` como fuente de verdad del proveedor activo. Sin embargo, el
sistema resultante aún arrastra herencias del diseño anterior:

- `apply-decision.sh` se ejecuta por cron cada 30 minutos, en lugar de responder bajo demanda.
- El provider global (`hermes config set provider`) sigue siendo el mecanismo de activación.
- Existen dos fuentes de verdad parciales (`state.json`, `ultima-decision.json`) sin jerarquía documentada.
- El log del Decision Engine duplica entradas.
- No hay tests.
- No hay un contrato formal del sistema.

## Problema

El laboratorio ha pasado de scripts que reescribían configuración a un motor
de decisiones, pero sigue siendo un conjunto de automatizaciones acopladas,
no un runtime agéntico estable.

## Decisión

Consolidar toda la arquitectura en un **Runtime Agéntico** antes de añadir
cualquier nueva funcionalidad. Durante este Sprint queda prohibido:

- Añadir nuevos modelos
- Añadir nuevas skills
- Modificar prompts
- Optimizar rendimiento
- Crear nuevos cron
- Introducir más capas

## Arquitectura objetivo

```
Runtime
│
├── State Manager       — conoce el estado actual del laboratorio
├── Policy Engine       — aplica reglas (horario, privacidad, coste)
├── Capability Registry — conoce qué puede hacer cada modelo
└── Decision Engine     — decide el proveedor en base a lo anterior
```

## Principios del Sprint

1. **Runtime First** — el Runtime es el único responsable de determinar el proveedor de ejecución.
2. **Contrato antes que implementación** — orden obligatorio: contrato, tests, implementación.
3. **Única fuente de verdad** — orden de precedencia documentado:

```
state.json
ultima-decision.json
defaults.yaml
```

## Entregables

1. **Runtime Contract** (`runtime/CONTRACT.md`)
   - Responsabilidades, límites, dependencias, módulos, API pública.
   - Estados válidos e inválidos.
   - Comportamiento sin state.json, sin Internet, sin cloud, sin Ollama.

2. **Runtime API** (contrato antes que código)
   - Entradas, salidas, códigos de error.
   - Ejemplo de respuesta:

```json
{
  "provider": "gemini",
  "model": "gemini-2.5-pro",
  "reason": "policy: horario",
  "privacy": "cloud",
  "verification": "LOW",
  "confidence": 1.0,
  "expires": 1800
}
```

3. **Eliminación del provider global**
   - El flujo actual (`DE → hermes config set provider → Hermes`) se sustituye por:
     `Hermes → Runtime.resolve() → Provider seleccionado`

4. **Eliminación del cron decisor**
   - Cualquier cron cuya única función sea decidir proveedor se elimina.
   - Único proceso periódico permitido: systemd timer → State Manager → state.json.
   - El Runtime consulta el estado bajo demanda.

5. **Limpieza del Decision Engine**
   - Eliminar llamadas duplicadas, logs duplicados, decisiones repetidas, código heredado.
   - El DE debe ser completamente determinista: una entrada, una salida, un log.

6. **Tests obligatorios**
   - Unit tests: State Manager, Policy Engine, Capability Registry, Decision Engine.
   - Integration tests:
     - Gemini disponible
     - DeepSeek disponible
     - Ambos disponibles
     - Ambos caídos
     - Privacidad activada
     - VRAM insuficiente
     - LM Studio apagado
     - Ollama apagado
     - state.json inexistente
     - Fallback funcionando

7. **Logging estructurado**

```json
{
  "timestamp": "...",
  "component": "DecisionEngine",
  "request_id": "...",
  "provider": "Gemini",
  "reason": "Horario",
  "duration_ms": 6
}
```

## Definición de terminado

El Sprint finaliza cuando:

- [ ] Exista un Runtime documentado
- [ ] El Runtime tenga contrato (`runtime/CONTRACT.md`)
- [ ] El Runtime tenga tests
- [ ] No existan decisiones duplicadas
- [ ] El provider deje de depender de `config.yaml`
- [ ] El cron ya no tome decisiones
- [ ] Exista una única fuente de verdad

## Consecuencias

- El laboratorio deja de ser un conjunto de scripts coordinados.
- Pasa a disponer de un Runtime agéntico estable, desacoplado de modelos concretos.
- Preparado para evolucionar sin rediseñar la arquitectura.
- La arquitectura queda lista para incorporar verificadores, evaluadores LLM o múltiples especialistas sin aumentar la complejidad.

## Alternativas consideradas

1. **Seguir añadiendo funcionalidad** — rechazado porque la base no está consolidada.
2. **Construir un Verifier/Evaluador ya** — rechazado, el Runtime debe ser sólido primero.
3. **Migrar a otra tecnología** — rechazado, la consolidación es más valiosa que el cambio tecnológico.

## Estado

Aprobado. Pendiente de ejecución.
