---
title: "Diseño de Implantación — Loop Engineering (L2)"
type: research
---

# Diseño de Implantación — Loop Engineering (L2)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Estado:** DECIDIDO — F1-F2 + Baseline como proyecto independiente (entregable: hechos, no conclusiones). F3-F6 BLOQUEADOS hasta que exista evidencia del comportamiento real del ledger. Decisión de Joseba (04-ago): no construir un mecanismo adaptativo antes de tener datos que justifiquen su comportamiento.
**Origen:** `research/runtime-feedback-loop.md` — pregunta L2: ¿el ciclo debe ser
automático o requiere intervención humana?

---

## 1. Definición operativa

**Loop Engineering (L2)** = el sistema observa sus propias decisiones, acumula
evidencia de resultados, y **propone ajustes de reglas** cuando la evidencia
supera umbrales. La DECISIÓN final siempre requiere validación humana (JL-012
preservado). L2 NO es auto-corrección ciega — es auto-DETECCIÓN + propuesta
con gobernanza.

**Principio rector:** el sistema nunca cambia una regla solo. Detecta,
acumula evidencia, formula la hipótesis de cambio y la presenta. El humano
decide. Esto responde a la pregunta 1 y 2 del doc origen.

---

## 2. Arquitectura (sobre componentes existentes)

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPONENTES NUEVOS (L2)                  │
│                                                             │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │ 1. OBSERVER │→  │ 2. EVIDENCIA │→  │ 3. PROPOSER      │  │
│  │  lee ledger │   │  agrega por  │   │  genera hipótesis │  │
│  │  + resultados│  │  regla/umbral│   │  de cambio (draft)│  │
│  └─────────────┘   └──────────────┘   └──────────────────┘  │
│        ↓                    ↓                    ↓          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 4. GATE (evidence_contract.py) — ¿la evidencia       │   │
│  │    supera el mínimo del contrato?                    │   │
│  └──────────────────────────────────────────────────────┘   │
│        ↓ (solo si GATE pasa)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 5. PROPUESTA — archivo YAML en proposals/ +          │   │
│  │    aviso a Joseba (Telegram)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
        ↓ (Joseba aprueba / rechaza / modifica)
┌─────────────────────────────────────────────────────────────┐
│  COMPONENTES EXISTENTES (sin cambios)                       │
│  - apply-decision.sh / Runtime.resolve()                    │
│  - policies/*.yaml (la propuesta modificaría ESTOS)         │
│  - decision-ledger.jsonl (ya acumula evidencia)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Componentes nuevos (4 módulos)

### Módulo 1 — Observer (observación)
**Archivo:** `hermes-lab/loop-engineering/observer.py`

| Campo | Detalle |
|---|---|
| **Entrada** | `decision-ledger.jsonl` (326 entradas ya) + `state.json` + logs |
| **Qué observa** | Decisiones tomadas, proveedor/modelo elegido, motivo, resultado |
| **Frecuencia** | Cron cada 30 min (con el DE) o bajo demanda |
| **Salida** | Ventana de observación: decisiones por regla en las últimas N horas |

**Pregunta clave que responde:** ¿qué regla está decidiendo más? ¿Alguna regla
domina de forma anómala (p.ej. `horario` decidió 90% de las veces)?

### Módulo 2 — Evidence Aggregator (acumulación)
**Archivo:** `hermes-lab/loop-engineering/evidence.py`

| Campo | Detalle |
|---|---|
| **Entrada** | Salida del Observer |
| **Qué hace** | Agrupa por regla, cuenta frecuencias, detecta patrones |
| **Métricas** | N decisiones por regla, % de uso, tendencia temporal |
| **Umbral de interés** | ⚠️ NO DEFINIDO a priori (decisión 04-ago). El "70%" del diseño original es un EJEMPLO, no un parámetro. Primero obtener la distribución real; el umbral se decide con los datos. |
| **Salida** | `evidence-summary.json` con métricas por regla |

**Pregunta clave:** ¿qué regla está "ganando" de forma desproporcionada? Eso
puede indicar que el umbral está mal calibrado.

### Módulo 3 — Proposer (formulación de hipótesis)
**Archivo:** `hermes-lab/loop-engineering/proposer.py`

| Campo | Detalle |
|---|---|
| **Entrada** | evidence-summary.json |
| **Qué hace** | Formula hipótesis de cambio: "La regla X decide Y% — ¿ajustar umbral?" |
| **Formato** | Propuesta en YAML (draft de cambio a la política) |
| **Plantillas** | 3 tipos: ajustar umbral, añadir regla, eliminar regla muerta |
| **Salida** | `proposals/` (archivos YAML pendientes de revisión) |

**Pregunta clave:** dado el patrón observado, ¿qué cambio concreto mejoraría la
decisión? El Proposer NO cambia nada — solo redacta la propuesta.

### Módulo 4 — Gate (validación de evidencia)
**Archivo:** reutiliza `tools/evidence_contract.py` (ya existe)

| Campo | Detalle |
|---|---|
| **Qué hace** | Verifica que la propuesta cumple el Evidence Contract |
| **Mínimos** | Según tipo (RULE: 2 experimentos, 1 review independiente, confianza ≥0.85) |
| **Resultado** | Propuesta APROBADA para revisión humana o DESCARTADA por falta de evidencia |
| **Salida** | Estado en la propuesta YAML: `gate: passed/failed` + motivo |

**Pregunta clave:** ¿la evidencia acumulada justifica tocar la regla? Sin
evidencia suficiente, la propuesta ni llega a Joseba.

---

## 4. Flujo de gobernanza (el humano decide — JL-012)

```
Observer → Evidence → Proposer → Gate → PROPUESTA lista
                                        ↓
                    Aviso a Joseba: "El sistema propone ajustar X
                    (evidencia: Y decisiones de la regla Z en N horas)"
                                        ↓
              ┌────────────────────────────────────────┐
              │   Joseba: aprueba / rechaza / modifica  │
              └────────────────────────────────────────┘
                       ↓ aprueba
              apply-decision.sh actualiza policies/*.yaml
                       ↓
              La propuesta se registra como DEC en el lab
```

**Garantías de gobernanza:**
1. **Nunca se auto-aplica** — el Gate solo habilita la propuesta, no la aplica
2. **Trazabilidad total** — cada cambio queda como DEC + entrada en ledger
3. **Rollback fácil** — las políticas YAML se versionan (git) y tienen `.bak`
4. **Auditable** — Joseba ve la evidencia detrás de cada propuesta

---

## 5. Políticas YAML — esquema de propuesta

```yaml
# proposals/2026-08-04-ajustar-horario.yaml
id: PROP-20260804-001
fecha: 2026-08-04
objetivo: ajustar_umbral
regla: horario
evidencia:
  decisiones_observadas: 120
  pct_uso: 85          # la regla horario decide el 85% de las veces
  fallos_asociados: 3
  ventana_horas: 72
gate:
  status: passed
  motivo: "85% de uso > umbral de interés (70%)"
cambio_propuesto:
  parametro: franja_noche
  valor_actual: "00:00-23:59"
  valor_sugerido: "20:00-08:00"
estado: pendiente_revision   # pending | approved | rejected | applied
revisado_por: null
```

---

## 6. Fases de implantación

**ENTREGA 1 (aprobada 04-ago — proyecto independiente): F1-F2 + Baseline**

| Fase | Contenido | Esfuerzo | Depende de |
|---|---|---|---|
| **F1 — Observer** | Lee ledger, agrupa por regla, métricas básicas (hechos, no conclusiones) | 1-2h | Ledger ya poblado (326 entradas) |
| **F2 — Evidence** | Dashboard: top reglas usadas/nunca usadas, fallos, incertidumbre, distribución temporal/tipo/agente | 1h | F1 |
| **Baseline** | Línea base por regla (media semanal, desviación, normal/anómalo) | 1h | F2 |

**ENTREGA 2 (BLOQUEADA hasta tener evidencia — no tocar hasta entonces):**

| Fase | Contenido | Esfuerzo | Depende de |
|---|---|---|---|
| **F3 — Proposer** | Plantillas de propuesta YAML | 1-2h | F2 + Baseline + DISTRIBUCIÓN REAL |
| **F4 — Gate** | Reutilizar evidence_contract.py | 30 min | F3, contrato ya existe |
| **F5 — Aviso** | Notificación Telegram + revisión humana | 1h | F4 |
| **F6 — Integración** | Cron + docs + skill | 1h | F1-F5 |

**Total Entrega 1: ~3-4h. F3-F6: solo cuando el piloto (1 semana) haya producido datos.**

**Prohibición explícita (04-ago): durante F1-F2+Baseline queda prohibido proponer
cambios automáticos. El entregable de la Entrega 1 es responder con evidencia a:
qué reglas gobiernan realmente el lab, cuáles casi nunca se activan, cuáles
concentran fallos, cómo cambia el uso por tipo de tarea y tiempo, y qué es
normal vs anómalo.**

---

## 7. Riesgos y límites

| Riesgo | Mitigación |
|---|---|
| Auto-corrección ciega | Gate + revisión humana OBLIGATORIA (JL-012) |
| Propuestas ruidosas | Umbral de interés (70%) + mínimo de decisiones observadas |
| Deriva por goteo (pregunta 7 del doc) | Cada cambio es un DEC explícito, no acumulativo |
| Sobre-ajuste a datos de corto plazo | Ventana mínima de observación (72h) + mínimo de decisiones |
| Conflicto con políticas manuales | Precedencia documentada: políticas manuales > propuestas L2 |

---

## 8. Decisiones de Joseba (04-ago) — respuestas a las 5 preguntas

1. **Ventana de observación:** DOS, no una — 7 días (detecta cambios rápidos) + 30 días (evita reaccionar al ruido). No elegir una sola.
2. **Umbral de interés:** NINGUNO por ahora. El primer objetivo es obtener la distribución real y después decidir. Un mismo 70% significa cosas muy distintas según la distribución (65/63/61/59 vs 92/3/2/1). Definirlo antes sería arbitrario.
3. **Reglas incluidas:** SOLO enrutamiento (horario, gpu, niveles). No privacidad, ni costes, ni otras con componente de política: las de enrutamiento son las más fáciles de medir objetivamente.
4. **Notificación:** AMBAS — Telegram (para actuar) + log local (imprescindible para auditoría).
5. **Fase piloto:** SÍ, 1 semana, con prohibición explícita:
   > Durante F1-F2 queda prohibido proponer cambios automáticos.
   El objetivo del piloto es aprender cómo se comporta el sistema, no mejorarlo.

---

## 9. Módulo Baseline (añadido por decisión 04-ago — entre F2 y F3)

**Función:** responder una sola pregunta: ¿QUÉ ES NORMAL?

**Archivo:** `hermes-lab/loop-engineering/baseline.py`

```yaml
rule:
  GPU_LOCAL
  weekly_mean: 34
  weekly_std: 3
  current_week: 35
  status: normal
```

frente a:

```yaml
rule:
  GPU_LOCAL
  weekly_mean: 34
  weekly_std: 3
  current_week: 82
  status: anomalía
```

**Justificación:** sin una línea base, cualquier umbral fijo ("70%") corre el
riesgo de generar falsos positivos o de pasar por alto cambios realmente
significativos. El Baseline es lo que convierte el Evidence (dashboard) en
conocimiento accionable sin necesidad de F3.

**No hace:** no propone, no toca policies, no recomienda. Solo clasifica
normal/anómalo respecto a la línea base.

---

## 10. Verificación del diseño

- [x] Reutiliza `decision-ledger.jsonl` (326 entradas reales)
- [x] Reutiliza `evidence_contract.py` (mínimos por tipo ya definidos)
- [x] Preserva JL-012 (humano decide siempre)
- [x] Sin cambios en el Runtime actual (apply-decision.sh intacto)
- [x] Propuestas versionables + rollback por git
- [x] Decisión 04-ago incorporada: F1-F2+Baseline aprobado; F3-F6 bloqueados
- [x] Umbrales NO definidos a priori (distribución real primero — decisión Joseba)

---

## 11. Lecciones de Autobots Abacusia — INCORPORADAS (07-ago-2026)

Fuente: `research/analisis-autobots-abacusia.md` (video YT, 06-ago). El pendiente
"ESTUDIO AUTOBOTS / LOOP SELF-IMPROVING" pedía incorporar 2 lecciones al diseño
L2 y decidir stack. Estado REAL verificado 07-ago: el Proposer (F3) ya existe en
producción (`tools/proposer.py`, proposals en `04-operations/proposals/` desde
05-ago, cron `l2-proposer-daily` job dce8b9d1dfb2 activo + aviso Telegram) —
la decisión de stack queda confirmada por la práctica, no por teoría.

### Lección 1 — Evaluador INDEPENDIENTE (no auto-evaluarse)

Abacusia: un agente que califica su propio trabajo = "fábrica de falsa
confianza"; la calificación la da OTRO modelo. Aplicación al lab, con matiz:

- El Gate del L2 ya es independiente en el sentido fuerte: `evidence_contract.py`
  es DETERMINISTA (script, no LLM) — no depende de ningún modelo que pueda
  auto-convencerse. Esto es MÁS robusto que el doble modelo de Abacusia.
- La lección aplica donde el L2 use LLM para evaluar contenido (p.ej. juzgar
  si una propuesta es coherente): el evaluador DEBE ser un modelo SEPARADO del
  que propone. Regla de diseño: nunca el mismo modelo propone y evalúa.
- Conexión con verifier TD-001: falso negativo → analizar log, no re-ejecutar
  el mismo detector. Un evaluador independiente no re-ejecuta: contrasta.

### Lección 2 — Panel gráfico de progreso (métrica consistente graficada)

Abacusia: cada Autobot tiene una métrica medida igual en cada ejecución,
graficada en el tiempo (no un resumen que la IA escribió). Aplicación al lab:

- `observer.py` ya produce métricas (375 decisiones, 9 RULEs nunca activadas);
  falta el panel gráfico. El lab YA tiene la capacidad validada de generar
  gráficas (HTML/CSS → Chrome headless → PNG, método del 04-ago usado en
  infografías).
- Diseño: script que consolida la métrica del L2 (decisiones por regla, % uso,
  fallos, baseline normal/anómalo) y genera un PNG por semana vía
  `google-chrome --headless --screenshot`. Referencia de formato:
  `research/infografias/l2-loop-engineering.html` (ya existe como boceto).
- No bloquea F3-F6: el panel es del Observer/Evidence (F2), no del Proposer.

### Decisión de stack (F3/F4): STACK PROPIO, confirmado por la práctica

| Opción | Veredicto |
|---|---|
| **Stack propio** (proposer.py + evidence_contract.py + observer.py + cron) | ✅ ELEGIDO — ya opera en producción desde 05-ago (10+ proposals) |
| CrewAI | ❌ No aporta: el lab no necesita crews multi-rol; el flujo es secuencial con puerta humana |
| LangGraph | ❌ No aporta: el grafo L2 es lineal (Observer→Evidence→Proposer→Gate); los 9 conceptos ya los cubre el lab sin framework (ver analisis-langgraph-concepts) |
| n8n | ❌ Solo si hubiera consumidor externo tipo API desatendida — no es el caso |

La pregunta "¿F3/F4 con stack propio o framework?" queda RESUELTA con datos:
el stack propio ya está funcionando y genera propuestas reales desde el 05-ago.
Introducir un framework ahora sería reemplazar lo que ya produce, sin ganancia
medible. El pendiente se cierra con esta evidencia.

---

## 12. Pendiente derivado del estudio (opcional, NO bloqueante)

- [ ] Panel gráfico del L2 (lección 2): script + PNG semanal desde la métrica
      de observer.py, reutilizando HTML→Chrome headless. Depende solo de F2
      (ya operativo). NO desbloquea F3-F6 (eso lo deciden los datos del piloto).
