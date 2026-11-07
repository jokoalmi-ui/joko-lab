## 2026-11-07 06:49 - Post de @0xsojalsec: el loop de 3 ficheros de Karpathy (autoresearch)
**VERACIDAD:** [ALCANCE INTERNO]

**Fuente**: instagram.com/p/DfYeovSj46H (Md ismail Sojal, @0xsojalsec), 05-nov-2026,
213 likes, 0 comentarios. No es video: `yt-dlp` responde "There is no video in this
post", asi que el contenido se extrae de `og:title`/`og:description`.
Recurso que difunde: `karpathy/autoresearch` en GitHub, que el post presenta como
"Karpathy's 3-file loop runs AI research all night". Cierre del caption:
"Sheet From : Buzzoni" (el post redistribuye material de un tercero).

### Que es el recurso (verificado en la fuente primaria)

- Repo de Karpathy creado el 2026-03-06, ultimo push 2026-03-26 (API de GitHub,
  medido el 07-11-2026).
- El README dice: "The repo is deliberately kept small and only really has three
  files that matter": `prepare.py` (constantes, preparacion de datos y
  evaluacion; marcado "Not modified"), `train.py` (modelo GPT, optimizadores
  Muon + AdamW y bucle de entrenamiento: el fichero que edita el agente) y
  `program.md` (las instrucciones, que edita el humano).
- Presupuesto declarado: "By design, training runs for a **fixed 5-minute time
  budget** (wall clock, excluding startup/compilation)". Metrica unica: "The
  metric is **val_bpb**" (validation bits per byte, mas bajo es mejor).
- Rendimiento declarado: "approx 12 experiments/hour and approx 100 experiments
  while you sleep".

### Cifras del post frente a la fuente

- Stars: el caption dice "98,844 GitHub stars"; la API mide 99.416 stars y
  13.701 forks el 07-11-2026. Es crecimiento desde el 05-11, no un error.
- "5 minutes per experiment, about 12 an hour, roughly 100 by morning": coincide
  con el README (12/h y ~100).
- Licencia "MIT": el README la declara en su seccion License, pero el repo NO
  tiene fichero LICENSE en la raiz (la API `contents/` no lo lista y el objeto
  `license` de la API viene vacio). Se cita como declaracion del README, no como
  fichero del repo.
- "the agent is told never to stop and ask 'should I keep going?'": NO aparece en
  el README (0 coincidencias de "pause to ask"). Es un claim del post, no
  verificado en la fuente primaria.

### Cruce con el lab

- El PATRON ya esta implementado aqui, y no como copia: `EXP-ITER100-20261104` es
  un bucle de 100 rondas con metrica y tres puertas (norma, maqueta, gate 17/17),
  con la ronda 1 medida en 350,7 s (literal del registro: "ronda 1 = **350,7 s**"). Tambien `auto-mejora-lab`,
  `retrabajo_ledger.jsonl`, `bolsa-autonoma` y el ciclo LPA trabajan con la misma
  forma: una metrica escalar por ronda y decision de quedarse o revertir.
- Equivalencias: `program.md` aqui es la skill o el procedimiento; `train.py` es
  el artefacto que se edita; la metrica unica ya existe.
- Lo que el lab NO hace y el repo tampoco resuelve: entrenar modelos. El repo es
  una instalacion de entrenamiento de nanochat en una GPU, y el lab no entrena.
  No es un futurible de herramienta.

### Lo que NO se adopta

- "No pares a preguntar si continuar": incompatible con la norma del lab de no
  actuar sobre servicios ni ficheros sin confirmacion explicita. Se descarta esa
  parte del prompt, no el patron.
- No se instala el repo ni se descarga el modelo: no hay nada que medir aqui.

### Lo que si aporta (2 piezas, sin instalar nada)

1. **Presupuesto de tiempo FIJO por ronda.** El README fija 5 minutos de reloj
   con independencia de lo que cambie el agente, para que las rondas sean
   comparables entre si. En EXP-ITER100 la duracion varia por ronda, asi que dos
   rondas con trabajo distinto no son comparables por la metrica sola.
   Aplicacion: tope de reloj por ronda y el tiempo consumido como campo de la
   fila del ledger.
2. **Desempate por parsimonia.** El caption: "a tiny gain that adds 20 hacky
   lines gets thrown out" y "the same score with less code stays". El lab mide
   puntuacion pero no penaliza el crecimiento del artefacto; con 31 skills de
   28 KB o mas (medido el 07-11-2026), el criterio "misma puntuacion con menos
   codigo se queda" es aplicable a la poda de monolitos y al refactor.

### Veredicto

REFERENCIA EXTERNA: valida parcialmente el patron que el lab ya ejecuta
(EXP-ITER100) y aporta dos criterios concretos (presupuesto fijo por ronda y
desempate por parsimonia). No hay herramienta que adoptar ni experimento que
abrir. No entra como conocimiento validado: el repo no se ha ejecutado aqui.

### Negativos

- No se ha descargado ni ejecutado el repo.
- No se ha medido ninguna cifra de entrenamiento: no es el objeto del analisis y
  no hay GPU reservada para 5 minutos x 12 experimentos.
- El caption no se ha contrastado con imagenes: el post no es video y no se ha
  descargado la imagen. El veredicto se apoya en el caption y en la fuente
  primaria.
- `autoresearch` no aparecia antes en `research/`, backlog ni `pendientes.md`
  (grep del termino y del shortcode: 0 coincidencias en ficheros vivos).
