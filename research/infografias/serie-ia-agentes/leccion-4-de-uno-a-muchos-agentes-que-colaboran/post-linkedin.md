# Lección 4 · «De uno a muchos: agentes que colaboran» — post de LinkedIn

- **Serie**: «IA y agentes, de cero a producción» · **pieza 7** (nivel 4)
- **Formato**: documento PDF (7 slides 1080×1350) + este texto
- **Fecha prevista**: lunes 28-sep-2026
- **Medición**: `medicion-multiagente-20260927.json` — 27-sep-2026, granite4.2:8b en Ollama (local), temperatura 0, num_ctx 8192, 6 tareas × 2 condiciones
- **Estado**: render + QA objetivo OK · revisión visual con VLM en curso · **pendiente de publicación**
- **Ficheros de la pieza**: `carrusel-leccion-4.pdf`, `slides/`, `build_slides.py`, `medicion-multiagente.py`, `revision-visual-20260927.json`

---

## Texto (pegar en LinkedIn)

Le puse un crítico a mi agente. Costó 3,9 veces más y acertó exactamente lo mismo.

En la lección 4 de la serie tocaba lo que más se vende ahora: equipos de agentes. Varios agentes; uno reparte, otro escribe, otro revisa. Suena bien. Así que lo medí, como las anteriores.

El montaje, todo en local:

· **A** — un agente con herramientas.
· **B** — el mismo agente más un crítico independiente, que comprueba el dato real con las mismas herramientas y pide corrección si lo ve mal. El coste de B incluye el de A: no se lo escondo.

Mismo mundo, las mismas 6 tareas de varios pasos que la lección anterior, mismo modelo (granite 4.2 8B en mi máquina), temperatura 0.

El resultado:

· A: 6 de 6 · 22.121 tokens · 537 segundos.
· B: 6 de 6 · 86.256 tokens · 2.515 segundos.
· ×3,9 en tokens, ×4,7 en tiempo. Tareas que el crítico rescató: 0. Reintentos disparados: 1.

Ese único reintento cuenta la historia entera: en la tarea 6 el crítico dijo «incorrecto» sobre una respuesta que era correcta. El agente rehízo el trabajo y volvió a dar el mismo número. Sin crítico: 6.530 tokens y 163 segundos. Con crítico: 35.633 tokens y 1.114 segundos. La misma respuesta.

Lo que esto NO dice, y me importa decirlo: no dice que el crítico no sirva. Dice que en este trabajo — datos que se pueden comprobar y un modelo que ya acierta — no cambia la precisión y sí multiplica la factura. Con tareas más duras, o con un modelo que falle, la pregunta vuelve a estar abierta. La volveré a medir.

Y me deja una regla: no se añade un agente a un sistema «por si acaso». Se añade cuando sabes qué error concreto va a cazar, y luego se mide si lo caza. Si no lo caza, es humo con factura.

El documento de abajo es la lección 4 completa (7 slides): las cuatro formas de organizar varios agentes, las tres preguntas antes de montar un equipo, cuándo NO usarlos y el detalle de esta medición.

Serie: IA y agentes, de cero a producción · Lección 4/6.

#IA #Automatizacion #Agentes #LLM #LocalFirst
