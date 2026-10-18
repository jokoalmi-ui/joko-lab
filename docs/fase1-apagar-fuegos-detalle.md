---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-30
---
# FASE 1 — APAGAR FUEGOS (detalle)

**Horas:** ~4h
**Estado:** PENDIENTE
**Regla:** no añadir componentes nuevos. Solo arreglar lo roto.

---

## 1.1 — Unificar fuente de verdad (30 min)

### Problema
`decision_router.py` tiene DOS fuentes de decisión:
1. `ROUTING_TABLE` hardcodeada en el código
2. `_integrate_lab_knowledge()` que consulta RAG

Si creas DEC-004 mañana, la tabla hardcodeada no la ve. Divergencia garantizada.

### Acción

**Archivo:** `tools/decision_router.py`

Eliminar `ROUTING_TABLE` y que TODO pase por RAG:

```python
# ANTES:
ROUTING_TABLE = {
    "creatividad": {"modelo": "gemma-4-12b", "razon": "DEC-003"},
    "json":       {"modelo": "granite-4.1-8b", "razon": "DEC-002"},
    ...
}

def decide(task_type):
    if task_type in ROUTING_TABLE:
        return ROUTING_TABLE[task_type]  # ← fuente 1
    return _integrate_lab_knowledge(task_type)  # ← fuente 2


# DESPUÉS:
def decide(task_type):
    return _integrate_lab_knowledge(task_type)  # ← única fuente
```

Si `_integrate_lab_knowledge()` no devuelve nada para ese task_type, loggear "sin decisión" y devolver modelo por defecto. No hardcodear.

### Verificación

```bash
python3 -c "
from tools.decision_router import decide
# Esto debe devolver resultado desde RAG, no desde tabla hardcodeada
r = decide('creatividad')
print(r)
assert 'ROUTING_TABLE' not in open('tools/decision_router.py').read(), 'ROUTING_TABLE aun existe'
print('OK: fuente unica')
"
```

---

## 1.2 — Formalizar OBS→HYP→EXP→DEC (30 min)

### Problema
Hay observaciones sueltas (OBS-001, OBS-002) pero no hay hipótesis formalizadas. El pipeline metodológico se salta pasos.

### Acción

**1. Crear directorio y plantilla:**

```bash
mkdir -p /home/jokoalmi/joko-lab/01-knowledge/hypotheses
```

Plantilla `01-knowledge/hypotheses/HYP-001-template.md`:

```markdown
# HYP-001: [título descriptivo]

**Origen:** OBS-XXX
**Fecha:** YYYY-MM-DD
**Estado:** [propuesta | validando | confirmada | descartada]

## Observación
¿Qué se observó?

## Hipótesis
¿Qué creemos que explica la observación?

## Predicción
Si la hipótesis es correcta, ¿qué debería pasar?

## Validación
- [ ] EXP-XXX diseñado
- [ ] EXP-XXX ejecutado
- [ ] Resultado: [confirma | refuta | inconcluso]

## Decisión derivada
- DEC-XXX (si confirmada)
```

**2. Crear HYP-001 (si hay material):**

Revisar OBS-001 (router dos fuentes) y OBS-002 (optimización cosmética). Si alguna justifica hipótesis, crearla. Si no, dejar la plantilla.

**3. Verificar estructura:**

```bash
ls /home/jokoalmi/joko-lab/01-knowledge/
# Debe mostrar: experiments/  hypotheses/  observations/  decisions/  models/  patterns/  rules/  policies/
```

### Verificación

```bash
ls /home/jokoalmi/joko-lab/01-knowledge/hypotheses/HYP-*.md 2>/dev/null | wc -l
# Debe ser >= 1 (al menos la plantilla)
```

---

## 1.3 — Evaluator contra modelo destino (1h)

### Problema
El Evaluator-Optimizer mide "parecido a la rúbrica", no "mejora real en la respuesta del modelo". Goodhart's Law: la métrica se convierte en el objetivo y se manipula.

La afirmación "el prompt mejoró de 16% a 83%" no está validada contra el modelo destino.

### Acción

**Archivo:** `tools/evaluator_optimizer.py`

La función `evaluate_response()` ya existe. Hay que usarla en un ciclo real:

```python
# Pseudocódigo de la verificación

# 1. Prompt original
original_prompt = "Escribe un poema sobre IA"
respuesta_original = llamar_modelo_destino(original_prompt)  # ej: Gemma 4

# 2. Prompt mejorado por E-O
mejorado = evaluator_optimizer.optimize(original_prompt)
respuesta_mejorada = llamar_modelo_destino(mejorado)

# 3. Comparar respuestas reales, no puntuaciones de rúbrica
comparacion = evaluate_response(original_prompt, mejorado, respuesta_original, respuesta_mejorada)
# Debe incluir: preservación de significado, mejora semántica real, no solo cambios cosméticos
```

Ejecutar con un script ad-hoc:

```bash
python3 -c "
from tools.evaluator_optimizer import EvaluatorOptimizer
eo = EvaluatorOptimizer()
result = eo.validate_against_model('Escribe un poema sobre IA', modelo='gemma-4-12b')
print(f'Score original: {result.score_original}')
print(f'Score mejorado: {result.score_mejorado}')
print(f'Delta real: {result.delta}')
print(f'Cambio cosmético: {result.cosmetic_only}')
"
```

Si `cosmetic_only == True`, el 83% es humo.

### Verificación

```bash
python3 tools/evaluator_optimizer.py --validate --model gemma-4-12b --prompt "Escribe un poema sobre IA"
# Debe mostrar comparación real, no solo rúbrica
```

---

## 1.4 — Sacar reglas a YAML (1h)

### Problema
`task_understanding.py` tiene `TASK_KEYWORDS` hardcodeado. `ROUTING_CACHE` en `decision_router.py` es un dict en memoria. Cualquier cambio requiere editar código Python.

### Acción

**Paso 1: Mover TASK_KEYWORDS a YAML**

Crear `01-knowledge/task_keywords.yaml`:

```yaml
# Mapeo de palabras clave → tipo de tarea
# Fuente única. Cargado por task_understanding.py al inicio.

creatividad:
  keywords: [creatividad, creativo, brainstorming, idea, inventa, imagina]
  tipo: creatividad

json:
  keywords: [json, estructurado, schema, formato, parse]
  tipo: json

codigo:
  keywords: [código, script, programa, función, clase, implementa, bug, test]
  tipo: codigo

analisis:
  keywords: [analiza, evalúa, compara, resume, explica, revisa]
  tipo: analisis

docker:
  keywords: [docker, contenedor, compose, imagen, puerto, volumen]
  tipo: docker
```

Modificar `task_understanding.py`:

```python
import yaml
from pathlib import Path

TASK_KEYWORDS_FILE = Path("~/joko-lab/01-knowledge/task_keywords.yaml").expanduser()

def load_task_keywords():
    with open(TASK_KEYWORDS_FILE) as f:
        return yaml.safe_load(f)

def detect_task_type(prompt: str) -> str:
    keywords_map = load_task_keywords()
    prompt_lower = prompt.lower()
    for task_name, config in keywords_map.items():
        for kw in config["keywords"]:
            if kw in prompt_lower:
                return config["tipo"]
    return "general"
```

**Paso 2: Eliminar ROUTING_CACHE hardcodeado**

`ROUTING_CACHE` en `decision_router.py` → alimentar siempre desde `_integrate_lab_knowledge()`. Sin caché manual.

### Verificación

```bash
python3 -c "
from tools.task_understanding import detect_task_type
# Añadir 'brainstorming' al YAML → debe detectarse como 'creatividad'
assert detect_task_type('hazme un brainstorming') == 'creatividad'
print('OK')
"
```

---

## 1.5 — Prompt Project automático (1h)

### Problema
Prompt Project solo se activa si Hermes "se acuerda". No hay activación automática al detectar "genera prompt para [modelo]".

Esto es exactamente el tipo de problema que el Activation Engine resolverá en Fase 3, pero necesita un parche ahora.

### Acción

**Archivo:** `tools/decision_engine.py` (o donde esté el pipeline de routing)

Añadir detección en el checklist de tarea tipo "prompt":

```python
# En TASK_CHECKLISTS["prompt"]["mandatory"], el paso prompt_project ya existe.
# Lo que falta es que el Decision Engine lo ejecute automáticamente.

def _check_mandatory_steps(task_type, context):
    checklist = TASK_CHECKLISTS.get(task_type, {})
    for step in checklist.get("mandatory", []):
        if step["id"] == "prompt_project":
            # Activar automáticamente si el prompt menciona un modelo
            if _detect_model_in_prompt(context.get("user_prompt", "")):
                result = _activate_prompt_project(context)
                context["prompt_project_active"] = True
                context["prompt_project_result"] = result
```

Donde `_detect_model_in_prompt` busca patrones como "genera prompt para Granite", "prompt para Gemma", etc.

### Verificación

```bash
python3 -c "
from tools.decision_engine import DecisionEngine
de = DecisionEngine()
result = de.decide('prompt', {'user_prompt': 'genera un prompt para granite 4.1'})
assert result.get('prompt_project_active') == True, 'Prompt Project no se activo'
print('OK: Prompt Project automatico')
"
```

---

## VERIFICACIÓN FINAL DE FASE 1

```bash
# Script de verificación consolidado
echo "=== F1.1: Fuente única ==="
grep -q "ROUTING_TABLE" tools/decision_router.py && echo "FAIL: ROUTING_TABLE existe" || echo "OK"

echo "=== F1.2: OBS→HYP→EXP→DEC ==="
ls 01-knowledge/hypotheses/ | grep -q "HYP" && echo "OK: hypotheses/" || echo "FAIL"

echo "=== F1.3: Evaluator real ==="
python3 -c "from tools.evaluator_optimizer import EvaluatorOptimizer; print('OK: importado')"

echo "=== F1.4: Reglas YAML ==="
python3 -c "from tools.task_understanding import load_task_keywords; d = load_task_keywords(); print(f'OK: {len(d)} tipos cargados')"

echo "=== F1.5: Prompt Project auto ==="
python3 -c "
from tools.decision_engine import DecisionEngine
de = DecisionEngine()
r = de.decide('prompt', {'user_prompt': 'genera prompt para granite'})
assert r.get('prompt_project_active', False), 'FAIL'
print('OK')
"
```
