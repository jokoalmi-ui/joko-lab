---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-25
---
# CP-011: Una escritura larga se trunca sin fallar: el artefacto queda a medias y con una marca que nadie busca

**ID:** CP-011
**Fecha:** 2026-09-25
**Estado:** E0 — Candidate Pattern
**Origen:** Revisión de fallos 2026-09-25 (ciclo semanal LPA, D0/INC-005) — 2 ficheros distintos medidos el mismo día con el marcador literal `[truncated]`, causados por escrituras del mismo canal automático
**Nivel de confianza:** Medio (2 ocurrencias confirmadas en 2 ficheros/skills distintos, con el segundo exacto del patch localizado en el ledger del curador; + 1 ocurrencia ya detectada el 24-09 y NO reparada; − 1 candidata descartada por no ajustar al mecanismo)

---

## 1. Qué ocurrió

Una escritura larga (un `patch`/`write_file` de más de ~1 KB sobre un fichero de skill) **no falló: escribió menos**. El canal devolvió OK, el fichero siguió existiendo y siendo legible, y el bloque quedó cortado a mitad de frase con el marcador literal `[truncated]` pegado al final del texto cortado. Como el fichero es válido y se lee con normalidad, **el fragmento cortado se cita después como contenido bueno** — nadie mira la cola ni el tamaño.

Medido el 2026-09-25 en dos skills distintas, las dos tocadas por el canal automático de consolidación (actor `curator`) esa misma mañana:

- `~/.hermes/skills/joko-lab/validacion-instrumentos-medicion/SKILL.md`, **línea 32**: el bloque del pitfall «El instrumento incluye tu propio comando de lectura» termina en «…Un cero o lista vacía de tu propio extractor** tampoco e**[truncated]» — es decir, la frase se corta a mitad de palabra y **el marcador queda al final de una línea que, además, es la que manda buscar el marcador**.
- `~/.hermes/skills/render-html-a-imagen/SKILL.md`, **línea 119**: el párrafo del visor de visión termina en «…ilegible, desce**[truncated]» — otra frase cortada, en otro dominio (render/QA visual), otro fichero y otra hora.

## 2. Evidencia que lo respalda

- **Caso 1 (skill de instrumentos de medida).** `stat`: 44.859 B, mtime **2026-09-25 07:48:50.700347906 +0200**, 173 líneas. El ledger del curador (`~/.hermes/skills/.curator_ledger.jsonl`) registra un `patch` con `actor: curator`, `skill: validacion-instrumentos-medicion` a las **2026-09-25T05:48:50.716103+00:00** (= 07:48:50 CEST): **el mismo segundo** que el mtime del fichero → la escritura que dejó el marcador está identificada.
- **Caso 2 (skill de render/packshot).** `stat`: 23.461 B, mtime **2026-09-25 08:16:08.653910839 +0200**, 142 líneas. El ledger registra 4 entradas `patch` de `curator` sobre `render-html-a-imagen` a las **06:15:59** (+00:00) y una `write_file` a las **06:16:08.675240+00:00** (= 08:16:08 CEST): de nuevo el mismo segundo que el mtime.
- **Tercera ocurrencia ya detectada y no reparada (1 día antes).** `pendientes.md`, 24-sep 08:00 (línea 357): «*Defecto detectado sin arreglar: esa SKILL.md ya traía un marcador literal `[truncated]` en la línea 32 (edición anterior truncada por el arnés); requiere OK para reescribir ese final*». El 25-09, tras nuevas pasadas del curador (`+1/-1` en esa skill), el marcador sigue exactamente donde estaba.
- **Cuarta ocurrencia (misma familia —pérdida silenciosa sin marca—, mecanismo distinto): el registro de ejecuciones pierde historia y no lo dice.** `~/.hermes/cron/executions.db` se lee sin error y declara 1.001 filas, pero su rango real es de **27 h** (08-10 11:30:21 → 09-10 14:32:34) porque `MAX_TERMINAL_EXECUTIONS = 1000` poda por `finished_at` (`~/.hermes/hermes-agent/cron/executions.py:33, 201-209`). Un conteo etiquetado «últimos 7 días» devolvió **1.001 filas** (acta 02-10, §0): el instrumento **no falla y no marca**, simplemente ya no contiene lo que se le pregunta. A diferencia del truncado por `patch`, aquí no hay ceguera — hay diseño —, pero el efecto para quien lee es el mismo. Se registra como ocurrencia de la **familia**; si reaparece en un tercer instrumento, merece CP propio.
- **La regla existe y no lo impidió.** El texto que manda buscarlo («*Un patch de más de ~1 KB puede quedar escrito TRUNCADO: buscar el marcador literal `[truncated]` en el fichero tras cada edición larga y, si aparece, mover ese bloque a un fichero propio con `write_file` (que no trunca) dejando en el original solo un puntero*») está escrito **en la misma línea que quedó truncada**.
- **El daño no es recuperable con lo que hay.** Búsqueda del fragmento perdido («Un cero o lista vacía de tu propio extractor», «debe NOMBRAR los modos de fallo») en las copias disponibles (`~/hermes-backup-pre-021`, `~/.hermes/profiles/**`): **0 coincidencias** → el texto original no está en ninguna copia; no se puede restaurar sin reescribir el bloque.

## 3. Contradicciones o limitaciones

- **No se mide el denominador.** Hay 2 ficheros truncados confirmados, pero **no está medido cuántas ediciones largas se hicieron sin daño** en la misma ventana (solo se sabe que las 2 que quedaron mal se localizaron porque se buscó el marcador). Sin denominador no hay tasa de fallo: el patrón describe el modo de fallo, no su frecuencia.
- **El mecanismo interno no está aislado.** Se ha medido el actor, la acción y el segundo exacto (ledger ↔ mtime), no **por qué** ese `patch` escribió menos: puede ser el límite del INSERT, el troceado del texto, el escape de un carácter o el tamaño del argumento. Sin causa interna, el antídoto es de comprobación, no de arreglo.
- **Candidata descartada (duda declarada).** `~/.hermes/skills/software-development/perfume-ia/references/capa-lpa-recomendacion.md`, línea 33: `from modules.[truncated] import recomendar`. **No se cuenta como ocurrencia**: el fichero continúa después del marcador y el resto del bloque está completo → es compatible con una redacción manual del nombre del módulo, no con un corte de escritura (un corte dejaría sin cola todo lo que venía detrás).
- **¿Se comporta igual un agente de forma interactiva?** Las dos ocurrencias medidas vienen del canal automático (curador). No está probado que el mismo tamaño por `swap` interactivo se trunque igual.
- **Un marcador puede ser legítimo.** Un `[truncated]` puede estar ahí a propósito (cita de un log acortado). Distinguirlo exige leer el CONTEXTO: corte a mitad de palabra/frase = escritura rota; marcador entre corchetes dentro de una cita = contenido intencional. Y como el verificador de hoy es un `grep`, la comprobación tiene que ir seguida de lectura, no solo de conteo.

## 4. Principio que parece emerger

> Una escritura que se pasa de tamaño no falla: escribe menos y no avisa. El artefacto queda a medias, y como sigue existiendo y se lee bien, el fragmento cortado se hereda como contenido válido en la siguiente edición y acaba citado como fuente. **La marca de la pérdida (`[truncated]`) es visible, pero solo para quien la busca.** Regla: el OK del escritor no es prueba de que el contenido llegó entero — tras una edición larga se comprueba el TAMAÑO y la COLA del fichero (y se busca el marcador) antes de dar el cambio por bueno; si el contenido es largo, se escribe por piezas y se verifica cada pieza. Y cuando la pérdida ya ocurrió, no se rellena de memoria ni se cierra la frase a ojo: se declara el hueco y se reescribe el bloque con quien lo conozca.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier sistema que escriba documentos largos por herramienta o API: agentes, wikis, CMS, plantillas de informes, generadores de documentación.
- Conocimiento que se citará después: un documento truncado no se detecta al usarlo, se hereda y se propaga a la siguiente versión (y a quien lo lea).
- Generación de informes largos con LLM: el corte por límite de salida es el mismo fallo con otro disfraz.
- Repositorios de procedimientos (SOP, runbooks): un paso cortado a la mitad es un paso que se ejecuta mal.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **N=10 ediciones largas (>1 KB)** del lab durante **2 ciclos LPA consecutivos**, **al menos 9** ficheros quedan completos (la cola coincide con el texto pretendido y no aparece el marcador literal) **sin** ninguna comprobación posterior de tamaño/cola, es decir, si escribir largo sin verificar no pierde contenido ≥90% de las veces. También lo falsaría que la pérdida ocurriera solo en ficheros que nadie vuelve a citar mientras el artefacto esté truncado (ruido, no riesgo).

## 7. Decisión

Incubar (E0). **Revisión mensual 2026-10-02: sigue en incubación** (D10 del acta `revision-fallos-2026-10-02.md`).

- [ ] Asciende a KNOWN.md como E1 (falta el denominador: cuántas ediciones largas salen bien)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto —comprobar tamaño y cola tras edición larga— ya está escrito en las propias skills, pero **no se está ejecutando**: D8 del acta 25-09 lleva 3 semanas sin cerrar)
- [x] Sigue en incubación (falta medir el denominador y aislar el mecanismo; 2 ocurrencias confirmadas en 2 contextos) — **+1 ocurrencia reforzada el 2026-10-02:** el bloque truncado **sobrevive a la reescritura del fichero**. `validacion-instrumentos-medicion/SKILL.md`: el marcador sigue dentro con mtime **2026-10-02 14:16:16** (66.857 B; línea 36, marcador en la posición 2.862 de 2.873 — la línea acaba en «…tampoco e[truncated]»; la misma línea contiene además una mención legítima del marcador entre backticks, posición 2.513). `render-html-a-imagen/SKILL.md`: marcador intacto con mtime **2026-09-30 11:21** (42.170 B; línea 128, acaba en «…ilegible, desce[truncated]»). Es decir: la edición posterior **hereda** el daño en vez de resolverlo
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón (candidato: **CP-010 un-instrumento-no-validado-miente** — frontera declarada: CP-010 es el MEDIDOR que devuelve una cifra falsa; CP-011 es el ESCRITOR que devuelve OK habiendo escrito menos. Coinciden en «el OK no es prueba»; si en la mensual se confirma que el antídoto es el mismo, se fusionan. **Decidido el 2026-10-02: NO se fusionan** — el antídoto de CP-011 es comprobar tamaño y cola del artefacto; el de CP-010 es etiquetar la validez del número)

**Fecha de revisión:** 2026-11-02 (próxima mensual)
**Justificación:** 2 ocurrencias confirmadas el mismo día en 2 skills de dominios distintos, cada una atada al segundo exacto del `patch` que la produjo (ledger ↔ mtime), más 1 ocurrencia detectada el 24-09 y no reparada. Falta el denominador (cuántas ediciones largas salen bien), aislar el mecanismo interno y decidir la reparación de los 2 bloques perdidos (D8), que no son recuperables desde las copias.
