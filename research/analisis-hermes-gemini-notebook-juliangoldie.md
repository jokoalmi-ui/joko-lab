---
title: "Análisis — \"Hermes + Gemini Notebook is ABSURD\" (Julian Goldie SEO, 25-ago-2026)"
type: research
---

# Análisis — "Hermes + Gemini Notebook is ABSURD" (Julian Goldie SEO, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/rQlYxtSxO7Y (9 min, 4.176 views)
**Método:** metadatos + subtítulos automáticos EN (ES dio 429, patrón conocido → fallback EN validado) → deduplicación → lectura completa (9.3K chars)

## Qué propone el vídeo

Julian Goldie SEO vende su "Agent OS" (dentro de su comunidad de pago "AI Profit Boardroom", 3.200 miembros): una arquitectura que conecta:

1. **Gemini Notebook** (ex-NotebookLM, renombrado por Google el **16-jul-2026**) = cerebro de investigación. Fuentes: PDFs, webs, YouTube, Drive, audio. Responde grounded solo en esas fuentes.
2. **Hermes** (el mismo agente que usa el lab) = el agente que actúa sobre la investigación.
3. **MCP de Gemini Notebook** (herramienta comunitaria gratuita) = puente Hermes ↔ notebooks: listar, consultar, extraer research sin copiar/pegar.
4. **Obsidian** = vault de memoria (el lab YA tiene uno unificado en /mnt/ssd_ia_datos/obsidian-vault).
5. **Hyperframes** = skill de vídeo open source (el lab tiene video-slides-tts equivalente).
6. **Novedad julio-2026**: Gemini Notebook añadió un **cloud computer** que ejecuta código dentro de los notebooks (análisis de datos real, no solo resumen) — Hermes puede acceder a esos insights vía MCP.

**El loop**: investigación → contenido → memoria → el siguiente workflow es más rápido.

**La entrega**: zip de pago con "todo pre-configurado" + 4 coaching calls semanales + 30-day roadmap + prompt library → **aiprofitboardroom.com** (bait comercial).

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (un futurible real + validación)

### ✅ Futurible real: MCP de Gemini Notebook ↔ Hermes
El lab ya tiene la skill `notebooklm` (cuadernos de Gemini/NotebookLM del usuario) y Hermes como agente. Conectar el **MCP comunitario de Gemini Notebook** permitiría consultar los cuadernos desde Telegram sin copiar/pegar. **Señal de activación**: cuando el usuario use NotebookLM con frecuencia como fuente de investigación. Anotado como futurible MEDIO (mismo patrón que MCP n8n → Hermes).

### ✅ Validación del concepto "Agent OS"
El lab **YA ES un Agent OS** con todos los componentes por separado:
| Componente del vídeo | En el lab |
|---|---|
| Gemini Notebook (research) | ✅ RAG LanceDB 21.975 fragmentos + skill notebooklm |
| Hermes (agente) | ✅ Hermes en producción |
| Obsidian (memoria) | ✅ Vault unificado + Syncthing |
| MCP bridge | ✅ 3 MCPs ya conectados (animation, lab-db, lancedb) |
| Skills (vídeo) | ✅ video-slides-tts, gen_ficha_animada |

El vídeo valida externamente la arquitectura del lab (como IBM Digital Librarian, pabloinpublic, mattpocock/addyosmani).

### ⚠️ NO pagar ni instalar el zip
- Es un **sales pitch**: el contenido real (configuración, prompts) está tras el muro de pago de la comunidad.
- El stack que describe es **100% gratis y open source** (lo admite él mismo: "the software stack costs nothing") — el lab ya tiene todo eso.
- Las "4 coaching calls semanales" y "3.200 miembros" son el modelo de negocio, no el valor técnico.

## Conclusión
- **Futurible anotado**: MCP de Gemini Notebook ↔ Hermes (MEDIO, señal = uso frecuente de NotebookLM).
- **Validación**: el lab ya implementa el "Agent OS" completo.
- **Sin acción de compra**: todo el stack es gratis y ya está construido en el lab.
