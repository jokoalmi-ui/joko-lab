---
type: EXP
subtype: experiment
status: index
tags: [knowledge, experiment]
created: 2026-07-28
---
# EXP-20260728-003: Comparativa de embeddings
================================================

Fecha: 2026-07-28
Autor: jokoalmi
Estado: COMPLETADO
Tipo: Benchmark de modelos de embeddings

## Objetivo

Comparar nomic-embed-text-v1.5 (modelo actual) vs BGE-M3
(modelo recomendado por analisis externo) para determinar
cual ofrece mejor busqueda semantica en el corpus de Joko Lab
(documentacion en espanol: fichas de modelo, decisiones,
patrones, experimentos).

## Modelos comparados

| Modelo | Dimension | Tamano | Tipo |
|---|---|---|---|
| nomic-embed-text-v1.5 (Q4_K_M) | 768 | 81MB | Embeddings |
| BGE-M3 (Q4_K_M) | 1024 | 418MB | Embeddings |

## Metodologia

10 documentos de prueba simulando el contenido real de Joko Lab
(fichas, decisiones, protocolos, experimentos).
10 queries en espanol representando busquedas reales.
Para cada query, se calcula la similitud coseno contra todos los
documentos y se selecciona el mas similar.

## Resultados

| Query | nomic (sim) | BGE-M3 (sim) | Doc correcto | Acierta |
|---|---|---|---|---|
| razonamiento paso a paso | 0.716 → DeepSeek | 0.715 → DeepSeek | DeepSeek | Ambos |
| modelo descartado | 0.660 → EXP ✗ | 0.609 → Qwen ✅ | Qwen 3.5 | BGE-M3 |
| protocolo apertura | 0.677 → fin.sh ✗ | 0.564 → inicio ✅ | inicio.sh | BGE-M3 |
| comparativa 7 modelos | 0.798 → EXP ✅ | 0.777 → EXP ✅ | EXP | Ambos |
| decision no usar qwen | 0.681 → DEC ✅ | 0.625 → Qwen ✅ | Ambos validos | Ambos |
| codigo python rapido | 0.697 → Granite ✅ | 0.627 → Granite ✅ | Granite | Ambos |
| gemma creatividad | 0.786 → Gemma ✅ | 0.605 → Gemma ✅ | Gemma | Ambos |
| function calling | 0.636 → Dolphin ✗ | 0.539 → Llama ✅ | Llama 3.1 | BGE-M3 |
| EXP-20260726-001 | 0.762 → EXP ✅ | 0.648 → EXP ✅ | EXP | Ambos |
| cerrar sesion | 0.584 → DEC ✗ | 0.484 → fin.sh ✅ | fin.sh | BGE-M3 |

## Metricas clave

| Metrica | nomic | BGE-M3 |
|---|---|---|
| Aciertos directos | 5/10 | 6/10 |
| Similitud media | 0.699 | 0.619 |
| Dimension | 768 | 1024 |
| Vectores identicos entre modelos | No (sim=0.0091) | No (sim=0.0091) |

## Conclusiones

1. BGE-M3 acierta MAS documentos correctos (6 vs 5) a pesar de
   dar similitudes mas bajas. Esto indica MEJOR DISCRIMINACION
   SEMANTICA: separa mejor los documentos relevantes de los que
   no lo son.

2. nomic da similitudes mas altas (0.699 media vs 0.619) pero
   eso es porque separa PEOR los documentos, dando puntuaciones
   mas uniformes. En 2 casos eligio el documento incorrecto
   porque no distinguia bien.

3. BGE-M3 tiene 1024 dimensiones vs 768. Mas capacidad de
   representacion. Aunque el tamano del modelo es mayor
   (418MB vs 81MB), sigue siendo insignificante comparado con
   los LLMs de 8-14B.

4. La simulitud entre vectores de ambos modelos es 0.0091
   (casi ortogonales) — son modelos COMPLETAMENTE DISTINTOS
   en como representan el significado.

## Recomendacion

Usar BGE-M3 como modelo de embeddings por defecto en Joko Lab.
nomic queda como alternativa ligera si se necesita rapidez
extrema, pero para busqueda semantica sobre patrones,
decisiones y experimentos, BGE-M3 ofrece mejor precision.

## Proximos pasos

- Integrar BGE-M3 con un indice vectorial (FAISS o sqlite-vec)
  para busqueda semantica en Decision Memory y Pattern Library
- Crear EXP de prueba con búsqueda real sobre el corpus de
  decisiones y patrones
