---
title: "KO formato PATRON — Extensión del esquema (WHEN/TEMPLATE/PITFALLS/CLASSICS)"
type: lpa
---

# KO formato PATRON — Extensión del esquema (WHEN/TEMPLATE/PITFALLS/CLASSICS)

**Estado:** PROPUESTA de diseño — 2026-08-04
**Origen:** Idea 1 del análisis del "50 Coding Patterns Handbook" (codedsoul_05),
entregado por el gateway de Telegram (20/20 páginas).
**Base:** `lpa/contracts/knowledge-object-schema.md` (v1, sin implementar).

## 1. Principio

El tipo `PATTERN` ya existe en el esquema. Esta extensión le da un cuerpo
ESTÁNDAR de 4 campos, copiado del formato del handbook (WHEN/TEMPLATE/
PITFALLS/CLASSICS), que es exactamente el formato que hace reutilizable un
patrón: cuándo se aplica, cómo, qué errores tiene y dónde se ha visto.

## 2. Extensión (bloque `patron:`, SOLO para type: PATTERN)

```yaml
type: PATTERN
id: PATTERN-0XX
status: activo
# ... (campos base del esquema: version, created, last_validated,
#      next_review, expires, confidence, confidence_label, evidence,
#      dependencies, contradicts, superseded_by, domain, scope,
#      monitoring, history) ...

patron:
  cuando: "Condiciones de disparo: ¿cuándo se aplica este patrón?"
  plantilla: "Esqueleto reutilizable: estructura, código o pasos concretos."
  trampas: "Errores conocidos al aplicarlo (con wikilink [[KO]]/[[EXP]] si hay)."
  clasicos: "Casos reales del lab donde se aplicó (wikilinks)."

body: >
  Descripción corta del patrón y su propósito.
```

## 3. Reglas de diseño

1. **Solo PATTERN.** DEC/RULE/POLICY/EXP/OBS no cambian. Cero ruido en los
   KOs existentes.
2. **Opcionales hasta la promoción.** Un PATTERN puede nacer sin bloque
   (hipótesis). Al pasar a `activo`, se completa el bloque (regla alineada
   con el Evidence Contract: la promoción exige evidencia + forma completa).
3. **`plantilla` verificable.** Debe ser ejecutable o comprobable de forma
   determinista (regla de oro del lab, misma que en PRED: si no puedes
   imaginar cómo verificarlo, reformúlalo).
4. **`trampas` y `clasicos` referencian.** Usar wikilinks [[KO]]/[[EXP]] para
   que el grafo (23 docs, 43 aristas) los conecte y el RAG los recupere.
5. **No romper nada:** el schema base y los 17 KOs actuales quedan intactos.
   Es adición, no sustitución.

## 4. Ejemplo real listo para usar (cuando se apruebe)

```yaml
type: PATTERN
id: PATTERN-001
status: propuesto
version: 1
created: 2026-08-04
last_validated: null
next_review: 2026-11-04
expires: 2027-02-04
confidence: null
confidence_label: SIN_LABEL
evidence:
  - EXP-20260804-VIGENCIA-OKF
dependencies: []
contradicts: []
superseded_by: null
domain: ai-architecture
scope: todo_joko_lab
monitoring:
  metric: precision
  baseline: null
  current: null
  last_checked: null
history:
  - date: 2026-08-04
    event: created

patron:
  cuando: >
    El RAG recupera conocimiento gobernado (DEC/RULE/POLICY) y hay riesgo de
    que un documento viejo gane por volumen a uno vigente. Disparo: cualquier
    consulta que toque decisiones, reglas o políticas del lab.
  plantilla: >
    1. Generar indice-okf.md con tools/generar_indice_okf.py (17 KOs,
    ~800 tokens, con expires/superseded_by/status).
    2. Inyectar bloque [Indice de conocimiento (vigencia)] en context_builder
    cuando detect_type no este vacio.
    3. El LLM recibe que existe y que esta vigente ANTES del retrieval.
  trampas: >
    - Usar body completo en el indice lo infla (2334 -> 800 tokens al
    truncar a 160 chars). [[RULE-008]]
    - Sin superseded reales el indice no discrimina aciertos (H1 no
    falsable, EXP-20260804-VIGENCIA-OKF). [[DEC-001]]
  clasicos:
    - EXP-20260804-VIGENCIA-OKF (3/3 con y sin indice; robustez de nombre
      canonico: "DeepSeek R1" vs "deepseek-r1-distill-qwen-14b").

body: >
  Patron de retrieval con vigencia: un indice compacto de Knowledge Objects
  con su estado (expires/superseded/status) se inyecta al contexto para que
  el LLM sepa que existe y que esta vigente, sin depender del reranker.
```

## 5. Aprobación pendiente

- [ ] Joseba aprueba la extension (o ajusta campos)
- [ ] Si se aprueba: crear PATTERN-001 real en 01-knowledge/objects/
- [ ] Cuando se implemente el schema v1, integrar el bloque en el contrato
