---
title: "MEL-3 — Metacognición Arquitectónica (medir el LAB como organismo)"
type: research
---

# MEL-3 — Metacognición Arquitectónica (medir el LAB como organismo)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 06-ago-2026
**Estado:** PRIMER CORTE REAL (datos del día) + diseño de métricas. Sin implementación de infraestructura nueva: usa los registros existentes (evolution.jsonl, mel_ledger.jsonl, svp_exp.jsonl, kvc_exp.jsonl).
**Marco:** EVF Nivel 4 (MEL Metrics). Complementa MEL-1 (decisión) y MEL-2 (procedimiento).

---

## 1. Qué responde

MEL-3 no mide una decisión (MEL-1) ni un procedimiento (MEL-2). Mide el LAB como organismo: qué evoluciones producen valor, qué gates apenas detectan nada, qué componentes consumen y no aportan.

Preguntas que responde:
- ¿Qué evolución produjo más reducción de errores?
- ¿Qué gate apenas detecta nada?
- ¿Qué componente consume mucho y aporta poco?
- ¿Qué procedimiento nunca genera defectos?
- ¿Qué capa tiene peor Detection Yield?

## 2. Métricas MEL-3 (definición)

| Métrica | Definición | Fuente de datos |
|---|---|---|
| Gates adoptados / total | % del mapa de gates con EVF completo | ecosistema-gobernanza.md |
| DY por gate | clases únicas / ítems revisados (definición EVF) | evolution.jsonl |
| Clases de defecto por gate | qué clases descubrió cada gate | evolution.jsonl + mel_ledger |
| Tasa de instancias | instancias de defecto / ítems revisados | svp_exp.jsonl + kvc_exp.jsonl |
| Integridad epistemológica | % de KOs evaluables | mel_ledger (MEL-Integrity) |
| Hallazgos manuales vs gate | defectos detectados por el mecanismo vs por el revisor | mel_ledger (origen del hallazgo) |
| Componentes sin valor | diseñados/implementados que no producen datos | evolución sin EXP |

## 3. PRIMER CORTE REAL (06-ago-2026, datos verificados)

| Métrica | Valor | Lectura honesta |
|---|---|---|
| Gates adoptados | 2/5 (40%) | SVP y KVC con EVF completo; KCR diseñado sin EXP; 002/004 de facto |
| DY por gate | SVP 0,10 · KVC 0,25 | NO comparables entre sí (ver advertencia EVF); ambos encontraron 1 clase única |
| Clases de defecto totales | 3 | missing_state_sources, missing_confidence, referencia_ko_no_verificada |
| Tasa de instancias | 8/15 = 0,53 | 5 (SVP) + 2 (KVC) + 1 (referencia KO, manual) / 15 ítems |
| Integridad epistemológica | 100% | 4/4 DECs evaluables tras DEC-004 (antes 50%) |
| Hallazgos por mecanismo | 2 de 3 clases | missing_state_sources y missing_confidence salieron del gate; referencia_ko_no_verificada fue manual (hueco del gate, capturado) |
| Componentes sin valor | KCR-001 | Diseñado, sin EXP — ni consume ni aporta datos aún (no es fallo: está en fase de diseño) |
| Coste total de la gobernanza | bajo | Sin infraestructura nueva; solo registros JSONL + documentos |

## 4. Hallazgos del primer corte

1. **El gate detecta, pero no todo:** 2/3 clases de defecto salieron del mecanismo; la tercera (referencia_ko_no_verificada) fue manual. MEL-3 cuantifica por primera vez la brecha entre "mecanismo" y "revisor".
2. **DY bajo no significa gate inútil:** ambos gates encontraron exactamente 1 clase única. El DY distinto (0,10 vs 0,25) refleja el denominador, no el rendimiento. La tasa de instancias (0,53) es la métrica más informativa: más de la mitad de los ítems revisados hoy tenían un defecto real.
3. **La gobernanza costó poco:** el ciclo completo (2 EXP + 3 informes + 5 documentos + 4 ledgers) no requirió infraestructura nueva: reutilizó JSONL y markdown. El coste dominante es tiempo de revisión, no medido aún.
4. **KCR sigue siendo el riesgo mayor:** la vigencia aún no participa en retrieval. MEL-3 lo confirma como componente sin datos.

## 5. Siguiente paso

El primer corte es una fotografía del día 1. Para que MEL-3 sea longitudinal hace falta:
- Medir tras cada nueva EXP (KCR-001 será la 3ª fotografía)
- Registrar tiempo de revisión (el gap actual: tiempo_s null)
- Decidir si la PIL (Process Integrity Layer) se formaliza como métrica MEL-3 o como capa propia

Sin implementación de infraestructura nueva: MEL-3 se alimenta de los registros existentes.
