---
title: "Análisis — Fine-tune an LLM End-to-End"
type: research
---

# Análisis — Fine-tune an LLM End-to-End
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Fuente:** Post de hackproduct (Sandro Rodrigues Braga) en redes sociales
**Imagen:** `~/.hermes/image_cache/img_b092ce4c6ab9.jpg`

---

## Lo que muestra la infografía

Flujo completo de fine-tuning de un LLM:

```
CONVERSATIONS / BEHAVIOR / SAFETY  (¿qué quieres enseñar?)
        ↓
CLEAN → TEMPLATE → TOKENIZE → SPLIT
        ↓
FULL FINE-TUNE  vs  LoRA/QLoRA (Freeze base • Train adapter) ✅
        ↓
TRAIN BATCH → FROZEN BASE (LoRA A/B) → FORWARD PASS → LOSS → OPTIMIZER
        ↓
EVALUATE: QUALITY + SAFETY + REGISTRY
        ↓
PASSES GATES? → NO: FIX DATA | SÍ: VERSION → CANARY → MONITOR (rollback)
```

**Lema:** "Teach behavior, keep facts fresh" — fine-tune para COMPORTAMIENTO,
recupera conocimiento cambiante con RAG.

---

## Los 3 puntos clave

| Idea | Valor |
|---|---|
| **LoRA/QLoRA preferido** | Congela base, entrena adapter — el estándar para GPUs pequeñas |
| **Teach behavior, keep facts fresh** | Fine-tune = comportamiento; RAG = conocimiento |
| **Gates + canary + rollback** | Evaluación ANTES de desplegar, con despliegue gradual |

---

## Conexión con Joko Lab (estado real 04-ago)

| Concepto | Equivalente en el lab | Estado |
|---|---|---|
| LoRA/QLoRA | Dolphin Cyber LoRA (8B) | ✅ En uso |
| Frozen base + adapter | LM Studio con GGUF | ✅ |
| Evaluación con gates | Evidence Contract + certificación 11 tests | ✅ |
| Registry/versiones | KOs + git + .bak | ✅ |
| **Canary** | — | ❌ No existe (cambios directos) |
| **Monitor** | Monitor LM Studio :5000 (parcial) | ⚠️ Solo GPU |
| **Rollback** | JL-014 backup + git | ✅ Parcial |

**Hueco real detectado:** los pasos de CANARY + MONITOR + ROLLBACK para cambios
de políticas/scripts del lab. Hoy se aplican cambios directamente sin
despliegue gradual ni monitorización post-cambio.

---

## Qué nos valdría

1. **Validación:** LoRA/QLoRA es el camino correcto para RTX A2000 12GB.
2. **Confirmación arquitectónica:** "Teach behavior, keep facts fresh" = la
   arquitectura actual del lab (modelos locales para comportamiento + RAG para
   conocimiento). Valida la separación que ya tenemos.
3. **Gap a considerar:** proceso de "canary" para cambios de políticas del lab
   (aplicar a un subconjunto, observar, luego extender). Relacionado con
   Loop Engineering (L2) — el Gate del L2 podría incluir canary.

---

## Nota

Infografía de divulgación técnica. Conceptualmente sólida, alineada con la
práctica estándar de fine-tuning. No requiere implementación inmediata —
queda como referencia de arquitectura (junto a skill lm-studio y
ai-architecture) y como input para el diseño L2 (canary/monitor).
