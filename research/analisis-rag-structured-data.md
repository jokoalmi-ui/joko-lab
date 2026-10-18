---
title: "Análisis — RAG Over Structured Data (AI Coach John Gabriel, 15 slides)"
type: research
---

# Análisis — RAG Over Structured Data (AI Coach John Gabriel, 15 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 10-ago-2026
**Fuente:** https://www.instagram.com/p/DbcZJWukytP/ — ai_coach_john
**Método:** Descarga 15 imágenes + GLM 4.6V local (600px para velocidad)

---

## Contenido (RAG sobre datos estructurados — BD/hojas de cálculo, no PDF)

1. **RAG Structured Data** — aplicar RAG cuando la base de conocimiento es una hoja de cálculo o BD, no un PDF. Ejecución segura/validada.
2. **Arquitecturas empresariales** con RAG estructurado.
3. *(tabla comparativa / casos)*
4. *(patrones de implementación)*
5. *(integración con SQL)*
6. *(normalización de datos)*
7. *(consultas sobre datos estructurados)*
8. *(chat sobre datos estructurados)*
9. *(generación de código Python/Pandas)*
10. **Manejo de muchas tablas** — embeddings + índice vectorial para recuperar SOLO las tablas relevantes a la pregunta (no cargar todo el esquema). Herramienta: `SentenceTransformer` con **BAAI/bge-small-en-v1.5** (familia BGE que el lab usa).
11. **Validación y autocorrección SQL** — `generate_and_execute_with_retry`: ejecuta la query, reintenta si falla, si persiste el LLM la corrige.
12. **Transformar datos brutos en respuestas conversacionales** — prompt de formato: pregunta + resultado bruto → respuesta natural con números. `format_answer`.
13. **Combinar fuentes estructuradas y no estructuradas** — router LLM clasifica SQL_DATA / DOCUMENT_SEARCH / BOTH; multi-herramienta decide SQL/RAG/ambos.
14. **Medir si la recuperación estructurada funciona** — (1) precisión de ejecución (query sin errores), (2) precisión de resultados (vs tests etiquetados), (3) equivalencia semántica (resultados, no texto SQL), (4) ...
15. **Pitfalls comunes en despliegue RAG estructurado**.

---

## 🎯 Aplicación al LAB — RELEVANTE (mejor que los anteriores)

| Concepto | Lab | Estado |
|---|---|---|
| **RAG sobre BD** | perfume-ia (SQLite coleccion.db) + ledgers JSONL | 🟡 **El lab NO hace RAG sobre su BD SQLite** — consulta SQL directa, sin embeddings |
| **Router SQL/Text/DOCS** (slide 13) | El lab separa: search.py (RAG texto) + consultas SQL manuales | 🟡 No hay router unificado |
| **Autocorrección SQL con LLM** (slide 11) | No existe | 🟢 Idea nueva |
| **Recuperar SOLO tablas relevantes** (slide 10) | No aplica (esquema pequeño) | 🟢 Para BD grandes |
| **Medir recuperación** (slide 14) | GAP ya anotado (Recall@K, MRR) | 🟡 Refuerza el gap |
| **Embeddings BGE** | ✅ El lab usa BGE-M3 (el carrusel usa BGE-small) | ✅ Validación |

### Veredicto honesto

**Este es el carrusel más accionable de los vistos hoy.** El lab tiene una BD SQLite
(perfume-ia, 200 decants) que consulta con SQL directo — **no hay capa de RAG
estructurado** (no se indexan las filas de la BD, no hay búsqueda semántica sobre
perfumes/decants).

**PERO:** con 200 decants, la búsqueda SQL directa + filtros es suficiente y más
rápida que embeddings. El RAG estructurado aporta cuando la BD es grande o las
consultas son ambiguas ("un perfume parecido a X pero más fresco").

### Opciones (no urgente)

1. **No hacer nada** — la BD de perfume-ia es pequeña; SQL directo funciona.
2. **Búsqueda semántica futura** — indexar perfumes/decants con BGE-M3 (el lab ya
   lo tiene) para consultas tipo "parecido a..." → sería el caso de uso del
   carrusel aplicado al lab.
3. **Autocorrección SQL con LLM** — el patrón `generate_and_execute_with_retry`
   es simple y aplicable si algún día el lab genera SQL con LLM.

## Conclusión

Carrusel de calidad (AI Coach John Gabriel, estilo tutorial real). Para el lab:
**material de referencia para el futurible "RAG sobre la BD"** — conecta con el
futurible #2 (evaluación formal RAG). El caso de uso más claro: búsqueda
semántica de perfumes "parecido a..." con BGE-M3 (ya disponible). NO urgente.

## Nota

GLM analizó las 15 slides a ~2 min/imagen (600px). Las slides 3-9 son de
implementación (el detalle fino se pierde en el resumen, pero la estructura
general del carrusel es un tutorial de RAG sobre BD con SQL + LLM).
