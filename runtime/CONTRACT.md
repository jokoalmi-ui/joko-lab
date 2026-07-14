# Runtime Contract — Joko Lab

**Versión:** 1.0-draft
**Estado:** Contrato de diseño. Pendiente de revisión antes de implementar.
**Fecha:** 2026-07-14

---

## 1. Propósito

El Runtime de Joko Lab es el único responsable de determinar el proveedor de
ejecución (cloud o local) para cada solicitud. No es un orquestador de tareas.
No es un agente. Es un motor de decisión puro que, dado un estado y unas
políticas, devuelve un proveedor.

---

## 2. Arquitectura

```
Runtime
│
├── State Manager       — observa el laboratorio, escribe state.json
├── Policy Engine       — interpreta políticas, nunca decide
├── Capability Registry — describe capacidades, nunca decide
└── Decision Engine     — decide basado en state + policies
```

### Reglas estructurales

- State Manager: solo observa. Nunca decide.
- Policy Engine: solo interpreta políticas. Nunca consulta APIs. Nunca modifica estado.
- Capability Registry: solo describe capacidades. Nunca toma decisiones.
- Decision Engine: solo decide. Nunca consulta hardware directamente. Nunca ejecuta herramientas. Nunca modifica configuración.

---

## 3. API pública

### `Runtime.resolve(task_hint: str = "") -> Decision`

**Entrada:**
- `task_hint` (string, opcional): pista sobre el tipo de tarea (reservado para el Capability Registry futuro).

**Salida:**
```json
{
  "provider": "gemini",
  "model": "gemini-2.5-pro",
  "reason": "Horario: 03:00-12:00, ahora 10:29",
  "privacy": "cloud",
  "verification": "LOW",
  "confidence": 1.0,
  "expires": 1800
}
```

### Campos de salida

| Campo | Tipo | Descripción | Obligatorio |
|---|---|---|---|
| `provider` | string | Proveedor seleccionado | Siempre |
| `model` | string | Modelo dentro del proveedor | Siempre |
| `reason` | string | Motivo legible de la decisión | Siempre |
| `privacy` | string | `"cloud"` o `"local"` | Siempre |
| `verification` | string | Nivel de verificación: `"LOW"`, `"MEDIUM"`, `"HIGH"` | Siempre |
| `confidence` | float | 0.0 - 1.0 | Siempre |
| `expires` | int | Segundos hasta que la decisión se considera obsoleta | Opcional |

### Códigos de error (caso de fallo)

Cuando el Runtime no puede decidir, devuelve:

```json
{
  "provider": "none",
  "model": "none",
  "reason": "ERROR: <descripción>",
  "privacy": "unknown",
  "verification": "NONE",
  "confidence": 0.0
}
```

| Escenario | `reason` contiene |
|---|---|
| state.json no existe y no hay fallback | `"state.json no disponible"` |
| Ningún proveedor disponible | `"ningún proveedor disponible"` |
| Error interno en política | `"ERROR en política '<nombre>': <detalle>"` |
| Sin Internet y sin local | `"sin conectividad y sin modelo local"` |

---

## 4. Orden de precedencia

### Fuentes de verdad

```
1. state.json          → Fuente principal (producida por State Manager cada 60s)
2. ultima-decision.json → Fallback inmediato (última decisión aceptada)
3. defaults            → Fallback final (valores compilados en el código)
```

### Evaluación de políticas (precedencia)

```
1. Privacidad       → si datos_sensibles=true, forzar local
2. Disponibilidad   → si proveedor caído, fallback al siguiente disponible
3. Costes           → si saldo insuficiente, forzar local
4. Horario          → política horaria (franjas)
5. Preferencias     → fallback por defecto
```

La primera política que devuelva una decisión no nula es la que se aplica.
Si todas devuelven None, se usa el fallback por defecto.

---

## 5. Comportamiento en casos de fallo

### Sin state.json

1. Intentar cargar `ultima-decision.json`.
2. Si existe, devolver esa decisión marcando `reason: "FALLBACK: state.json no disponible"`.
3. Si no existe, devolver fallback por defecto (`deepseek/deepseek-v4-flash`).

### Sin Internet

1. State Manager detecta `cloud.deepseek.disponible = false` y `cloud.gemini.disponible = false`.
2. Policy Engine (disponibilidad) fuerza a local.
3. Si local tampoco está disponible, devuelve `provider: "none"`.

### Sin cloud (Gemini y DeepSeek caídos)

Ídem "Sin Internet". El Runtime no puede operar en cloud, fuerza local o error.

### Sin Ollama (local caído)

1. State Manager detecta `services.ollama.activo = false`.
2. Policy Engine (disponibilidad) detecta que no hay fallback local.
3. Si al menos un cloud está disponible, usa cloud.
4. Si ningún cloud está disponible, devuelve `provider: "none"`.

### Sin LM Studio

No afecta al Runtime. LM Studio es opcional. Si no está activo, el
Capability Registry (futuro) simplemente no listará sus modelos.

---

## 6. Dependencias

### Dependencias directas del Runtime

| Componente | Depende de | Tipo |
|---|---|---|
| Decision Engine | state.json (State Manager) | Archivo |
| Decision Engine | policies/*.yaml | Archivo |
| State Manager | nvidia-smi | Comando externo |
| State Manager | curl | Comando externo |
| State Manager | Servicios locales (Ollama, LM Studio, etc.) | Red local |

### NO dependencias

El Runtime NO depende de:
- Hermes Agent (config.yaml, hermes CLI)
- Docker Compose
- Cron
- Director Estratégico (futuro)
- Internet para funcionar (aunque sin Internet no puede elegir cloud)

---

## 7. Límites

- El Runtime no ejecuta tareas. Solo decide qué proveedor usar.
- El Runtime no almacena datos de usuario. Solo estado del sistema.
- El Runtime no tiene estado mutable propio. Solo lee state.json y escribe ultima-decision.json.
- El Runtime no hace autenticación. Las API keys se gestionan fuera (lab-state/secrets/).
- El Runtime no orquesta flujos de trabajo. Eso es responsabilidad del Director Estratégico (futuro).

---

## 8. Estados válidos e inválidos

### Estados válidos de una decisión

- `provider` en: `"deepseek"`, `"gemini"`, `"ollama"`, `"none"`
- `privacy` en: `"cloud"`, `"local"`, `"unknown"`
- `verification` en: `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"NONE"`
- `confidence` en: `[0.0, 1.0]`

### Estados inválidos

- `provider: ""` o `null`
- `confidence < 0.0` o `> 1.0`
- `privacy: ""` o `null`
- Que `provider` y `model` sean inconsistentes (ej: `provider: "deepseek"` con `model: "gemini-2.5-pro"`)

---

## 9. Logging (diseño)

Cada módulo del Runtime genera eventos estructurados con este formato:

```json
{
  "timestamp": "2026-07-14T10:30:01",
  "component": "DecisionEngine",
  "operation": "resolve",
  "provider": "gemini",
  "model": "gemini-2.5-pro",
  "reason": "Horario: 03:00-12:00, ahora 10:29",
  "duration_ms": 6,
  "status": "success"
}
```

- `component` en: `"StateManager"`, `"PolicyEngine"`, `"CapabilityRegistry"`, `"DecisionEngine"`
- `operation` en: `"collect"`, `"resolve"`, `"evaluate"`, `"fallback"`
- `status` en: `"success"`, `"fallback"`, `"error"`

No se permiten logs ambiguos. Cualquier log debe poder trazarse a un componente y una operación concretos.

---

## 10. Tests (diseño)

### Unit tests

| Componente | Test |
|---|---|
| State Manager | state.json se escribe correctamente |
| State Manager | Campos requeridos están presentes |
| Policy Engine | Cada política devuelve None cuando no aplica |
| Policy Engine | Privacidad fuerza local si datos_sensibles=true |
| Policy Engine | Disponibilidad fuerza fallback si proveedor caído |
| Decision Engine | decide() devuelve un dict con todos los campos |
| Decision Engine | decide() sin state.json usa fallback |

### Integration tests

| Escenario | Comportamiento esperado |
|---|---|
| Gemini disponible, DeepSeek caído | Usar Gemini |
| Ambos cloud disponibles | Seguir política horaria |
| Ambos cloud caídos | Forzar local o none |
| Privacidad activada | Forzar local |
| state.json inexistente | Usar fallback (ultima-decision o defaults) |
| Ollama caído | Seguir con cloud si disponible |
| VRAM insuficiente (futuro) | Reportado por State Manager, evaluado por Policy |

---

## 11. Versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0-draft | 2026-07-14 | Contrato inicial del Runtime |

Este contrato es un documento vivo. Se actualiza cuando cambia la arquitectura,
nunca por conveniencia.
