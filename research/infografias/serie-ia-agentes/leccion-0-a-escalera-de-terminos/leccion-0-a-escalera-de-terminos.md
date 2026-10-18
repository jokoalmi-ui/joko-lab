---
title: "Curso IA y agentes — Lección 0-A: IA, ML, Deep Learning y LLM: la escalera de términos"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 0-A (segunda pieza del nivel 0)
estado: verificado — render + QA 7/7 + transcripción visual, pendiente de publicar
created: 2026-09-16
---

# LECCIÓN 0-A — IA, ML, Deep Learning y LLM: la escalera de términos

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada pieza termina con un gancho a la siguiente.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL»).
**Escalera didáctica:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.
**Regla de la pieza:** cada peldaño lleva la columna «qué le pides / qué NO le pides». Sin ella la pieza es glosario (corrección del 2026-09-16).

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `LA ESCALERA DE TÉRMINOS`
- Subtítulo: `IA, machine learning, deep learning y LLM: qué es cada cosa`
- Pie: `6 lecciones · de lo básico a lo avanzado` / `Lección 0 · pieza 2`
- Arte: `arte/s1-escalera.png` (SDXL, escalera de 4 peldaños)

**S2 · Qué es (1/5)**
- Titular: `CUATRO PALABRAS, CUATRO ALTURAS`
- Arte: `arte/s2-munecas.png` (muñecas rusas = cajas dentro de cajas)
- Cuatro fichas (en orden de escalera): `IA — cualquier máquina que hace algo que llamamos inteligente.` · `ML — aprende de datos, no de reglas escritas.` · `DL — redes neuronales con muchas capas.` · `LLM — deep learning especializado en lenguaje.`

**S3 · Cómo funciona (2/5)** — los cuatro peldaños, cada uno con su ejemplo y su límite
- Titular: `LOS CUATRO PELDAÑOS`
- Pasos:
  - `1. IA — un rival de ajedrez con reglas fijas.` → `NO le pides: que aprenda de tus datos.`
  - `2. ML — predecir qué cliente se dará de baja.` → `NO le pides: que te explique el porqué.`
  - `3. DL — reconocer una cara en una foto.` → `NO le pides: que te diga en qué se fija.`
  - `4. LLM — escribirte un correo entero.` → `NO le pides: tus datos ni cuentas exactas.`
- Caja: `Cada peldaño hereda el anterior. Por eso a cada uno le pides una cosa: cumplir reglas, acertar una predicción, escribir texto.`

**S4 · Confusión típica (3/5)**
- SVG de barras decrecientes (IA 430px → LLM 152px): `IA: cualquier máquina «inteligente»` · `ML: aprende de datos` · `DL: redes profundas` · `LLM: escribe texto`
- Columna ✗: `«La IA, el machine learning y ChatGPT son lo mismo.»`
- Columna ✓: `Todo LLM es IA. Casi ninguna IA es un LLM.`
- Caja: `Un filtro de spam es ML y no es deep learning. Y un LLM no "sabe" cosas: predice texto.`

**S5 · Ejemplo real (4/5)**
- Titular: `LA MISMA TIENDA, CUATRO SOLUCIONES`
- Arte: `arte/s5-cesta.png`
- Cuatro filas: `Reglas → si compra pan, ofrecer mantequilla.` · `ML → predecir qué producto se va a agotar.` · `DL → leer la matrícula de un coche en el parking.` · `LLM → contestar por escrito una reclamación.`
- Caja: `Los cuatro son IA. Solo el último escribe como una persona.`

**S6 · Dato medible (5/5)** — PRUEBA REAL, medida el 16-sep-2026
- Titular: `SIN EL DATO, SE LO INVENTA`
- Dato: `0/3 → 3/3` (`aciertos sin el dato en el texto · con el dato en el texto`)
- Columna ✗ `SIN DARLE EL DATO`: `No dijo «no lo sé». Contestó 1, 45 y 1234.56.` — preguntas: nº de modelos de IA del equipo, nº de piezas de la serie, total de un albarán inexistente.
- Columna ✓ `DÁNDOLE EL DATO`: `Contestó 15, 8 y 30.50. Las tres correctas.` — el dato escrito en la propia pregunta.
- Caja: `Un LLM no consulta tu ordenador: predice texto. Si el dato no está en lo que le escribes, se lo inventa con toda la seguridad del mundo.`
- Pie de método: `Medición propia · 16-sep-2026 · qwen2.5:7b en local (CPU, temperatura 0), 3 preguntas con y sin el dato en el contexto`

**S7 · Cierre**
- `En 1 minuto: (1) IA es el paraguas; el LLM es la punta. (2) ML aprende de datos; DL son redes profundas. (3) Pide texto al LLM; no le pidas exactitud.`
- Arte: `arte/s7-mochila.png`
- Gancho: `Siguiente · Lección 0-B — Qué puedes pedirle y qué no: usos y tamaño del modelo.`

## DATOS
- **Prueba con/sin dato (16-sep-2026, medida y verificada):** `qwen2.5:7b` en Ollama, `num_gpu=0` (CPU), temperatura 0.
  - Sin el dato: **0/3 aciertos** y **0/3 admiten no saberlo** → respuestas literales: `1`, `45`, `1234.56`.
  - Con el dato en el contexto: **3/3 aciertos** → `15`, `8`, `30.50`.
  - Registro crudo: `medicion-contexto-20260916.json` (incluye la nota de recálculo: el script inicial dio 2/3 por un bug de comparación de texto; recalculado con normalización numérica = 3/3).
- **Inventario del equipo (16-sep-2026, medido):** 12 modelos en LM Studio + 3 en Ollama = 15; 20 ficheros de pesos, 112,1 GB; desglose: 9 texto / 4 visión / 2 embeddings. Pasa a ser el **origen de la primera pregunta** de la prueba, no el dato de portada.
- **Sin verificar (no se publica):** ninguna cifra de mercado ni tamaño de modelos comerciales.

## FORMATO
Estilo fijado de la serie (L0): paneles claros estilo MAURYS, 1080×1350, 7 slides, PDF como documento en LinkedIn. Arte SDXL para escenas; diagramas en SVG dentro del HTML (no SDXL para diagramas).

## HISTORIAL
- 2026-09-16 · v1: guion + arte + render inicial (7 slides), con el inventario del equipo como slide de dato.
- 2026-09-16 · v2 (corrección por revisión del usuario: «¿la gente aprende algo?»): S3 gana la columna «qué NO le pides» a cada peldaño; S6 sustituye el inventario por una **prueba real con/sin dato**; S7 cambia la tercera idea por una aplicable. Rebuild + QA 7/7 + transcripción visual. PDF nuevo: 784.007 B.
