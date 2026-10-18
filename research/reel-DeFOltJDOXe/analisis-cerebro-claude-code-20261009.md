---
title: "Análisis reel notfound404.es (DeFOltJDOXe) — «El cerebro» para Claude Code / Codex + tutorial de YouTube"
type: research
source: "https://www.instagram.com/reel/DeFOltJDOXe/"
pieza_2: "https://youtu.be/1T5b47WEcQs"
account: notfound404.es
published: 2026-10-04
analyzed: 2026-10-09
tags: [claude-code, codex, memoria, contexto, agentes, tutorial]
---

# Reel «el cerebro» (IG notfound404.es, DeFOltJDOXe) + tutorial completo en YouTube

## 0. Las dos piezas (extracción completa)
- **Reel IG** `DeFOltJDOXe` · cuenta **notfound404.es** · publicado **4-oct-2026** · **328 likes, 323 comentarios** · vídeo 720x1280 h264/aac, 5.376.921 B (descargado y transcrito).
- **Tutorial completo** (lo que el reel anuncia): YouTube **`1T5b47WEcQs`** — «*Cómo crear un cerebro para Claude Code y ChatGPT FÁCIL*» · **346 s** (5:46) · **6.935 visualizaciones** · publicado **2026-10-04 11:13 (-07:00)** · canal **@NOTFOUND404dev**.
- Canal localizado por la página de enlaces del autor (`notfound404.es/links`), no por búsqueda a ciegas.
- Método: `og:*` + descarga del MP4 + transcripción (whisper) + 12 frames por escena (GLM-4.6V) para el reel; para YouTube, transcript oficial (6.578 chars) + descripción completa (4.637 chars, vía `ytInitialPlayerResponse`).

## 1. Qué dice el reel (transcripción literal, resumen sin alterar cifras)
- «En el vídeo del cerebro muchos me pedisteis un tutorial… **pero no aquí**: esta plataforma está hecha para gente dopamínica, aquí nadie aguanta más de un minuto».
- El cerebro = «**una carpeta con una ficha por proyecto**»; con ella el agente «sabe cómo va todo sin que se lo expliques otra vez».
- El tutorial está «en una plataforma mejor: **YouTube**, de principio a fin, **cinco pasos, sin programar**; copias los prompts de la descripción y los pegas en Claude Code».
- «El **mismo cerebro sirve para ChatGPT (Codex)**»; dura menos de 6 minutos, gratis; pide like/suscripción y «comenta TUTORIAL y te paso el enlace».
- Caption: «Necesitas **Claude Code, que va con plan de pago**»; etiquetas `#claudecode #ia #chatgpt`.

## 2. El método «cerebro» (tutorial de YouTube, 5 pasos)
1. **Demostración (0:29)** — Abre Claude Code y pregunta por un proyecto sin dar pistas: no recorre el disco, lee **una ficha** del cerebro y contesta.
2. **Qué es (0:42)** — Una **carpeta** con **una ficha por proyecto**; cada ficha dice tres cosas: **qué es, cómo va y dónde están sus archivos**. «No copia nada, solo apunta». Arriba, un **índice** con una línea por ficha: el agente lee el índice (cortísimo) y abre **solo** la ficha que necesita → gasta pocos tokens. Al ser texto plano, lo lee **cualquier IA**.
3. **Paso 1 (1:47)** — Crear la carpeta `cerebro` con subcarpeta `ramas/`; el agente pregunta **de una en una** dónde guardas los proyectos y en qué áreas divides el trabajo (3-6); crea una rama por área y una ficha Markdown por proyecto; crea `cerebro/INDICE.md`.
4. **Paso 2 (2:26)** — Anatomía de la ficha: cabecera con **id / estado / alias**, una línea de *qué es*, la sección clave **«Cuándo entrar aquí»** (sin eso «la IA no sabe que tiene que abrirla»), **Estado** (cómo va hoy) y **Dónde está** (rutas; sin copiar archivos). Regla dura: **cada ficha cabe en una pantalla**.
5. **Paso 3 (3:06)** — Añadir el bloque «El cerebro» al **`CLAUDE.md`** global (`~/.claude`): mirar el cerebro antes de recorrer el disco; **escribir en el cerebro sin que se lo pidas**; el estado **se sobrescribe** (las fichas no crecen); **nunca contraseñas ni datos bancarios**.
6. **Paso 4 (3:43)** — Prueba real: cerrar y reabrir; preguntar por un proyecto (debe leer índice + una ficha); después contarle algo nuevo («el taller ha aceptado el presupuesto») y comprobar que **lo apunta solo**.
7. **Paso 5 (4:11)** — El cerebro es **tuyo, no de Claude**: el mismo bloque se pega en **`AGENTS.md`** (`~/.codex`) y **Codex/ChatGPT lee lo mismo**; si a una IA se le acaba la cuota, la otra sigue donde lo dejó.
8. **Mantenimiento (4:35)** — Tres reglas: **cada dato en un solo sitio**; **lo que se acaba se archiva** (rama `archivo`); **revisión mensual** (fichas con estado viejo, rutas rotas, fichas de más de una pantalla, fichas fuera del índice).
9. **Buscador (4:55)** — Con ~100 fichas va sobrado; el suyo tiene casi 200 y añadió **`cerebro.py`**: `scan` indexa todas las fichas en **SQLite con FTS5** (`.index/cerebro.db`, índice desechable), `buscar PALABRAS` devuelve hasta 10 fichas con id/ruta/fragmento, `contexto ID` imprime la ficha entera.

## 3. Los 4 prompts (literales, copiables)
**PROMPT 1 · CREAR EL CEREBRO**
> Quiero montar un "cerebro": una carpeta que sea el índice de todos mis proyectos, para que tú y cualquier otra IA sepáis dónde está cada cosa sin recorrer el disco.
> 1. Crea la carpeta "cerebro" en mi carpeta de usuario, con una subcarpeta "ramas".
> 2. Hazme dos preguntas, de una en una: en qué carpeta guardo mis proyectos, y en qué áreas se divide mi trabajo (de 3 a 6; por ejemplo: web, vídeos, clientes, proyectos).
> 3. Mira esa carpeta por encima (solo nombres de carpetas, sin abrir archivos) y crea una rama (subcarpeta de "ramas") por área y, dentro, una ficha en Markdown por proyecto.
> Cada ficha lleva, en este orden: una cabecera con "id" (su ruta dentro del cerebro, por ejemplo clientes/taller-ruiz), "estado" y "alias" (otros nombres con los que lo llamo); una línea que diga qué es; "Cuándo entrar aquí" (en qué casos esta ficha es la respuesta); "Estado" (cómo va hoy, en dos o tres líneas); y "Dónde está" (las rutas de sus archivos; no copies ningún archivo, solo apunta a su ruta).
> 4. Crea cerebro/INDICE.md con una línea por ficha: su id, qué es en pocas palabras y su estado.
> Reglas: cada ficha cabe en una pantalla. Nunca contraseñas, datos bancarios ni documentos de identidad. Lo que no sepas, pregúntamelo en vez de inventarlo. Al acabar, enséñame el árbol de lo que has creado.

**PROMPT 2 · QUE CLAUDE LO MIRE SIEMPRE** (va al `CLAUDE.md` global; el mismo bloque para Codex en `AGENTS.md`)
> Añade este bloque a mi CLAUDE.md global (está en mi carpeta de usuario, dentro de .claude; si no existe, créalo). No toques lo que ya haya.
> ## El cerebro
> En la carpeta "cerebro" de mi carpeta de usuario hay un índice de todos mis proyectos.
> - Antes de recorrer el disco o buscar archivos, lee cerebro/INDICE.md y abre solo la ficha que haga falta.
> - Escribe en el cerebro sin que te lo pida: si te cuento algo nuevo o cambia algo (un proyecto, un cliente, un plazo, una decisión), actualiza su ficha o créala, y añádela al índice.
> - El estado se sobrescribe: las fichas no crecen. Lo que se acaba pasa a la rama "archivo".
> - Nunca guardes contraseñas, datos bancarios ni documentos de identidad.

**PROMPT 3 · REVISIÓN MENSUAL**
> Revisa mi cerebro (la carpeta "cerebro" de mi carpeta de usuario) y dame un informe, sin cambiar nada todavía: fichas con el estado viejo, rutas de "Dónde está" que ya no existen, fichas que ocupan más de una pantalla y fichas que no están en INDICE.md. Después pregúntame qué arreglas.

**PROMPT 4 · EL BUSCADOR** (necesita Python)
> Dentro de mi carpeta "cerebro", crea cerebro.py: un programa de terminal en Python, solo con la librería estándar. "python cerebro.py scan" lee todas las fichas de ramas/ y las indexa en una base SQLite con búsqueda de texto (FTS5) en cerebro/.index/cerebro.db; el índice es desechable, la verdad son las fichas. "python cerebro.py buscar PALABRAS" devuelve como mucho 10 fichas que coincidan, con su id, su ruta y un fragmento. "python cerebro.py contexto ID" imprime la ficha entera. Pruébalo con dos búsquedas y enséñame el resultado. Después cambia el bloque "El cerebro" de mi CLAUDE.md para que use "buscar" antes que el índice.

**Instalación de Claude Code** (la del vídeo; requiere plan de pago): Windows `irm https://claude.ai/install.ps1 | iex` · Mac/Linux `curl -fsSL https://claude.ai/install.sh | bash`.

## 4. Aplicabilidad al Joko Lab (OBS → HYP)
- **CONFIRMA** tres criterios ya vigentes en el lab: (a) «cada dato en un solo sitio» ↔ el defecto real de duplicados en la BD de perfumes (id 926 vs 1055); (b) «nunca contraseñas ni datos bancarios» ↔ la norma de credenciales en fichero local `chmod 600`, nunca impresas; (c) «lo que se acaba **se archiva**» ↔ `AGENTS.md` §2 «no se borra: se archiva». También confirma el gobierno de contexto (`skill-compaction`): índice corto → leer solo lo necesario.
- **NUEVO / accionable**:
  1. **Ficha por proyecto con «Cuándo entrar aquí»**. El lab tiene `pendientes.md` (782 líneas, 233 KB) que **crece** y `GUIA-JOKO-LAB.md` como índice general, pero **no fichas por proyecto** (`perfume-ia`, `cafe-ia`, `automation-stack`, `lmstudio_real_monitor`) con estado sobrescribible. La sección «Cuándo entrar aquí» es justo lo que permite a un agente decidir **sin** recorrer el disco.
  2. **Revisión mensual con informe y sin tocar nada** (fichas viejas, rutas rotas, fichas de más de una pantalla, fichas fuera del índice). Encaja con el cron de higiene `detectar-sin-uso`, pero aquí el informe es sobre la documentación, no sobre procesos.
  3. **Buscador FTS5 de las propias fichas** (`scan` / `buscar` / `contexto`). El lab tiene RAG LanceDB (~21K notas) para corpus grande; un índice FTS5 de los documentos del lab sería la pieza barata y local para consultas puntuales, sin modelo de embeddings.
- **Límite honesto**: no hace falta «montar un cerebro» desde cero ni instalar Claude Code (el tutorial lo exige con plan de pago). El equivalente del lab ya existe (`AGENTS.md`, RULEs, skills, `GUIA-JOKO-LAB.md`) y es más estricto. Lo aprovechable son **las tres piezas de §4**: ficha con «cuándo entrar», revisión mensual y buscador FTS5 — y se pueden implementar con Hermes, sin Claude Code.
- **Riesgo detectado**: la carpeta «cerebro» del tutorial vive en la carpeta de usuario y el agente **escribe en ella sin que se lo pidas**; en el lab eso choca con la norma de escritura autorizada (RULE-018) → si se replicara, la escritura debería quedar en rutas de lab y con el visto bueno del patrón.

## 5. Verificación y artefactos
- Datos del tutorial (título, duración 346 s, 6.935 vistas, fecha 2026-10-04, capítulos, descripción con los 4 prompts) leídos de `ytInitialPlayerResponse` del propio vídeo; transcript oficial de 6.578 chars.
- Descarga de frames de YouTube: **no disponible** en esta ejecución (el `yt-dlp` del lab no bajó el vídeo: «vídeo no disponible»); el contenido del tutorial está íntegro en audio/descripción, así que no afecta al análisis.
- Glosario de Whisper: transcribe «Claude Code» como «Kloz/Cloud/Cloth Code» y «Codex» como «Chat GPT»; el original escrito (descripción) confirma los nombres.
- Artefactos: `reel_transcripcion.txt`, `reel_metadatos.json`, `yt_1T5b47WEcQs_transcripcion.txt`, `yt_1T5b47WEcQs_descripcion.txt`, 12 `frame_NN.jpg` y `reel.mp4` (jpg/mp4 fuera de git por `.gitignore`).
