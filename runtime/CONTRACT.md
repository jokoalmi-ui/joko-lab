---
type: infrastructure
subtype: infrastructure
status: active
tags: [infrastructure]
created: 2026-07-14
---
# Runtime Contract — Joko Lab

**Versión:** 1.0
**Estado:** Congelado. Cualquier cambio incompatible requiere incrementar la versión.
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
├── Decision Engine     — decide basado en state + policies
└── Metrics             — registra métricas de uso (diseño, sin implementar)
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
  "policy": "horario.yaml",
  "privacy": "cloud",
  "verification": "LOW",
  "confidence": 1.0,
  "expires": "2026-07-14T12:00:00+02:00",
  "decision_id": "20260714-103812-a1f4"
}
```

### Campos de salida

| Campo | Tipo | Descripción | Obligatorio |
|---|---|---|---|
| `provider` | string | Proveedor seleccionado | Siempre |
| `model` | string | Modelo dentro del proveedor | Siempre |
| `reason` | string | Motivo legible de la decisión | Siempre |
| `policy` | string | Nombre del archivo de política que ganó | Siempre |
| `privacy` | string | `"cloud"` o `"local"` | Siempre |
| `verification` | string | `"LOW"`, `"MEDIUM"`, `"HIGH"` | Siempre |
| `confidence` | float | 0.0 - 1.0 | Siempre |
| `expires` | string | ISO 8601 del momento en que la decisión caduca | Siempre |
| `decision_id` | string | Identificador único de esta decisión | Siempre |

### Códigos de error (caso de fallo)

Cuando el Runtime no puede decidir, devuelve:

```json
{
  "provider": "none",
  "model": "none",
  "reason": "ERROR: <descripción>",
  "policy": "none",
  "privacy": "unknown",
  "verification": "NONE",
  "confidence": 0.0,
  "expires": null,
  "decision_id": "20260714-103812-a1f4"
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
2. ultima-decision.json → Fallback inmediato (última decisión aceptada, escrita por el Runtime)
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
2. Si existe, devolver esa decisión con `reason: "FALLBACK: state.json no disponible"`.
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
- El Runtime no tiene estado mutable propio. Solo lee state.json y escribe ultima-decision.json y decision.log.
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
- `expires` en formato distinto a ISO 8601

---

## 9. El Runtime registra sus decisiones

El Runtime es responsable de registrar cada decisión que toma. Esto NO es
responsabilidad del adaptador (apply-decision.sh).

El Runtime escribe dos cosas:

### a) `ultima-decision.json`

La última decisión completa. Sobrescrita en cada `resolve()`.

```json
{
  "provider": "gemini",
  "model": "gemini-2.5-pro",
  "reason": "Horario: 03:00-12:00, ahora 10:29",
  "policy": "horario.yaml",
  "privacy": "cloud",
  "verification": "LOW",
  "confidence": 1.0,
  "expires": "2026-07-14T12:00:00+02:00",
  "decision_id": "20260714-103812-a1f4"
}
```

### b) `decision.log`

Cada decisión se añade al final del log estructurado:

```json
{
  "timestamp": "2026-07-14T10:38:12+02:00",
  "component": "DecisionEngine",
  "operation": "resolve",
  "provider": "gemini",
  "model": "gemini-2.5-pro",
  "policy": "horario.yaml",
  "decision_id": "20260714-103812-a1f4",
  "reason": "Horario: 03:00-12:00, ahora 10:29",
  "duration_ms": 6,
  "status": "success"
}
```

- `operation` en: `"resolve"`, `"fallback"`, `"error"`
- `status` en: `"success"`, `"fallback"`, `"error"`

No se permiten logs ambiguos.

---

## 10. apply-decision.sh como adaptador

`apply-decision.sh` NO contiene lógica de negocio.

Su responsabilidad se limita a:

1. Llamar a `Runtime.resolve()` (vía `python3 runtime/api.py --json`)
2. Aplicar el resultado mediante `hermes config set`
3. Informar del resultado

No decide. No registra. No parsea políticas. No conoce el estado del laboratorio.

Es un adaptador entre el Runtime y Hermes CLI.

---

## 11. Golden Dataset

Los tests se basan en un conjunto de casos YAML en `runtime/tests/cases/`.

Cada caso:

```yaml
name: horario-manana
description: Franja 03:00-12:00 debe elegir Gemini
state:
  hora_actual: "09:30"
  deepseek_disponible: true
  gemini_disponible: true
  ollama_activo: true
  privacidad_activada: false
expect:
  provider: gemini
  policy: horario.yaml
  privacy: cloud
```

El suite de tests itera sobre todos los casos, simula el estado, llama al
Runtime y verifica que la salida coincida con `expect`.

---

## 12. Metrics (diseño, sin implementar)

El Runtime deberá registrar métricas acumuladas para permitir decisiones
basadas en datos reales en el futuro.

Métricas a registrar (diseño):

| Métrica | Descripción |
|---|---|
| TTFT por proveedor | Tiempo hasta el primer token (media, p99) |
| tokens/minuto | Throughput por proveedor |
| latencia por petición | Tiempo de respuesta completo |
| coste acumulado | USD gastado por proveedor (a partir de precios oficiales y tokens) |
| cambios de proveedor | Cuántas veces se cambió de proveedor en X tiempo |
| fallos por proveedor | Errores 4xx/5xx, timeouts |
| % local vs cloud | Proporción de uso local frente a cloud |

No implementar hasta que el Runtime esté estable y tenga tests.

---

## 13. Control de versiones del contrato

Cualquier cambio incompatible con este contrato requiere incrementar la
versión (v1.0 → v2.0).

Se considera cambio incompatible:
- Añadir un campo obligatorio a la salida de `resolve()`
- Eliminar un campo obligatorio
- Cambiar el tipo de un campo existente
- Cambiar el orden de precedencia de políticas
- Añadir o eliminar un proveedor soportado

No requiere cambio de versión:
- Añadir un campo opcional
- Añadir una política nueva (se evalúa después de las existentes)
- Cambiar valores por defecto en policies/*.yaml
- Correcciones de bugs que no alteren el comportamiento esperado del contrato

---

## 14. Versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-14 | Contrato congelado del Runtime Joko Lab |

Este contrato es la fuente de verdad del Runtime. Cualquier implementación
debe cumplirlo, no redefinirlo.
