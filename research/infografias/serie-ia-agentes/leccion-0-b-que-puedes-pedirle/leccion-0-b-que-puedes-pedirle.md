---
title: "Curso IA y agentes — Lección 0-B: Qué puedes pedirle y qué no (usos y tamaño del modelo)"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 0-B (tercera pieza del nivel 0)
estado: guion
created: 2026-09-18
---

# LECCIÓN 0-B — Qué puedes pedirle y qué no: usos y tamaño del modelo

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada pieza termina con un gancho a la siguiente.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL»).
**Escalera didáctica:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.
**Regla de la pieza:** los usos («sí puedes pedirle») se enumeran con la columna «qué le pides / qué NO le pides»; el tamaño del modelo se trata con una medición propia (3 tamaños, misma tarea), no con una opinión.

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `QUÉ PEDIRLE Y QUÉ NO`
- Subtítulo: `Los usos que resuelve hoy y lo que cambia el tamaño del modelo`
- Pie: `6 lecciones · de lo básico a lo avanzado` / `Lección 0 · pieza 3`
- Arte: `arte/s1-caja-herramientas.png` (caja de herramientas de taller, objeto único centrado)

**S2 · Qué es (1/5)** — los usos que sí están resueltos
- Titular: `CUATRO USOS QUE SÍ`
- Arte: `arte/s2-papeles.png` (taco de folios con clip: el material que le das tú)
- Cuatro fichas (todos son «transformar texto que ya le das»):
  - `RESUMIR — un hilo de 40 correos → 5 líneas.`
  - `REDACTAR — un guion de 4 puntos → el correo entero.`
  - `CLASIFICAR — 200 reseñas → positivas o negativas.`
  - `TRADUCIR / EXTRAER — un texto en inglés → los datos que pides.`
- Caja: `Los cuatro comparten una cosa: el material se lo das tú. El modelo no busca nada fuera; reescribe lo que le entregas.`

**S3 · Cómo funciona (2/5)** — la mecánica, con su límite en cada paso
- Titular: `ENTRA TEXTO, SALE TEXTO`
- Pasos:
  - `1. Le das la instrucción y el material.` → `NO le pides: que busque fuera lo que no le has dado.`
  - `2. Predice la siguiente pieza de texto.` → `NO le pides: cuentas exactas ni datos de hoy.`
  - `3. Devuelve el texto con el formato que pediste.` → `NO le pides: que sepa si lo que dice es verdad.`
  - `4. Tú lees, corriges y decides.` → `NO le pides: que asuma la responsabilidad del resultado.`
- Caja: `Los usos de la slide anterior funcionan porque el paso 2 es suficiente: reescribir texto que ya existe se le da bien. Lo que falla no es el idioma: es la exactitud.`

**S4 · Confusión típica (3/5)**
- SVG de barras de tamaño (2,6B · 8B · 35B) con la etiqueta «parámetros = tamaño»
- Columna ✗: `«Cuanto más grande, mejor en todo. Para clasificar necesito el de 70B.»`
- Columna ✓: `El tamaño se nota en la tarea difícil, no en todas. Clasificar lo hicieron igual de bien los tres (5 de 5 cada uno); el grande cobra en recursos y en tiempo.`
- Caja: `Y al contrario tampoco: «como es pequeño, no sirve» es falso. Para resumir, redactar o clasificar, un modelo de 2,6B hace el trabajo.`

**S5 · Ejemplo real (4/5)**
- Titular: `LA MISMA TAREA, TRES TAMAÑOS`
- Arte: `arte/s5-tres-llaves.png` (tres llaves de distinto tamaño, misma forma)
- Tres filas (la misma tanda de tareas a los tres modelos, temperatura 0):
  - `2,6B → clasifica 5/5 · el importe no lo llega a dar · la cuenta 360 ✔`
  - `8B → clasifica 5/5 · el importe en 0,3 s ✔ · la cuenta 342 ✘`
  - `35B → clasifica 5/5 · el importe en 48,8 s ✔ · la cuenta 360 ✔`
- Caja: `Mismo texto de entrada para los tres. Lo que cambia no es «entiende o no entiende»: es dónde acierta. Y el que falló la cuenta no fue el pequeño: fue el de 8B.`

**S6 · Dato medible (5/5)** — PRUEBA REAL, medida el 18-sep-2026
- Titular: `CLASIFICAR: 3 DE 3 · LA CUENTA: FALLA 1`
- Dato grande: `5/5` · `los tres modelos clasificaron las cinco reseñas sin fallar`
- Columna ✗ `LA CUENTA` — `El de 8B contestó 342,00 cuando el total era 360,00: 4 × 89,50 − 10,00 + 12,00. Ninguno de los tres es fiable para aritmética: comprueba el número.`
- Columna ✓ `EL TIEMPO` — `El mismo importe: el de 8B en 0,3 s y el de 35B en 48,8 s. Para el mismo acierto, ~160 veces más lento. Y el de 2,6B se quedó razonando sin llegar a contestar.`
- Caja: regla que se lee → `Para reescribir texto, hasta el pequeño vale. Para exactitud, no lo uses: dale el dato o calcula tú.`
- Pie de método: `Medición propia · 18-sep-2026 · LM Studio, temperatura 0, misma pregunta a 2,6B / 8B / 35B`

**S7 · Cierre**
- `En 1 minuto: (1) Si la tarea es reescribir texto que le das, hasta un modelo pequeño sirve. (2) Para cuentas y datos exactos, no lo uses: dale el dato o calcula tú. (3) El tamaño se paga en recursos; se nota en la tarea difícil.`
- Arte: `arte/s7-cuaderno.png`
- Gancho: `Siguiente · Lección 1 — Instrucciones: el prompt.`

## DATOS
- **Prueba de tamaño (18-sep-2026):** 3 modelos locales, misma API (LM Studio), temperatura 0, misma tanda de tareas.
  - Clasificar 5 reseñas (POSITIVA/NEGATIVA): **2,6B 5/5** (18,2 s) · **8B 5/5** (13,8 s) · **35B 5/5** (119,6 s).
  - Extraer el importe del transporte (12,00 €): **2,6B no responde** (agota el presupuesto razonando, 31,6 s; repetido con 1.600 tokens, igual) · **8B 12,00 ✔** (0,3 s) · **35B 12,00 ✔** (48,8 s).
  - Calcular el total (4 × 89,50 − 10,00 + 12,00 = **360,00**): **2,6B 360 ✔** (6,5 s) · **8B 342,00 ✘** (0,2 s) · **35B 360 ✔** (49,1 s).
  - Ficheros: `medicion-tamano-20260918.json` (crudo), `medicion-tamano-2,6b-repeticion.json`, `medicion-tamano-consolidado.json` (veredictos recalculados). Scripts: `medicion-tamano.py`, `retest-26b.py`, `consolidar-medicion.py`.
  - **Corrección metodológica:** la primera pasada llevaba un esperado erróneo en la cuenta (370 en vez de 360). El valor correcto es 360,00 (358 − 10 + 12); los veredictos publicados salen de recalcular sobre la salida literal de cada modelo.
  - **Hallazgo operativo (no se publica en la pieza):** con el VLM `glm-4.6v-flash` residente, los modelos 8B y 35B **no cargaban** (`llama-server exited before becoming healthy, exitCode=1`); tras `lms unload` cargaron los dos.
- **Sin verificar (no se publica):** ninguna cifra de mercado ni de modelos comerciales; ninguna comparación con modelos de pago.

## FORMATO
Estilo fijado de la serie (L0 / L0-A): paneles claros estilo MAURYS, 1080×1350, 7 slides, PDF como documento en LinkedIn. Arte SDXL para escenas; diagramas en SVG dentro del HTML.

## HISTORIAL
- 2026-09-18 · v1: guion base + medición de tamaño en tres modelos locales (misma API, temperatura 0).
- 2026-09-18 · v2: guion con los números reales; arte SDXL (5 escenas) verificado por visión; PDF 7 páginas (`carrusel-leccion-0-b.pdf`) con QA 7/7 y transcripción literal slide a slide (corregido un corte en S4); `post-linkedin.md` escrito. Estado: VERIFICADO, pendiente de publicar.
