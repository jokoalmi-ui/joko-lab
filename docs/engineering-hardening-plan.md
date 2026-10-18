---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-29
---
# Engineering hardening plan

ENGINEERING HARDENING — Fase 5 de Joko Lab
=============================================
Fecha: 2026-07-29
Estado: PLAN DE ACCION
Origen: Analisis de las 11 pruebas de validacion (resultado: 43/66)

═══════════════════════════════════════════
DIAGNOSTICO
═══════════════════════════════════════════

Las 11 pruebas revelaron que los fallos NO son aleatorios.
Son exactamente 3 zonas donde el conocimiento no gobierna
el comportamiento:

1. Evaluator-Optimizer: Mide "parecido a la rubrica" en vez de
   "mejora real". Goodhart's Law. Acepta cambios cosmeticos.

2. Prompt Project: No se activa automaticamente. Depende de
   que Hermes "se acuerde" de usarlo.

3. Confidence Badge: Marca ALTA con datos irrelevantes (cos
   negativo). La confianza depende de cantidad, no de calidad.

CONCLUSION: El laboratorio YA funciona. Pero todavia hay
procesos que dependen de "Hermes recuerda..." en vez de
"el sistema decide".

═══════════════════════════════════════════
PLAN: 4 NIVELES DE ENDURECIMIENTO
═══════════════════════════════════════════

NIVEL 1 — Eliminar "Hermes recuerda..."
  [ ] Todo conocimiento debe venir de RAG, Decision Memory,
      Pattern Library o Model Cards.
  [ ] Ninguna decision basada en memoria del modelo.
  [ ] Evaluator: anyadir check semantico de preservacion de
      significado (OBS-005)
  [ ] Prompt Project: activacion automatica al detectar
      "genera prompt para [modelo]"
  [ ] Tiempo estimado: 2h

NIVEL 2 — Eliminar reglas hardcodeadas
  [ ] Mover reglas restantes de codigo a YAML/config
  [ ] ROUTING_CACHE en decision_router.py → alimentar desde RAG
  [ ] TASK_KEYWORDS en task_understanding.py → YAML externo
  [ ] Tiempo estimado: 1h

NIVEL 3 — Eliminar duplicidades
  [ ] Routing Table + Decision Memory → unica fuente (RAG)
  [ ] Dos confidence badges distintos → unificar calculo
  [ ] Metricas en 7 archivos → store.jsonl unificado
  [ ] Tiempo estimado: 1.5h

NIVEL 4 — Cada componente responde 4 preguntas
  [ ] ¿Que sabe?
  [ ] ¿De donde lo sabe?
  [ ] ¿Que decision toma?
  [ ] ¿Como demuestra que era correcta?
  [ ] Implementar como wrapper en confidence.py
  [ ] Tiempo estimado: 2h

═══════════════════════════════════════════
METRICA DE EXITO
═══════════════════════════════════════════

Antes (prueba 11): sin RAG 42% → con RAG 83% (+41%)
Objetivo post-hardening: sin RAG 42% → con RAG 90%+ (+48%)

Si el endurecimiento NO mueve ese numero, no sirvio.

═══════════════════════════════════════════
NO HACER
═══════════════════════════════════════════

- No anyadir nuevos componentes
- No disenyar nuevos patrones
- No crear nuevas herramientas
- Solo eliminar dependencias manuales y consolidar

═══════════════════════════════════════════
FIN
═══════════════════════════════════════════
