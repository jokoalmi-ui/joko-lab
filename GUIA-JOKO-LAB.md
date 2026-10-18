---
title: "GUIA COMPLETA DE JOKO LAB"
type: guia
---

# GUIA COMPLETA DE JOKO LAB

> **¿Quieres entender el lab desde cero?** Existe una guía de APRENDIZAJE
> (progresiva, explica cada término en contexto): `GUIA-APRENDIZAJE-JOKO-LAB.md`
> (creada 05-ago-2026). Esta guía es para CONSULTA rápida.

**Version:** 1.6.28 - 2026-10-13
**Autor:** Hermes (agente) para Joseba — Joko Lab
**Alcance:** Todo el laboratorio, de lo mas basico a lo mas complejo
**Fuente:** Datos reales verificados del sistema (1-ago-2026) + skills del lab
**v1.6.28 (13-oct-2026):** LOS CUATRO CAMBIOS DEL DIA QUE FALTABAN + `AGENTS.md` AL DIA (18 -> 21 reglas). Auditoria de esta sesion contra la realidad medida: la seccion 3.10 no recogia el arranque del motor local bajo demanda ni el criterio cloud-first sin trinquete, y no habia ninguna entrada para los instrumentos nuevos (dimension 2, rutas, incluida). Evidencia por commit:

**1. Router: arranque del motor local BAJO DEMANDA (commit `b806b7c`, 13-oct 19:52, `tools/llm-router.sh` +50/-3).** Si `:1234` esta caido el router ya no se planta: asegura el servidor con `lms server start` (sin GUI), con lock, timeout doble y el exito acreditado en el puerto. Medido: `:1234` caido -> servidor arriba en 2 s -> gpt-oss-20b cargado -> respuesta en 39 s, sin la app abierta. **Bug medido y corregido**: `lms server start` lanza la app DESPRENDIDA y esa app heredaba el fd del lock (sin CLOEXEC), con lo que el lock quedaba retenido para siempre y el arranque siguiente moria esperando 60 s a un proceso inexistente; el arranque va en subshell con el fd 9 cerrado. Detalle en 3.10.

**2. Orquestador: criterio cloud-first SIN trinquete (commit `07cb051`, 13-oct 12:50, +48/-6).** El criterio contaba toda fila con `local_ok` falso — incluidas las decisiones `cloud_directo`, que no son fallos del motor — y sin ventana temporal: eso lo convertia en un trinquete, porque un fallo de codigo (`lms` fuera del PATH, RULE-021) dejaba el tipo en cloud PARA SIEMPRE al no llegar nunca un ok que lo reseteara. Ahora cuenta solo intentos locales REALES y vigentes (`VENTANA_DIAS = 7`) y respeta un corte declarado, humano y reversible (`INVALIDAR_ANTES_DE = 2026-10-13T07:37+02:00`, la hora del arreglo del PATH). `tasa_fallo()` gana el parametro `vigente`. Detalle en 3.10.

**3. Instrumento nuevo: auditoria de crons en 3 CAPAS (commit `acd3e8d`, 13-oct 07:20, `tools/auditar_crons.py` 305 l. + `tests/test_auditar_crons.py` 251 l., 556 inserciones).** Cubre el punto ciego MEDIDO de los dos vigilantes que ya existian (`watchdog-informes-cron.py`, cron diario 12:00, y `barrido-informes-fallidos.py`): los dos detectan el fallo solo por la cabecera `(FAILED)` o la cola `## Error`, y el formato de fallo ACTUAL de Hermes es `**Status:** script failed` (informe real: `~/.hermes/cron/output/da39a2148b34/2026-10-12_08-05-44.md`). Solo lectura. Detalle en 4.6.

**4. Instrumentos nuevos del paquete de evaluacion de resultados (commit `297ee8b`, 13-oct 07:20, +350/-17).** `tools/cerrar_ficha_dia.py` (135 l., punto 1: cierra la marca de valoracion pendiente de la fila `uso_diario` del dia y ANADE la linea de cierre, nunca reescribe; no inventa valores: sin fila para la fecha sale con error) y `tools/revision_produccion_semanal.py` (149 l., punto 3: 4 numeros medidos; sobre los JSONL grandes usa solo `os.stat` para no repetir el kill del 12-oct). Ademas `tools/escanear_predicciones.py` (21 lineas tocadas) y `PRED-001/002` + plantilla al dia. Detalle en 9.1b.

**5. Ruta (dimension 2):** la telemetria diaria F1/F2 del cron `telemetria-observer-diario` (22:00, script `observer-daily.sh`) aterriza en `04-operations/metrics/telemetria/`: un `YYYY-MM-DD.json` + un `YYYY-MM-DD.md` por dia (ultimo medido: `2026-10-13`). La ruta no estaba escrita en ninguna seccion. Detalle en 4.6.

**Deuda anterior detectada, NO tocada aqui:** las guias de aprendizaje (`GUIA-APRENDIZAJE-JOKO-LAB.md` y `.txt`) siguen en 04-sep-2026; su puesta al dia necesita plan propio (47 KB + 65 KB de prosa).

**v1.6.27 (13-oct-2026):** ERRATA DE LA v1.6.26 + ETIQUETAS DEL BLOQUE `## GPU` EN EL INSTRUMENTO DE ORIGEN (RULE-013: el fallo se declara como dato). **Lo que se corrige**: la v1.6.26 afirmaba que la fuente «no da usado» y que el cloud habia escrito la memoria DISPONIBLE. Falso por medicion sobre el propio instrumento (`tools/informe-diario-local.sh`, consulta `nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu`): el crudo SI trae usado y temperatura (13-oct: `9561 MiB, 12282 MiB, 1 %, 38` -> usado `9561`, libre `2721`, temperatura `38` grados); el «Memoria disponible 9561» y los «38 procesos en cola» los escribia el RESUMEN del propio informe (LLM local): la fuente se contradecia a si misma. **Arreglo aplicado** (2 ficheros, commit de esta misma fecha): el instrumento imprime la leyenda `memoria_usada_mb | memoria_total_mb | uso_gpu_pct | temperatura_c` sobre los numeros crudos, y el prompt del resumen tiene prohibido renombrarlos. **Medido, no supuesto**: copia del instrumento en `/tmp` con la salida redirigida (el informe de produccion NO se toco) + extractor local con el prompt real de `04-operations/metrics/batch/cola.jsonl` -> `gpu_mem_usado_mb: 1560` y `gpu_temp_c: 44`, `FIDELIDAD: (True, 'fidelidad_ok')` y `verifier: (True, 'json_valido')`; antes de la cura el mismo camino daba `95.61`, `123` y `null`. **No verificado**: la prosa del resumen (en la corrida de prueba salio degradada por motor ocupado). JL-013/RULE-005 en la misma sesion; backups PRE `tools/informe-diario-local.sh.bak-20261013-gpu-etiquetas` y `GUIA-JOKO-LAB.md.bak-20261013-errata-gpu`.

**v1.6.26 (13-oct-2026):** GATE DE FIDELIDAD DE DATOS EN EL CAMINO `batch-json` DEL ORQUESTADOR (RULE-021). **El fallo medido**: la salida local del orquestador (`tools/local_cloud_orchestrator.py`, `cmd_run`) escribio `gpu_mem_usado_mb: 95.61` —cifra que NO existe en la fuente (el informe trae `9561`; `grep -c '95\.61'` sobre `04-operations/reports/20261013-informe-local.txt` = **0**)— y el verifier determinista la dio por BUENA (`local_ok: true`, `motivo: json_valido`): solo comprobaba FORMATO (JSON parseable + claves), no contenido, y ese JSON es el que alimenta el artefacto de produccion (`04-operations/metrics/batch/2026-10-13/informe-json.json`). Un `ok` con el error descartado es un `ok` falso. **El arreglo** (commit `8182799`, 1 fichero, +36/-4, recibo `tree_sha=26e29ad15e41923867b543bf28a55055cca77dac`, aprobado `joseba` 16:54:32): `verifier(tipo, salida, fuente="")` recibe tambien la fuente, y una salida `batch-json` que pase el formato se cruza ADEMAS contra el prompt con `tools/verificador_fidelidad.py` (numeros/IDs/fechas; determinista, 0 LLM, sin umbrales): sin respaldo -> `cifras_sin_respaldo: <detalle>` y NO pasa. **Fail-closed**: si el verificador no se puede cargar o revienta, tampoco pasa. **Probado con dato real, no supuesto**: las dos salidas reales de hoy (`95.61` y `123`) -> bloqueadas; un control correcto (campos `null` donde la fuente no da el dato) -> `PASA`; la firma antigua de dos argumentos sigue valiendo. **Limite conocido y declarado**: el gate es NUMERICO, no semantico — el mismo dia el motor cloud escribio `gpu_mem_usado_mb: 9561` **[CORREGIDO en v1.6.27: estaba mal leido — `9561` es la memoria USADA (libre = 12282 - 9561 = 2721) y el crudo SI trae «usado» y la temperatura; el renombrado erroneo lo hacia el resumen del propio informe, y el arreglo fue en el INSTRUMENTO (etiquetas), no en el prompt]**. **Cadena completa medida por primera vez** en la 3ª corrida del dia: el local devolvio JSON truncado -> `json_invalido` -> **escalo a cloud** (`local_ok: false`, `escalo_cloud: true`, `latencia_s: 22.34`; cloud ok en 4,4 s). **Tambien queda documentado el otro eslabon de la misma cadena** (commit `46a5214`, 13-oct): el PATH del planificador no incluye `~/.lmstudio/bin`, asi que `lms` pelado no existe (`command -v lms` rc=1) y el router antiguo se tragaba el 127 a `/dev/null`; el router ya autocarga ese PATH y reporta el error real. **Verificado end-to-end** el 13-oct 15:30 con el modelo descargado y el PATH del planificador: el log de LM Studio muestra `Client=lms-cli Endpoint=loadModel ... openai/gpt-oss-20b` y la GPU pasa de 1662 a 9818 MiB con el modelo `loaded` (55,02 s, 0 USD); el 12-oct 23:15 no hubo NI UN evento de la CLI (0 `Client=lms-cli`, 0 `Endpoint=loadModel`), que es lo que delato que la causa era el PATH y no la VRAM. **Pendiente, no oculto**: `~/.hermes/scripts/lmstudio-headless.sh:45` llama `lms` pelado (mismo agujero, sin comprobar). JL-013/RULE-005 aplicados en la misma sesion; backup PRE `GUIA-JOKO-LAB.md.bak-20261013-gate-fidelidad`.
**v1.6.25 (13-oct-2026):** CORRECCION DE UN DATO YA OBSOLETO DE LA SECCION 7.10 — el puente manual LAB <-> Gemini web **no esta virgen**. Su `outbox/` guarda desde el **12-oct 17:05** un prompt REAL de 6.905 B (`2026-10-12-1705-cabos-sueltos-futuribles-envio-a-espana-y-vias-r.md`, herramienta prevista `deep-research`, 7 marcas "futuribles" de `futuribles.db`) esperando a pegarse en la web de Gemini; estado medido el 13-oct: `outbox 1 / inbox 0 / procesados 0` y `registro-puente.md` sigue en "(ninguno todavia)" -> lo que falta es la ida y vuelta manual, no estrenar el puente. El dato anterior ("el puente real quedo virgen (`outbox 0 / inbox 0 / procesados 0`)") era **cierto al escribirlo** (12-oct, verificacion PREVIA al estreno) y quedo obsoleto al usarse el puente esa misma tarde; la entrada historica v1.6.23 **no se reescribe** (el changelog es registro). Alcance del dato comprobado (grep `virgen|puente-gemini|puente real` en `~/joko-lab/**/*.{md,txt}`): vivia solo en esta guia — `puente-gemini/README.md` y `04-operations/registro-uso-gemini.md` no lo afirman. Backup PRE: `GUIA-JOKO-LAB.md.bak-20261013-puente-virgen`. JL-013/RULE-005 aplicados en la misma sesion.
**v1.6.24 (12-oct-2026):** FIX DE ANCLA INTERNA. El ancla `<a name="capitulo-8"></a>` estaba en la **linea 1904**, justo antes del encabezado de la seccion **7.10** (`Instrumento de coste y ahorro de tokens`), mientras que el encabezado `# CAPITULO 8 — SINCRONIZACION ENTRE SESIONES` vive en la **1968** -> el indice (`[Capitulo 8 — Sincronizacion entre sesiones](#capitulo-8)`, linea 199) saltaba al sitio equivocado. Ahora el ancla esta **inmediatamente antes** del encabezado del capitulo 8, como las otras 10 (`capitulo-0` .. `capitulo-10`). Solo se movio 1 linea: no cambia ni una palabra de contenido.
**v1.6.23 (12-oct-2026):** PUENTE MANUAL LAB <-> GEMINI WEB (INSTRUMENTO DE MEDIDA DE LA SUSCRIPCION AI PRO). Peticion del usuario (12-oct, opcion 1 de 3). **El problema medido**: `04-operations/registro-uso-gemini.md` llevaba **todas las semanas en blanco** (2.304 -> 3.350 B con el anadido de hoy; agosto semanas 1-5 vacias, septiembre y octubre sin abrir) -> las **dos revisiones mensuales** del KO `DEC-GAIPRO-001` (05-sep y 04-oct) se decidieron por **testimonio** del usuario (`monitoring.current: 3`, ultimo chequeo REAL 05-sep). La causa no era falta de uso sino **falta de instrumento**. **Lo que NO es posible (verificado 05-sep-2026, no supuesto)**: la suscripcion AI Pro **no da creditos de API**; el **login OAuth de Gemini CLI se cerro el 18-jun-2026** para cuentas individuales (AI Pro incluido); automatizar la web (cookies, scraping, MCP de navegador) **viola los ToS -> riesgo de baneo**. Manual si, programatico no. **Puente creado**: `04-operations/puente-gemini/` con `README.md` (66 lin.), `plantilla-prompt.md` (45 lin.), `registro-puente.md` (17 lin.), `.gitignore` propio y 3 carpetas de trabajo (`outbox/` el LAB escribe el prompt, `inbox/` el usuario pega la respuesta, `procesados/` las verificadas) -> **el contenido de esas 3 carpetas queda FUERA de git**; se versionan solo los 3 documentos. **Herramienta**: `tools/puente_gemini.py` (199 lin.; `nuevo "<tema>" [--herramienta X] [--contexto FICHERO] [--nota-interna TXT]` / `estado` / `archivar <fichero> [--valor N] [--herramienta X] [--nota TXT]`; herramientas `3.1-pro`, `deep-research`, `notebooklm`, `gem`, `workspace`; `TOPE_CONTEXTO` 400 KB; **no usa red, no borra y no sale de su carpeta**; override `PUENTE_BASE` para pruebas). **Verificado ANTES de estrenarlo, no despues**: 2 pases completos en sandbox (`nuevo` -> respuesta simulada en `inbox/` -> `archivar --valor 4` -> idempotencia -> `estado`); en el primer pase se cazo un **bug de acentos** (el placeholder del registro se buscaba sin tilde y no se limpiaba), corregido y **re-probado**; el puente REAL queda **virgen** (`outbox 0 / inbox 0 / procesados 0`). **Registro al dia**: semanas 6-10 marcadas SIN REGISTRO con su causa y **cierre del 04-oct** (MANTENER, tomado del KO, no reinventado); backup PRE `.bak-20261012-puente`. **Frontera de datos del puente**: no credenciales, no datos de terceros, no sesiones enteras. **NO se toco** `monitoring.current` (sigue 3: es testimonio del 05-sep y hoy no se ha medido ninguna tarea nueva). Backups PRE de esta entrada: GUIA `.bak-20261012-puente` y `DEC-GAIPRO-001.yaml.bak-20261012-puente`. JL-013/RULE-005 aplicados en la misma sesion. **Pitfall de doc detectado y NO tocado en ese commit**: el ancla `<a name="capitulo-8"></a>` estaba **antes** de la seccion 7.10 -> **corregido en v1.6.24**, misma sesion.
**v1.6.22 (10-oct-2026):** PROTOTIPO DE CV DEL LAB (2 COLUMNAS · 1 HOJA A4 · COURIER) FIJADO COMO FORMATO POR DEFECTO PARA ENVIAR A OFERTAS. Peticion del usuario (10-oct 13:32 CEST, hora medida con `date` por RULE-012): «vamos a dejar de momento este formato como el prototipo de CV para enviar a las ofertas de trabajo. Lo quiero asi o lo mas parecido cuando te pida un CV, claro esta que habra veces que tendremos que ajustarlo a la oferta en concreto. Documentalo». **Origen**: el CV en 2 columnas construido hoy desde `~/empleo-seguimiento/cv-2col-1pag-2026.{html,pdf,docx}` tras 3 correcciones suyas en el mismo dia (email `jalbizua@gmail.com` y telefono `677 016459` **en negrita**; tipografia **Courier New**; linea del **carnet sin zonas cubiertas**; **Master sin «Online» y con 105 h**). **Cifras medidas, no supuestas** (`pdfinfo` / `pdftotext -bbox` / `pdffonts`, 10-oct): con Calibri 8 pt cabia en 1 hoja (A4 594,96 x 841,92 pts, yMax 763,80); **con Courier 8 pt se iba a 2 paginas** (a la 2ª caian idiomas, carnet y S.M.D.) -> apretado a **7,6 pt / interlineado 1,15 / margenes `8 9 7 9 mm`** vuelve a **`Pages: 1`**, yMax **764,28** (limite util 799) = ~35 pt (~12 mm) libres. **Dos limites medidos y declarados, no ocultados**: (1) **Courier New no esta instalado** en el PC -> el sistema resuelve a **Liberation Mono**, metricamente compatible (el PDF embebe `LiberationMono` + `LiberationMono-Bold`); (2) **el DOCX NO cabe en 1 hoja**: convertido desde el HTML, LibreOffice no respeta ni el `@page` ni el reparto de columnas y da **3 paginas** -> el entregable de «1 hoja» es el **PDF de Chrome**, y el DOCX se corrige con `scripts/fix_docx_font.py` (LibreOffice escribe la pila CSS entera como **nombre de fuente literal** `"Courier New;Liberation Mono;Nimbus Mono PS;Courier;monospace"`, que Word no resuelve; 4 sustituciones en `word/styles.xml` verificadas con `w:ascii=`). **Artefactos**: en la skill `cv-adaptado-ats` quedan en disco `templates/cv-prototipo-2col-1hoja.html` (**copia byte a byte** del documento real, md5 `ee836b84858b736f5da898061f36ae37`) y `scripts/fix_docx_font.py` (md5 `a7cd2de29eabe86b8ed019fd13b17ba4`); la especificacion completa (tabla de valores CSS, pipeline, verificacion y ajuste por oferta) va a su `references/prototipo-cv-2col-1hoja.md` (5.057 B) y a la nueva §3.b del SKILL.md (**v1.4.2**, 24.001 -> 25.660 B / 368 -> 396 lineas). **Gate de skills**: el lote lo bloqueo `skills.write_approval` (quedo en `~/.hermes/pending/skills/7651374d.json`; verificado que el SKILL.md seguia en `1.4.1` y el reference no existia) y se aplico despues **escribiendo los bytes del lote con herramientas de fichero, con OK explicito del usuario** — la via que funciono el 08-oct (v1.6.16). **Verificado tras aplicar**: `diff` contra el backup = **exactamente 4 hunks** (frontmatter, §3 paso 1, §3.b, pitfalls) y **ninguna linea del original perdida** (solo 3 lineas sustituidas); md5 de la plantilla identico al documento real. El **maestro `cv-maestro-2026.*`** se dejo intacto al crear el prototipo, pero se **alineo despues en la misma sesion** (10-oct): la linea del Master tambien quedo `Master en IA e Innovacion, 105 h — Founderz (2026)` en el maestro y se regeneraron sus dos derivados con el mismo pipeline. **PDF**: Chrome headless 155 (`--no-pdf-header-footer`; el PDF viejo tampoco llevaba cabecera/pie), `Pages: 2`, A4 594,96 x 841,92 pts. **DOCX**: `soffice --headless --infilter="HTML (StarWriter)" --convert-to "docx:MS Word 2007 XML"` — **sin `--infilter` falla con «no export filter for ...docx found»** (pitfall medido) — y corregido con `fix_docx_css_stack.py`: la etiqueta `w:rFonts` llevaba la pila CSS entera como nombre literal `"Calibri;Carlito;Liberation Sans;Arial;sans-serif"` **en sus 4 atributos** (`w:ascii`, `w:hAnsi`, `w:eastAsia`, `w:cs`) -> 4 sustituciones a `Calibri`, verificado `0 etiquetas con ';'`. **`diff` del texto del DOCX antes/despues = solo esa linea**. Backups PRE: `cv-maestro-2026.{html,pdf,docx}.bak-20261010-align-master`. **Linea de contacto del maestro**: detectada con el marcador `correo: (por confirmar)` al alinear el maestro (misma sesion del 10-oct) y **resuelta despues esa misma tarde, con autorizacion del usuario** (10-oct 13:47 CEST, hora medida con `date` por RULE-012): la linea queda `Erandio (Bizkaia) · **677 016459** · **jalbizua@gmail.com** · linkedin.com/in/joseba-albizua-millan-287b4328`, con **telefono y email en negrita** (`<b>` en el HTML: la misma decision de contacto que el usuario pidio para el prototipo de 2 columnas). Regenerados los dos derivados con el mismo pipeline de la linea anterior y verificados **antes** de copiarlos a sitio: **PDF** (Chrome headless) -> **`Pages: 2`** (el paginado no cambia), A4 594,96 x 841,92 pts, `pdftotext` -> `por confirmar` **0** coincidencias / `jalbizua@gmail.com` **1**; **DOCX** (`--infilter=\"HTML (StarWriter)\"` + `fix_docx_css_stack.py`) -> **4 sustituciones** (`Calibri;Carlito;Liberation Sans;Arial;sans-serif` -> `Calibri`), `unzip -p word/document.xml` -> `jalbizua@gmail.com` **1** y `por confirmar` **0**, **0** etiquetas `w:rFonts` con `;`. **`md5` POST**: HTML `40c14024651c42ae5d7bd523ffd3d42c`, PDF `f608091ee31ba33b5c7328450d1a7e73`, DOCX `b93de32664009892f06800c94da3443d`. **Backups PRE**: `.bak-20261010-contacto` (HTML `5c070a7df527be642ecaec836e2221fd`, PDF `3def55ed98c9f244f53593fb88c3b740`, DOCX `7a607ee27c3fb163090b67fb512868d1`). `~/empleo-seguimiento` **no es repositorio git** -> ahi la red de seguridad son las copias `.bak-*`. Backups PRE: GUIA `.bak-20261010-cv-prototipo` y `cv-adaptado-ats/SKILL.md.bak-20261010-2col`. Commit de esta entrada: el commit de cierre de la entrada v1.6.22 (solo `GUIA-JOKO-LAB.md`), firmado con recibo RDD en la misma sesion. **RULE-020** (`01-knowledge/objects/RULE-020.yaml`, 25 campos canonicos identicos a RULE-019: `type` RULE, `status` activo, `decision_origin` directriz_usuario, `confidence` 0,9 ALTA, `domain` contenido, `scope` cv_entregables_ofertas, `dependencies` RULE-015, `next_review` 10-nov-2026, `expires` 10-ene-2027): «CV para ofertas: prototipo de 2 columnas en 1 hoja A4 (Courier 7,6 pt) y el entregable de «1 hoja» es el PDF de Chrome, nunca el DOCX», con alcance (solo CV para ofertas; el maestro no hereda el formato de 2 columnas), los dos limites medidos y su indicador de vigilancia (`paginas_del_pdf_de_chrome_del_cv`, baseline 1, revision 10-nov-2026). Indice OKF regenerado con el generador canonico (`/usr/bin/python3 tools/generar_indice_okf.py`, que necesita el `yaml` del python del sistema): **32 -> 33 objetos**, diff del indice = **solo la linea de RULE-020** (+ la cuenta Total); `verificar_fk_kos.py --gate` -> **GATE FK: OK** (sin rotas bloqueantes; sigue **1** aviso de prosa, el preexistente DEC-004 -> RULE-CONF-001).

**v1.6.21 (09-oct-2026):** DEC-006 Y RULE-019 - LA CACHE DE EXPERTOS ENTRA EN LA NORMA DEL LAB (MoE QUE NO CABE EN VRAM). El veredicto del `EXP-20261009-008` deja de ser un informe y pasa a norma. **DEC-006** (`01-knowledge/objects/DEC-006.yaml`, 108 lineas, `confidence` 0,6 MEDIA, 9 evidencias, `next_review` 09-nov, `expires` 09-ene): «para el patron MoE que no cabe, lanzar `llama-server` con `--moe-cache-mib 512`, nunca con 0». Cifras que la sostienen (`temp=0`, `-ngl 99 -ncmoe 28 -c 2048 -ub 128`, Qwen3.6-35B-A3B MXFP4 de 18,9 GiB en RTX A2000 12 GB): estructurada **5,55 -> 8,54 tok/s** (512 da 8,95; 256 da 7,47; 1024 da 8,54/9,01) y prosa **7,54 -> 11,88 tok/s**; **C=2048 NO arranca** (fallo al reservar los buffers de la cache); 3 replicas contra 3 sin solape; ruido medido 9-11 %. **RULE-019** (`01-knowledge/objects/RULE-019.yaml`, derivada de DEC-006, `domain` ai-architecture, `dependencies` DEC-006 + RULE-015): la regla operativa con su alcance (no aplica a densos ni a modelos que caben enteros), sus limites declarados (swap al 100 % y ComfyUI de fondo durante la medida: el contraste relativo vale, la cifra absoluta no se extrapola) y el bloqueo del lanzador (`lms load` NO expone el flag -> `llama-server` 2.55.0 a mano en puerto propio, con `LD_LIBRARY_PATH` al vendor CUDA; receta en la DEC). Indice OKF regenerado con el generador canonico: **30 -> 31 objetos indexados** (linea de DEC-006 con `exp:2027-01-09`); `verificar_fk_kos.py` sigue en **1 sola referencia a revisar**, la preexistente (prosa de DEC-004 -> RULE-CONF-001). Cadena de commits: `383383a` (diseno) -> `6bbe675` (ejecucion + veredicto) -> `73ed096` (DEC-006 + indice + GUIA) -> commit de cierre de esta entrada (RULE-019 + GUIA). Backups PRE-cambio de esta GUIA: `.bak-20261009-dec006` y `.bak-20261009-rule019`. JL-013/RULE-005 aplicado en la misma sesion.
**v1.6.20 (09-oct-2026):** COMPROBACION EN SOLO LECTURA DEL FUTURIBLE `--moe-cache-mib` (autorizada por el usuario desde Telegram, tras el analisis A4 de Nichonauta). Pregunta: ¿lo admite el servidor de llama.cpp del lab? **Medido sin ejecutar mas que `--help` y greps**: (1) de los **23 runtimes** de llama.cpp instalados por LM Studio (**2.16.0 -> 2.55.0**), **solo el mas nuevo** `llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0` (`libllama-common.so.0.6.0`) contiene la cadena `moe-cache-mib`; en `2.52.0` (mismo `libllama-common.so.0.6.0`) y en los 21 anteriores NO; `-n-cpu-moe` si esta en todos desde `libllama-common.so.0.0.1`. (2) El **lanzador no lo expone**: `lms load --help` -> `--gpu`, `-c/--context-length`, `--parallel`, `--ttl`, `--speculative-draft-*`, `--identifier`, `--estimate-only`, `-y` (ningun flag de llama.cpp). (3) El binario suelto **falla**: `llama-server --help` -> `error while loading shared libraries: libcudart.so.12: cannot open shared object file` (exit 127); el runtime SI esta en `~/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1/libcudart.so.12` -> lanzamiento manual **posible, NO probado**. **Correccion de lo escrito en v1.6.19**: la condicion no es «exige llama.cpp propio» sino «el lanzador no pasa el flag». Analisis actualizado en su §7 (`research/analisis-nichonauta-llamacpp-optimizacion-20261009.md`). Sin experimento propuesto.

**v1.6.19 (09-oct-2026):** CARPETA `research/transcripciones/` PARA TRANSCRIPCIONES LIMPIAS + 1 ANALISIS NUEVO (Nichonauta, llama.cpp). Creada al archivar la transcripcion del video tecnico `zR7nPlyLQGo` («IA Local con llama.cpp — Guia de OPTIMIZACION para Modelos y GPUs», 09-10-2026): `research/transcripciones/<video_id>-<tema>.txt`. Criterio (ahora en el paso 7 de la skill `vigilancia-canales-youtube`): la transcripcion limpia de un video **tecnico** se archiva; la de un video de **venta** NO. Analisis del video: `research/analisis-nichonauta-llamacpp-optimizacion-20261009.md` ([VERIFICADO], 15.061 B) -> **VALIDACION, no hallazgo**: el tema ya estaba cubierto (`analisis-tutorial-llamacpp-rendimiento.md` 13-ago, `estudio-moe-12gb-lab.md` y `veredicto-qwen-35b-a3b-lab.md` 10-ago). Verificado a nivel de CODIGO contra `ggml-org/llama.cpp` (master): el release CUDA se compila con `-DGGML_NATIVE=OFF` (10 ocurrencias en `release.yml`) y el conjunto por defecto de arquitecturas de `ggml/src/ggml-cuda/CMakeLists.txt` incluye **`86-real`**; el `compute_cap` del A2000 del lab es **8.6** (medido con `nvidia-smi --query-gpu=name,compute_cap`) -> mismo `86-real` -> **no hay nada que compilar para ganar velocidad en esta maquina**. `GGML_CUDA_FA_QUANTS` por defecto = `q4_0-q4_0;q8_0-q8_0;f16-f16;bf16-bf16` (lo que el video llama «Q4, Q8, F16, BF16»): **las combinaciones no compiladas caen al kernel f16-f16 con aviso** -> matiz nuevo para la regla de KV cuantizada del lab. Futurible registrado y NO propuesto: `--moe-cache-mib` (exige llama.cpp propio; LM Studio no lo expone). Backups PRE `.bak-20261009-transcripciones`.

**v1.6.18 (09-oct-2026):** ALTA DEL CANAL `NotFound404` EN EL RADAR DE YOUTUBE (8 -> 9 canales). Peticion del usuario («Añadelo») tras analizar 4 de sus videos (`research/canal-notfound404-videos-20261009.md`). Canal **@NOTFOUND404dev**, ID **`UCBYcKHnzmc9nkOXCRJ0VZJQ`** VERIFICADO contra su propio feed RSS (9 videos, 218 suscriptores). Cambio en `tools/monitor_yt.py` (`CANALES` + comentario de trazabilidad). **Verificado antes de commitear, en solo lectura**: `py_compile` sin errores; `--check` -> `feeds OK: 9/9`, state 356 videos; consulta en vivo al feed del canal -> 9 videos / 218 subs; radar `_detectar_outliers(min_views=100)` -> **2 outliers REALES** (`Claude Code: el sistema que gano el hackathon de Anthropic` 1.026 views = **13,9x**; `Como crear un cerebro para Claude Code y ChatGPT FACIL` 6.937 views = **93,7x**; baseline 74). Es el caso que justifica el canal: un canal pequeno (baseline 74) con picos fuertes alimenta el radar justo por encima del corte. **Estado sembrado en el mismo momento del alta** (`python3 tools/monitor_yt.py`, patron de la skill): 11 videos marcados como vistos -> 5 de Nichonauta (4 nuevos de hoy, entre ellos «IA Local con llama.cpp — Guia de OPTIMIZACION para Modelos y GPUs»), 1 de IBM Technology, 1 de Nick Saraev y los 4 de NotFound404; a partir de ahora el cron `vigilar-yt-outliers` (09:30) ya los incluye. **Tres copias sincronizadas a la vez** (leccion del 19-sep): script + tabla de `instagram-monitor` + tabla de `vigilancia-canales-youtube` (**v1.3.0**; su descripcion pasa a 9 canales); la skill `youtube-content` deja de repetir la cifra y apunta a `CANALES` como fuente de verdad. Backups PRE `.bak-20261009-alta-notfound404` (GUIA + 3 SKILL.md). Detalle del procedimiento: `references/alta-de-canal.md` de la skill `vigilancia-canales-youtube`.
**v1.6.17 (09-oct-2026):** VIGILANCIA DE CANALES DE TELEGRAM + CRITERIO DEL RADAR DE OUTLIERS MEDIDO Y AJUSTADO. (Aclaracion del usuario: los «canales del lab» son Telegram + YouTube.) **(1) Monitor de Telegram**: `tools/monitor_tg.py` (166 lin., 6583 B en `e4d17a0`, recibo `tree f25d620a4ca9f48b1697402bdf89388084b4802b`) + wrapper `~/.hermes/scripts/vigilar-tg.sh` + cron `vigilar-canales-tg` (`b9f9a6491c84`, `45 9 * * *`, `no_agent`, Telegram). Via `https://t.me/s/<usuario>` (vista web publica: sin login y sin token del bot). **Medido con HTTP real**: solo `techwith_ram` es vigilable (**200**, 128.187 B); `jugaldb` y `dailydoseofds` devuelven **302** (sin vista web) -> NO vigilables por esta via. Diferencia con el monitor YT: la primera vez que ve un canal **siembra su historico SIN imprimirlo** (no inunda el chat). Verificado de punta a punta con 5 pruebas (`--check` 0 -> 1a pasada 20 publicaciones registradas -> 2a en silencio -> `--check` 20) y run manual del cron (`silent (empty output)`, `Result: ok`); state `~/.hermes/state/monitor_tg_state.json` 6.725 B / 20 entradas. **(2) Radar de outliers (opcion B) medido y ajustado**: `_detectar_outliers` recorre **los 8 canales** (`monitor_yt.py:186`) — el informe del cron solo MUESTRA los que pasan el corte, asi que leerlo como «el radar solo mira 3 canales» era un falso positivo de lectura. Con `min_views=1000` **Nichonauta quedaba ciego por construccion** (mediana 116, maximo 526: 0 candidatos y `max_score` 0.0). Cambio aplicado (decision del usuario «las 3»): `min_views` 1000 -> **100** + flag nuevo `--min-views`; md5 del tool `e802dbeaa8fe101d6b3798e65471a0d3`. **Re-medido DESPUES del cambio** (misma pasada, sin escribir nada): Nichonauta pasa de 0 a **9 candidatos** y su `max_score` sube a **4,8x** — sigue por debajo de 10x, asi que quedan **los mismos 3 outliers** (IBM 43,1x / Nate Herk 10,1x / Joaquin Ruiz 35,2x) = cobertura SIN ruido. **Pitfall de lectura registrado**: el informe del radar NO es la lista de canales vigilados. Documentado en `~/.hermes/skills/joko-lab/vigilancia-canales-youtube` (v1.2.0, + `references/monitor-telegram.md`) y `references/outlier-detector-detalle.md`. Backups PRE: `monitor_yt.py.bak-20261009-minviews`, `GUIA-JOKO-LAB.md.bak-20261009-tg`, `SKILL.md.bak-20261009-telegram`, `outlier-detector-detalle.md.bak-20261009-radar`.

**v1.6.16 (08-oct-2026):** SKILL DE EMPLEO PUBLICO DEL AYUNTAMIENTO DE ERANDIO + SEGUNDO GATE (ESCRITURA DE SKILLS). Peticion del usuario: «Crea una skill para busqueda de empleo en el ayuntamiento de Erandio». **Comprobado ANTES de escribir**: 0 ficheros «randio» en `~/.hermes/skills` y las dos vecinas (`empleo-emprendimiento-bizkaia`, `seguimiento-empleo`) cubren BeHargintza/DEMA/HAZILAN+ y el scan general de ofertas, NO el empleo publico municipal -> **skill nueva** con referencias cruzadas que prohiben duplicar. **`~/.hermes/skills/bizkaia/empleo-publico-erandio/SKILL.md`** (12.873 B / 213 lin., md5 `bb4dcfe8680b5c5e8add8e825923ab4a`) + **`references/fuentes-verificadas-20261008.md`** (6.303 B, md5 `e79b497d8e63a2d39200f55124d1fb8a`). **Fuentes verificadas EN VIVO con navegador el 08-oct a las 12:30 CEST** (hora medida, RULE-012): OPE `.../Hacienda/Paginas/FuncionPublica-prueba.aspx` (14.301 chars; la variante SIN `-prueba` **no renderiza**, contraprobado), «Bolsa de trabajo» (historico 2009-2020: NO es listado vigente), Area de empleo (cita 94 417 56 16), BOB `bizkaia.eus/es/bob` (nº 193, CVE `BOB-2026a193`, 33 anuncios, buscador TEXTO LIBRE) y sede `tramitegunea.erandio.eus`. **Declarado SIN VERIFICAR**: Lanbide (el host `.eus` lo bloquea el navegador; el valido es `.net`) y el nº de dias del plazo (se cita de las bases, nunca de memoria). **Leccion de proceso (consolidada en `autorizacion-escritura-lab`, seccion del gate de ejecucion)**: con `skills.write_approval` encendido `skill_manage` NO escribe — deja el lote en `~/.hermes/pending/skills/<id>.json` y el directorio sigue vacio; «Aprobada» por chat no lo aplica y desde Telegram el usuario no puede lanzar el comando de aprobacion, asi que la via que funciono fue escribir los BYTES del payload aprobado con herramientas de fichero, con OK explicito previo. Backups PRE: GUIA `.bak-20261008-erandio` y `autorizacion-escritura-lab/SKILL.md.bak-20261008-erandio`. JL-013/RULE-005 aplicados en la misma sesion.

**v1.6.15 (07-oct-2026):** INSTRUMENTO DE VISIBILIDAD DEL FRASCO + GUARDIA DE IDIOMA DEL AGENTE + CRIBA DE COBERTURA DEL 07-OCT. Tres piezas medidas, sin umbral a priori (RULE-015). **(1) `tools/medir_visibilidad_frasco.py`** (260 lín. / 11.555 B, md5 `aa361fab65a96c5a5e2bd7f3ea67cb53`; commit `22162b8`, recibo `tree_sha 6233258ba6af990291948dfdd68b26b2bb5a85c9`): mide sobre el **PNG FINAL** (no sobre el HTML ni a ojo) la luminancia mediana del **tapon**, del **cuerpo** y del **fondo contiguo**, el **ratio de contraste WCAG** y el **% de claros** (L>225) dentro del rectangulo real del frasco. **Las 4 versiones de la ficha del 07-oct medidas con el mismo instrumento** (re-medido 13:54 CEST): v5 **4,0 %** claros / cuerpo **1,54:1** -> frasco INVISIBLE, PARAR; v6 63,2 % / 1,53:1; v7 63,0 % / 2,26:1; v8 63,0 % / 2,25:1 (**enviada**). **(2) `~/.hermes/scripts/guardia-idioma.py`** (330 lín. / 13.116 B, md5 `c1560aaacf13aa898a3923fd3bd3a7b2`; cron `7c3fe0c3fc71` cada 10 min, `no_agent`, silencioso): **mide** el idioma del PROPIO agente sobre `~/.hermes/state.db` (`role='assistant'`, cursor por `ultimo_id`), con 2 señales (script no latino sostenido - griego excluido - y prosa larga sin marcadores ES con muchos EN), recorte latino para no copiar el texto raro en el aviso, `no` fuera de las palabras españolas y hora fija Europe/Madrid. Precision medida sobre **57.910 mensajes**: **8 alertas, 0 falsos positivos**, todas del mismo modelo. **(3) Criba de cobertura del contexto (07-oct 13:45 CEST, `rc=0`)**: corpus **45.597 chunks** (baseline 45.552), utiles 45.565, del banco 32, hechos en corpus **24** (baseline 23), comparables 11 -> **VERDE 6 / AMBAR 3 / ROJO 0 / EXENTO 2 = VEREDICTO OK** (minimo 5 verdes, maximo 2 rojos: ninguno). El candidato a ROJO `multi-rendimiento-local` se midio **AMBAR** (cob@5 1/2, ratio 0,500; el hecho que falta es `deepseek`, que solo vive en esta GUIA y el instrumento por eso lo DESCARTA como banco): **la caja `FALLO_RECUPERACION` sigue con 0 casos** y el instrumento lo avisa. Backups: GUIA `.bak-20261007-visibilidad-guardia`. JL-013/RULE-005 aplicado en la misma sesion del cambio estructural.

**v1.6.14 (06-oct-2026):** EL ROJO `fallo-detalle-reel` ERA UN CASO MAL DISENADO, NO UN FALLO DE RECUPERACION - MATCHER ENDURECIDO + CASO CURADO + HECHO RE-DECLARADO. Revision medida del unico ROJO de la v1.6.13 (`fallo-detalle-reel`, ratio 0,000): sondas de SOLO LECTURA sobre el indice -> el documento del reel (`research/analisis-reel-rag-evals-gauravgoyalai.md`, 6 chunks de 210-978 chars) quedaba en **puesto 26** (`d=0.544`) con la consulta del caso, pero **puesto 1** (`d=0.266`, 6/6 hechos en el top-5) con el **TITULO LITERAL** del documento y **puesto 2** (`d=0.319`, 6/6) con una parafrasis en espanol. **Causa**: la consulta del caso (`rubrica de abstencion`) pedia algo que NO EXISTE en el corpus (0 chunks) y arrastraba el embedding a otro grupo; y sus 2 hechos eran **FALSOS** - `corpus_abstention` no aparece en ningun chunk (0) y `19 33` casaba con horas (`19:33:35`) y con `19.337` porque `_norm` convierte todo caracter no alfanumerico en espacio. **No era fallo del RAG, ni del corpus, ni del umbral.** **Cura aplicada (al instrumento; cortes y limites intactos)**: (1) **matcher endurecido** - un hecho que no contiene NINGUNA letra es INVALIDO (fail-closed) y todo match exige **frontera de digito** (un numero no casa dentro de otro mayor: `45552 chunks` ya no casa con `455522 chunks`; `33 chunks` no casa con `x133 chunks` ni con `133 chunks`), probado **11/11** en `check_matcher.py`; los hechos invalidos se **LISTAN** en el detalle y en el JSON (`hechos_invalidos`) en vez de inflar el techo en silencio; (2) el caso se **renombra y recura** `fallo-detalle-reel` -> **`cub-detalle-reel`** (consulta "como evaluar pipelines RAG con LLMs evals de retrieval y contexto", hechos reales `groundedness` y `retrieval quality` - sostenidos por `research/analisis-reel-rag-evals-gauravgoyalai.md` y `04-operations/backlogs/2026-07-31-backlog.md` - y esperada declarada **CUBIERTO**): medido **CUBIERTO 3/3 (VERDE)**; (3) el hecho de `abst-dato-vivo` se re-declara **VALOR+ETIQUETA** (`45552 chunks`), ya no numero desnudo. **Medido con el instrumento curado** (`rc=0`, `set_sha256 4c14cd6d269fef8b`, **3 pasadas identicas**): corpus **45.591 chunks** | utiles **45.565** | del banco **26**; hechos en corpus **24**; `cobertura@5` **0,70 (21/30)** y **0,88 (21/24)** sobre corpus util; **VERDE 6 - AMBAR 3 - ROJO 0 - EXENTO 2**; comparables **11** (`abst-dato-vivo` y `cub-detalle-reel` NO comparables por techo movido); dirigidos **8 -> 7**; **VEREDICTO OK**, y por primera vez **ROJOS 0** con la caja `FALLO_RECUPERACION` VACIA (el instrumento lo AVISA: cajas SIN NINGUN caso). **Instrumento**: 613 lin. / 31.512 B, md5 `3384dbd86333d2b6ff454ff0fcba3678`; backup PRE-cambio `.bak-20261006-caso-reel`. Unico desvio dirigido: `multi-rendimiento-local` (esperaba CUBIERTO -> DESVIO: falta `deepseek`) - candidato a hueco REAL de recuperacion.

**v1.6.13 (06-oct-2026):** CURA DEL INSTRUMENTO DE COBERTURA — LA DOCUMENTACION DEL BANCO DEJA DE CONTAR COMO CORPUS (TECHO FANTASMA ELIMINADO). Los 2 «huecos de recuperacion» de la v1.6.12 (`abst-dato-vivo`, `fallo-dato-bd-perfume`) **no eran un fallo del corpus**: eran **cobertura fantasma**. Barrido medido del indice (45.578 chunks, `path`+`text`): los hechos que el probe daba por «en corpus» solo existian en `GUIA-JOKO-LAB.md` (`45552`) y en el asiento de `04-operations/backlogs/pendientes.md` (`turathi` 2+1, `4 sprays` 2+1) — es decir, en la **documentacion del propio banco de pruebas que dice que el dato NO esta** (el probe lo leia como «si esta»); el `.py` del instrumento NO esta indexado. **Cura del INSTRUMENTO, no del umbral**: `tools/evaluar_cobertura_contexto.py` incorpora el filtro `BANCO_HABLA` — un chunk que HABLA del banco (marca `[BANCO]`, `cobertura@`, `evaluar_cobertura_contexto`, `huecos medidos`, `hechos en corpus`, ids de caso) se excluye del **techo** y del **top-k**, y el **techo bruto** se sigue imprimiendo para que la contaminacion no se esconda. **Defecto propio detectado y corregido en la misma sesion**: la 1ª version del patron incluia `top-5` y `banco de pruebas` y marcaba documentos LEGITIMOS — medido con `cura_calibra.py`: `top-5` en 9 ficheros / 5 legitimos (`research/experimento-hyde-20260831.md`, `research/analisis-mcps-mas-usados-2026.md`, `research/analisis-shivabytes-vectorless-rag.md`, `GUIA-APRENDIZAJE-JOKO-LAB.md`, `backlogs/bak-20260902-shivabytes-vectorless.md`) y `banco de pruebas` en 4 / 2 legitimos → **descartados**; leccion medida (RULE-015): un filtro de vocabulario se calibra **midiendo los paths que toca**, no solo el caso objetivo. **Medido con el instrumento curado** (`rc=0`, `set_sha256 a9ae27b05e3c0b1a`): `abst-dato-vivo` techo **0** (bruto 1) → **EXENTO**; `fallo-dato-bd-perfume` techo **0** (bruto 2) → **EXENTO**; los dos **dirigido OK** (`ABSTENCION_CORRECTA`, la caja declarada de antemano) → **dejan de ser huecos**. Reparto: **VERDE 6 · AMBAR 3 · ROJO 1** (`fallo-detalle-reel`) **· EXENTO 2**; comparables 12; NO comparable `abst-dato-vivo` (su techo de baseline 1 era fantasma) — exclusion **explicada**, ya no «el indice se movio»; corpus **45.583 chunks** | utiles **45.563** | del banco **20**; hechos en corpus **22** (baseline 23, tambien contaminado); `cobertura@5` **0,62 (18/29)** y **0,82 (18/22)** sobre corpus util. **Cortes y limites globales INTACTOS** (1,00 / 0,50 y 5 VERDE / 2 ROJO): **VEREDICTO OK**. Instrumento: 553 lín. / 27836 B, md5 `e2a52798d45767ead65d80f1e511e1a5`. Backups PRE: `.bak-20261006-cura` y `.bak-20261006-cura2` (instrumento).
**v1.6.12 (06-oct-2026):** CRIBA DE LA COBERTURA DEL CONTEXTO FIJADA SOBRE EL DATO (RULE-015) + 2 HUECOS DE RECUPERACION MEDIDOS. El instrumento `tools/evaluar_cobertura_contexto.py` (16.105 B / 353 lín. en `f5e3977` → **22460 B / 468 lín., md5 `bf24f509806c23c52cca2b4996e7e2ee`**; backups PRE-cambio `.bak-20261006-criba` y `.bak-20261006-criba2`) deja de ser solo medida: lleva fijada la criba **despues** de medir la distribucion real de los 13 casos. **La regla**: `ratio = cobertura@5 / techo` por caso → `VERDE` 1,00 · `AMBAR` 0,50-1,00 · `ROJO` < 0,50 · `EXENTO` (techo 0, sin hecho exigible: no hay ratio que juzgar); los cortes caen en los HUECOS de la distribucion del BASELINE (1,00 x5 --incl. `cub-recup-mixto` 2/2-- · 0,50 x4 · 0,00 x2, mas 2 casos de techo 0 = EXENTOS: ningun caso entre 0,50 y 1,00), no en un umbral a priori. **El juicio global** corre solamente sobre los casos **comparables** —aquellos cuyo TECHO no se ha movido desde el baseline— y exige **no bajar de 5 `VERDE` ni subir de 2 `ROJO`**; un caso con el techo movido es **NO COMPARABLE** y se EXCLUYE del veredicto en vez de contaminarlo. Esa regla no es teorica: al estrenar la v1 de la criba el indice se reindexo solo durante la prueba (**45.552 → 45.568 chunks**; hechos en corpus 23 → **26**) y 2 casos cambiaron de techo → la v1 dio un **FALLO falso**; de ahi la comparabilidad por techo. **Baseline**: pasada de 15:37:53 CEST del 06-oct (`set_sha256 de40e6bec98a2525`, 45.552 chunks, 23 hechos en corpus). **Veredicto: medido 2 veces seguidas el 06-Oct-2026** (mismo set `de40e6bec98a2525`, `rc=0`): **OK en las dos**. 23:04 CEST (45.568 chunks) → 11 comparables, `VERDE` 5 / `AMBAR` 4 / `ROJO` 1 / `EXENTO` 1. 23:13 CEST, con el indice movido otra vez (45.575) → 11 comparables, `VERDE` 6 / `AMBAR` 3 / `ROJO` 1 / `EXENTO` 1 (`exp-hel` paso de 1/2 a 2/2). Unico ROJO en ambas: `fallo-detalle-reel`; excluidos por techo movido: `abst-dato-vivo` y `fallo-dato-bd-perfume`. La leccion medida: **las cifras por caja oscilan con el reindexado diario; el veredicto se apoya solo en los comparables**. **Sigue sin haber criba sobre ratios AGREGADOS** (1 hecho = 1/26 = 3,8 % del denominador EN CORPUS hoy). **NO medido aqui**: si el modelo USA el contexto. **Huecos pendientes medidos** (asiento en `pendientes.md`): `fallo-dato-bd-perfume` (el contenido de la BD de perfumes —`turathi`, `4 sprays`— no llega al RAG) y `abst-dato-vivo` (un dato vivo numerico tampoco), los dos con los hechos YA en el corpus y 0/2 en el top-5 → fallo de RECUPERACION, no de techo.
**v1.6.11 (06-oct-2026):** INSTRUMENTO DE COBERTURA DEL CONTEXTO (RAG) - MEDIDO, SIN UMBRAL. Nace de una de las 3 entradas reales de `04-operations/metrics/aplicabilidad_ledger.jsonl` (dailydoseofds_, 19-sep: «`evaluar_rag.py` mide `recall@K` pero NO cobertura del contexto»). **`tools/evaluar_cobertura_contexto.py`** (16.105 B, md5 `5730448dc2846905d96a28fcd4cbefe6`; **respalda** a `evaluar_rag.py`, que NO se toca) mide, por consulta y **sin LLM**, si el hecho ESTA en el corpus y si LLEGA al contexto: `hechos` (variantes), techo real del corpus, `cobertura@k` / `@top1` / `@presupuesto` y 5 cajas (`CUBIERTO`, `PARCIAL`, `CUBIERTO_RECUPERABLE`, `FALLO_RECUPERACION`, `ABSTENCION_CORRECTA`), con **3 controles obligatorios en la misma pasada** (1 positivo + 3 negativos; si fallan, `rc=2`) y `set_sha256` del set medido. **NO fija umbral (RULE-015)**: mide, no juzga. **Primera pasada (15:16 CEST, 6 casos heredados)**: 4 CUBIERTO / 2 PARCIAL, **3 cajas sin estrenar** y el presupuesto de 6000 chars sin morder. **Set endurecido a 13 casos** (6 heredados + 7 dirigidos) con campo `esperada` (caja hipotesis declarada ANTES de medir, para poder falsarla) y contador `dirigidos_ok`: **8 dirigidos -> 5 cayeron donde se disenaron**. **Defecto propio detectado y corregido en la misma sesion**: con techo 0 de hechos en corpus, la rama `CUBIERTO_RECUPERABLE` (0 == 0) tapaba `ABSTENCION_CORRECTA` y ninguna abstencion era etiquetable -> ramas reordenadas. **Medicion final (15:37 CEST, 13 casos, `k=5`, `rc=0`, ~25 s)**: CUBIERTO 4 / PARCIAL 4 / CUBIERTO_RECUPERABLE 1 / FALLO_RECUPERACION 2 / ABSTENCION_CORRECTA 2 (**las 5 cajas estrenadas**); `cobertura@5` **0,57** (17/30) frente a un techo de corpus **0,74** (17/23) -> **7 de 30 hechos no estan en el indice**; `cobertura@top1` **0,37** (usar solo el primer chunk perderia 6 de 17 hechos recuperables); `cobertura@presupuesto(1200)` **0,43**. **Huecos medidos**: el contenido de la BD de perfumes (`turathi`, `4 sprays` ausentes) y el tamano del indice (`45552`) NO estan en el corpus; `langchain` y `deepseek` SI estan pero no llegan al top-5. Backup PRE-cambio del instrumento: `.bak-20261006` (12.179 B, md5 `752fb151efb3ecffa4027ac5e4a8e335`).

**v1.6.10 (04-oct-2026):** INYECCION DE CONTEXTO RAG — DIAGNOSTICO + HOOK `pre_llm_call` CABLEADO (INACTIVO POR DECISION DEL USUARIO). Pregunta de partida: ¿el contexto RAG entra en prefijo o sufijo? **Medido: SUFIJO** (entra como resultado de herramienta — MCP `buscar_rag` / `tools/search.py` — asi que no tira la cache de prefijo, pero el recall no es determinista porque depende de que el modelo decida llamar). **Uso real medido** (`~/.hermes/state.db` en `?mode=ro`): el RAG se consulta en **~1 % de las sesiones** con actividad (`tool_calls LIKE '%buscar_rag%'` o `%search.py%` frente a `message_count >= 5`) → el fallo de recall es real, no una impresion. **Causa raiz**: la inyeccion automatica estaba DESCONECTADA — `~/.hermes/skills/joko-context/SKILL.yaml` y `.../joko-search/SKILL.yaml` eran 2 ficheros en un formato que el Hermes actual NO carga (218 `SKILL.md` frente a 2 `SKILL.yaml` en el perfil; 0 coincidencias de `SKILL.yaml` en `hermes-agent`), `config.yaml` no tenia bloque `hooks:` y `tools/context_builder.py` no tenia consumidor que llegara a un prompt (solo informes/blackboard). **Remediado en lo tecnico**: hook `~/.hermes/agent-hooks/joko-context.py` (177 lin.) declarado en `config.yaml` como `hooks.pre_llm_call` con `hermes config set` (el guardian de Hermes bloquea editar el config a mano; ensayo previo en sandbox `HERMES_HOME=/tmp/hermes-sandbox`; backup `config.yaml.bak-20261004-joko-context`). Diseno por niveles: **Tier 1 siempre** (ultimos 4 eventos de `shared-events.jsonl`, ~70 ms) + **Tier 2 condicional cacheado por sesion** (TTL 600 s, tope 2.200 chars), porque el coste medido es query nueva **15,6 s** / cache **106 ms** / solo eventos **66 ms** — un hook ingenuo anadiria ~15 s a cada turno. **Pruebas**: 8/8 casos sinteticos por stdin (frio 17,0 s; cache 42 ms; cron, JSON invalido y kill switch → no-op). **Estado: NO allowlisted → NO dispara en runtime** (`hermes hooks doctor`: «hook will NOT fire at runtime»); la aprobacion (`hermes --accept-hooks hooks test pre_llm_call`) es la puerta de seguridad del usuario y hasta entonces el efecto en un turno real esta **NO verificado**. **Fosiles archivados** (AGENTS.md §2 «no se borra: se archiva»): `joko-context/SKILL.yaml` → `.archive/joko-context-fosil-20261004/SKILL.yaml` y `joko-search/SKILL.yaml` → `.archive/joko-search-20261004/SKILL.yaml`; la skill **`joko-context` portada a `SKILL.md` v2.0.0** (operativa). Corregida ademas la fila del diagrama de la skill `local-rag` (decia «inyecta RAG al LLM») y archivado el borrador suelto `~/.hermes/skills/joko-lab-skill.md` (10-jul, sin frontmatter y con la instruccion «ejecuta comandos … no pidas permiso») en `.archive/joko-lab-skill-md-20261004/`. Detalle y mediciones: skill `local-rag` → `references/inyeccion-contexto-en-hermes.md`. **RULE-005**: esta entrada.

**v1.6.9 (30-sep-2026):** TRASLADO DEL MATERIAL DE LA SESION AL LAB — FORENSE DEL CURADOR COMO TOOL + SCRIPT GENERICO DE COMMIT CON RECIBO + PAQUETE DE EVIDENCIA. El material de la sesion vivia en `/tmp/ig-4posts` (64 ficheros / 512 K, volatil). Se traslada lo que tiene valor durable. **`tools/auditar_curador_skills.py`** (245 lín. / 9.658 B, solo lectura): antes **no existia ninguna utilidad del curador en `tools/`** (medido: 0 coincidencias de `curator|curador|forense` en el directorio); resume el ledger por actor/skill/sesion, inventaria los volcados intermedios y mide el estado en disco de lo tocado (`--horas`, `--desde`, `--skill`, `--diff`, `--salida`). **`03-automation/scripts/commit-con-recibo.sh`** (123 lín. / 4.633 B): commit con recibo generico — dry-run por defecto, staging de una sola ruta, verificacion blob/tree y `--push` explicito. **`research/curator-skills-20260930/`**: `INDEX.md` + `MANIFEST.txt` + **27 ficheros / 238.114 B** (17 de medida cruda + 10 scripts de la sesion), verificados byte a byte contra el origen (`cmp`, ademas de tamano+md5 en la copia). **Lo que NO se copio y por que**: logs de dry-run/apply (el lab no los versiona), 5 duplicados exactos por md5, volcados de recon superados por `medir_ko.txt`/`counts.txt` y el borrador del OBS (identico al backup pre-addendum ya versionado). **Hallazgo medido**: el curador **generalizo** los scripts de la sesion como plantillas de skill (`templates/edicion-anclas.py`, 5.475 B / 135 lín., diff de 247 lín. contra `fix_rule018_figs.py`) → por eso el traslado **no duplica los patrones**: `references/edicion-correctiva-y-cifras.md` ya contiene la leccion de las cifras rectificadas con instrumento, incluidos los dos numeros mal medidos de esta sesion (skills de la lista de supresion y blobs del curador). Backups: GUIA `.bak-20260930-keeper`. JL-013/RULE-005 aplicado en la misma sesion del cambio estructural.
**v1.6.8 (30-sep-2026):** FLUJO DIARIO DEL PERFUME HECHO IDEMPOTENTE + PLANTILLA V5 ALINEADA AL CANON + PURGA DEL ONE-SHOT. **Paso 0B — CHECKPOINT en la skill `perfume-del-dia`** (`SKILL.md` 229 → 239 líneas, backup `.bak-20260930-checkpoint`): antes de generar nada, el flujo consulta `uso_diario` del día en `perfume-ia/data/coleccion.db` y PARA si ya hay fila para hoy. Causa real medida el 30-sep: el defecto no era el cron, sino que el flujo no comprobaba si la ficha del día ya existía — el recurrente de las 07:05 había corrido y un catch-up manual lanzado a las 07:57 volvía a arrancar el pipeline completo (riesgo de ficha duplicada y de fila duplicada en `uso_diario`). **Plantilla `templates/plantilla-ficha-v5.html` alineada**: iba un escalón por detrás del canon aceptado y con sus valores desbordaba ~42 px (medido 1358 reales frente al límite 1350); md5 `92847ac7c488b19bfcfd811bfd12c70b` → `e70fb8b4ff1395ee9ce182d817e96209`, el diff son exactamente 5 líneas (padding 12/10 → 8/8, sello 80 → 74, hero 4/8 → 2/6, reflejo −8/34 → −6/24, `.sec` 6 → 3), backup `.bak-20260930-canon`. **One-shot `187aa5513d56` (`ficha-perfume-30sep-catchup`)**: cerró por sí solo en `state=completed`, `enabled=False`, `next_run_at=None` (repetición 1/1 consumida) y se ha **eliminado del store** (47 → 46 jobs); su definición queda copiada en `~/.hermes/skills/joko-lab/perfume-del-dia/backups/job-187aa5513d56-ficha-perfume-30sep-catchup.json`. **Lección de cron medida**: un one-shot con la hora ya pasada es frágil (gracia `ONESHOT_GRACE_SECONDS=120`) y `cronjob_manage pause` no admite jobs de terminal ("Cannot activate terminal cron job ... use cron resume --run-now or --at"); lo robusto es el recurrente con catch-up. **Contraste de la ficha entregada** (`tools/medir_contraste_ficha.py` + `tools/inventario_legibilidad.py`, doble render): 63 nodos medidos, **35 por debajo de 4,5:1**, **22 por debajo de 3,0:1**, peor 1,01:1 en `r-num` (el rating) — en línea con la ficha aceptada del 26-sep (31/62 y 22/62); el criterio V0 lo fija el usuario y no se reabre. **Cifra corregida**: hay **18 RULEs activas** en `01-knowledge/objects/` (la cronología de esta GUIA seguía citando 16); medido con `ls -1 01-knowledge/objects/RULE-*.yaml | wc -l`. Backups: GUIA `.bak-20260930-checkpoint`. JL-013/RULE-005 aplicado en la misma sesión del cambio estructural.
**v1.6.7 (29-sep-2026):** EL GATE DEL RECIBO ENTRA EN LA GUIA + LOS DOS REPOS DOCUMENTADOS. **Gate (RULE-006)**: los hooks del recibo ya existian en `hermes-lab` (el log del gate arranca el 03-ago-2026), pero **no estaban versionados en `joko-lab`**; se han añadido a git (2 ficheros, md5 identico al de hermes-lab: pre-commit `df169c48`, generar_recibo `63670ea0`) y `core.hooksPath=hooks` esta activo en los dos, asi que un clon ya no se queda sin gate. **RULE-006 revalidada (29-sep)**: alcance ampliado a los dos repos git del lab (los hooks de joko-lab eran identicos, sha256 verificado) y confianza 0.7 -> 0.8 (ALTA). El gate lleva actuando desde el 04-ago: su log `~/.hermes/logs/joko-rdd.log`, medido el 29-sep con `wc -l` y `grep -c`, tiene **56 asientos = 36 `OK recibo_valido` + 12 `BLOQUEADO` + 8 `BYPASS`**. **`AGENTS.md` en los dos repos**: el de `joko-lab` (enrutador de RULEs, prohibiciones, ciclo obligatorio y mapa) y el contrato de `hermes-lab` refrescado — es lo que leen los agentes que trabajan dentro (Hermes, opencode). **`hermes-lab/docs/estado-real.md` refrescado contra medida real**: kernel `7.0.0-34-generic`, Python 3.11.16, Docker 29.8.1 + Compose v5.5.1, 34 entradas en `docs/decisiones` (32 `.md`), 32 ficheros en `scripts/` (13 `.sh`) y 3 `test_*.py` en `tests/` — todos medidos el 29-sep; mas la seccion «lo que NO se ha medido»; las cifras que caducan al commitear se citan **por su orden de medicion**, no por su valor. **joko-lab al dia**: 92 entradas de `git status` (= 238 ficheros reales) commiteadas en 5 commits tematicos, cada uno con su recibo, hasta `97104c2` y empujadas al bare local; queda fuera a proposito el unico `.parcial` incompleto. **Ultimas reglas**: van por RULE-018 (20-sep) — la linea de esta GUIA que decia RULE-008/009 era de agosto y se ha corregido.
**v1.6.6 (04-sep-2026):** MAPA DEL CONOCIMIENTO COMO TOOL + DELEGACIÓN gpt-oss-20b VALIDADA + CIFRAS REALES ACTUALIZADAS. **Herramienta reusable**: tools/mapa_conocimiento.py (305 lín.) + .sh — mapa 2D del conocimiento del lab 100% local, 0 LLM (LanceDB 42.931 → filtro conocimiento real → PCA(50d)→TSNE(2d)→KMeans→etiquetas TF → HTML autónomo ~610 KB; default K=18; args --out/--k). **Delegación validada (04-sep)**: delegation.model = gpt-oss-20b (MXFP4, 6/6 tareas reales OK; r1-14b/llama31 NO aptos) — LM Studio localhost:1234. **Catálogo LM Studio por API**: 11 modelos (8 LLM/VLM + bge-m3 + nomic + gpt-oss-20b nuevo). **Cifras reales**: RAG LanceDB 42.931 filas (no 15.200 de 05-ago); 185 skills reales (no 119); 40 crons registrados (38 activos + 2 one-shot completados); 39 KOs yaml (16 RULEs + 23 objetos); 16 RULEs activas (RULE-015 instrumentos 02-sep + RULE-016 actualizaciones Hermes 03-sep). **n8n (zona protegida, solo lectura)**: 13 workflows en export de 04-sep 14:16 (incluye ENVIO WHATSAPP active=True, original viOMJPiqszOrDhGO sin bifurcación); la bifurcación OCR vive en v2 de prueba NQXgQ8nRv9JlJUaG (active=False, creado después del export — por eso el total llega a 14 con export fresco) — validación final pendiente de token WhatsApp renovado (401/code 190). **Video Base44 (04-sep) analizado → valor BAJO** (SaaS vibe-coding Wix; duplica n8n+RAG; metodología transferible anotada). Backups GUIA .bak-20260904. JL-013 aplicado en la misma sesión del cambio estructural.
**v1.6.5 (03-sep-2026):** INCIDENTE state.db CORRUPCIÓN v0.21.0 (02-03 sep) + CAUSA RAÍZ UPSTREAM + RULE-016. Corrupción de ~/.hermes/state.db (1.3 GB, 124k msgs): primer malformed 02-sep 22:31 (cron Bolsa), `file is not a database` 22:57 (gateway). Reparación verificada 03-sep 10:16 (FK vacío, quick_check ok, 7 sesiones huérfanas reinsertadas desde JSONL sesiones-20260902, 551 sesiones; verif end-to-end OK). **Causa raíz NO local**: clase de corrupción multi-writer WAL conocida y ABIERTA upstream — issue #100313 (entorno casi idéntico: v0.21.0, kernel 7.0.0-30, gateway+CLI+cron), mecanismo confirmado por mantenedores: probe `_read_sqlite_application_id` (commit 71256df, 2026-08-18) cancela locks POSIX propios en cada escritura; fix PR #100519 (os.pread) mergeado 01-sep 17:51 UTC, DESPUÉS de nuestra release (HEAD 5a8e8a6b 09:32 UTC) → **v0.21.0 publicada NO incluye el fix; 0.21.1 no existe**. DECISIONES: (D1) esperar v0.21.1 con criterio de salida (no saltar a main); (D2) mitigación puente `database.journal_mode: delete` en config.yaml (aplicada, backup .bak-20260903-journaldelete; journal real pasa a delete en próximo reinicio del gateway); (D3) **RULE-016: al publicarse nueva versión de Hermes, investigar incidencias 5 días ANTES de actualizar en el lab**. Check check-state-db.sh mejorado (filtro payload message_sanitization + baseline ActiveEnterTimestamp gateway → OK post-reparación inmediato). Doc: hermes-lab/docs/decisiones/2026-09-03-corrupcion-state-db-v021.md + skill recuperacion-state-db. 15→16 RULEs activas.
**v1.6.4 (18-ago-2026):** GRAPH DE DELEGACIÓN MULTI-AGENTE — frontera de maduración del lab (fase LOOP GOVERNS → GRAPH COORDINATES, validada externamente por codewithbrij/mentalhotfix/hackproduct el mismo día). **PRD**: research/prd-graph-delegacion-multiagente.md — graph de 4 nodos (Coordinador→Investigador→Redactor→Revisor) con contratos de edges, política de modelos por nodo y métricas. **Piloto F1 COMPLETADO** (research/piloto-f1-graph-post-rag.md): investigador llama31-8b con prompt JSON cerrado SÍ ejecutó (9 búsquedas, 5 api_calls, 8 claims verificados 8/8) · revisor delegado = ZOMBIE (api_calls=1, plan en vez de informe) → **revisión crítica SIEMPRE en sesión**. Se detectó y corrigió 1 error factual sin fuente ("CRAG se monta ENCIMA de Self-RAG"). **Skill graph-lab v1.0.0** creada (flujo reutilizable + plantilla de prompts + pitfalls). Auditoría checklist agentes: **7/8 cumplidas** (research/auditoria-checklist-agentes-codewithbrij.md) — la 8 (edges con contrato) es el graph, ahora cubierta. **Decisión F4 (con datos del piloto): NO pinear config global a cloud** — investigador local ✅ con prompt cerrado + revisión en sesión; el cloud solo si el volumen de revisión delegada lo justifica. Backlog 534 líneas, backups 18o→18u + GUIA bak-20260818-graph.
**v1.6.3 (17-ago-2026):** PRIMER MCP DEL LAB — **Manim MCP (animation-server) IMPLEMENTADO** (PoC completa verificada 08:13). Stack: venv dedicado `~/manim-mcp/venv` (manim 0.21.0 + fastmcp 1.0 + mcp 1.29; pre-requisito sistema pangocairo 1.57/cairo 1.18 instalado con sudo autorizado) · servidor corregido `~/manim-mcp/server/animation_mcp.py` · registrado en Hermes `hermes mcp add animation-server --command ~/manim-mcp/venv/bin/python3 --args ~/manim-mcp/server/animation_mcp.py` (config.yaml, 2/2 tools) · MANIM_EXECUTABLE → binario del venv. **3 bugs del repo original corregidos** (ruta media/media → temp/media/videos con glob; flag `-p` abre reproductor → `-ql` headless; búsqueda del .mp4). Verificación real vía protocolo MCP: INIT ✓ → tools/list ✓ → tools/call renderizó Demo.mp4. **Pendientes**: tools MCP visibles en sesión NUEVA (/new); producción con `-qm`/`-qh`; LaTeX (texlive) para MathTex; fastmcp 1.0 con 14 avisos OSV (monitorizar). Futurible Manim MCP → estado IMPLEMENTADO. Research: analisis-mcp-presentaciones-animaciones.md. Backlog 470 líneas, backups ag/ah/ai + GUIA bak-20260817-mcp.
**v1.6.2 (16-ago-2026):** SKILL LEAST-PRIVILEGE-LAB (política de mínimo privilegio, v1.0.0) — tras investigación "AI agents = superficie de ataque" (IBM short C6aZx47q7Zc + Marchward/CISO playbook). **5 reglas**: R1 delegate_task SIEMPRE con toolsets mínimos (código→terminal+file; investigación→web; vídeo→terminal+file; NUNCA todo junto); R2 cron NUEVO con agente → enabled_toolsets obligatorio; R3 cron no_agent (script puro) no requiere toolsets; R4 credenciales redact_secrets + [REDACTED]; R5 MCP futuro → evaluar inherit_mcp_toolsets=false. **Corrección honesta del análisis**: el gap "24/30 crons sin toolsets" era FALSO — los 24 son no_agent=True (scripts puros sin LLM/tools); los 5 jobs con agente TODOS tienen toolsets ✅. Research: analisis-least-privilege-agentes-lab.md [ALCANCE INTERNO]. **Primera delegación con least-privilege probada en vivo**: delegate_task con toolsets=['web'] (investigación sala de subastas WhatsApp, deleg_f631cd85) — validación de R1. Backlog 445 líneas, backups w/x, GUIA backups cierre/cierre2.
**v1.6.1 (16-ago-2026):** RULE-010 — botón de paso de control entre sesiones: `~/.hermes/scripts/ceder-control.sh <cli|telegram> [mensaje]` (handoff activo CLI↔Telegram: claim en domain-bus + handoff en lab.md + push real al móvil si destino=telegram; semipasivo si destino=cli — la CLI lee el file bus en su prompt del canal). Creado a petición de Joseba. Backlog 442 líneas, backup u.
**v1.6.0 (16-ago-2026):** GATE DE VERACIDAD COMPLETO (5 fases, objetivo "100% veraz y contrastable"): tools/verificador_alucinaciones.py (detección 4 tipos de alucinación: sentence/prompt/factual/randomness + etiquetas [VERIFICADO]/[ALCANCE INTERNO]/[NO VERIFICADO]/[REVISAR]; exit 1 bloqueante), tools/contrastar_externo.py (gate externo: sin fuente → BUSCAR:keywords → agente busca → fuente → [VERIFICADO]), tools/verificar_research.py (post-procesador de research/: inserta **VERACIDAD:** en los 154 análisis; backfill completo 107 VERIFICADO + 47 ALCANCE INTERNO + 0 REVISAR), integrado en informe-diario-local.sh (# Gate de veracidad: [ETIQUETA]); suite 233 OK (205+25+3); skill gate-veracidad obligatoria para outputs factuales. RULE-009 (16-ago): protocolo de lock para el backlog — tools/lock-backlog.sh (acquire/release/status/force-release) resuelve colisiones de sesiones paralelas (CLI vs TG) en 04-operations/backlogs (joko-lab NO es repo git → no aplica worktree; find_hermes_pid sube por PPIDs al gateway). 3 skills nuevas: gate-veracidad, revisar-decisiones (revisar DECISIONES de cambios grandes, no el diff — patrón David Ondrej), recursos-gratuitos-desempleados (12 recursos verificados, inventario references/recursos-recopilados.md). Guardrails verificados en producción (2 bloqueos en vivo: hardline blocklist de Hermes — mkfs/rm -rf / ni con --yolo; approvals smart fail-closed; cron_mode deny). Veting de skills de terceros (F4, ~110 skills): LIMPIO en 7 vectores. Backlog 440 líneas, backups .bak-20260816 a-t.
**v1.5.0 (14-ago-2026):** EXP-HEL-001 fase 2 instrumento IMPLEMENTADO (C1+C2+C3, OK usuario): activacion_declarada deja de escribirse (null, leccion KVC-001); metrica primaria = activacion_verificada; filtro ruido con golden set del corte (38 entradas, 0 capturas; es_ruido re.IGNORECASE; 'perfume' generico descartado por romper 2 genuinas); tools/verificar_hel.py creado (verificacion automatica primera respuesta ±180s, validado contra el verifier manual del corte). Diseño: research/exp-hel-001-fase2-instrumento-diseno.md (estado implementado). Futuribles en freeze hasta resultados fase 2: ToT/GoT/scratchpad/Strategy Controller/self-consistency/ReAct (backlog 2026-08-14). Corte fase 1: 04-operations/reports/2026-08-14-exp-hel-001-corte.md.
**v1.4.2 (11-ago-2026):** 0 funciones complejas de nuevo (462 totales): local_cloud_orchestrator.verifier 12→6 (helpers _verificar_json/_verificar_batch) + registrar_hel_diario._escanear_sesion 12→3 y _mensajes_usuario 11→4 (_mensaje_valido). OPs 003-004. Router con carga bajo demanda + swap automático (llm-router.sh: lms load si falta, swap si VRAM ocupada; fix _model_cargado con state:loaded). LanceDB compactado 13GB→311MB (259 versiones→2). Suite 205 OK.
**v1.4.1 (11-ago-2026):** refactor de las 2 últimas amarillas → **0 funciones complejas** (458 totales): registrar_hel_diario.main 19→6 (helpers _parsear_fecha, _escanear_sesion) y watchdog_salud_sistema.main 15→7 (5 helpers _check_uptime/_check_swap/_check_ram/_check_zombies/_check_swap_procesos); backups .bak-20260811; suite 205 OK; OPs 001-002. Watchdog salud sistema creado (cron 4h no_agent, alerta solo si problema). Reinicio manual del PC (swap 94%→0, residuos 46h limpiados).
**v1.4.0 (10-ago-2026):** router local/cloud por tipo de tarea (tools/llm-router.sh: batch/batch-json → R1-14B local, vision → GLM local; informe-diario movido a R1 local, primer informe 100% local 10-ago 09:00, 0 cloud); 3 recordatorios LLM convertidos a no_agent scripts fijos (investigacion/sueno/pendientes); crons 24 → 25 reales (+registrar-hel-diario EXP-HEL 22:35, +hel-registro-watchdog 22:45; cap 4.6); servicio systemd hermes-pipeline-proxy documentado (cap 2.3); Qwen 35B A3B probado y DESCARTADO (2.7-9 tok/s, CPU debil para MoE; R1-14B sigue de referencia); tanda de refactors: 61 refactors (v1.3.34-81), 0 funciones >20, 1 amarilla restante (registrar_hel_diario.main 19, instrumento del baseline EXP-HEL — refactor post-corte 14-ago); suite 205+ tests.
**v1.3.33+ (08-09-ago):** 61 refactors de la tanda (v1.3.34-81) — 0 funciones muy complejas, 1 amarilla restante. Detalle en la cabecera v1.4.0 y en la skill refactor-seguro.
**v1.1.0:** patron OKF (indice KOs + completitud_parcial + fix vigencia), 10 KOs, RULE-005, Activation Engine arreglado (lee objects/)
**v1.2.0 (06-ago-2026):** revision estructural completa — 21 crons reales (cap 4.6), 119 skills (cap 4.2), tabla 3.6 sin modelos retirados (llama-3.1-8b/qwen3-14b/gemma-4-e4b fuera del catalogo), servicios systemd corregidos (sin lmstudio-llmster; + hermes-gateway), checkpoint solo en hermes-lab, tipos KO + PATTERN/DEC-004, glosario OKF corregido (implementado), Perfume IA sin cifra de perfumes (coleccion amplia indeterminado), integracion Gemini API documentada (cap 4).
**v1.3.0 (07-ago-2026):** EXP-HEL-001 (capa cognitiva: activacion del razonamiento, via C en curso, corte 14-ago) + H-HEL-001 en HYPOTHESIS.md; Mission Contract (research/mission-contract-diseno.md + lpa/contracts/mission.schema.json, PROPUESTA) como capa de ejecucion; telemetria reformulada (activaciones por canal: active_rules/model_selection/blocks; RAG = universo de consultas, no recuperabilidad; dedupe por path en search.py); RULE-005..008 declaradas canal no_engine (supervision PIL, no task_type); 23 crons reales (22 activos + 1 pausado, cap 4.6).
**v1.3.1 (07-ago-2026):** revalidacion KEL operativa — watchdog diario 22:12 (tools/revalidar_kos.py, solo lectura) que avisa de KOs activos vencidos o proximos a next_review/expires; silencioso si todo en orden. 24 crons reales (23 activos + 1 pausado, cap 4.6).
**v1.3.2 (07-ago-2026):** integridad referencial FK — tools/verificar_fk_kos.py (detector solo lectura de la clase referencia_ko_no_verificada) + ficha EVF research/fk-integridad-referencial-evf.md (baseline: 1 mencion historica en KOs, 25 en docs con 3-4 candidatas a rotas reales). El gate SVP/KVC NO se modifica hasta la EXP.
**v1.3.3 (07-ago-2026):** agentic RAG loop Fase 1-4 (tools/agentic_loop.py + medir_agentic.py + skill agentic-rag; medicion 07-ago: clasico 5/7 vs agentic 6/7, +14% tiempo, mejora solo en consultas con señal de conflicto/vigencia). Fase 0 (activacion en produccion) PENDIENTE de aprobacion del usuario. Limitacion conocida anotada: evaluador con prohibidos da falso negativo.
**v1.3.4 (07-ago-2026):** EXP-FK-001 EJECUTADA — el detector de integridad referencial (tools/verificar_fk_kos.py) confirma DY positivo (4 rotas reales detectadas y resueltas; 25 menciones clasificadas). Adopcion del gate (extender SVP/KVC con FK) pendiente de decision; el gate no cambia.
**v1.3.5 (07-ago-2026):** gate FK ADOPTADO — el SVP incluye la comprobacion de integridad referencial (estructurados y wikilinks bloquean; prosa avisa; tools/verificar_fk_kos.py --gate, exit 1 si bloqueantes). Verificado: 0 bloqueantes en corpus.
**v1.3.6 (07-ago-2026):** saneamiento de seguridad — el valor de GOOGLE_API_KEY se retira de la guia (placeholder <ENV>); la key vive solo en ~/.hermes/.env. Revisado PRED-001/002: completos y vigilados (falso pendiente retirado).
**v1.3.7 (07-ago-2026):** OpenCode 1.18.15 instalado como worker de codigo gobernado (npm prefix ~/.npm-global, auth DeepSeek). Piloto OK: refactor de observer.py (extraccion calcular_metricas_activaciones) con salida de telemetria IDENTICA y registro PIL. OpenCode nunca escribe directamente: propone diff -> VERIFIER -> SVP-diff -> backup -> merge.
**v1.3.8 (07-ago-2026):** red de seguridad — tests/test_knowledge_health.py (unittest estandar, 22 tests OK) cubriendo las funciones puras de knowledge_health.py (parse_frontmatter, classify_file, extract_date, find_knowledge_files). Previa al refactor de audit() (52 de complejidad). Ejecutar: python3 -m unittest tests/test_knowledge_health.py.
**v1.3.9 (07-ago-2026):** refactor de audit() con OpenCode — extraidas _procesar_ko, _detectar_contradicciones y _calcular_health; complejidad de audit() de 52 a 9. Red de seguridad completa: salida JSON identica + 34 tests OK (python3 -m unittest discover -s tests). Conocido: claves de stats con tilde (sin_expiracion) heredadas sin tocar; OpenCode pierde comentarios al refactorizar (revisar en SVP-diff).
**v1.3.10 (07-ago-2026):** refactor de audit_structure() con OpenCode — extraida _chequear_estructura_md(txt) (funcion pura: flags frontmatter/H1-H3/enlaces); complejidad de audit_structure de 17 a 14. Red: JSON identico + 39 tests OK. Backups: knowledge_health.py.bak-20260807{b}, GUIA.bak-20260807k.
**v1.3.11 (07-ago-2026):** refactor de verificar_fk_kos.escanear_ko() con OpenCode — extraidas _escanear_estructurados y _revisar_texto (a nivel de modulo); complejidad de escanear_ko de 26 a 13. Red: JSON del detector identico + suite completa 47 tests OK (tests/test_verificar_fk.py nuevo). Backup verificar_fk_kos.py.bak-20260807b.
**v1.3.12 (07-ago-2026):** refactor de migrate_to_ko.migrate_dec() con OpenCode — extraidas _inferir_tipo y _inferir_confianza; complejidad de migrate_dec de 30 a 19. Red: dry-run identico (sin --apply) + suite completa 61 tests OK (tests/test_migrate_to_ko.py nuevo). Backup migrate_to_ko.py.bak-20260807.
**v1.3.13 (07-ago-2026):** refactor de context_builder_estructurado.extraer_resumen_estructurado() con OpenCode — extraidas _resumen_markdown y _resumen_yaml; complejidad de 30 a 4 (zona verde). Red: salida identica sobre 5 rutas reales + suite completa 70 tests OK. Leccion: la red cazo 2 falsos positivos de los tests propios (no bugs del codigo) — el split por " | " cuenta separadores internos de campos agrupados y "::: no es yaml [" no lanza en PyYAML. Backups: context_builder_estructurado.py.bak-20260807, GUIA.bak-20260807o.
**v1.3.14 (07-ago-2026):** refactor de knowledge_resolver.format_synthesis() con OpenCode — extraidas _limpiar_texto_item, _calcular_confianza, _detectar_boundaries y _seccion_fuentes; complejidad de 23 a 17. Red: salida identica sobre Synthesis de ejemplo + suite completa 80 tests OK (tests/test_knowledge_resolver.py nuevo). Leccion: _seccion_fuentes devuelve una linea por fuente (test inicial asumia todas en la primera). Backups: knowledge_resolver.py.bak-20260807, GUIA.bak-20260807p.
**v1.3.15 (07-ago-2026):** refactor de activation_engine.activate() con OpenCode — extraidas _match_rule (incluye el caso del bug condicion:null del 04-ago), _es_block, _es_modelo, _mejor_modelo, _aplicar_politicas y _trace_modelo; complejidad de activate de 22 a 9 (zona verde). Red: salida identica para 5 casos con _log_activation neutralizado + suite completa 91 tests OK (tests/test_activation_engine.py nuevo). Backups: activation_engine.py.bak-20260807, GUIA.bak-20260807q.
**v1.3.16 (07-ago-2026):** refactor de indexer.load_notes_con_hash() con OpenCode — extraidas _excluir_directorio, _parsear_archivo y _construir_documentos; complejidad de 22 a 10. Red: hashes anclados identicos (los conteos totales son inestables por el vault vivo: otra sesion escribe .md; dos ejecuciones consecutivas estables) + suite 100 OK con el venv del RAG (tests/test_indexer.py nuevo; requiere ~/.venv/hermes-rag/bin/python3). Backups: indexer.py.bak-20260807, GUIA.bak-20260807r.
**v1.3.17 (07-ago-2026):** refactor de indexer.build_index() con OpenCode — extraidas _clasificar_cambios, _cargar_modelo (fallback OOM) y _recrear_indices; complejidad de 21 a 15. Red: dry-run identico + suite 105 OK con venv. CON ESTA, LAS 9 FUNCIONES MUY COMPLEJAS DEL INFORME DEL 07-ago QUEDAN REFACTORIZADAS (todas <=19; 6 en zona verde). Suite total: 105 tests (95 estandar + 10 venv). Backups: indexer.py.bak-20260807b, GUIA.bak-20260807s.
**v1.3.18 (07-ago-2026):** Mission Contract cerrado — RULE-010 ADOPTADA como KO activo (activar el Mission Runner solo si la mision lo REQUIERE: propiedades, no numero de fases; motor por mision: n8n para workflows existentes, Python para lo que n8n no cubre). KOs: 20 -> 21. Indice OKF regenerado. OP-20260807-030.
**v1.3.19 (07-ago-2026):** cortes de datos preparados — cron EXP-HEL (14-ago 09:00, b9ffffa1ead8) reforzado con criterios no binarios y execution path; cron NUEVO corte telemetria Proposer OBSERVER (18-ago 09:00, one-shot, 173a0d36d7ee): resume telemetria 04-18 ago y evalua la activacion del Proposer. Crons: 25 totales. OP-20260807-031.
**v1.3.20 (07-ago-2026):** tarea 5 (tanda de zona amarilla) — 1er refactor: decision_engine.evaluate() con OpenCode, extraidas _procesar_reglas_engine y _procesar_regla_hardcodeada; evaluate 19 -> 11. Red: salida identica + 140 combinaciones 0 mismatches (verificacion propia de OpenCode) + suite 114 OK (14 skip venv). Quedan 43 funciones amarillas. Backup decision_engine.py.bak-20260807, GUIA.bak-20260807v.
**v1.3.21 (07-ago-2026):** tarea 5 (2o refactor): knowledge_resolver.extract_knowledge_items() con OpenCode — extraidas _fuente_para_buffer, _crear_item y _clasificar_y_anadir (elimina dispatch duplicado); 19 -> 6 (verde). Red: Synthesis identica + suite 120 OK. Quedan 42 amarillas. Backups: knowledge_resolver.py.bak-20260807b, GUIA.bak-20260807w.
**v1.3.22 (07-ago-2026):** tarea 5 (3er refactor): consolidador_sesiones.main() con OpenCode — extraidas _contar_sesiones y _construir_resumen; main 18 -> 5 (verde). Red: flujo identico en entorno aislado (mocks) + suite 124 OK. Quedan 41 amarillas. Backups: consolidador_sesiones.py.bak-20260807, GUIA.bak-20260807x.
**v1.3.23 (08-ago-2026):** tarea 5 (4o refactor): evaluator_optimizer.improve_prompt() con OpenCode — extraidas _build_critique, _run_optimization_loop y _apply_gate; improve_prompt 18 -> 6 (verde). Red: salida identica (3 casos con mocks, diff vacio) + verificacion propia de OpenCode (0 mismatches) + 13 tests nuevos (suite 137 OK). Quedan 42 amarillas. Backups: evaluator_optimizer.py.bak-20260808, GUIA.bak-20260808. Leccion RULE-008: el auth.json de opencode vive fuera del arbol (~/.local/share/opencode/) sin copia y se perdio entre 07 y 08-ago (5h colgado); credencial deepseek restaurada 08-ago.
**v1.3.24 (08-ago-2026):** tarea 5 (5o refactor): evaluator_optimizer.format_report() con OpenCode — extraidas _cabecera_informe, _seccion_historia y _seccion_gate (puras, list[str]); format_report 17 -> 2 (verde). Red: salida byte-identica (4 casos con unicode, diff vacio) + verificacion propia de OpenCode (0 mismatches) + 8 tests nuevos (suite 145 OK). Quedan 41 amarillas. Backups: evaluator_optimizer.py.bak-20260808b, GUIA.bak-20260808b.
**v1.3.25 (08-ago-2026):** tarea 5 (6o refactor): knowledge_health.classify_file() con OpenCode — extraida _clasificar_por_nombre (cascada de nombres/dir padre); classify_file 18 -> 2 (verde). Red: salida identica (30 casos, diff vacio) + verificacion propia de OpenCode (300 combinaciones, 0 mismatches) + suite 145 OK. Quedan 40 amarillas. Backups: knowledge_health.py.bak-20260808, GUIA.bak-20260808c.
**v1.3.26 (08-ago-2026):** tarea 5 (7o refactor): migrate_to_ko.migrate_dec() con OpenCode — extraidas _construir_ko_base y _preservar_legacy_fields; domain/scope a constantes; migrate_dec 19 -> 10 (verde). Red: salida identica (5 YAML temporales, diff vacio) + verificacion propia de OpenCode (100 campos, 0 mismatches) + 8 tests nuevos (suite 153 OK). Quedan 39 amarillas. Backups: migrate_to_ko.py.bak-20260808, GUIA.bak-20260808d.
**v1.3.27 (08-ago-2026):** tarea 5 (8o refactor): evidence.main() con OpenCode — extraidas 4 funciones puras de cuerpo (_cuerpo_decisiones_por_politica, _cuerpo_fallback_rate, _cuerpo_uso_rules, _cuerpo_uso_rag) y _registrar_obs; main 17 -> 8 (verde). Red: flujo identico en entorno aislado (dirs temporales, rutas normalizadas) + verificacion propia de OpenCode (0 mismatches) + 14 tests nuevos (suite 167 OK). Quedan 38 amarillas. Backups: evidence.py.bak-20260808, GUIA.bak-20260808e.
**v1.3.28 (08-ago-2026):** tarea 5 (9o refactor): knowledge_resolver.format_synthesis() con OpenCode — extraidas 7 secciones puras (_cabecera_sintesis, _seccion_hechos/decisiones/conflictos/hipotesis/acciones/confianza); format_synthesis 17 -> 2 (verde). Red: salida byte-identica (Synthesis completa, diff vacio) + verificacion propia de OpenCode (6 casos, 0 mismatches) + 7 tests nuevos (suite 174 OK). Backups: knowledge_resolver.py.bak-20260808, GUIA.bak-20260808f.
**v1.3.29 (08-ago-2026):** tarea 5 (10o refactor): decision_engine.format_output() con OpenCode — extraidas 7 secciones puras (_cabecera_output, _seccion_checklist/bloqueos/activaciones/inyecciones/modelo/avisos); format_output 16 -> 10 (verde). Red: salida byte-identica (2 casos, diff vacio) + verificacion propia de OpenCode (0 mismatches) + 8 tests nuevos (suite 182 OK). Backups: decision_engine.py.bak-20260808, GUIA.bak-20260808g.
**v1.3.30 (08-ago-2026):** tarea 5 (11o refactor): bolsa_scan.main() con OpenCode — extraidas _parsear_args, _escaneo_tickers, _guardar_snapshot y _formatear_tabla; main 15 -> 3 (verde). Red: flujo identico en entorno aislado (fetch mockeado, OUT_DIR temporal, rutas/timestamp normalizados) + verificacion propia de OpenCode (0 mismatches) + suite 182 OK. Backups: bolsa_scan.py.bak-20260808, GUIA.bak-20260808h.
**v1.3.31 (08-ago-2026):** tarea 5 (12o refactor): debt_detector.check_huerfano_rules() con OpenCode — extraidas _nombres_origen, _origen_existe y _origen_referenciado; 15 -> 5 (verde). Red: salida identica (9 rules, dirs temporales) + verificacion propia de OpenCode (8 casos, 0 mismatches) + suite 182 OK. Backups: debt_detector.py.bak-20260808, GUIA.bak-20260808i.
**v1.3.32 (08-ago-2026):** tarea 5 (13o refactor): verificar_fk_kos.main() con OpenCode — extraidas _dedupe_mantener_orden, _salida_json, _salida_texto y _salida_gate; main 15 -> 8 (verde). Red: salida real del lab identica (6 combinaciones de args incl. exit codes) + verificacion propia de OpenCode (0 mismatches) + suite 192 OK. Backups: verificar_fk_kos.py.bak-20260808, GUIA.bak-20260808j.
**v1.3.33 (08-ago-2026):** NIVEL 1 cerrado (validacion de instrumentos). Obs 1: knowledge_health.extract_date() tenia bug real - yaml.safe_load convierte fechas ISO a datetime.date y extract_date solo aceptaba datetime/str -> None SIEMPRE para todas las fechas (pitfall 2 de refactor-seguro existia en tests desde 07-ago pero nunca aplicado al codigo). Fix: caso isinstance(v, date) -> datetime.combine. Verificado: RULE-010 lee created/last_validated/expires (coincide con KEL); health 64->68, issues 14->12 (los 12 restantes son OBS de telemetria, legitimos). OP-20260808-012. Obs 2: el '565 nuevos' del dry-run del indexer en check-lab-integral.sh es FALSO POSITIVO del propio script (linea 44 usa --force, que ignora el sidecar por diseno). Verificado: sin --force 0 nuevos/1 modificado/564 sin cambios. Indexer SANO. OP-20260808-013. Leccion: en el chequeo integral, el paso 11 SIEMPRE mostrara 'N nuevos' por el --force; senal real = dry-run sin --force.

**v1.3.34 (09-ago-2026):** tarea 5 (14o refactor): knowledge_health._procesar_ko() con OpenCode — extraidas _construir_item_ko, _contar_estado_dec, _detectar_problemas_ko y _verificar_evidencia_transitiva; complejidad 36 -> 12 (verde). Red: salida identica + suite 192 OK. Backup knowledge_health.py.bak-20260809.

**v1.3.35 (09-ago-2026):** tarea 5 (15o refactor): observer.main() con OpenCode — extraidas _cargar_kos_conocidas, _metricas_decisiones, _metricas_activaciones y _metricas_rag; complejidad 28 -> <15 (verde). Red: JSON y .md identicos + suite 192 OK. Backup observer.py.bak-20260809. **CON ESTA, EL LAB QUEDA CON 0 FUNCIONES MUY COMPLEJAS (>20)** — de 2 a 0. Quedan 36 amarillas (11-20).

**v1.3.36 (09-ago-2026):** tarea 5 (16o refactor): knowledge_health._clasificar_por_nombre() — cascada de 7 ifs convertida a tabla de reglas (tupla (condicion, tipo) + loop); complejidad 17 -> 13. Red: condiciones IDENTICAS al original (substring en cualquier posicion, no startswith — corregido al detectar el cambio de semantica) + suite 192 OK. Backup knowledge_health.py.bak-20260809b. Quedan 36 amarillas (13 son resultado de refactors previos con tests, umbral de prioridad real >=14).

**v1.3.37 (09-ago-2026):** tarea 5 (17o refactor): context_builder_estructurado._resumen_yaml() — extraida _campos_clave(data, claves) (helper puro reutilizable); complejidad 16 -> 14. Red: salida identica + suite 192 OK. Backup context_builder_estructurado.py.bak-20260809. Quedan 36 amarillas.

**v1.3.38 (09-ago-2026):** tarea 5 (18o refactor): knowledge_health._detectar_problemas_ko() — extraidas _chequear_expiracion (4) y _chequear_validacion (3); el triple if de expiración convertido a if/elif/elif (casos mutuamente excluyentes, equivalente). Complejidad 16 -> 8 (verde). Red: suite 192 OK. Backup knowledge_health.py.bak-20260809c. Quedan 35 amarillas.

**v1.3.39 (09-ago-2026):** tarea 5 (19o refactor): indexer.build_index() — extraidas _conservar_sin_cambios (3) y _embedear_docs (3); complejidad 15 -> 11. Red: suite completa OK con venv RAG. Backup indexer.py.bak-20260809. Quedan 35 amarillas.

**v1.3.40 (09-ago-2026):** tarea 5 (20o refactor): medir_agentic.main() — refactor de la sesión CLI (extraidas _parsear_args, _clasificar_y_contar, _construir_resultado, _guardar_history, _imprimir_json, _imprimir_texto; main 15 -> 4) + aporte de Telegram (extraida _medir_banco, main 4 -> 3). Red: salida idéntica original-vs-nuevo + 13 tests nuevos (tests/test_medir_agentic.py) + suite 205 OK. Pitfall 25 aplicado (no es instrumento de baseline). Backup medir_agentic.py.bak-20260809. OP-20260809-001. Quedan 34 amarillas.

**v1.3.41 (09-ago-2026):** tarea 5 (21o refactor): escanear_predicciones.cargar_predicciones() — extraidas _validar_campos (5) y _validar_no_autoeval (4); complejidad 14 -> 9 (verde). Red: suite 205 OK. Backup escanear_predicciones.py.bak-20260809. Quedan 33 amarillas.

**v1.3.42 (09-ago-2026):** tarea 5 (22o refactor): evidence_contract.verify_ko() — extraido _chequear_minimo (patrón común de los 3 chequeos de mínimo; caso evidence con ausente_a_missing=True porque el original lo metía en MISSING y no en notes — semántica preservada); complejidad 14 -> 8 (verde). Red: suite 205 OK. Backup evidence_contract.py.bak-20260809. Quedan 32 amarillas.

**v1.3.43 (09-ago-2026):** tarea 5 (23o refactor): indexer.yaml_to_text() — extraida _campos_presentes (helper puro, mismo patrón que _campos_clave de context_builder); complejidad 14 -> 10 (verde). Red: suite completa OK con venv RAG. Backup indexer.py.bak-20260809b. Quedan 31 amarillas.

**v1.3.44 (09-ago-2026):** tarea 5 (24o refactor): knowledge_health.audit_structure() — extraida _acumular_archivo (acumulación de stats por archivo); complejidad 14 -> 9 (verde). Red: suite 205 OK. Backup knowledge_health.py.bak-20260809d. Quedan 30 amarillas.

**v1.3.45 (09-ago-2026):** tarea 5 (25o refactor): revalidar_kos.clasificar() — extraida _clasificar_ko (clasificación individual, 13) + dispatch por diccionario destino; clasificar 14 -> 3 (verde). Red: suite 205 OK. Backup revalidar_kos.py.bak-20260809. Quedan 29 amarillas (main de revalidar_kos 14 sigue pendiente).

**v1.3.46 (09-ago-2026):** tarea 5 (26o refactor): revalidar_kos.main() — extraida _imprimir_grupo (patrón común de impresión de los 3 grupos); main 14 -> 8 (verde). Red: suite 205 OK. Backup revalidar_kos.py.bak-20260809b. Quedan 28 amarillas.

**v1.3.47 (09-ago-2026):** tarea 5 (27o refactor): run_10_tests.format_results() — extraida _formatear_fila (formato de fila con métricas ✅/❌/— + detalle activación); format_results 14 -> 4 (verde). Red: suite 205 OK. Backup run_10_tests.py.bak-20260809. Quedan 27 amarillas.

**v1.3.48 (09-ago-2026):** tarea 5 (28o refactor): agentic_loop.evaluar_vigencia() — extraida _motivo_no_vigente (cálculo del motivo: status/expires/superseded); evaluar_vigencia 13 -> 7 (verde). Red: suite 205 OK. Backup agentic_loop.py.bak-20260809. Quedan 26 amarillas.

**v1.3.49 (09-ago-2026):** tarea 5 (29o refactor): consolidador_sesiones._contar_sesiones() — extraida _extraer_fecha (parseo de timestamp: epoch numérico o ISO string); _contar_sesiones 13 -> 9 (verde). Red: suite 205 OK. Backup consolidador_sesiones.py.bak-20260809. Quedan 25 amarillas.

**v1.3.50 (09-ago-2026):** tarea 5 (30o refactor): evidence_contract._parse_yaml_simple() — extraida _procesar_linea_clave (parseo de línea sin indentar); _parse_yaml_simple 13 -> 9 (verde). Red: suite 205 OK. Backup evidence_contract.py.bak-20260809b. Quedan 24 amarillas.

**v1.3.51 (09-ago-2026):** tarea 5 (31o refactor): agentic_loop.imprimir_informe() — extraidas _imprimir_fuentes (✓/✗) y _imprimir_vigencia (⚠ no vigentes); imprimir_informe 12 -> 5 (verde). Red: suite 205 OK. Backup agentic_loop.py.bak-20260809b. Quedan 23 amarillas.

**v1.3.52 (09-ago-2026):** tarea 5 (32o refactor): context_builder.extract_card_summary() — extraidas _es_inicio_captura y _es_fin_captura + constante SECCIONES_CAPTURA; los dos ifs independientes convertidos a if/elif (equivalente: "## Fortalezas" nunca resetea); extract_card_summary 12 -> 6 (verde). Red: suite 205 OK. Backup context_builder.py.bak-20260809. Quedan 22 amarillas.

**v1.3.53 (09-ago-2026):** tarea 5 (33o refactor): context_builder.build_context() — extraidas _marcar_checks, _contexto_generico y _bloque_ficha_modelo; build_context 12 -> 7 (verde). Red: suite 205 OK. Backup context_builder.py.bak-20260809b. Quedan 21 amarillas.

**v1.3.54 (09-ago-2026):** tarea 5 (34o refactor): convert_sessions.convert() — extraidas _formatear_conversacion y _construir_contenido; convert 12 -> 6 (verde). Red: formato byte-idéntico (detectado y corregido: el helper original cambiaba \n\n por \n — restaurado a byte-idéntico) + suite 205 OK. Backup convert_sessions.py.bak-20260809. Quedan 20 amarillas.

**v1.3.55 (09-ago-2026):** tarea 5 (35o refactor): search._busqueda_hibrida() — extraidas _construir_where (cláusula where de filtros) y _calcular_rrf (fusión por rango recíproco); _busqueda_hibrida 12 -> 6 (verde). Red: suite completa OK con venv RAG. Backup search.py.bak-20260809. Quedan 19 amarillas.

**v1.3.56 (09-ago-2026):** tarea 5 (36o refactor): task_understanding.analyze() — extraidas _detectar_artefacto, _detectar_complejidad y _detectar_restricciones; analyze 12 -> 1 (verde). Red: suite 205 OK. Backup task_understanding.py.bak-20260809. Quedan 18 amarillas.

**v1.3.57 (09-ago-2026):** tarea 5 (37o refactor): context_builder_estructurado._resumen_yaml() — extraidas _campos_legacy y _params_legacy con OpenCode; _resumen_yaml 14 -> 8 (verde). Red: suite 205 OK. Backup context_builder_estructurado.py.bak-20260809b. **CON ESTA, EL LAB NO TIENE NINGUNA FUNCION >=14** — quedan 19 amarillas (11-13).

**v1.3.58 (09-ago-2026):** tarea 5 (38o refactor): knowledge_health._clasificar_por_nombre() — extraida _coincide (chequeo substring+dir); tabla de reglas con tuplas (substrings, dirname, tipo); 13 -> 3 (verde). Red: suite 205 OK. Backup knowledge_health.py.bak-20260809e. Quedan 18 amarillas.

**v1.3.59 (09-ago-2026):** tarea 5 (39o refactor): revalidar_kos._clasificar_ko() — extraida _clase_por_dias (vencido/proximo/en_orden); 13 -> 7 (verde). Red: suite 205 OK. Backup revalidar_kos.py.bak-20260809c. Quedan 17 amarillas.

**v1.3.60 (09-ago-2026):** tarea 5 (40o refactor): run_10_tests.evaluate_problem() — extraidas _evaluar_m4 (3 ramas) y _puntuar; 13 -> 3 (verde). Red: suite 205 OK. Backup run_10_tests.py.bak-20260809b. Quedan 16 amarillas.

**v1.3.61 (09-ago-2026):** tarea 5 (41o refactor): verificar_fk_kos.escanear_ko() — extraida _revisar_prosa (string/list/dict); 13 -> 3 (verde). Red: suite 205 OK. Backup verificar_fk_kos.py.bak-20260809. Quedan 15 amarillas (14 de 11 + _revisar_prosa 11).

**v1.3.62 (09-ago-2026):** tarea 5 (42o refactor): complejidad_crap.imprimir_reporte() — extraidas _marca, _formatear_funcion y _contar_categorias; 11 -> 7 (verde). Red: suite 205 OK. Backup complejidad_crap.py.bak-20260809. Quedan 14 amarillas.

**v1.3.63 (09-ago-2026):** tarea 5 (43o refactor): debt_detector.check_version_antigua() — extraida _leer_versiones_modelos; 11 -> 6 (verde). Red: suite 205 OK. Backup debt_detector.py.bak-20260809. Quedan 13 amarillas.

**v1.3.64 (09-ago-2026):** tarea 5 (44o refactor): decision_engine.evaluate() — extraida _aplicar_accion (dispatch de 5 acciones); 11 -> 5 (verde). Red: suite 205 OK. Backup decision_engine.py.bak-20260809. Quedan 12 amarillas.

**v1.3.65 (09-ago-2026):** tarea 5 (45o refactor): evaluator_optimizer._integrate_lab_knowledge() — extraida _consultar_seccion (patrón RAG repetido x3); sigue en 11 (bloques condicionales, aceptable). Red: suite 205 OK. Backup evaluator_optimizer.py.bak-20260809.

**v1.3.66 (09-ago-2026):** tarea 5 (46o refactor): evaluator_optimizer.evaluate_response() — extraidas _calcular_similitud (jaccard) y _metricas_estructura; 11 -> 6 (verde). Red: suite 205 OK. Backup evaluator_optimizer.py.bak-20260809. Quedan 11 amarillas.

**v1.3.67 (09-ago-2026):** tarea 5 (47o refactor): evidence_collector.evaluate_evidence() — extraidas _accion_observacion, _accion_hipotesis y _accion_e3_candidato; sigue en 11 (condiciones and, aceptable). Red: suite 205 OK. Backup evidence_collector.py.bak-20260809.

**v1.3.68 (09-ago-2026):** tarea 5 (48o refactor): indexer.build_index() — extraida _clasificar_y_reportar (clasificación + early-returns); 11 -> 7 (verde). Red: suite OK (venv RAG). Backup indexer.py.bak-20260809c. Quedan 10 amarillas.

**v1.3.69 (09-ago-2026):** tarea 5 (49o refactor): knowledge_health._verificar_evidencia_transitiva() — extraida _dep_aporta_evidencia (chequeo de dependencia); 11 -> 6 (verde). Red: suite 205 OK. Backup knowledge_health.py.bak-20260809f. Quedan 9 amarillas.

**v1.3.70 (09-ago-2026):** tarea 5 (50o refactor): proposer.cmd_list() — extraidas _parsear_propuesta y _imprimir_lista; 11 -> 7 (verde). Red: suite 205 OK + prueba funcional cmd_list (3 pendientes, 15 decididas). Backup proposer.py.bak-20260809. Quedan 8 amarillas.

**v1.3.71 (09-ago-2026):** tarea 5 (51o refactor): proposer.main() — extraida _construir_contenido (YAML de propuesta); sigue en 11 (dispatch CLI inherente, aceptable). Red: suite 205 OK. Backup proposer.py.bak-20260809. Quedan 8 amarillas.

**v1.3.72 (09-ago-2026):** tarea 5 (52o refactor): rag_telemetry.resumen_ultimas() — extraidas _leer_entradas y _calcular_medias; 11 -> 4 (verde). Red: suite 205 OK. Backup rag_telemetry.py.bak-20260809. Quedan 7 amarillas.

**v1.3.73 (09-ago-2026):** tarea 5 (53o refactor): run_10_tests._formatear_fila() — extraidas _emoji (conversión métrica→emoji) y _detalle_activacion; 11 -> 1 (verde). Red: suite 205 OK. Backup run_10_tests.py.bak-20260809c. Quedan 6 amarillas.

**v1.3.74 (09-ago-2026):** tarea 5 (54o refactor): verificar_fk_kos._escanear_estructurados() — extraida _chequear_ref (referencia rota); 11 -> 6 (verde). Red: suite 205 OK + verificación funcional (misma salida: 1 referencia histórica). Backup verificar_fk_kos.py.bak-20260809b.

**v1.3.75 (09-ago-2026):** tarea 5 (55o refactor): verificar_fk_kos.escanear_docs() — extraida _escanear_archivo_doc (wikilinks + menciones); 11 -> 6 (verde). Red: suite 205 OK. Backup verificar_fk_kos.py.bak-20260809b. Quedan 5 amarillas: _revisar_prosa (11), _integrate_lab_knowledge (11), evaluate (11), evaluate_evidence (11), proposer.main (11) — todas aceptables (condiciones inherentes).

**v1.3.76 (09-ago-2026):** tarea 5 (56o refactor): verificar_fk_kos._revisar_prosa() — extraida _revisar_valor_prosa (str/list/dict); 11 -> 4 (verde). Red: suite 205 OK. Backup verificar_fk_kos.py.bak-20260809c. Quedan 4 amarillas.

**v1.3.77 (09-ago-2026):** tarea 5 (57o refactor): evaluator_optimizer._integrate_lab_knowledge() — extraidas _consultar_antipatrones, _consultar_ficha_modelo y _consultar_decisiones (3 bloques RAG); 11 -> 3 (verde). Red: suite 205 OK. Backup evaluator_optimizer.py.bak-20260809b. Quedan 3 amarillas.

**v1.3.78 (09-ago-2026):** tarea 5 (58o refactor): decision_engine.evaluate() — extraidas _procesar_reglas_hardcodeadas y _construir_resultado; 11 -> 2 (verde). Red: suite 205 OK. Backup decision_engine.py.bak-20260809b. Quedan 2 amarillas.

**v1.3.79 (09-ago-2026):** tarea 5 (59o refactor): evidence_collector.evaluate_evidence() — extraidas _calcular_improvement, _nivel_evidencia y _next_step; 11 -> 3 (verde). Red: suite 205 OK. Backup evidence_collector.py.bak-20260809b. Quedan 1 amarilla.

**v1.3.80 (09-ago-2026):** tarea 5 (60o refactor): proposer.main() — extraidas _dispatch_comandos y _escribir_propuestas; 11 -> 5 (verde). Red: suite 205 OK + prueba funcional cmd_list OK. Backup proposer.py.bak-20260809b. Quedan 0 amarillas de la lista original.

**v1.3.81 (09-ago-2026):** tarea 5 (61o refactor): context_builder_estructurado._resumen_markdown() — extraidas _parsear_frontmatter y _resumen_body (reutiliza _campos_clave); 12 -> 3 (verde). Red: suite 205 OK. Backup context_builder_estructurado.py.bak-20260809c. **HITO: LAB CON 0 FUNCIONES COMPLEJAS (11-20) Y 0 MUY COMPLEJAS (>20) — 423 funciones, todas <=10.**

---

## INDICE

- [Capitulo 0 — El Lab en 5 minutos](#capitulo-0)
- [Capitulo 1 — Hardware y sistema operativo](#capitulo-1)
- [Capitulo 2 — Infraestructura: Docker, servicios y protocolos](#capitulo-2)
- [Capitulo 3 — Motor de inferencia local (LM Studio)](#capitulo-3)
- [Capitulo 4 — Hermes Agent: el cerebro](#capitulo-4)
- [Capitulo 5 — Sistemas de conocimiento (LPA y Knowledge Objects)](#capitulo-5)
- [Capitulo 6 — RAG local (BGE-M3 + LanceDB)](#capitulo-6)
- [Capitulo 7 — Arquitectura y enrutamiento (ai-router)](#capitulo-7)
- [Capitulo 8 — Sincronizacion entre sesiones](#capitulo-8)
- [Capitulo 9 — Los productos del lab](#capitulo-9)
- [Capitulo 10 — Glosario completo](#capitulo-10)

---

<a name="capitulo-0"></a>
# CAPITULO 0 — EL LAB EN 5 MINUTOS

## Que es Joko Lab

Joko Lab es un laboratorio personal de inteligencia artificial que funciona
100% en casa (Erandio), sobre un PC con GPU NVIDIA RTX A2000 de 12 GB.
Combina modelos de IA en la nube (DeepSeek) y locales (LM Studio) con un
sistema de conocimiento que aprende de cada sesion de trabajo.

**Objetivo:** que la IA no solo responda, sino que el laboratorio acumule
conocimiento verificable que mejore decisiones futuras.

## El mapa en una frase

```
[Tu] → [Hermes Agent] → [DeepSeek cloud / LM Studio local] → [Conocimiento LPA] → [Mejores decisiones]
```

## Las piezas principales

| Pieza | Que es | Donde vive | Puerto |
|-------|--------|-----------|--------|
| Hermes Agent | El agente que te asiste (esto) | ~/.hermes/ | CLI + Telegram |
| DeepSeek | Modelo cloud principal (razona, coordina) | api.deepseek.com | — |
| LM Studio | Motor de inferencia local (11 modelos, 04-sep-2026) | /mnt/ssd_ia_datos/LM STUDIO/ | 1234 |
| Ollama | Motor local secundario (Docker) | /mnt/ssd_ia_datos/ollama | 11434 |
| n8n | Automatizacion de workflows | /mnt/ssd_ia_datos/n8n | 5678 |
| Stirling PDF | Utilidades PDF | Docker | 8081 |
| pdf-cleaner | Limpieza de PDFs | Docker | 8000 |
| LanceDB | Base vectorial (RAG) | ~/joko-lab/.lancedb/ | — |
| Monitor LM Studio | Dashboard de observabilidad | systemd user | 5000 |
| Gemini Notebook | Copia de guia + normas para estudio | gdrive:NOTEBOOKLM/JOKO-LAB/ | — |

## El conocimiento en 4 capas

```
CAPA 1 — Infraestructura    (modelos, Hermes)
CAPA 2 — Recuperacion       (RAG, embeddings, contexto)
CAPA 3 — Gobierno           (decisiones, reglas, salud del conocimiento)
CAPA 4 — Evolucion          (validacion, poda, ciclo de vida)
```

## Los 4 cerebros (modelo cognitivo)

| Cerebro | Rol | Donde | Que responde |
|---------|-----|-------|--------------|
| DeepSeek | Piensa, decide, coordina | Cloud | Que tiene sentido hacer |
| LM Studio | Ve, evalua, critica | Local GPU | Es correcto visualmente |
| Ollama | Simula, genera, explica | Local | Que pasaria si... |
| Telemetria/Runtime | Mide, observa, contrasta | El sistema | Que ocurre realmente |

**Reglas duras:**
- DeepSeek nunca ve (no tiene vision) → delega en LM Studio
- LM Studio nunca decide → evalua, y DeepSeek decide
- Ollama nunca critica → genera escenarios
- Telemetria nunca opina → solo mide

## Rutas criticas del sistema

```
/home/jokoalmi/automation-stack/        → Stack Docker (n8n, ollama, pdf)
/home/jokoalmi/joko-lab/                → Conocimiento, herramientas, protocolos
/home/jokoalmi/hermes-lab/              → Scripts de sesion, informes, git
/mnt/ssd_ia_datos/                      → Datos persistentes (n8n, modelos, backups)
/home/jokoalmi/lmstudio_real_monitor/   → Monitor Flask de LM Studio
/home/jokoalmi/lm-studio-benchmarks/    → Resultados de benchmarks de modelos
/home/jokoalmi/perfume-ia/              → PRODUCTO: Perfume IA (Experimento 001)
```

## Protocolo de sesion (importante)

- **inicio.sh** — al arrancar una sesion: ejecuta checks, genera estado-inicial.json, compara con el ultimo cierre
- **fin.sh** — al cerrar: snapshot final, diff, backup git, informe, para el stack Docker
- **checkpoint.sh** — durante la sesion: punto de recuperacion sin cerrar
- **recibo antes de commit (RULE-006)** — no se commitea sin recibo: primero `hooks/generar_recibo.sh <quien-aprueba> [nota]` y despues `git commit`; el gate `hooks/pre-commit` **aborta** si el arbol en staging no coincide byte a byte con el recibo (un solo byte distinto lo invalida). Activo en los DOS repos git del lab (`core.hooksPath=hooks`), con los hooks versionados desde el 29-sep. Log: `~/.hermes/logs/joko-rdd.log`; kill switch `JOKO_RDD_DISABLE=1` (una vez) o fichero `.joko-rdd-disable`.

## DIRECTIVA MAESTRA DEL LAB: NUNCA RESPONDER DE MEMORIA (16-ago-2026, añadida a la GUIA 19-ago-2026)

Mas alla de minimizar alucinaciones, el lab **nunca jamás debe responder "de memoria"**
(desde lo que el modelo "sabe" sin verificar), sino siguiendo las normas y reglas del
lab para dar la mejor respuesta posible SIEMPRE.

Jerarquia de respuesta obligatoria:
1. **Consultar la skill/procedimiento del dominio** (gate-veracidad, SVP, pipeline
   video/registro, etc.)
2. **Usar datos reales** (BD/logs/archivos) — nunca lo que el LLM "recuerde"
3. Si falta fuente o procedimiento → **buscar** (agente, web_search) o marcar NO VERIFICADO
4. Si el procedimiento está documentado → **EJECUTAR sin preguntar** (LEC-001/002)

Formaliza como REGLA GENERAL lo que LEC-001/002 corrigieron en casos concretos
("preguntar = responder de memoria sin consultar la skill"). El gate de veracidad
etiqueta el OUTPUT; esta regla garantiza el PROCESO antes de emitir. Aplica a todos
los emisores: Telegram, CLI, crons, subagentes.

## Zonas protegidas (nunca tocar sin confirmacion explicita)

```
/mnt/ssd_ia_datos/n8n        → datos de n8n
/mnt/ssd_ia_datos/exports    → exportaciones
/mnt/ssd_ia_datos/backups    → backups
```

---

<a name="capitulo-1"></a>
# CAPITULO 1 — HARDWARE Y SISTEMA OPERATIVO

## 1.1 El equipo

| Componente | Valor real (verificado) |
|-----------|------------------------|
| GPU | NVIDIA RTX A2000 12 GB |
| Driver NVIDIA | 595.84 (Production Branch, junio 2026) |
| Sistema | Ubuntu (derivado, kernel 7.0.0-28-generic) |
| Zona horaria | Europe/Madrid (CEST, +0200) |
| Usuario | jokoalmi |

**Regla del driver:** el driver 595.84 esta confirmado como optimo. No
actualizar salvo necesidad concreta (un modelo nuevo que lo exija, un bug
de driver, etc.).

## 1.2 La GPU: RTX A2000 12 GB — limitaciones y consecuencias

Esta GPU tiene 12 GB de VRAM. Es la restriccion central de todo el lab:

- **No caben modelos > 12 GB** (ej: Granite 4.0 H Small de 19.5 GB NO cabe)
- **Un solo modelo grande cargado a la vez** (rotacion obligatoria)
- **El modelo grande tipico**: 7-9 GB de VRAM deja 3-5 GB libres
- **Embeddings (BGE-M3) compiten por la misma GPU** — problema conocido y
  resuelto usando el endpoint de LM Studio (ver capitulo 6)

Comando para ver el estado real:

```bash
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits
```

## 1.3 Medir GPU, RAM, discos y procesos

| Que quieres saber | Comando |
|------------------|---------|
| GPU (uso, VRAM, temperatura) | `nvidia-smi` |
| Donde esta nvidia-smi | `which nvidia-smi` |
| RAM | `free -h` |
| Discos | `df -h` |
| Procesos por CPU | `ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu \| head -20` |
| Puertos en escucha | `ss -ltnp` |
| Que usa el puerto 5000 | `ss -ltnp \| grep 5000` |

## 1.4 Discos y datos persistentes

Todo lo importante vive en `/mnt/ssd_ia_datos/`:

| Ruta | Contenido |
|------|-----------|
| /mnt/ssd_ia_datos/n8n | Datos de n8n (ZONA PROTEGIDA) |
| /mnt/ssd_ia_datos/exports | Exportaciones (ZONA PROTEGIDA) |
| /mnt/ssd_ia_datos/backups | Backups (ZONA PROTEGIDA) |
| /mnt/ssd_ia_datos/ollama | Modelos de Ollama |
| /mnt/ssd_ia_datos/LM STUDIO | Modelos de LM Studio (9 GGUF) |
| /mnt/ssd_ia_datos/lab-state | Estado del Runtime, politicas, secretos, logs |

**Nota:** la ruta real del volumen n8n es `/mnt/ssd_ia_datos/n8n`, NO
`/home/jokoalmi/automation-stack/n8n/secrets.json` (esa ruta no existe).

## 1.5 Rutina del PC

- El PC se apaga de madrugada (~1:00-9:00 CEST)
- No programar tareas nocturnas
- La franja de trabajo tipica es 9:00-1:00
- Los crones diarios se programan a las 22:00 (antes de apagar)

## 1.6 Herramientas base instaladas

| Herramienta | Para que |
|-------------|----------|
| uv | Gestor de entornos Python moderno |
| cargo | Compilador de Rust (algunas herramientas lo usan) |
| node | JavaScript (n8n, MCP servers) |
| python3 | Scripts del lab (indexer, search, decision engine...) |
| docker + docker compose v2 | Contenedores (SIEMPRE `docker compose`, nunca `docker-compose`) |

---

<a name="capitulo-2"></a>
# CAPITULO 2 — INFRAESTRUCTURA: DOCKER, SERVICIOS Y PROTOCOLOS

## 2.1 El stack Docker

Definido en `/home/jokoalmi/automation-stack/docker-compose.yml`.
Red interna: `automation_net`. Todos los puertos escuchan solo en
`127.0.0.1` (no expuestos a la red local).

### 2.1.1 n8n (puerto 5678) — ZONA PROTEGIDA

```yaml
n8n:
  image: docker.n8n.io/n8nio/n8n:latest
  ports: ["127.0.0.1:5678:5678"]
  environment:
    - TZ=Europe/Madrid
    - N8N_RUNNERS_TASK_TIMEOUT=900
    - N8N_RESTRICT_FILE_ACCESS_TO=/files;/backups
  volumes:
    - /mnt/ssd_ia_datos/n8n:/home/node/.n8n
    - /mnt/ssd_ia_datos/exports:/files
    - /mnt/ssd_ia_datos/backups:/backups
  deploy: { memory limit: 2G }
```

**Que es:** plataforma de automatizacion de workflows (visual, con nodos).
**Para que se usa en el lab:** automatizaciones (ej: workflow ENVIO WHATSAPP).
**Proteccion:** n8n es zona protegida. No reiniciar, parar, recrear ni
actualizar sin confirmacion explicita. Sus datos viven en volumenes reales
que NO se pierden al recrear contenedores.

### 2.1.2 stirling-pdf (puerto 8081)

```yaml
stirling-pdf:
  image: frooodle/s-pdf:latest
  ports: ["127.0.0.1:8081:8080"]
  environment: [SECURITY_ENABLELOGIN=false]
```

**Que es:** suite de utilidades PDF autocontenida (convertir, dividir, OCR...).

### 2.1.3 pdf-cleaner (puerto 8000)

```yaml
pdf-cleaner:
  build: { context: ./pdf-cleaner }
  ports: ["127.0.0.1:8000:8000"]
```

**Que es:** servicio propio (imagen construida localmente) para limpiar PDFs.

### 2.1.4 ollama (puerto 11434) — con GPU

```yaml
ollama:
  image: ollama/ollama:latest
  ports: ["127.0.0.1:11434:11434"]
  volumes: [/mnt/ssd_ia_datos/ollama:/root/.ollama]
  gpus: all
  environment:
    - OLLAMA_HOST=0.0.0.0:11434
    - OLLAMA_CONTEXT_LENGTH=65536
    - OLLAMA_NUM_PARALLEL=1
    - OLLAMA_MAX_LOADED_MODELS=1
    - OLLAMA_KEEP_ALIVE=10m
    - OLLAMA_FLASH_ATTENTION=1
    - OLLAMA_KV_CACHE_TYPE=q8_0
```

**Que es:** motor de inferencia local alternativo a LM Studio.
**Configuracion clave:** contexto 64K, un solo modelo cargado, flash attention.
**En este lab:** actualmente es secundario; LM Studio es el motor principal.
Hermes puede depender de Ollama si usa `http://localhost:11434/v1`.

## 2.2 Comandos Docker esenciales

```bash
# Estado real de los contenedores (SIEMPRE este comando)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps

# Logs de un servicio (solo lectura)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=80 n8n

# Configuracion efectiva (solo lectura)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml config
```

**Regla critica:** NO usar `docker compose ls -a` para concluir si los
contenedores estan activos. `ps` muestra el estado real.

**Comandos que requieren confirmacion explicita:** stop, restart, down,
up -d, pull, prune. El stack entero es zona sensible.

## 2.3 Servicios systemd de usuario

Ademas de Docker, hay servicios systemd de usuario (sobreviven a la sesion):

| Servicio | Funcion |
|----------|---------|
| lmstudio-headless.service | Arranque headless LM Studio + carga GLM (vision) |
| lmstudio-monitor.service | Monitor web en :5000 (dashboard de observabilidad) |
| joko-indexer.service | Watchdog de re-indexacion RAG (incremental v2) |
| joko-reranker.service | Daemon del reranker (CPU, --max-seq 256, Nice=-10) |
| team-bus-watch.service | File bus multi-sesion (polling 5s, snapshot README) |
| hermes-gateway.service | Gateway de Telegram (Hermes) |
| hermes-pipeline-proxy.service | Proxy de observabilidad del pipeline LLM (TTFB, inferencia, tokens) en :9911 → upstream DeepSeek |

```bash
systemctl --user status lmstudio-monitor.service --no-pager
```

**Regla:** si un script Python/Flask debe estar siempre disponible, crear un
`.service` en `~/.config/systemd/user/` con `Restart=on-failure`.

## 2.4 Protocolo de apertura: inicio.sh

Ruta: `~/joko-lab/02-infrastructure/inicio/inicio.sh`

**Que hace (en orden):**
1. **Flock** — bloquea ejecucion paralela (evita corrupcion de JSON)
2. **Ejecuta los checks** — cada `check-*.sh` de `02-infrastructure/inicio/checks/`
   devuelve OK (0), WARN (1) o FAIL (2+)
3. **Genera estado-inicial.json** — git, docker, herramientas, PATH, kernel,
   driver NVIDIA, CUDA, modelos LM Studio. Escritura atomica (.tmp + mv)
4. **Compara con el ultimo estado-final.json** — detecta cambios entre sesiones
5. **Reporta anomalias** — con severidad [ALTA]/[MEDIA]
6. **Resumen** — FAIL>0 = revisar antes de trabajar; WARN>0 = se puede pero ojo

**Salida tipica:**

```
--- CHECKS ---
  ollama .......... OK
  lmstudio ........ OK
  docker .......... OK
--- ESTADO INICIAL ---
  Git:    main @ a1b2c3d
  Docker: 4/4 contenedores
  Checks: 5 pass, 0 warn, 0 fail
--- LABORATORIO LISTO ---
```

## 2.5 Protocolo de cierre: fin.sh

Ruta: `~/joko-lab/02-infrastructure/fin/fin.sh`

**Que hace (en orden):**
1. **Snapshot del estado actual** (git, docker, herramientas, kernel)
2. **Diff contra estado-inicial.json** — que cambio durante la sesion
3. **Backup si hay cambios** — commit automatico en hermes-lab
4. **Guarda estado-final.json** (escritura atomica)
5. **Genera informe** — `04-operations/reports/<fecha>-cierre-joko-lab.txt`
6. **Para el stack Docker** — `docker compose down` (por diseno)
7. **Cierre** — mensaje SESION CERRADA

**Importante:** fin.sh PARA el stack Docker. Es un comportamiento por diseno
(ahorro de recursos nocturno). Al dia siguiente hay que levantarlo con
inicio.sh o `docker compose up -d`.

## 2.6 checkpoint.sh

Ruta: `~/hermes-lab/scripts/checkpoint.sh`

**Que hace:** punto de recuperacion en medio de la sesion (sin cerrar).
Genera sessions.jsonl, guarda estado, etc. Tuvo un bug de variable
($POINT_DIR vs $TEMP_DIR) que se arreglo el 31-jul-2026.

## 2.7 Diagnostico rapido del stack

Skill: `diagnostico-stack-local` — solo lectura, informa en espanol:

```bash
# Estado de todos los servicios
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps -a

# Estado de la API de LM Studio
curl -s -m 5 http://localhost:1234/api/v0/models

# Estado de Ollama
curl -s -m 5 http://localhost:11434/v1/models

# Estado del monitor
curl -s http://localhost:5000/api/health
```

---

<a name="capitulo-3"></a>
# CAPITULO 3 — MOTOR DE INFERENCIA LOCAL (LM STUDIO)

## 3.1 Que es

LM Studio es el **Motor de Inferencia Local** de Joko Lab: sirve modelos
GGUF (formato de cuantizacion) sobre la GPU RTX A2000, exponiendo una API
compatible con OpenAI en `http://localhost:1234/v1`.

**Abstraccion importante:** la herramienta actual es LM Studio, pero el
conocimiento (parametros, metodologia, modelos) esta abstraido. Si manana
se sustituye por vLLM u Ollama, las capacidades permanecen (principio
JL-011: el flujo del conocimiento tiene prioridad sobre la optimizacion
de herramientas).

## 3.2 Arquitectura de procesos

```
Proceso lm-studio (daemon, se inicia con la GUI o autostart)
    └── hijo llama-server → atiende :1234 (API OpenAI-compatible)
```

- La GUI no es accesible por computer_use, pero el CLI `lms` permite
  cargar/descargar modelos sin intervencion manual.
- El daemon se inicia al abrir la GUI, por autostart
  (`~/.config/autostart/lmstudio.desktop`) **o BAJO DEMANDA con `lms server
  start`**. Medido el 13-oct-2026 (commit `b806b7c`): con `:1234` caido y la app
  cerrada, `lms server start` levanto el servidor en 2 s y sirvio una respuesta
  en 39 s. Ojo: lanza la app DESPRENDIDA, que hereda el fd del lock (sin
  CLOEXEC); el router la invoca en subshell con el fd 9 cerrado (ver 3.10).
- Servicio systemd: `lmstudio-llmster.service` (headless en :1234).

## 3.3 CLI lms

Ruta: `/home/jokoalmi/.lmstudio/bin/lms`

| Comando | Funcion |
|---------|---------|
| `lms server start` | Activa API Server en :1234 |
| `lms server stop` | Para el API Server |
| `lms server status` | Estado del servidor |
| `lms load <modelo>` | Carga un modelo en GPU |
| `lms unload` | Descarga el modelo actual |
| `lms ls` | Lista modelos en disco |
| `lms ps` | Modelos cargados ahora |
| `lms get <modelo>@q4_k_m -y` | Descarga un modelo |

## 3.4 Inventario real de modelos (04-sep-2026)

Los 11 modelos descargados (verificado por API hoy):

### No-reasoning (sin cadena de pensamiento)
| Modelo | Cuant. | VRAM | Velocidad media | Resultado |
|--------|--------|------|-----------------|-----------|
| dolphin3.0-llama3.1-8b-cyber-lora | Q4_K_M | 4.58 GiB | 5.6s | 5/5 ✅ |
| granite-4.1-8b | Q4_K_S | 4.74 GiB | 15.6s | 5/5 ✅ (mejor T2 no-reasoning) |
| granite-4.0-h-tiny | Q4_K_S | 3.72 GiB | 23.7s | 5/5 ✅ (minima VRAM) |
| lfm2.5-2.6b | Q4_K_M | 1.67 GiB | 55 tok/s | 7/7 ✅ (bateria 06-ago, tool calling) |

### Reasoning (con cadena de pensamiento en reasoning_content)
| Modelo | Cuant. | VRAM | Velocidad media | Resultado |
|--------|--------|------|-----------------|-----------|
| deepseek-r1-distill-qwen-14b | Q4_K_M | 8.37 GiB | 73.4s | 5/5 ✅ |
| openai/gpt-oss-20b (MXFP4) | MXFP4 | — (no medido) | — | 6/6 ✅ delegación (04-sep); sustituye a r1-14b/llama31 en delegation.model |
| gemma-4-12b-qat | Q4_0 | 6.66 GiB | 88.4s | 5/5 ✅ |
| glm-4.6v-flash | Q4_K_M | 7.41 GiB | 54.2s | 4/5 ⚠️ (T2 falla; rol=vision) |
| lfm2.5-vl-3b | — (no medido) | — | — | Respaldo vision VLM (04-sep): usado cuando vision_analyze/GLM cae (LM Studio localhost:1234) |

### Embeddings (para RAG, no chat)
| Modelo | Dimension | Uso |
|--------|-----------|-----|
| text-embedding-bge-m3 | 1024 | Ganador EXP-20260728-003 (multilingue, espanol) |
| text-embedding-nomic-embed-text-v1.5 | 768 | Alternativa (optimo ingles) |

## 3.5 Modelos reasoning: la regla del max_tokens

Los modelos reasoning separan la salida en dos canales:
- `reasoning_content` → cadena de pensamiento interna (invisible)
- `content` → la respuesta real

**Los reasoning tokens cuentan contra max_tokens.** Si el presupuesto es
bajo, el modelo se gasta todo en pensar y `content` sale VACIO.

**Regla practica:**
- max_tokens minimo: 400 (solo prompts triviales)
- max_tokens recomendado: 1024-2048 (uso real)
- max_tokens con vision: 2000 minimo
- Ratio reasoning:respuesta ≈ 10:1

**Tabla de fallo (ejemplo Gemma 4 12B, prompt "Di hola en espanol"):**
| max_tokens | content | resultado |
|-----------|---------|-----------|
| 50 | VACIO | length |
| 200 | VACIO | length |
| 400 | "¡Hola!" | stop |
| 800 | "¡Hola!" | stop |

**Sintoma de max_tokens insuficiente:** `content` vacio (`""`) con
`finish_reason: "length"`, mientras `reasoning_content` tiene texto
coherente.

## 3.6 Seleccion de modelo por rol (resumen operativo)

| Necesidad | Modelo | Por que |
|-----------|--------|---------|
| Chat rapido | Dolphin Cyber LoRA | 5.6s, 5/5 |
| Tool use / agentes | LFM 2.5 2.6B | 55 tok/s, tool calling nativo, 7/7 (06-ago) |
| JSON estructurado | Dolphin o Granite 4.1 | rapidos y fiables |
| Razonamiento ligero | Granite 4.1 8B | mejor T2 no-reasoning (3337ch) |
| Minima VRAM | Granite 4.0 h-tiny | 3.72 GiB |
| Razonamiento pesado | DeepSeek R1 14B | 5/5, equilibrado |
| Razonamiento profundo | Gemma 4 12B | 5/5, calidad maxima |
| Vision rapida | GLM 4.6V Flash | unico VLM rapido (15-30s) |
| Vision precisa | Gemma 4 12B | analisis detallado |

**Retirados del catalogo (no existen en disco):** llama-3.1-8b, qwen3-14b,
gemma-4-e4b — sustituidos por LFM 2.5 2.6B (tool calling) y la rotacion
granite/deepseek/gemma segun rol. No usar estos nombres.

## 3.7 Protocolo estandar de evaluacion (JL-010)

Cada modelo se prueba con 5 tests (script `evaluate-model.py`):

| Test | Dimension | Prompt |
|------|-----------|--------|
| T1 | Conocimiento | Explica el transformer en 3 frases |
| T2 | Razonamiento | Problema de las 3 cajas |
| T3 | Estructura | JSON con 3 recetas |
| T4 | Codigo | Funcion Python CSV + filtro edad + media saldo + type hints |
| T5 | Creatividad | Microrrelato 3 frases (IA cobra conciencia un martes) |

Parametros: temperature=0.7, top_p=0.9. max_tokens=1024 (no-reasoning)
o 2048 (reasoning).

Resultados ronda 3 (1-ago-2026) en:
`/home/jokoalmi/lm-studio-benchmarks/resultados/`

## 3.8 Fallos comunes y soluciones

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| content vacio, finish=length | max_tokens insuficiente (reasoning) | subir a 2048 |
| connection refused :1234 | LM Studio cerrado o API OFF | puede estar abierto con API apagada |
| lms load crashea ~50-76% | llama-server zombie (VRAM ocupada) | kill -9 llama-server, esperar, reintentar |
| VRAM ~8GB sin proceso visible | zombie de carga fallida | kill -9 $(pgrep llama-server) |
| Qwen3 14B T2 timeout >180s | razona 1200+ tokens en T2 | timeout >=300s en tests |
| modelo no cambia | API no expone load/unload REST | lms load <modelo> via CLI |

## 3.9 Monitor de observabilidad (:5000)
Proyecto `/home/jokoalmi/lmstudio_real_monitor`:
- Python + Flask + psutil + requests + nvidia-smi
- Dashboard en localhost:5000 (servicio systemd lmstudio-monitor.service)
- Muestra: VRAM, temperatura (de nvidia-smi), CPU/RAM (de psutil),
  modelos cargados, uso de API
- Endpoints: /api/health, /api/lmstudio/models, /api/gpu

Arranque manual (si el servicio no corre):

```bash
cd /home/jokoalmi/lmstudio_real_monitor
source .venv/bin/activate
python3 app.py
```

## 3.10 Router local/cloud por tipo de tarea (10-ago-2026)

Capa nueva sobre el Runtime (ai-router): decide el motor por TIPO DE TAREA
SIN tocar config.yaml (el modelo principal de Hermes sigue siendo deepseek
cloud; este router solo gobierna tareas batch/delegadas). Script:
`tools/llm-router.sh`.

| Modo | Motor | Uso |
|---|---|---|
| `batch` | R1-14B local (LM Studio :1234) | resumen, clasificacion, extraccion |
| `batch-json` | R1-14B local | JSON estricto (con fences) |
| `vision` | GLM 4.6V local | requiere GLM cargado |
| `check` | — | diagnostico de motores |

```bash
bash ~/joko-lab/tools/llm-router.sh batch "prompt"
bash ~/joko-lab/tools/llm-router.sh batch-json "prompt"
bash ~/joko-lab/tools/llm-router.sh check
```

**Uso en produccion:** informe-diario-joko-lab (cron 09:00) genera el
resumen con R1-14B local (0 cloud). Primer informe 100% local verificado
10-ago-2026.

**Pitfalls del router (verificado 09-10-ago):**
- El router necesita el modelo cargado en el :1234, NO en la GUI de LM
  Studio (la GUI usa un backend interno con API key). Si `lms load` muere
  al ~49% es VRAM: matar el backend llama-server de la GUI primero.
- R1 responde en `reasoning_content`; pedir "NO razones en voz alta".
- R1 envuelve JSON en ```json; limpiar en el consumidor.
- Qwen 35B A3B probado 10-ago y DESCARTADO (2.7-9 tok/s, CPU debil para
  MoE). R1-14B sigue de referencia.

- El PATH del planificador NO incluye `~/.lmstudio/bin`: `lms` pelado no
  existe (`command -v lms` rc=1) y el fallo se tragaba a `/dev/null`. El router
  ya autocarga ese PATH y reporta el error real (commit `46a5214`, 13-oct-2026).

**Arranque del motor local BAJO DEMANDA (13-oct-2026, commit `b806b7c`).** Si
`:1234` esta caido, el router no se planta: asegura el servidor con
`lms server start` (sin GUI), con lock, timeout doble y el exito acreditado en el
puerto. Medido: `:1234` caido -> servidor arriba en 2 s -> gpt-oss-20b cargado ->
respuesta en 39 s, sin la app abierta. El bug que esto destapo: `lms server start`
lanza la app DESPRENDIDA, y esa app heredaba el fd del lock (sin CLOEXEC): el lock
quedaba retenido para siempre y el arranque siguiente moria esperando 60 s a un
proceso que ya no existia. El arranque va en subshell con el fd 9 cerrado.

**Criterio cloud-first SIN trinquete (13-oct-2026, commit `07cb051`).** Antes el
criterio contaba toda fila con `local_ok` falso — incluidas las decisiones
`cloud_directo`, que no son fallos del motor — y sin ventana temporal: un fallo de
codigo (`lms` fuera del PATH, RULE-021) dejaba el tipo en cloud PARA SIEMPRE,
porque sin nuevos intentos locales nunca llegaba un ok que lo reseteara. Ahora
solo cuentan los intentos locales REALES (`intento_local`) y vigentes:
`VENTANA_DIAS = 7` y un corte declarado, humano y reversible,
`INVALIDAR_ANTES_DE = 2026-10-13T07:37+02:00` (la hora del arreglo del PATH).
`tasa_fallo(tipo, min_muestras, vigente=False)` expone el nuevo modo.

**Gate de fidelidad de DATOS del camino `batch-json` (13-oct-2026).** El
verifier del orquestador miraba solo el FORMATO: el 13-oct dio por bueno un JSON
con `gpu_mem_usado_mb: 95.61`, cifra que no existe en la fuente (el informe dice
`9561`), y ese contenido alimentaba el artefacto de produccion. Desde el commit
`8182799` el verifier recibe tambien la fuente (`verifier(tipo, salida,
fuente)`) y una salida `batch-json` que pase el formato se cruza ademas contra el
prompt con `tools/verificador_fidelidad.py` (numeros/IDs/fechas, determinista,
0 LLM): sin respaldo -> `cifras_sin_respaldo` y no pasa. Fail-closed: si el
verificador no se puede cargar, tampoco pasa (RULE-021). Probado contra las dos
salidas reales de hoy (`95.61` y `123` -> bloqueadas) y contra un control
correcto (`PASA`). Limite medido: el gate es numerico, no semantico — copiar una
cifra REAL en el campo equivocado. **[Corregido en v1.6.27]** Aquel caso estaba mal leido: el crudo del informe (`nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu`) trae, en ese orden, usado, total, uso % y temperatura; `9561` era la memoria USADA (libre = 12282 - 9561 = 2721) y el cloud copio bien. El «disponible 9561» y los «38 procesos en cola» los escribia el resumen del propio informe (LLM local): la fuente se contradecia a si misma.

**Arreglo en el INSTRUMENTO (v1.6.27), no en el prompt.** `tools/informe-diario-local.sh` imprime la leyenda del orden de los numeros en el bloque `## GPU`, y el prompt del resumen tiene prohibido renombrar o inventar datos. Medido con una copia del instrumento en `/tmp` (sin tocar el informe de produccion) y el prompt real de `04-operations/metrics/batch/cola.jsonl`: el extractor local devuelve `gpu_mem_usado_mb: 1560` y `gpu_temp_c: 44` (antes `95.61`, `123` y `null`) -> `FIDELIDAD: (True, 'fidelidad_ok')` y `verifier: (True, 'json_valido')`, sin escalar a cloud. **Pendiente, no oculto**: la prosa del resumen (la corrida de prueba la degrado: motor ocupado).

---

<a name="capitulo-4"></a>
# CAPITULO 4 — HERMES AGENT: EL CEREBRO

## 4.1 Que es

Hermes Agent (de Nous Research) es el agente que ejecuta las instrucciones
del laboratorio. Es quien te lee, decide, ejecuta y documenta. Vive en
`~/.hermes/` y se usa desde CLI, Telegram (gateway) o cron.

## 4.2 Componentes principales

| Componente | Ruta | Funcion |
|------------|------|---------|
| config.yaml | ~/.hermes/config.yaml | Configuracion (modelo, proveedor, gateway) |
| Skills | ~/.hermes/skills/ | Conocimiento procedimental (185 skills, 04-sep-2026) |
| Memoria | ~/.hermes/memories/ | Datos persistentes entre sesiones |
| Sesiones | ~/.hermes/ (DB) | Historial de conversaciones (session_search) |
| Cron | ~/.hermes/cron/ | Tareas programadas |
| Scripts | ~/.hermes/scripts/ | shared-events, session-state, consolidador... |

## 4.3 Modelo principal (configuracion)

```yaml
model:
  provider: deepseek
  default: deepseek-v4-flash
```

- Proveedor principal: DeepSeek (cloud) — modelo deepseek-v4-flash
- `deepseek-chat` es alias legacy retirado desde 2026-07-24
- El enrutamiento automatico (ai-router) puede cambiar esto segun
  politicas (ver capitulo 7)

## 4.4 Skills del lab (las ~20 nucleo)

| Skill | Para que |
|-------|----------|
| ai-architecture | Gobierno: QUE debe ocurrir (principios, roles) |
| ai-router | Implementacion: COMO ocurre (enrutamiento, scripts) |
| lpa | Programa de investigacion (epistemologia E0-E4, KAP) |
| lm-studio | Motor de inferencia local |
| local-rag | RAG semantico (BGE-M3 + LanceDB) |
| n8n-admin | Analisis y optimizacion de workflows n8n |
| hermes-expert | Operacion de Hermes (config, modelo, cron) |
| hermes-salud | Autodiagnostico estructural y funcional |
| diagnostico-stack-local | Diagnostico solo lectura del stack Docker |
| cross-session-awareness | Contexto entre sesiones (CLI, Telegram) |
| contexto-multimodal | Protocolo de deteccion de imagenes |
| combined-mode | Modo combinado cloud+local |
| thinking-patterns | Patrones de razonamiento y procesos cognitivos |
| perfume-ia | Proyecto Perfume IA |
| forense-digital | Peritaje informatico (correo, casos judiciales) |
| telegram-inbox | Inbox de captura via Telegram |
| prompt-engineering | Creacion y optimizacion de prompts |
| gate-veracidad | Gate obligatorio de veracidad (16-ago): etiquetar outputs factuales [VERIFICADO]/[ALCANCE INTERNO]/[NO VERIFICADO]/[REVISAR]; verificar contra fuente antes de emitir |
| revisar-decisiones | Revisar DECISIONES de cambios grandes de codigo, no el diff (16-ago, patron David Ondrej); complementa SVP-diff y gate de veracidad |
| recursos-gratuitos-desempleados | Recursos GRATUITOS verificados para desempleados (12: Lanbide, SEPE, BBK Bootcamps, Talento 45+, Cámaras...) — solo fuente oficial, excluye lo que exija "en activo" |
| least-privilege-lab | Política de mínimo privilegio (16-ago): delegate_task con toolsets mínimos, cron con agente → enabled_toolsets obligatorio, deny-by-default, credenciales [REDACTED], MCP futuro |
| empleo-publico-erandio | Empleo publico del Ayuntamiento de Erandio: OPE, bolsas de trabajo, planes de empleo y canal BOB |

## 4.5 Memoria del agente

La memoria es informacion persistente inyectada en cada turno:

- **Perfil de usuario**: quien eres (Joseba, 55, Erandio, ex-Indra/Minsait,
  Master IA 2026), tus preferencias (tono directo, datos reales, nada de
  respuestas prefabricadas)
- **Notas del agente**: entorno (driver 595.84, rutas), convenciones,
  lecciones aprendidas

**Regla:** los hechos que cambiaran en una semana NO van a memoria.
Los procedimientos reutilizables van a skills.

## 4.6 Cron jobs activos (04-sep-2026)

40 jobs registrados en total (38 activos programados + 2 one-shot completados/deshabilitados). Los principales:
**Medido el 07-oct-2026:** 46 jobs en el store y los 46 habilitados (12 con agente + 34 script puro `no_agent`); la tabla de abajo es la foto del 04-sep y se completa con lo nuevo.
**Medido el 09-oct-2026:** 48 jobs en el store y los 48 habilitados (13 con agente + 35 script puro `no_agent`).

| Job | Horario | Funcion |
|-----|---------|---------|
| auditoria-hermes | cada 1440m (20:00) | Diagnostico de Hermes (hermes-diag.sh) |
| informe-diario-joko-lab | 9:00 | Informe ejecutivo del estado del lab — script informe-diario-local.sh (cron lista model=deepseek-v4-flash; mecanismo interno del script no verificado en esta sesión) |
| Hermes version watchdog | cada 1440m | Vigila versiones nuevas de Hermes (script puro) |
| Founderz Watchdog | cada 10m | Vigila algo del master Founderz |
| Recordatorio investigacion | 19:00 | Recuerda temas pendientes de investigar (**no_agent** desde 10-ago) |
| telegram-watchdog | cada 15m | Comprueba que el gateway de Telegram vive |
| Recordatorio pendientes | 8:00 | Recordatorio del roadmap activo (**no_agent** desde 10-ago; antes "RAG" con 3 tareas, completadas 09-ago) |
| session-heartbeat-cli | cada 10m | Escribe estado de sesion CLI |
| rag-reindex-daily | 8:00 | Re-indexa RAG en LanceDB (BGE-M3) |
| rag-reindex-catchup | cada 60m | Respaldo si el reindex diario fallo |
| consolidador-sesiones | 22:30 | Exporta sesiones a metrics + resumen-dia |
| backup-joko-lab-diario | 22:15 | Backup automatizado de joko-lab (script puro) |
| Recordatorio datos sueno | 9:00 | Recordatorio diario de medicion (Biohacking, **no_agent** desde 10-ago) |
| prediction-log-watchdog | 22:05 | Avisa de predicciones PRED vencidas sin revisar |
| telemetria-observer-diario | 22:00 | Telemetria diaria F1/F2/F2.5 (observer + evidence) |
| lab-health-watchdog | 8:30 | Salud de Joko Lab; silencioso si todo bien (Telegram) |
| l2-proposer-daily | 8:45 | Ejecuta tools/proposer.py; avisa si hay propuestas nuevas |
| perfumes-biblioteca-revision | 9:00 dia 1 | Revision mensual de la biblioteca de perfumes inaccesibles |
| bolsa-juego-diario | 22:30 L-V | Pasada diaria del juego de bolsa (Experimento 002) |
| nvidia-suspend-solucion-watchdog | 9:00 lunes | Vigila el fix de suspend de NVIDIA |
| registrar-hel-diario (EXP-HEL-001) | 22:35 | Registro automatico diario del baseline HEL (no_agent, creado 10-ago) |
| hel-registro-watchdog | 22:45 | Vigila que el registro HEL del dia exista; avisa por Telegram si falta (no_agent, creado 10-ago) |
| kel-revalidacion-diaria | 22:12 | Watchdog KEL: avisa de KOs vencidos o proximos a next_review (solo lectura) |
| prospective-watchdog | 9:30 | Prospective Memory: avisa cuando hay intenciones con deadline cercano (no_agent) |
| watchdog-salud-sistema | cada 4h | Vigila swap, zombies, RAM, uptime (no_agent; silencioso si OK) |
| detectar-sin-uso-semanal | lunes 10:00 | Detecta cron muertos, scripts huerfanos, skills sin uso (script puro) |
| descargador-modelos-inactivos | cada 30m | Descarga modelos de LM Studio con 30+ min sin inferencia (libera VRAM) |
| vigilar-canales-ig | 9:00 | Vigila canales Instagram de referencia (skill instagram-monitor) |
| vigilar-canales-yt | 9:15 | Vigila canales YouTube de referencia A4 (script vigilar-yt.sh) |
| vigilar-yt-outliers | 9:30 | Deteccion de outliers en canales YouTube |
| vigilar-canales-tg | 9:45 | Vigila canales PUBLICOS de Telegram por su vista web t.me/s (script vigilar-tg.sh; creado 09-oct-2026) |
| detector-perdida-contexto | cada 240m | Vigila sintomas de perdida de contexto en sesiones Hermes |
| watchdog-control-cli | cada 2m | Watchdog de control del CLI |
| monitor-precios-ia-semanal | lunes 9:00 | Monitor semanal de precios/calidad de proveedores IA (31-ago delivery error, revisar) |
| investigacion-modelos-locales-semanal | lunes 10:00 | Investigacion semanal de modelos locales (31-ago delivery error, revisar) |
| auto-mejora-semanal-hermes | lunes 13:00 | Sesion semanal de auto-mejora del lab (31-ago delivery error, revisar) |
| lpa-revision-incidentes-semanal | viernes 11:00 | Ciclo semanal LPA de revision de fallos/incidentes (skill lpa) |
| backup-hermes-diario | 22:20 | Backup del estado critico de ~/.hermes (config, memories, skills) |
| scan-empleo-diario | 19:00 | Scan de ofertas de empleo con skill seguimiento-empleo (ACTIVO; 04-sep last_status=error, revisar) |
| guardia-idioma | cada 10m | Mide el idioma real del agente en `state.db` y avisa si responde en otro idioma (script puro, silencioso; creado 07-oct) - ver 4.10 |

**Como se auditan estos crons (13-oct-2026).** `tools/auditar_crons.py` (305 l.,
solo lectura) audita en **3 capas**: los jobs, los informes que producen y las
entregas. Existe porque los dos vigilantes previos —`watchdog-informes-cron.py` y
`barrido-informes-fallidos.py`— comparten un punto ciego MEDIDO: detectan el fallo
solo por la cabecera `(FAILED)` o la cola `## Error`, y el formato de fallo actual
de Hermes es `**Status:** script failed` (informe real:
`~/.hermes/cron/output/da39a2148b34/2026-10-12_08-05-44.md`). Tests:
`tests/test_auditar_crons.py` (251 l.).

**Salida de la telemetria diaria.** El cron `telemetria-observer-diario` (22:00,
script `observer-daily.sh`) escribe en `04-operations/metrics/telemetria/`: un
`YYYY-MM-DD.json` + un `YYYY-MM-DD.md` por dia (ultimo medido: `2026-10-13`).

## 4.7 Gateway de Telegram

Permite hablar con Hermes desde el movil:

- Canal de entrada: Telegram (gateway)
- El channel_prompt inyecta shared-events + session_search antes de responder
- Watchdog cada 15 min comprueba que sigue vivo
- Telegram puede procesar imagenes → las enruta a LM Studio (vision)

**Pitfall:** tras cambiar config del gateway hay que reiniciarlo desde
otra shell (`hermes gateway restart`), nunca desde dentro del gateway.

## 4.7b Integracion Gemini API (06-ago-2026)

Ademas de DeepSeek (cloud) y los modelos locales, el lab tiene una API key
de Google AI Studio (proyecto "Hermes Agent", creada 09-jul-2026) para usar
Gemini programaticamente (vision fina, analisis de capturas, etc.):

- Key en `~/.hermes/.env` → `GOOGLE_API_KEY=<ENV:~/.hermes/.env>` (el valor NO se documenta en la guia; rotada 07-ago).
- Modelo actual usable: `gemini-3-flash-preview` (gemini-2.5/1.5 dan 404 a
  usuarios nuevos).
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/<modelo>:generateContent`
- La suscripcion Google AI Pro (~20€/mes) NO da creditos de API — la key es
  de AI Studio (free tier + pago por uso). Detalle en skill `google-ai-pro`.
- Uso real verificado: analisis de capturas de formato con especificacion
  tecnica fina (paleta hex, tipografias, espiral) para slides del TFM.

## 4.8 Reglas de seguridad del agente (importantes)

1. NO ejecutar comandos automaticamente — proponer, esperar salida real
2. n8n es zona protegida — no reiniciar/parar/modificar sin confirmacion
3. No inventar datos — si no aparece en la salida, decir "no aparece"
4. Comandos de solo lectura primero (ps, ss, df, free, nvidia-smi, curl)
5. `sudo` solo con autorizacion explicita
6. No borrar/mover/modificar archivos sin autorizacion
7. Formato de diagnostico: salida cruda + resumen en espanol

## 4.9 Autodiagnostico: hermes-salud

Skill `hermes-salud` — autodiagnostico estructural y funcional del lab.
Ejecuta una revision sistematica de los subsistemas y reporta el estado.

---

## 4.10 Guardia de idioma del agente (07-oct-2026)

Hermes puede derivar de idioma sin avisar. Medido: **8 respuestas salieron en chino**, todas del mismo modelo (`deepseek-v4-flash`), la ultima el 07-oct (id 212304, 574 chars). La guardia **no pregunta al modelo: MIDE** el texto ya emitido.

- **Script:** `~/.hermes/scripts/guardia-idioma.py` (330 lín. / 13.116 B, md5 `c1560aaacf13aa898a3923fd3bd3a7b2`)
- **Cron:** `7c3fe0c3fc71` - cada 10 min, `no_agent` (script puro), `deliver=origin`; **silencioso** si no hay nada que avisar
- **Que mide:** sobre `~/.hermes/state.db` (solo lectura) los mensajes `role='assistant'` con contenido y activos, a partir de un cursor (`ultimo_id`)
- **2 señales:** (1) script no latino **sostenido** (CJK, kana, hangul, cirilico, arabe, devanagari, thai, hebreo; **griego EXCLUIDO**); (2) prosa larga sin marcadores en español y con muchos en inglés
- **Detalles que importan:** `no` esta FUERA de la lista de palabras españolas (lo usaban las frases en inglés) · el aviso **recorta a latino** para no repetir el texto raro · la hora se lee en **Europe/Madrid**, no en la del sistema
- **Cursor:** `~/.hermes/scripts/.cache-guardia-idioma.json` (`checks`, `ultimo_id`, `fallos`)
- **Precision medida (07-oct):** **57.910 mensajes** revisados -> **8 alertas, 0 falsos positivos**

<a name="capitulo-5"></a>
# CAPITULO 5 — SISTEMAS DE CONOCIMIENTO (LPA Y KNOWLEDGE OBJECTS)

## 5.1 Que es LPA

**LPA (Living Product Architecture)** es el programa de investigacion del
lab. Definicion oficial:

> LPA es un sistema para construir sistemas complejos sin perder coherencia
> cuando intervienen humanos, IA y el paso del tiempo.

No es una metodologia ni un framework. Es una **hipotesis fuerte [E2]**:
los patrones de LPA emergen naturalmente cuando humanos e IA colaboran en
sistemas que deben preservar identidad mientras evolucionan.

**Los tres agentes de cambio:** Humanos (decisiones, sesgos), IA
(automatizacion, escala, deriva), Tiempo (obsolescencia, evolucion).
LPA existe porque estos tres combinados tienden a degenerar sistemas
complejos.

## 5.2 Niveles de evidencia E0-E4

Todo conocimiento del lab pasa por niveles de evidencia:

| Nivel | Definicion | Requisito | Derechos |
|-------|-----------|-----------|----------|
| E0 | Observacion unica | 1 experimento, 1 dominio | Ninguno |
| E1 | Patron | 2+ experimentos, contextos distintos | Mencionable |
| E2 | Hipotesis | 2+ experimentos + falsificacion fallida | Usable como guia |
| E3 | Validacion | 3+ dominios distintos + falsificacion fallida | Enseñable |
| E4 | Principio | 5+ dominios, 3+ categorias, 6 meses sin contraejemplos | Fundacional |

**E∅ — Revocado:** afirmacion que fue E1+ y fue falseada. No se elimina,
se marca con fecha y experimento.

**Regla de oro:** la evidencia va siempre por delante de la metodologia.
Un experimento no confirma: intenta falsear.

## 5.3 El proceso epistemologico

```
Observacion (E0) → Patron (E1) → Hipotesis (E2) → Validacion (E3) → Principio (E4)
```

Entre E3 y E4 existe el **Candidate Principle**: un estado intermedio donde
la hipotesis validada acumula evidencia longitudinal. La mayoria nunca
alcanzan E4 — esa tasa de descarte es el mecanismo de defensa del sistema.

## 5.4 Knowledge Objects (los "KOs")

Desde julio 2026, las decisiones/reglas/politicas del lab son **entidades
YAML con ciclo de vida** en `01-knowledge/objects/`:

| Tipo | Significado | Ejemplos reales |
|------|-------------|-----------------|
| DEC | Decision | DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, DEC-GAIPRO-001 |
| RULE | Regla activa derivada de DEC | RULE-001..021 |
| POLICY | Restriccion global | POLICY-001, POLICY-002, POLICY-003 |
| PRED | Prediccion con veredicto | PRED-001, PRED-002 (anti-Goodhart: quien predice no resuelve) |
| PATTERN | Patron de conocimiento | PATTERN-001 |
| OBS | Observacion factual | OBS-005/006/007 (telemetria F2) |
| HYP | Hipotesis | HYP-001 |

Total a 07-ago-2026: **21 KOs** en `01-knowledge/objects/` (22 archivos
incluyendo PRED-template.yaml), todos con
`expires`/`next_review`/`superseded_by` (KEL). Total a **13-oct-2026**: **34 KOs** en `01-knowledge/objects/` (35 archivos `*.yaml`, plantillas incluidas), con **21 RULE** activas (RULE-001..021).

Ultimas reglas (corregido 29-sep-2026):
RULE-017 (canales de contenido no confiables, 6-sep) y RULE-018 (un proceso de fondo no
escribe skills sin OK, 20-sep) — antes esta linea citaba RULE-008/009 (agosto).

(**Medido 29-sep-2026:** 53 ficheros en `01-knowledge/objects/` segun `ls 01-knowledge/objects/ | wc -l`. Las cifras de recuento se citan con su instrumento, porque caducan en el mismo commit que las escribe.)
Desde 07-ago, `legacy_fields.canal` distingue reglas del motor (engine:
RULE-001..004, 009) de reglas de procedimiento (no_engine: RULE-005..008,
supervisadas via JL/PIL, no via task_type del Activation Engine) — sync de
telemetria tras validar el instrumento.

**Esquema de un KO (ejemplo real DEC-002):**

```yaml
id: DEC-002
type: DEC
status: activo
created: '2026-07-28'
last_validated: '2026-07-31'
next_review: '2026-10-26'
expires: '2027-01-24'
confidence_label: NO_EVALUADA
evidence:
- 'EXP-20260728-003: Superior en razonamiento logico multi-paso'
domain: ai-architecture
scope: todo_joko_lab
monitoring: { metric, baseline, current, last_checked }
history: [created, migrated_to_ko, validated]
body: "DeepSeek R1 destilado en Qwen 14B para tareas de razonamiento paso a paso. Límite de tokens: max_tokens 2048 (nunca menos)."
legacy_fields: { modelos_afectados, params, nota }
```

**Ejemplo real RULE-001 (regla activa):**

```yaml
id: RULE-001
type: RULE
confidence: 0.94
confidence_label: ALTA
dependencies: [DEC-003]
body: Usar Gemma 4 para tareas creativas
legacy_fields:
  condicion: { tipo_tarea: [creatividad, brainstorming, poema, relato...] }
  accion: { modelo: google/gemma-4-12b-qat, proveedor: lmstudio,
            params: { temperature: 0.7, max_tokens: 2048 } }
  prioridad: 90
  activa: true
```

**Campos clave del ciclo de vida:**
- `expires` — cuando caduca la validez
- `next_review` — cuando hay que revisarlo
- `last_validated` — ultima validacion
- `confidence_label` — NO_EVALUADA / BAJA / MEDIA / ALTA
- `dependencies` — de que otros KOs depende
- `contradicts` — que KO contradice
- `superseded_by` — que KO lo sustituye

## 5.5 Knowledge Health Auditor (salud del conocimiento)

Script: `~/joko-lab/tools/knowledge_health.py` (solo lectura)

- Metricas global 0-100 con 4 dimensiones
- Historial JSONL con tendencias (`--trend`)
- **Progresion real: 31 → 43 → 67 → 70 → 76 → 88/100**
- Mide SOLO los 10 Knowledge Objects de `01-knowledge/objects/`
- NO mide los ~96 docs de conocimiento del resto del lab

**Integridad referencial (07-ago-2026):** `tools/verificar_fk_kos.py` (solo
lectura) detecta la clase de defecto `referencia_ko_no_verificada` (un ID de
KO citado que no existe). Baseline 07-ago: 1 mencion historica en KOs (DEC-004/
RULE-CONF-001, nota de correccion) y 25 en docs (mayoria de diseno/historicas;
OBS-003/004, OBS-021 y HYP-002 candidatas a rotas reales). Ficha EVF en
`research/fk-integridad-referencial-evf.md`. El gate NO se modifica hasta la
EXP (ciclo EVF).

**Importante (diferencia):** un Health Score alto NO implica que la
estructura documental este sana. Auditoria estructural complementaria:
`scripts/audit-docs-structure.py` (frontmatter, H1, enlaces).

## 5.6 KAP — Knowledge Assimilation Pipeline (M-001)

Procedimiento para convertir cualquier fuente externa (video, articulo,
libro) en conocimiento operativo. Tres fases:

1. **Fase A — Extraccion** (Hermes)
2. **Fase B — Revision adversarial** (modelo externo: ChatGPT/Claude)
3. **Fase C — Asimilacion** (que cambia en Joko Lab)

**6 preguntas obligatorias (en orden):**
1. ¿Ya lo sabiamos?
2. ¿Cambia realmente como trabaja Joko Lab?
3. ¿Acelera la obtencion de resultados fisicos?
4. ¿Pertenece al proyecto o pertenece a LPA?
5. ¿Que experimento concreto podremos hacer manana gracias a esta idea?
6. ¿Que problema estructural de Joko Lab confirma esta fuente?

**Regla de oro:** ningun recurso externo entra por ser interesante. Solo
entra si cambia la forma en que el laboratorio trabaja, aprende o construye.

Prompt Fase B: `lpa/meta/M-001-prompts-v5.md` (10 pasos, 3 reglas).

## 5.7 KVC — Knowledge Validation Cycle (CP-003)

```
Observacion → Analisis → Critica adversarial → Falsacion → DEC → Aplicacion
→ Monitorizacion (4 dimensiones) → ¿Mejoro? → Si: conservar / No: reabrir
```

**Principio emergente:** la unidad de progreso no es el componente, es la
decision validada. Una decision sin monitorizacion no es una decision —
es una apuesta.

**Filtro anti-DEC-inflacion:** ¿Esta decision cambia realmente el
comportamiento futuro? Si NO → no es DEC, es OBS (observacion).

## 5.8 KEL — Knowledge Evolution Loop

Maquina de estados del conocimiento:

```
OBS → HIPOTESIS → EXP → EVIDENCIA → DEC → MONITORIZACION
→ REVALIDACION → (conservar | retirar)
```

**KEL operativo (07-ago-2026):** el disparador temporal de la REVALIDACION es
el watchdog diario `tools/revalidar_kos.py` (cron 22:12, `kel-revalidacion-diaria`,
entrega a Telegram). Escanea `01-knowledge/objects/`, clasifica los KOs
activos (no superseded) por next_review/expires y avisa de: vencidos (revisar
ya), proximos (<= 7 dias antes de next_review) y activos sin fechas (deuda).
NO modifica KOs: es solo lectura; la revalidacion en si (mantener, reabrir,
degradar, retirar) la hace el agente/humano con KVC en sesion cuando llega el
aviso. Mismo patron que el watchdog de predicciones (escanear_predicciones.py).

Propiedad clave: incorpora el **olvido** como operacion de primer orden.
Un sistema que solo acumula conocimiento se degrada.

## 5.9 Knowledge Pruning (poda)

7 operaciones: VALIDAR, DEGRADAR, RETIRAR, DIVIDIR, FUSIONAR, VERSIONAR,
ARCHIVAR. 5 fases de implementacion progresiva (no saltar fases).

Regla: un sistema que solo anade DEC/EXP/OBS sin retirar las obsoletas
se degrada por acumulacion. Ejecutar `knowledge_health.py` periodicamente.
KHI < 50 requiere intervencion.

## 5.10 Evidence Contract (contrato de evidencia)

Umbrales verificables para promocionar EXP → DEC. Convierte el paso de
"juicio" a "contrato verificable". Verificador: `tools/evidence_contract.py`
(solo lectura, alias EN/ES).

Estado real (31-jul-2026): 0/9 KOs cumplen = deuda senalada.
NO integrar en decision_engine.py (dominio distinto).

## 5.11 Normas constitucionales (JL)

| Norma | Proposito |
|-------|-----------|
| JL-001 | Modo Mentor Permanente — Hermes aumenta tu capacidad metodologica |
| JL-002 | Deteccion Activa de Oportunidades LPA |
| JL-003 | Cada conversacion mejora el laboratorio |
| JL-004 | Consolidacion del conocimiento (5 niveles: recordar→enseñar) |
| JL-005 | Umbral de herramientas — no por tendencias, solo por problemas objetivos |
| JL-007 | Capacidades, no modelos (taxonomia v2) |
| JL-008 | MCP (Model Capability Profile) v3 |
| JL-009 | Misiones, no modelos individuales |
| JL-010 | Toda evaluacion enriquece LPA |
| JL-011 | El flujo del conocimiento tiene prioridad sobre la optimizacion |
| JL-012 | El AI Router es un mecanismo interno, no un comando |
| JL-013 | La guia del laboratorio se actualiza ante cada cambio estructural |
| JL-014 | Copia de seguridad antes de cambios grandes (creada 03-ago) |

## 5.12 Estructura de archivos del conocimiento

```
/home/jokoalmi/joko-lab/
├── 01-knowledge/
│   ├── objects/          ← Knowledge Objects YAML (DEC, RULE, POLICY)
│   ├── decisions/        ← decisiones legacy (migradas a objects/)
│   ├── policies/         ← politicas legacy
│   ├── rules/            ← reglas legacy
│   ├── hypotheses/       ← hipotesis (HYP-001...)
│   ├── experiments/      ← experimentos (EXP-...)
│   ├── observations/     ← observaciones
│   ├── patterns/         ← patrones y anti-patrones
│   ├── models/           ← fichas de modelos
│   ├── benchmarks/       ← benchmarks
│   ├── task_keywords.yaml← fuente unica de keywords por tipo de tarea
│   └── prompt-compiler/  ← compilador de prompts
├── lpa/
│   ├── constitucion/     ← normas-jl.md
│   ├── contracts/        ← knowledge-object-schema, evidence-contract...
│   ├── procedures/       ← knowledge-pruning...
│   ├── meta/             ← M-001 (KAP), como aprende el lab
│   ├── pattern-incubator/← maduracion E0→E1 (CP-001..005)
│   ├── experiments/      ← plantilla y experimentos
│   └── KNOWN.md, HYPOTHESIS.md, UNKNOWN.md, EPISTEMOLOGY.md
├── tools/                ← scripts (decision_engine, indexer, search...)
├── verification/         ← bank.yaml + comparador (verificacion determinista)
├── 04-operations/
│   ├── backlogs/         ← pendientes priorizados
│   ├── changelog/        ← registro de cambios
│   ├── incidents/        ← incidencias
│   ├── metrics/          ← knowledge_health.jsonl, sesiones/
│   └── reports/          ← informes de cierre
└── 02-infrastructure/
    ├── inicio/           ← inicio.sh + checks + estado-inicial.json
    ├── fin/              ← fin.sh + estado-final.json
    ├── recovery/         ← rescue.sh + backups + procedures
    └── services/         ← CONTRACT.md + api.py (Runtime)
```

## 5.13 Principios eticos del lab (POLICY-003)

**Norma constitucional (nivel Constitución, decisión del fundador 04-ago-2026).**
Origen: Modulo 9 Founderz (M9-01 "Ley y etica en la IA: Alineamiento y peligros")
+ declaracion explicita de Joseba. Implementada como **POLICY-003** en
`01-knowledge/objects/POLICY-003.yaml`.

Los 4 componentes del alineamiento (Stuart Russell), adoptados como marco:

| # | Principio | Significado operativo en el lab |
|---|-----------|--------------------------------|
| 1 | Alineacion con valores humanos | Dignidad, autonomia, justicia, derechos humanos. No optimizar solo eficiencia. |
| 2 | Beneficio social explicito | Todo producto debe mejorar bienestar colectivo, no solo generar output. |
| 3 | Minimizacion de danos | Anticipar riesgos (sesgos, alucinaciones, mal uso) y poner salvaguardas. |
| 4 | Diseno guiado por valores desde el inicio | La etica se incorpora al disenar, no como parche posterior. |

**Acciones obligatorias cuando se trabaja en un producto del lab**
(Perfume IA, Forense Digital, SkillBridge o futuros):

1. Documentar impacto etico de la funcionalidad antes de implementarla.
2. Preferir procesamiento local (datos que no salen del equipo).
3. Permitir auditoria y explicabilidad (que una decision se pueda rastrear).
4. Detectar y documentar sesgos reales (RAG bge-m3, automatizaciones n8n).

**Checklist de deteccion de sesgos (M9-02/M9-03, 04-ago-2026):** al auditar
un producto del lab, revisar las 5 fases del ciclo de vida del sesgo:

| Fase | Pregunta de auditoria |
|------|----------------------|
| Definicion del problema/metricas | Que significa "exito"? Solo eficiencia o tambien justicia distributiva? |
| Recopilacion de datos | Los datos historicos contienen discriminacion sistemica sin depurar? |
| Entrenamiento/ajuste | Que variables se incluyen y ponderan? Favorecen a algun grupo? |
| Implementacion/uso | La integracion en procesos reales introduce sesgos nuevos? |
| Retroalimentacion | El sistema se retroalimenta de sus propios resultados sin supervision? |

Mitigacion (5 pasos): definir contexto/riesgos → auditar datos → disenar con
criterios de equidad → evaluar desagregada por grupos (falsos positivos/
negativos en vulnerables) → involucrar comunidades. Regla: NO corregir sesgos
"a ciegas" (corregir uno puede introducir otro); documentar, medir por grupos
y gestionar compromisos (equidad/precision/impacto).

**Metodos de auditoria de sesgos (M9-05, 04-ago-2026):**
- **Analisis contrafactico**: cambiar una variable sensible (edad, genero) y
  ver si la decision cambia cuando no deberia. Para SkillBridge: cambiar la
  edad del candidato y comprobar que la decision no varia injustamente.
- **Inferencia causal**: distinguir correlaciones espurias de causalidad real.
- **Auditorias algoritmicas**: internas/externas, documentar riesgos.
- **Pruebas de equidad estadistica**: igualdad de oportunidades, paridad
  demografica, tasa de falsos positivos/negativos por grupo.

**4 rasgos de una IA explicable y auditable**: visibilidad del proceso interno
(que datos influyen en cada decision), documentacion completa del modelo
(datos, supuestos, limitaciones, contextos inadecuados), metricas de equidad
integradas, facilidad de auditoria externa. El lab ya cubre 3 de 4 con
confidence.trace(), Knowledge Objects y verificacion determinista; pendiente:
metricas de equidad integradas.

**Marco de IA responsable (M9-10, 04-ago-2026):** antes de construir o
desplegar cualquier funcionalidad de un producto, responder 3 preguntas
sistematicamente:
1. Que podria salir mal? (escenarios de fallo: errores, usos indebidos, datos
   sesgados, comportamientos no previstos)
2. Quien podria ser perjudicado? (3 niveles: individuo/usuario directo,
   personas cercanas y transeuntes, sociedad en su conjunto)
3. Como prevenir o mitigar el dano? (salvaguardas tecnicas y organizativas,
   revision humana, monitoreo post-despliegue)

Regla adicional: preguntarse si el sistema deberia construirse — NO construir
si existe alternativa no automatizada con menos riesgos, si el dano potencial
es grave e irreversible, si los beneficios se concentran en pocos y los
riesgos en vulnerables, o si facilita usos maliciosos.

**Relacion con otras normas:** POLICY-003 complementa POLICY-002 (privacidad):
002 protege los datos, 003 protege los valores. No crea RULEs nuevas hasta
que exista evidencia de un caso real (principio de orden: evidencia primero).

**Caso de referencia:** SkillBridge (M7, AI-THINK) combate el sesgo de edad en
seleccion (+50): la IA en contratacion debe alinearse con equidad desde el
diseno, no corregirse a posteriori. Es el caso practico que valida esta norma.

---

<a name="capitulo-6"></a>
# CAPITULO 6 — RAG LOCAL (BGE-M3 + LANCEDB)

## 6.1 Que es el RAG del lab

RAG (Retrieval-Augmented Generation) = generar respuestas usando
informacion recuperada de una base de conocimiento, en vez de solo el
conocimiento interno del modelo. 100% local, sin cloud.

**Caso de uso principal:** cuando preguntas algo del lab, Hermes busca en
la base vectorial (LanceDB) los documentos relevantes (sesiones, decisiones,
experimentos) y usa ese contexto para responder con datos reales.

## 6.2 Componentes del stack

| Componente | Que es | Detalle |
|-----------|--------|---------|
| BGE-M3 | Modelo de embeddings multilingue | 1024 dimensiones, espanol nativo |
| LanceDB | Base vectorial | daemonless, zero-copy (Arrow) |
| indexer.py | Indexa documentos .md y .yaml | chunks 1000 tokens, solapamiento 150, **v2 INCREMENTAL (5-ago)**: hash sha256 + sidecar → solo re-embebe cambios | 
| search.py | Busqueda HIBRIDA | **FTS + vectorial + RRF (5-ago)**, BGE-M3 + reranker, filtros --type/--status | 
| context_builder.py | Inyecta contexto al LLM | detecta tipo + busca + formatea ESTRUCTURADO (desde 2-ago) |
| context_builder_estructurado.py | Variante de medicion P1 | misma logica, formateo compacto (referencia) |
| medir_p1.py | Medidor P1 (4 dimensiones) | tokens, latencia, precision, cobertura |
| knowledge_resolver.py | Sintetiza conocimiento | hechos, conflictos, decisiones, confianza |
| lmstudio_embeddings.py | Embeddings via LM Studio API | evita competencia por VRAM |
| reranker_daemon.py | Daemon persistente del reranker | carga CrossEncoder UNA vez, sirve /rerank en :8765, **--max-seq 256 + Nice=-10 (5-ago)** |

## 6.3 Flujo completo

```
Documentos .md/.yaml → indexer.py v2 (hash incremental) → embeddings BGE-M3 → LanceDB
                                                          ↓
Pregunta → search.py (HIBRIDA: FTS + vectorial + RRF → filtros type/status → reranker)
              ↓
context_builder.py (contexto inyectado al prompt + índice OKF vigencia)
              ↓
knowledge_resolver.py (conocimiento estructurado)
              ↓
LLM responde con contexto real
```

> **NOTA (04-oct-2026):** este diagrama describe la CADENA de piezas, no la inyeccion
> real al prompt. Medido ese dia: `context_builder.py` **no inyecta** hoy (no tiene
> consumidor que llegue a un turno; alimenta informes/blackboard) y la inyeccion por
> turno va por el hook `pre_llm_call` → `~/.hermes/agent-hooks/joko-context.py`,
> **cableado pero inactivo** (sin allowlist → no dispara). Detalle: skill `local-rag` →
> `references/inyeccion-contexto-en-hermes.md` y skill `joko-context`.

## 6.4 Metricas reales (verificadas)

| Operacion | Volumen | Tiempo |
|-----------|---------|--------|
| Indexacion completa | 42,931 filas (04-sep-2026) | ~90s (GPU) / ~4h (CPU, no usar) |
| **Re-index incremental v2 (5-ago)** | solo cambios | **~30s por pocos archivos** (antes: vault entero) |
| Busqueda semantica HIBRIDA (5-ago) | 5 recuperados, 3 devueltos | **~3.2s en caliente** (con daemon reranker + TOP_K 5) |
| Busqueda antigua (hasta 5-ago) | 10 recuperados | ~6.2s (reranker CPU = cuello de botella) |
| Embeddings via LM Studio API | 1024 dims | 59ms, sin VRAM extra |

**Cuello de botella del reranker RESUELTO (5-ago-2026):** con TOP_K_RETRIEVE=10
y el reranker en CPU, el rerank costaba ~6s (97% del tiempo de busqueda).
Causa raiz: bge-reranker-v2-m3 en CPU cuesta ~0.6s/par y el coste escala con
la longitud (max_seq 8192 no truncaba). Fix en 3 capas:
1. `search.py`: TOP_K_RETRIEVE 10→5 — el rerank solo refina el top del retrieve;
   el top-3 resultante es IDENTICO (verificado) y la latencia baja a la mitad.
2. `reranker_daemon.py`: `--max-seq 256` — limita tokens por fragmento.
3. `joko-reranker.service`: `Nice=-10` — prioridad del daemon sobre Chrome/GNOME.
Resultado: busqueda 6.24s → **3.23s** en caliente, calidad identica
(top-3: 0.738/0.413/0.799 antes y despues). Backups: search.py.bak-rerank-20260805,
reranker_daemon.py.bak-20260805.

**Metrica de telemetria reformulada (07-ago-2026):** el informe "KOs nunca
recuperados" media el universo de consultas, NO la recuperabilidad (verificado
con consulta dirigida: POLICY-002 y PATTERN-001 si son recuperables). Ahora
etiquetado como "no recuperados en el periodo" + desglose por tipo. Ademas,
dedupe por path en search.py: LanceDB guarda chunks y el mismo documento
entraba varias veces por consulta; ahora se devuelven top_k unicos.

## 6.5 Búsqueda híbrida FTS + vectorial (P3, 5-ago-2026)

search.py usa `_busqueda_hibrida()`: ejecuta FTS (BM25, índice Spanish) y
vectorial (IVF_HNSW cosine) en paralelo y fusiona por RANGO con Reciprocal
Rank Fusion (K=60) — los scores BM25 y distancias no son comparables, por eso
se fusiona por rango, no por score. **El indexer recrea los índices tras cada
re-index** (create_table overwrite los destruiría; sin esto el watchdog habria
degradado la busqueda a vectorial en silencio).

Filtros por frontmatter (mismo dia): `--type` y `--status` en search.py
(pre-filtro `where` ANTES de FTS y vectorial). Ejemplo real:
`search.py -q "reglas del laboratorio" -k 3 --type RULE` devuelve SOLO
RULE-008/006/009; sin filtro, la misma query da normas-jl.md. Columnas
`type`/`status` en la tabla (extraidas del frontmatter .md o raiz YAML de KOs).

Verificacion: 13/13 PASS (3 queries). Mejora real: con "modelo descartado
Monty Hall", FTS aporta qwen3-14b.md (termino exacto) que la vectorial sola
no veia. Backups: search.py.bak-hybrid-20260805.

## 6.7 Agentic RAG Loop (Fase 1-4, 07-ago-2026)

Loop de recuperacion con reformulacion determinista para consultas con señal
de conflicto/vigencia. Piezas:
- `tools/agentic_loop.py` — EVALUATE determinista (no depende del criterio del
  LLM): RETRIEVE (search.py) → EVALUATE cobertura (verification/comparador.py
  sobre texto completo) → EVALUATE vigencia (status/expires/superseded de KOs
  recuperados) → REFORMULATE determinista (anade keywords faltantes, max 3
  iteraciones). Solo lectura.
- `tools/medir_agentic.py` — medicion clasico vs agentic sobre verification/bank.yaml.
- Skill `agentic-rag` (USO MANUAL).

Medicion real (04-operations/reports/2026-08-07-medicion-agentic-loop.md):
- Clasico 5/7 vs agentic 6/7 en el banco. Unica mejora: EXP4-001 (conflicto/
  vigencia: "¿Debe utilizarse Qwen 3.5?"). Sin mejora en consultas simples (6/7).
- Coste: +14% tiempo en el peor caso del banco; la reformulacion solo se
  dispara con señal.

Umbrales decididos con datos (Fase 4): activar SOLO para consultas con señal
de conflicto/vigencia (comparativa, contradiccion, "debe usarse", "descartado",
superseded); NO para simples. Fase 0 (activacion en produccion) PENDIENTE de
aprobacion del usuario — el loop sigue INACTIVO.

Limitacion conocida (anotada 07-ago): el evaluador de cobertura con `prohibido`
da falso negativo (EXP1-001: "AMBOS incompletos" con faltantes=[] porque el
contexto recuperado menciona la keyword prohibida, aunque la respuesta seria
correcta). Correccion pendiente con EXP: comprobar prohibidos SOLO en la
respuesta final, no en el contexto (tocar verification/comparador.py afecta a
run_eval.py — requiere su propio experimento).

## 6.6 El cuello de botella de GPU (resuelto)

**Problema (descubierto 30-jul-2026):** BGE-M3 cargado independientemente
(~2 GB) competia con LM Studio por la misma GPU → 75% de queries devolvian
contexto vacio aunque hubiera documentos relevantes.

**Solucion (31-jul-2026):** usar el endpoint de embeddings de LM Studio
(`localhost:1234/api/v0/embeddings`) via `tools/lmstudio_embeddings.py`.
Respuesta: 59ms, 1024 dims, sin VRAM extra. search.py y buscar_perfume.py
ya integrados.

## 6.6 Verificacion determinista (anti-Goodhart)

Para medir si el conocimiento realmente se capitaliza (no que un LLM juzgue
a otro LLM), existe un banco de preguntas objetivas:

- `verification/bank.yaml` — preguntas con respuesta esperada + ruta fuente
- `verification/comparador.py` — compara respuestas del modelo contra banco
- `run_eval.py` — ejecuta la evaluacion con un modelo (recomendado:
  granite-4.1-8b, 5/5 y rapido)

**Reglas:**
- El banco NO debe estar indexado en el RAG (contaminacion)
- Las keywords de `respuesta_esperada` deben existir literalmente en la fuente
- Evaluador `completitud_parcial`: detecta el fallo silencioso (respuesta que
  suena completa pero le falta 1 de N hechos)

## 6.6b Cobertura del contexto (`tools/evaluar_cobertura_contexto.py`, 06-oct-2026)

`evaluar_rag.py` mide `recall@K`; este instrumento mide otra pregunta: **¿esta el
hecho en el corpus y, si esta, llega al contexto?** El juicio es determinista
(coincidencia de variantes normalizadas), **sin LLM**.

- Ejecutar:
  `~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/evaluar_cobertura_contexto.py --k 5 --presupuesto 6000 --detalle`
- Flags: `--k`, `--presupuesto` (chars de contexto, por defecto 6000), `--detalle`, `--json`.
- **Cajas**: `CUBIERTO` (llega todo lo pedido) · `PARCIAL` (llega parte de lo que
  existe) · `CUBIERTO_RECUPERABLE` (el corpus no tiene todo lo pedido, pero lo que
  tiene SI llega) · `FALLO_RECUPERACION` (esta en el corpus y NO llega) ·
  `ABSTENCION_CORRECTA` (no esta: lo correcto es no responder) · `NO_CALCULABLE`.
- **Controles obligatorios en la misma pasada**: 1 positivo + 3 negativos +
  declaracion de ceguera; si fallan, `rc=2`. El `set_sha256` identifica el set
  exacto medido: dos pasadas con sha distinto NO son comparables.
- **La caja esperada se declara ANTES** de medir (campo `esperada`) y el resumen
  cuenta `casos_dirigidos` / `dirigidos_ok`: sin eso, un set solo confirma lo que
  ya se sabia.
- **Criba FIJADA (06-oct-2026, sobre el baseline medido — RULE-015)**: el instrumento
  sigue sin umbral a priori; lo que se fija es el juicio sobre el DATO. `ratio =
  cobertura@5 / techo` por caso: `VERDE` 1,00 · `AMBAR` 0,50-1,00 · `ROJO` < 0,50 ·
  `EXENTO` (techo 0: no hay hecho exigible). El juicio GLOBAL corre solo sobre los casos
  **comparables** (techo igual al del baseline) y exige **no bajar de 5 `VERDE` ni subir
  de 2 `ROJO`**: un caso cuyo TECHO se movio desde el baseline (el corpus se reindexa a
  diario) es **NO COMPARABLE** y se excluye del veredicto en vez de contaminarlo. **No hay
  criba sobre ratios agregados** (1 hecho = 1/26 = 3,8 % del denominador EN CORPUS hoy).

**Medicion 06-oct-2026** (13 casos, `k=5`, `rc=0`): ver la entrada v1.6.11 del changelog.

**Criba del 06-Oct-2026 — 2 pasadas medidas** (`set_sha256 de40e6bec98a2525`, `rc=0`; `[BANCO]` — esta seccion DOCUMENTA el banco de pruebas: no cuenta como corpus):
- **23:04 CEST** (45.568 chunks): 11 comparables → `VERDE` 5 / `AMBAR` 4 / `ROJO` 1 /
  `EXENTO` 1 → **VEREDICTO: OK** (baseline de 15:37:53 CEST: 45.552 chunks, 23 hechos).
- **23:13 CEST** (45.575 chunks, el indice se movio otra vez durante la verificacion):
  11 comparables → `VERDE` 6 / `AMBAR` 3 / `ROJO` 1 / `EXENTO` 1 (`exp-hel` 1/2 → 2/2) →
  **VEREDICTO: OK**.
Unico ROJO en las dos: `fallo-detalle-reel`. Excluidos por techo movido (hechos que entraron
en el indice con el reindexado diario): `abst-dato-vivo`, `fallo-dato-bd-perfume` — los dos,
con los hechos YA en el corpus y 0/2 en el top-5, quedan anotados como **huecos de
recuperacion** en `pendientes.md`.

> **RECTIFICACION (06-oct-2026, misma sesion, tras medirlo)**: la frase «los dos, con los
> hechos YA en el corpus» es **FALSA**. Medido barriendo el indice (`path` + `text` de los
> 45.578 chunks): `45552` existia SOLO en esta GUIA; `turathi` y `4 sprays` SOLO en la GUIA
> (2 chunks) y en el asiento de `pendientes.md` (1 chunk); `espacio en disco` SOLO en un
> espejo externo de skills sin relacion (Volatility3: «Espacio en disco suficiente»). O sea:
> el probe leia la frase «NO estan en el corpus» como prueba de que SI estaban =
> **cobertura fantasma**; el corpus no gano ni un documento util. **CURA aplicada al
> instrumento** (`BANCO_HABLA` + marca `[BANCO]`): un chunk que HABLA del banco de pruebas
> no cuenta ni como TECHO ni como evidencia del top-k, y el **techo bruto** se sigue
> imprimiendo para que la contaminacion no se esconda. Con la cura, `fallo-dato-bd-perfume`
> vuelve a techo 0 (EXENTO) y su hipotesis «FALLO_RECUPERACION» queda **falsada** ->
> `ABSTENCION_CORRECTA` (el dato de dosis vive en `coleccion.db`, no en documentos); y
> `abst-dato-vivo` pierde el hecho generico `espacio en disco`. Los cortes de la criba
> (1,00 / 0,50) y los limites globales (5 VERDE / 2 ROJO) **NO se tocan**.

>
> **MEDIDO CON EL INSTRUMENTO CURADO (misma sesion, `rc=0`, `set_sha256 a9ae27b05e3c0b1a`)**:
> `abst-dato-vivo` techo **0** (bruto 1: solo la GUIA y el asiento) -> **EXENTO**, y
> `fallo-dato-bd-perfume` techo **0** (bruto 2) -> **EXENTO**: los dos dejan de ser «huecos de
> recuperacion» y pasan a **abstencion correcta** (el top-k no trae el dato porque no existe
> documento que lo sostenga). Reparto con el instrumento curado: **VERDE 6 · AMBAR 3 · ROJO 1
> (`fallo-detalle-reel`) · EXENTO 2**; comparables 12; **NO comparable** `abst-dato-vivo` (su
> techo del baseline, 1, era fantasma: lo midio el probe contaminado) — ahora la exclusion esta
> **explicada**, ya no es «el indice se movio»; corpus **45.583 chunks** | utiles **45.563** |
> del banco **20**; hechos en corpus **22** (baseline 23, tambien contaminado); `cobertura@5`
> **0,62 (18/29)** y **0,82 (18/22)** contando solo el corpus util. Los cortes y los limites
> globales NO se mueven: **VEREDICTO OK**.
> **Calibracion MEDIDA del filtro** (leccion): la 1ª version del patron incluia `top-5` y caia
> en **9 ficheros, 5 legitimos** (`research/experimento-hyde-20260831.md`,
> `research/analisis-mcps-mas-usados-2026.md`, `research/analisis-shivabytes-vectorless-rag.md`,
> `GUIA-APRENDIZAJE-JOKO-LAB.md`, `04-operations/backlogs/bak-20260902-shivabytes-vectorless.md`)
> y `banco de pruebas` en 2 legitimos -> **descartados los dos**. Discriminan sin falso
> positivo lo que solo existe en la doc del banco: `[BANCO]`, `cobertura@`,
> `evaluar_cobertura_contexto`, `huecos medidos`, `hechos en corpus` y los **ids de caso**.
> **MATCHER ENDURECIDO + CASO CURADO (v1.6.14, 06-oct-2026, misma sesion)**: el unico ROJO
> (`fallo-detalle-reel`) era un caso MAL DISENADO, no un hueco de recuperacion: su consulta pedia
> algo inexistente en el corpus (0 chunks) y sus 2 hechos eran falsos (`corpus_abstention` no
> existe en ningun chunk; `19 33` casaba con `19:33:35` y con `19.337` porque `_norm` convierte
> todo signo en espacio). El recuperador esta bien: el documento sale **puesto 1** (`d=0.266`) con
> el titulo literal y **puesto 2** (`d=0.319`) con una parafrasis. **Cura**: un hecho sin NINGUNA
> letra es invalido y todo match exige **frontera de digito** (11/11 en `check_matcher.py`); el
> caso pasa a `cub-detalle-reel` (esperada CUBIERTO) con consulta y hechos reales; el hecho de
> `abst-dato-vivo` se re-declara VALOR+ETIQUETA (`45552 chunks`). **Cortes y limites NO se
> tocan.** Medido (`rc=0`, `set_sha256 4c14cd6d269fef8b`, 3 pasadas identicas):
> `cub-detalle-reel` **CUBIERTO 3/3 (VERDE)**, **ROJOS 0**, `VERDE` 6 / `AMBAR` 3 / `EXENTO` 2,
> comparables 11, `cobertura@5` 0,70 (21/30) y 0,88 (21/24) sobre corpus util -> **VEREDICTO OK**.
> La caja `FALLO_RECUPERACION` queda VACIA (lo avisa el propio instrumento): no se estrena
> fabricando un caso.



## 6.7 Pitfalls criticos del RAG

1. **Vigencia (RESUELTO 1-ago-2026 con patron OKF)** — el pipeline ordena
   SOLO por similitud; un doc viejo con mas trozos puede ganar al KO vigente.
   Solucion aplicada (patron OKF, ver 6.9): indice de Knowledge Objects
   (`verification/indice.md`, ~359 tokens) inyectado en el system prompt +
   curacion de bodies de KO con keywords + exclusion de duplicados
   pre-migracion (`04-operations/decisions/` y `*.BACKUP`) del indexador.
   Resultado medido: 5/6 → 6/6 en el banco de verificacion con +36% tokens.
2. **Cache del contexto** — `~/tmp/rag-cache` con TTL 300s. Tras re-indexar,
   el cache puede seguir sirviendo resultados viejos hasta 5 min. Limpiar o
   esperar. Clave: `md5(query:top_k)` — cambiar top_k da ejecucion fresca.
3. **Indexador y YAML** — el indexador debe aceptar .yaml/.yml (Knowledge
   Objects). Si buscas un KO y no aparece, sospecha del filtro de extensiones.
4. **Subprocess pattern para Flask** — si una app web usa RAG, NO cargar
   BGE-M3 en el proceso Flask (~2GB). Usar subprocess al venv hermes-rag.
5. **verify-lab.sh con set -e** — lanzar SIEMPRE con redireccion a log:
   `cd ~/joko-lab/verification && nohup ./verify-lab.sh > /tmp/verify-lab.log 2>&1 &`
   Un 0/N con errores HTTPConnectionPool = LM Studio caido, no fallo de RAG.

## 6.8 Comandos utiles

```bash
# Buscar en el RAG (hibrido: FTS + vectorial + RRF)
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "consulta" --top_k 3
# Con filtros por frontmatter (5-ago)
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "reglas" --top_k 3 --type RULE
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "vigentes" --top_k 5 --status activo

# Re-indexar (incremental v2: solo cambios; --force = total ~4h CPU, evitar)
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/indexer.py --device cpu
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/indexer.py --dry-run   # ver que haria sin tocar
# El watchdog (joko-indexer.service) lo hace solo al detectar cambios

# Contexto inyectado (lo que ve el LLM)
echo "consulta" | ~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/context_builder.py

# Conocimiento estructurado
echo "consulta" | ~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/knowledge_resolver.py
```

## 6.9 Patron OKF — indice de Knowledge Objects (implementado 1-ago-2026)

**Origen:** video de RAG+OKF (Open Knowledge Format, Google 12-06-2026).
Problema que resuelve: el fallo mas caro de un RAG no genera error — la
respuesta "suena completa" pero le falta un hecho, o el doc viejo gana al
vigente por volumen de trozos. Verificado en el lab con EXP1-001/EXP3-001.

**Componentes nuevos:**

| Componente | Ruta | Proposito |
|-----------|------|-----------|
| Generador de indice | `tools/generar_indice_okf.py` | Regenera el indice desde `objects/` (lee `body`, scope obligatorio) |
| Indice de KOs | `verification/indice.md` | 10 KOs, ~359 tokens, scope declarado `decisions_rules_policies_only` |
| Prompt con indice | `verification/system_prompt_con_indice.txt` | system_prompt.txt + indice.md concatenados |
| Evaluador completitud_parcial | `verification/comparador.py` | Detecta el fallo silencioso (respuesta que suena completa pero le falta 1 de N hechos) |

**Como se usa (Fase 4):** el indice se concatena al system prompt de
produccion. Coste medido: +36% tokens de prompt, beneficio 5/6 → 6/6
(elimina el fallo residual V002, cuya keyword "0/5" queda literal en el
indice via DEC-001).

**Reglas del indice:**
- Cubre SOLO los KOs (scope declarado en el propio fichero) — no generalizar
  "no existe" a fichas o patrones que no estan en el indice
- Regenerar con `python3 tools/generar_indice_okf.py --scope decisions_rules_policies_only`
  cuando cambien los KOs
- El indice vive en `verification/` (excluido del indexador RAG, no contamina)

**Leccion clave:** la composicion se escribe en el conocimiento (body del KO
curado con keywords), no se espera que el RAG la reconstruya. Ejemplo:
DEC-002 body incluye "Limite de tokens: max_tokens 2048" para que el
embedding y el reranker lo suban cuando se pregunta por el limite.

## 6.10 Experimento P1: contexto CRUDO vs ESTRUCTURADO (2-ago-2026)

**Objetivo (backlog P1):** medir el ahorro real de tokens del contexto RAG
crudo vs estructurado, en 4 dimensiones: tokens, latencia, precision,
cobertura. Hipotesis inicial del skill: ~70 tok/consulta estructurado vs
~280 crudo (ahorro 75%).

**Metodo:** `verification/medir_p1.py` ejecuta el banco (6 items) con cada
variante contra granite-4.1-8b en LM Studio. Variante estructurada en
`tools/context_builder_estructurado.py` (ruta + campos clave + summary
corto, sin snippets completos).

**Resultados medidos (2-ago-2026, despues de curar DEC-001 y RULE-001):**

```
Variante        tok_ctx prompt_tok  t_total(s)  precision  cobertura
CRUDO            303.83     527.50       21.63        5/6        6/6
ESTRUCTURADO     319.17     476.67       21.92        6/6        6/6
```

**Ronda 3 (2-ago-2026, bge-reranker-v2-m3 multilingue + curacion):**

```
Variante        tok_ctx prompt_tok  t_total(s)  precision  cobertura
CRUDO            351.00     524.50       23.21        6/6        6/6
ESTRUCTURADO     339.17     503.50       21.86        6/6        6/6
```

El fallo de fondo del reranker (KOs en español hundidos por ms-marco, solo
ingles) quedo resuelto con bge-reranker-v2-m3: el CRUDO paso de 5/6 a 6/6
(V002 ya no falla). Evolucion completa del banco hoy: ms-marco sin curar
5/6+4/6 → ms-marco curado 5/6+6/6 → bge-v2-m3 curado 6/6+6/6, cobertura 6/6.
Repo_id correcto: `BAAI/bge-reranker-v2-m3` (el nombre sin "v2" NO existe,
404). HF token en `~/.cache/huggingface/token` (permisos 600).

**Conclusiones (DEC adoptada):**
1. **Hipotesis del 75% NO confirmada.** El ahorro real de prompt_tokens es
   ~10% (527 → 477). El formateo compacto tokeniza mejor, pero la extraccion
   estructurada aun incluye muchos campos. NO perseguir el 75% como objetivo.
2. **El valor real esta en la curacion (OKF), no en el formateo.** Al curar
   los bodies de DEC-001 (anade "modelo principal") y RULE-001 (anade
   "creatividad", "codigo completo", "recomendado"), ambos KO subieron de
   posicion 8+/fuera del top-10 a posicion 1 del reranker. Cobertura
   4/6 → 6/6 y precision del estructurado 4/6 → 6/6.
3. **context_builder.py adopto el formateo estructurado** (2-ago-2026):
   search_rag y get_model_card usan ahora la extraccion compacta
   (import desde context_builder_estructurado). Backup:
   `context_builder.py.bak-20260802`. Misma CLI y API publica; los
   consumidores (run_eval, joko-context, knowledge_resolver) no cambian.
4. **Cuello de botella real:** search.py (~15s de construccion en ambas
   variantes). El formateo es secundario; la recuperacion manda.
5. **Backups de hoy:** DEC-001.yaml.bak-20260802, RULE-001.yaml.bak-20260802,
   context_builder.py.bak-20260802.

**Comandos del experimento:**
```bash
# Medicion completa (requiere LLM en :1234)
cd ~/joko-lab/verification && ~/.venv/hermes-rag/bin/python3 medir_p1.py
# Solo contexto, sin LLM
cd ~/joko-lab/verification && ~/.venv/hermes-rag/bin/python3 medir_p1.py --no-llm
```

**Informe final (04-ago-2026):** `04-operations/reports/2026-08-04-p1-informe-final-ahorro-tokens.md`.
Aclara los DOS niveles de la metrica: a nivel de contexto RAG recuperado el
ahorro es ~10% (el RAG ya filtra); a nivel de documento INTEGRO vs extracto
estructurado (medicion v2) es 98.4% (19.9k → 323 tok) — confirma el 55x del KAP.


## 6.11 Experimento grafo: wikilinks entre Knowledge Objects (2-ago-2026)

**Objetivo (backlog P4):** el grafo de conocimiento era casi inexistente (3
enlaces en 100 docs). Hipotesis: enlazar los KOs entre si crea aristas
navegables e indexadas que mejoran la recuperacion sin degradar la
verificacion.

**Accion:** 8 wikilinks `[[...]]` anadidos al body de los KOs, solo con
relaciones reales (dependencies declaradas + coherencia de dominio):
DEC-001→[[RULE-004]], DEC-002→[[RULE-003]], DEC-003→[[RULE-001]],
RULE-001→[[DEC-003]], RULE-002→[[RULE-001]], RULE-003→[[DEC-002]],
RULE-004→[[DEC-001]], POLICY-001→[[RULE-004]], POLICY-002→[[POLICY-001]].
RULE-005 queda sin par interno (su relacion es con la norma JL-013, no con
otro KO). Backup: `.bak-wikilinks-20260802/`.

**Resultado medido (2-ago-2026):** banco de verificacion intacto — 6/6
precision y 6/6 cobertura en CRUDO y ESTRUCTURADO tras re-indexar (13185
registros). Los wikilinks no degradan la verificacion. Bonus: la latencia de
construccion del contexto bajo de ~15s a ~4.3s por el daemon del reranker
(ver 6.4). Grafo del lab: de 3 a ~11 wikilinks.

**Pendiente:** enlazar fichas de modelo (granite-4.1-8b.md ↔ RULE-002, etc.)
y evaluar Obsidian como visualizador con datos del experimento (JL-005).

---

<a name="capitulo-7"></a>
# CAPITULO 7 — ARQUITECTURA Y ENRUTAMIENTO (AI-ROUTER)

## 7.1 La arquitectura v3 en 4 capas

```
CAPA 1 — Infraestructura      (LM Studio, DeepSeek, Hermes)
CAPA 2 — Recuperacion         (RAG, Knowledge Resolver, Context Builder)
CAPA 3 — Gobierno del conocimiento (KAP, Health Auditor, KOs, Decision Engine)
CAPA 4 — Evolucion del conocimiento (KVC, KEL, Pruning, Evidence Contract)
```

La transicion clave de julio 2026: el lab paso de construir componentes a
gobernar como nace, se valida, evoluciona y se retira el conocimiento.

**Capa de ejecucion de misiones (07-ago-2026, PROPUESTA):** el Router no
orquesta pipelines de multiples fases (limite declarado). Mission Contract
(`research/mission-contract-diseno.md` + `lpa/contracts/mission.schema.json`,
validado contra el caso Indra) define el contrato de mision: id, goal,
status, current_node, inputs/outputs, evidence, retries, checkpoints,
shared_state y transiciones. Motor-agnostico (n8n para lo visual; Python
solo para lo que n8n no cubre). El Mission Runner se activaria por
PROPIEDADES de ejecucion (estado compartido, retries, ramas, paralelismo,
checkpoints), no por numero de fases — criterio a validar contra misiones
reales antes de fijarse. Sigue congelado hasta decision.

**Worker de codigo (OpenCode, 07-ago-2026):** herramienta de ingenieria, no
decisor. Instalado `opencode` 1.18.15 (npm prefix `~/.npm-global`, auth
DeepSeek via DEEPSEEK_API_KEY del .env; PATH: `export PATH="$HOME/.npm-global/bin:$PATH"`).
Gobernado por el gate de codigo del lab: Hermes detecta la funcion candidata
(informe de complejidad: 264 funciones, 9 >20, top knowledge_health.audit()
52) -> OpenCode propone el refactor -> VERIFIER (comportamiento identico) ->
SVP-diff (alcance revisado) -> backup (RULE-008) -> registro PIL. Piloto
validado 07-ago: extraccion de `calcular_metricas_activaciones()` en
tools/observer.py, telemetria identica, OP-20260807-014.

## 7.2 Los componentes del Runtime

```
State Manager       — observa, escribe state.json (cada 60s, 0% CPU)
Policy Engine       — interpreta politicas, nunca decide
Capability Registry — describe capacidades, nunca decide
Decision Engine     — decide basado en state + policies (7.5ms, sin LLM)
Runtime API         — interfaz estable (Runtime.resolve(), 9 campos)
Metrics             — datos de uso para decisiones basadas en evidencia
```

**Regla contract-first:** todo componente expone contrato (YAML/JSON)
antes que implementacion. Contrato: `runtime/CONTRACT.md` v1.0.

## 7.3 El flujo de decision

```
apply-decision.sh (cron cada 30 min o bajo demanda)
    ↓
Runtime.resolve()  ← runtime/api.py — UNICA puerta de entrada
    ↓
decision_engine.decide()  ← puro: solo {provider, model, reason}
    ├── lee state.json (State Manager)
    ├── lee policies/*.yaml (8 archivos, 100% declarativas)
    └── devuelve {provider, model, reason}
    ↓
escribe ultima-decision.json + decision.log
    ↓
devuelve 9 campos: {provider, model, reason, policy, privacy,
                    verification, confidence, expires, decision_id}
    ↓
apply-decision.sh → hermes config set (modelo/proveedor/URL)
```

**El DE es puro:** solo recibe input y devuelve JSON. No escribe archivos,
no modifica config, no conoce ~/.hermes/.

## 7.4 Las 8 politicas YAML (en /mnt/ssd_ia_datos/lab-state/policies/)

| Archivo | Proposito |
|---------|-----------|
| privacidad.yaml | Datos sensibles → forzar local (precedencia 1) |
| disponibilidad.yaml | Fallback si un proveedor cae |
| costes.yaml | Saldo minimo antes de cloud |
| gpu.yaml | Desactivada para modelo principal (04-ago): VRAM ya no decide; uso local via delegacion | 
| horario.yaml | Todo el dia deepseek (04-ago): franja gemini eliminada; PRO manual (/model) |
| niveles.yaml | Nivel de verificacion por tarea |
| preferencias.yaml | Fallback final por defecto |
| modelos.yaml | Modelo por defecto por proveedor |

**Precedencia (orden de evaluacion):** privacidad → disponibilidad →
costes → GPU → horario → niveles → preferencias.

## 7.5 Registro de decisiones (decision-ledger)

- `decision-ledger.jsonl` (JSONL append-only en lab-state/)
- Cada llamada a `decide()` anade: {timestamp, provider, model, reason,
  nivel, temperature, max_tokens}
- Alimenta LPA (aprendizaje)

```bash
tail -5 /mnt/ssd_ia_datos/lab-state/decision-ledger.jsonl
```

## 7.6 Knowledge Activation Layer (Phase 3, 30-jul-2026)

Input estrategico de Luis: "el laboratorio ya sabe cosas pero no actua en
consecuencia". Capitalizacion: 2/10 → 9/10.

Pipeline completo:

```
Usuario → Task Understanding → Planning → Activation Engine (RULEs + POLICYs)
       → Decision Engine → Event Bus → Confidence Decay → Debt Detector → Trazabilidad
```

Componentes nuevos:
- **Activation Engine** (`tools/activation_engine.py`): busca RULE activas
  y las inyecta. No responde, no razona. Solo activa.
  **⚠ ARREGLADO 1-ago-2026:** leia de rutas fantasma
  (`01-knowledge/rules/` y `01-knowledge/policies/`) que ya no existen tras
  la migracion a `objects/` → cargaba 0 reglas → nunca activaba nada.
  Ahora lee de `01-knowledge/objects/`, filtra por `type` (RULE/POLICY) y
  aplana `legacy_fields`. Verificado: "escribe un poema" → RULE-001 (Gemma 4);
  "usa qwen 3.5" → bloqueo (RULE-004 + POLICY-001).
- **Event Bus** (`tools/event_bus.py`): capitalizacion automatica.
  Eventos: dec.created, exp.completed, model.updated, benchmark.new.
- **Confidence Decay** (`tools/confidence_decayer.py`): envejecimiento.
  Formula: evidencia x recencia x validaciones x compatibilidad.
  Periodo de gracia 7 dias, umbral 0.3.
- **Debt Detector** (`tools/debt_detector.py`): 6 checks de deuda tecnica.
- **Orchestrator** (`tools/orchestrator.py`): fases 1+2 unificadas.

## 7.7 Verificacion determinista y anti-Goodhart

Referencia: `references/deterministic-verification.md` (30-jul-2026).
Mide capitalizacion real sin que un LLM juzgue al propio LLM.

Baseline real: 0% sin pipeline, 25% con pipeline. Capitalizacion 2→9/10.
RAG es el limitante operativo (cuello de botella GPU, resuelto).

## 7.8 Diagnostico rapido del Runtime

```bash
# Decision actual (9 campos del contrato)
python3 /home/jokoalmi/hermes-lab/runtime/api.py --json

# Estado del laboratorio
cat /mnt/ssd_ia_datos/lab-state/state.json | python3 -m json.tool

# Ultima decision
cat /mnt/ssd_ia_datos/lab-state/ultima-decision.json

# Log del Runtime
tail -5 /mnt/ssd_ia_datos/lab-state/logs/decision.log | python3 -m json.tool

# Tests (DE + contrato + state-manager)
python3 -m unittest tests/test_decision_engine.py tests/test_contract.py tests/test_state_manager.py
```

## 7.9 Llamadas al router y la taxonomia de capacidades

El router no pregunta "¿que modelo?" sino "¿que capacidad necesito?":

**🧠 Cognitivas:** Conocimiento, Razonamiento, Creatividad, Codigo, Espanol, Consistencia
**⚙️ Funcionales:** JSON, Tool Calling, Vision, Memoria
**📊 Operativas:** Velocidad

Ejemplo:

```
Mision: landing pagina
  → ¿Necesito Vision? Si → GLM (Vision=9)
  → ¿Necesito Creatividad alta? Si → Gemma (Creatividad=10)
  → ¿Necesito Velocidad? Si → Dolphin (Velocidad=10, Codigo=8)
```

**Escalada:** si los modelos locales fallan sistematicamente en un tipo de
problema (ej: razonamiento secuencial), escala a cloud (DeepSeek V4 Pro).

---

## 7.10 Instrumento de coste y ahorro de tokens (`coste_ahorro.py`, 11-oct-2026)

Mide el GASTO REAL de DeepSeek y prepara el espejo local (USD evitados). Solo OBSERVA, MIDE y
REGISTRA: no cambia nada del sistema y no fija umbrales a priori (RULE-015).

- Script: `joko-lab/tools/coste_ahorro.py` (solo stdlib; lee `04-operations/metrics/pipeline_obs.jsonl`).
- Config: `04-operations/metrics/config_coste.json` (`umbral_dias_alerta`: null = sin alerta).
- Serie/historial: `04-operations/metrics/coste_historial.jsonl` (append; 1 linea por snapshot).
- Wrapper de cron: `~/.hermes/scripts/coste-ahorro.sh` (mode 755).
- Cron: `coste-ahorro-diario`, id `404f3a96481c`, `40 7 * * *`, `no_agent`, deliver origin.
- Tarifa: DeepSeek V4-Flash oficial 11-oct-2026 — hit 0,003 / miss 0,15 / out 0,60 USD por 1M
  (peak x2 L-V 01-04h y 06-10h UTC = 03-06h y 08-12h Espana).
- Informa: ayer + hoy (parcial), serie y media de 7 dias, reparto del coste por componente
  (hit/miss/out), saldo real de la API y dias restantes, y el estado del espejo local.
- Medido el 11-oct-2026: 7 dias = 9,23 USD (media 1,32 USD/dia); reparto miss 45% / out 43% /
  hit 12%; saldo 4,33 USD (aprox. 3,3 dias). El ledger registra SOLO DeepSeek: los tokens locales
  YA estan instrumentados (11-oct-2026, commit `5067d99`): el espejo local escribe su propio
  ledger y el informe ya calcula los «USD evitados» con ESTA misma tabla.
- ESPEJO LOCAL MONTADO (11-oct-2026, commit `5067d99`): el ledger cloud registra SOLO DeepSeek, asi
  que los tokens locales se anotan aparte. `tools/ledger_local.py` extrae `usage` (LM Studio :1234)
  o `prompt_eval_count`/`eval_count` (Ollama :11434) y calcula «USD evitados» con la MISMA tabla de
  tarifas (importa `TARIFA`/`es_peak` de `coste_ahorro.py`). `tools/llm-router.sh` es el unico embudo
  hacia LM Studio y ya lo llama en cada consulta (`|| true`: nunca rompe al llamante).
  - Ledger local: `04-operations/metrics/ahorro_local_ledger.jsonl` (1 linea por consulta OK); log de
    fallos: `04-operations/metrics/ahorro_local.log` (ambos ignorados por git: `metrics/*.jsonl` y `*.log`).
  - E2E real del 11-oct: `lfm2.5-2.6b` por el router -> prompt 57 + salida 600, `latencia_s` 9.01, 0 errores.
  - PITFALL (cazado por el E2E, no leyendo): `awk` con locale es_ES daba `lat=2,13` (coma decimal) y
    `argparse --latencia type=float` abortaba con exit 2 OCULTO por un `2>&1 || true`: el ledger quedaba
    vacio y parecia que el router no registraba. Fix: `LC_NUMERIC=C` en el awk, `a_float` en argparse
    (acepta coma o punto) y el stderr del registrador al log en vez de descartarse.
- Complementa al `monitor-precios-ia-semanal`, que vigila PRECIOS de proveedores, no el consumo.

## 7.11 Puente manual LAB <-> Gemini web (12-oct-2026)

Palanca de coste para el gasto fuerte (DeepSeek) y, a la vez, el instrumento de
medida de la suscripcion Google AI Pro (21,99 EUR/mes). Dirigido a tareas caras
en tokens y SIN prisa: documentos enormes, investigacion larga, revision de
papers (el contexto de 1M, Deep Research y NotebookLM solo existen en la web).

- Carpeta: `04-operations/puente-gemini/` — `README.md`, `plantilla-prompt.md`,
  `registro-puente.md` y `.gitignore` propio.
- Herramienta: `tools/puente_gemini.py` — `nuevo "<tema>" [--herramienta X]
  [--contexto FICHERO] [--nota-interna TXT]`, `estado`, `archivar <fichero>
  [--valor N] [--herramienta X] [--nota TXT]`.
- Herramientas validas: `3.1-pro`, `deep-research`, `notebooklm`, `gem`,
  `workspace`. Tope de contexto por fichero: 400 KB. No usa red, no borra y no
  sale de su carpeta (override `PUENTE_BASE` para pruebas).
- Ciclo: el LAB escribe el prompt redactado en `outbox/` -> el usuario lo pega en
  Gemini web -> guarda la respuesta en `inbox/` -> `archivar` la mueve a
  `procesados/` y anota la linea en `registro-puente.md` con valor 1-5.
- Contenido: las 3 carpetas de trabajo estan FUERA de git; se versionan solo los
  3 documentos del puente.
- Frontera de datos: no credenciales, no datos de terceros, no sesiones enteras.
- Lo que NO se puede automatizar (verificado 05-sep-2026): la suscripcion no da
  creditos de API y el login OAuth de Gemini CLI se cerro el 18-jun-2026 para
  cuentas individuales (AI Pro incluido); automatizar la web (cookies, scraping,
  MCP de navegador) viola los ToS -> riesgo de baneo. Manual si; programatico no.
- Verificacion previa al estreno: 2 pases completos en sandbox (bug de acentos
  cazado y corregido en el primer pase). **Primer uso real: 12-oct 17:05** ->
  prompt en `outbox/` (6.905 B, 7 marcas "futuribles", `deep-research`).
  Estado a 13-oct: `outbox 1 / inbox 0 / procesados 0` -> queda la ida y vuelta
  manual (pegar el prompt en la web de Gemini y guardar la respuesta en
  `inbox/`; despues `puente_gemini.py archivar <fichero> --valor N`).
- Sustituye al testimonio en la revision mensual del KO `DEC-GAIPRO-001`
  (`log_file: 04-operations/registro-uso-gemini.md`, next_review 2026-11-03).

<a name="capitulo-8"></a>
# CAPITULO 8 — SINCRONIZACION ENTRE SESIONES

## 8.1 El problema que resuelve

Hermes ejecuta sesiones separadas por canal (CLI, Telegram gateway, cron).
Cada una arranca con contexto vacio. Si trabajas en CLI y luego sales a la
calle y sigues por Telegram, la sesion de Telegram no sabe que estabas a
mitad de algo.

**Solucion:** un sistema de estado y eventos compartidos que todas las
sesiones leen y escriben.

## 8.2 Los canales compartidos (3 niveles, 5-ago-2026)

| Canal | Archivo | Contenido |
|-------|---------|-----------|
| shared-state.json | ~/.hermes/shared-state.json | Estado vivo de cada sesion (activa/inactiva, temas) |
| shared-events.jsonl | ~/.hermes/shared-events.jsonl | Eventos relevantes (decision, pendiente, completado, cambio, alerta, nota) |
| **file bus por dominio** | ~/.hermes/team-context/ | **1 archivo .md por dominio** (cli, telegram, lab, biohacking, perfume, founderz...), ownership por convencion |

El **file bus** (evolucion del shared-state, 5-ago-2026, basado en issue #4529
de Hermes) es la capa principal: cada sesion escribe SOLO en su dominio y
todas leen todos. Un daemon (`team-bus-watch.service`) hace polling cada 5s y
regenera `README.md` (snapshot consolidado) + actualiza shared-state con
`team_bus.<dominio>.last_change`.

**El canal_prompt de Telegram lee el file bus** (`domain-bus.sh read`) antes
de responder — asi ve el estado en vivo de todas las sesiones (F3, 5-ago).

**RULE-009 (regla fija, 5-ago):** toda sesion que complete una tarea/fase/hito
DEBE registrar ANTES de declararlo cerrado: (1) evento en shared-events,
(2) su dominio en el file bus. El bus NO se llena solo — es lectura bajo
demanda; sin registro, las otras sesiones ven info congelada aunque el
trabajo se haya hecho (incidente real: Telegram no veia el trabajo del dia).

## 8.3 Scripts

```bash
# Estado de sesiones
bash ~/.hermes/scripts/session-state.sh read
bash ~/.hermes/scripts/session-state.sh write cli "tema1, tema2"

# Eventos
bash ~/.hermes/scripts/shared-events.sh write cli completado "Resumen del evento" /ruta/ref
bash ~/.hermes/scripts/shared-events.sh read --limit 10
bash ~/.hermes/scripts/shared-events.sh read --since "2026-07-31T12:00:00+02:00"
bash ~/.hermes/scripts/shared-events.sh count

# File bus por dominio
bash ~/.hermes/scripts/domain-bus.sh read [dominio]      # leer un dominio o todos
bash ~/.hermes/scripts/domain-bus.sh write <dominio> "..."  # escribir SOLO en el tuyo
bash ~/.hermes/scripts/domain-bus.sh list                # dominios con last_updated
bash ~/.hermes/scripts/domain-bus.sh claim "recurso" "motivo"  # advisory lock
bash ~/.hermes/scripts/domain-bus.sh release "recurso"
```

**Reglas de eventos:**
- Solo eventos relevantes (resumen ≤200 chars)
- Tipos: decision | pendiente | completado | cambio | alerta | nota
- Poda automatica: >14 dias o >500 lineas
- El gateway de Telegram inyecta `domain-bus.sh read` + `shared-events.sh read --limit 10`
  al responder, asi tiene contexto en vivo de la CLI sin pedir nada

**Reglas del file bus:**
- Cada sesion escribe SOLO en su dominio; todos leen todos
- Formato: frontmatter `owner` + `last_updated` + cuerpo markdown
- Claim ANTES de tocar un recurso compartido (repo, puerto, archivo); release al terminar
- Latencia del snapshot: ≤5s (daemon team-bus-watch)
- Pitfall cron: NO usar `exec bash` en wrappers (mata el resto del script)

## 8.4 Heartbeat y consolidador

- **Heartbeat cron** (cada 10 min): la CLI escribe su estado para que
  Telegram la vea viva
- **Consolidador** (cron 22:30): exporta TODAS las sesiones del dia a
  `~/joko-lab/04-operations/metrics/sesiones/` y genera `resumen-dia-*.md`

## 8.5 Protocolo de inicio de sesion CLI

Al abrir sesion CLI, el agente debe:
1. Leer shared-events (ultimos 10)
2. Leer shared-state
3. Buscar sesiones recientes (session_search)
4. Escribir su estado con los temas reales

## 8.6 Pitfalls verificados

1. **El shared-state se queda desactualizado** si no hay heartbeat o la
   sesion no escribe. Verificado 31-jul-2026: decia "29-jul" mientras la
   sesion CLI seguia abierta.
2. **Registro de sesiones congelado** — las exportaciones a
   metrics/sesiones/raw/ pueden quedarse paradas sin que nadie lo note.
   Verificar que el rango de fechas llega al dia actual.
3. **Checkpoint bug** — el checkpoint diario fallaba silenciosamente
   ("5/12 pasos OK") por variable equivocada ($POINT_DIR vs $TEMP_DIR).
   Leccion: verificar el registro, no darlo por hecho.
4. **Reiniciar gateway** — tras cambiar config del gateway, reiniciar
   desde otra shell (`hermes gateway restart`), nunca desde dentro.

## 8.7 Repaso de pendientes ("repasa todo")

Cuando pidas un repaso general, el orden de lecturas correcto es:
1. Backlog mas reciente (04-operations/backlogs/)
2. Metricas reales (metrics/knowledge_health.jsonl — tendencias)
3. Crontab (verificar automatizaciones activas)
4. session_search (cierre de la ultima sesion)
5. Verificar antes de afirmar (logs/metricas ganan al backlog)

---

<a name="capitulo-9"></a>
# CAPITULO 9 — LOS PRODUCTOS DEL LAB

## 9.0 Distincion fundamental: el lab produce productos

Joko Lab NO es un fin en si mismo. Es el **medio** (infraestructura +
conocimiento + metodologia) para producir **productos reales**.

```
Joko Lab (laboratorio)
    ↓ produce
PRODUCTOS (Perfume IA, Forense Digital, ...)
    ↓ generan
Problemas reales
    ↓ revelan
Principios
    ↓ suben a
LPA (conocimiento)
    ↓ retroalimenta
Joko Lab
```

**Regla LPA (direccion del conocimiento):** la direccion siempre es desde
el proyecto hacia LPA, nunca al reves. LPA se desarrolla construyendo
productos reales y observando que principios sobreviven.

Los productos actuales del lab:
1. **Perfume IA** — Experimento 001 (coleccion personal con IA)
2. **Forense Digital** — peritaje informatico (servicio real)
3. **Monitor LM Studio** — herramienta de observabilidad interna
4. **Benchmarks** — evaluacion sistematica de modelos
5. **Experimentos LPA** — bolsa, mente-natural, psicologia
6. **Biohacking Cerebral** — dominio de optimizacion cognitiva natural
   (creado 03-ago-2026, en `/home/jokoalmi/proyectos/biohacking-cerebral/`):
   pilares de vida (sueno, ejercicio, nutricion, estres) + suplementos +
   tecnicas + protocolos + medicion. Fuentes curadas sobre memoria de
   trabajo (Oberauer 2012, meta-analisis, NICE) migradas del CSV original.

## 9.1 Perfume IA (Experimento 001 — el primer producto)

**Que es:** el primer producto real del lab — una aplicacion web para
gestionar y descubrir tu coleccion de perfumes con IA. Es el "primer
especimen vivo de LPA": cada problema que revela alimenta el conocimiento.

**Estructura real verificada en disco (1-ago-2026):**

```
/home/jokoalmi/perfume-ia/
├── app/
│   ├── api.py                    # Flask backend (+ RAG endpoint, post-filtro)
│   ├── templates/                # 11 templates activos
│   │   ├── landing.html          # Landing principal
│   │   ├── landing-room-v2.html  # Gabinete v2 (holograma + chatbot + RAG)
│   │   ├── index.html, coleccion.html, perfume.html
│   │   └── chat.html, stats.html, destacados-vimg.html
│   └── static/                   # CSS, JS, imagenes, botellas/
├── modules/                      # Solo 2 modulos activos
│   ├── 03-recomendacion/recommendation.py   # Motor LPA v2
│   └── 04-rag/                               # RAG semantico
│       ├── indexador_perfumes.py  # Indexa 167 perfumes en LanceDB
│       └── buscar_perfume.py      # Busqueda BGE-M3
├── scripts/                      # crud-coleccion.py, test_gabinete.py,
│                                 # inicio-perfume.sh (4 checks)
├── data/
│   ├── coleccion.db              # 167 perfumes, 74 casas, 284 notas
│   ├── .lancedb/perfumes.lance   # Indice vectorial BGE-M3
│   └── logs/                     # Trazas del chat
├── lpa → joko-lab/lpa            # symlink
├── experiments → joko-lab/lpa/experiments  # symlink
├── experience/                   # Prototipos visuales + archive/
├── product/                      # Evaluaciones del Gabinete
├── README.md, MEMORANDUM.md, PERFUME_IA_DOSSIER.txt
└── start-web.sh
```

**Datos de la BD (verificados):**
- Coleccion amplia (indeterminado) — la BD refleja tu coleccion REAL fisica,
  no el catalogo de Parfumo
- Marcas sin perfumes en coleccion fueron eliminadas (criterio: solo lo real)
- Los 8 perfumes de Mario Galindo (The Lab) estan registrados (casa_id=95)
- El Laud (id 1023) NO esta en la coleccion fisica → eliminado de la BD

**RAG sobre la coleccion (3 capas):**
- BGE-M3 + LanceDB (CPU, ~3-5s) para no competir con Dolphin en GPU
- El chat consulta la coleccion REAL antes de cada mensaje
- Ejemplo real: "citrico fresco verano" → Fresh Vetiver (The Lab) top-1

**Anti-alucinacion (3 capas, v3):**
- Capa 1: fallback con top 5 del motor LPA si RAG devuelve <2
- Capa 2: prompt estricto ("NUNCA inventes un perfume que no este en las listas")
- Capa 3: post-filtro con regex \b (palabras completas) + verbos de
  recomendacion. ~95% de alucinaciones atrapadas, 0 falsos positivos

**Motor de recomendacion (LPA v2):** 5 factores: temperatura, humedad,
estacion, hora del dia, laboral/fin de semana. OJO: usa Erandio fijo —
en dias de viaje el motor NO sirve (usar open-meteo + SQLite directo).

**Servicio:** Flask en :5050. Endpoints: /, /gabinete-v2, /api/recomendar,
/api/perfume/<id>, /api/rag/buscar, POST /api/chat.

**Arranque:** `start-web.sh` o `scripts/inicio-perfume.sh` (4 checks:
BD, Flask, LM Studio, RAG).

## 9.1b Ficha del dia del perfume (la tarjeta) y sus instrumentos (07-oct-2026)

**Que es:** la tarjeta diaria que se publica en el canal de Telegram: un perfume elegido por el flujo, con su piramide, el clima del dia, QR a Fragrantica y sello. Cada dia abre su carpeta `research/infografias/perfume-del-dia-YYYYMMDD/` y el uso del dia se registra en `uso_diario` de `perfume-ia/data/coleccion.db`.

**Regla dura (no se degrada):** el fondo se genera con **SDXL en ComfyUI (GPU)**; si la GPU no esta disponible -> **PARAR y reportar**, no improvisar. Prohibido tapar un frasco mal recortado con velo, halo o placa (veto del 26-sep).

**Instrumentos (todos de solo lectura):**

| Instrumento | Que mide |
|-------------|----------|
| `tools/medir_contraste_ficha.py` (192 lín. / 8.624 B) | contraste WCAG nodo a nodo sobre el render |
| `tools/inventario_legibilidad.py` (134 lín. / 6.297 B) | inventario de nodos por debajo de 4,5:1 y de 3,0:1 |
| `tools/validar_ficha_preenvio.py` (160 lín. / 8.965 B) | comprobaciones de la ficha ANTES de enviarla |
| `tools/medir_visibilidad_frasco.py` (260 lín. / 11.555 B) | visibilidad real del frasco sobre el PNG final |

**`tools/medir_visibilidad_frasco.py`** (commit `22162b8`, recibo `tree_sha 6233258ba6af990291948dfdd68b26b2bb5a85c9`): lee la geometria REAL del frasco del HTML (`.frasco-figura`) y, sobre el **PNG final**, mide la L mediana del **tapon**, del **cuerpo** y del **fondo contiguo**, el **ratio de contraste WCAG** y el **% de pixeles claros** (L>225) dentro del rectangulo. **4 versiones de la misma ficha, el mismo instrumento** (re-medido 07-oct 13:54 CEST):

| Version | Fondo contiguo (L) | Tapon | Cuerpo | Claros (L>225) |
|---------|--------------------|-------|--------|----------------|
| v5 | 142,0 | 6,41:1 | 1,54:1 | **4,0 %** (3.865 px) -> frasco invisible: PARAR |
| v6 | 193,6 | 11,74:1 | 1,53:1 | 63,2 % (60.853 px) |
| v7 | 159,1 | 7,95:1 | 2,26:1 | 63,0 % (60.695 px) |
| v8 (enviada) | 159,4 | 7,97:1 | 2,25:1 | 63,0 % (60.698 px) |

**Umbrales** (fijados DESPUES de medir las 4 versiones, RULE-015): `--min-claros 40 --min-contraste 2.0`.

**Leccion medida - el veredicto lo da la medida, no el modelo:** **ningun VLM del lab sirve como juez de contraste** sobre la imagen real; el arbitro es la medicion objetiva. El VLM solo vale para preguntas atomicas con control conocido (leer, contar, detectar).

**Instrumentos del paquete de evaluacion de resultados (13-oct-2026, commit `297ee8b`).**

- `tools/cerrar_ficha_dia.py` (135 l.): cierra la marca de valoracion PENDIENTE de
  la fila `uso_diario` del dia (`[VAL: sin respuesta aun | ventana H-H]` ->
  `[VAL: <veredicto> | ventana H-H]`) y ANADE la linea de cierre al final de
  `nota_personal`; nunca reescribe ni borra lo ya escrito (regla
  `edicion-aditiva-registros` §3). Apunta una linea al ledger JSONL. Si no hay
  fila para la fecha, sale con error y no escribe: NO inventa valores.
- `tools/revision_produccion_semanal.py` (149 l.): responde con 4 numeros medidos
  — fichas de la semana (mtime < 7 dias), cuantas con valoracion real, PRED
  vencidos sin revisar (via `escanear_predicciones.py`) e instrumentos con >7 dias
  sin escribir (mtime). Sobre los JSONL grandes usa solo `os.stat`, para no repetir
  el kill del 12-oct.
- `tools/escanear_predicciones.py` (21 lineas tocadas) y `PRED-001/002` + la
  plantilla, al dia en el mismo commit.

## 9.2 Forense Digital (producto de peritaje)

**Que es:** un producto/servicio de peritaje informatico — analisis de
buzones de correo para procedimientos judiciales laborales en Espana.
NO es "buscar correos": es peritaje con cadena de evidencia.

**Que hace (skill forense-digital):**
- Extraccion y preservacion de evidencias
- Clasificacion y valoracion probatoria
- Construccion de dossier documental para abogados y tribunales
- Mapeo a convenio colectivo
- Empaquetado ZIP para entrega

**Caso real 2026:** 8.545 correos analizados.

**Metodologia:** procedimiento LPA aplicado a un dominio real (judicial).
Cada caso genera jurisprudencia — no crea reglas nuevas, pero explica como
se aplicaron las existentes.

## 9.3 Monitor de LM Studio (:5000)

Ver capitulo 3.9. Dashboard de observabilidad del motor local:
- VRAM y temperatura reales (nvidia-smi)
- CPU/RAM (psutil)
- Modelos cargados y uso de API
- Servicio systemd: lmstudio-monitor.service

## 9.4 Benchmarks de modelos (lm-studio-benchmarks)

Carpeta `/home/jokoalmi/lm-studio-benchmarks/`:
- `run_one.sh` — carga modelo, ejecuta 5 tests, descarga
- `bateria_ronda3.sh` — secuencia completa de 8 modelos
- `resultados/` — JSON + logs por modelo
- Ronda 3 (1-ago-2026): 9/9 modelos probados, qwen3-14b confirmado,
  gemma-4-e4b rescatado

## 9.5 Inbox de Telegram (captura rapida)

Skill `telegram-inbox` — clasifica mensajes enviados por Telegram como:
Observacion | Idea | Imagen | Audio | Tarea | Referencia.
Solo captura y consulta — nunca ejecuta acciones destructivas sin
confirmacion en sesion CLI.

## 9.6 Experimentos LPA (dominios)

El lab produce experimentos en dominios distintos para validar que los
principios de LPA son universales:

| # | Experimento | Dominio | Hallazgo |
|---|-------------|---------|----------|
| 001 | Perfume IA | Coleccion personal | 10 organos funcionales, 12 leyes verificables |
| 002 | Bolsa | Decision financiera | Hero=precio+chart, stress-test 4/4 |
| 003 | Mente Natural | Optimizacion personal | 5 capas no emergen (8 eslabones) |
| 004 | Joko Lab | Aprendizaje humano-IA | IE=0%: LPA describe, no prescribe |
| 005 | Psicologia | Autopercepcion | IE maximo, primer dominio psicometrico |

---

<a name="capitulo-10"></a>
# CAPITULO 10 — GLOSARIO COMPLETO

## A

| Termino | Definicion |
|---------|-----------|
| Activation Engine | Busca RULE activas y las inyecta en el pipeline. No responde, solo activa |
| ai-architecture | Skill de gobierno: define QUE debe ocurrir (roles, principios) |
| ai-router | Skill de implementacion: define COMO ocurre (scripts, enrutamiento) |
| Anomalia | Check fallido o cambio detectado entre inicio y cierre de sesion |

## B

| Termino | Definicion |
|---------|-----------|
| BGE-M3 | Modelo de embeddings multilingue (1024 dims). Ganador para RAG en espanol |
| Backlog | Lista priorizada de pendientes del lab (04-operations/backlogs/) |
| Baseline | Medicion inicial de referencia (ej: verificacion determinista) |

## C

| Termino | Definicion |
|---------|-----------|
| Candidate Principle | Estado intermedio entre E3 y E4. La mayoria nunca alcanzan E4 |
| Candidate Pattern (CP) | Patron en incubacion (pattern-incubator/) |
| Checkpoint | Punto de recuperacion en medio de sesion (checkpoint.sh) |
| Confidence Decay | Envejecimiento de confianza: evidencia x recencia x validaciones x compatibilidad |
| Confidence Stamp | Wrapper estandar: confidence + confidence_label + evidence |
| Context Builder | Inyecta contexto RAG al prompt del LLM |
| Contract-first | Regla: todo componente expone contrato antes que implementacion |
| Cron | Tarea programada (Hermes o sistema) |
| Cross-session | Sincronizacion de contexto entre sesiones (CLI, Telegram, cron) |

## D

| Termino | Definicion |
|---------|-----------|
| DEC (Decision) | Decision registrada con evidencia, caducidad y revision |
| Debt Detector | Detecta deuda tecnica del conocimiento (6 checks) |
| DeepSeek | Modelo cloud principal del lab (deepseek-v4-flash) |
| decision-ledger | Registro JSONL de decisiones del router (alimenta LPA) |
| Decision Engine | Decide proveedor/modelo basado en state + policies (determinista, sin LLM) |
| Docker Compose | Orquestador de contenedores. SIEMPRE `docker compose` (v2) |

## E

| Termino | Definicion |
|---------|-----------|
| E0-E4 | Niveles de evidencia (observacion → principio) |
| E∅ | Afirmacion revocada (fue E1+ y fue falseada) |
| Embeddings | Vectores numericos que representan el significado del texto |
| Event Bus | Capitalizacion automatica (dec.created, exp.completed...) |
| Evidence Contract | Umbrales verificables para promocionar EXP → DEC |
| Experimentos | Casos de estudio (EXP-...) que aportan evidencia a LPA |
| EXP | Experimento |

## G

| Termino | Definicion |
|---------|-----------|
| GGUF | Formato de modelo cuantizado (para GPU con poca VRAM) |
| GPU bottleneck | Competencia por VRAM entre BGE-M3 y LM Studio (resuelto via API) |
| Gateway | Conexion de Hermes con plataformas (Telegram) |

## H

| Termino | Definicion |
|---------|-----------|
| Hermes Agent | El agente del lab (Nous Research) |
| HYP (Hipotesis) | Afirmacion pendiente de validacion |
| Health Score (KHI) | Salud del conocimiento 0-100 (88/100 real) |

## I

| Termino | Definicion |
|---------|-----------|
| Indexer | Script que indexa docs .md/.yaml en LanceDB |
| inicio.sh | Protocolo de apertura de sesion |
| fin.sh | Protocolo de cierre de sesion (para el stack Docker) |

## J

| Termino | Definicion |
|---------|-----------|
| JL-001..012 | Normas constitucionales del lab |
| Joko Lab | El laboratorio completo (este sistema) |
| JSONL | Formato JSON por linea (append-only, ideal para logs) |

## K

| Termino | Definicion |
|---------|-----------|
| KAP | Knowledge Assimilation Pipeline (M-001): asimilar fuentes externas |
| KEL | Knowledge Evolution Loop: maquina de estados del conocimiento |
| KO (Knowledge Object) | Entidad YAML con ciclo de vida (DEC/RULE/POLICY) |
| KVC | Knowledge Validation Cycle (CP-003): validar decisiones |
| Knowledge Resolver | Sintetiza conocimiento: hechos, conflictos, confianza |

## L

| Termino | Definicion |
|---------|-----------|
| LanceDB | Base vectorial daemonless (RAG) |
| LM Studio | Motor de inferencia local (:1234, 11 modelos) |
| LPA | Living Product Architecture — programa de investigacion |
| lms | CLI de LM Studio (load, unload, ps, ls, server) |

## M

| Termino | Definicion |
|---------|-----------|
| M-001 | KAP — procedimiento de asimilacion de conocimiento |
| MCP | Model Capability Profile (perfil de capacidades por modelo) |
| Memoria | Datos persistentes de Hermes entre sesiones |
| MoE | Mixture of Experts (arquitectura con expertos activos parciales) |

## N

| Termino | Definicion |
|---------|-----------|
| n8n | Plataforma de automatizacion de workflows (ZONA PROTEGIDA) |
| NVIDIA-SMI | Herramienta de monitorizacion de la GPU |

## O

| Termino | Definicion |
|---------|-----------|
| OBS (Observacion) | Dato E0 sin nivel de evidencia |
| OKF | Open Knowledge Format — capa curada sobre el RAG (implementado 1-ago: indice de KOs en verification/indice.md) |
| Ollama | Motor de inferencia local secundario (:11434) |
| Orchestrator | Pipeline unificado (Task Understanding → Planning → Activation) |

## P

| Termino | Definicion |
|---------|-----------|
| Pattern Incubator | Maduracion E0→E1 (obligatoria antes de KNOWN) |
| POLICY | Restriccion global (precedencia sobre RULEs) |
| Preflight Checklist | 6 verificaciones pre-respuesta |
| Pruning | Poda de conocimiento (7 operaciones, 5 fases) |
| psutil | Libreria Python de metricas de sistema (CPU/RAM) |

## Q

| Termino | Definicion |
|---------|-----------|
| QAT | Quantization-Aware Training (cuantizacion entrenada) |
| Q4_K_M | Cuantizacion 4-bit (calidad/precio equilibrada) |

## R

| Termino | Definicion |
|---------|-----------|
| RAG | Retrieval-Augmented Generation |
| Reranker | Modelo que reordena resultados por relevancia |
| RULE | Regla activa derivada de una DEC |
| Runtime | Conjunto: State Manager + Policy Engine + Decision Engine + API |
| Runtime.resolve() | Unica puerta de entrada al enrutamiento (9 campos) |

## S

| Termino | Definicion |
|---------|-----------|
| Session search | Busqueda en historial de sesiones (FTS5) |
| Shared-events | Canal de eventos compartido entre sesiones |
| Shared-state | Estado vivo de sesiones |
| Skill | Conocimiento procedimental de Hermes (SKILL.md) |
| State Manager | Observa el sistema y escribe state.json |
| Stirling PDF | Utilidades PDF en Docker (:8081) |
| systemd | Sistema de servicios (user units para LM Studio, monitor, indexer) |

## T

| Termino | Definicion |
|---------|-----------|
| Task Understanding | Deteccion del tipo de tarea por keywords (task_keywords.yaml) |
| Telemetria | Medicion del comportamiento real del sistema |
| TPS | Tokens por segundo (velocidad de inferencia) |
| Trace | Trazabilidad: que sabe, de donde, que decide, como lo demuestra |

## U

| Termino | Definicion |
|---------|-----------|
| UNKNOWN.md | Preguntas abiertas (P000-P020) |
| uv | Gestor de entornos Python |

## V

| Termino | Definicion |
|---------|-----------|
| VRAM | Memoria de video (12 GB en la A2000 — restriccion central) |
| Verificacion determinista | Banco de preguntas objetivas (anti-Goodhart) |

## W

| Termino | Definicion |
|---------|-----------|
| Watchdog | Proceso que vigila otro (telegram-watchdog, version watchdog) |
| wget -c | Descarga con resume (workaround para timeouts de lms get) |

---

## NOTAS FINALES

1. **Fuente de esta guia:** datos verificados del sistema el 1-ago-2026.
   Si algo cambio despues, los archivos reales mandan.
2. **Donde vive:** /home/jokoalmi/joko-lab/GUIA-JOKO-LAB.md
3. **Actualizacion:** cuando el lab cambie (nuevo modelo, nuevo servicio,
   cambio de arquitectura), esta guia debe actualizarse.
4. **Siguientes pasos sugeridos:** leer capitulo a capitulo en orden.
   Si quieres profundizar en cualquier seccion, pedirmelo y amplio.

---

FIN DE LA GUIA
