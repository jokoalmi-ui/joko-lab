---
title: "Análisis — MCP de Highfield en Hermes Agent (Dev Knives, 22-ago-2026)"
type: research
---

# Análisis — MCP de Highfield en Hermes Agent (Dev Knives, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/-hhvAlFPWHQ (Dev Knives, 30-05-2026, 10 min — detectado por el usuario)
**Método:** subtítulos ES descargados (16 KB) + metadatos. ⚠️ VÍDEO PATROCINADO (declarado al inicio).

## Contenido
- **Highfield** = plataforma cloud de generación de vídeo/imagen (patrocinador del vídeo)
- El vídeo muestra cómo integrar el **MCP de Highfield** en **Hermes Agent** (config en un canal de Slack, pero vale Telegram/terminal)
- Proceso: copiar instrucciones → Hermes genera URL de autorización → autorizar → reiniciar Hermes → pedir imagen/vídeo
- El propio autor admite: **"ha costado un poquito... a veces Hermes se vuelve loco dependiendo del LM que utilices"** — la integración por MCP fue farragosa (URLs inválidas, "esto se lo está inventando")
- Para generar de verdad necesita **plan de pago** (el autor usó el plan gratuito, modelo básico, resultado pobre: "una luna explotando" de baja calidad)
- **Cierre honesto del autor**: "el nivel artístico tampoco es que sea muy fuerte" + enlace de descuento

## 🔴 Para el LAB — VALOR: BAJO (patrocinado + cloud + pago + el lab YA tiene esto local)

| Aspecto | Análisis |
|---|---|
| ¿Es contenido útil? | ❌ Vídeo patrocinado — promociona Highfield con enlace de descuento |
| ¿Generación de imagen? | ✅ El lab YA lo hace LOCAL con ComfyUI+SDXL (gratis, privado, sin plan) |
| ¿Generación de vídeo? | ✅ El lab YA lo hace local (Manim MCP + gen_video_corto.sh) |
| ¿MCP en Hermes? | ✅ El lab YA tiene MCPs (animation-server, lab-db, lancedb) — patrón conocido |
| ¿Cloud de pago? | ❌ Contradice el principio local-first del lab |
| Calidad | El propio autor admite que el resultado artístico era pobre |

**Conclusión**: vídeo patrocinado que promociona una plataforma cloud de pago para algo que **el lab ya hace gratis y local** (ComfyUI + Manim + gen_video_corto.sh). El único aprendizaje: el patrón de integrar un MCP en Hermes (copiar config → autorizar → usar) es el mismo que el lab ya usa con sus 3 MCPs.

**Sin futuribles** — el lab no necesita Highfield ni su MCP (local-first, 0 €, mejor calidad con SDXL propio). Descartar.
