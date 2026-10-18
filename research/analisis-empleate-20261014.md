# Analisis: Empleate (empleate.gob.es) como fuente para el seguimiento de empleo

Fecha de medicion: 2026-10-14 (sondeo de solo lectura del propio portal, ~09:35-10:00 CEST)
Origen: repaso de la tarde del bloque `MARCA: empleate-20261014` de `04-operations/backlogs/pendientes.md`.

## Que es

Portal del SEPE. Es a la vez SPA (Angular) y AGREGADOR: no publica ofertas propias, reingesta de
portales privados y de servicios publicos de empleo. Portada leida el 14-oct:
28.458 ofertas privadas / 5.352 plazas de empleo publico / 94.334 empresas / 914.803 personas.

## Hallazgo util: API JSON abierta

- Busqueda: `/empleate/open/offersearch/selectBuscador?...&wt=json` (backend Solr). Sin login, no documentada.
- Ficha por oferta: `/empleate/open/offer/load/<id>`.

Pegas medidas:

- El certificado del servidor llega SIN cadena completa: `curl` falla con exit 60 (hace falta `-k`).
  `-k` no puede quedar como norma: la ruta correcta es resolver la cadena
  (`openssl s_client -showcerts` -> `--cacert`). Sin verificar todavia.
- El WAF devolvio `FAIL!` una vez por rafaga de peticiones.
- No hay RSS: esas rutas devuelven la pagina del WAF.

## Medido: Bizkaia, 575 ofertas activas

Origen de la oferta: LANBIDE 359 (62 %), INSERTIA 167 (29 %), PORTALENTO 15, WEB 11,
GESTIONANDOTE 8, COGITI 7, HACESFALTA 5, TECNO_EMPLEO 2, SOC 1. Nuevas en los ultimos 7 dias: 96.

Terminos en Bizkaia: informatica 56 / redes 43 / automatizacion 6 / soporte informatico 6 /
ciberseguridad 2 / python 1 / IA 1 / `inteligencia artificial` 0 / machine learning 0.
En toda Espana, `inteligencia artificial`: 233.

## Veredicto

Para el nicho del usuario (IA / LLM / RAG) en Bizkaia aporta poco: el termino `inteligencia
artificial` da 0 ofertas en Bizkaia. Lo aprovechable es (a) INSERTIA y LANBIDE como fuentes
mayoritarias y (b) que sea API oficial en vez de scraping.

## Decision

P1 (anadir Empleate como fuente API en `perfil.json` de `~/empleo-seguimiento/`) queda APLAZADO
hasta resolver la cadena TLS. Hoy `fuentes.api` de ese perfil contiene solo `remotive`; LANBIDE y
PortalBizkaia entran por `web_search`, no por API.

## Lo que NO se puede afirmar

- Que los recuentos sigan iguales: el indice es vivo y cambia (los de arriba son la foto del 14-oct).
- Que la busqueda por terminos sea exhaustiva: `q=` es texto libre, no la clasificacion CNO.
- Que exista endpoint legible de la seccion de empleo publico: no se encontro.

## Evidencia de origen

Sondeo de solo lectura del portal (portada, facetas de Solr y fichas de oferta) el 14-oct-2026.
El slide que motivo el analisis se leyo con `glm-4.6v-flash` y sus nombres dudosos se contrastaron
contra la fuente que cita al pie (`elenahuerga.com/listado-de-portales-de-empleo-generales-y-por-sectores/`).
