---
title: "TFM — Estado del proyecto"
type: tfm
---

# TFM — Estado del proyecto

**Actualizado:** 21-ago-2026 (sesión CLI, cierre tras verificación en disco)

## Decisión tomada
- Módulo 11 (TFM): se presenta **Joko Lab** como trabajo final.
- Opción elegida: **Opción 3 — Técnica: Desarrollo de una Solución IA de Impacto**
  (el lab es un sistema real, no una propuesta teórica).
- Enunciado completo del TFM: ver `~/master-founderz-seguimiento/` (pegado por
  el usuario en sesión CLI el 06-ago-2026).

## ESTADO REAL (verificado en disco 21-ago-2026)

### ✅ COMPLETADO Y ENTREGADO
- **VÍDEO DE PRESENTACIÓN (3 min) — ENTREGADO**: la evaluación de Founderz se
  hizo sobre el vídeo (feedback recibido y respondido 18-ago). Versiones en
  `~/joko-lab/founderz/`:
  - `video_joko_lab_founderz_20260816.mp4` (22 MB, 16-ago)
  - `presentacion-viva-fusion-cuaderno-v5-apaisado-final.mp4` (15 MB, 17-ago
    14:28) — versión final de la iteración cuaderno
  - + 9 versiones previas (v1/v2/v3-manim/v3-timelapse/v4-apaisado...) en
    `~/joko-lab/founderz/` y backups `.BACKUP.20260818/` `.BACKUP.20260820/`
- **GUÍA DE PRESENTACIÓN**: `GUIA-FOUNDERZ-TFM.txt` v1.1 (17-ago, 8 partes,
  23 KB): qué es, 4 cerebros, conocimiento/LPA, RAG, enrutador, productos,
  resultados, evolución.
- **CONTESTACIÓN AL FEEDBACK**: `CONTESTACION-FEEDBACK-FOUNDERZ.txt` (18-ago):
  respuesta punto por punto con evidencia; reconoce carencias válidas y
  aclara limitaciones del formato vídeo (el feedback automático evaluó solo
  el vídeo sin acceso a documentación).
- **ANEXO METODOLÓGICO**: `ANEXO-METODOLOGICO-JOKO-LAB.txt` (18-ago):
  métricas, 233 tests, evaluador RAG, verificador de alucinaciones.
- **NARRACIÓN**: `narracion-tfm-v2.txt` + `narracion-alvaro.mp3` + guion
  `GUION-VIDEO-3MIN.txt` (10-ago).
- **INFRAESTRUCTURA DE SLIDES**: plantilla cuaderno base + paso de página 3D
  validados (08-ago, 3 iteraciones). Iteraciones de slides: `gui-*` (8,
  10-ago), `narr-*` (11, 10-ago), `labnotes-*` (3, 11-ago), portada y mapa
  general verificados con GLM.

### ⏳ PENDIENTE (por confirmar con el enunciado)
- **PDF (15-45 págs)**: el ESTADO-TFM.md antiguo mencionaba F3 "redactar el
  PDF". No hay PDF en disco todavía. **VERIFICAR si el enunciado de la
  Opción 3 lo exige** (la entrega evaluada fue el vídeo + documentación;
  si el PDF es obligatorio, es la única pieza grande que queda).
- Confirmar cierre de la entrega en la plataforma Founderz (lo hace el usuario).

## Historia (fases previas, resumen)
- 06-ago: decisión de presentar Joko Lab (Opción 3). Formato vídeo "powerpoint"
  con ilustraciones. Pipeline HTML→PNG→verificación GLM local.
- 06-ago: portada "notas premium" beige/espiral refinada con especificación
  fina de Gemini (paleta #FDF8E9/#2D5D62/#D4A017, espiral 24 anillas).
- 08-ago: plantilla "hoja cuaderno" base (papel crema cuadriculado, espiral
  wire-o, geometría medida) + paso de página 3D (3 iteraciones: degradado GPU,
  rotación determinista, movimiento más largo).
- 10-ago: guion 3 min + narración edge-tts (Alvaro) + iteraciones gui/narr.
- 11-ago: iteración labnotes.
- 16-17-ago: vídeos de presentación (7 versiones viva-joko-lab + 5
  fusion-cuaderno apaisado) — ENTREGADO.
- 18-ago: feedback recibido → anexo metodológico + contestación punto por punto.

## Archivos actuales
```
/home/jokoalmi/joko-lab/tfm/
├── ESTADO-TFM.md          (este archivo — actualizado 21-ago)
├── GUIA-FOUNDERZ-TFM.txt  (v1.1, 17-ago)
├── ANEXO-METODOLOGICO-JOKO-LAB.txt (18-ago)
├── CONTESTACION-FEEDBACK-FOUNDERZ.txt (18-ago)
├── GUION-VIDEO-3MIN.txt / narracion-tfm*.txt / narracion-alvaro.mp3
└── slides/  (plantilla cuaderno, paso-pagina, gui-*, narr-*, labnotes-*)

/home/jokoalmi/joko-lab/founderz/  (vídeos MP4, entregado el 16-17-ago)
```
