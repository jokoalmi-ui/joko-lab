---
title: "REVISIÓN DE FALLOS — 2026-11-06 (ciclo semanal LPA, D0/INC-005)"
type: knowledge
---

# REVISIÓN DE FALLOS — 2026-11-06

> **Fecha real de ejecución:** 2026-11-06 14:34 CET (`date`), viernes; host `up 6 hours, 31 minutes` (arrancado 08:02:38).
> **Ventana revisada:** 2026-10-30 14:36 → 2026-11-06 14:34 (7 días).
> **Fuente:** `~/.hermes/cron/executions.db` en **solo lectura** (`mode=ro`), `~/.hermes/cron/jobs.json`, artefactos de `~/.hermes/cron/output/<job>/`, `journalctl --user` / `--list-boots`, informes de `04-operations/reports/`, `perfume-ia/data/coleccion.db` (solo lectura) y el artefacto del job `8bf412ac2ba3`.
> **Ningún fichero de sistema modificado.** Las únicas escrituras son las de este ciclo en `joko-lab` (esta acta, 3 reexámenes de CP, 3 lecciones, 1 parche de skill, `pendientes.md`), todas con backup RULE-008 `.bak-20261106`.

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo en `lpa/incidentes/` desde el 01-09.** La carpeta no ha recibido ficheros de incidentes en toda la ventana; el ciclo trabaja por tanto sobre la base `cron_incidents` (28 filas, **todas `resolved`**) y sobre los artefactos. No se fuerza ninguna promoción por este frente.

Filas tocadas en la ventana (8):

- `bbc1d8_a5731c9ceec0` (job `bbc1d841e8a7`): `first_seen` 24-10 18:02 → `last_seen` **01-11 18:01** → `closed_at` 02-11 18:02. Reaparece tras un cierre dado por bueno el 28-10.
- `67d5fc_74c14f4af0d6`, `67d5fc_8bfe3bf75670`, `67d5fc_2b5c43c6a8c3`, `67d5fc_1e374c70107a` (job `67d5fcc5b69e`): las cuatro cerradas en bloque el **31-10 09:03:06**.
- `b99e58_7001a6df2270` (job `b99e589b52e2`, accesos al catálogo): 31-10 22:12 → cerrada 01-11 22:10. Error literal: `Script exited with code 1 stdout: sin conexión con el catálogo: [Errno 101] Network is unreachable`.
- `67d5fc_438985bd1afe` (job `67d5fcc5b69e`, informe local): 02-11 09:00 → cerrada 03-11 09:02. Error literal: `Script exited with code 3 stderr: FALLO: informe sin resumen verificado (GATE_OMITIDO)`.
- `7b5207_f37327b04e28` (job `7b52075a99e5`): 03-11 00:00:43 → cerrada 03-11 07:04:26, `failure_type=unknown`. Error: `Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.`

---

## 1. Actividad de la ventana (contexto verificado)

- `executions`: **1.001 filas** (1.000 `completed` + 1 `running`) que cubren **2026-11-05 12:57 → 2026-11-06 14:32 = 25 h 35 min**. El tope de 1.000 filas sigue recortando la semana (D10).
- `jobs.json`: **64 jobs**, 60 activos, 4 desactivados; **63 con `last_status=ok`**, 1 sin estado (`f9615035320a`, desactivado).
- Informes locales 31-10 → 06-11: **7/7 presentes**. Motor `ollama:qwen2.5:7b` los días 31-10 y 01-11; `lmstudio:openai/gpt-oss-20b` los días 02, 03, 04, 05 y 06-11. Gate: 6 × `OK_INTERNO` + 1 × `GATE_OMITIDO` (02-11). Juez de calidad: `ERROR (?)` 31-10 y 01-11, `omitido` 02-11 y 03-11, `PASA` 4,80 / 4,87 / 4,73 los días 04, 05 y 06-11.
- Ficha de perfume diaria (`8bf412ac2ba3`): **7 artefactos** (30-10 → 06-11), el último el 06-11 08:32.
- Gateway: **10 salidas `exited UNCLEANLY`** en 7 días consecutivos (una por día, `suspected_oom=False` en las 10, último heartbeat ~23:00) más 3 el 02-11 en la franja 11:54–12:22 (reinicios manuales, con 3 boots seguidos de 5 y 22 minutos).
- Vigilante de Telegram (`264c02dae003`): **0** líneas `Reiniciando gateway` en todos los artefactos de octubre y noviembre → CP-016 sin recurrencia en la ventana.

---

## 2. Fallos y hallazgos de la ventana

### F1. [REPETIDO · CP-018, 7ª fila] El mismo fallo sigue contando como incidencia nueva cada día
`67d5fcc5b69e` acumula **7 incidencias con 7 firmas distintas** (100 % de firmas únicas) para un solo defecto: la firma incluye la ruta con la fecha. La ventana añade la 7ª (`67d5fc_438985bd1afe`, 02-11) y un cierre en bloque de 4 filas el 31-10. El patrón promovido el 30-10 se confirma: ninguna de las 7 filas es comparable con las demás.

### F2. [CERRADO EN PARTE · el respaldo funciona donde se le pidió, no donde falla] 
El frente A del acta anterior (informe sin resumen con `:1234` caído) **tiene reparación aplicada y usada**: commit `8b2404c` (30-10, "llm-router: respaldo a Ollama si LM Studio no da motor") y `tools/llm-router.sh` modificado el 01-11 14:54. Resultado medido: los informes del **31-10 y 01-11 salieron con `ollama:qwen2.5:7b`** y `OK_INTERNO`.

Lo que **no** cubre: el 02-11 el motor era `lmstudio:gpt-oss-20b`, es decir el puerto respondía y el modelo cargó, pero la salida no pasó el gate → `GATE_OMITIDO` → exit 3. El respaldo se dispara cuando **no hay motor** (`_llm_ollama` solo entra si falla `_cargar_si_falta`), no cuando **el motor responde mal o vacío**. Una ocurrencia → observación, no CP.

### F3. [REABIERTA Y VUELTA A CERRAR · CP-017] El cierre «verificado» del 28-10 duró 4 días
`bbc1d8_a5731c9ceec0` se cerró el 28-10 con las 3 condiciones (reparación real, sin recaída, producto siguiente correcto). Volvió a fallar el **01-11 18:01** y se cerró de nuevo el **02-11 18:02**, sobrescribiendo el `closed_at` anterior. Consecuencia: el criterio de 3 condiciones no distingue una reparación de una tregua; el expediente de CP-017 necesita un criterio temporal (7 días sin recurrencia **o** cambio de causa), no la corrida siguiente.

### F4. [INSTRUMENTO · CP-010/CP-015] El juez de calidad no da veredicto 4 de 7 días y 3 de ellos el job sale en verde
`ERROR (?)` el 31-10 y el 01-11; `omitido` el 02-11 y el 03-11. En los tres días con `OK_INTERNO` + juez roto (31-10, 01-11, 03-11) el job terminó **exit 0**: el gate solo bloquea el resumen ausente, no el juez ausente. El 02-11 el exit 3 fue correcto (faltaba el resumen), pero por el motivo equivocado. Es un falso ok **parcial y medido**: el producto dice «calidad» y la calidad no se midió.

### F5. [ANTÍDOTO CONFIRMADO, sin ascenso · CP-016] 0 reinicios del vigilante en 7 días
Antes: 4 reinicios en 3 noches. Ahora: 0 en 7 días, con 8 vidas del gateway en la ventana y ninguna reiniciada por el vigilante. No se sube de nivel: no se ha verificado que el vigilante llegara a **detectar** red caída con el host encendido en la franja 00–07 (los apagados nocturnos se solapan con esa franja), así que sigue E0 con evidencia a favor.

### F6. [NUEVO · observación, sin CP] Ficha de perfume 03-11: una nota intermedia se leyó como veredicto final
Cronología medida: la corrida `ficha-perfume-diaria` empieza a las 07:05 y su artefacto se escribe a las **07:54** (49 min). La fila 129 de `uso_diario` decía «gate 17/17 no enviado por corte»; el usuario reclamó la ficha a las **07:29**; el envío real figura en `gateway.log` a las **07:36:20**. La propia corrida lo detectó y **no reenvió** (idempotencia correcta), pero el coste quedó registrado: **28.250 tokens** de retrabajo en `retrabajo_ledger` y **dos ficheros base sobrescritos** (`perfume_del_dia_v5_desert_marocain.png`, `ficha_desert_marocain.html`), que choca con la regla de no-retrofit; la nota se corrigió con backup `coleccion.db.BACKUP.20261103_correccion129`.

Mecanismo: nada distingue «corrida en vuelo» de «corrida muerta». El estado intermedio lleva un veredicto («no enviado») que se lee como final. **Una sola ocurrencia de este mecanismo** → no se promueve; va a lección y a parche de skill, con condición de falsación: si una segunda ficha repite «nota de no-envío» + «envío real posterior», se abre CP.

### F7. [INSTRUMENTO RETIRADO QUE ESCRIBE] `retrabajo_ledger` recibió una fila después de ser declarado no-instrumento
El 30-10 se declaró no-instrumento (con `retrabajo_ledger.STATUS.md` prohibiendo citarlo como dato). El **03-11** el fichero recibió una fila nueva (1.569 B, E6, los 28.250 tokens de F6) → hay un productor vivo o una escritura manual. La declaración y su `STATUS.md` están desactualizados respecto al uso real. No se toca: la decisión es del usuario (D7).

### F8. [SIN CAUSA ASIGNADA] `7b5207`: worker `-15` a las 00:00:43 del 03-11
El worker «restart-safe» adoptó la ejecución y murió con `-15` sin dejar estado terminal; los efectos secundarios quedan como desconocidos por el propio sistema. Coincide con el apagado del host (boot `-4` termina 03-11 00:00:54). El registro es correcto y honesto; lo que falta es que una ejecución adoptada tenga estado terminal durable antes del apagado (familia CP-015).

---

## 3. Decisiones D0..D11

**D0 — Fuente y alcance.** Sin `*-incidentes.md` nuevos desde el 01-09. Se revisa base + artefactos + journal. No se fuerza ninguna promoción por falta de material narrativo.

**D1 — CP-018: +1 ocurrencia (7ª).** Expediente actualizado con la fila del 02-11 y el dato de 7/7 firmas distintas. Backup `.bak-20261106`.

**D2 — Frente A: promesa cumplida a medias, y se dice dónde.** El respaldo a Ollama está aplicado y **medido en producción** (31-10, 01-11). No cubre el motor que carga y devuelve salida no verificable (02-11). Criterio nuevo: **el respaldo se acredita por el resultado (gate + juez), no por la disponibilidad del puerto.** 1 ocurrencia → lección, no CP.

**D3 — CP-017: criterio de cierre insuficiente.** Un cierre aceptado el 28-10 reabrió el 01-11 y volvió a cerrar el 02-11. Propuesta al expediente: exigir **7 días sin recurrencia o cambio de causa**, y no sobrescribir `closed_at` sin registrar la reapertura. No se modifica el núcleo del criterio sin el usuario.

**D4 — Juez de calidad: deuda medida, sin acción.** 4/7 días sin veredicto; 3 de ellos con exit 0 y `OK_INTERNO`. Toca producción (gate del informe): se anota y se propone, no se implementa en este ciclo.

**D5 — CP-016: evidencia a favor, nivel sin cambio.** 0 reinicios en 7 días frente a 4 en 3 noches. Sigue E0 porque no hay prueba de detección con red caída y host encendido. Se anota la noche del 01→02-11 (host encendido hasta las 11:54) como pista, **no** como evidencia.

**D6 — F6: lección + parche de skill, sin CP.** Fallo real, mecanismo claro, una sola ocurrencia. Se registra la lección y se añade al Paso 0B de `perfume-del-dia` la comprobación de «corrida en vuelo vs corrida muerta» antes de reconstruir nada.

**D7 — F7: `retrabajo_ledger`.** No se toca ni se cita como dato. Se propone revisar la declaración de no-instrumento del 30-10 y su `STATUS.md` en el próximo ciclo, con decisión del usuario.

**D8 — Gateway: la señal «unclean» ya no discrimina.** 10 salidas sucias en 7 días consecutivos, todas con `suspected_oom=False` y heartbeat ~23:00 (apagado nocturno normal). Una señal que salta el 100 % de los días no informa. Sin acción; si se quiere que informe, hay que medirla solo en reinicios no programados.

**D9 — Deuda mensual.** La revisión mensual del 02-11 **no consta ejecutada**: no existe `revision-fallos-2026-11-02.md` ni job mensual en `jobs.json`. Los 18 CP (CP-001..CP-018) siguen en incubación sin revisión mensual. Hoy **no se promueve nada a `KNOWN.md`/`HYPOTHESIS.md`** (no es la revisión del día 1 y no se fuerza).

**D10 — Tope de 1.000 filas (mantener).** `executions` solo cubre 25 h 35 min; la semana se reconstruye con `cron_incidents` + artefactos. Se mantiene, recordando que CP-018 degrada justo esa fuente.

**D11 — Escrituras del ciclo.** Acta nueva, 3 expedientes de CP con backup `.bak-20261106`, 3 lecciones en `lecciones_ledger.jsonl`, 1 parche de skill, 1 bloque en `pendientes.md` (con backup). Sin commit. Sin tocar sistema, servicios ni n8n.

---

## 4. Estado de la cadena incidente → lección → mejora

- **Respaldo del informe (`67d5fcc5b69e`)** → incidente ×5 en 7 días → lección «el respaldo se acredita por el resultado» → mejora aplicada (commit `8b2404c`, router 01-11) **parcial**: cubre motor ausente, no motor que responde mal.
- **Firma con fecha (CP-018)** → 7 incidencias para 1 defecto → patrón en incubación, sin reparación → cada semana se pierde la comparación; la única fuente semanal útil (`cron_incidents`) queda degradada.
- **Cierre de incidencias (CP-017)** → cierre aceptado 28-10, recaída 01-11 → lección de criterio (días sin recurrencia) → sin cambio de código; el riesgo es dar por reparado lo que solo dejó de fallar unos días.
- **Juez de calidad** → 4/7 sin veredicto, 3 con verde → sin lección nueva (ya está en CP-010) → deuda abierta con el usuario.
- **Vigilante Telegram (CP-016)** → 0 reinicios en 7 días → antídoto sostenido → pendiente de una prueba con red caída y host encendido para subir de nivel.
- **Ficha de perfume 03-11** → nota intermedia leída como final, 28.250 tokens, 2 ficheros sobrescritos → lección + parche de skill → condición de falsación fijada para abrir CP si se repite.
- **`7b5207` (`-15`)** → ejecución adoptada sin estado terminal → sin lección asignada todavía → familia CP-015, vigilar la próxima caída de host con ejecución en vuelo.
