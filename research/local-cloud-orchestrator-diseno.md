---
title: "Diseño — Orquestador local-first con escalada automática (ESQUELETO v0.1)"
type: research
status: propuesta-evaluada
created: 2026-08-10
evaluada: 2026-08-10
---

# Orquestador local-first con escalada por calidad — diseño
**VERACIDAD:** [ALCANCE INTERNO]

**Estado:** PROPUESTA EVALUADA (10-ago-2026). No se implementa por ahora.
Script: `tools/local_cloud_orchestrator.py`. Este documento mapea las piezas
que ya existen en el lab, qué aporta el esqueleto, qué falta para producción
y el veredicto de la evaluación.

## ESTADO 22-ago-2026 (re-evaluado con gpt-oss, ver comparativa-local-cloud-20260822.md)

`ejecutar_cloud()` CORREGIDO y VALIDADO: id `deepseek-v4-flash` (sin prefijo; antes `deepseek/...` = 400), max_tokens 4000 (a 800 DeepSeek se corta), key desde ~/.hermes/.env (Bitwarden desactivado desde 06-jul), header construido por partes. Prueba real: DeepSeek respondió en 2.28s. El veredicto de latencia (90-223s con R1) quedó OBSOLETO: con gpt-oss el batch-json local tardó 6.62s, 0 USD. Batería 22-ago: el local IGUALA al cloud en batch estructurado (T3/T4/T5 con presupuesto suficiente) y PIERDE en redacción abierta (T1/T2, juicio ciego: alucina datos). DECISIÓN: orquestador operativo para batch estructurado (verifier determinista reforzado: JSON vacío rechazado); redacción abierta se queda en cloud. Verifier de tareas abiertas = mejora futura condicionada a mover redacción a local.

## VEREDICTO DE LA EVALUACIÓN (10-ago-2026)

El esqueleto FUNCIONA en lo esencial (clasificación, loop local, verifier,
escalada, ledger, auto-corrección por datos). La evaluación real detectó y
corrigió un bug (doble escritura del ledger en la rama de escalada).
Decisión: queda como PROPUESTA EVALUADA, sin implementar, porque el ahorro
absoluto es bajo (coste cloud real ~1 USD/día) y la latencia local
(90-223s/tarea) la limita a batch. Re-evaluar al integrar el Mission
Runner (RULE-010).

## Propuesta (una frase)

El modelo LOCAL es el trabajador principal; DeepSeek queda detrás como
supervisor que solo interviene cuando el verifier determinista rechaza el
resultado local o cuando la tarea es de razonamiento complejo. El objetivo
es minimizar tokens cloud sin perder calidad, con fallos del local
corregidos automáticamente por escalada.

## Flujo del loop

```
Tarea
  └─ clasificar_tipo()  → batch | batch-json | vision | razonamiento
        │
        ├─ razonamiento → CLOUD directo (no intenta local: ahorra latencia)
        │
        └─ resto → sugerir_motor() desde ledger
              │
              ├─ "cloud" (tipo con historial de fallos) → CLOUD
              │
              └─ "local" → llm-router.sh (R1 / GLM)
                    │
                    └─ verifier() determinista (0 LLM)
                          ├─ ✅ → resultado (0 cloud) + ledger
                          └─ ❌ → CLOUD (reintenta) + ledger + escalado
```

## Piezas que YA existen en el lab (no hay que inventar)

| Pieza | Dónde | Rol en el loop |
|---|---|---|
| Clasificador por tipo | llm-router.sh (batch/batch-json/vision/check) | base del `clasificar_tipo` |
| Motor local R1-14B | LM Studio :1234 | trabajador local |
| Motor local GLM 4.6V | LM Studio :1234 | visión |
| Verifier/gate determinista | SVP Procedure Check, evaluator con rúbricas, red de refactor-seguro | patrón del `verifier()` |
| LPA Casebook | lpa/casebook (5 casos: R1/Dolphin fallan razonamiento) | auto-corrección por aprendizaje |
| Ledgers | /mnt/ssd_ia_datos/lab-state/ + metrics/*.jsonl | patrón del ledger nuevo |
| Cloud deepseek flash | proxy :9911 | supervisor/escalada |
| Router local/cloud | tools/llm-router.sh (09-ago) | ejecución local |

## Qué aporta el esqueleto (v0.1)

1. `clasificar_tipo()` — heurística simple (keywords). Ampliable con
   RULE-PROC-005 (State Question Detector).
2. `verifier()` — gate determinista por tipo: JSON válido, salida no vacía,
   sin errores de motor. CERO tokens en verificación.
3. `sugerir_motor()` — lee el ledger: si un tipo falla ≥2 veces seguidas o
   tasa ≥50%, sugiere cloud-first. Ese es el mecanismo de auto-corrección
   por datos: el tipo de tarea "aprende" a no usar el local.
4. Ledger `local_cloud_ledger.jsonl` — cada intento registra tipo, motor,
   local_ok, motivo, escalado, latencia. Alimenta el Casebook.
5. Modos evaluables: `--plan` (qué haría, sin ejecutar), `--check`
   (diagnóstico), `--stats` (tasas por tipo), `--run -y` (ejecuta).

## Qué falta para producción (PENDIENTE, no está en el esqueleto)

1. **Hook cloud real**: `ejecutar_cloud()` está como stub. En producción:
   curl al proxy :9911 (deepseek flash) o el cliente del lab.
2. **Verifier de tareas abiertas** (resumen, redacción): el gate
   determinista no cubre calidad semántica. Opciones: (a) verifier con
   rúbrica simple (longitud, estructura, keywords esperadas), (b) segundo
   LLM local barato (LFM 2.5) como revisor, (c) humano. Decidir en
   evaluación — para no gastar cloud verificando, el revisor local es lo
   natural.
3. **Integración con Hermes**: que el orquestador sea una herramienta
   (tool) o una skill, no un script suelto. El Mission Runner (RULE-010,
   pendiente) es el destino natural.
4. **Carga/rotación de modelos**: el loop necesita saber qué modelo está
   cargado y rotar si hace falta (VRAM 12 GB). Integrar con lms.
5. **Protección contra el "orquestador que verifica con cloud"**: si el
   verifier usa cloud, el ahorro se come. Regla: verificación SIEMPRE
   determinista o local, nunca cloud.
6. **Pitfall conocido (ai-router)**: "try local, escalate to cloud" no
   existe nativamente en Hermes (solo fallback por error HTTP). Este
   orquestador LO CONSTRUYE explícitamente — por eso es un componente
   nuevo, no una config.

## Criterios de aceptación (para la evaluación)

- [ ] `--plan "razona sobre X"` → tipo=razonamiento, motor=cloud (sin intento local)
- [ ] `--plan "clasifica estos items en json"` → tipo=batch-json, motor=local
- [ ] `--run -y` con salida JSON válida → local_ok=True, 0 cloud
- [ ] `--run -y` con salida corrupta → verifier falla → escala cloud → ledger
- [ ] `--stats` tras 3+ intentos fallidos del mismo tipo → sugerido=cloud
- [ ] Ningún paso de verificación consume tokens cloud

## Riesgos / contras (verificados en el lab)

- Locales ≤14B fallan razonamiento secuencial (certificación 26-jul) → por
  eso razonamiento va directo a cloud, nunca intenta local.
- Latencia local (R1 ~11 tok/s) — para tareas batch aceptable; para
  orquestar no.
- VRAM 12 GB: no caben R1+GLM+Gemma a la vez → rotación obligatoria.
- El esqueleto actual NO reordena modelos ni gestiona carga: solo planifica
  y registra. La gestión de carga es fase 2.

## Decisión pendiente del usuario

1. ¿Evaluamos el esqueleto con --plan/--check ahora (solo lectura)?
2. ¿El verifier de tareas abiertas será (a) determinista simple, (b) LFM 2.5
   local como revisor, o (c) humano?
3. ¿Integramos como herramienta de Hermes o lo dejamos como script + skill?
