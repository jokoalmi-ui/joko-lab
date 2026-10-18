---
title: "Itinerario de revisión e implementación — Joko Lab (2026-08-20)"
type: operations
---

# Itinerario de revisión e implementación — Joko Lab (2026-08-20)

fecha: 2026-08-20
autor: agente (jokoalmi) + análisis en disco
tipo: itinerario / operaciones
estado: vigente (revisar con cada corte)

Objetivo: qué implementar de lo "en estudio", SIN duplicar lo ya hecho.
Método: cada ítem verificado en disco (tools/, scripts/, skills/, MCPs, crons)
antes de clasificarlo como pendiente.

---

## PARTE 1 — VERIFICADO YA IMPLEMENTADO (NO re-hacer, NO duplicar)

Verificado en disco con salida real (2026-08-20):

| Ítem (futurible) | Dónde vive | Fecha |
|---|---|---|
| Hybrid RAG con RRF | `tools/search.py` (FTS/BM25 + vectorial, fusión RRF, `hybrid_rank`) | 05-ago |
| Reranking CrossEncoder | daemon joko-reranker.service (bge-reranker-v2-m3, puerto 8765) | 02-ago |
| Evaluación formal RAG | `tools/evaluar_rag.py` (recall@5 100%, 8 consultas) | 12-ago (OP-007) |
| RAG multimodal CLIP | `tools/indexar_imagenes.py` (tabla joko_images) | 12-ago (OP-006) |
| RAG cubre biohacking | fix indexer VAULT_EXTRA (+91 registros) | 12-ago (OP-007) |
| Memory episódica MEP-001 | episodic_ledger + memoria-episodica.sh + RULE-011 | 20-ago |
| Skill Bundles 4/4 | /lab-diag, /perfume-dia, /vigilar-ig, /bolsa | 20-ago |
| MCP BD propias | lab-db (SQLite) + lancedb (RAG joko_notes) | 18/20-ago |
| Gate de veracidad 5 fases | verificador + contrastar + verificar_research (233 tests) | 16-ago |
| Mover crons batch a local | router respeta MAX_TOKENS; informe-diario local | 14-ago |
| Ledger de lecciones | `tools/registrar_leccion.py` + lecciones_ledger | 14-ago |
| Clasificador sensación perfume | `tools/clasificar_sensacion.py` (144/152) | 12-ago (OP-004) |
| Compactación skills | 4 skills grandes 98→55K (OP-008); perfume 54K | 12-ago |
| Capa metacognitiva F1-F2 | adoptado (metacognitive-layer-diseno.md) | 05-ago |
| Decisión estilo contenido | paneles light LinkedIn / cuaderno | 14-15-ago |
| Mejora reindexado (optimize) | ⚠️ PARCIAL: compactado manual 13GB→311MB; optimize() NO en script | 11-ago |

NOTA: el "futurible Hybrid RAG con RRF" de codewithbrij (19-ago) NO es pendiente
— está implementado desde 05-ago. Idem "Reranking", "Evaluación formal RAG",
"CLIP imágenes", "exponer BD como MCP" (hoy, completado).

---

## PARTE 2 — ITINERARIO DE IMPLEMENTACIÓN (ordenado por incidencia en el LAB)

Criterio: (1) toca funcionamiento diario, (2) señal de activación disponible
hoy, (3) coste/esfuerzo, (4) no depende de hardware nuevo. Prioridad del
usuario: LAB primero (directiva 16-ago).

### 🟢 FASE A — AHORA (funcionamiento diario, señal clara, bajo esfuerzo)

A1. **Query + Summary Indexing RAG** (futurible dailydoseofds_ 11-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: indexar preguntas posibles (query) y resúmenes de doc (summary)
      además del chunk; probar si las búsquedas de estado mejoran.
    - Señal: búsquedas de estado del lab ("¿qué decidimos sobre X?") — hoy
      funcionan (recall 100%) pero con indexing se afina el top-1.
    - Esfuerzo: bajo (ampliar indexer.py + search.py, BGE-M3 ya disponible).
    - Verificación: evaluar_rag.py con las 8 consultas + casos de estado.
    - Criterio de aceptación: recall@5 no baja; top-1 mejora en ≥2 consultas.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago (ver entrada backlog del día):
      tablas joko_summaries (842) + joko_queries (12.584) en el mismo LanceDB;
      índice cosine creado; search.py fusiona con _origen="qs"; recall@5 100%
      (8/8, sin bajar); consultas de estado añaden docs nuevos relevantes
      (reasoning-gate → RULE-003 + gate-005; cafeína → OBS-035-decisiones).
      Pitfalls anotados: (1) tablas nuevas necesitan create_index(cosine) —
      sin índice, LanceDB usa L2 y las distancias no son comparables con 1-d;
      (2) umbral 0.55 demasiado alto para queries reales → 0.35; (3) evaluar_rag
      no tiene --device: si GLM ocupa VRAM, usar CUDA_VISIBLE_DEVICES="" (CPU).

A2. **LLM-as-Judge formal** (futurible #3, validado por 3 fuentes) ✅ IMPLEMENTADO 20-ago
    - Qué: 2 modelos independientes juzgan calidad (no solo veracidad) de
      respuestas del pipeline; cerrar el bucle OBS→EXP→DEC.
    - Estado real: parcial (gate valida veracidad; juez GLM existe).
    - Esfuerzo: medio (script juez + integración en pipeline).
    - Verificación: juicio sobre N respuestas reales vs veredicto del usuario.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: `tools/llm_as_judge.py`
      (2 jueces: glm-4.6v-flash + openai/gpt-oss-20b, ambos locales 0€;
      5 dimensiones: fidelidad/completitud/relevancia/claridad/utilidad;
      veredictos PASA/REVISA/FALLA/DISCREPANCIA; UN_JUEZ honesto si falta
      VRAM; regla determinista: fid/completitud ≤1 → FALLA, el LLM tiende a
      suavizar). Validado con 3 casos reales (correcta→PASA 4.4, incompleta→
      REVISA, invento→FALLA) + 4 pruebas unitarias de consolidación.
      LIMITACIÓN REAL: con GLM cargado (7.87GB) gpt-oss no cabe en 12GB →
      modo UN_JUEZ; para 2 jueces hay que descargar GLM antes (LM Studio).
      Pendiente de decisión: integrar en el pipeline (informe diario /
      análisis / respuestas del agente) cuando el usuario lo pida.

A3. **Bot Mode de Hermes / A2A** (futurible prioritario, bloqueado) ⏳ CHECKLIST PREPARADO 20-ago
    - Qué: agentes persistentes multi-rol; formalizar colaboración
      CLI↔Telegram con A2A.
    - Señal: requiere Hermes ≥0.20 (lab en 0.17.0). Revisar el 23-ago
      (hito 0.21.0) — NO implementar hasta actualizar.
    - Acción ahora: preparar checklist de verificación de upgrade
      (skills/config/crons/bundles/MCPs) para el día del salto.
    - ✅ HECHO 20-ago: `04-operations/checklist-upgrade-hermes-021-20260820.md`
      (11 pasos: snapshot previo, backup config, diff post-upgrade, bundles 4/4,
      MCPs 3/3, crons, skills, hermes mcp test lancedb). Ejecutar el 23-ago con
      confirmación del usuario.

A4. **Monitor YT (5 canales)** (futurible 12-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: vigilar Nichonauta ⭐, IBM, Rodolfo Carrasco, Fazt Code,
      hdeleon.net — mismo patrón que vigilante IG (cron + aviso).
    - Esfuerzo: bajo-medio (script fetch_transcript + cron + aviso TG).
    - Verificación: primer aviso real con transcripción.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: `tools/monitor_yt.py`
      (feeds RSS públicos, channel IDs verificados con salida real — 5/5 feeds
      OK; state en ~/.hermes/state/monitor_yt_state.json; patrón watchdog:
      stdout vacío = silencio) + wrapper `~/.hermes/scripts/vigilar-yt.sh` +
      cron `vigilar-canales-yt` (c84f8d890630, diario 09:15, deliver=telegram,
      no_agent). Primera pasada: 25 vídeos marcados como vistos (los actuales);
      2ª ejecución en silencio (correcto). Avisos futuros solo con vídeos nuevos.

A5. **optimize() en reindexado RAG** (GAP real 11-ago, pendiente) ✅ IMPLEMENTADO 20-ago
    - Qué: añadir `optimize()` al final de rag-reindex.sh/indexer.py para
      evitar acumular versiones LanceDB (caso real: 259 versiones = 13 GB).
    - Esfuerzo: bajo (1 línea en el script + verificación).
    - Verificación: wc del .lancedb antes/después en el próximo reindex.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago. HALLAZGO REAL: el fix del
      12-ago era INCOMPLETO — rag-reindex.sh tenía solo `t.optimize()` sin
      `cleanup_old_versions` → joko_notes con 453 versiones = 26 GB (peor que
      el caso original). Corregido: el bloque de compactación ahora itera TODAS
      las tablas (joko_notes, joko_summaries, joko_queries, joko_images) con
      optimize() + cleanup_old_versions(older_than=0). Resultado: 26 GB → 320
      MB (98.8%), versiones 453→1-2, recall@5 100% (8/8) intacto. Skill
      local-rag actualizada con el pitfall. Regla de verificación: du -sh
      ~/joko-lab/.lancedb debe quedar ~300-400 MB tras el daily.

### 🟡 FASE B — PRÓXIMA (ampliación de capacidades, señal clara)

B1. **Apps con IA — instalar Ionic** (90% listo, falta 1 paso) ✅ IMPLEMENTADO 20-ago
    - Qué: `npm install -g @ionic/cli` para apps móviles. Web/escritorio ya
      no necesita nada. 5-10 min.
    - Señal: decidido 15-ago (futurible "capacidad de crear apps con IA").
    - Requiere confirmación (instalación global npm).
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: `npm install -g @ionic/cli`
      → Ionic CLI 7.2.1 en ~/.npm-global/bin (sin sudo, PATH ya lo incluye).
      Prueba real: app blank React creada + `npx ionic build` ✓ (7.01s, dist/
      generado). ⚠️ PITFALL: la plantilla `--type=angular` NO compila con el
      node del sistema (22.22.1 < 22.22.3 requerido por Angular CLI) — usar
      `--type=react` (Vite) o actualizar node antes de Angular. Capacitor
      disponible para iOS/Android (native-run/cordova-res no instalados —
      solo hacen falta para publicar en stores).

B2. **Pipeline LinkedIn Lab** (proyecto planificado 12-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: generar_carrusel_linkedin.py + plantilla maurys.html + skill
      linkedin-carrusel-lab. Estilo YA decidido (paneles light).
    - Esfuerzo: medio (script + plantilla + render + verificación GLM).
    - Desbloquea: marca personal para empleo + feedback loop de aprendizaje.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago:
      `~/joko-lab/research/linkedin-lab/generar_carrusel_linkedin.py` (6
      arquetipos maurys: gancho/concepto/como/por_que/escala/cta; --demo con
      caso A5 real 26GB→320MB; --guion guion.json para custom; salidas en
      research/linkedin-lab/salidas/<fecha>-<slug>/).
      `plantilla-maurys.html` (1080×1350, crema #F5EFE6 + negro + naranja
      #FF7A00, Inter, marca Joko Lab, densidad baja).
      Skill nueva `linkedin-carrusel-lab` (pipeline + datos reales + pitfalls).
      Demo verificada con browser_vision: slide 1 (gancho) 6/6, slide 3
      (métricas) 5/5 — sin cortes ni solapamientos.

B3. **Inpainting local ComfyUI** (idea M12-05, 20-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: workflow de retoque (seleccionar→sin prompt=eliminar, con
      prompt=añadir) — el lab ya tiene generador SDXL, falta retoque.
    - DÓNDE: nodos inpaint sobre gen_comfy.py. PARA QUÉ: corregir artefactos
      (tipografía SDXL), limpiar fondos sin regenerar imagen completa.
    - Esfuerzo: medio (workflow ComfyUI + integración en skill).
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: `~/ComfyUI/gen_comfy_inpaint.py`
      (workflow LoadImage+LoadImageMask→VAEEncode→SetLatentNoiseMask→KSampler
      con --denoise→VAEDecode; máscara blanco=retocar; --prompt vacío=eliminar;
      --mascara-invertida). Prueba real con imagen generada SDXL (botella de
      perfume): ELIMINAR OBJETOS ✓ (botella entera→fondo limpio, verificado
      con GLM visión); AÑADIR/MODIFICAR ✓. ⚠️ LÍMITE REAL documentado:
      ELIMINAR TEXTO NO funciona con SDXL base — el modelo reinterpreta la
      zona como etiqueta y regenera texto inventado ("P.ERME"→"RAIME"→"BERME").
      Para borrar texto limpio haría falta modelo inpaint dedicado o
      inpaint-controlnet (futurible, no urgente). Skill generacion-imagen-local
      actualizada con el flujo + el límite. ComfyUI parado tras la prueba
      (bajo demanda).

B4. **Checklist de calidad visual pre-publicación** (M12-04, 20-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: 6 verificaciones (foco, legibilidad, coherencia cromática,
      composición, nitidez, sin distracciones) como gate de CALIDAD visual
      (complementa el gate de VERACIDAD).
    - Esfuerzo: bajo (checklist en skill generacion-imagen-local).
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago:
      `tools/checklist_calidad_visual.py` — 5 checks OBJETIVOS con PIL puro
      (foco Laplaciano, nitidez bordes, composición márgenes con bordes
      fuertes, coherencia cromática, distracciones) + 6º legibilidad con GLM
      visión (--vision, formato SÍ/SÍ/NO interpretado correctamente).
      Umbrales CALIBRADOS con datos reales (nunca a priori): foco 300 (slide
      nítida 1086 vs blur 30 = 191), nitidez 1% (slide limpia 2.1%),
      margen 2% con bordes >150 ignorando contorno PNG. Verificado: slide
      carrusel → PASS 6/6 (con GLM), blur 12 → REVISAR, blur 30 → FAIL,
      infografía validada → PASS 5/5 (sin falsos negativos). Skill
      generacion-imagen-local actualizada con la sección del gate.

B5. **Tabla ajuste→efecto→aplicación SDXL** (M12-04, 20-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: catálogo de presets (Dark vs luminoso, vibrante vs fríos, Wide vs
      cerrada, Vivid vs suave) con efecto medido — elegir con criterio.
    - Esfuerzo: bajo (doc/skill generacion-imagen-local).
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago con datos REALES medidos:
      4 pares generados (misma semilla 1234, mismo prompt base, solo el
      ajuste) y medidos con PIL (brillo/saturación/contraste/foco/nitidez).
      Tabla en research/presets-sdxl/tabla-ajuste-efecto-sdxl.md + 8 imágenes
      de referencia en research/presets-sdxl/. Hallazgos: Dark/Luminoso es el
      ajuste más potente (Δbrillo +63); vibrante=saturación (-41%) y
      vivid=foco (-587) NO son lo mismo; wide/cerrada no se mide por píxel
      (verificar con GLM); luminoso baja saturación (antagónico a vibrante);
      producto con textura → Vivid, nunca Fríos. Skill generacion-imagen-local
      actualizada (sección presets + reglas). ComfyUI parado tras la prueba.

B6. **Arquitectura de prompt en 6 componentes** (M12-06, 20-ago) ✅ IMPLEMENTADO 20-ago
    - Qué: formalizar en skill prompt-engineering las plantillas
      (contexto/instrucción/estilo/longitud/público/restricciones).
    - Esfuerzo: bajo (documentación + plantillas).
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: sección nueva
      "Arquitectura de prompt en 6 componentes" en la skill
      prompt-engineering (tabla de componentes + 4 reglas + diagnóstico
      por componente) + referencia reutilizable
      `references/prompt-6-componentes.md` (plantilla rellenable, ejemplo
      resuelto con el caso B2 real, tabla de diagnóstico). No duplicaba
      nada existente (verificado: la skill tenía patrones por tarea y
      Prompt Project, pero no los 6 campos canónicos como checklist).

B7. **Open Deep Research** (media-alta, TFM antes de octubre) ✅ IMPLEMENTADO 20-ago
    - Qué: investigación con fuentes citadas (síntesis + citas en vez de
      meter todo el contexto). Ataca el cuello de botella nº1 (coste de
      contexto 99.7%).
    - Señal: TFM (antes de oct) — estudiar cuando toque investigar en serio.
    - ✅ ESTADO: IMPLEMENTADO y verificado 20-ago: `tools/deep_research.py`
      (pipeline: fuentes → síntesis GLM local con citas [S1..Sn] → informe
      compacto con métrica de ahorro) + skill nueva `deep-research-lab`
      (research/). Prueba real "Graph vs Loop Engineering" con 3 fuentes:
      síntesis con citas correctas (design-time vs runtime), matiz honesto,
      AHORRO 85% de tokens de contexto (2510→365). investigacion-web
      actualizada (enlace entre skills: corta vs seria). Pitfall
      verificado: ddgs directo está anti-bot (anomaly/challenge) — usar
      web_search del agente o --urls/--fragmentos.

### 🔵 FASE C — MADURACIÓN (cuando aparezca la señal o el hardware)

C1. **RAG semántico sobre BD SQLite** ("parecido a..." en perfume/café con
    BGE-M3) — señal: cuando la BD crezca o las consultas sean ambiguas.
C2. **Fan-out/fan-in paralelo GLM** para batches de visión (15 slides ~3x
    más rápido) — señal: cuando el batch de imágenes sea recurrente.
C3. **Checkpoints formales pausar/reanudar** — para refactors largos.
C4. **Knowledge graph multi-hop RAG** — consultas con saltos múltiples.
C5. **Docling** (parser PDF layout-aware) — señal: TFM/bibliografía/BBK.
C6. **Motion Canvas** (infografías animadas TS) — señal: retomar pipeline vídeo.
C7. **Speculative decoding n-gram / MTP** — señal: LM Studio exponga flags;
    batch iterativo con plantillas repetidas.
C8. **Tailscale** — señal: trabajar en remoto sin exponer puertos.
C9. **CodeGraph** (RAG de código) — señal: el código del lab crezca.
C10. **Google Workspace MCP oficial** — confirmado «Si» 18-ago; hacer cuando
     la integración con Gmail/Calendar del lab lo requiera.
C11. **Screenpipe** (memoria de pantalla/audio) — baja prioridad (privacidad
     y recursos); el lab ya tiene sesión_search.
C12. **B1/B2/B3 benchmark interno** — post-corte EXP-HEL (28-ago).
C13. **Métricas de seguridad en evaluador** (PII, toxicidad) — baja prioridad
     (lab local/personal).
C14. **Gemma 26B A4B + llama.cpp** — cuando se quiera subir nivel local
     (4x R1); requiere llama.cpp.
C15. **Meta Muse Glimmer 30B** — cuando salgan GGUF llama.cpp (medir, no hype).
C16. **PEFT/LoRA** — post-GPU 24GB (fine-tuning local).
C17. **RL para agentes (GRPO/GEPA)** — roadmap largo plazo, GPU 24GB.
C18. **GPU 24GB (RTX 3090 usada ~840€)** — el salto de hardware cuando toque;
     verificado 12-ago con precios y estafas documentadas.
C19. **i9-9900K + Z390** — pendiente de montar (CPU, no resuelve VRAM).

---

## PARTE 3 — MANTENIMIENTO (pendientes pequeños ya identificados)

- 9 sensaciones sin rellenar en perfume-ia (A Grove, Afternoon Swim, Oud
  Satin Mood, Interlude Man, Pegasus, Vibrato, Etruscan Water, Gntonic) —
  requiere UPDATE a BD con confirmación.
- Rellenar batch codes de 320 perfumes batch VACÍO (rellenar_batch_codes.py).
- 4 skills >90K pendientes de compactar cuando toque (diagnostico-stack-local,
  hermes-expert, founderz-seguimiento, research-paper-writing).
- Research sin referencia (19 archivos): revisar archivar vs enlazar
  (detectar-sin-uso, informe 11-ago).
- Revisar uso Gemini (INT-003, deadline 03-sep).

---

## PARTE 4 — HITOS Y REVISIONES

- 23-ago: revisar Hermes 0.21.0 (A3 — Bot Mode desbloqueado) + verificar
  bundles/MCPs/crons tras upgrade.
- 28-ago: corte EXP-HEL fase 2 → C12 (benchmark B1/B2/B3).
- 03-sep: revisión uso Gemini (INT-003).
- TFM antes de octubre: B7 (Open Deep Research) + C5 (Docling).
- Revisión mensual del itinerario: criterio anti-FOMO (futurible #8) —
  archivar lo que no resuelve un problema ni sirve a TFM/entrevistas.

---

## Nota honesta

La Parte 2 es un PLAN, no un compromiso de ejecución. Cada ítem requiere su
propia confirmación antes de tocar el sistema (ninguno se implementa solo).
La Parte 1 es la que evita duplicar: verificar en disco ANTES de marcar un
futurible como pendiente (patrón ya validado 3 veces: Proxy Atómico, Hybrid
RAG, expone BD como MCP).
