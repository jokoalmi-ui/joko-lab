---
title: "EXP-HEL-001 — Fase 2: diseño de la mejora del instrumento"
type: research
fecha: 2026-08-14
estado: implementado (C1+C2+C3, 14-ago-2026)
---

# EXP-HEL-001 — Fase 2: diseño de la mejora del instrumento
**VERACIDAD:** [ALCANCE INTERNO]

## Contexto

El corte de la fase observacional (04-operations/reports/2026-08-14-exp-hel-001-corte.md)
cerró con: baseline que discrimina (tasa de memoria entre genuinas 6.7%,
concentrada en la familia "¿cuánto queda / qué hay urgente?"), H-HEL-001
sostenida, y tres defectos del instrumento que impiden medir la fase 2 con
rigor. Este documento diseña la mejora del instrumento ANTES de medir la
activación deliberada. Es diseño, no implementación: nada de esto se ejecuta
sin OK (freeze + EVF).

## Defectos del instrumento a resolver (del corte)

1. `declarada_true_fijo`: tools/registrar_hel_diario.py escribe
   activacion_declarada=True SIEMPRE (línea 107). El ratio
   declarada/verificada no es medible; todo el peso cae en la verificación.
2. `ruido_detector`: 38/103 entradas (37%) son ruido (afirmaciones,
   instrucciones, temas no-lab: perfumes, entreno, bolsa, Instagram,
   infografías). Exige clasificación manual para no diluir métricas.
3. `verificacion_no_automatizada`: activacion_verificada queda null hasta
   un corte manual; 5 entradas no matchearon por timestamp.

## Diseño (3 cambios)

### C1 — Registro del universo completo y métrica primaria = verificada

- El detector registra TODAS las preguntas de estado que pasan keywords
  (ya lo hace), pero el campo declarada deja de escribirse como true fijo.
- Propuesta: eliminar `activacion_declarada` como métrica (el lab ya tiene
  la lección: auto-reporte ≠ métrica, KVC-001) y dejar como métrica
  primaria `activacion_verificada` (evidencia de ejecución real).
- Si se quiere el ratio declarado/verificado textual, definirlo aparte:
  declarada = ¿el texto del primer assistant message ANUNCIA consulta
  ("voy a revisar", "déjame consultar", "compruebo", "miro el estado")?
  Extraíble por regex, opcional, no bloqueante. Recomendación: NO medirla
  en fase 2 — la señal relevante es la ejecución real, no la intención.

### C2 — Filtro de ruido con golden set del corte

- Las 38 descripciones marcadas ruido en el corte forman el golden set de
  referencia (quedan en respuestas_hel.jsonl con clasificacion=ruido).
- Añadir a RUIDO de registrar_hel_diario.py los patrones que las cubren,
  p.ej.: "^ok reinicio", "si con lo más urgente", "entonces no queda nada",
  "estado de la marea", "entreno", "sorteo", "perfume", "bolsa",
  "carrusel", "notebooklm", "slides", "infograf", "gin tonic",
  "a la disciplina", "material aprovechable", "chuncless", "vamos con ello",
  "coordinar sesiones", "multi-agente" (pregunta conceptual), "anota como
  norma", "analiza el formato", "independientemente de que valor",
  "en 0.3", "analiza y anota", "pregunta inversa", "que aportaria",
  "la tienes ya en lms studio", "como definirias", "de todas maneras en
  casa slide", "coge la guia", "se ha quedado muy corto", "te doy a dejar
  los datos", "he creado un directorio llamado USAGE", "pasame esto",
  "si comprueba", "si y deja pendiente", "al tope segun hardware".
- Test de aceptación del filtro: reprocesar el golden set con el detector
  modificado → 0 capturas de las 38; y reprocesar el corpus del 07-13 →
  la tasa de ruido baja de 37% a <10%.

### C3 — Verificación automática

- Script tools/verificar_hel.py (solo lectura): replica el verifier usado
  en el corte (cargar sesiones de 04-operations/metrics/sesiones, matchear
  por id de sesión + timestamp ±180s, primera respuesta assistant con
  tool_calls → true/false) y rellena activacion_verificada + evidencia en
  las entradas con null.
- Uso: bajo demanda antes de cada corte, o cron diario (22:36, tras el
  detector). Con backup del ledger antes de escribir (RULE-008).
- Casos no matcheables (sin user message en rango): se dejan null y se
  listan para revisión manual (5 en el corte actual, todas ruido/dudosas).

## Criterio de éxito falsable de la fase 2 (intervención)

- Intervención ÚNICA: activación deliberada — cuando la pregunta es de
  estado, forzar la consulta de fuentes antes de responder (RULE-PROC-005 /
  State Question Detector ya diseñado; sin cambiar el tipo de pregunta).
- Objetivo: familia "¿cuánto queda / qué hay urgente?" responde 0 veces de
  memoria en 14 días; O tasa global de memoria entre genuinas < 6.7% con
  N ≥ 60. Decisión por EVF al cierre (DY + coste + adopción).
- Control del matiz del corte (10.8% → 0.0%): comparar las MISMAS familias
  de pregunta antes/después; no basta con la tasa global.
- Umbrales derivados de la distribución (nunca a priori); sin ToT/GoT/
  scratchpad/controller/debate en la intervención (contaminarían).

## Alcance

Diseño cerrado 14-ago-2026. Implementación pendiente de OK (C1+C2+C3 como
una sola tanda, con tests del golden set, antes de arrancar la medición de
fase 2).

## Implementación (14-ago-2026, OK del usuario)

- C1: `tools/registrar_hel_diario.py` — `activacion_declarada` deja de
  escribirse como true fijo; nuevas entradas con valor null y comentario
  (auto-reporte != métrica, KVC-001). Backup: `.bak-20260814`.
- C2: patrones de ruido del golden set añadidos a RUIDO, ajustados al TEXTO
  REAL del ledger (tildes, mayúsculas, casos no listados en el diseño).
  El patrón `perfume` genérico se descartó: rompía 2 genuinas
  ("clasificación de cada perfume"); se sustituyó por `depende de que
  perfume sea` (el caso de sorteo queda cubierto por `sorteo`).
  `es_ruido` pasa a `re.IGNORECASE`.
  TEST DE ACEPTACIÓN: 0 capturas de las 38 ruido del golden set (pasado);
  las 4 genuinas que el detector no detecta son las de registro manual de
  la sesión gobernanza 07-ago (nunca pasaron keywords; sin regresión).
- C3: `tools/verificar_hel.py` creado (solo lectura, backup automático del
  ledger RULE-008). Reproduce el verifier manual del corte: id de sesión del
  contexto + timestamp ±180s + PRIMERA respuesta assistant con tool_calls.
  VALIDADO contra una entrada de referencia del corte (True, "tools: terminal").
  Las 5 entradas sin matchear del corte (99-103) se quedan null y se listan
  (3 ruido + 2 dudosas, no afectan a métricas), tal como diseñado.
- Futuribles NO abiertos (freeze, dependen de resultados fase 2): ToT, GoT,
  scratchpad, Strategy Controller, self-consistency, ReAct. Ver backlog
  2026-08-14.
- Siguiente paso: medición fase 2 (activación deliberada, RULE-PROC-005 /
  State Question Detector) tras el primer corte con el instrumento nuevo;
  decisión EVF al cierre.
