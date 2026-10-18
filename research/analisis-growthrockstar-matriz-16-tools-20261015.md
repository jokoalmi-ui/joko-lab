# Análisis — post @growthrockstar: «La matriz de programación con IA» (Defhr5-IPXQ)

**VERACIDAD:** [ALCANCE INTERNO]
**Fecha del análisis:** 2026-10-15 17:18:34 (medida con `date`)
**Fuente:** https://www.instagram.com/p/Defhr5-IPXQ/ — cuenta **@growthrockstar**
**Formato:** carrusel de **2 slides** (`media_type 8`, `carousel_media_count 2`, leído en el nodo del shortcode dentro del JSON del feed a las ~16:0x del 15-oct)
**Fecha del post:** la que imprime su propio `og:description` — «el October 14, 2026». La etiqueta relativa del feed marcaba «16 h» a las 17:1x del 15-oct. **No se ha leído `taken_at`**.
**Interacciones (`og:description`, 15-oct 17:1x):** **16 likes · 0 comentarios** (literal: «16 likes, 0 comments - growthrockstar el October 14, 2026»). Es un contador en vivo: a las ~16:0x del mismo día marcaba 15 likes.
**Método:** caption por `og:description` de la página del post, leído con el navegador (`chrome-lab`, CDP) y **volcado literal** a `/tmp/ig-defhr/og_caption.txt` (1.030 B, md5 `e975c74a26263c045110b90b9049d4f5`). El `curl` de la MISMA URL devuelve HTTP 200 y 589.121 B pero **sin** el caption (0 apariciones de «sobrevaloradas» en `/tmp/ig-defhr/pagina.html`): para `curl` hay muro. Portada descargada aparte a `/tmp/ig_defhr_s1.jpg` (1080×1349, HTTP 200) y **no transcrita**. Cobertura del lab medida con `rg -il "<término>" /home/jokoalmi/joko-lab | wc -l` (15-oct 17:1x).

## Qué es
Una **matriz 2×2 de 16 herramientas de programación con IA**. Titular del caption, **literal**: «La matriz de programación con IA: herramientas ordenadas según qué tan sobrevaloradas o infravaloradas están (eje vertical) y qué tan élite o comunes son (eje horizontal).». Los cuatro cuadrantes, también **literales**:
- «Comunes y sobrevaloradas: Replit, v0, Lovable y Bolt.»
- «Élite y sobrevaloradas: Cursor, Windsurf, GitHub Copilot y Claude Code.»
- «Comunes e infravaloradas: Cline, Aider, Goose y Kilo Code.»
- «Élite e infravaloradas: OpenCode, Codex, Hermes y OpenHands.»

Cierra con el CTA al **«Curso Xtreme Growth AI»** («🔗 Link en la bío para más información») y la frase de captación «Guardalo. No te va a volver a salir.».

**Es una OPINIÓN, no un dato.** El post no declara criterio, ni metodología, ni fecha de medición, ni una sola métrica: la posición de cada herramienta es atribución del autor. No hay cifra que contrastar (los únicos números del post son los contadores de Instagram). Lo único aprovechable como material es la **taxonomía** (eje sobre/infravalorado × élite/común), **no** la clasificación.

## Cobertura real en el lab (ficheros que mencionan el término, 15-oct 17:1x)
| Herramienta | Cuadrante del post | Ficheros en `~/joko-lab` |
|---|---|---|
| OpenCode | élite e infravalorada | 74 |
| Codex | élite e infravalorada | 41 |
| Hermes | élite e infravalorada | 464 |
| OpenHands | élite e infravalorada | 6 |
| Cursor | élite y sobrevalorada | 42 |
| Windsurf | élite y sobrevalorada | 3 |
| GitHub Copilot | élite y sobrevalorada | 11 |
| Claude Code | élite y sobrevalorada | 55 |
| Cline | común e infravalorada | 7 |
| Aider | común e infravalorada | 9 |
| Goose | común e infravalorada | 2 |
| Kilo Code | común e infravalorada | 1 |
| Replit | común y sobrevalorada | 2 |
| v0 | común y sobrevalorada | 173 |
| Lovable | común y sobrevalorada | 10 |
| Bolt | común y sobrevalorada | 16 |

Patrón: `rg -il "<término>" /home/jokoalmi/joko-lab | wc -l`. Son **ficheros que mencionan la cadena**, no uso efectivo. Tres términos son ruido y no se deben leer como presencia: `hermes` (464: es el orquestador del lab, no la herramienta homónima), `v0` (173: caza versiones `v0.x`) y `bolt` (16: otras acepciones). Los demás sí se leen como rastro real (docs, skills, research, scripts).

**Lo que de verdad está en el lab, con fichero propio:**
- **OpenCode** — `tools/opencode-local.sh` (4.684 B) y la skill `opencode` (delegación de código).
- **Aider** — `tools/aider-lab.sh` (1.428 B), que el autor coloca en el cuadrante «común».
- **Hermes** — el propio orquestador (Hermes Agent).

3 de las 16 coinciden con la elección previa del lab y las 3 caen en los cuadrantes que el autor llama infravalorados. Eso **no valida la matriz** (no mide nada): solo dice que el lab y el autor señalan los mismos nombres. Sin rastro propio de uso: Kilo Code (1), Goose (2), Replit (2), Windsurf (3), OpenHands (6), Cline (7).

## Encaje con el lab
- **Aporta**: una taxonomía discutible para el eje «qué herramienta usar para delegar código», y 6 nombres sin evaluar (Cline, Goose, Kilo Code, OpenHands, Windsurf, Replit) que serían material de un futurible si algún día se quiere comparar delegación.
- **NO aporta**: técnica, método, medición, recurso descargable ni código. El único recurso que ofrece es un **curso de pago externo** (ni local-first ni verificable).

## Lo que NO se puede afirmar
- No se ha leído la **slide 2** (muro de login: probadas la clave directa, `?img_index=2` y `/embed/captioned/`, que hoy sirve solo la portada). Si la slide 2 dice algo distinto del caption, no está aquí.
- **No hay transcripción** de la portada: la imagen está descargada y no se ha pasado por VLM en este análisis.
- Los **33,9K seguidores** proceden de la captura del embed a las 16:0x y **no se re-verifican**: `/embed/captioned/` devuelve ya la página genérica `@embed` (que imprime «0 seguidores»: un falso cero que no mide nada). No se usa como cifra.
- Los conteos del lab son de **menciones**, no de uso: no dicen si la herramienta se usa, se descartó o solo se nombra.
- La **fecha del post** es la que imprime su `og:description` (14-oct-2026); no hay `taken_at` leído.

## Estado del lab devuelto
- **Ningún modelo cargado ni descargado** por este análisis: no se usó VLM (la slide 2 no era accesible y la portada no se ha transcrito).
- Sin tocar: `n8n`, Docker, `automation-stack`, `/mnt/ssd_ia_datos/`, LM Studio, `~/.hermes/config.yaml`. Sin commit ni push.
- **Registro de la escritura**: entrada del 15-oct en `04-operations/backlogs/pendientes.md` (marca `ig-defhr-matriz-20261015`), tras el anexo: 300.175 B / 1.286 líneas (md5 `0b6e08c33f777c894a667c3257dff5a6`); antes 297.653 B / 1.272 líneas (md5 `198956c4e73bf75c86bba7f4d27259d8`); aporta 2.521 B. Backup `pendientes.md.bak-ig-defhr-matriz-20261015` (297.653 B, md5 `198956c4e73bf75c86bba7f4d27259d8`).
