---
title: "EXP-20260916-007 — Supervisión multi-agente vs sesión directa (coste, latencia y calidad verificada)"
type: EXP
---

# EXP-20260916-007 — Supervisión multi-agente vs sesión directa

**Estado:** DISEÑO — redactado 2026-09-16. **NO ejecutado**: la ejecución gasta cloud (6 tareas) y necesita OK explícito + presupuesto.
**Tipo:** EXP-20260916-007 (séptimo experimento secuencial del lab; abre el eje "multiagente" del HYP-004).
**Método:** Medición comparada A/B con tareas gemelas, rondas intercaladas. Solo lectura sobre los instrumentos existentes (`pipeline_obs.jsonl`, `remote_usage` si aplica). **NO se modifica el router, ni el daemon, ni los ledgers, ni la config de delegación.**
**Origen:** HYP-004 (`hypotheses/HYP-004-supervision-multiagente-vs-sesion-directa.md`) ← post EP8 «Supervisor & Specialist» + «Single vs Multi-Agent» (@mentalhotfix, 15-sep) ← `research/analisis-cron-ig-20260916-lote-4.md`.

## Hipótesis

> **H-EXP-007:** En tareas de investigación acotada con fuentes verificables (las que el lab ya resuelve en sesión directa), el modo **supervisado** (`hermes kanban swarm`, perfil `default` cloud) **no mejora la calidad verificada** y **aumenta el coste (tokens × precio) y/o la latencia** por tarea resuelta, con el MISMO modelo en ambos modos.

Estado: **NO VALIDADA**. No hay ninguna medida comparable; la única cifra es un piloto único sin contraste (R1).

## Reconocimiento previo (solo lectura, 2026-09-16)

### R1. Único dato existente del modo supervisado (piloto kanban, 01-sep-2026)

- `hermes kanban swarm` con perfil `default` (cloud deepseek-v4-flash): 2 workers → verifier → synthesizer, tenant `piloto-kanban-01`, tema Spec-Driven vs Vibe Coding.
- Resultado: **6/6 cards done, ~15 min**, **16 fuentes reales** (14 HTTP 200 + 2 confirmadas por búsqueda por anti-bot 403).
- Fenómenos ya medidos que afectan a la latencia de B: dispatcher con intervalo 60 s; pitfall de assignee (`default:verificador` no se despacha sin `reassign`); workspace scratch **efímero** (los informes se borran al cerrarse la card).
- **Sin coste registrado**: el piloto no midió tokens ni € → no sirve como cifra, solo como aviso de qué medir.

### R2. No existe medida del modo directo comparable

No hay ninguna ejecución del modo A registrada con el mismo contrato (misma tarea, mismo formato de salida, misma ventana temporal medida). Hay que producirla.

### R3. Instrumento de coste disponible y con límites

- Fuente: `hermes-lab/observability/pipeline_proxy.py` → `pipeline_obs.jsonl` (tokens de prompt/completion y `prompt_cache_hit_tokens` **desde 01-sep-2026 17:38:57**; antes de esa fecha el campo es null).
- Precios vigentes (F0 del EXP-006, cerrado): flash **hit 0,0028 / miss 0,14 / output 0,28** USD/1M; franja peak ×2 (3-6 h y 8-12 h España). Pro: hit 0,003625 / miss 0,435 / out 0,87.
- `04-operations/metrics/local_cloud_ledger.jsonl` = **5 líneas y sin coste** → NO sirve para atribuir (R8 del EXP-006).
- **Límite a comprobar en F1**: si las llamadas de los subagentes del swarm pasan por el proxy (deberían, usan el mismo perfil/modelo) → si NO aparecen, el coste de B es no medible y se declara así.

### R4. La calidad se puede medir con instrumento OBJETIVO (sin juicio de LLM)

Método ya validado en `graph-lab`: extraer las URLs del entregable y comprobar **HTTP 200** con `curl`, y comprobar que la **cita literal** aparece en la página. Eso convierte "calidad" en algo contable: nº de claims, nº de URLs 200, nº de citas literales encontradas. Sin coste y sin opinión del modelo.

## Diseño

### F0 — Contrato y tareas gemelas (coste 0)

1. Fijar **3 tareas acotadas** (1-3 subconceptos, tema técnico del lab) y un **contrato idéntico** para ambos modos:
   - objetivo explícito;
   - formato de salida cerrado: N claims con `{claim, url, cita, fecha}`;
   - criterio de éxito: claims con URL verificable + cita literal presente.
2. Preparar 2 scripts de medida (en `/tmp`, no en `tools/` sin Gate de código):
   - `medir_coste.py <t_inicio> <t_fin>` → filtra `pipeline_obs.jsonl` por ventana temporal, deduplica, aplica precios de R3 → tokens in/out, cache hit/miss, coste USD;
   - `medir_calidad.py <entregable>` → nº de claims, nº de URLs con HTTP 200, nº de citas literales halladas.
3. Registrar la hora exacta (`date`) de inicio y fin de CADA celda: es lo que permite recortar el ledger.

### F1 — Verificar el instrumento en el modo supervisado (1 tarea, coste mínimo)

Lanzar **una** tarea en modo B con `--workspace dir:/abs/path` (para que el informe NO se pierda con el workspace efímero) y comprobar:
- que aparecen líneas nuevas en `pipeline_obs.jsonl` en esa ventana → el coste de B es medible;
- que el informe queda en el directorio persistente y `medir_calidad.py` lo puede leer.
**Gate fail-closed:** si el coste de B no es medible, este EXP solo puede concluir sobre latencia y calidad, y se declara antes de gastar más.

### F2 — Baseline: 3 tareas × 2 modos, intercalado (coste cloud)

Orden: **A1, B1, A2, B2, A3, B3** (intercalado por la lección de la batería MTP: repartir la carga de la máquina y no medir todo un modo en un bloque).

- Modo A (sesión directa): la sesión investiga con `web_search`/`web_extract` y produce el mismo formato de salida.
- Modo B (supervisado): `hermes kanban swarm --worker ... --verifier ... --synthesizer ... --tenant exp007-<n> --json "<mismo contrato>"`, con el pitfall 1 de `graph-lab` aplicado (`reassign` si los assignees no se despachan) y `--workspace dir:` persistente.

Por celda se registra:

| Métrica | Cómo se obtiene |
|---|---|
| latencia de reloj (min) | `date` inicio/fin |
| tokens in/out, cache hit/miss | `medir_coste.py` sobre la ventana |
| coste USD | precios R3 (franja real aplicada) |
| nº de claims | `medir_calidad.py` |
| URLs HTTP 200 / citas literales | `medir_calidad.py` |
| traspasos/reintentos entre nodos | `hermes kanban show <id>` (modo B); nº de reintentos de búsqueda (modo A) |
| errores detectados en revisión | revisión en sesión (mismo criterio en A y B) |

### F3 — Veredicto

Comparar por pares de tarea (A vs B, misma tarea) y agregado. **Umbral: NO a priori (RULE-015)** → el baseline de F2 es lo que fija el umbral. Lectura esperada si H-EXP-007 es correcta: coste y/o latencia peores en B **sin** mejora en URLs 200 / citas literales.

## Criterios de éxito

- Mismo modelo en los dos modos (perfil `default` cloud) y mismas 3 tareas.
- Ventanas temporales registradas al minuto → coste trazable línea a línea.
- Calidad medida con instrumento objetivo (R4), nunca con juicio de LLM.
- Si el coste de B no aparece en el ledger → se declara "coste no medible" y **no** se imputa 0 (el error que produjo el −76,5 % del EXP-006).

## Riesgos y límites

- **El dispatcher infla la latencia de B** (60 s por ciclo): se registrará explícitamente; no se presenta como "el modelo tarda más".
- **Variabilidad web**: dos ejecuciones de la misma tarea traen fuentes distintas → el criterio de calidad es "verificable y citable", no "las mismas fuentes".
- **Workspace efímero** (pitfall 2 de `graph-lab`): sin `--workspace dir:` el entregable se borra y la calidad de B queda sin medir.
- **Coste acotado pero no despreciable**: 6 tareas cloud + F1. Fuera de la franja local (≥12:00) para no competir con el trabajo local; presupuesto máximo a fijar por el usuario antes de F2.
- **n=3 es un baseline, no una conclusión**: si las diferencias son pequeñas, el resultado honesto es "inconcluso".
- **Lo que este EXP NO mide**: calidad "semántica" del texto (se mide verificabilidad, no estilo), ni el efecto de cambiar de modelo, ni el modo local (descartado por la decisión F4 de `graph-lab` → la comparación es cloud vs cloud).

## Pendiente / dependencias externas

1. **OK explícito del usuario + presupuesto** para F1/F2 (gasta cloud).
2. Decidir las 3 tareas de prueba (propuesta: temas técnicos del lab ya tratados, para poder juzgar si el resultado sirve para algo real).
3. Si el coste de B no es medible → decidir si se ejecuta el EXP solo con latencia + calidad (versión reducida).

## Trazabilidad

- HYP: `01-knowledge/hypotheses/HYP-004-supervision-multiagente-vs-sesion-directa.md`
- Origen externo: `research/analisis-cron-ig-20260916-lote-4.md` (EP8 / single-vs-multi, @mentalhotfix)
- Procedimiento y pitfalls: skill `graph-lab` (kanban swarm, assignees, workspace efímero, dispatcher 60 s)
- Instrumento de coste: `pipeline_obs.jsonl` + `04-operations/metrics/precios-ia/precios-vigentes-2026-09-15.md` (F0 del EXP-006)
- Antecedente: EXP-20260915-006 (coste por ejecución) — la parte de € depende de su F2 (export oficial de septiembre)
