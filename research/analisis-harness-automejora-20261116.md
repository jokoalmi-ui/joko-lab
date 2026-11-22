---
title: "Análisis — «The End of Harness Engineering»: el post viral y los dos papers que sí existen (16-nov-2026)"
type: research
---

# Análisis — «The End of Harness Engineering»: el post viral y los dos papers que sí existen (16-nov-2026)

**VERACIDAD:** [VERIFICADO] en lo que se contrasta contra fuente primaria: los dos abstracts se han descargado de la API de arXiv y las citas de este documento son literales de esa copia. [NO VERIFICADO] el «modelo 4B» y las «8 ediciones» del post: no aparecen en ninguno de los dos abstracts.
**CALIDAD:** pendiente (el juez requiere LM Studio con modelo cargado)

**Fuente analizada:** https://www.instagram.com/p/Dfvyri2DKFq/ — @0xsojalsec (Md ismail Sojal), publicado el 14-nov-2026, imagen única de 1242×1535 con el resumen del paper. Contador leído el 16-nov-2026 en el HTML del post: «98 likes, 0 comments». El texto del post es el mismo hilo que @Mr_Buzzoni publicó el 13-nov; el post no añade nada propio.

**Método:** los metadatos del post se han capturado del propio HTML con el navegador y se han congelado en una copia local; los papers se han identificado y descargado por la API pública de arXiv (`export.arxiv.org/api/query`), no por lo que dicen los agregadores. Las cifras que aparecen aquí se han leído del abstract, no de un resumen de terceros.

## Qué afirma el post

El post empieza así: «Chinese researchers put out a paper with a title that should make every agent framework nervous». A partir de ahí sostiene cinco cosas: que el paper se titula «The End of Harness Engineering»; que un modelo pequeño de 4B lee los fallos y propone ocho ediciones; que solo sobrevive la edición que mejor puntúa en preguntas reservadas; que el modelo grande permanece congelado todo el tiempo; y que el trabajo humano se reduce a un solo artefacto, el conjunto de preguntas con el que se examina al sistema.

## Verificación contra fuente primaria

La consulta a la API de arXiv por el título exacto devuelve cero resultados: el campo `totalResults` de la respuesta vale 0 y el documento no trae ninguna entrada. No existe un paper con ese título en arXiv. El propio buscador de X llegó a la misma conclusión y apuntó a los dos papers que sí existen, que son los que se han verificado aquí.

El primero es **Harness²: Recursive Agent Harnessing for an Open World** (`arXiv 2610.14224v1`, 9-oct-2026), de Ruiyao Xu, Yanfei Chen, Zhongying CuiZhu, Bhavana Dalvi Mishra, Yifei Ming, Han Yu, Rujun Han, Chen-Yu Lee y Tomas Pfister. La afiliación dominante es Google Research, con académicos invitados: no es un paper «de investigadores chinos». Su punto de partida es el problema contrario al que describe el post, porque trabaja precisamente en el escenario en que no hay respuestas correctas: los autores escriben que las tareas abiertas llegan sin resolver, «leaving no ground-truth verifiers to reliably guide online harness edits». La solución que proponen no es un filtro por puntuación sino un paso de comparación entre propuestas, el «contrastive Propose-Probe-Compose step», con dos niveles de recursión: uno que mejora el harness de la tarea en curso y otro que extrae experiencia para el harness de mejora continua. Los modelos que usan son GLM-5 y Gemini 3.5 Flash, ambos congelados, y el resultado que publican es «yielding gains of up to 11.5 points on WorkBuddy-Bench, 4.5 points on JobBench, and 11.8 percentage points on LAB». Son tres bancos de trabajo profesional, no una mejora genérica.

El segundo es **Self-Harness: Harnesses That Improve Themselves** (`arXiv 2606.09498v3`, 8-jun-2026), de Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai y Shuyue Hu, del Shanghai AI Lab. Este sí es el paper chino, y es el que se parece al mecanismo del post. Su bucle tiene tres fases: minería de debilidades sobre trazas de ejecución reales, propuesta de modificaciones mínimas atadas a esos fallos, y una fase final de «Proposal Validation, which accepts candidate edits only after regression testing». Trabajan con «MiniMax M2.5, Qwen3.5-35B-A3B y GLM-5» y sostienen que «improves both held-in and held-out pass rates, with overall relative gains of up to 132%». La diferencia con el post es de fondo: aquí el harness se construye «without relying on human engineers or stronger external agents», es decir, el modelo se mejora a sí mismo, no un modelo de 4B que edita a otro.

## Discrepancias, punto por punto

El título es inventado. El post atribuye el paper a investigadores chinos cuando el que lleva el mecanismo descrito es el de Shanghái y el que lleva las cifras de 11,5 puntos es el de Google. La cifra de 11,5 puntos existe, pero es de Harness² en WorkBuddy-Bench, no una mejora general de un «single step» sobre cualquier tarea. El «4B» y las «ocho ediciones» no aparecen en ninguno de los dos abstracts: el post los presenta como datos del paper y no hay forma de sostenerlos con la fuente. El modelo citado, «Claude Fable 5.2», tampoco es el que usan los papers; los modelos reales son GLM-5, Gemini 3.5 Flash, MiniMax M2.5 y Qwen3.5-35B-A3B.

Lo que el post acierta es la dirección: la idea de que el harness se escribe por un bucle de evaluación y no a mano, y la de que el humano se queda con el examen, están en los dos papers. La idea del examen como puesto de trabajo está incluso más clara en Self-Harness, que llama «regression testing» a lo que el post describe como «solo sobrevive la que mejor puntúa».

## Qué aporta al lab

CONFIRMA lo que ya está montado. El ciclo que el laboratorio ya ejecuta —fallo real registrado, propuesta de cambio, validación antes de aceptar— es el bucle de Self-Harness, y el golden set de `evaluar-alucinaciones` es el examen del que habla el post. El aviso del paper coincide con RULE-015: si el examen está mal construido, el bucle se vuelve experto en aprobar un examen malo.

NUEVO y pendiente: ninguna de las dos mecánicas de validación está en el lab tal como las describen los papers. Self-Harness exige una partición **held-out** reservada que no se consulta al proponer la edición, y una regresión que compare held-in y held-out antes de aceptar. Hoy el lab evalúa con el mismo conjunto con el que propone, así que una mejora puede estar sobreajustada al caso que la motivó y parecer igual de buena. La propuesta concreta, no ejecutada: separar del golden set un bloque que se toque solo al final y aceptar una edición de skill únicamente si no baja en ese bloque.

## Lo que NO se puede afirmar

No se puede afirmar que exista un paper titulado «The End of Harness Engineering»: la consulta por título devuelve cero resultados. No se puede afirmar el 4B ni las ocho ediciones: no están en los abstracts, y sin el cuerpo del paper no hay forma de saber si el post los tomó de ahí o los añadió. No se puede afirmar la autoría china del paper que cita 11,5 puntos: sus autores y su afiliación dominante son de Google Research. No se ha leído el cuerpo de ninguno de los dos papers, solo el abstract, así que ningún detalle del método más allá de lo citado está verificado. Y las cifras de arXiv son de las versiones indicadas: `2610.14224v1` y `2606.09498v3`, consultadas el 16-nov-2026.

## Fuentes

- Post: https://www.instagram.com/p/Dfvyri2DKFq/ (@0xsojalsec, 14-nov-2026).
- `arXiv 2610.14224v1` — Harness²: Recursive Agent Harnessing for an Open World (9-oct-2026).
- `arXiv 2606.09498v3` — Self-Harness: Harnesses That Improve Themselves (8-jun-2026).
- API de arXiv consultada el 16-nov-2026; copia de los abstracts y de la consulta por título en `/tmp/src_arx_2610.14224v1.txt`, `/tmp/src_arx_2606.09498v3.txt` y `/tmp/arx_titulo.xml`.
