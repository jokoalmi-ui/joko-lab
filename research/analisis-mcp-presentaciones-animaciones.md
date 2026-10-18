---
title: "Análisis — MCPs para presentaciones, infografías y animaciones (16-ago-2026)"
type: research
---

# Análisis — MCPs para presentaciones, infografías y animaciones (16-ago-2026)

**Fuente:** web_search + GitHub API (datos verificados de repos)
**VERACIDAD:** [ALCANCE INTERNO]
costes/tier de servicios cloud sin verificar al detalle ([NO VERIFICADO] donde aplique)

## Pregunta del usuario
¿Existe una herramienta MCP para crear presentaciones, infografías o
animaciones complejas, gratis o muy barata?

## Hallazgos (repos verificados en GitHub)

### 1. Animaciones: MANIM MCP server (el más relevante para el lab)
- **Repo**: Gorav22/Animated_video | ⭐3 | Python | MIT | push 2025-06
- **Qué hace**: ejecuta código Manim y devuelve el vídeo renderizado — el
  agente (Claude u otro cliente MCP) genera animaciones dinámicas.
- **Por qué importa al lab**: el lab YA tiene la skill `manim-video`
  (animaciones estilo 3Blue1Brown). Este MCP es exactamente la capa MCP de
  lo que el lab ya sabe hacer — conectar Manim como servidor MCP haría que
  CUALQUIER cliente MCP (Hermes incluido) genere animaciones sin scripts.
- **Coste**: 0 € (MIT, local — encaja con local-first).
- **⚠️ Madurez**: 3⭐ y un solo push → proyecto joven, calidad a verificar.

### 2. Presentaciones: PowerPoint MCP servers (2 verificados)
- **Ichigo3766/powerpoint-mcp**: ⭐53 | Python | MIT | push 2025-03 —
  crea diapositivas, gráficos desde datos, slides con imagen.
- **trsdn/mcp-server-ppt** (de la búsqueda): cubre trabajo completo: crear
  slides, editar texto, shapes, imágenes, charts, temas, VBA, exportar a
  PDF/vídeo, controlar PowerPoint por COM API.
- **Coste**: 0 € (open source), pero requieren PowerPoint instalado (COM)
  o python-pptx (solo .pptx, sin PowerPoint).
- **⚠️ Encaje lab**: el lab genera slides HTML/CSS propias (maurys, cuaderno,
  1080×1350). Un MCP de PPTX no sustituye eso — serviría para entregar
  archivos .pptx a terceros (p.ej. entregable del máster si lo pidieran).

### 3. Vídeo: free-video-maker (búsqueda)
- **Repo bilalnaseer/free-video-maker**: NO encontrado en GitHub API (404) —
  [NO VERIFICADO] / posiblemente borrado o renombrado. No contar con él.

### 4. Referencia general de MCPs para creadores (Snyk, 2025)
- Lista de 8 MCP servers para flujos de creadores: Luma AI API (vídeo/
  imagen, cloud con coste por token), OpenRouter API (prompt enhancement)...
  La mayoría cloud con coste → chocan con local-first salvo excepciones.

## Veredicto honesto

| Necesidad | Mejor opción MCP hoy | Coste | Veredicto lab |
|---|---|---|---|
| Animaciones complejas | **Manim MCP** (Gorav22) | 0 €, local | ✅ Prometedor — conecta con skill manim-video existente; madurez a verificar |
| Presentaciones .pptx | powerpoint-mcp / mcp-server-ppt | 0 € | 🟡 Solo si necesitas entregar .pptx a terceros; el lab genera HTML propio |
| Infografías | **NO hay MCP destacado** — el lab ya las hace con HTML/CSS (infografia-html) | — | ❌ No necesario |
| Vídeo generativo | Luma AI MCP (cloud, coste) | $$$ | ❌ Choca con local-first |

## Conclusión
SÍ existe — la joya es **Manim MCP** (animaciones, gratis, local), que
extiende como MCP lo que el lab ya domina como skill. Los de PowerPoint
sirven solo si algún día hay que entregar .pptx. Para infografías no hay
nada que mejore el pipeline actual del lab (HTML/CSS + infografia-html).
Se anota como futurible con señal de activación: probar Manim MCP como
**primer MCP del lab** cuando se active el futurible MCP (la madurez del
repo 3⭐ invita a una prueba de concepto antes de integrarlo).
