---
title: "Análisis reel notfound404.es (DeCtOohDB2h) — animaciones con Remotion + Claude Code"
type: research
source: "https://www.instagram.com/reel/DeCtOohDB2h/"
account: notfound404.es
published: 2026-10-03
analyzed: 2026-10-09
tags: [claude-code, remotion, motion-graphics, video, agentes]
---

# Reel «Claude ha matado a los Motion Designers» (IG notfound404.es, DeCtOohDB2h)

## 0. Fuente y métricas (09-oct-2026)
- **282 likes · 441 comentarios** · publicado **3-oct-2026** · duración **56,25 s** · 720x1280 h264/aac · 5.108.985 B.
- Tercer reel del mismo autor analizado en el lab (los otros dos: `DeH6T4FDLa3` ECC, `DeFOltJDOXe` «cerebro»).

## 1. Qué dice (transcripción literal, 1.037 B)
- Gancho: «**Claude ha matado a los Motion Designers**. Ahora puedes crear las animaciones de tus vídeos desde cero sin salir de Claude».
- Paso 1: instala las **skills oficiales de Remotion** (`npx skills add remotion-dev/skills`). «Remotion hace vídeo con código, y escribir código es lo que mejor hace Claude. **Es gratis si trabajas solo**».
- Paso 2: «pídele que te cree una **skill con tu estilo**: colores, tipografía y ritmo, para que todas tus animaciones parezcan de la misma marca».
- Paso 3 — «**lo que casi nadie cuenta**»: «hice la misma animación **5 veces**, unas con Opus 5.5 y otras con Sonnet 5.5, **y ganó Sonnet, que es el barato**. El truco no es el modelo, es cómo se lo pides: (a) pásale un **vídeo de referencia**, (b) descríbele la escena **paso a paso, como un director**, (c) pídele que **mire sus propios fotogramas** y se corrija».
- Cierre: «lo que estás viendo ahora mismo lo ha hecho Sonnet» + **CTA «Comenta MOTION y te paso la guía»**.
- Caption: reproduce los 3 pasos y añade el matiz de licencia — «gratis para una persona sola y para equipos de hasta 3».

## 2. Frames (12 por escena, GLM-4.6V) — texto en pantalla
- Personaje fijo: encapuchado con **máscara y gafas**, dos monitores, luz azul (la imagen de marca del autor).
- Rótulos: **CLAUDE** (rojo), **CÓMO SE LO PIDES**, **PÁSALE**, **3 FOTOGRAMAS**, **COSA 3 DE 3**, «skill de …» y un **contador de fotogramas (26 de 79)**.
- Los propios overlays del reel son las animaciones que el método produce: **el reel es la demo**.

## 3. Verificación de sus afirmaciones (dato externo, 09-oct-2026)
- **`remotion-dev/skills` existe y está activo**: repositorio **oficial** de Remotion («Agent Skills») — **4.948 ⭐**, 548 forks, creado **19-ene-2026**, último push **07-oct-2026**. El comando que da apunta a algo real y en mantenimiento.
- **`remotion-dev/remotion`**: **62.718 ⭐**, 4.891 forks, licencia **NOASSERTION** (licencia propia). La página oficial de licencias confirma la estructura **Free License / Company License** → su frase «gratis si trabajas solo» es coherente; el matiz «hasta 3» viene de su caption y encaja con el modelo de asientos.
- «Hice la misma animación 5 veces con Opus 5.5 y Sonnet 5.5 y ganó Sonnet» → **anécdota propia, no verificable** (no publica los 5 renders). Es el único punto que pide fe.
- «Claude ha matado a los Motion Designers» → **hipérbole de gancho**, no afirmación técnica.

## 4. Aplicabilidad al Joko Lab (OBS)
- **Encaja con su pipeline de vídeo actual**: el lab monta vídeos con slides HTML/PNG + TTS + ffmpeg (`video-slides-tts`, `album-fotos-video`, `guiones-video-cortos`). Remotion aporta lo que ese pipeline no tiene: **animación con código**, revisable y versionable en git, y **reutilizable** (una skill de estilo propia → coherencia de marca).
- **Coste real para el lab**: Node/React en el flujo y licencia de pago si el uso supera el umbral (empresas >3 o render para terceros). Con 1 persona, **la Free License aplica** → 0 €.
- **El truco más transferible no es Remotion**: «pásale un vídeo de referencia + descríbele la escena paso a paso + **pídele que revise sus propios fotogramas**» es exactamente el patrón de QA por frames que el lab ya usa (extraer frames y mirarlos). Encaja como regla al generar vídeo o carrusel: **auto-revisión por fotogramas antes de publicar**.
- **Sinergia con la valoración del canal**: el «cerebro» (reel 2) y la «skill de estilo» (reel 3) son la misma idea — **empaquetar el estilo y el contexto en ficheros** que el agente lee. Es el patrón del lab (`AGENTS.md` + skills).

## 5. Defecto de instrumento (repetido)
- GLM **filtró razonamiento** en **2 de 12** frames (`frame_02`, `frame_08` devolvieron `[REASONING] …` en vez del resumen). Es el **segundo reel consecutivo** con el mismo fallo → el prompt de `analizar_carrusel_rapido.py` no está bloqueando el canal de razonamiento del modelo (candidato a arreglo en `tools/`).

## 6. Artefactos
`reel_transcripcion.txt`, `reel_metadatos.json`, 12 `frame_NN.jpg` y `reel.mp4` (jpg/mp4 fuera de git por `.gitignore`).
