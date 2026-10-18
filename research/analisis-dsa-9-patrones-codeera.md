---
title: "Análisis carrusel codeera.tech — 9 DSA Patterns (13-ago-2026)"
type: research
---

# Análisis carrusel Instagram — codeera.tech: DSA Patterns (9 patrones)
**VERACIDAD:** [VERIFICADO]

- Fecha: 2026-08-13
- Fuente: https://www.instagram.com/p/DbdZgOQluKq/ (cuenta codeera.tech — repost "DSA Pattern and comment pdf")
- Tipo: carrusel 9 slides (jpg directo)
- Método: navegación sin login → URLs JSON embebido (dedup por ig_cache_key) →
  descarga 9 slides → análisis GLM 4.6V local (`analizar_carrusel_rapido.py`,
  9 imgs en 110s, 12.2s/img) + reintento slide 05 con max_tokens 1200.
  ⚠️ Slide 01 dio 403 con efg truncado y con efg completo reconstruido a mano;
  se resolvió usando los chunks exactos del `<img>` del DOM (5×20 chars) con
  headers de navegador completos (Referer + Sec-Fetch). Pitfall 13 confirmado
  una vez más: NO transcribir efg a mano — extraer del DOM en chunks.
- Clasificación: **APORTA / CONFIRMA** — 9 patrones DSA clásicos, muy alineados
  con la serie de análisis DSA del lab (sliding-window, dynamic-programming,
  system-design). El usuario lo considera "fundamental para el lab".

## CONTENIDO (lo que dice) — ✅ los 9 patrones DSA con su receta

1. **Sliding Window (ventana deslizante):** ventana dinámica sobre
   array/subcadena, mover bordes para solución óptima. Ejemplo: Maximum Sum
   Subarray of size K=3 (inicializar → deslizar → actualizar máximo →
   reconocer patrón). Reconocer: subarray/subcadena contigua con tamaño fijo
   o variable.
2. **Two Pointers (dos punteros):** dos punteros desde posiciones distintas
   (ej. array ordenado) para buscar pares que sumen un valor. O(n) vs O(n log
   n). Reconocer: listas ordenadas, pares, palíndromos.
3. **Fast & Slow Pointers (rápido y lento):** dos punteros a velocidades
   distintas para detectar ciclos en listas enlazadas. Reconocer: estructura
   enlazada, recorrido secuencial, ciclos.
4. **Binary Search (búsqueda binaria):** divide y vencerás sobre datos
   ordenados o espacio monótono; low/high/mid. Ejemplo: buscar 7 en
   [1,3,5,7,9,11]. Reconocer: datos ordenados, encontrar valor o condición.
5. **Greedy (codicioso):** óptimo local en cada paso buscando óptimo global
   (no siempre óptimo). Ejemplo: Selección de Actividades (ordenar por fin
   ascendente, seleccionar sin solapamiento). Reconocer: propiedades "Elección
   Greedy" + "subestructura óptima"; keywords "programar", "maximizar valor
   total", "menor número de ítems". Contraste visual con Programación Dinámica
   (local vs global optimum).
6. **Backtracking:** recursivo e incremental, explora espacio de estados y
   retrocede ante soluciones inválidas. Ejemplo: N-Reinas 4x4 (por columnas,
   conflictos, retroceso).
7. **Monotonic Stack (pila monotónica):** pila en orden creciente/decreciente
   para siguiente mayor/menor en O(n). Ejemplo: Next Greater Element.
8. **Prefix Sum (suma de prefijos):** precomputar sumas → consultas de rango
   en O(1). Ejemplo: [3,1,4,3,1,9] con consultas de rango. Reconocer: muchas
   sumas de subarreglos contiguos.
9. **Difference Array (arreglo diferencia):** múltiples actualizaciones de
   rango en O(1) sobre matriz fija; D[i]=A[i]-A[i-1], reconstruir con prefijo.

## FORMATO (cómo se ve) — 🟡 reutilizable

- Patrón visual "cheat sheet de un patrón por slide": título del patrón en
  grande, estructura de 3 bloques consistentes — (a) "Pattern" / descripción,
  (b) "Example" con diagrama paso a paso numerado (tablas de pasos, estado de
  punteros/ventana/pila en cada iteración), (c) "How to Recognize" con
  checklist de señales del problema.
- Tablas de estado del algoritmo por iteración (muy didáctico: se ve el
  movimiento de pointers/ventana/pila).
- Diagramas específicos: listas enlazadas con punteros (fast/slow), tablero
  N-Reinas, diagrama de comparación Greedy vs DP (local vs global optimum).
- Paleta no extraída en detalle (el análisis de formato fino con browser_vision
  falló en la sesión — ver nota técnica); estilo general de infografía técnica
  con fondo claro.

## APLICACIÓN AL LAB (veredicto honesto)

- **CONFIRMA y amplía la serie DSA del lab** (ya existen analisis-dsa-
  sliding-window.md y analisis-dynamic-programming.md): este carrusel aporta
  el set completo de 9 patrones con su receta de reconocimiento, que es
  exactamente el "marco de patrones" que el usuario considera fundamental.
- **FORMATO: 🟡 accionable** — la estructura "Pattern / Example paso a paso
  con tabla de estado / How to Recognize" es una plantilla excelente para
  material de estudio propio (slides TFM, flashcards, cheatsheet).
- **CONTENIDO: ✅ conocimiento de base** — para el lab (y para el TFM/empleo)
  los 9 patrones son el vocabulario de entrevistas de DSA; no requiere
  implementación en el lab, es material de estudio/referencia.
- **Acción concreta sugerida:** consolidar en un único
  `research/analisis-dsa-9-patrones.md` (o ampliar la serie existente) con la
  tabla de "cuándo usar cada patrón" — el usuario lo valora como fundamental.

## Registro

- Backlog 2026-08-06: entrada añadida (13-ago).
- Slides en /tmp/ig_dsa_pattern/ (limpiadas tras análisis).
- Nota técnica: browser_vision falló (modelo auxiliar rechaza image_url) →
  para formato fino usar GLM con max_tokens >=1200 o el fallback de la skill
  instagram-carruseles-analisis (browser_navigate file:// + browser_vision).
