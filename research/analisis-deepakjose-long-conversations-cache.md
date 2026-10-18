---
title: "Análisis — \"How do you handle long conversations?\" (Deepak Jose / datasciencebrain, 01-sep-2026)"
type: research
---

# Análisis — "How do you handle long conversations?" (Deepak Jose / datasciencebrain, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/Dcv3q7HmOsX/ (Deepak Jose | Data Science & Gen AI, @datasciencebrain, caption íntegro — post de texto, sin necesidad de visión)

## Contenido (del caption)

**La pregunta de entrevista**: "¿Cómo manejas conversaciones largas?" — la respuesta típica "resumo el historial" **termina la entrevista**.

**La respuesta que NO la termina (4 puntos sobre cache-aware prompting)**:
1. **Resumir reescribe el FRENTE del prompt** → cada token cacheado detrás se recomputa y se RE-factura (rompe el prompt cache)
2. **Sliding window expulsa el turno más viejo** → hace lo mismo CADA turno (invalida el prefix cache)
3. **Capping de mensajes grandes**: los encoge EN SU SITIO (in-place) y siguen siendo cacheables
4. **Retrieval va al FINAL del prompt (sufijo)** → los cambios por query no pueden envenenar el prefijo cacheado

**Lo que vende** (suscriptores pagos, Rs.45/mes): "five-layer assembler" + "ablation ladder" (cada escalón añade UN mecanismo) + "cache measurement que cuesta 0 llamadas API" + "validity gate que anula la ejecución si una sonda pudo responderse de otra forma".

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (con matiz)

| Ángulo | Veredicto |
|---|---|
| **Prompt caching es sagrado** | 🟢🟢 **Valida la regla #1 de Hermes** (AGENTS.md: "Per-conversation prompt caching is sacred — anything that mutates past context invalidates the cache y multiplica el coste"). El lab ya opera con ese principio: los 4 puntos del post son exactamente lo que el AGENTS.md prohíbe/permite |
| **"Resumir rompe el cache"** | 🟢 Es el motivo real de que el lab use **context compaction** con cuidado y **skill-compaction** (reducir coste de contexto) en vez de resumir a la ligera — validación externa del diseño |
| **Retrieval como SUFIJO (al final del prompt)** | 🟢🟢 **Idea accionable**: el post dice que el RAG debe ir al FINAL para no envenenar el prefijo cacheado. El lab hace RAG (buscar_rag) — habría que VERIFICAR dónde se inyecta el contexto recuperado en el prompt (¿prefijo o sufijo?) y si el orden actual es cache-friendly. **Acción pendiente de verificación** |
| **Ablation ladder + medición de cache** | 🟢 = patrón OBS→HYP→EXP→DEC del lab + observabilidad del pipeline (TTFB/tokens). El lab ya mide; añadir "medición de cache hits" sería natural |
| **Validity gate** | 🟢 Coincide con el gate de veracidad + verificador de fidelidad del lab (fail-closed) |
| **Paywall (PDF suscriptores)** | ⚪ La parte "cómo construir" está detrás de suscripción — el caption ya da las 4 ideas clave gratis |

**Conclusión**: sin implementar nada nuevo, pero con **1 acción concreta pendiente**: verificar dónde inyecta el lab el contexto RAG en el prompt (¿prefijo = cache-friendly o sufijo?) y, si es prefijo, considerar moverlo a sufijo como recomienda el post (algo que el proveedor DeepSeek cachea). El resto valida el diseño actual del lab (prompt caching sagrado, medición, gates).

**Nota honesta**: el post vende un curso (Rs.45/mes, suscriptores IG exclusivos) — el contenido gratuito del caption es suficiente para el lab; no pagar.
