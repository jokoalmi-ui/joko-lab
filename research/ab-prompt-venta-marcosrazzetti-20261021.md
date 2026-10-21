# A/B de dos prompts de calendario de contenido — carrusel @marcosrazzetti vs versión corregida V2

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** medición propia ejecutada en el host del lab. Datos crudos en `/tmp/ab_prompt.jsonl` y `/tmp/ab_prompt_reanalizado.json`.
**Fecha de las corridas:** 2026-10-21, 11:19–12:16 CEST (verificado con `date`; el fin de la última corrida consta en el log del timer, 12:16:56).
**Modelo:** `qwen2.5:7b` servido por Ollama (`/api/chat`), `num_ctx 8192`, `num_predict 3000`, `temperature` por defecto.
**Potencia:** n = 3 corridas por prompt, intercaladas. Ninguna corrida descartada: 6 de 6 válidas.

## Qué se compara

- **V1**: el prompt tal como lo propone el carrusel del post `DevIL45ChAS` de @marcosrazzetti (1.730 caracteres / 279 palabras). Seis bloques: Rol, Tarea, Contexto, Razonamiento, Formato de salida, Condiciones de finalización.
- **V2**: versión corregida por el lab (1.173 caracteres / 191 palabras). Siete componentes: ROL, MÉTODO, PÚBLICO, CONTEXTO, TAREA, FORMATO, RESTRICCIONES, FIN.

La diferencia de diseño: V2 elimina las cifras de negocio ancladas (5K, 20K, 100K, 2.000 €), mueve las prohibiciones a un bloque normativo, exige TSV parseable, cuantifica la proporción 12/10/8, prohíbe inventar cifras fuera del contexto y añade cláusula de incumplimiento (`[INCOMPLETO: faltan N]`).

## Métrica estática (sin LLM, sobre el texto del prompt)

| Indicador | V1 | V2 |
|---|---|---|
| Componentes presentes (B6 + condición de fin) | 4/7 | 7/7 |
| Prohibiciones, y dónde están | 1 (dentro de Contexto, 0 en bloque normativo) | 4 (3 en Restricciones, 1 en Formato) |
| Cifras de negocio ancladas | 4 | 0 |
| Instrucción de veracidad | no | sí |
| Plantilla repetida en el texto | 4 veces | 0 |
| Formato parseable exigido | no | sí |
| Unidad por fila declarada | no | sí |
| Cláusula de fallo | no | sí |
| Mezcla objetivo/artefacto dentro de la tarea | sí | no |
| Ambigüedades detectadas | 4 | 0 |

## Resultado de las 6 corridas

| Indicador | V1 (n=3) | V2 (n=3) |
|---|---|---|
| Filas generadas | 30, 30, 30 | 30, 30, 30 |
| Filas con 5 campos | 30, 30, 30 | 30, 30, 30 |
| Proporción de tipos | 10/10/10 en las tres | 30/0/0 en las tres |
| Hooks únicos (de 30) | 9, 6, 7 (media 7,3) | 5, 2, 1 (media 2,7) |
| % hooks únicos | 24,4 % | 8,9 % |
| Hooks con estructura repetida | 23, 24, 25 | 26, 28, 29 |
| Molde de hook dominante | «listo para» 10 / «oferta especial» 10 / «sabías que» 10 | «por qué» 15 / 29 / 30 |
| Declara incompleto | 0 de 3 | 3 de 3 |
| Muestra el conteo | 0 de 3 | 3 de 3 |
| Se autocritica | 0 de 3 | 3 de 3 |
| Tabla en markdown | sí | no (columnas alineadas con espacios) |
| Longitud media | 4.667 caracteres | 5.401 caracteres (+16 %) |
| Duración media | 228,8 s | 220,8 s |

## Hallazgos

1. **El formato no se rompe en ninguno de los dos.** 30 filas × 5 campos, 6 de 6. La hipótesis de que la plantilla repetida cuatro veces en V1 induciría una salida de cuatro filas queda refutada.
2. **La instrucción vaga ganó a la cuota explícita.** V1 pedía «alterna» entre tres tipos y produjo 10/10/10 exacto tres veces. V2 declaraba la cuota 12/10/8 y produjo 30 piezas de un solo tipo en las tres corridas. Más precisión en el enunciado no implicó más cumplimiento.
3. **La variedad de hooks no la consigue ninguno.** V1 rota tres moldes distintos (24 % únicos); V2 usa «¿Por qué…?» casi en todas las filas (9 % únicos). V2 declara la repetición en el 100 % de las corridas y la entrega igual.
4. **La condición de finalización funciona como detector, no como corrector.** V2 cuenta, admite y marca `[INCOMPLETO: faltan N hooks únicos]` en 3 de 3. V1 entrega 30 piezas con el 76 % de hooks clonados y las presenta como calendario completo. Ese es el falso ok descrito en RULE-021, reproducido con un modelo pequeño.
5. **Interpretación causal**: con un 7B la carga de autocontrol consume capacidad. V2 gasta un 16 % más de texto, tarda lo mismo y rinde peor en contenido. No se sigue de aquí que V2 sea peor prompt: se sigue que **un 7B no puede ejecutar criterios de aceptación en la misma pasada en que genera**. La corrección exige un segundo paso con el conteo como entrada, o un script que valide.

## Qué NO demuestra esta medición

- No es un test de significación: n = 3 por condición, sin prueba estadística. Las diferencias de proporción (3/3 frente a 0/3) son consistentes, pero no se calcula p-valor.
- Un solo modelo (`qwen2.5:7b`). No se extrapola a 14B, 20B ni a modelos con cadena de razonamiento.
- Un solo caso de contenido (coach de nutrición). No se mide la calidad del texto más allá de la contabilidad: filas, campos, tipos, hooks repetidos.
- Sin evaluación humana de si las piezas sirven para vender. Solo se mide lo que se puede contar.

## Trampas de instrumento encontradas (3)

1. **Regex de prohibiciones con falso negativo.** `\bprohibid\b` no casa con «prohibido»: daba 0 prohibiciones en V2. Corregido a `prohibid\w*`.
2. **Métrica «cifras ancladas» engañosa.** Contaba igual «30 filas» que «100K €», haciendo que V2 saliera peor (17 frente a 10). Separada en «cifras de negocio».
3. **Parser de filas que no cuenta columnas alineadas.** El parser del runner solo entendía tabuladores y pipes y devolvió **0 filas** para las tres respuestas de V2, que tenían 30 × 5. Si se hubiera creído esa cifra, la conclusión habría sido «V2 rompe el formato». Corregido con detección de columnas separadas por dos o más espacios y normalización de tildes.

## Artefactos

- `/tmp/ab_prompt_run.py` — runner del A/B, 3 corridas por prompt intercaladas, JSONL reanudable.
- `/tmp/ab_analiza.py` — analizador v2 (parser de filas, métricas, normalización de tildes).
- `/tmp/ab_prompt.jsonl` — 6 registros crudos.
- `/tmp/ab_prompt_reanalizado.json` — registros con las métricas recalculadas por el analizador v2.
- `/tmp/ollama_repair_20261021_1206.log` — log del relanzamiento de las 3 corridas perdidas.
