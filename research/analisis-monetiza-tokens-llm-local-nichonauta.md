---
title: "Análisis — Monetiza los TOKENS de tu LLM Local (Nichonauta, directo 15-ago-2026)"
type: research
---

# Análisis — Monetiza los TOKENS de tu LLM Local (Nichonauta, directo 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/live/xC0ZiB9CrO0 (1h46m, Nichonauta — canal de referencia #1)
**Transcripción:** completa (es, 90 KB)

## Qué propone (el modelo de negocio completo)
"Como minar criptomonedas, pero sin minar: aprovechar tu hardware (o servicio en línea) para generar contenido que atraiga tráfico de Google y monetizarlo con anuncios/afiliados" — igual que el 99% de internet.

**Pipeline (3 directos de la serie, este es el 3º):**
1. **Keywords**: Google autocomplete gratis (palabras clave con tráfico y poca competencia), Keyword Sheeter, Keyword Planner, Ubersuggest, Ahrefs, SEMrush. Criterio: miles de búsquedas/mes + poca competencia.
2. **Generación de contenido con LLM LOCAL**: Gemma 3 2B a 4 bits en llama.cpp, 12 respuestas en paralelo (30 tok/s × 12 = 360 tok/s), 147 artículos generados con título/contenido/descripción/categoría.
3. **Imágenes**: prompts para Z-Image/Flux/SD (429 prompts), generación local (ComfyUI) o servicio en línea.
4. **Montaje web** (el directo 4º, pendiente): hosting compartido (no VPS), dominio, Search Console, sitemap → Google indexa → tráfico → anuncios.

**Adaptación nueva de este directo**: agrupar keywords por SIGNIFICADO (no solo por intención) — "características de perro" vs "características de PC" comparten la palabra pero no el tema. Da ~20% más calidad pero 80% más trabajo → ajustar el umbral.

## Datos técnicos valiosos (para el lab)
- **Un modelo 2B a 4 bits basta para SEO básico** — corre hasta en CPU. El lab tiene MUCHO más (Gemma-4-12B, Qwen3.6-35B-A3B, R1-14B).
- **llama.cpp paralelismo**: 12 slots en paralelo multiplican el throughput (360 tok/s); cada slot con su propio contexto (32K-65K); un solo modelo cargado sirve para todo (no hace falta "un modelo por tarea").
- **Gemma es el preferido del autor para redacción** (no por open weights, por calidad de escritura).
- **Los modelos de lenguaje hacen "en resumen," al final** → se elimina con código, no con prompt (fiable).
- Prompts adaptados por modelo (cada modelo entiende diferente: tablas vs listas vs HTML).

## Veredicto para Joseba (honesto, directo al grano)
**VALIDA EL CONCEPTO + es EXACTAMENTE la dirección de "ingresos desde casa" que Joseba quiere pensar. PERO con matices críticos:**

### ✅ Lo que encaja
- **Infraestructura 100% lista**: el lab tiene hardware (A2000), LLMs locales (Gemma/Qwen/R1), llama.cpp vía LM Studio, scripts. **Coste marginal ≈ 0** (electricidad).
- Es un trabajo "sencillo" repetible: encontrar keywords → generar → publicar.
- Nichonauta es prueba viviente de que funciona (vive de esto desde los 13 años; ahora con IA).

### ⚠️ Los matices que NO dice el título
1. **NO es ingreso rápido**: el SEO tarda **meses** en posicionar (él lo dice: "en un año me estuvo dando tráfico"). No es para el mes que viene.
2. **Es un NEGOCIO, no un trabajo sencillo**: requiere constancia (él: "cuesta trabajo, es un trabajo"), aprendizaje del pipeline (los 2 directos previos + este + el de hosting = 6+ horas de formación), y gestión (dominio ~10€/año, hosting ~30-60€/año).
3. **Riesgo Google**: contenido 100% IA puede ser penalizado; la estrategia es buscar nichos donde la IA no quite tráfico.
4. **El autor MONETIZA doble**: con el contenido Y vendiendo el servicio/scripts ($50 sitio en 1 semana, cupos limitados). Eso también es una vía.
5. **No es mágico**: "puedes ganar muchísimo o nada, como cualquier emprendimiento".

### 🎯 Lectura para Joseba (56 años, sin empleo, perfil técnico)
- **Como plan B de ingresos a medio plazo (3-6 meses)**: viable y barato de arrancar. El lab ya tiene el 80% técnico.
- **Como ingreso inmediato**: NO — no reemplaza HAZILAN+ (21/09) ni el soporte técnico remoto.
- **Siguiente paso concreto**: ver el directo 4º (subir a hosting/dominio — pendiente de publicar) y los 2 previos de la serie si Joseba quiere montarlo de verdad.
- El pipeline completo es replicable con las skills del lab (generar contenido con LLM local ya se sabe hacer).

## Registro
- Guardado: research/analisis-monetiza-tokens-llm-local-nichonauta.md
- Futurible: cuando Joseba decida si monta la web → ver directos previos + directo 4º (hosting/dominio), decidir nicho, y montar el pipeline con el estilo del lab.
