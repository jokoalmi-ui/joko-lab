---
title: "Análisis — Episodio 831 de atareao: «Esto es lo que le faltaba a tu IA para ser útil de verdad» (MCPs frente a skills)"
type: research
fecha: 2026-09-17
---

# Análisis — Episodio 831 de atareao: «Esto es lo que le faltaba a tu IA para ser útil de verdad» (MCPs)

**VERACIDAD:** [VERIFICADO]

**Fuente:** `https://www.youtube.com/watch?v=ZN13wNOPZ40` — título «831 - Esto es lo que le faltaba a tu IA para ser útil de verdad», canal **atareao** (`@atareao`, Lorenzo Carbonell). Metadatos leídos con `yt-dlp --print` el **17-sep-2026**: duración **1.804 s = 30 min 04 s**, subida **2026-09-14** (`20260914`), **3.606 visualizaciones**, **60 me gusta**, **7 comentarios**. El usuario lo envió dos veces (`https://youtu.be/ZN13wNOPZ40?is=ipKS6vHjams8LXXA`), pendiente desde días atrás.

**Método** (0 GPU, 0 descarga de vídeo/audio, 0 €): subtítulos automáticos con `yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs 'es.*' --sub-format vtt` → `/tmp/atareao831/ZN13wNOPZ40.es-orig.vtt` y `.es.vtt` (223,0 KiB cada uno). Limpieza: el primer intento (dedup de frases + supresión por n-gramas) **dejó triplicaciones** («Hola, soy Lorenzo y esto es Atare…» ×3) porque los *cues* se solapan **a mitad de frase**; la que funciona es el **stitching por solape palabra a palabra sobre los *cues*** → `/tmp/atareao831/stitch.txt`, **144 párrafos, 4.443 palabras, 24.397 B**, md5 `e8f0c41b2aba7da42935645960214b50`, ratio 0,11 del crudo. Texto leído íntegro. *(Lección de método aplicable a la skill de transcripción: en VTT *rolling* de YouTube el dedup por frases no basta.)*

**Relación con el mapa de la serie:** existe `research/analisis-serie-atareao-ia-local.md` (mapa de la temporada 8, episodios 789-827) cuya regla de cierre es **no analizar episodios sueltos «salvo que aporten algo nuevo al lab»**. El 831 es **posterior a ese mapa** y aporta tres cosas nuevas: (a) es el episodio donde el autor **enfrenta MCP frente a skills**, justo después del episodio sobre skills; (b) es la **primera medición externa** de coste de contexto por servidor MCP que aparece en la serie; (c) **confirma desde fuera** que el problema real es la *elección* de herramienta, no su falta.

## Cómo lo plantea

- Precedente declarado en el propio audio: en el episodio anterior sobre **skills** «no mostré ninguna concreta»; este es la continuación con MCP.
- Arquitectura en **tres capas** (cliente / servidor / host) y **JSON-RPC 2.0** como protocolo. *(En el audio suena «Jason RPC 2.0»: es ASR de JSON-RPC 2.0.)*
- Cinco ventajas que enumera: **estandarización, autodescubrimiento, eficiencia de tokens, modularidad y ser abierto** («no es de ninguna empresa»).
- Dice en directo *«te voy a hablar de estos **cinco** MCPs imprescindibles»* y a continuación recorre **siete**. La contradicción es del propio guion (dicha en vivo, no un error de transcripción). Los tres que añade respecto a los cinco «imprescindibles» son **Time**, **Memory** y **Sequential Thinking**.

## Los siete MCPs que muestra (lo que dice de cada uno)

1. **Filesystem** — leer y buscar archivos; **limitar el acceso a rutas concretas** (no a todo el sistema). Usos que propone: buscar ficheros de configuración, leer logs, diagnosticar fallos, crear notas, mover descargas. Cifra que da de coste: **3.400 tokens**.
2. **SQLite** — el **servidor oficial** (`modelcontextprotocol/servers`, el de SQLite) **«no termina de funcionar»** en su caso → usa la alternativa **`moki/mcpsqlite`**, que «funciona la mar de bien». Da SELECT (devuelve la primera fila) e INSERT. Demo con una base de datos de distribuciones Linux generada por IA.
3. **GitHub** — consultar repos, issues y PRs; pide **token** («con el token va mucho más rápido»); crear issues, revisar PRs, comentar y **aprobar o rechazar**, crear repos. Uso real que confiesa: en cada PR abierta le pide *«revisa la PR, comenta lo que encuentres y apruébala o no»*.
4. **Fetch / busca web** — `fetch` convierte una URL a **texto plano** (fuera HTML, CSS y JavaScript) y `search` busca. Dos cosas que solo tiene el MCP: **caché local** y **límite de peticiones**. Cifra: sin MCP, sacar un dato de una página ≈ **15.000 tokens**; con MCP, **50-100**.
5. **Time** — hora del sistema y de **cualquier zona horaria**, conversión entre zonas y diferencias de fechas. **El paquete oficial no existe como npm** → usa **`oneion/mcp-server-time`**. Coste: **0 tokens si no se usa** (dice).
6. **Memory** — **grafo de conocimiento local en un JSON**: entidades (personas, conceptos, proyectos), observaciones (hechos) y relaciones; resuelve la amnesia entre sesiones. Coste: **2.870 tokens**. En su demo el grafo estaba **vacío** y no encontraba nada: hay que rellenarlo para que sirva.
7. **Sequential Thinking** — guía de razonamiento **paso a paso**; el modelo documenta el pensamiento y el servidor le pregunta. Coste: **1.190 tokens**. Lo recomienda para depuración y problemas complejos; en su propia demo «se lió».

## Cuatro hallazgos transversales (lo que vale del vídeo)

1. **No determinismo en la elección de herramienta — él lo llama «realmente peligroso».** Con dos MCPs conectados a la vez (notas + SQLite) el modelo responde con el que le viene en gana; deshabilitó el de notas y «aun así hace lo que le da la gana». Es el mismo eje que el lab ya trata cuando **fija la herramienta y verifica el resultado** en vez de dejar que el modelo elija entre veinte.
2. **MCP frente a skill, dicho por él:** *«muchas de las cosas que haces con un MCP también las puedes hacer con una skill»*, y hay que mirar cuál consume menos. Coincide con la política del lab (MCP mínimos y expuestos bajo demanda; el resto, skills y tools nativas).
3. **Carga diferida (su afirmación):** sostiene que los servidores **no cargan sus tokens hasta que se necesitan** («si nunca le pides la hora, el MCP Time no carga»). Es cierto **según su cliente**; no es una propiedad del protocolo.
4. **Coste de un MCP propio:** en **Python/JavaScript** el arranque es lento y consume **50-80 MB de RAM**; en **Rust**, **4-5 MB** y arranque en microsegundos. Distingue «ideal para pruebas» (interpretado) de producción.

## Contraste medido con el lab (mapeo propio, no del vídeo)

De los siete, **cinco ya están cubiertos** por herramientas nativas o MCPs existentes del lab:

- **Filesystem** → tools nativas de fichero (`read_file`/`write_file`/`search_files`); un MCP de disco además choca con el principio de **mínimo privilegio**.
- **SQLite** → MCP **`lab-db`** (perfume-ia, cafe-ia) ya activo.
- **GitHub** → se cubre con **`gh`** por terminal.
- **Fetch/busca** → **`web_extract`/`web_search`** nativos.
- **Memory** → **MEMORY** persistente + **MEP-001** (memoria episódica); lo que **no** hay es grafo explícito de relaciones.
- **Sequential Thinking** → dudoso y, en el lab, contraproducente en coste (fuerza razonamiento paso a paso cuando el problema medido es la verificación, no el número de pasos).
- **Time** → **el único que toca un fallo real del lab**: RULE-012 (tres fallos de hora/fecha afirmadas sin ejecutar `date`). Pero la corrección es **ejecutar `date`**, no instalar un servidor; si algún día se quisiera, el dato útil es que **el oficial no existe como npm** → `oneion/mcp-server-time`.

Dos matices que separan su setup del lab:

- **Coste de contexto:** sus cifras por servidor (**1.190 / 2.870 / 3.400 tokens**) **no aplican tal cual**: la medición real del lab (F1, 16-sep) dio **619 tokens para los tres MCP juntos** (2,7 % de 23.292) porque Hermes los sirve en **catálogo diferido**. En este eje el lab ya está mejor que su cliente, por arquitectura del cliente, no por mérito de una decisión.
- **Coste de RAM:** su rango **sí se confirma hoy en el lab**, medido con `ps -eo pid,rss,etime,cmd` (17-sep): los tres servidores son **Python** y había **6 procesos** (dos instancias por servidor, arranques a las 07:49:02 y 07:51:09) con **RSS de 21,7 a 65,9 MiB** cada uno y **235,2 MiB de suma bruta** (sin descontar páginas compartidas): `mcp-lancedb` 67.480 + 23.132 KB, `mcp-sqlite (lab-db)` 55.884 + 22.180 KB, `manim-mcp (animation-server)` 47.640 + 24.528 KB. Es decir: **la carga diferida que él atribuye al protocolo no evita el proceso residente**, que es justo el coste que no mide.

## Decisión

**No se instala nada.** El vídeo no aporta componente nuevo al lab: aporta (a) **validación externa** de que el problema es la **elección** de herramienta y no la cantidad, (b) **dos datos operativos** para el día en que haga falta un MCP propio —**el servidor SQLite oficial es el que no funcionaba y la alternativa probada es `moki/mcpsqlite`; el MCP Time oficial no existe como npm y la alternativa citada es `oneion/mcp-server-time`**— y (c) **la confirmación medida** del coste de los MCP propios en Python (≈50-80 MB por proceso), que el lab paga hoy.

Queda **propuesto, no ejecutado**: si algún día se quiere dar hora fiable al agente sin depender de que ejecute `date`, la vía más barata es un MCP propio mínimo (Rust, 4-5 MB) o **nada** — la RULE-012 ya resuelve el problema por proceso.

## Verificado, no verificado, inferido

- **Verificado aquí (transcripción propia + metadatos):** identidad y cifras del vídeo (duración, fecha, vistas, me gusta, comentarios); los siete servidores; las afirmaciones en primera persona; sus cifras de su cliente; la incoherencia «cinco MCPs» → siete mostrados; el encabezado «Jason RPC 2.0» como ASR de JSON-RPC 2.0.
- **No verificado (dato suyo, sin metodología):** 15.000 → 50-100 tokens del fetch; 1.190 / 2.870 / 3.400 tokens por servidor; 50-80 MB frente a 4-5 MB; el fallo del servidor SQLite oficial (es su experiencia, no un issue comprobado); la existencia y bondad de `moki/mcpsqlite` y `oneion/mcp-server-time` (citadas por él, **no comprobadas aquí**).
- **Incoherencias del audio, no usadas como dato:** dice que graba el **1 de septiembre** y que en Tokio ya es «miércoles» (el 1-sep-2026 es **martes**); anuncia que «el próximo episodio será el **828**, el primero de la novena temporada» estando en el **831**; y menciona como último podcast publicado uno que el lab ya analizó (**827**, 31-ago-2026).
- **Inferido (mío):** el mapeo de cada MCP con su equivalente en el lab.

## Fuentes y fechas

- Vídeo: `https://www.youtube.com/watch?v=ZN13wNOPZ40` — metadatos leídos el **2026-09-17**.
- Subtítulos: `/tmp/atareao831/ZN13wNOPZ40.es-orig.vtt`, `.es.vtt` (223,0 KiB c/u); texto limpio `/tmp/atareao831/stitch.txt` (4.443 palabras, md5 `e8f0c41b2aba7da42935645960214b50`).
- Contexto interno: `research/analisis-serie-atareao-ia-local.md` (mapa T8 789-827); F1 (16-sep) para la cifra de 619 tokens de MCP; `ps` del 17-sep para el RSS.
- Coste de este análisis: **0 GPU, 0 descargas de vídeo/audio, 0 €, 0 servicios tocados, nada publicado**.
