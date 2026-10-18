---
title: "Análisis — Vídeo de Joaquín Ruiz (@jokioki): «Así construí un kernel para que mis agentes de IA no se pisen»"
type: research
fecha: 2026-10-01
hora: "17:33 CEST"
canal: "@jokioki (Joaquín Ruiz — IA para Desarrolladores)"
video_id: xAFRuBxfapM
estado: "investigación cerrada — 0 instalaciones, 0 cuentas, 0 €, 0 GPU; propuestas pendientes de OK"
peticion_usuario: "Enlace enviado por el usuario (01-10-2026). Análisis autorizado: autorización nº 1 del turno."
---

# Análisis — Vídeo: «Así construí un kernel para que mis agentes de IA no se pisen» (Joaquín Ruiz)

**VERACIDAD:** [VERIFICADO]

## 1. Fuente

- **Vídeo:** `https://youtu.be/xAFRuBxfapM` → `https://www.youtube.com/watch?v=xAFRuBxfapM` · ID `xAFRuBxfapM`
- **Título real (oEmbed):** «Así construí un kernel para que mis agentes de IA no se pisen»
- **Canal:** Joaquín Ruiz — IA para Desarrolladores (**@jokioki**, `UCnZCS1XKBTi_RpM67O3DiRg`)
- **Publicado:** **01-10-2026** (`upload_date: 20261001`) · **17:33** (1.053 s) · **132 vistas / 21 likes / 13 comentarios** en la lectura (01-10-2026 17:27 CEST)
- **Ficha `yt-dlp`:** leída el 01-10-2026 (`/tmp/yt_json.txt`, 2.201.218 B)
- **Transcripción:** íntegra, **351 líneas / 14.662 B** con timestamps (`/tmp/yt_trans.txt`)
- **Canal ya vigilado:** está en `tools/monitor_yt.py` (añadido 25-sep-2026) → el vídeo saldrá igualmente en el digest del cron `vigilar-canales-yt` (09:15)

**Cruce previo anti-duplicado (no se repite lo ya escrito):**

- `research/analisis-jev-video-jokiruiz-20260925.md` (25-sep-2026) — vídeo de Jev/TypeSafe del mismo canal. **NO se modifica.** Aquel ya cerró la pieza «Jev»: nube, sin pesos publicados → *no se adopta nada*, con futuribles F1/F2/F3 y sus señales.
- `research/analisis-jev-typesafe-system-one.md` (18-sep-2026) — Jev desde un post de LinkedIn.
- `research/analisis-canal-jokiruiz-20260925.md` (25-sep-2026) — barrido de los 59 vídeos del canal.
- `research/analisis-jokiruiz-ahorro-tokens-20260908.md` (08-sep-2026).

Este documento **añade lo que no estaba**: el kernel open source, su matriz de mediciones, la evidencia cruda y el punto donde el propio autor dice que falla.

## 2. Qué presenta el vídeo

- **Tesis:** cuando varios agentes de código trabajan a la vez sobre el mismo repositorio, **git no ve el choque** porque el conflicto está en la *intención*, no en las líneas. Cada agente en su rama, todos con sus tests en verde, merge limpio y el resultado roto.
- **Analogía:** los **semáforos** de Dijkstra (1965). Los agentes son procesos; el código, la BD de test o el presupuesto de tokens son recursos.
- **Dónde se rompe la analogía (lo interesante):** (a) aquí una operación puede durar minutos, no nanosegundos, así que bloquear «por si acaso» es carísimo; (b) dos agentes chocan **sin tocar el mismo fichero**.
- **Médula:** servidor local pequeño. Antes de cada `Edit`/`Write`/`Bash` un **hook `PreToolUse`** le pasa la *intención* (tarea de la spec + qué va a tocar + qué pretende cambiar + lo que hacen los demás) y pregunta «¿choca?» → probabilidad `p`. `p` baja concede, `p` alta espera, `p` intermedia **camino lento** (Sonnet propone salida, Opus si no). Tras cada escritura (`PostToolUse`) pregunta si el cambio invalida el plan de otro y **avisa solo a quien le afecta**.
- **Lo no obvio del resultado:** sin declarar dependencias entre tareas en la spec, el orden correcto **emergió** de las decisiones de choque (el login antes que la exportación; el renombrado antes que el filtro).

## 3. Verificación externa (fuentes primarias)

**Leídas íntegras:**

- `https://raw.githubusercontent.com/JoaquinRuiz/medula/main/README.md` — **313 líneas / 20.652 B** (`/tmp/medula_readme.md`).
- `https://github.com/JoaquinRuiz/medula` — **MIT**, creado **2026-09-29**, **3★**, 0 forks, **7 issues abiertos**, Python + Shell, rama `main`. Topics: multi-agent, concurrency, merge-conflicts, claude-code, calibration, openrouter.
- `https://typesafe.ai/blog/introducing-system-one-models-and-jev` — anuncio de Jev (14-sep-2026, Diogo Almeida, ex-OpenAI); ya analizado en detalle el 25-sep.

**Matriz de mediciones publicada (`results/summary.csv`), promedios de las ejecuciones válidas:**

| Modo | Qué es | Runs | Tests verde/rojo | Choques reales detectados (de 2) | Bloqueos innecesarios | Tiempo | Coste agentes | Coste decisiones | Decisiones | Escalados a camino lento |
|---|---|---|---|---|---|---|---|---|---|---|
| A | Secuencial | a1, a2 | **30 / 7** | — | — | 341 s | $0.86 | — | — | — |
| B | Rama por tarea + merge final | b1–b5 | **31 / 6** | — (git: 2 conflictos textuales, resueltos) | — | 329 s | $1.20 | $0.40 | — | — |
| C | Directorio compartido + locks por fichero | c1–c3 | 37 / 0 | **1,7** | **1,7** | 452 s | $1.65 | $0 | 88 | 0 |
| D | Directorio compartido + Médula + **Jev** | d2–d4 | 37 / 0 | **2,0** | **0** | 415 s | $1.36 | $0.29 | 118 | 20 |
| E | Directorio compartido + Médula + Haiku | e1–e3 | 37 / 0 | 2,0 | 1,0 | 824 s | $1.74 | $0.55 | 149 | 22 |
| F | Directorio compartido + Médula + Sonnet | f1 | 37 / 0 | 2,0 | 0 | 376 s | $1.40 | $0.59 | 114 | 9 |

**Lo que la matriz dice de verdad (y el titular del vídeo matiza):**

1. **Los cuatro modos con directorio compartido (C, D, E, F) acaban 37/0.** Compartir directorio —no el kernel— es lo que cambia el juego. La ventaja de Médula **no es el resultado ni el coste** ($1.65 en C vs $1.65 en D sumando decisiones), sino **detectar los 2 choques en vez de 1,7** y **no bloquear a nadie sin motivo** (0 vs 1,7).
2. **En modo A el agente de T2 se niega** a implementar un login sin segundo factor y pide confirmación que nunca llega en modo no interactivo.
3. **La mayor parte del coste de decisión de D es el camino lento** (~20 escalados por ejecución, uno de cada seis; el 61% de las decisiones de Jev **sobre escrituras** cae en la banda insegura).

## 4. Coste: Jev es de pago (punto planteado por el usuario)

- Jev **no es gratis**: es un modelo **propietario en nube**, en **acceso anticipado**, servido vía **OpenRouter** (`typesafe/jev-1.13`). El vídeo del 25-sep ya lo dejó claro: **0,042 $/M tokens de entrada**, salida gratis, y la demo de Doom ≈ **7 $/hora**. Esta medición de Médula lo confirma: **~0,3 s y $0,00006 por decisión**, pero el gasto real del modo D incluye el camino lento.
- **Lo que sí es gratis en el mismo experimento:** el **kernel Médula** (MIT), el decider de **locks** (modo C, sin modelo, coste de decisión $0), los **tests sin clave de API** (proveedor simulado) y la **evidencia cruda** de todas las ejecuciones.
- **Conclusión de coste:** el *patrón* es gratis y se puede replicar; el *decider* de nube no. Y según su propia matriz, **el modo gratis (locks) acaba 37/0 igual**: lo que se paga es la detección semántica, no el resultado.
- **Nada de esto obliga a pagar en el lab:** el decider rápido podría ser local (LM Studio `:1234/v1` / Ollama `:11434/v1`, vía el contrato del SDK ya identificado el 25-sep) o, más barato aún, **un registro determinista de escritores, sin modelo**.

## 4.bis. Laya: el «Jev gratis» — ya medido por el lab (23–25 sep 2026)

**Pregunta del usuario (01-10-2026):** «¿no analizamos hace unos días un equivalente a Jev llamado Laya?» → **Sí.** No se repite la medición: se cita la que ya existe.

- **Qué es:** `convaiinnovations/laya` — **Apache-2.0**, corre en local. `laya` 421M (ModernBERT-large, 512 tok) · `laya-multilingual` 322M (mmBERT-base) · `laya-typed-decisions` 421M. Paquete PyPI `laya` **0.3.10** (Apache-2.0); repo `github.com/NandhaKishorM/laya`. Decisión **no autorregresiva** («System 1»): estado + preguntas tipadas → respuestas tipadas con probabilidad; **no genera texto**.
- **Por qué es, literalmente, «el Jev gratis»:** `laya-serve` expone `POST /v1/systemone` con **la misma forma de petición/respuesta que TypeSafe Jev** («Jev-compatible»), y su model card trae tabla «Laya (with routing) vs TypeSafe Jev 1.13.0» (MASSIVE EN 0,783 vs 0,657 · XNLI EN 0,860 vs 0,843 · otras 14 lenguas 0,521 vs 0,731 — material del proveedor, no medición independiente). Latencia declarada 39,5 ms (english) / 32,8 ms (multilingual) frente a 236–276 ms p50 de Jev → «7,8×», cifra **del proveedor y que él mismo declara no haber medido**.
- **Dónde está la evidencia:** `joko-lab/instruments/laya-comparativa/` (rig **6,3 GB**, coste **0 €**); ficha fechada `REFERENTE-laya.txt` (7.074 B, 24-sep); 8 ficheros `resultados_laya_*.json`; caché HF `models--convaiinnovations--laya` (**2,3 GB**). Conocimiento consolidado en `validacion-instrumentos-medicion/references/comparacion-modelos-set-congelado.md` y `evaluar-alucinaciones/references/evaluar-modelo-decision-externo.md`.
- **Veredicto del lab (24–25 sep): SÍ como referente secundario fechado; NO como componente.**
  - n=299: granite4.2:8b **0,9164** (Brier 0,0836) > r1-14b 0,8060 > qwen2.5:7b 0,7993 > Laya `typed-decisions` 0,7860 > `english` 0,7458 > `multilingual` 0,6054 > `router` 0,6020.
  - n=120 congelado: `typed-decisions` **0,5083** (azar 0,5000; dice SI en 107/120) → hipótesis refutada al cumplirse la condición de aborto pre-registrada (tarjeta `t_d35590c6` → `done`, 0 €). El 20/20 inicial era coincidencia de un subconjunto homogéneo.
  - **`memoria` 0/6 en los cuatro checkpoints** (granite/qwen/r1: 6/6); `multihop` 9/22 en el mejor caso.
  - `RuntimeWarning: ships invalid temperatures` en 3 checkpoints → Brier/ECE **no comparables**.
  - Lo que sí aguantó: **trampas 8/8** (igual que granite).
  - Riesgo anotado (no ejecutado): `laya-serve` escucha en `0.0.0.0` **sin autenticación**.
- **Cruce con este vídeo (nuevo):** el hueco donde Médula coloca a Jev es exactamente el que Laya dice ocupar gratis — pero decidir un choque exige **saber qué están haciendo los otros agentes**, el eje `memoria`/contexto, y ahí Laya hizo **0/6**. El modelo gratis que le gana en el lab (**granite4.2:8b**) ya está levantado. Refuerza **M1** (registro determinista, sin modelo) como primer paso antes de meter cualquier decider.
- **Regla vigente que dejó esta medición:** citar Laya **siempre con versión** (0.3.10).

## 5. Caveats que el propio autor admite (lo más valioso del repo)

- **Umbrales ajustados con las mismas 100 parejas con las que se miden.** No hay set de validación separado.
- **Las etiquetas de esas parejas las escribió Claude** (misma familia que Haiku y Sonnet), **sin revisión humana** → probablemente **favorece a Haiku y Sonnet** en la comparación de acierto. El **98,5% de Sonnet** está inflado por construcción.
- **El camino rápido no es la norma:** **61% de las decisiones de Jev sobre escrituras reales caen en la banda «no estoy seguro»** (vs 13% en las parejas de calibración). Va al camino lento. El autor lo llama *el mayor problema abierto*.
- **Muestras pequeñas:** F=1, A=2, C/D/E=3, B=5. Los tiempos de **a1, b2 y b3 no son fiables** (solaparon con otra ejecución) y quedan fuera de las medias de tiempo.
- **Contaminación admitida:** en **e1 y f1** los agentes usaron herramientas de Claude Code (`ListAgents`/`SendMessage`) para hablarse **fuera** de Médula (en f1, cinco mensajes: T3 avisó a T4 del renombrado). Ambas ejecuciones se conservan marcadas; esas herramientas están ahora desactivadas.
- **En el choque del login Jev puntuó más alto un falso** y fue el camino lento el que salvó la papeleta → «no es magia, es un modelo probabilístico que a veces se equivoca».
- **Política de publicación:** no se mergean tests que necesiten clave de API, ni ediciones a mano de resultados publicados, ni ocultar un caveat. Un run defectuoso **se marca, no se borra**.

## 6. Qué es NUEVO respecto al análisis del 25-sep

1. **El banco reproducible.** 6 modos, 6 tareas de una API de reservas escritas para colisionar de formas conocidas, mismas agentes y mismo modelo en todos los modos, y **toda la evidencia cruda publicada** (`results/runs/<id>/`, incluido el `medula.db` de cada decisión). Coste del banco completo: **~20 $ y ~1 h**; los tests corren gratis.
2. **Un resultado honesto sobre coordinación:** compartir directorio ya arregla el rojo (C–F); el kernel aporta **detección y no-bloqueo**, no velocidad ni coste.
3. **El primer dato real de calibración** que tocaba al futurible F2 del informe del 25-sep: **Jev 92,5% / Haiku 91,5% / Sonnet 98,5%** (100 parejas, 2 repeticiones) — con las dos taras declaradas (umbrales ajustados en la misma muestra; etiquetas escritas por un modelo de la misma familia).
4. **Un caso de estudio del modo en que el lab ya se rompió una vez** (ver §7).

## 7. Relación con Joko Lab

- **El problema del lab es el mismo, con otro nombre.** En `OBS-154` (30-sep-2026) el **curador de fondo escribió en 7 ficheros de skills a las 23:03** mientras la sesión trabajaba sobre ellos. No había conflicto de líneas: había **dos escritores sin nadie que decidiera quién espera**. Eso es exactamente el choque semántico que Médula ataca.
- **Hermes tiene el mecanismo equivalente (verificado hoy en la doc instalada, `user-guide/features/hooks.md`):** el hook **`pre_tool_call`** (con `matcher` por nombre de herramienta) **puede BLOQUEAR** la llamada devolviendo `{"decision":"block","reason":"..."}` (estilo Claude Code) o `{"action":"block","message":"..."}` (canónico Hermes), y **el motivo llega al modelo** como error. También existen `post_tool_call`, `pre_llm_call`, `pre_verify` y `subagent_stop`.
- **Estado actual del lab: NINGÚN hook configurado** (`hermes hooks list` → «No shell hooks or outbound webhooks configured»; `hooks_auto_accept: false` en `config.yaml`). Es decir: el hueco existe y está vacío.
- **Diferencia importante de arranque:** el lab **no tiene un decider rápido**. Sus modelos locales van a ~7,7 tok/s (qwen3.6-35b), así que «una decisión por escritura» con el modelo en el camino del agente sería lenta. El equivalente útil y barato **no es el modelo, es un registro determinista de escritores** («quién está tocando qué, ahora»): coste 0, sin GPU, y habría cazado el caso OBS-154 sin necesidad de probabilidades.
- **Prudencia (RULE-015):** antes de fiarse de cualquier probabilidad de choque hay que **validar el instrumento**; el propio repo enseña cómo se infla una métrica cuando se ajustan umbrales y etiquetas en la misma muestra.

## 8. Decisión

**No se adopta ni instala nada** (0 componentes, 0 descargas, 0 cuentas, 0 €, 0 GPU, ningún servicio tocado). El valor es: (a) criterio para leer titulares («con el kernel acaban en verde» — con locks también); (b) el reparto **kernel gratis / decider de pago**; (c) el patrón *decidir antes de escribir* con **`pre_tool_call` de Hermes**, que es la pieza que le falta al problema de escritores concurrentes del lab.

## 9. Futuribles (con señal de activación; ninguno se ejecuta sin señal ni sin OK)

- **M1 — Registro de escritores del lab (sin modelo).** Anotar quién escribe qué (sesión, curador, crons, subagentes) y **comprobar si habría cazado OBS-154**. Solo si sale que sí se discute el veto en `pre_tool_call`. Coste 0, reversible. **Señal:** el siguiente episodio de dos escritores sobre el mismo fichero.
- **M2 — Verificar la matriz desde la evidencia cruda.** Clonar el repo en `/tmp` y leer `results/summary.csv` y un `medula.db` real, sin clave de API (tests con proveedor simulado). **Señal:** si se decide reutilizar sus números en un informe del lab.
- **M3 — Decider local para el patrón.** Probarlo con LM Studio/Ollama vía el contrato del SDK de TypeSafe (ya identificado el 25-sep). **Señal:** cuando el registro determinista se quede corto.
- **M4 — Calibración por tramos con datos del lab** (4º dato para el F2 del informe del 25-sep). **Señal:** al validar el próximo instrumento de medición.

## 10. Errores del ASR en este vídeo (para futuras lecturas)

`Cloud Code` → **Claude Code** · `Jeff`/`Jef` → **Jev** · `Edger Dixtra` → **Edsger Dijkstra** · `Sonet` → **Sonnet** · `Haiku` (correcto) · `type safe` → **TypeSafe** · `SPC Driven / Spect Driven / BEV coding` → **Spec-Driven / vibe coding** · `lock` → **locks** (decider) · `loss` → **locks** · `Jeff le da un 0,05 a la gente` → **a los del login** · `los 37 t en verde` → **37 tests en verde** · cifras de coste por decisión del ASR (**0,0029 / 0,0087 / 0,0022**) **no cuadran con la fuente** → no usarlas.

## 11. Fuentes

- **Vídeo y ficha:** `yt-dlp` sobre `xAFRuBxfapM` (leída 01-10-2026 17:27 CEST); oEmbed para título y autoría; transcripción íntegra (`fetch_transcript.py`, 351 líneas).
- **Leídas íntegras:** `raw.githubusercontent.com/JoaquinRuiz/medula/main/README.md` (313 líneas / 20.652 B); `github.com/JoaquinRuiz/medula` (README renderizado + metadatos).
- **Consultadas:** `typesafe.ai/blog/introducing-system-one-models-and-jev`; informes previos del lab citados en §1; `hermes hooks --help` / `hermes hooks list` / `hermes hooks test --help`; doc instalada `user-guide/features/hooks.md`.
- **No accesible / no intentado:** resultados crudos de `results/runs/` (no clonado, requiere OK → futurible M2); clave de OpenRouter (no usada, no hay).

## 12. Registro

- **Fichero NUEVO.** No se ha modificado ningún otro fichero: `analisis-jev-video-jokiruiz-20260925.md`, `analisis-jev-typesafe-system-one.md`, `04-operations/backlogs/pendientes.md` ni ningún registro acumulativo quedan intactos.
- **Sin commit** (fuera del alcance de esta autorización).
- **Escritura autorizada:** autorización nº 1 del turno del 01-10-2026 («1, pero en el vídeo usan Jev…»).
- **Ampliación 01-10-2026 17:40 CEST (autorización: «Si» a «¿Amplío la nota con esta sección de Laya?»):** añadido el **§4.bis** (Laya = el «Jev gratis», con la medición del lab del 23–25 sep citada, no repetida). Resto del documento sin cambios. Copia de seguridad previa en scratch (`/tmp/analisis-medula-precopy.md`, 14.649 B). **Sin commit.**
