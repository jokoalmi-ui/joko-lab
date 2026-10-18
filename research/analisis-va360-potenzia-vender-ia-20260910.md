---
title: "Análisis: PotenzIA «De 0 a vender con IA» (VA360 | @Valen) — directo de venta de mentoría"
type: research
---

# Análisis: PotenzIA «De 0 a vender con IA» (VA360 | @Valen)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/SAlOXTA6S1Y · canal VA360 | @Valen (UCxNmXU0TEFM7DqJahdLKNCQ) · publicado 10-sep-2026
**Vídeo**: 2:44:40 (directo) · 318 vistas · 10 likes (consultado 14-sep-2026)
**ID**: SAlOXTA6S1Y · **Analizado**: 14-sep-2026 10:44 CEST (sesión CLI)
**Transcripción**: auto-subs `es-orig` (yt-dlp venv del repo) → limpieza + dedup n-gramas → 147.734 chars / 26.680 palabras. Es ASR automático: hay palabras mal transcritas («Clou»/«Cloude»=Claude, «potencia»=PotenzIA, «setería»=setter, «webhood de Culify»=webhook de Meta).

## Qué es este vídeo

Directo de **venta de formación**. No es un tutorial: es la demo comercial de
PotenzIA (marca de formación del propio canal).

- Protagonista: **Valen**, fundador de VA360 LAB y «director académico de
  PotenzIA» (él mismo se presenta así). Le acompaña **Laura** (compañera de
  VA360, contesta el chat) y **Sara** (en su casa).
- Emite en varias plataformas (pide estar en YouTube para leer el chat).
- Público objetivo declarado: gente que «trabaja para alguien y quiere
  cambiar», consultorías, desarrolladores y quien quiera montar negocio con IA.
- Estructura: presentación + demo práctica en vivo (construir un **setter con
  IA que agenda citas** por WhatsApp: webhook de Meta, APIs de cal.com, la app
  `agente.potencia.io`, ejemplo «administración de lotería») + respuestas del
  chat + **oferta final**.
- Regalo de permanencia: la solución construida en el directo se la llevan
  «completamente gratis, sin soltar ni 1 euro, sin tarjeta» quienes aguantan
  hasta el final.

## Herramientas que nombra (conteo real sobre la transcripción limpia)

Codex **38** · Claude/Claude Code **6** · n8n **1** · Ollama **1** ·
Lovable **1** · OpenCode **1** · **Hermes 1** · Antigravity **1**.

- Hay una **encuesta en el chat: Claude Code vs Codex** y gana Codex; a partir
  de ahí el directo se hace con Codex. Cuentan una migración real
  «desde Claude a Codex sin perder nada» y que Codex «es de pago al igual que
  Claude».
- **Hermes aparece una sola vez**, dentro de una enumeración: «Cloud Code como
  herramienta con Claude como modelo, Codex como herramienta con GPT como
  modelo, Open Code, Hermes, OpenCloud, Orca X. Hay muchísimas herramientas».
  Es decir: Hermes figura en el mapa mental del circuito hispano de agentes,
  pero aquí no se explica ni se usa (el lab ya lo tiene como sistema propio).

## La oferta comercial (textual, verificable en la transcripción)

- Precio: **«un precio único de 4,500 y una financiación de 375 € durante 12
  meses»** (en el chat se oye «4500 y creo que son 378 al mes»).
- Inicio del programa: **13-oct-2026** (martes y jueves de 18 a 20 h en la
  1.ª edición; dicen que el horario lo decidirán por encuesta).
- Qué venden: «**no es un curso, es una mentoría, un acompañamiento**» — clases
  en vivo **grabadas**, comunidad tipo Circle/Skool, grupo de WhatsApp, sesión
  1-a-1 previa, y **masterclass de venta** con Diego Abreu («fanel para captar
  clientes en frío» = funnel) y Miguel RMS (TikTok Ads). *«Los técnicos
  normalmente somos malos vendiendo y por eso nosotros tenemos en potencia los
  cracks que tenemos de venta»*.
- «Grupo reducido» como argumento de escasez (el ponente admite que no dice la
  palabra «plazas delimitadas», pero mantiene el argumento).

## Claims del ponente — NO CONTRASTADOS

Marco RULE-017 / gate de veracidad: son afirmaciones de parte, sin fuente
externa. Se registran como claims, no como hechos.

1. «**7.000 € facturados en dos semanas**» (atribuido a gente de la comunidad /
   la 1.ª edición). Sin prueba en el vídeo.
2. «En dos semanas puedes tener un proyecto hecho y derecho para entregar a un
   cliente... y cobrar un buen dinero por él».
3. «Muchos de los alumnos de la primera edición han...» (claim cortado, sin
   detalle).
4. Argumento de precio: «cualquier profesional que se precie es capaz de
   conseguir 375 € al mes; y si no es capaz, quizá no es momento de estar por
   aquí» (presión de encuadre, no dato).

Dato duro del texto (búsqueda literal): **0 apariciones de «garantía» y
0 de «devolución»** en las 2 h 44 min. Hay «14 grabad»/«acompañamiento 14» pero
ninguna mención a devolver el dinero.

## Disección técnica: qué construyen y cómo (lo replicable)

Artefactos del método, en el orden en que los cuenta:

1. **Reunión con cliente → briefing escrito.** Se leyó un briefing previo (generado
   antes del directo, no en vivo).
2. **PRD antes de tocar nada.** Prompt literal que muestra en pantalla: «*Lee el
   briefing setter y app y prepara un PRD para un MVP*» (lo fecha: miércoles 22:55).
   «PRD = requerimientos de producto», «MVP = producto mínimo viable». El propio PRD
   deja una lista de **pendientes**: «la documentación deja pendientes Meta, el modelo
   de IA y la agenda de prueba».
3. **Alcance cerrado + exclusiones explícitas**, textual: «*vamos a tener un alcance
   cerrado: un único negocio (ficticio), un número de prueba de WhatsApp con la API
   oficial de Meta, un tipo de cita — reunión inicial…*» y «***NO** vamos a hacer
   prospección, **NO** vamos a prometer precios ni condiciones, ni cobrar, ni lo vamos a
   conectar con sistemas actuales del negocio*».
4. **Construcción con Codex sobre la documentación**: «*que se encargue de leer la
   documentación y genere este proyecto*». Enseña el panel de Codex y explica a los
   asistentes que «aunque parezca código por el tipo de letra, no es código».
5. **Validación paso a paso**: «*lo único que necesitas es validar que lo que está
   haciendo es correcto… paso por paso*».

Stack que usa para entregar:

- **WhatsApp Cloud API oficial de Meta**, con **número de prueba** para desarrollo;
  ojo al detalle útil: WhatsApp e Instagram «comparten la misma API» y el mismo proceso
  de aprobación ante Meta.
- **cal.com** como agenda («el estándar de agendación de todo el mundo»), con API key
  creada desde Ajustes → Claves de API.
- **Supabase** para BD + autenticación + migraciones (un asistente lo define como
  «como un backend»).
- **Coolify** como PaaS autoalojado («100 % gratis, tú pagas tu servidor»): contenedor
  de aplicaciones, dominios temporales, backups. Sobre **VPS de 15-20 €/mes**.
- Diseño generado por IA a partir de un **documento de diseño previo** «*para que no se
  invente absolutamente nada*» (el ASR no permite confirmar el nombre de la herramienta:
  suena «Claude Design»; lo relevante es el patrón, no la marca).
- Funciones del setter que sí definen: agendar 24/7, **evitar no-shows** (recordatorio
  con botón de confirmar en WhatsApp, ejemplo clínica de fisioterapia), **KPIs de valor**
  («¿cómo vamos a vender un setter que no te dice cuántas personas ha agendado, cuántos
  no-show te ha librado?»), derivación a humano y cobro **por canales** + mantenimiento
  o instalación en servidor del cliente.
- Complementos dichos (no demostrados): no pegar tokens/URLs/contraseñas en la
  conversación con la IA, RGPD y «validaciones del IAC» como parte del entregable, y
  venta cruzada (del setter a agente de llamadas, presupuestos, OCR de facturas).

### Contraste honesto con lo que el lab ya tiene

CONFIRMA (el lab ya lo hace, y mejor verificado):

- Documento-spec entregado al modelo para que no improvise: el lab tiene el PRD PROMPT
  del 17-ago, el patrón SVP y la skill `design-md` (DESIGN.md) para exactamente eso.
- Agente conversacional por canal con webhook: en el lab, Telegram + n8n.
- No meter secretos en el contexto del modelo.
- Validar por pasos en vez de confiar en el resultado final (el lab lo tiene
  automatizado con gates; aquí es a ojo).

NUEVO / aprovechable (candidatos; nada implementado):

1. ✅ **APLICADO 14-sep-2026** — Sección de NO-ALCANCE obligatoria en las specs del lab
   (skill `plan` v2.1.0: cabecera obligatoria + gate en la Clarification Phase; skill
   `documentacion-joko-lab` v1.1.0: el método PRD PROMPT exige NO-ALCANCE). Cierran el
   alcance con una lista explícita de exclusiones *antes* de construir. El lab tiene PRD/plan, pero
   el «NO-alcance» explícito no está formalizado como sección fija — y es justo lo que
   ataca el fallo que el lab persigue (que el agente invente alcance o datos).
2. **Blueprint de entrega a cliente con costes reales**: WhatsApp Cloud API (+número de
   prueba para desarrollar) + cal.com + Supabase + Coolify sobre VPS de 15-20 €/mes. El
   lab no tiene documentado ningún stack de «producto para cliente» (todo su material es
   local: Ollama/LM Studio/n8n/Hermes). Referencia de precios y piezas si algún día
   vende servicios — y las cuatro son open source o autoalojables.
3. **KPIs de valor del agente** (citas agendadas, no-shows evitados) frente a los KPIs
   técnicos del lab (TTFB, tokens, VRAM, temperatura). Idea anotable de cara a terceros.
4. **Tasar precios con un agente alimentado con tu histórico de presupuestos ganados**
   (lo regalan como «agentito» al final). Es RAG sobre datos propios: técnica que el lab
   domina, aplicada a un dominio (pricing) que no ha tocado.

NO HAY (nada nuevo para el lab): ninguna técnica de IA local, modelos, cuantización,
RAG, evaluación, memoria, orquestación ni coste de inferencia. El stack que enseñan es
cloud (Codex, Supabase, Coolify/VPS) y su validación es humana a ojo. En todo el eje
técnico del lab, este vídeo va por detrás.

## Valor para el lab (filtro 20-ago)

**BAJO como contenido técnico. MEDIO como información de mercado.**

- BAJO técnico: lo que construyen (agente/setter que agenda citas por WhatsApp
  sobre webhook de Meta + n8n + APIs) es exactamente lo que el lab ya tiene
  montado (Hermes + Telegram + n8n). No aparece ninguna técnica, modelo o
  patrón nuevo; las herramientas que cita son las de siempre.
- MEDIO de mercado — lo NUEVO/anotable:
  1. **Benchmark de formación IA en España: 4.500 € (o ~375 €/mes × 12)** para
     una mentoría de agentes + venta. Dato de precio real, útil como referencia.
  2. **Coste de entregar a cliente: VPS «unos 15 o 20 € al mes»** por
     automatización; modelo de cobro «por canales» (WhatsApp, Instagram...) y
     por mantenimiento. Coincide con la capa de costes del lab.
  3. **Tesis del canal: el cuello de botella es vender, no programar** (meten
     masterclass de ventas, no de código; «los técnicos somos malos
     vendiendo»). Encaja de lleno con la situación de Joseba (parado,
     buscando empleo/negocio con IA): el mensaje es que la técnica ya no
     diferencia, la venta sí.
  4. **Menciona a Hermes** como una de las herramientas del circuito → señal
     menor de que el ecosistema del lab es mainstream en el nicho hispano.

## Veredicto

**CONFIRMA + INFORMATIVO NO ACCIONABLE (para el lab).** No hay nada que
implementar: el lab ya hace esto y mejor verificado. Lo aprovechable es la
lectura de mercado (precios, encuadre de venta, tesis «vender > programar») y
el dato de que Hermes ya se nombra en directos de formación del sector.

**Para decisión personal del usuario (no del lab)**: es una oferta de 4.500 €
con claim de resultados no verificado y sin garantía de devolución mencionada;
el temario declarado (montar agentes y venderlos) es adyacente a lo que él ya
está construyendo por su cuenta. Ninguna recomendación desde el lab: decisión
suya, con estos datos delante.

Conecta con: `analisis-jokiruiz-ahorro-tokens-20260908.md` (costes y
arquitectura local), `analisis-barrido-canales-20260908.md` (criterio de valor
de canales), skill `recursos-gratuitos-desempleados` (alternativas de coste 0
antes de pagar formación), `analisis-dailydoseofds-qm-yc-20260909.md` (Hermes
como estándar de facto en el sector).

## Trazabilidad

- Transcripción limpia: `/tmp/potenzia-limpio.txt` (147.734 chars) — no se
  guarda copia permanente en el lab (vídeo de venta, sin valor técnico
  reutilizable); si se quiere conservar, pedirla.
- Anti-duplicado previo: `grep -ril "SAlOXTA6S1Y|potenzia"` sobre
  research/ + inbox/ + docs/ + 01-knowledge/ → 0 resultados.
- Backup del backlog antes de anotar:
  `.BACKUP.20260914-potenzia-va360`.
