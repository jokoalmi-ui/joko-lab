---
title: "Análisis: Batería de Visión — LFM 2.5 VL 3B vs GLM-4.6v-flash (21-ago-2026)"
type: research
---

# Análisis: Batería de Visión — LFM 2.5 VL 3B vs GLM-4.6v-flash (21-ago-2026)

**VERACIDAD:** [ALCANCE INTERNO]

## Contexto

Batería de visión comparativa entre **LFM 2.5 VL 3B** (Liquid AI, GGUF Q4_K_M 1.56 GB + mmproj Q8_0 0.54 GB, 2.10 GiB cargado) y **GLM-4.6v-flash** (7.41 GiB), ambos locales en LM Studio (`localhost:1234`). Ejecutada por el cron one-shot `002b1c600328` (21-ago-2026, ~12:07-12:19) con el orquestador `joko-lab/tools/bateria_vision_orquestador.sh` + `bateria_vision_compare.py`.

4 tareas REALES del lab:
1. **sueño_ocr** — captura estrecha de app de sueño Xiaomi Smart Band 8 Pro (214×1280): puntos, duración, horas, % etapas, FC, SpO2, respiración.
2. **frasco_adonis** — identificar frasco de perfume (etiqueta "ARGOS") en `adonis_frasco_real.png`.
3. **fondo_sdxl** — describir escena del fondo generado con ComfyUI/SDXL (`adonis_fondo.png`).
4. **infografia** — verificar si se ve la tarjeta "Si te gusta, prueba" y el pie en la infografía v4.

JSONs: `/tmp/bateria_vision_LFM2.5-VL-3B-GGUF.json` y `/tmp/bateria_vision_glm-4.6v-flash.json`. Log: `/tmp/bateria_vision_log.txt`.

**⚠️ Incidencia del orquestador**: el paso `lms load LFM2.5-VL-3B-GGUF` se colgó >9 min (sin llama-server, VRAM libre 1206 MiB). Causa: el orquestador usaba el NOMBRE DE CARPETA (`LFM2.5-VL-3B-GGUF`) como id; el id real de la API es `lfm2.5-vl-3b`. Con el id real, carga en 6.69 s. Se ejecutaron los pasos manualmente (unload GLM → load LFM → batería → unload → load GLM → batería). **PITFALL registrado**: usar SIEMPRE el id de `lms ls`/`lms ps`, no el nombre de carpeta.

## Resultados crudos (salida real)

| Tarea | LFM 2.5 VL 3B | GLM-4.6v-flash |
|---|---|---|
| sueño_ocr | 0.7s, 20 tok → `76 / 6:28 / 00:43 / 40% / 0% / 98% / 72% / 8` | 27.8s, 800 tok → **content VACÍO** (max_tokens=800 agotado en reasoning; re-consultado con 2000: `76, 6-28 min, 0:38, 9.3%/59.7%/30.9%, 58 bpm, 97%, 12`) |
| frasco_adonis | 0.5s, 4 tok → `Argos.` | 5.3s, 135 tok → `Argos (casa y nombre: Argos)` |
| fondo_sdxl | 1.0s, 38 tok → escena serena con taza de café y rosa, luz suave | 12.8s, 349 tok → vaso de café, plato, madera, rosa rosada, luz cálida, más flores |
| infografia | 0.4s, 2 tok → `SI` | 3.3s, 79 tok → `SI` |

VRAM (nvidia-smi real):
- LFM: **3581 MiB** al inicio de su batería (2.10 GiB modelo + buffers); final 3649 MiB.
- GLM: **9254 MiB** al inicio de su batería; final 9309 MiB.

## Verdad de las imágenes (verificación con transcripción troceada + consultas dirigidas)

**sueño_ocr** (transcripción literal por 4 trozos con GLM, patrón validado 20-ago):
- Puntos: 76 · Duración: 6 h 28 min · Tiempo dormido: 00:38 → despertado: 07:06
- Etapas: **REM 11% (42 min) · Ligero 58% (3:44 min) · Profundo 31% (2:02 min)**
- FC: 60 LPM · SpO2: 96% · Puntuación de respiración: 99 puntos

**frasco_adonis**: la etiqueta del frasco real dice literalmente **"ARGOS"** (verificado: "ARGOS / ARGOS").

**infografia v4**: la estructura SÍ incluye la sección **"Si te gusta, prueba"** (punto 8: Swiss Arabian Rose 0%, Van Cleef & Arpels Rouge, Issey Miyake L'Eau d'Issey Rosee) y **pie de página** (punto 9) → la respuesta correcta es SI.

## Evaluación por tarea

### 1. sueño_ocr — **GLM GANA (con presupuesto suficiente); LFM FALLA**
- **LFM** respondió en 0.7s pero con valores **inventados/mezclados**: `00:43` (real 00:38), `40% / 0% / 98% / 72% / 8` — esos números NO existen en la captura (real: REM 11 / Ligero 58 / Profundo 31 / FC 60 / SpO2 96 / resp 99). Es un fallo claro de OCR fino en captura estrecha.
- **GLM** en la batería devolvió content vacío (el presupuesto de 800 tokens se agota en razonamiento — pitfall ya documentado). Re-consultado con max_tokens=2000 dio valores **coherentes y cercanos**: 00:38 ✓, 9.3/59.7/30.9 (≈11/58/31 reales), FC 58 (≈60), SpO2 97 (≈96). Solo falló respiración (12 vs 99).
- **Matiz de robustez**: con el presupuesto del script (800) GLM falla y LFM no (LFM no razona, responde directo). Con presupuesto adecuado (2000), GLM es claramente más preciso.

### 2. frasco_adonis — **EMPATE (ambos correctos)**
- Ambos dicen "Argos" y es correcto. LFM en 0.5s/4 tok (directo), GLM en 5.3s/135 tok (con explicación). LFM suficiente para identificación simple.

### 3. fondo_sdxl — **EMPATE (ambos correctos; GLM más detallado)**
- Ambos describen correctamente (taza de café + rosa + luz cálida). GLM añade plato/madera/más flores; LFM es correcto y conciso. Para descripción rápida, LFM sobra.

### 4. infografia — **EMPATE (ambos correctos)**
- Ambos responden "SI" y es correcto (la tarjeta y el pie SÍ se ven en v4). LFM en 0.4s/2 tok.

## Tabla comparativa final

| Métrica | LFM 2.5 VL 3B | GLM-4.6v-flash | Ganador |
|---|---|---|---|
| sueño_ocr (precisión OCR fino) | ❌ valores inventados (0.7s) | ✅ valores coherentes con 2000 tok (27.8s) | **GLM** |
| frasco_adonis | ✅ Argos (0.5s) | ✅ Argos (5.3s) | Empate |
| fondo_sdxl | ✅ correcto, conciso (1.0s) | ✅ correcto, detallado (12.8s) | Empate |
| infografia | ✅ SI (0.4s) | ✅ SI (3.3s) | Empate |
| Latencia media | **~0.65s** | ~12.3s (≈19x más lento) | **LFM** |
| VRAM cargado | **2.10 GiB (3581 MiB)** | 7.41 GiB (9254 MiB) | **LFM** (3.5x menos) |
| Robustez (content vacío) | ✅ 4/4 respondió | ⚠️ 1/4 content vacío con 800 tok | **LFM** |
| Detalle de respuesta | Escueto (2-38 tok) | Verboso (79-800 tok) | Según uso |

## Veredicto

**LFM 2.5 VL 3B NO sustituye a GLM en OCR de precisión (sueño_ocr: inventa valores), pero SÍ es válido como visión LIGERA para tareas rápidas de verificación, identificación y descripción.** En 3 de 4 tareas responde correctamente y en 0.4-1.0s, con 3.5x menos VRAM. GLM sigue siendo el VLM principal para extracción de datos de capturas (salud, formularios) con presupuesto ≥2000 tokens.

**Recomendación final (honesta):**
- **LFM VL 3B SE QUEDA como visión ligera complementaria** (Futurible F8 VALIDADO parcialmente): convive con gpt-oss en 12 GB y sirve para verificación SI/NO, identificación de frascos/marcas y descripciones cortas cuando la velocidad importa. Coste 0, 2.10 GiB.
- **GLM-4.6v-flash SE MANTIENE como VLM principal** para OCR de datos críticos (sueño, formularios, capturas estrechas) — siempre con max_tokens ≥2000 (pitfall del content vacío).
- **Regla de ruteo propuesta**: tareas de visión "verificar/identificar/describir" → LFM VL 3B (rápido, ligero); tareas de "extraer datos exactos de captura" → GLM (preciso, presupuesto alto).
- ⚠️ Fix del orquestador: usar `lms load lfm2.5-vl-3b` (id real), no `LFM2.5-VL-3B-GGUF` (nombre de carpeta) — se cuelga >9 min. Corregido en este análisis, pendiente actualizar el script.

**Fuente:** salida real de la batería (JSONs en /tmp), verificación con transcripción troceada GLM y consultas dirigidas; log `/tmp/bateria_vision_log.txt`.
