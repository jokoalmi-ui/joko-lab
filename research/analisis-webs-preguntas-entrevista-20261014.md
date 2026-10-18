---
title: "Investigación — Webs que registran preguntas de entrevista de trabajo y «pruebas conjuntas» (14-oct-2026)"
type: research
---

# Investigación — Webs que registran preguntas de entrevista de trabajo y «pruebas conjuntas»

Fecha de medición: 2026-10-14, 23:01 CEST (sondeo web de solo lectura; sin coste).
Origen: petición directa del usuario del 14-oct («realiza una investigación sobre webs que
registren preguntas de entrevistas de trabajo o pruebas conjuntas» + «guárdalo como informe
para seguir investigando»). Complementa `analisis-empleate-20261014.md` (fuentes de ofertas)
y `analisis-tecnoempleo-gestionable.md` (portales de empleo IT).

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** búsquedas `web_search` (10 consultas ES/EN, 14-oct-2026) + extracción `web_extract`
(clave-less Exa) de `laentrevista.ai/entrevista`, `comparably.com/interviews`, `leakcode.dev/leaked`,
`psicopol.com/`, `glassdoor.es/Interview/index.htm`, `es.indeed.com/orientacion-laboral/entrevistas`
y variantes. **Dos extracciones fallaron y NO se citan:** `laentrevista.ai/entrevista/bbva` (HTTP 429,
límite de Exa) y `es.indeed.com/career-advice/interviewing` (CRAWL_NOT_FOUND).

**Método:** 10 búsquedas (ES y EN) sobre cuatro categorías: (a) recopilatorios españoles de preguntas
reales, (b) plataformas globales de preguntas por empresa, (c) bancos de psicotécnicos/pruebas de
selección y dinámicas de grupo, (d) sector específico ATM/mantenimiento bancario. Más `search_files`
en `joko-lab` (pattern `entrevista|prueba t[eé]cnica|psicot[eé]cnic`) → 44 ficheros, ninguno con
investigación previa sobre este tema.

---

## 1. Webs con preguntas reales de entrevista por empresa

| Web | Qué ofrece | Acceso | Estado de la cifra |
|---|---|---|---|
| **Glassdoor** (`glassdoor.es`) | El archivo más grande. Fichas por empresa/puesto con preguntas, dificultad y duración del proceso | Gratis **con cuenta Indeed** + modelo **«give-to-get»**: publicas review/salario/reporte de entrevista y obtienes acceso ampliado (se cita 12 meses) | Cifras del snippet (BBVA ~981; Cajero 28 / Gestor Comercial 41 entrevistas): **sin verificar en ficha** |
| **Indeed España** (`es.indeed.com`) | Guías + preguntas por puesto y por empresa; comparte datos con Glassdoor (fusión legal 01-jul-2026) | Gratis con cuenta | Cifras: **sin verificar** |
| **JobMentis** (`jobmentis.com/es/interviews`) | 2.030+ empresas, 20+ sectores; guía gratis con 3 preguntas reales por empresa; más contenido con cuenta gratis. Cubre **banca española** | Freemium | Cifras del snippet: **sin verificar en ficha** |
| **Comparably** (`comparably.com/interviews`) | Alternativa a Glassdoor, sin cuenta Indeed | — | **NO VERIFICADO** en este sondeo |
| **laentrevista.ai**, **Blind**, **levels.fyi**, **leakcode.dev** | Alternativas varias: preguntas por empresa (laentrevista.ai), foro anónimo verificado por email corporativo (Blind), datos de compensación (levels.fyi), fugas de pruebas de código (leakcode.dev — solo dev) | Mixto | **NO VERIFICADO** (429 / sin extracción) |

## 2. Práctica de psicotécnicos y pruebas de selección

| Web | Qué ofrece | Acceso |
|---|---|---|
| **Psicoreto** (`psicoreto.com`) | Banco de 13.518 ejercicios, 12 aptitudes, 92 tipos. Declara servir también para procesos de empresa | **2 tests/día gratis sin registro**; Premium ~10 €/mes |
| **CocoTest** (`cocotest.net`) | Gratis; sección explícita «Selección de personal: CI, personalidad, competencias profesionales y mecanografía» | Gratis |
| **Psicopol** (`psicopol.com`) | El clásico de oposiciones y selección | Gratis con registro |
| **Red Opositor / Opositor.com** | Tests con la penalización real de cada convocatoria | Gratis |

## 3. «Pruebas conjuntas» — el término tiene DOS sentidos (no mezclarlos)

1. **Selección de empresa (prueba grupal / dinámica de grupo / assessment center):** varios
   candidatos a la vez evaluados en equipo. Guías y casos descritos: **Indeed España**, **Randstad**,
   **Infoempleo**, **JobFuturo** (casos «isla desierta», «búnker», «globo»), **trabajoypersonal**
   (assessment center «a la española», 30-45 min). La expresión es la que usa el sector para
   describir la dinámica con todos los candidatos.
2. **Oposición (examen conjunto de varias materias):** un solo ejercicio que agrupa temario y se
   valora en bloque (p. ej. Correos: 60 preguntas tipo test + 40 específicas con valoración conjunta;
   convocatorias de policía: psicotécnicos + conocimientos + personalidad).
   Recursos: Red Opositor, Opositor.com, portales de cada convocatoria.

## 4. Sector del usuario (mantenimiento de cajeros ATM + microinformática bancaria)

Hallazgo principal: **no existe banco de preguntas específico de mantenimiento de cajeros en España.**
Lo aprovechable es genérico de campo/ATM:

- **RoleCatcher**: guía por ocupación «Técnico de reparación de cajeros automáticos» con **10 preguntas
  reales** (priorización de avisos, conectividad de red del ATM, cumplimiento PCI DSS, prueba funcional
  tras reparar, gestión de repuestos) y 13 habilidades con preguntas de ejemplo. Es el único banco de
  preguntas por ocupación localizado para ese puesto.
- **Manatal** y **Breezy** (plantillas de reclutador, ES): *técnico de servicio en campo* — diagnóstico,
  mantenimiento preventivo/calibración, cliente difícil, plazos ajustados.
- **Contexto real del mercado:** ofertas de **Prosegur España** piden NCR, Wincor/Diebold Nixdorf,
  Hyosung, GRG y Fujitsu; recicladores/TVPs; FP Grado Superior; inglés medio.

## 5. Hilos abiertos para seguir investigando

1. Verificar `laentrevista.ai` y `comparably.com` (hoy 429) — ¿cobertura real por empresa y gating?
2. Comprobar si **Laboral Kutxa** tiene ficha con entrevistas en Glassdoor o Indeed (no apareció nada).
3. Confirmar la cobertura de **JobMentis** en banca española (BBVA, Santander, CaixaBank, Kutxa) y su
   nivel de detalle real.
4. Re-verificar las condiciones vigentes del «give-to-get» de Glassdoor (fecha y nº de contribuciones).
5. Ampliar el bloque sectorial ATM: RoleCatcher + plantillas de *field service*, y valorar si merece
   un **banco propio** con las preguntas técnicas de su experiencia (Fujitsu RBU-10/RBU-12, ARCA
   CM14.4/CM14.8/CM24/C18.8, NCR, Wincor, Diebold, Hyosung, De La Rue).
6. Fijar con el usuario si «pruebas conjuntas» = **dinámicas de grupo** o **examen tipo oposición**
   (ramas separadas; hoy están cubiertas las dos, pero sin profundidad).

## 🎯 Aplicación al LAB / a la búsqueda de empleo del usuario

- **Sin coste y con retorno inmediato:** Glassdoor (contribuir un reporte de entrevista propia →
  acceso ampliado) + RoleCatcher/Manatal (preparar 20-25 preguntas técnicas del puesto) +
  Psicoreto/CocoTest (diagnóstico del psicotécnico antes de cualquier proceso, porque suele ser
  el primer filtro de ETT/empresa).
- **Encaja con el seguimiento de empleo** (`seguimiento-empleo`, perfil de `~/empleo-seguimiento/`):
  estas webs son **material de preparación**, no una fuente de ofertas — van aparte de Empleate,
  LANBIDE o PortalBizkaia.
- **Futurible LAB:** un «banco de preguntas técnico» local (markdown o SQLite) alimentado con su
  propia experiencia de campo; coste 0 y reutilizable para cada candidatura.

## Lo que NO se puede afirmar

- Los recuentos por empresa (BBVA ~981; Cajero 28) provienen de **snippets de buscador**, no de la
  ficha abierta: pueden referirse a opiniones totales y no a entrevistas.
- No se ha verificado el contenido de `laentrevista.ai` ni `comparably.com` (429 / sin extracción).
- No se ha abierto ninguna ficha real de Glassdoor/Indeed logueado: el funcionamiento del
  «give-to-get» es lo que dicen fuentes secundarias.
- **No aparece ninguna web con preguntas de entrevista de Laboral Kutxa** ni de mantenimiento de
  cajeros en España: la ausencia es un resultado del sondeo, no una prueba de que no existan.
- Los precios citados (Psicoreto ~10 €/mes) son los del snippet del 14-oct; no se ha pagado ni
  registrado en ninguna de estas webs.

## Veredicto

Categoría **útil y con material real y gratis** para preparación de entrevistas: hay bancos globales
por empresa (Glassdoor/Indeed/JobMentis), bancos de psicotécnicos accesibles sin coste (Psicoreto,
CocoTest) y, para su puesto concreto, solo guías genéricas de campo/ATM (RoleCatcher, Manatal/Breezy).
Nada de pago es imprescindible para empezar. El hueco real (y la oportunidad) es el **banco propio**
de preguntas técnicas de mantenimiento de cajeros, que no existe en abierto.

## Evidencia de origen

10 `web_search` del 14-oct-2026 y extracciones `web_extract` (clave-less Exa) de las URLs citadas
en el bloque **Fuente**. Los volcados crudos de esas consultas **no se persistieron en disco**
(quedan solo en la sesión): lo verificable es el listado de URLs y los puntos reseñados aquí.
