# Análisis — Curso "El Nuevo ChatGPT" (The BIG school) + skills mostradas
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha análisis:** 04-sep-2026
**Fuente:** directos Clase 1 (Wlyiydx6cD4), Clase 2 (cVe0icmwH_4), Clase 3 (gw8NugDjQfY) — canal Inteligencia Artificial (@la_inteligencia_artificial), The BIG school (Jon Hernández + Romu Alfons)
**Transcripciones:** subs auto ES descargadas con yt-dlp (clase1: ~88K chars, clase2: ~83K, clase3: ~132K) en /tmp (curso_ia_clase*_subs.es-orig.vtt)
**Veredicto:** VALIDA la arquitectura del lab (skills+agentes como paradigma mainstream). Valor técnico: BAJO. Nada de MCP.

## Qué es
Lead magnet de captación de The BIG school para vender su Máster IA de pago.
Curso gratuito de 3 días con certificado. 456K + 218K + 138K views (04-sep).

- **Clase 1** (1h13m): ChatGPT **Work** (app con proyectos/hilos), narrativa "superagente" (un asistente que se crea agentes y skills solo). Cero profundidad técnica.
- **Clase 2** (1h09m): **Vibe Coding con Lovable** (crear apps sin programar; 60M proyectos, 80% no-técnicos). Lovable = "agente especializado en programar".
- **Clase 3** (1h45m): **Skills en ChatGPT** (122 menciones). Demos en vivo + regalo de 5 skills. Promo del Máster (9 menciones).

## Skills mostradas/regaladas en Clase 3 (con qué hacen)
1. **Skill menú/carta → app digital** — le das la carta de restaurante/cafetería y genera app digital para clientes. Demo: 25 min de Work con un prompt vs "equipo de programadores contratado". Regalada; funciona también con Claude y Copilot. Invocación: pides a ChatGPT "créame un skill que haga esto".
2. **Skill de currículums** (símbolo `$currículum` para invocarla) — mejora un CV "del montón" y lo optimiza para una oferta concreta (demo con oferta de InfoJobs). Pregunta para qué oferta aplicas.
3. **Skill presupuesto → propuesta → contrato** — "next level": a partir de un presupuesto genera propuesta comercial interactiva tipo landing page + seguimiento de clientes que aceptan + generación de contrato con la misma skill. Todo en uno.
4. **Skill de reuniones** — a partir de transcripción/audio de reunión genera actas/documentos. Demo: 13 min para generar todo.
5. **Skill extra** mencionada: conectores con apps de empresa (ej. "Magnific" / Make / automatizaciones).

**Instalación según ellos:** descargas el archivo de la skill, lo metes en la ventana de ChatGPT y dices "instálame este skill" (o `$nombre`). Funciona en ChatGPT, Claude, Copilot.

## Patrón de skill que enseñan (comparable con el lab)
- "Decirle a la IA CÓMO quieres que haga algo una vez, para repetirlo siempre con el mismo patrón".
- Personalización: pedirle a la skill que pregunte lo que necesite ("personalízala para mí y pregúntame lo que necesites") — táctica de prompt que el lab ya aplica en fichas.
- Una skill = tarea repetitiva del negocio (presupuestos, CV, actas de reunión, menús).

## Comparación con el lab (Hermes)
- El lab YA vive de skills (40+, versionadas con RULE-008, en ~/.hermes/skills/ con frontmatter name+description, progressive disclosure) — el curso explica a nivel usuario exactamente el paradigma Hermes.
- DIFERENCIA: las skills de ChatGPT son instrucción natural a un LLM cloud; las de Hermes son instrucción + scripts + referencias + agentes (más potentes, ejecutan código real).
- MCP: 0 menciones en las 3 clases → el curso NO cubre MCP (el lab ya conecta 3 servidores MCP + n8n).
- El Máster de pago sí menciona "Make/N8N" e "IA audiovisual" como módulos → confirma que n8n y automatización son estándar en formación IA comercial.

## Conclusión / uso para el lab
- Nada accionable técnicamente nuevo.
- Útil como REFERENCIA de lo que el público general no-programador está aprendiendo (skills = mainstream) → el lab está por delante del contenido comercial.
- Si se quisiera contenido LinkedIn: el ángulo "skills que la IA adquiere y reutiliza" ya es tema masivo; el lab lo demuestra con implementación real local.

## Archivos fuente
- /tmp/clase1_limpio.txt, /tmp/clase2_limpio.txt, /tmp/clase3_limpio.txt (dedup n-gramas)
- /tmp/curso_ia_clase*.vtt (subs originales)
