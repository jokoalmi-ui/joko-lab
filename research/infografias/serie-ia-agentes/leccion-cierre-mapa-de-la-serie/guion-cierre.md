# Guion — pieza 9 (CIERRE) · «El mapa de la serie»

- **id**: `CIERRE` · **nivel**: 6 (la serie tiene 6 niveles, 0-5: **no es un nivel del curso**, es la pieza que cierra el arco) · **pieza 9 de 9**
- **Título (registro)**: «El mapa de la serie: 6 niveles y 8 piezas»
- **Canal**: LinkedIn, **documento PDF de 7 páginas** · **cadencia**: lunes, miércoles y viernes · **objetivo**: 2026-10-05 (lunes)
- **Serie**: «IA y agentes, de cero a producción» (`research/infografias/serie-ia-agentes/`)
- **Carpeta**: `leccion-cierre-mapa-de-la-serie` (empieza por `leccion-` a propósito: así la recoge `extraer_post.py --todas`)

## 0. Fuente del contenido (receta §0)
Es una pieza **de cierre**, no un subnivel: el plan no tiene subnivel para ella. Desviación declarada:
- el **índice de niveles** sale de la tabla «CLASIFICACIÓN POR NIVELES» del plan (`research/analisis-techyybanda-ai-agents-20260914.md`);
- los **títulos, fechas y ganchos** de las 8 piezas salen del registro de la serie (`seguimiento.json`), que es el crudo de la serie;
- **no se ejecuta medición nueva** (decisión del usuario, 30-sep-2026): se citan las mediciones propias ya publicadas y se **recuentan** con `verificar_cifras.py` desde los dos crudos copiados a esta carpeta (`medicion-multiagente-20260927.json` y `medicion-alucinaciones-20260914.json`).
- La otra serie del lab (`linkedin-lab`) no se toca.
- **Sin enlaces**: 6 de las 7 publicadas tienen `url: null` en el registro (la app móvil no deja copiar el enlace). Solo L0 tiene URL; meter una sola rompería el índice, así que el texto remite a «mi perfil».

## 1. Para qué existe
Cerrar el arco: quien llega tarde ve por dónde entrar; quien las ha leído tiene el recorrido entero de un vistazo. No enseña nada nuevo — **ordena lo ya publicado**.

## 2. Las 7 slides (textos exactos)

**S1 · portada.** kicker `CURSO DE IA Y AGENTES · CIERRE` · h1 `EL MAPA DE LA SERIE` · sub `6 niveles y 8 piezas: de «qué es un LLM» a sacarlo a producción` · arte `s1-escalera-crema.png` · pie `6 NIVELES · 8 PIEZAS` | `CIERRE · PIEZA 9`

**S2 · el mapa.** kicker `CIERRE · 1/5 EL MAPA` · h1 `SEIS NIVELES, UNA ESCALERA` · 6 filas (nivel 0-5), cada una con qué cubre y **qué te llevas**:
- `0 · FUNDAMENTOS` — Qué es un LLM, la escalera de términos y qué se le puede pedir. *Te llevas*: la máquina no busca, genera, y tiene un techo de contexto.
- `1 · INSTRUCCIONES` — Cómo pedirlo: formato, ejemplos, rol. *Te llevas*: el mismo modelo, otra instrucción, otra salida.
- `2 · CONECTADO AL MUNDO` — Tus documentos (RAG) y herramientas. *Te llevas*: el modelo pasa de hablar a tocar tus ficheros.
- `3 · EL BUCLE` — Percibir, razonar, actuar, revisar. *Te llevas*: la diferencia entre contestar y hacer.
- `4 · DE UNO A MUCHOS` — Varios agentes colaborando. *Te llevas*: colaborar cuesta x3,90 en tokens y x4,68 en tiempo (medido).
- `5 · PRODUCCIÓN` — Fiabilidad, coste y límites. *Te llevas*: el listón lo fija una batería de casos, no una demo.
- Caja: `El orden no es decorativo: casi todos los atascos que veo son una pieza usada sin la anterior. Si una te suena a chino, el hueco está antes.`

**S3 · pieza a pieza (el «qué se llevó cada una»).** kicker `CIERRE · 2/5 PIEZA A PIEZA` · h1 `QUÉ TE LLEVAS DE CADA UNA` · 8 filas con el **título real** de cada pieza + su idea:
- `L0` «Qué es un LLM: la máquina que no busca, genera» → Genera, no consulta; y cada palabra cuesta ~1,4 tokens (medido).
- `L0-A` «IA, ML, Deep Learning y LLM: la escalera de términos» → Dejar de mezclar cuatro palabras que no son lo mismo.
- `L0-B` «Qué puedes pedirle y qué no (usos y tamaño del modelo)» → Lo que sí (resumir, clasificar, traducir) y por qué el tamaño decide.
- `L1` «Instrucciones: el prompt» → Formato, ejemplos y rol: pedir bien cambia la salida.
- `L2` «El modelo conectado al mundo: datos y herramientas» → Tus documentos (RAG) y herramientas: de hablar a hacer.
- `L3` «El agente: el bucle» → Percibir, razonar, actuar, revisar: la diferencia con un chat.
- `L4` «De uno a muchos: agentes que colaboran» → Colaborar cuesta x3,90 tokens y x4,68 tiempo para el mismo acierto (medido).
- `L5` «Producción: fiabilidad, coste y límites» → El listón es una batería de casos, no una demo.
- Caja: `Ocho piezas, una idea cada una. Ninguna pide programar: piden leerlas en orden.`

**S4 · la confusión típica.** kicker `CIERRE · 3/5 LA CONFUSIÓN TÍPICA` · h1 `EMPEZAR POR EL FINAL` · tabla 3 filas (`SE DICE` / `QUÉ PASA`):
- «Con ChatGPT ya sé lo suficiente» → El chat te da la salida; la pieza que falta es la que la vuelve repetible.
- «Los agentes son lo importante; lo demás es relleno» → Un agente sin instrucciones ni datos es un bucle que se equivoca rápido y caro.
- «Un modelo mejor lo arregla» → El modelo es una pieza: el listón lo fija el control más flojo.
- Par ✗/✓: ✗ `Saltar al nivel 5 y montar un agente el primer día.` ✓ `Entrar por la pieza que cubre tu duda y subir de una en una.`
- Caja: `El orden de la serie no es un temario: es el orden en el que aparecen los atascos.`

**S5 · ejemplo real.** kicker `CIERRE · 4/5 EJEMPLO REAL` · h1 `UNA TAREA, SEIS CAPAS` · arte `s5-torre-capas-crema.png` · 6 filas: el mismo encargo («resume este PDF y avísame por correo») y qué añade cada nivel:
1. Saber qué puede hacer (nivel 0): resume, pero no copia literalmente.
2. Pedirlo bien (nivel 1): formato, longitud, destinatario.
3. Darle el PDF y el correo (nivel 2): el dato y la herramienta.
4. Dejarlo en bucle (nivel 3): que lo mande, lo compruebe y se repita si falta algo.
5. Poner dos (nivel 4): uno resume y otro revisa (y cuesta x3,90).
6. Medirlo (nivel 5): diez PDFs de prueba y un techo de gasto.
- Caja: `La misma tarea existe en el nivel 0 y en el nivel 5. Lo que cambia es lo que se cae por el camino.`

**S6 · dato medible.** kicker `CIERRE · 5/5 DATO MEDIBLE` · h1 `LA SERIE EN NÚMEROS` · dato grande `0/81` · sub `respuestas que se inventaron un dato: 27 casos x 3 pasadas, con 16 aciertos y 11 abstenciones correctas en cada una.` · tabla: `8 piezas · 6 niveles` / `3 mediciones propias` / `1,4 tokens por palabra (pieza 1)` / `x3,90 tokens y x4,68 tiempo al colaborar (pieza 7)` · caja con el límite del medidor · método al pie.

**S7 · cierre.** kicker `CIERRE · CIERRE` · h1 `POR DÓNDE EMPEZAR` · 3 ideas:
1. ¿Aún no sabes qué es un LLM? Empieza por el nivel 0.
2. ¿Ya lo usas y quieres que haga cosas? Niveles 1 y 2: instrucciones y herramientas.
3. ¿Quieres que trabaje solo y sin sustos? Niveles 3, 4 y 5: el bucle, varios agentes y la medición.
- arte `s7-llave-crema.png` · bloque final: `FIN DE LA SERIE · 8 PIEZAS + ESTE MAPA` + `Nueve entregas, de cero a producción. Si una te sirvió, dime cuál.`

## 3. Cifras y de dónde salen (recuento propio, no heredado)
Salida literal de `python3 verificar_cifras.py` (recuenta los dos crudos copiados a esta carpeta):
- multiagente 27-sep: A 6/6 · 22.121 tokens · 537 s | B 6/6 · 86.256 tokens · 2.515 s | **x3,90 tokens, x4,68 tiempo** | reintentos 1 (0 útiles, 1 inútil) | llamadas 14 → 30.
- alucinaciones 14-sep: 3 pasadas think=**False** (seeds 42/43/44) → **0 invenciones**, 16 aciertos + 11 abstenciones en cada una, honestidad 1,0 → **0 de 81 respuestas**.
- pasadas con razonamiento ACTIVADO (3,70 / 11,11 / 14,81 %) → **no se publican**: son del contador, no del modelo (una quedó invalidada en el crudo por artefacto del clasificador).
- tokens por palabra: 1,4 (medición de la pieza 1, en sus notas del registro; su crudo no está en esta carpeta).

## 4. Límites declarados
- El índice **no lleva enlaces** (registro con `url: null`): es un mapa por títulos, no un enlazador.
- La pieza **no mide nada nuevo**: reutiliza dos mediciones propias y su límite (el medidor marcaba rechazos honestos como invención) ya publicado en la pieza 8.
- La L5 publicada dice «FIN DEL RECORRIDO · 5 LECCIONES»: sigue siendo cierto (5 niveles de lecciones); este mapa no es una lección más.

## 5. Incidencias de producción (30-sep-2026)
- **Arte escena 1**: la semilla 202 (escalera) salió con fondo gris (160,158,155) y no normalizaba con ningún umbral. Se generaron candidatos (303/404/515) y se usó la **303** (borde exacto crema). Detalle en `arte/arte.txt`.
- **Pies**: el primer montaje puso pie en las 7 slides; las **8 piezas anteriores de la serie llevan 1** (la portada). Se alineó a 1 pie y se re-renderizó. El render anterior (7 pies) queda **descartado**: su revisión visual ya no aplica.
- **Revisor**: `revisar_slides.py` guarda ahora el md5 de cada slide y solo reutiliza una fila si el PNG no ha cambiado. Antes, tras un re-render, habría dado por buenas imágenes que ya no existen (el mismo fallo que reutilizar la caché temporal de otra pieza: los ficheros se llaman igual).
- **Cifras**: recalculadas del crudo con `verificar_cifras.py`, no heredadas del registro.

## 6. Pendientes
- Publicar: es un documento PDF (`carrusel-cierre.pdf`) + texto de post.
- Empujar el commit de L5 (`8a16b23`) sigue pendiente de OK.
