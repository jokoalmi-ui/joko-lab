---
title: "🔄 HANDOFF 20-AGO-2026 (mañana) — Telegram → CLI"
type: operations
---

# 🔄 HANDOFF 20-AGO-2026 (mañana) — Telegram → CLI

**Fecha:** jueves 20-08-2026 · sesión Telegram de mañana (08:16 → ~11:35)
**Creado para:** retomar en CLI sin perder contexto

---

## 1. RESUMEN EJECUTIVO DEL DÍA

Todo lo hecho esta mañana está [VERIFICADO] y registrado. Nada quedó a medias
salvo lo indicado en "PENDIENTES". El estado del lab es estable.

**Temas tocados**: perfume del día (Akdeniz) + correcciones de skill ·
sueño fila 18 (captura procesada con GLM) · arranque LM Studio · 8 análisis
de contenido (5 IG + 3 YT) · regla de costes en skill · 4 futuribles
consolidados · 3 bundles de Hermes creados.

---

## 2. ARCHIVOS NUEVOS (todos verificados)

### research/ (10 archivos + infografía)
```
analisis-ai-coach-john-llm-eval.md          (métricas evaluación LLM)
analisis-codewithbrij-top5-rag.md           (Top 5 RAG Architectures)
analisis-ds-ai-ketan-mcp-ecosystems.md      (MCP Fundamentals/Architecture)
analisis-nichonauta-atomic-ai.md            (ayer, batch 20b)
analisis-nichonauta-monetizacion.md         (ayer, batch 20c)
analisis-nichonauta-ngram-mtp.md            (ayer, batch 20a)
analisis-nichonauta-reto-modelos-2b.md      (hoy, Gemma4-2B/Qwen3.5-2B)
analisis-nichonauta-speculative-decoding.md (hoy, comparativa SD)
analisis-shiva-bytes-26-skills.md           (26 AI skills)
analisis-skill-bundles-hermes.md            (feature nativa Hermes)
infografias/perfume-del-dia-20260820/       (HTML+PNG+frasco+fondo ComfyUI)
```

### Backups del día (RULE-008, todos presentes)
```
backlog: 20260820a · 20b · 20c · ig · ig2 · futuribles · mcp · nichonauta2
sueño:   seguimiento-prueba1.md.bak-20260820-sueno
skill:   instagram-monitor/SKILL.md.bak-20260820-costes
```

### Bundles de Hermes (NUEVOS, feature nativa 0.17.0)
```
~/.hermes/skill-bundles/perfume-dia.yaml  → /perfume-dia (1 skill)
~/.hermes/skill-bundles/vigilar-ig.yaml   → /vigilar-ig  (2 skills)
~/.hermes/skill-bundles/lab-diag.yaml     → /lab-diag    (3 skills)
```
Verificados con `hermes bundles list` + `show` + arranque del flujo (Paso 1
fecha/clima OK). ⚠️ El disparo por slash command desde gateway NO se ha
probado aún — primera invocación real pendiente.

---

## 3. BACKLOG — ESTADO

- Archivo: `joko-lab/04-operations/backlogs/2026-07-31-backlog.md`
- Futuribles consolidados del día: **F1 bundles Hermes (INMEDIATO, HECHO) ·
  F2 ROUGE (menor) · F3 RRF (validado) · F4 bundle lab-diag (HECHO)**
- Entradas de análisis del día: 8 (5 IG + 2 YT Nichonauta + resumen general)
- DIRECTIVA MAESTRA intacta (línea 441)

---

## 4. SUEÑO — FILA 18 (noche 19→20-ago) ✅ COMPLETA

```
| 18 | 20-ago | | | | 7 | 7 | | | 🟢 8 (Buena, 87 pts +16) |
Noche 19→20-ago: 7h59m (23:54→07:52), 87 pts (↑16 vs 71),
REM 17% (1h21m) · Ligero 55% (4h23m) · Profundo 28% (2h15m) ·
2 despertares · FC 51 · SpO2 97 · Resp 98 · foco 7 · energía 7
```
Verificado aritméticamente (81+263+135=479min=7h59m ✅).
**Lectura**: gran recuperación tras la caída de ayer (estrés del juicio era la causa).

---

## 5. SKILLS MODIFICADAS

1. **instagram-monitor** (backup `.bak-20260820-costes`):
   - NUEVA regla de costes: análisis después de las 12:00 → router local
     gpt-oss (`llm-router.sh batch`) para el resumen; visión ya es GLM local.
     Antes de las 12: flujo normal. Excepción: análisis interactivo en el momento.
   - Se corrigió un patch que duplicó la sección → quedó 1 sola sección (verificado).

2. **instagram-carruseles-analisis** (sin cambios de hoy; ya tiene el patrón
   alt/caption del DOM validado el 20-ago y el pitfall de capturas estrechas).

---

## 6. LM STUDIO / MODELOS — ESTADO

- LM Studio arrancado a las ~10:10 (el PC estuvo apagado por la mañana).
  Patrón: `bash ~/.hermes/scripts/lmstudio-headless.sh` (6s) + `lms load glm-4.6v-flash`.
- ⚠️ ComfyUI quedó PARADO (lo paré yo a las 10:07 para liberar 6.8 GB VRAM
  antes de cargar GLM — estaba activo porque generé el fondo del perfume).
  Arrancar bajo demanda con `systemctl --user start comfyui` si hace falta.
- GLM-4.6v-flash: cargado y verificado (responde con max_tokens>=2000;
  pitfall conocido: razona mucho, content vacío con max_tokens bajos).
- gpt-oss-20b (razonamiento batch): NO convive con GLM (14.9 GB > 12 GB VRAM).
  Si el CLI necesita gpt-oss: `lms unload glm-4.6v-flash` + `lms load gpt-oss-20b`.

---

## 7. PENDIENTES PARA LA SESIÓN CLI (importantes)

1. **Cron vigilar-canales-ig**: 25 posts restantes (prioridad media-baja,
   fotos/memes/entrevistas) NO analizados → quedan para el cron de mañana
   o análisis selectivo. La regla de costes (post-12:00 → router local)
   aplica si se procesan por la tarde.
2. **Cruce vigilar-canales-ig del 19-20 ago**: el informe marcó 28 novedades
   reales (3 de alta prioridad YA analizados hoy) + 23 pendientes de ayer
   (16-18 ago) + ~125 deuda histórica. Los 23 de ayer NO se han procesado.
3. **Bundle /perfume-dia**: primera invocación real pendiente (escribir
   `/perfume-dia` en el chat) — verificar que el gateway lo reconoce.
4. **OWASP futurible tabletop**: oferta previa pendiente de respuesta
   (¿marcar "bajo valor" o borrar?) — sigue abierta.
5. **Confirmaciones pendientes del usuario (previas)**: borrar 3 modelos
   (33 GB) · integrar gpt-oss en router · gráfico lluvia 3 capitales.
6. **Fecha del juicio** (preguntada 2x, sin respuesta) — para el informe
   del sueño.
7. **MRVL 27-ago** (EXP-002) · EXP-HEL fase 2 (~28-ago) · Gemini 03-sep ·
   HAZILAN+ 21/09 · BBK 05/10 · TFM antes de octubre.

---

## 8. CRONS ACTIVOS (referencia rápida)

- vigilar-canales-ig 09:00 · hermes-version-watchdog 22:12 ·
  investigacion-modelos-locales-semanal (lun 10:00) · prospective 09:30 ·
  l2-proposer 8:45 · observer 22:00 · informe-diario 09:00 · EXP-002 22:30 ·
  cloud-backup · scan-empleo OFF (32 activos).
- MCPs: animation-server (⚠️ bug de cache Manim — verificar con ls -lat antes
  de enviar) + lab-db (solo lectura).

---

## 9. LECCIONES DEL DÍA (para no repetir)

1. **La visión local (GLM) es el plan B fiable cuando el proveedor cloud de
   visión falla** — pero hay que arrancar LM Studio si el PC se reinició
   (el usuario lo autoriza explícitamente).
2. **Capturas estrechas de apps (204×1280)**: trocear SIEMPRE con PIL y pedir
   transcripción literal a GLM — la imagen completa mezcla valores.
3. **Los futuribles se anotan SIEMPRE en el mismo turno** (regla del usuario)
   y con backup.
4. **Primer intento de búsqueda de alternativas puede dar falso negativo**
   (Akdeniz): buscar 2-3 veces + fragranova.com/smells-like antes de omitir
   la sección "si te gusta, prueba".
5. **Toda la ficha del perfume en ESPAÑOL** (incluidas citas traducidas) —
   regla añadida a la skill.
6. **Al finalizar, verificar que no quedó nada sin entregar al usuario**
   (pitfall 18-ago: análisis completado pero no entregado = reclamo).

---

## 10. DATOS RÁPIDOS ÚTILES

- Clima Erandio hoy: 21.5°C, 89% humedad, 100% nubes, llovizna densa, 75% lluvia.
- Perfume del día (20-ago): **Akdeniz** (Unique'e Luxury) — marino-mediterráneo.
- Akdeniz: perfume_id 1035, decant 176, 7h longevidad, 2019, Hüseyin Erdoğmuş (probable).
- Nichonauta: 2 vídeos de hoy (reto 2B + speculative decoding) → VALIDAN la
  dirección del lab; n-gram futurible reforzado con números reales.
- Skill Bundles: `hermes bundles create <nombre> --skill s1 --skill s2`
  (YAML en ~/.hermes/skill-bundles/).
