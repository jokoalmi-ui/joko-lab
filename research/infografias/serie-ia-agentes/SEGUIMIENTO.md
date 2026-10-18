---
title: "SEGUIMIENTO — IA y agentes, de cero a producción"
type: research
---

# SEGUIMIENTO DE PUBLICACIÓN — IA y agentes, de cero a producción

Generado por `serie_estado.py md` el 2026-09-30. **Fuente de datos: `seguimiento.json`** (no editar este .md a mano).

Canal: **LinkedIn** · Cadencia: lunes, miércoles y viernes (3 piezas por semana) · Colchón mínimo: 3

## Piezas

| id | nivel | título | estado | verificado visual | publicada | url |
|---|---|---|---|---|---|---|
| L0 | 0 | Qué es un LLM: la máquina que no busca, genera | publicado | sí | 2026-09-14 | https://www.linkedin.com/posts/activity-7505285343475322880--QAj?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAXdHccBtUt1XuWmue7V2L-nyeiQhODwalw |
| L0-A | 0 | IA, ML, Deep Learning y LLM: la escalera de términos | publicado | sí | 2026-09-16 | — |
| L0-B | 0 | Qué puedes pedirle y qué no (usos y tamaño del modelo) | publicado | sí | 2026-09-18 | — |
| L1 | 1 | Instrucciones: el prompt | publicado | sí | 2026-09-21 | — |
| L2 | 2 | El modelo conectado al mundo: datos y herramientas | publicado | sí | 2026-09-23 | — |
| L3 | 3 | El agente: el bucle | publicado | sí | 2026-09-25 | — |
| L4 | 4 | De uno a muchos: agentes que colaboran | publicado | sí | 2026-09-28 | — |
| L5 | 5 | Producción: fiabilidad, coste y límites | verificado | sí | — | — |
| CIERRE | 6 | El mapa de la serie: 6 niveles y 8 piezas | verificado | sí | — | — |

Estados: idea → guion → arte → render → verificado → publicado

## Avisos (7)

- [FALTA DATO] L0-A esta publicada sin url/fecha
- [FALTA DATO] L0-B esta publicada sin url/fecha
- [FALTA DATO] L1 esta publicada sin url/fecha
- [FALTA DATO] L2 esta publicada sin url/fecha
- [FALTA DATO] L3 esta publicada sin url/fecha
- [FALTA DATO] L4 esta publicada sin url/fecha
- [COLCHON] 2 pieza(s) listas sin publicar; el minimo del lab es 3

## Notas por pieza

- **L0** — (doc: ¿ que es un llm? La máquina que no busca , genera.) 7 slides + PDF. Dato medido: 1 palabra ~ 1,4 tokens (granite4.2:8b, Ollama local, 14-sep-2026); ventana 131.072. Falta el coste por millon de tokens. PUBLICADA 2026-09-14 en LinkedIn; texto del post en post-linkedin.md. Analitica LinkedIn (captura del usuario, 16-sep-2026 14:48): documento «Que es un LLM? La maquina que no busca, genera.» 7 paginas = 33 impresiones, 0 interacciones. Envíos en LinkedIn: 0.
- **L0-A** — (objetivo 2026-09-17) (doc: IA, machine learning, deep learning y LLM: en qué se diferencian) Pieza propia: el tema de fundamentos que la L0 no cubre. Decision del usuario 14-sep: sin trabajo previo. Producida y verificada el 16-sep-2026 (miercoles) y PUBLICADA ese mismo dia con la cadencia l/m/v; el jueves 17 que figuraba como transicion queda sin efecto. L0-B pasa a viernes 18-sep-2026. Analitica LinkedIn (captura del usuario, 16-sep-2026 14:48): documento «La escalera de terminos en IA.» 7 paginas = 10 impresiones, 0 interacciones. REGISTRO: publicada el 16-sep-2026 con la fecha real de publicacion; la URL queda como hueco declarado (el compartir/copiar enlace de la app movil de LinkedIn falla), asi que el script mantiene el aviso [FALTA DATO] hasta que se pueda completar. Analitica LinkedIn (captura del usuario, 20-sep-2026): documento «La escalera de terminos en IA.» 7 paginas = 16 impresiones (antes 10 el 16-sep), 10 miembros alcanzados, 100% en la red / 0% fuera, 0 visualizaciones del perfil, 0 interacciones.
- **L0-B** — (objetivo 2026-09-21) Usos: chat, resumir, redactar, clasificar, traducir + parámetros (8B/70B). producida 18-sep: guion+medicion real 3 tamanos+arte SDXL+PDF 7 pag; pendiente de publicar PUBLICADA el 2026-09-18 (viernes; dato del usuario, 20-sep-2026), 3.a pieza de la semana l/m/v: registrada el 2026-09-20 SIN url (opcion b autorizada por el usuario, mismo criterio que L0-A): el compartir/copiar enlace de la app movil de LinkedIn falla. Aviso [FALTA DATO] asumido y visible hasta completar la url.
- **L1** — PUBLICADA 2026-09-21 por confirmacion del usuario (Telegram). url=null a proposito: la app movil no permite copiar el enlace del post; no hay captura ni enlace disponibles. Su palabra es la unica evidencia; el hueco queda declarado.
- **L2** — PUBLICADA 2026-09-23 (miercoles) por confirmacion del usuario (Telegram, 2026-09-24): el registro decia 'verificado' y el usuario corrigio que el material ya estaba publicado. url=null a proposito (mismo criterio que L0-A/L0-B/L1): sin enlace ni captura disponibles; su palabra es la unica evidencia y el hueco queda declarado. Material: post-linkedin.md + carrusel-leccion-2.pdf (7 pag), verificado visualmente el 2026-09-22.
- **L3** — Revision visual GLM-4.6V-Flash 25-sep 07:18: 7/7 slides sin defectos (revision-visual-20260924.json). PUBLICADA 2026-09-25 (viernes) por confirmacion del usuario (Telegram, 2026-09-27): el registro decia 'verificado' y el usuario corrigio que la pieza salio el viernes. url=null a proposito (mismo criterio que L0-A/L0-B/L1/L2): la app movil no permite copiar el enlace; su palabra es la unica evidencia y el hueco queda declarado. Material: post-linkedin.md + carrusel-leccion-3.pdf (7 pag), revision visual GLM-4.6V-Flash 7/7 sin defectos.
- **L4** — Leccion 4 producida y verificada el 27-09-2026 (noche, camino A). Medicion propia con medicion-multiagente.py: granite4.2:8b en Ollama local, temperatura 0, num_ctx 8192, 6 tareas x 2 condiciones. A (un agente con herramientas) 6/6, 22.121 tokens, 537 s. B (mismo agente + critico independiente; el coste de B INCLUYE el de A) 6/6, 86.256 tokens, 2.515 s. Resultado: x3,90 en tokens y x4,68 en tiempo, 0 tareas rescatadas por el critico, 1 reintento disparado por un FALSO NEGATIVO (tarea 6: dijo incorrecto sobre una respuesta correcta; 6.530 -> 35.633 tokens y 163 -> 1.114 s para la misma respuesta). El eje de la pieza es 'colaborar cuesta', no 'colaborar mejora'. Arte SDXL 768 px (4 imagenes, via ComfyUI) normalizado al crema de la serie. 7 slides 1080x1350 + PDF de 7 paginas; QA objetivo sin desbordamientos; revision visual GLM-4.6V-Flash 7/7 sin defectos (revision-visual-20260927.json). Material: guion-leccion-4.md, post-linkedin.md/.txt (1.966 caracteres), carrusel-leccion-4.pdf. PENDIENTE DE PUBLICAR (lunes 28-09-2026). PUBLICADA 2026-09-28 por confirmacion del usuario (CLI, 2026-09-28): el usuario confirmo la publicacion sin facilitar el enlace. url=null a proposito (mismo criterio que el resto de la serie): el hueco queda declarado.
- **CIERRE** — (objetivo 2026-10-05) 

## Bitácora

- 2026-09-14 — L0 registrada como verificada, pendiente de publicar
- 2026-09-14 — Texto del post escrito (post-linkedin.md, 14-sep); pendiente solo la publicacion manual.
- 2026-09-14 — https://www.linkedin.com/posts/activity-7505285343475322880--QAj?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAXdHccBtUt1XuWmue7V2L-nyeiQhODwalw
- 2026-09-14 — Cadencia nueva: lunes y jueves (2/semana). L0-A con objetivo jueves 2026-09-17.
- 2026-09-14 — Titulo publicado: ¿ que es un llm? La máquina que no busca , genera.
- 2026-09-15 — Cadencia subida a 3/semana (decision del usuario 15-sep): lunes+miercoles+viernes, colchon minimo 3 (antes 2). L0-A se mantiene el jueves 2026-09-17 como transicion; el regimen de 3 arranca la semana del 2026-09-21.
- 2026-09-15 — El usuario confirma (15-sep): 3 publicaciones semanales, lunes+miercoles+viernes, con la misma tematica de la serie iniciada con L0 ('que es un LLM'). Las 3 piezas semanales son de esta serie; sin serie paralela en esos dias.
- 2026-09-16 — Producida y verificada el 16-sep-2026 (miercoles) para publicar hoy: la cadencia de 3/semana l/m/v adelanta la pieza respecto al jueves 17 que figuraba como transicion; L0-B pasa a viernes 18-sep-2026.
- 2026-09-16 — Analitica LinkedIn (captura del usuario, 16-sep-2026 14:48): documento «Que es un LLM? La maquina que no busca, genera.» 7 paginas = 33 impresiones, 0 interacciones. Envíos en LinkedIn: 0.
- 2026-09-16 — Analitica LinkedIn (captura del usuario, 16-sep-2026 14:48): documento «La escalera de terminos en IA.» 7 paginas = 10 impresiones, 0 interacciones. Publicado hoy segun el usuario; URL pendiente: copiar/compartir el enlace desde la app movil le falla.
- 2026-09-16 — registrada como publicada el 2026-09-16 SIN url (opcion b, autorizada por el usuario): el compartir/copiar enlace de la app movil de LinkedIn falla. Aviso [FALTA DATO] asumido y visible hasta completar la url.
- 2026-09-18 — producida 18-sep: guion+medicion real 3 tamanos+arte SDXL+PDF 7 pag; pendiente de publicar
- 2026-09-18 — registrada el 2026-09-20 SIN url (opcion b autorizada por el usuario, mismo criterio que L0-A): el compartir/copiar enlace de la app movil de LinkedIn falla. Aviso [FALTA DATO] asumido y visible hasta completar la url.
- 2026-09-20 — Analitica LinkedIn (captura del usuario, 20-sep-2026): documento «La escalera de terminos en IA.» 7 paginas = 16 impresiones (antes 10 el 16-sep), 10 miembros alcanzados, 100% en la red / 0% fuera, 0 visualizaciones del perfil, 0 interacciones.
- 2026-09-21 — confirmado por el usuario por Telegram; sin url (no disponible desde el movil)
- 2026-09-24 — registrada el 2026-09-24 SIN url (opcion b, mismo criterio que L0-A/L0-B/L1) por confirmacion del usuario: la pieza salio el 2026-09-23. El registro decia 'verificado' y el usuario corrigio que si el carrusel existe la pieza esta publicada.
- 2026-09-25 — Revision visual GLM-4.6V-Flash 25-sep 07:18: 7/7 slides sin defectos (revision-visual-20260924.json).
- 2026-09-27 — registrada el 2026-09-27 SIN url (mismo criterio que L0-A/L0-B/L1/L2) por confirmacion del usuario (Telegram): la pieza salio el 2026-09-25 (viernes). El registro decia 'verificado' y el usuario corrigio.
- 2026-09-27 — Leccion 4 producida y verificada la noche del 27-09-2026 (camino A elegido por el usuario). Medicion multi-agente propia, 100% local (granite4.2:8b en Ollama, temp 0): A un agente con herramientas 6/6, 22.121 tokens, 537 s; B mismo agente + critico independiente (su coste incluye el de A) 6/6, 86.256 tokens, 2.515 s. Resultado: x3,90 en tokens y x4,68 en tiempo, 0 tareas rescatadas y 1 reintento disparado por un FALSO NEGATIVO (tarea 6: dijo incorrecto sobre una respuesta correcta). El dato cambio el eje de la pieza respecto a la hipotesis de partida: el titular es 'colaborar cuesta', no 'colaborar mejora'. Arte SDXL 768 px (ComfyUI, 4 imagenes) normalizado al crema de la serie; 7 slides 1080x1350 + PDF de 7 paginas con QA objetivo sin desbordamientos (la slide 4 desbordaba y se corrigio); revision visual GLM-4.6V-Flash 7/7 sin defectos (revision-visual-20260927.json). Pendiente de publicar el lunes 28-09-2026.
- 2026-09-28 — registrada el 2026-09-28 SIN url (mismo criterio que el resto de la serie) por confirmacion del usuario: la pieza salio el 2026-09-28. El registro decia 'verificado' y el usuario corrigio.

## Cómo se registra la publicación

La publicación es MANUAL (la hace Joseba). Cuando el post esté arriba, se registra:

```bash
python3 serie_estado.py publicar <id> --url <url-del-post>
```

Ejecutar el script desde su carpeta (research/infografias/serie-ia-agentes/).
