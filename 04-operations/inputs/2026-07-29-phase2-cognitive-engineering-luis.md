---
type: operations
subtype: input
status: active
tags: [operations, input]
created: 2026-07-29
---
# Phase 2 — Cognitive Engineering

**Autor:** Luis (DeepSeek)
**Fecha:** 2026-07-29
**Contexto:** Respuesta a la evaluación de capacidades actuales de Joko Lab.
**Estado:** INPUT ESTRATÉGICO — Pendiente de asimilar y priorizar.

---

## Tesis central

> Añadir más componentes aporta menos valor que aumentar la calidad de las decisiones que toma el laboratorio.

El objetivo de la siguiente fase no es construir nuevas herramientas, sino conseguir que las herramientas **cooperen automáticamente**.

---

## Línea 1 — Convertir el conocimiento en comportamiento (Prioridad 1)

**Problema:** El laboratorio sabe mucho pero aplica poco. La capitalización automática está en 0%.

**Flujo actual:**
```
Usuario → Context Builder → Knowledge Resolver → Hermes recibe info → Hermes decide si usarla
```

**Flujo propuesto:**
```
Usuario → Task Understanding → Decision Engine → Aplicar reglas
  → bloquear FATAL
  → activar Prompt Project
  → seleccionar modelo
  → inyectar patrones
  → consultar decisiones
→ Hermes
```

El cambio clave: Hermes deja de decidir si consulta. El sistema le entrega el contexto correcto.

---

## Línea 2 — Crear un Knowledge Graph

**Estado actual:** Experimentos, Decisiones, OBS, Patrones, Anti-patrones, Modelos, Skills existen como documentos independientes.

**Propuesta:** Tratarlos como nodos relacionados.

Ejemplo:
```
Granite 4.1 → EXP-002 → DEC-003 → Pattern Large Creative → AntiPattern-07
```

La consulta deja de ser "busca Granite" y pasa a ser "dame todo el conocimiento relacionado con Granite".

---

## Línea 3 — Sustituir reglas por evidencia

**Problema:** Constantes fijas sin origen (80%, 5/6, TTL=1h, cos=0.2).

**Principio propuesto:** Toda constante debe tener un origen.

Ejemplo:
```yaml
threshold:
    value: 80
    origen: EXP-004
    confianza: E3
    revisable: true
```

Toda decisión del sistema debe ser auditable.

---

## Línea 4 — Medir decisiones, no respuestas

**Cambio de métrica:**
- Antes: ¿Ha respondido bien?
- Después: ¿Ha tomado la decisión correcta?

Árbol de decisión medible:
```
Usuario pide JSON → ¿Seleccionó Granite? → ¿Consultó DEC-003? → ¿Aplicó AntiPattern? → ¿Bloqueó FATAL? → Resultado
```

Permite detectar fallos antes de que lleguen a la respuesta final.

---

## Línea 5 — Banco permanente de regresión

**Estado actual:** 11 pruebas diseñadas como experimento.

**Propuesta:** Convertirlas en banco permanente:
```
tests/
  001-routing.md
  002-patterns.md
  003-rag.md
  004-evaluator.md
  ...
  050...
```

Comando: `python run_regression.py`

Salida esperada:
```
Routing: 47/47
Evaluator: 19/20
Knowledge: 18/18
Prompt Compiler: 15/17
TOTAL: 99/102
```

---

## La mejora única de mayor impacto

> **Crear un Decision Engine central.**

No un Router. No un Prompt Compiler. No otro patrón.

Un motor cuya responsabilidad sea:

```
Tengo este objetivo.
→ ¿Qué conocimiento aplica?
→ ¿Qué decisiones activas existen?
→ ¿Qué patrones obligatorios existen?
→ ¿Qué anti-patrones bloquean?
→ ¿Qué herramienta debo ejecutar?
→ ¿Qué evidencia he utilizado?
```

Todos los módulos deben preguntarle a él. No decidir por su cuenta.

---

## Relación con el estado actual de Joko Lab

| Propuesta | Estado actual | Brecha |
|-----------|---------------|--------|
| Decision Engine central | Existe DE en hermes-lab/decision-engine/ pero es solo router horario | Muy grande |
| Knowledge Graph | Nodos existen como documentos sueltos | No hay relaciones |
| Capitalización automática | Documentada en autoanalysis como 0% | Crítica |
| Reglas con origen | Constantes fijas en varios módulos | Media |
| Medición de decisiones | Solo se mide output | Alta |
| Banco de regresión | 11 tests experimentales | Convertir a permanentes |

---

## Notas de Hermes

Esto no es para ejecutar ahora. Es el mapa estratégico para la siguiente fase. 
Cuando se aborde, el orden debería ser:
1. Formalizar el banco de regresión (línea 5) — es la base para medir el progreso.
2. Atacar la capitalización automática (línea 1) — es el síntoma más crítico.
3. El Decision Engine central como integración de todo lo anterior.
