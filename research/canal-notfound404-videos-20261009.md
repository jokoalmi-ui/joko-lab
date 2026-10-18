# Canal `notfound404.es` — 4 vídeos de YouTube analizados (post-hit vs pre-hit)

Fecha del análisis: 2026-10-09 · Autor del canal: NotFound404 (Baix Penedès) · Canal YT `UCBYcKHnzmc9nkOXCRJ0VZJQ` (`@NOTFOUND404dev`, 218 subs)
Método: transcripción oficial de YouTube (`tools/analizar_youtube_completo.py`) + fotogramas (10 en 3 de los 4 vídeos; el primero no generó frames) + contraste de **cada afirmación verificable** contra la fuente oficial que el propio vídeo cita. Se analizan 4 de los 9 vídeos del canal: los 2 más recientes (después del vídeo viral del «cerebro» del 4-oct) y los 2 más antiguos (antes: 8 y 9-sep).

## 1. Los 4 vídeos, en números

| id | título | fecha | dur | vistas | likes | coments | descripción |
|---|---|---|---|---|---|---|---|
| `Jk2vt4-lZ8Q` | Marca de agua de ChatGPT: mi skill para intentar romperla | 6-oct | 73 s | **706** | 22 | 3 | skill publicada gratis + fuente oficial + límites declarados |
| `PCDz107gxOA` | Mods de Claude Code: 3 usos de los que nadie habla | 8-oct | 54 s | **237** | 6 | 1 | requisito de versión, `/plugin`, aviso de seguridad, doc oficial |
| `Hd70NYZd7mo` | El comando de ChatGPT que desmonta completamente tu producto | 9-sep | **25 s** | 74 | 4 | 1 | una línea, sin fuente, CTA «comenta guía» |
| `YyOHlBD14xM` | 3 Comandos ocultos de ChatGPT | 8-sep | **28 s** | 36 | 4 | 0 | una línea, CTA «sígueme que en mi bio…» |

Contexto del canal: mediana pre-hit ≈ 50-70 vistas; vídeo «cerebro» (4-oct) = 6.937 (outlier ×100); siguientes 1.016 / 706 / 237.

## 2. Vídeo `Jk2vt4-lZ8Q` (marca de agua de ChatGPT) — **el más sólido del canal**

Tesis: OpenAI pone una marca de agua invisible (`textGrain`) en los textos de ChatGPT en la UE; él monta una skill para Claude que reescribe el texto (cambia estructura, palabras y ritmo) y **no afirma que funcione**.

Verificación de sus 4 afirmaciones:
- «No son caracteres ocultos ni metadatos: es un patrón estadístico en las palabras» → **VERIFICADO** (openai.com/index/eu-text-provenance, 5-oct-2026 + informe técnico `textGrain`).
- «Con el 25 % de las palabras cambiadas por sinónimos, su detector pasa del 92 % al 17 %» → **VERIFICADO, literal**: OpenAI publica «replacing 10% of words with synonyms reduced detection from about 92% to 66%. Replacing 25% of words reduced it to 17%» (pasajes de 400 tokens, inglés, datos ELI5).
- «El detector no es público: OpenAI solo se lo da a investigadores y organizaciones aprobadas» → **VERIFICADO** (la propia web lo dice).
- «Claude también marca sus textos desde agosto y en todo el mundo» → **VERIFICADO**: Anthropic anunció el 11-ago-2026 (efectivo 2-ago, obligación Art. 50 del Reglamento europeo de IA), modelos ≥2-ago, mundial, sin opt-out, método SynthID-Text.

Cita al final, fuera de guion: «no puedo demostrar que funcione… puede que no borres la marca, puede que solo la cambies por otra» + opinión propia: «esto no va a pillar a quien quiera esconderse, va a pillar a quien no sabía que existía». Cierra con pregunta a la audiencia y ofrece una segunda parte.
Nota: es **dato de terceros bien citado**, no método propio vendible — coherente con el patrón del canal (herramienta verificable + empaquetado), aquí con honestidad explícita sobre el límite.

## 3. Vídeo `PCDz107gxOA` (mods de Claude Code)

3 usos: (1) sesiones que se hablan entre sí (una planifica, otra construye), (2) panel propio dentro de Claude Code, (3) desviar lo fácil a un modelo más barato. Más: «solo hay que describir el mod, Claude lo escribe».
Verificación: la **doc oficial existe** en la URL exacta que da (`code.claude.com/docs/en/plugins/mods/overview`) y dice lo mismo (un mod es un plugin que cambia aspecto y comportamiento, con manejadores en JS/TS; se crea describiéndolo en una sesión). El **aviso de seguridad** («un mod se ejecuta con tus permisos y puede leer tus archivos») coincide con la doc. La versión mínima que cita (`2.1.287`) **no verificada** (dato menor).
Valor: pieza corta, con requisito, ruta de instalación y aviso. Es la versión honesta de un vídeo «3 trucos».

## 4. Vídeos pre-hit (`Hd70NYZd7mo` 9-sep, `YyOHlBD14xM` 8-sep) — **relleno de captación**

- `Hd70NYZd7mo` (25 s, 74 vistas): «escribes `/exploded w` con la foto de tu producto → imagen desmontada» + ElevenLabs (imagen→vídeo) para animaciones de scroll. Termina: «si quieres la guía completa comenta guía y te paso el link». Sin fuente, sin límites, sin método.
- `YyOHlBD14xM` (28 s, 36 vistas): «`/together` (foto tuya + foto de un famoso → foto juntos), `/transfer outfit` (cambiar ropa), `/pro shot` (foto profesional)» + «sígueme que en mi bio tienes una lista de comandos».
Verificación: **`/pro shot`, `/together` y `/transfer outfit` no son comandos oficiales de OpenAI**; circulan como «códigos de ChatGPT para fotos» recopilados por terceros, y las propias recopilaciones advierten de que «no todos forman parte de una lista oficial y su funcionamiento puede variar». Es decir: contenido **no verificable**, reciclado de un formato viral ajeno, con CTA de captación. La promesa concreta de este vídeo (foto con un famoso) es la versión más agresiva del formato.

## 5. El patrón medido: el canal cambió de formato después del vídeo viral

| | pre-hit (8-9 sep) | post-hit (6-8 oct) |
|---|---|---|
| duración | 25 s y 28 s | 54 s y 73 s |
| transcripción | 495 y 557 chars | 1.155 y 1.521 chars |
| fuentes citadas | 0 | 2 documentos oficiales |
| límites declarados | 0 | sí, explícitos en ambos |
| cierre | «comenta guía», «sígueme» | pregunta abierta + artefacto publicado gratis |
| vistas | 36 y 74 | 237 y 706 |

Los dos vídeos post-hit son **verificables de principio a fin**; los dos pre-hit no contienen ninguna afirmación comprobable. El cambio es de formato y de rigor, no de tema (los cuatro son «comando/truco de IA para…»).

## 6. Corrección de la valoración previa (09-oct, misma fecha)

En la valoración del canal (`canal-notfound404-valoracion-20261009.md`) se dijo que «los 3 siguientes sostienen el tirón». Con los datos de estos 4 vídeos, la lectura correcta es:
- El vídeo «cerebro» (6.937) **sigue siendo un pico aislado**: los publicados después hacen 1.016 / 706 / 237.
- Lo que sí cambió de forma sostenida es la **base**: de ~50-70 vistas de mediana (pre-hit) a ~250-700 en los vídeos nuevos (×3 a ×10). El canal se ha nivelado hacia arriba, pero **no** ha retenido el nivel del outlier.
- Los **comentarios** (1-3 en los 4 vídeos de YouTube) confirman que el embudo «comenta X» es un fenómeno de **Instagram** (323 y 441 comentarios en los reels del 4 y 3-oct), no de YouTube.

## 7. Qué es aplicable al lab

1. **Formato «dato + límite + fuente + pregunta»** (vídeo de la marca de agua): es exactamente la forma que exige el gate de veracidad del lab, y sirve para LinkedIn: afirmar solo lo verificado, declarar explícitamente lo que no se puede comprobar, enlazar la fuente oficial y cerrar con pregunta. **Aplicable ya.**
2. **Publicar el artefacto completo y gratis** (la skill, en el blog) como imán: mismo patrón que las recetas públicas del lab.
3. **Los 3 usos de los mods de Claude Code** son un mapa conceptual del enrutado y la orquestación del lab (sesiones que se coordinan; panel de estado; desviar lo fácil a un modelo barato = `ai-router`). **No instalar** mods ni tocar Claude Code (RULE-016).
4. **Marca de agua (`textGrain` / Anthropic)**: dato relevante y verificado para decidir qué se publica: el texto salido de ChatGPT/Claude queda marcado (mundial, sin opt-out); el de modelos locales del lab, no. Afecta a cómo se etiqueta el contenido publicado.

## 8. Veredicto actualizado

Se mantiene **7/10 con filtro**, con un matiz importante y nuevo: **en YouTube el autor es prudente y verifica; en Instagram vende hypérbole**. Los dos vídeos nuevos de YouTube declaran sus límites y citan la fuente oficial, mientras el reel del mismo autor dice «Claude ha matado a los Motion Designers». Por tanto:
- **Canal de YouTube: seguimiento útil.** Es la parte del embudo donde publica método verificable y reconoce lo que no puede probar. Las piezas de 8-9 sep (comandos no oficiales con CTA) quedan como lo que eran: arranque del canal buscando alcance.
- **Lo que NO hay que copiar**: el reciclaje de «comandos ocultos» sin fuente ni comprobación, y el gancho agresivo de Instagram.
- **Señal de degradación ya vista** (una de las fijadas en la valoración): el material útil convertido en simple gancho de venta. En YouTube, de momento, ocurre lo contrario.
