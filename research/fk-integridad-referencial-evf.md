---
title: "FK-001 — Integridad referencial de Knowledge Objects (extensión de gate)"
type: EVF
---

# FK-001 — Integridad referencial (extensión SVP/KVC) — ficha EVF
**VERACIDAD:** [ALCANCE INTERNO]

**Estado:** ADOPTADO (07-ago, decision de Joseba): SVP extendido con comprobacion FK (estructurados + wikilinks bloquean; prosa avisa). Instrumento tools/verificar_fk_kos.py --gate (exit 1 si bloqueantes; verificado exit 0 sobre corpus).
**Fecha:** 07-ago-2026
**Origen:** MEL-2026-08-06-004 (clase de defecto `referencia_ko_no_verificada`) + state-verification-pattern.md (líneas 165-169): "evaluar si SVP/KVC deben extenderse con una comprobación de integridad referencial... No se implementa sin pasar por el EVF".

## Clase de defecto

`referencia_ko_no_verificada`: un ID de KO citado (en campos estructurados o en prosa) que no resuelve a un fichero real en 01-knowledge/objects/ (o observations//hypotheses/ para OBS/HYP). Caso real: DEC-004 citaba RULE-CONF-001, que no existe; lo detectó el revisor manual, no el gate (2/3 clases de defecto salieron del mecanismo; esta fue manual — brecha mecanismo vs revisor, cuantificada en MEL-3).

## Hipótesis

> **H-FK-001:** añadir una comprobación de integridad referencial (FK) a la revisión SVP/KVC reduce la clase de defecto `referencia_ko_no_verificada` sin generar falsos positivos inmanejables (menciones históricas o ejemplos de diseño).

## Instrumento (creado 07-ago, solo lectura)

`tools/verificar_fk_kos.py` — escanea KOs (campos estructurados dependencies/superseded_by/contradicts + prosa body/nota) y, con `--docs`, documentos (01-knowledge, lpa, research, GUIA). Regla FK: solo IDs con prefijo de KO (DEC/RULE/POLICY/PRED/PATTERN/OBS/HYP); OBS/HYP validan contra observations//hypotheses/; excluye .bak-*; distingue menciones históricas/ejemplos (aviso "revisar", no bloqueo).

## Baseline medido (07-ago, salida real)

- Solo KOs: 1 mención a revisar — DEC-004 body cita RULE-CONF-001, pero es la NOTA DE CORRECCIÓN del 06-ago (documenta que la referencia previa era incorrecta). No es defecto activo: es historia. El detector la marca y el revisor la clasifica.
- KOs + docs: 25 menciones, clasificables:
  - Históricas/diseño (no defecto): RULE-PROC-001..005 (reasoning-gate, reglas propuestas), RULE-MEL-001 (propuesta MEL), RULE-CONF-001 (state-verification-pattern, documenta el incidente), DEC-005/007/009 y PATTERN-002 (ejemplos en lpa/contracts/).
  - POTENCIALMENTE ROTAS (candidatas a defecto real): OBS-003 y OBS-004 citados sin archivo en observations/ (coinciden con los duplicados del backlog 04-ago, "pendientes de borrar con OK"); OBS-021 citado en OBSERVER-diseno sin archivo; HYP-002 citado en EXP-20260730-005/resultados.md sin archivo en hypotheses/.

## Estado tras la resolucion (07-ago)

Referencias rotas REALES resueltas (edicion a texto descriptivo, sin crear
archivos — Historical Integrity: OBS-003/004 eran anotaciones sin archivo,
retiradas como duplicados; OBS-021 era ejemplo de formato; HYP-002 era
mencion condicional "podria crearse"):
- 01-knowledge/jerarquia-autoridad.md (OBS-004 ejemplo -> texto descriptivo).
- 01-knowledge/experiments/EXP-20260730-005/resultados.md (OBS-003, OBS-004,
  HYP-002 -> texto descriptivo, 8 ediciones).
- lpa/meta/OBSERVER-telemetria-F1-F2-diseno-20260804.md (OBS-021 -> OBS-NNN).

Quedan SOLO menciones historicas o de diseno (no defecto activo):
- DEC-004 body cita RULE-CONF-001 (nota de correccion del 06-ago).
- RULE-PROC-001..005 y RULE-MEL-001 (reglas propuestas, reasoning-gate/MEL).
- DEC-005/007/009 y PATTERN-002 (ejemplos en lpa/contracts/).
- Esta propia ficha y GUIA-JOKO-LAB.md citan los IDs del incidente para
  documentarlo (trazabilidad, esperado).

Leccion para el gate: las menciones historicas y de diseno son el ruido
revisable; el diseno propuesto (campos estructurados y wikilinks bloquean,
prosa avisa) lo maneja sin falsos bloqueos.

## Resultado de la EXP (07-ago)

Registrada en evolution.jsonl (EXP-FK-001). El instrumento detecto 4 rotas
reales que el revisor manual no habia listado (OBS-003, OBS-004, OBS-021,
HYP-002) y clasifico el resto sin falsos bloqueos. DY positivo. Adopcion del
gate (extender SVP/KVC con FK, alcance: estructurados + wikilinks bloquean,
prosa avisa) queda como decision de Joseba; sin decision, el gate no cambia.

## Diseño del gate (a evaluar en la EXP)

- Alcance propuesto: (1) campos estructurados de KOs (dependencies, superseded_by, contradicts) — bloqueo si FK rota; (2) [[wikilinks]] explícitos a KOs en documentos — bloqueo si no resuelve; (3) menciones sueltas en prosa — aviso "revisar", no bloqueo (por el caso histórico DEC-004).
- Umbral de aviso: decidido con la distribución, nunca a priori.
- Integración: como paso del SVP (fase 2) o del KVC, no como gate nuevo (menos superficie; mismo principio del lab).

## Experimento (EXP-FK-001, propuesta)

1. Aplicar `verificar_fk_kos.py` al corpus completo y clasificar las 25 menciones (histórica / diseño / rota real).
2. Resolver las rotas reales candidatas (OBS-003/004: borrar referencias o crear archivos; OBS-021/HYP-002: crear o corregir) — con OK de Joseba.
3. Medir DY de la clase sobre N revisiones reales con el gate propuesto.
4. Criterios NO binarios:
   - ÉXITO: detecta ≥1 defecto real no histórico en la EXP, con falsos positivos revisables.
   - NEUTRO: solo menciones históricas/diseño (el defecto no reaparece → el gate es trámite).
   - NEGATIVO: falsos positivos inmanejables (menciones de diseño constantes) o el gate no añade valor → no adoptar.

## Ciclo

Diseño (esta ficha) → EXP-FK-001 → BENCHMARK PASS → ADOPTADO → RULE. El gate NO se toca antes de la EXP. Registro en evolution.jsonl cuando la EXP arranque.

## Decisiones pendientes de Joseba

1. Alcance del gate: solo KOs estructurados, o + wikilinks en docs.
2. Qué hacer con OBS-003/004 (borrar referencias o archivos) y OBS-021/HYP-002.
3. Si la EXP se ejecuta sobre el corpus histórico completo o sobre revisiones nuevas.
