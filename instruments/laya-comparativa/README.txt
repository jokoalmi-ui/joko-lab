========================================================================
LAYA-COMPARATIVA — instrumento de medida para Laya (decisiones tipadas)
Joko Lab · ~/joko-lab/instruments/laya-comparativa
Ultima actualizacion: 2026-09-23 22:46 CEST (bloque 8 = latencia limpia)
========================================================================

ESTADO
  [x] Rig preparado y verificado en ejecucion real (15 PASS / 0 FALLO).
  [x] Paquete `laya` 0.3.10 instalado en .venv SIN dependencias (sin torch).
  [x] SET v1 (27 casos) y SET v2 (177 casos, near-miss) generados.
  [x] SET v3 (299 casos = v2 + 122 duros) generado y verificado con stub.
  [x] Test de ROUTING ejecutado sobre v1 y sobre v2 (0 pesos, 0 EUR).
  [x] Baseline local gratuito ejecutado sobre v1, v2 y v3 (+ choice): granite4.2:8b.
  [x] Bloque choice ejecutado sobre v2 (20 casos, 4 opciones).
  [ ] Inferencia Laya: BLOQUEADA. No instalado numpy/torch/transformers y
      no descargados los checkpoints (~843 MB x 3). Nada descargado.

========================================================================
1. QUE MIDE
========================================================================
SET v1 — 27 casos desde el golden set CONGELADO
  tools/golden_set_alucinaciones.json  sha256 2a2da99c... (verificado por script)
  Bloque A (grounding, n=13): 10 true + 3 false. Incluye 5 con formato FICHA.
  Bloque B (trampas, n=8): hechos fabricados que hay que rechazar.
  Bloque D (memoria, n=6): hechos reales sin state (control, NO es el uso previsto).
  Total 16 true / 11 false.

SET v2 — 177 casos = v1 (27, intactos) + 150 near-miss generados
  Fuente: coleccion.db en SOLO LECTURA. Solo campos de catalogo (nombre, casa,
  año, familia olfativa, concentracion, volumen, genero, precio). NO se leen
  notas personales, sensaciones, situaciones ni uso_diario.
  30 fichas x 5 plantillas. Subtipos y clases:
     literal          30  true   el dato, tal cual
     parafrasis       30  true   el dato, dicho de otra forma
     valor_vecino     30  false  el campo esta, pero con OTRO valor
     campo_ausente    30  false  el campo no aparece en el texto
     negacion         15  false  se niega un dato que si esta
     soporte_parcial  15  false  una clausula cierta + una falsa
     grounding        13  true/false  (v1, bloque A)
     memoria           6  true   (v1, bloque D)
     trampa            8  false  (v1, bloque B)
  Total 76 true / 101 false.  0 afirmaciones duplicadas.

DEFINICION DE VERDAD: la verdad la define EL TEXTO del estado que se le entrega
al modelo, no la realidad ni la BD. Asi el instrumento no depende de si la BD
tiene erratas: si el texto dice X, la afirmacion que dice X es verdadera.

SET v3 — 299 casos = v2 (177, intactos) + 122 casos DUROS
  Buscan los puntos donde un modelo pequeño suele romperse:
    multihop      22  dos fichas; comparar el AÑO y atribuir OTRO campo del ganador
    comparacion   22  dos fichas; "el año de A es posterior al de B"
    distractor    25  dos fichas; el valor de una atribuido a la otra
    no_aparece    25  negacion de ausencia ("el campo X no aparece en la ficha")
    cuantificador 20  "las 5 fichas incluidas indican X" (falso si a UNA le falta)
    aguja          8  estado largo (ocho fichas, hasta 1.049 chars) y pregunta por UNA
  Total v3: 138 true / 161 false. States: mediana 135 chars, max 1.049.

Metricas: accuracy (umbral 0.5), Brier, ECE propio (5 bins), ECE con la
convencion del proveedor (15 bins, laya.common.ece_score), sesgo de confianza,
P50/P95, y desglose por bloque y por SUBTIPO (ahi se ve donde se rompe un modelo).

TEMPERATURA DE LOS CASOS: los estados miden 123-300 caracteres (~40-80 tokens).
El limite de 512 tokens del checkpoint ingles no aprieta en este rol de juicio.

========================================================================
2. RESULTADO A — ROUTING (0 pesos, 0 EUR)          [test_routing.py]
========================================================================
El routing del paquete es Python puro (laya/lang.py no importa nada externo) y
Router.route() no carga ni ejecuta ningun modelo: se mide sin descargar nada.

v1 (27 casos, default de fabrica):
    multilingual 19/27    english 8/27
    los 8: trap-03/04/06 + ficha-01..05  (texto corto en español SIN acentos)
v2 (177 casos, default de fabrica):
    multilingual 169/177  english 8/177   (4,5 %)
    los 8 son EXACTAMENTE los mismos del v1: los 150 generados van bien.
v2 con prompt simulado (state + afirmacion juntos):
    default='english'       multilingual 170, english 7
    default='multilingual'  multilingual 174, english 3  <- residuales

DOS MODOS DE FALLO DISTINTOS, medidos:
  A) texto corto, latin, SIN diacriticos y sin evidencia de stopwords ->
     idioma INDECISO -> va al `default`, que de fabrica es "english".
     Casos: los 8 de arriba. Arreglo: Router(default="multilingual").
  B) deteccion POSITIVA erronea de ingles (diacritic_rate justo por debajo del
     umbral de 2 %): 3 casos (gen-017, gen-019, gen-123). El cambio de default
     NO los cubre. Arreglo: pasar el idioma explicito:
         Router().route(state, lang="es")   -> verificado, va a multilingual
     (route() acepta lang= y lang_guess=, segun laya/router.py)

LECTURA PARA EL LAB (español primero): no dejar el idioma a la deteccion.
Pasar lang="es" (o default="multilingual"), porque el formato de ficha en
español sin acentos y el texto corto son justo los dos casos que fallan.

CORRECCION DE UNA HIPOTESIS PROPIA: se planteo que el router mandaria el
español al checkpoint ingles por ser alfabeto latino. FALSO en general: acierta
'es' en 169/177. El fallo es mas estrecho (texto corto sin acentos / deteccion
positiva erronea), y tiene arreglo de una linea.

========================================================================
3. RESULTADO B — BASELINE LOCAL GRATUITO
========================================================================
Modelo: ibm/granite4.2:8b-q4_K_M (Ollama local, 0 EUR). temperature 0, seed 42,
salida restringida por esquema JSON.

v1 (27 casos)  [ollama_granite42.txt]
    n=27  accuracy=1.0  Brier=0.0  ECE=0.0  confiado_y_fallado=0
    P50=3551.1 ms  P95=5217.8 ms      A 13/13   B 8/8   D 6/6
    -> EL SET v1 ESTA SATURADO. No discrimina: cualquier sistema que responda
       "no" cuando el dato no esta y "si" cuando esta saca 27/27.

v2 (177 casos)  [ollama_granite42_v2.txt]
    n=177  accuracy=0.9944  Brier=0.0056  ECE(5 bins)=0.0056
    P50=2906.4 ms  P95=4151.4 ms      confiado_y_fallado=1
    POR SUBTIPO: negacion 14/15 (0.9333) y TODO lo demas a 1.0000
      (literal 30/30, parafrasis 30/30, valor_vecino 30/30, campo_ausente 30/30,
       soporte_parcial 15/15, grounding 13/13, trampa 8/8, memoria 6/6)
    El UNICO fallo es gen-085 (negacion): el texto dice "Concentracion: EDP" y
    la afirmacion NEGABA ese dato; la respuesta correcta era false y el modelo
    respondio p=1.0 (certeza maxima justo en el unico error).
    -> Ampliar con near-miss NO rompio al 8B: el set v2 sigue casi saturado.
       Lo unico que separa es la NEGACION, y ese fallo unico esta ademas
       maximamente confiado (dato de calibracion, no de acierto).

BLOQUE CHOICE (20 casos, 4 opciones)  [resultados_choice_ollama_v2.json]
    n=20  accuracy=1.0  P50=3109.3 ms  P95=3484.4 ms   -> tambien saturado.

v3 (299 casos, con los DUROS)  [ollama_granite42_v3.txt]
    n=299  accuracy=0.9264 (277/299)  Brier=0.0736  ECE(5 bins)=0.0736
    P50=2957.1 ms  P95=4022.6 ms      fallos con p>=0.8: 10 de 22
    POR SUBTIPO (peor -> mejor):
      cuantificador   20  0.6000   <- 8 fallos, TODOS falsos negativos (gt=True, p=0.0)
      distractor      25  0.8000   <- 5 fallos (4 aseveran el valor cruzado con p=1.0)
      multihop        22  0.8182   <- 4 fallos
      aguja            8  0.8750
      no_aparece      25  0.8800   <- 3 fallos: afirma "no aparece" cuando SI aparece, p=1.0
      negacion        15  0.9333   <- el unico fallo es gen-085 (el mismo del v2)
      comparacion     22  1.0000
      campo_ausente   30  1.0000   literal 30/30  parafrasis 30/30  valor_vecino 30/30
      soporte_parcial 15  1.0000   grounding 13/13  memoria 6/6  trampa 8/8
    -> El v3 SI DISCRIMINA: 22 fallos frente a 1 en v2. Modos de fallo encontrados:
       (a) cuantificador: niega un "todas las fichas incluyen X" que es verdadero
           (sesgo a decir que no: 8 de 8 fallos son falsos negativos).
       (b) no_aparece: AFIRMA AUSENCIA cuando el dato SI esta en el texto. Es el
           fallo mas relevante para un gate: una ausencia inventada, con p=1.0.
       (c) distractor: acepta el valor de la OTRA ficha como propio.
    -> 10 de los 22 errores van con p>=0.8: errores CONFIADOS (dato de calibracion).
    -> Desde aqui el v3 permite comparar modelos por acierto, no solo por latencia:
       es el set con el que tiene sentido medir a Laya.

COMPARACION DE MODELOS SOBRE v3 (299 casos, mismo codigo de puntuacion)
[comparativa_v3.txt]
  modelo                          n     acc   Brier    ECE5   P50ms  err.conf
  granite4.2:8b-q4_K_M          299  0.9264  0.0736  0.0736  2957.1   10
  qwen2.5:7b                    299  0.8094  0.1612  0.1610   250.8   32
  deepseek-r1-distill-qwen-14b  299  0.7960  0.2015  0.2027  1997.4   36
  discrepancias entre modelos: 77/299 (26%) -> el set SI separa modelos.
  Detalle, tabla por subtipo y conclusiones: ver COMPARATIVA-v3.txt

CAVEAT DE INSTRUMENTO (propio, importante): la metrica `sesgo` (confianza media
modelo perfecto tiene confianza media ~0,43 (no 1,0), asi que sale un "sesgo" de
-0,56 que NO significa infraconfianza. En sets desbalanceados usar Brier y ECE,
que si lo hacen bien. En el v1 (16 true / 11 false) el sesgo era interpretable;
en el v2 ya no lo es.

FALLO DE INSTRUMENTO CORREGIDO (no era el modelo): el primer intento dio 27/27
casos sin respuesta ("Okay, let's see. The user"): el modelo no obedecio
"responde SOLO con un numero". Arreglado con salida JSON restringida (format +
esquema) y parser tolerante (JSON -> ultimo numero). Sin ese arreglo habria
sido un falso negativo del modelo.

========================================================================
4. BACKENDS Y ESTADO
========================================================================
  stub    : offline, determinista. Verifica el arnes. NO es un resultado.
  ollama  : ejecutado en v1 y v2 (granite4.2:8b). 0 EUR. Tambien implementa
            la primitiva choice (elegir 1 de N).
  laya    : BLOQUEADO limpio (exit 5). Falta numpy/torch/transformers y los
            checkpoints (~843 MB por checkpoint, ~2,5 GB los tres).
            OJO: el paquete compila la doc de `choice` con >20 opciones como
            punto debil; por eso el bloque choice usa 4 opciones.
  jev     : no ejecutado. Requiere token en ~/.config/joko-lab/jev.env
            (chmod 600), que aporta el usuario; nunca por el chat.

========================================================================
5. COMO SE REPRODUCE
========================================================================
  cd ~/joko-lab/instruments/laya-comparativa
  .venv/bin/python run_test.py --selftest
  .venv/bin/python run_test.py --backend stub
  .venv/bin/python run_test.py --backend ollama                  # v1
  .venv/bin/python run_test.py --backend ollama --set v2         # v2
  .venv/bin/python run_test.py --backend ollama --set v3         # v3 (duros)
  .venv/bin/python run_test.py --backend ollama --set v2 --choice
  .venv/bin/python run_test.py --backend ollama --dry-run
  .venv/bin/python run_test.py --entorno
  .venv/bin/python test_routing.py            # v1
  .venv/bin/python test_routing.py v2         # v2
  .venv/bin/python test_routing.py v2 --detalle
  .venv/bin/python generar_casos_v2.py        # regenera v2 (determinista)
  .venv/bin/python generar_casos_v3.py        # regenera v3 (determinista)

========================================================================
6. AVISOS
========================================================================
· Casos con detalles internos del lab: ctx-06 y trap-08 (marcados `interno`).
  Usar --excluir-internos antes de sacar esto del lab.
· Valores de PRUEBA en los casos de campo ausente: son fixtures para provocar
  invencion, NO datos sobre la realidad. No publicar como cifras.
· `laya.ece_score` (contraste del proveedor) requiere numpy/torch: contraste
  pendiente.
· COBERTURA REAL DE LA BD (medida, no supuesta): de 328 filas, `precio` tiene
  dato en 1 y `volumen` en 1; `año`, `familia olfativa`, `concentracion` y
  `genero` en 108/108. Por eso los ejes numericos de precio y volumen NO se
  pueden usar en los casos duros: comparan por AÑO. Si algun dia se rellenan
  esos campos, el generador los vuelve a usar solo (pools por campo).
· El set v2 se genera desde la BD en solo lectura; si la BD cambia, v2 cambia
  (mismo ORDER BY id + misma semilla = mismo resultado mientras la BD no cambie).
  Regenerarlo invalida los resultados v2 guardados: hay que re-ejecutar el
  baseline si se toca.

========================================================================
7. INTEGRIDAD (sha256) — ver comando al final
========================================================================
(preparar_casos.py, motor.py, run_test.py, test_routing.py, generar_casos_v2.py,
 casos_noul.json, casos_v2_noul.json, casos_v2_choice.json, README.txt,
 routing_out.txt, routing_out_v2.txt, ollama_granite42.txt, ollama_granite42_v2.txt,
 resultados_*.json)
  golden set de origen : 2a2da99cc7001128f9c58bc2812f78a590f1a13aa34195191dafa01934fbe1d1
  laya                 : 0.3.10 (PyPI, instalado --no-deps; torch no importado)
  python               : 3.11.16

  sha256 verificados el 2026-09-23 20:26 CEST:
  preparar_casos.py           8a015fe42a1a2d4233b81e116b06a84adbd562e72d202ce05da45660dccd33cf
  motor.py                    89cce1a3b2dd0444591318e1cfaa5b2ef0d4904e2eb0520a961a1fcf4d186249
  run_test.py                 5aef76be17588ac86487d1a1de0d4edeb4264cbc1016d757f7c6f0ac1c42a54e
  test_routing.py             db9bc59c8f6a8415b259e013a232d1e6acfbde3d56969c1e320a0721026279f3
  generar_casos_v2.py         f1280588b502215b51d1aeab08e6767a10cc3c109faf505e8e5700827844e1bb
  generar_casos_v3.py         a9822afa1daaab57757dfc80b152ec85ffc62b9aa09db5dc0584926011075972
  casos_noul.json             f5bb2a1f6b3d5cde5d182eecb71dd9cac26e45f90b97289e758a62289d84af48
  casos_v2_noul.json          765503df4e84a0a7854e23aa6cbd955f217ff9322815332cbfa1687a0947cddf
  casos_v3_noul.json          d86aed0600a3f1b7efd4056e479865dcc3843df6c25eb5fc346146406e04648d
  resultados_ollama.json      cb41caf66f161542bd67daf43e762817855387a270004aa571d5baad15df0dd0
  resultados_ollama_v2.json   1eb26b0f6db86afd548c17eb94777ef7f15e3b5b49f2d072927df618a074a03e
  resultados_ollama_v3.json  b7678a447487ae0b5ad0fb1719da2e5e8d9dde69adf3fbd5bdde62b557aecfd5
  -- hashes posteriores (2026-09-23 20:44) --
  run_test.py           c3a62b9d55ee692b0ac8ef9bcb26700bdc18179ebb451cc965d73cde16a17cc1
  comparar_modelos.py   d68b36bd8fb8a117c398298754b7718650b0e329f7ee97c419d880faf0667725
  COMPARATIVA-v3.txt    c1d9346c3f82f0e2d39c75f016ad4de917d354c219147036cb06b3a6297b5eda
  comparativa_v3.txt    b79c84577e9cb73f960b4f38d751dec4283b8607c42bdc5e393b400e5af8fce9
  ollama_qwen25_v3.txt  fba545d379fb2dc948ad75a5be29115cf73e97d39a5eb4dec6e5f65024bae4c6
  ollama_r1distill14b_v3.txt  ee614723d13ee771c5b49012c7b01de9102e3753ec16748119aa4ef30e2a1807
  resultados_ollama_qwen257b_v3.json  68f65e4e5a5c8b72a8a8724f4b1c57068c8a22dbc23e1d99d67fde297c479bc9
  ...deepseekr1distillqwen14blatest_v3.json  ef5bd7832b2c6df0380f42080804e67deb49e1a86f0c487dd5149b507e5de7b5
  (el sha256 de ESTE README se calcula aparte: un fichero no puede contener el suyo)
========================================================================

========================================================================
8. LATENCIA LIMPIA Y CAUSA RAIZ DEL DESBORDAMIENTO (2026-09-23 22:46)
========================================================================
TRES PASADAS DEL MISMO SET v3, para separar el MODELO de la CONFIGURACION:
  (1) 20:44  LM Studio ocupaba ~9 GB de VRAM · num_ctx por defecto del Modelfile
  (2) 22:23  VRAM libre (810 MiB)          · num_ctx por defecto del Modelfile
  (3) 22:45  VRAM libre                    · num_ctx=8192   <- LA VALIDA
Ficheros de las tres: previaVRAM_* · vramlibre_* · numctx8192_*
(el runner AVISO "no se detecto fichero nuevo" en la pasada 2: una excepcion
 hardcodeada para granite le devolvia el nombre generico y pisaba el fichero de
 la pasada 1. Corregido: ahora TODOS los modelos llevan su sufijo. Los
 resultados de (1) se salvaron por copia previa, con sha256 coincidente con los
 ya publicados.)

CAUSA RAIZ (medida con /api/ps y /api/show, no supuesta)
  El runner enviaba temperature 0.0, seed 42 y esquema JSON, pero NO num_ctx.
  Mandaba el default del Modelfile: granite4.2:8b 131072, r1-14b 64000.
  -> huellas de 18,05 GB y 16,27 GB en una GPU de 12 GB: 8 y 6 GB a la CPU.
  Solo qwen2.5:7b cabia entero (5,71/5,71 GB) porque su default ya era pequeno.
  Fijando num_ctx=8192 (sobra: los estados miden 123-300 caracteres):
     granite4.2:8b  vram 6,05 / total 6,05 GB   ENTERO EN GPU
     qwen2.5:7b     vram 4,91 / total 4,91 GB   ENTERO EN GPU
     r1-14b         vram 9,52 / total 9,52 GB   ENTERO EN GPU
  Se envia via env LAYA_NUM_CTX (default en codigo: 8192) y queda REGISTRADO
  en el meta de los resultados junto a temperature y seed.

LATENCIA: LO QUE COSTABA LA CONFIGURACION, NO EL MODELO
  modelo        num_ctx Modelfile   num_ctx=8192   ganancia
  granite4.2:8b       2957,1 ms        473,7 ms      6,2x
  r1-14b              1997,4 ms        737,8 ms      2,7x
  qwen2.5:7b           250,8 ms        273,1 ms      (ruido)
  [comparativa_numctx8192.txt]

TABLA FINAL (medicion valida: los tres enteros en GPU)  [numctx8192_*_v3.json]
  modelo                          n     acc   Brier    ECE5   P50ms   P95ms  c.err
  granite4.2:8b-q4_K_M          299  0.9164  0.0836  0.0836   473.7   683.4    11
  qwen2.5:7b                    299  0.7993  0.1674  0.1701   273.1   449.3    34
  deepseek-r1-distill-qwen-14b  299  0.8060  0.1908  0.1923   737.8   974.2    34
  (c.err = errores con p>=0,8)

VEREDICTO DEL GATE — invariante en las tres pasadas
  subtipo `trampa` (hechos fabricados; la respuesta correcta es "falso"):
     granite4.2:8b  8/8 -> 8/8 -> 8/8   (las tres condiciones)
     qwen2.5:7b     2/8 -> 1/8 -> 1/8   (ECE 0,74 en ese subtipo)
     r1-14b         2/8 -> 2/8 -> 2/8
  -> GATE: granite4.2:8b con num_ctx fijado. Cuesta 474 ms, no 2957 ms.
  -> qwen2.5:7b: solo filtrado barato de bajo riesgo.
  -> r1-14b: sin ventaja (peor calibracion, 9,52 GB, 1,6x mas lento que granite).
  -> DEBIL EN LOS TRES: `cuantificador` 0,55 los tres. Esa decision deberia
     resolverla codigo determinista, no un modelo.
  El `accuracy` agregado se movio <=1 punto entre pasadas identicas (mismo set,
  temp 0, seed 42): lo unico que cambiaba era el reparto GPU/CPU, asi que ese
  reparto perturba tambien las respuestas. HIPOTESIS declarada, no hecho.

INFORME COMPLETO: FINAL-gate-y-latencia.txt

  sha256 verificados el 2026-09-23 22:46 CEST:
  motor.py                     daba6ce19c8eec9b15258efd65c223e522377749521e93370a2021a60a343af2
  run_test.py                  a0187053e196a585d97b852644aa4ada357544bd8e41784378c9a5d5403cf57e
  FINAL-gate-y-latencia.txt    8bf1d9df4621d0139aa110662b941949932ca543a278d71618c328ffb8bef056
  comparativa_numctx8192.txt   2d205ecb4dacd06a6b1bc38d7825be2550bd25dbce844353a62cc80271139f53
  numctx8192_granite_v3.json   c2631f1d593e8d325041c63cd0003c1004832ba7911bf5dce11e0265f08e19b9
  numctx8192_qwen_v3.json      38ac575b6023cbfa8e077cc4d0b89699417cd8890ae6d5b3423c41348067fb2b
  numctx8192_r1_v3.json        6bb6e6801bea0312b77c070008b8cd1d2b6a6ce6b1e04e16614c1aa3f1c4fc14
  (el sha256 de ESTE README se calcula aparte)
========================================================================"""

