---
title: "Análisis — Spec-Driven Development vs Vibe Coding (vídeo YT, 11-ago)"
type: research
---

# Análisis — Spec-Driven Development vs Vibe Coding (vídeo YT, 11-ago)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 11-ago-2026
**Fuente:** https://youtu.be/EOiv7RywtQM — vídeo de desarrollo (transcripción completa)
**Tema:** Comparación empírica: el MISMO proyecto (buscar texto en 200 notas
markdown, contar coincidencias, filtrar por etiqueta) hecho de 2 formas:
Vibe Coding (Sonet, modelo caro, sin spec) vs Spec-Driven (Haiku, modelo
barato, con especificación).

---

## El experimento (resultados medidos)

| Métrica | Vibe Coding (Sonet) | Spec-Driven (Haiku) |
|---|---|---|
| Modelo | Claude Sonet (grande, caro) | Claude Haiku (pequeño, barato) |
| Archivos abiertos por ejecución | **400** (200 notas × 2) | **0** (usa metadatos/índice) |
| 1ª ejecución (fría) | 1.38s | 1.47s |
| 2ª ejecución (cálida) | 0.23s | **0.14s (39% más rápido)** |
| Funcionalidades extra sin pedir | 4 (no validadas, deuda técnica) | 0 |
| Requisitos verificados | — | 16/16 checklist, 0 preguntas de vuelta |
| Código | (más líneas) | 303 líneas, 8 módulos, test anti-regex |
| Índice/caché | ❌ NO (nadie lo pidió) | ✅ SÍ (en la spec) |

**Resultado: el modelo GRANDE y caro (Sonet) improvisando hizo la PEOR app
(400 archivos); el modelo PEQUEÑO y barato (Haiku) con especificación hizo la
MEJOR (0 archivos, más rápido, trazable).**

---

## Los 4 mensajes clave del vídeo

1. **El vibe coding no falla por donde crees:** no se queda corto — CONSTRUYE
   DE MÁS (4 funcionalidades no pedidas = deuda técnica) y a la vez OLVIDA lo
   que importa (el índice) porque no estaba en el prompt. Sin spec, tus
   requisitos = los que recuerdas en ese momento, ni uno más.
2. **El modelo importa menos de lo que crees; el contrato importa más:**
   Sonet+vibe perdió contra Haiku+spec. No porque Haiku sea mejor, sino porque
   a uno le dieron un contrato y al otro una corazonada. Si tu código sale
   regular, cambiar a un modelo más caro probablemente NO lo arregle; escribir
   la spec sí.
3. **El vibe coding SÍ tiene su sitio:** prototipos desechables, validar una
   idea en una tarde, scripts de un solo uso. El problema NO es usarlo — es
   cuando el prototipo se convierte en producto sin que nadie tome la decisión
   de convertirlo.
4. **El cambio de mentalidad clave:** el prompt es la PETICIÓN; la especificación
   es el CONTRATO — no son lo mismo. Sin contrato escrito: no se puede auditar,
   ni repetir, ni pasar a otra persona, ni ejecutar contra una herramienta de
   selección de modelo (SpecJuts).

**Herramienta mencionada:** SpecJuts (open source, en PyPI) — lee tu spec y
tareas y te dice qué modelo del mercado está bien dimensionado (marca Sonet/
Opus/Gemini Pro como "overkill" citando fragmentos de tu spec). Para este
proyecto recomendó: llama 3.3 local gratis como "oro", Haiku/Lluna/Gemini
Flash como opciones de pago baratas.

---

## 🎯 Aplicación al LAB — VALIDACIÓN DIRECTA DE LA METODOLOGÍA LPA

### El lab YA hace Spec-Driven Development (es LPA)

| Concepto del vídeo | Lab |
|---|---|
| **Spec como contrato** | ✅ **SVP (State Verification Pattern)** — verificación por estados |
| **Criterios de aceptación medibles** | ✅ **KVC/KCR** (Knowledge Verification Criteria/Review) |
| **Requisitos trazables a tareas** | ✅ Mission Contract (research/mission-contract-diseno.md) |
| **No construir de más** | ✅ RULE-008 (backup antes de cambios) + revisión anti-colisión |
| **Tests que verifican lo que NO se debe hacer** | ✅ El lab verifica exclusiones (verification/, *.bak) |
| **Selección de modelo por tarea** | ✅ **llm-router.sh** (batch→R1, visión→GLM, interactivo→DeepSeek) |
| **Índice/caché explícito** | ✅ RAG con índice + context_builder con TTL |

### La conexión MÁS fuerte
El vídeo demuestra con datos lo que el lab ya decidió por diseño:
**"el salto de calidad no lo dio el modelo, lo dio el contrato"** — exactamente
el principio de SVP/mission contract. Y la conclusión del vídeo (Haiku barato
+ spec > Sonet caro + improvisación) es la misma lógica del router del lab
(tareas simples no necesitan el modelo más caro).

### El mensaje incómodo para el lab (honesto)
- El lab a veces sigue el patrón vibe coding en análisis de contenido
  (carruseles: "analiza esto" sin spec formal) — pero es el uso legítimo
  (prototipos/desechables, punto 3 del vídeo).
- Los refactors del lab YA usan el patrón spec-driven de facto (GUIA +
  verificación de equivalencia + suite de tests) — validado.

### Futurible
🟢 **SpecJuts como referencia** — la herramienta open source para dimensionar
el modelo según la spec. El lab ya tiene su equivalente (llm-router.sh +
presupuesto de coste), pero SpecJuts podría inspirar una mejora: **anotar el
modelo recomendado en cada spec/tarea del backlog** (ya se hace informalmente
con el router por tipo).

## Conclusión
**El análisis MÁS valioso del día** — valida con datos empíricos la
metodología central del lab (SVP + mission contract + router). Confirma que el
lab está en el camino correcto: contrato > modelo. Guardado + futurible menor
(SpecJuts como referencia de dimensionamiento).

## Futuribles anotados
- SpecJuts (open source, PyPI): dimensionar modelo según spec — referencia
  para mejorar la selección de modelo por tarea del lab
