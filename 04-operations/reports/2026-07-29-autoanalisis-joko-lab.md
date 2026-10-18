---
type: operations
subtype: report
status: active
tags: [operations, report]
created: 2026-07-29
---
# 2026 07 29 autoanalisis joko lab

AUTOANALISIS DE JOKO LAB — Usando el propio laboratorio
===========================================================
Fecha: 2026-07-29 (22:50 CEST)
Metodo: Context Builder → Knowledge Resolver → Evidence Collector
Pipeline ejecutado sobre query "puntos debiles joko lab"

──────────
1. CONTEXTO RECUPERADO (Context Builder)
──────────

Documentos encontrados por RAG:
  [1] README.md (cos: 0.170) — Documento raiz del laboratorio
  [2] Sesion 2026-07-16 (cos: 0.144) — Sesion historica

Confidence: 30% (⚠ corregido por cos < 0.2)

El Context Builder NO encontro documentos especificos sobre
debilidades porque las 12 observaciones (OBS-001 a OBS-012)
no estan indexadas como "debilidades" — son archivos .md en
01-knowledge/observations/ que el RAG no prioriza.

→ Esto es en si mismo un hallazgo: el RAG no encuentra sus
  propias observaciones porque no estan en el indice de
  busqueda semantica con suficiente peso.

──────────
2. CONOCIMIENTO SINTETIZADO (Knowledge Resolver)
──────────

Hechos confirmados (E3):
  - Los 5 patrones de agente estan implementados al 100%
  - El pipeline responde 83% mejor con RAG que sin el (+41%)
  - 11 pruebas de validacion: 43/66 (65%)
  - 4 bugs corregidos hoy (GATE fail-closed, confidence cos,
    keywords task_understanding)

Conflictos detectados:
  - Confidence badge: marcaba 100% ALTA con cos = -0.183
    (corregido hoy: maximo 30% si cos < 0.1)
  - Evaluator-Optimizer: acepta mejoras cosmeticas (Goodhart)
  - Prompt Project: no se activa automaticamente
  - Capitalizacion automatica: 0% — todo depende de memoria

Decisiones activas:
  - DEC-001: Qwen 3.5 descartado
  - DEC-002: DeepSeek R1 para razonamiento
  - DEC-003: Gemma 4 para creatividad

Hipotesis:
  - El laboratorio mejoraria +5-8% si se eliminan las
    dependencias manuales (Engineering Hardening)
  - La confianza deberia recalcularse con pesos: evidencia
    40% + actualidad 30% + consenso 20% + conflictos 10%

──────────
3. PUNTOS DE MEJORA (Evidence Collector)
──────────

Nivel de evidencia: E2 (hipotesis basada en 11 pruebas)

MEJORA 1 — Evaluator-Optimizer: Goodhart's Law
  Gravedad: ALTA
  Evidencia: Prueba 3 (1/6), Prueba 11 (diferencia +41%)
  Que pasa: Mide "parecido a rubrica", no "mejora real".
            Acepta cambios cosmeticos.
  Impacto estimado: +12% en precision de evaluacion
  Solucion: Anyadir check semantico de preservacion de
            significado + test contra modelo destino (OBS-005)
  Tiempo: 2h

MEJORA 2 — Confidence Badge: calculo enganoso
  Gravedad: ALTA
  Evidencia: Prueba 8 (3/6), OBS-010
  Que pasa: La confianza depende de cantidad de fuentes, no
            de calidad. Muestra ALTA con datos irrelevantes.
  Impacto estimado: +10% en fiabilidad del badge
  Solucion: Recalcular con pesos: relevancia (cos) 40% +
            actualidad 30% + consenso 20% + conflictos 10%
  Tiempo: 1h

MEJORA 3 — Prompt Project: no se auto-activa
  Gravedad: MEDIA
  Evidencia: Prueba 6 (3/6), Ejercicio 11 (0% capitalizacion)
  Que pasa: El formato Prompt Project existe pero depende de
            que Hermes "se acuerde" de usarlo.
  Impacto estimado: +8% en trazabilidad de prompts
  Solucion: Auto-trigger en task_understanding.py al detectar
            "genera prompt para [modelo]"
  Tiempo: 1h

MEJORA 4 — Capitalizacion: 0% automatica
  Gravedad: CRITICA
  Evidencia: Ejercicio 11 (0/6), 5 decisiones dependen de memoria
  Que pasa: El conocimiento existe pero NADA se aplica sin
            intervencion manual. El router recomienda pero no
            ejecuta. Los anti-patrones se consultan pero no
            bloquean. El Prompt Project se conoce pero no se activa.
  Impacto estimado: +15% en autonomia del laboratorio
  Solucion: Engineering Hardening — 4 niveles, ~6.5h
  Tiempo: 6.5h (planificado en engineering-hardening-plan.md)

MEJORA 5 — Observaciones no indexadas
  Gravedad: BAJA
  Evidencia: Este mismo autoanalisis — el RAG no encontro las
            12 OBS porque son archivos nuevos no indexados
  Que pasa: El watchdog re-indexa cada 15s, pero las OBS se
            crearon despues del ultimo ciclo de indexacion
  Impacto estimado: +3% en cobertura de busqueda
  Solucion: Forzar re-indexacion tras crear OBS nuevas
  Tiempo: 15 min

──────────
4. RESUMEN (Decision Router)
──────────

┌─────┬──────────────────────────┬──────────┬────────┐
│  #  │ Mejora                    │ Gravedad │ Tiempo │
├─────┼──────────────────────────┼──────────┼────────┤
│  1  │ Goodhart en Evaluator     │ ALTA     │ 2h     │
│  2  │ Confidence mal calculado  │ ALTA     │ 1h     │
│  3  │ Prompt Project manual     │ MEDIA    │ 1h     │
│  4  │ Capitalizacion 0%         │ CRITICA  │ 6.5h   │
│  5  │ Observaciones no indexad. │ BAJA     │ 15min  │
├─────┼──────────────────────────┼──────────┼────────┤
│     │ TOTAL                     │          │ 10.75h │
└─────┴──────────────────────────┴──────────┴────────┘

Orden recomendado: 1→2→3→5→4 (por impacto/esfuerzo)

──────────
5. VEREDICTO (Evidence Collector)
──────────

El laboratorio se auto-diagnostico usando 3 de sus 7 herramientas
(Context Builder, Knowledge Resolver, Evidence Collector).
NO uso: Decision Router, Evaluator-Optimizer, Preflight Checklist,
ni Blackboard Orchestrator.

De las 5 mejoras detectadas, 4 ya estaban documentadas (OBS-005,
OBS-010, Ejercicio 11, Engineering Hardening). Solo 1 es nueva
(observaciones no indexadas).

Esto confirma que el laboratorio:
  ✅ Sabe detectar sus propias debilidades
  ✅ Las tiene documentadas (OBS, validacion, hardening)
  ❌ No las aplica automaticamente (capitalizacion 0%)
  ❌ No usa todas sus herramientas en el autoanalisis

El autoanalisis es valido pero INCOMPLETO: 3/7 herramientas
utilizadas. Las 4 restantes (Router, E-O, Preflight, Blackboard)
no se activaron porque el pipeline no las disparo automaticamente.

Eso es, en si mismo, la mejora mas importante.

═══════════════════════════════════════════
FIN DEL AUTOANALISIS
═══════════════════════════════════════════

## Conexiones

- [[2026-07-31-backlog]] — backlog 2026-07-31: priorización derivada del autoanálisis
- [[GUIA-JOKO-LAB]] — GUIA-JOKO-LAB: mapa del lab analizado
