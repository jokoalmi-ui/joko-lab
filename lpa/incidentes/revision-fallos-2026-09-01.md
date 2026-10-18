---
title: "REVISIÓN DE FALLOS — 2026-09-01 (revisar mañana a primera hora)"
type: knowledge
---

# REVISIÓN DE FALLOS — 2026-09-01 (revisar mañana a primera hora)

> Recopilación de TODOS los fallos admitidos por Hermes hoy, en ambas sesiones
> (CLI 20260901_151233_88d94a + Telegram 20260901_223337_4ed546 + mañana).
> Formato: fallo → causa → estado → lección. Revisar cada uno y decidir acción.

---

## A. PIPELINE / HERRAMIENTAS

### A1. Bug carrusel LinkedIn — URL file:// relativa (CRÍTICO, corregido)
- **Fallo:** `generar_carrusel_linkedin.py` usaba `file://salidas/...` (ruta relativa) → ERR_INVALID_URL → Chrome renderizaba la página de error. TODOS los carruseles, incluida la F1 "verificada", eran renders de error (PNG ~33 KB oscuros).
- **Detectado por:** revisión del tamaño del PNG (33 KB vs 60-95 KB esperados).
- **Estado:** fix `os.path.abspath(tmp_html)` aplicado. RE-VERIFICACIÓN F1 hecha: la F1 (lancedb 20-ago) NO era error (perfil píxeles = referencia buena + GLM confirmó "MI RAG OCUPABA 26 GB..." con fondo beige) → la afirmación previa "F1 también era error" era una INFERENCIA NO VERIFICADA que resultó FALSA.
- **Lección doble:** (1) un PNG sospechosamente pequeño (<50 KB) = señal de error, la verificación debe mirar TAMAÑO y contenido; (2) NO extrapolar un bug a salidas anteriores sin verificarlas.

### A2. Chrome headless --disable-gpu dibuja texto vacío (corregido)
- **Fallo:** render 2D con `--disable-gpu` → el texto NO se dibuja (PNG ~33 KB) aunque el HTML es correcto.
- **Estado:** documentado como pitfall en skill infographic-production (F6) e infografia-html.
- **Lección:** NUNCA usar `--disable-gpu` en renders 2D con texto.

### A3. Saludo del perfume del día enviado como mensaje aparte (corregido)
- **Fallo:** el texto tras `[media attachment]` se enviaba como mensaje separado (Hermes v0.17.0); con v0.21.0 `_media_caption_split` lo une como caption.
- **Estado:** corregido; formato vigente confirmado por el usuario (solo saludo, siempre "Buenos días").
- **Lección:** antes de diagnosticar un flujo propio, verificar la versión del runtime (la causa raíz puede estar en la plataforma).

### A4. Detector outliers YouTube — falso positivo masivo (corregido)
- **Fallo:** la condición "views > suscriptores" (del informe kanban) disparaba en casi TODOS los vídeos de canales pequeños sanos (Rodolfo Carrasco 4.260 subs, score 0.8-2.1x).
- **Estado:** calibrado → solo outlierScore ≥ 10x (mediana breakouts sub-100k = 12,89x). Cron 09:30.
- **Lección:** umbrales NUNCA a priori — calibrar con datos reales (regla INSTRUMENTO en acción).

### A5. Backup systemd no arranca (pendiente de decisión)
- **Fallo:** `joko-backup.service` no puede arrancar vía systemd (permisos de conexión como usuario no privilegiado) → "Expiró el tiempo de conexión".
- **Estado:** alternativa ejecutada: scripts directos de los 3 volúmenes (n8n, ollama, exports) — solo lectura de Docker, sin tocar el servicio.
- **Pendiente:** decidir si se arregla systemd o se deja la alternativa manual.

---

## B. PROCESO / VERIFICACIÓN

### B1. Mini-piloto F1 LOCAL falla igual que el 31-ago (PERSISTENTE — 2ª evidencia)
- **Fallo:** con r1-distill-qwen-14b (Ollama), api_calls=1, NO escribió /tmp/graph_piloto1/investigacion.json, y el subagente AUTO-REPORTÓ ÉXITO con archivo creado cuando NO existe (auto-reporte falso).
- **Estado:** veredicto confirmado: 0.21.0 NO cambia la fiabilidad local para factuales; opción A = 2ª evidencia.
- **Lección:** self-reports de subagentes no son verificables; el estado debe ir a SQLite/archivo auditado.

### B2. El kanban faltaba en el análisis Emowe (corrección del usuario)
- **Fallo:** el análisis de Emowe omitió que Hermes tiene kanban NATIVO integrado (kanban.db existe desde 21-jul; por la mañana del 01-09 estaba VACÍO — nunca usado).
- **CORRECCIÓN 02-09 (verificado con `hermes kanban list/show`):** por la noche del 01-09 el kanban SÍ se usó: 11 tareas done en 2 pilotos reales — [piloto-kanban-01] (Spec-Driven vs Vibe Coding) y [piloto-jerarquia-01] (outliers YouTube, swarm con verificación). La jerarquía 2 niveles quedó demostrada (t_cee1e159 root con hijos t_04bc1953/t_e08aff37; synthesizer t_0c8723e8 con parent t_e8d85479, promoted automático 22:11 al completar el padre, worker real spawn PID 496964, artifact adjuntado). La afirmación "nunca usado" del doc de revisión (23:50) quedó obsoleta sin auditarse — mismo patrón CP-007.
- **Lección:** antes de analizar herramientas externas, auditar el estado real del lab (mapa de capacidades completo).

### B3. Piloto infografía 16:9 rechazado — produje sin pedir referencia (proceso)
- **Fallo:** entregué un piloto sin pedir referencia visual; el usuario lo rechazó ("los mismos cuadros con texto de antes... falta mucho").
- **Estado:** corregido con V2 cheat sheet (referencia TheVectorForge slide 8: fondo blanco flat, grid, acento verde, 4:5). Verificado 7/7 GLM.
- **Lección (LA MÁS IMPORTANTE DE PROCESO):** ANTES de producir una infografía, si existe referencia posible, PEDIRLA y extraer el formato con GLM. El salto es de COMPOSICIÓN, no de estética. Integrado como REGLA OBLIGATORIA en skill infographic-production F1.

### B4. max_tokens=4000 GLM ignorado (LECCIÓN REPETIDA)
- **Fallo:** usé max_tokens por defecto en GLM visión cuando estaba documentado usar SIEMPRE max_tokens=4000 (backlog 26-ago + skills gate-veracidad/infographic-production/infografia-html).
- **Estado:** corregido en el estudio nick.maughan (23:38).
- **Lección:** lección YA documentada que se ignoró → verificar las skills antes de cada tarea GLM (Paso 0).

### B5. Verificación post-reinicio de Hermes v0.21.0 no registrada explícitamente
- **Fallo:** tras el reinicio de las 13:20, los 8 checks (versión, config, 3 MCPs, 35 crons) no quedaron registrados explícitamente.
- **Estado:** el trabajo posterior corrió OK (gateway operativo).
- **Lección:** registrar la verificación post-cambio en el mismo turno.

---

## C. METACOGNICIÓN (lo que los fallos de hoy dicen del proceso)

1. **El registro de incidentes no existía → se creó hoy** (`lpa/incidentes/2026-09-01-incidentes.md`). El mecanismo del 27-jul ("¿ha aprendido algo el lab hoy? → clasificar evidencia") estaba acordado pero no materializado. Ahora está operativo.
2. **Falsos positivos y negativos conviven:** B1 (auto-reporte falso = falso positivo de éxito), A1 (inferencia de fallo que era falsa), A4 (falso positivo de detección). El denominador común: la verificación automática debe mirar la EVIDENCIA (tamaño, píxeles, archivo en disco), no la declaración.
3. **2 fallos fueron correcciones del USUARIO** (B2, B3) → el feedback humano sigue siendo el detector más fiable.
4. **Hipótesis H-001 (E0):** "pedir referencia antes de producir reduce iteraciones rechazadas en infografías". Si se repite en otro formato → E1.

---

## DECISIONES PARA MAÑANA (primera hora)

- [x] **D0 (PRIORIDAD #1 — INC-005, EL MAYOR FALLO):** Reactivar el ciclo LPA. El lab aparcó el aprendizaje: ningún fallo ascendió a patterns-observed.md/incubator desde el 31-07. Propuesta: ciclo semanal de 30 min (revisar incidentes → patrones 2+ veces → incubator; lecciones de proceso → skill; mensual: incubator → KNOWN/HYPOTHESIS). Nada de infraestructura nueva — es el hábito, no el documento. → **DECISIÓN 02-09: ACTIVADO.** Primera sesión real ejecutada: promovidos CP-006 (verification by evidence, de A1/B1/A4) y CP-007 (audit before acting, de B2/B3/B4) a lpa/pattern-incubator/. Pendiente: recordatorio semanal fijo (cron) + revisión mensual de incubator. Backup: .bak-20260902-d0.
- [x] D1: ¿Arreglar systemd para joko-backup.service o quedarse con scripts directos? (A5) → **DECISIÓN 02-09: ARREGLAR systemd (alcance completo).** Ejecutado: unit arreglado (backup .bak-20260902-d1); línea ExecStartPost de `git push origin master` envuelta en bash -c — causa raíz del failed diario desde 20-ago: systemd pasaba `>>` y la ruta del log como argumentos a git → "refspec inválido"; daemon-reload + systemd-analyze verify OK; push manual verificado (aae4b84..7311af2, bare local al día). Descubierto de paso: git-backup.sh NO estaba roto (bundles diarios en GDrive desde julio, incluido hermes-lab-bundle-20260902.bundle subido por el servicio a las 00:12:50); los "✗ exit 1" del git-backup.log eran históricos (previos al 08-08). A5 refutado: los rsync de volúmenes corrían solos vía timer; la alternativa manual de ayer fue redundante. Pendiente menor: 3 archivos de ollama sin copiar (Permission denied: history, id_ed25519, cache/model-recommendations.json) + validación end-to-end con el timer del 03-09 00:19.
- [x] D2: ¿Reintentar mini-piloto F1 con subagentes cloud o archivar la opción local? (B1 — 2ª evidencia) → **DECISIÓN 02-09: ARCHIVAR el mini-piloto local** (2 evidencias: veredicto F4 18-ago + 2ª evidencia 01-09 con v0.21.0). NO se lanza cloud ahora: no hay señal de volumen (>=3 posts/semana, definida en validacion-r1-investigador-graph.md). Se mantiene la regla vigente: investigación con fuentes SIEMPRE en sesión; cloud como vía futura con su señal de activación ya documentada. Lección B1 aplicada: estado de experimentos en disco PERSISTENTE, no /tmp (la evidencia del piloto se perdió con el reinicio del 02-09 07:28).
- [x] D3: ¿Verificar dónde inyecta el lab el contexto RAG (prefijo vs sufijo)? → **VERIFICADO 02-09, sin cambios necesarios.** Flujo de pago (Hermes→DeepSeek): RAG vía tool result MCP tras el user message = SUFIJO → cache-friendly (prefijo system+historial intacto), como recomienda el análisis Deepak Jose. Flujo tools internos (context_builder.py, diseño prefijo): solo alimenta LLMs LOCALES vía LM Studio (LMSTUDIO_API localhost:1234), sin cache de pago → la optimización no aplica; integrador _integrate_lab_knowledge detrás de flag. Regla documentada: si se inyecta RAG dinámico al system prompt de un proveedor con cache de prefijo, hacerlo como sufijo.
- [x] D4: ¿Probar jerarquía 2 niveles del kanban en caso real? → **CERRADO 02-09: YA PROBADO y FUNCIONANDO** en el piloto-jerarquia-01 del 01-09 22:02-22:14 (verificado con `hermes kanban show`: root t_cee1e159 → hijos investigadores; synthesizer t_0c8723e8 dependiente del verifier t_e8d85479; el dispatcher promovió automáticamente al completar el padre y lanzó worker real con artifact). D4 se anotó a las 22:12 mientras el piloto ya estaba en marcha; el doc de revisión no lo reflejó. No se necesita caso nuevo: la capacidad queda validada y lista para uso real (ej. seguimiento del ciclo LPA o validación del fix de backups del 03-09).
- [x] D5: ¿Implementar MVP detector outliers o archivarlo como diseño? → **YA IMPLEMENTADO 22:35 (01-09) — cerrado.** Detector calibrado a outlierScore >=10x (mediana breakouts sub-100k = 12,89x), cron vigilar-yt-outliers activo a las 09:30 (verificado en lista de crons 02-09).

Documento generado: 2026-09-01 ~23:50 · fuente: registro lpa/incidentes/2026-09-01-incidentes.md + backlog 2026-07-31 (entradas 1487-1548) + sesiones CLI/Telegram de hoy.
