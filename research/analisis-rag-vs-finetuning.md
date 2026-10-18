---
title: "Análisis — RAG vs LoRA vs Full Fine-Tuning (HackProduct, 13s)"
type: research
---

# Análisis — RAG vs LoRA vs Full Fine-Tuning (HackProduct, 13s)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 11-ago-2026
**Fuente:** https://www.instagram.com/reel/Db4migNOCjg/ — hackproduct
**Método:** Descarga MP4 (13s) + 7 frames + GLM
**Tiempo:** ~3 min total

---

## El contenido — "RAG in one frame" (3 formas de adaptar un LLM)

El reel es un **diagrama comparativo** de las 3 vías para especializar un LLM:

### 1. RAG (Add context, keep weights)
**Etapas:** QUERY → RETRIEVE VECTOR DB → CONTEXT TOP-K CHUNKS → LLM (mismos pesos) → ANSWER GROUNDED
**Mejor para:** conocimiento FRESCO, PRIVADO, CITABLE (con fuentes)

### 2. LoRA Fine-Tuning (Train adapter, freeze base)
**Etapas:** EJEMPLOS (tarea/estilo) → BASE FROZEN → LoRA ΔW pequeño → BASE+LoRA servidos juntos → OUTPUT ADAPTADO
**Mejor para:** adaptación de TAREA, ESTILO, FORMATO a bajo coste

### 3. Full Fine-Tuning (Unlock base, update all weights)
**Etapas:** DATOS DE ENTRENAMIENTO (grandes) → BASE UNLOCKED → TODOS los pesos actualizados → MODELO NUEVO especializado → OUTPUT con control máximo
**Mejor para:** especialización profunda

---

## 🎯 Aplicación al LAB — VALIDA EL ESTUDIO DE FINE-TUNING (05-ago)

**El lab ya llegó a esta conclusión** (research/analisis-finetuning-*.md):

| Vía | Lab | Estado |
|---|---|---|
| **RAG** | ✅ **Lo usa** (LanceDB + BGE-M3 + reranker) — "mejor para conocimiento fresco/privado/citable" | Operativo |
| **LoRA** | 🟡 Estudiado — "cuando prompting+RAG no basten" | Futurible |
| **Full FT** | ❌ Descartado — requiere GPU hours | No viable A2000 |

### El diagrama confirma el criterio de decisión del lab:
> **RAG para conocimiento · LoRA para estilo/tarea · Full FT para especialización**
El lab eligió correctamente: RAG como base (ya operativo), LoRA como siguiente paso lógico cuando haya un caso (post-i9-9900K), Full FT fuera del alcance.

### 🟡 Lo aprovechable
- El criterio "ADD CONTEXT vs TRAIN ADAPTER vs UNLOCK BASE" es un buen **checklist de decisión** para cuando Joseba se pregunte "¿RAG o fine-tuning?" (ya documentado, pero el frame lo resume visualmente).

### Conclusión
**VALIDACIÓN directa del estudio de fine-tuning del lab (05-ago).** El reel no
aporta nada nuevo técnicamente, pero es el resumen visual perfecto del
criterio de decisión que el lab ya adoptó. Guardado como referencia.

## Nota técnica
- 7 frames en ~3 min (paralelo)
- GLM capturó las 3 vías correctamente (frame_3 = el más completo)
- Los frames 1,2,4 quedaron en reasoning (GLM razonando en voz alta)
