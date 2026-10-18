---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-24
---
# Protocolo de Validación E0 → E1 para Candidate Patterns

**Versión:** 1.0
**Fecha:** 2026-07-24
**Propósito:** Definir criterios objetivos y reproducibles para elevar un Candidate Pattern de E0 (observación) a E1 (patrón confirmado).

---

## Requisitos para promoción E0 → E1

Un Candidate Pattern alcanza E1 cuando cumple **todos** los siguientes criterios:

### 1. Evidencia — Mínimo 3 instancias independientes

Las instancias deben cumplir:
- Provienen de al menos **2 dominios distintos** (según categorías LPA: A-G)
- Al menos **1 instancia es externa** a Joko Lab (evidencia de que el patrón no es idiosincrático)
- Las instancias están documentadas con: fecha, contexto, resultado observado

### 2. Falsación — Al menos 1 intento fallido de refutación

- Se ha diseñado un experimento específico para romper el patrón
- El experimento se ejecutó y el patrón **sobrevivió**
- O: se identificó una condición bajo la cual el patrón dejaría de ser cierto, y esa condición no se ha observado

### 3. Reproducibilidad — El patrón es ejecutable por otro

- El patrón está documentado como procedimiento, no solo como observación
- Una persona que no participó en el descubrimiento puede seguir el procedimiento y obtener un resultado equivalente
- No depende de conocimiento tácito del descubridor

### 4. Estabilidad — Sin contraejemplos activos

- No existe ninguna instancia documentada donde el patrón haya fallado sin explicación
- Si existe un contraejemplo, debe estar explicado (condición de borde, dominio no aplicable)

---

## Proceso de validación

```
Candidate Pattern (E0)
        │
        ▼
┌──────────────────────────────┐
│ 1. Acumular ≥ 3 instancias   │
│    - ≥ 2 dominios distintos  │
│    - ≥ 1 fuente externa      │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ 2. Diseñar experimento de    │
│    falsación                 │
│    - Ejecutar                │
│    - ¿Sobrevive? → continuar │
│    - ¿Cae? → descartar o     │
│      reformular              │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ 3. Test de reproducibilidad  │
│    - Documentar como         │
│      procedimiento           │
│    - ¿Otro puede ejecutarlo? │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ 4. Revisión de contraejemplos│
│    - ¿Hay fallos no          │
│      explicados?             │
└──────────────────────────────┘
        │
        ▼
   ┌─────────┐
   │   E1    │
   │ PATRÓN  │
   │CONFIRMADO│
   └─────────┘
```

---

## Ejemplo: CP-00X (Workflow como unidad de conocimiento)

| Criterio | Estado | Evidencia |
|---|---|---|
| ≥ 3 instancias | ✅ 5 instancias | GLM, KAP, Perfume IA, Procedures→Skills, Founders D2 |
| ≥ 2 dominios | ✅ 4 dominios | Diseño visual, extracción conocimiento, asimilación externa, producción publicitaria |
| ≥ 1 fuente externa | ✅ Founders D2 | We Make Studio — estudio profesional independiente |
| Falsación intentada | ❌ Pendiente | Elevar KAP a Workflow y medir si mejora o empeora |
| Reproducibilidad | ❌ Pendiente | KAP como workflow no ha sido ejecutado por otra persona |
| Sin contraejemplos | ✅ | Ninguno documentado |

**Estado:** CP-00X tiene evidencia observacional suficiente pero carece de validación experimental y test de reproducibilidad. No promociona a E1 hasta que ambos se completen.

---

## Diferencia clave

- **E0:** "Esto ha pasado varias veces. Parece un patrón."
- **E1:** "Hemos intentado romperlo y no hemos podido. Otra persona puede aplicarlo."
