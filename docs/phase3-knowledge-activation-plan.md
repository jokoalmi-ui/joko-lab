---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-30
---
# Phase 3 — Plan Técnico: Knowledge Activation Layer

**Versión:** 1.0 — 2026-07-30
**Origen:** Input de Luis + estado actual de Joko Lab
**Estado:** PLAN — No ejecutar sin revisión

---

## RESUMEN EJECUTIVO

Añadir 4 componentes nuevos y modificar 3 existentes.
Tiempo estimado: ~15h distribuidas en 5 sprints.
Resultado: el laboratorio pasa de "sistema documental" a "sistema adaptativo".

---

## ARQUITECTURA OBJETIVO

```
Usuario
  │
  ▼
Task Analyzer          [EXISTENTE — modificar]
  │
  ▼
Knowledge Resolver     [EXISTENTE — sin cambios]
  │
  ▼
Activation Engine      [NUEVO — Sprint 2]
  │
  ▼
Decision Engine        [EXISTENTE — modificar]
  │
  ▼
Respuesta
  │
  ▼
Event Bus              [NUEVO — Sprint 3]
  │
  ▼
Confidence Decayer     [NUEVO — Sprint 4]
  │
  ▼
Debt Detector          [NUEVO — Sprint 5]
```

---

## MAPEO DE COMPONENTES ACTUALES A MODIFICAR

### Componentes nuevos (4)

| # | Componente | Qué hace | Sprint |
|---|-----------|----------|:------:|
| 1 | **RULE Store** | YAML con reglas activas derivadas de DEC | 1 |
| 2 | **Activation Engine** | Busca conocimiento activable y lo inyecta | 2 |
| 3 | **Event Bus** | Dispara eventos ante nueva DEC/EXP/benchmark | 3 |
| 4 | **Confidence Decayer** | Recalcula confianza con factor temporal | 4 |
| 5 | **Debt Detector** | Análisis estático de dependencias rotas | 5 |

### Componentes a modificar (3)

| # | Componente | Cambio | Sprint |
|---|-----------|--------|:------:|
| 1 | **decision_engine.py** | Aceptar input del Activation Engine (RULE activas) | 2 |
| 2 | **KNOWLEDGE_TYPES** | Añadir tipo RULE y POLICY a la clasificación actual | 1 |
| 3 | **jerarquia-autoridad.md** | Incluir RULE y POLICY en la jerarquía de autoridad | 1 |

### Componentes sin cambios

| Componente | Por qué no se toca |
|-----------|-------------------|
| Context Builder | No participa en activación |
| Knowledge Resolver | Ya devuelve DEC/EXP correctamente |
| Evaluator-Optimizer | Se beneficiará indirectamente de RULE activas |
| Prompt Compiler | Ídem |
| State Manager | Ya funciona, consumirá eventos en Sprint 3 |

---

## SPRINT 1 — Formalizar RULE y POLICY (3h)

### Objetivo
Crear la base de datos de reglas activas. Sin esto, nada de lo demás funciona.

### Entregables

**1.1 — `01-knowledge/rules/` (directorio nuevo)**

```
01-knowledge/rules/
  RULE-001-modelo-creatividad.yaml
  RULE-002-modelo-json.yaml
  RULE-003-modelo-razonamiento.yaml
  RULE-004-bloqueo-fatales.yaml
  index.md
```

Formato de RULE:

```yaml
id: RULE-001
origen: DEC-003
desc: "Usar Gemma 4 para tareas creativas"
condicion:
  tipo_tarea: ["creatividad", "brainstorming"]
accion:
  modelo: "gemma-4-12b"
  proveedor: "lmstudio"
prioridad: 90
activa: true
validaciones: 3
ultima_revision: "2026-07-29"
confianza: 0.94
```

**1.2 — `01-knowledge/policies/` (directorio nuevo)**

```
01-knowledge/policies/
  POLICY-001-fatales.yaml
  POLICY-002-privacidad.yaml
  index.md
```

Formato de POLICY:

```yaml
id: POLICY-001
desc: "Nunca usar modelo con FATAL activo"
alcance: "global"
condicion:
  FATAL: "activo"
accion: "bloquear_modelo"
prioridad: 100
```

**1.3 — Ampliar `decision_engine.py` KNOWLEDGE_TYPES**

Añadir:

```python
"RULE":   {"type": "activo", "can_modify": True,  "priority": 8},
"POLICY": {"type": "activo", "can_modify": True,  "priority": 9},
```

**1.4 — Actualizar `jerarquia-autoridad.md`**

Añadir entrada para RULE y POLICY en la tabla de niveles de autoridad.

### Verificación

```bash
python3 -c "from tools.decision_engine import KNOWLEDGE_TYPES; assert 'RULE' in KNOWLEDGE_TYPES; assert 'POLICY' in KNOWLEDGE_TYPES; print('OK')"
ls /home/jokoalmi/joko-lab/01-knowledge/rules/RULE-*.yaml | wc -l  # debe ser >= 4
ls /home/jokoalmi/joko-lab/01-knowledge/policies/POLICY-*.yaml | wc -l  # debe ser >= 2
```

---

## SPRINT 2 — Activation Engine (4h)

### Objetivo
El componente que busca RULE activas antes de cada ejecución y las inyecta en el Decision Engine.

### Entregables

**2.1 — `tools/activation_engine.py` (nuevo)**

```python
class ActivationEngine:
    """
    Busca reglas activas aplicables a la tarea actual.
    No responde. No razona. Solo activa.
    """
    def activate(self, task_type: str, context: dict) -> list[dict]:
        # 1. Cargar todas las RULE activas de rules/*.yaml
        # 2. Filtrar por task_type
        # 3. Ordenar por prioridad
        # 4. Devolver lista de reglas aplicables
        pass
```

Pseudo-flujo:

```
cargar RULE-*.yaml
→ filtrar activas=True
→ filtrar por task_type
→ ordenar por prioridad desc
→ devolver [
    {"rule_id": "RULE-001", "modelo": "gemma-4-12b", "razon": "DEC-003: creatividad"},
    ...
  ]
```

**2.2 — Modificar `decision_engine.py` para aceptar RULE activas**

El método `decide()` actual acepta `task_type` y `context`. Añadir parámetro opcional `active_rules`:

```python
def decide(self, task_type: str, context: dict, active_rules: list[dict] = None) -> dict:
    if active_rules:
        # Las RULE activas tienen prioridad sobre la lógica por defecto
        for rule in active_rules:
            if rule["prioridad"] >= 90:
                # Auto-aplicar sin preguntar
                decision["modelo"] = rule["modelo"]
                decision["origen"] = rule["razon"]
                return decision
    # Fallback a lógica actual
    ...
```

**2.3 — Integración en el pipeline**

Donde actualmente se llama:

```python
context = knowledge_resolver.resolve(task_type)
decision = decision_engine.decide(task_type, context)
```

Pasa a:

```python
context = knowledge_resolver.resolve(task_type)
active_rules = activation_engine.activate(task_type, context)
decision = decision_engine.decide(task_type, context, active_rules)
```

### Verificación

```bash
python3 tools/activation_engine.py --task-type creatividad
# Debe devolver: RULE-001 activa → Gemma 4

python3 tools/activation_engine.py --task-type json
# Debe devolver: RULE-002 activa → Granite 4.1
```

---

## SPRINT 3 — Event Bus (3h)

### Objetivo
Capitalización automática: cuando se crea una DEC/EXP nueva, el sistema reacciona.

### Entregables

**3.1 — `tools/event_bus.py` (nuevo)**

Eventos definidos:

| Evento | Disparador | Acción |
|--------|-----------|--------|
| `dec.created` | Nueva DEC en decisions/ | Buscar RULE afectadas, sugerir activación |
| `exp.completed` | Nuevo EXP con resultados | Buscar DEC relacionadas, sugerir revisión |
| `benchmark.new` | Nuevo benchmark de modelo | Buscar DEC que mencionen ese modelo, marcar para revisión |
| `model.updated` | Nueva versión de modelo (ej: Granite 4.2) | Invalidar DEC/EXP basadas en versión anterior |

**3.2 — `tools/event_bus.py` implementación inicial**

```python
class EventBus:
    def emit(self, event_type: str, payload: dict):
        """Dispara evento. Los suscriptores reaccionan."""
        pass
    
    def on_dec_created(self, dec_id: str):
        """Buscar si la nueva DEC invalida RULE existentes."""
        pass
    
    def on_model_updated(self, model_name: str, new_version: str):
        """Marcar DEC/EXP/RULE que referencian versiones antiguas."""
        pass
```

**3.3 — Watchdog simple**

Script que monitorea `01-knowledge/decisions/` y `01-knowledge/experiments/`:

```bash
# cron o systemd path watcher
inotifywait -m /home/jokoalmi/joko-lab/01-knowledge/decisions/ -e create |
while read path action file; do
    python3 tools/event_bus.py --event dec.created --payload "$file"
done
```

### Verificación

```bash
# Simular nueva DEC
touch /home/jokoalmi/joko-lab/01-knowledge/decisions/DEC-007.yaml
python3 tools/event_bus.py --event dec.created --payload DEC-007.yaml
# Debe mostrar: "Buscando RULE afectadas por DEC-007..."
```

---

## SPRINT 4 — Confidence Decay (3h)

### Objetivo
Las decisiones envejecen. La confianza debe reflejarlo.

### Entregables

**4.1 — `tools/confidence_decayer.py` (nuevo)**

Fórmula:

```python
def recalculate_confidence(rule: dict) -> float:
    base = rule["evidencia"]          # 0.0 - 1.0
    recencia = recency_factor(rule["ultima_revision"])  # decae con el tiempo
    validaciones = min(rule["validaciones"] / 5, 1.0)   # satura en 5
    compatibilidad = version_compat(rule.get("version_modelo"))
    
    return base * recencia * validaciones * compatibilidad

def recency_factor(last_review_date: str) -> float:
    days = (today - last_review_date).days
    if days < 30: return 1.0
    if days < 90: return 0.8
    if days < 180: return 0.5
    return 0.3
```

**4.2 — Integración con RULE store**

Cada RULE tiene `confianza` recalculable:

```bash
python3 tools/confidence_decayer.py --recalc-all
# Actualiza confianza de todas las RULE
```

**4.3 — Umbral de desactivación**

Si confianza < 0.4 → `activa: false` automáticamente + notificar.

### Verificación

```bash
python3 tools/confidence_decayer.py --rule RULE-001
# DEC-003 de hace 30 días: confianza 0.94
# DEC-003 de hace 9 meses: confianza 0.28 → DESACTIVADA
```

---

## SPRINT 5 — Debt Detector (2h)

### Objetivo
Detección automática de deuda técnica en el conocimiento.

### Entregables

**5.1 — `tools/debt_detector.py` (nuevo)**

Checks:

| Check | Qué detecta | Severidad |
|-------|------------|:---------:|
| `huerfano` | RULE sin DEC origen válida | ALTA |
| `conflicto` | 2+ RULE para misma tarea con modelos distintos | MEDIA |
| `no_usado` | RULE activa nunca invocada en 90 días | BAJA |
| `huerfano_exp` | DEC que referencia EXP inexistente | ALTA |
| `sin_validar` | DEC/RULE sin validación en 180 días | MEDIA |
| `version_antigua` | DEC basada en versión de modelo ya superada | MEDIA |

**5.2 — Reporte**

```bash
python3 tools/debt_detector.py --full
```

Salida:

```
DEBT REPORT 2026-07-30
======================
ALTA (2):
  RULE-002 → referencia DEC-005 que no existe
  DEC-004  → referencia EXP-001 que fue eliminado

MEDIA (3):
  RULE-001 y RULE-005 → conflicto: dos modelos para 'creatividad'
  DEC-003 → sin validar en 210 días
  DEC-007 → basada en Granite 4.1, versión actual: 4.2

BAJA (1):
  RULE-004 → activa pero nunca invocada
```

### Verificación

```bash
python3 tools/debt_detector.py --full | grep "ALTA"
# Debe listar deuda de alta prioridad si existe
```

---

## ORDEN DE EJECUCIÓN

```
Sprint 1 ──► Sprint 2 ──► Sprint 3 ──► Sprint 4 ──► Sprint 5
 (3h)        (4h)        (3h)        (3h)        (2h)
```

No se puede invertir:
- Sprint 2 depende de Sprint 1 (RULE store)
- Sprint 4 depende de Sprint 1 (RULE store)
- Sprint 5 depende de Sprint 1-2 (RULE + Activation Engine)
- Sprint 3 es independiente a partir de Sprint 1

---

## MÉTRICA DE ÉXITO

Antes: capitalización 2/10 (conocimiento documentado pero no aplicado automáticamente).

Después (target tras Sprint 2):

```
Prueba: "hazme un prompt creativo"
→ Activation Engine detecta task_type=creatividad
→ Activa RULE-001 → Gemma 4
→ Decision Engine recibe modelo forzado
→ Hermes responde usando Gemma sin que el usuario lo pida

Resultado esperado: la decisión de modelo es automática, no manual.
Medible: % de tareas donde se aplica RULE sin intervención del usuario.
```

---

## QUÉ NO SE INCLUYE (por ahora)

- **UI de gestión de RULE**: edición manual de YAML por ahora
- **ML para sugerir RULE**: solo derivación manual DEC→RULE
- **Rollback de activaciones**: si una RULE causa problemas, desactivar manualmente
- **Confidence decay con ML**: fórmula determinista simple en Sprint 4
