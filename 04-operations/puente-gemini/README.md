---
title: "Puente manual LAB <-> Gemini web (Google AI Pro)"
type: operations
---

# Puente manual LAB ↔ Gemini web

Instrumento para aprovechar la suscripción **Google AI Pro** (21,99 EUR/mes)
donde es insuperable —3.1 Pro con contexto 1M, Deep Research, NotebookLM,
Gems, Workspace— **sin API** y sin violar los términos: el trasvase lo hace el
usuario a mano, pegado en la web. Nada de scraping, cookies ni proxies.

Referencias: `01-knowledge/objects/DEC-GAIPRO-001.yaml` · skill `google-ai-pro`.

## Por qué manual y no automatizado

- La suscripción **no da créditos de API** (la API se paga aparte).
- El login OAuth de **Gemini CLI / Code Assist se cerró el 18-jun-2026** para
  cuentas individuales → el CLI exige API key propia.
- Automatizar la web (cookies, scraping, MCP de navegador) **viola ToS y
  arriesga el baneo de la cuenta** → descartado (verificado 05-sep-2026,
  `~/.hermes/skills/productivity/google-ai-pro/references/gemini-gratis-20260905.md`).
- Manual = dentro de los términos y 0 EUR extra.

## Las tres carpetas

- `outbox/` — el prompt listo, con el contexto ya redactado. **Escribe el LAB.**
- `inbox/` — la respuesta pegada desde Gemini web. **Escribe el usuario.**
- `procesados/` — respuestas ya verificadas e incorporadas. **Escribe el LAB.**

El contenido de esas tres carpetas **no se versiona** (lo ignora
`puente-gemini/.gitignore`, verificado en el archivo); solo se versionan este
README, la plantilla y el registro.

## Ciclo completo (3 pasos)

1. **El LAB prepara el prompt**
   `python3 tools/puente_gemini.py nuevo "<tema>" --herramienta 3.1-pro`
   → escribe `outbox/AAAA-MM-DD-HHMM-<tema>.md` con la ficha y el bloque de
   prompt rellenos.
2. **El usuario trasvasa** — abre el fichero del outbox, copia SOLO el bloque
   `PROMPT`, lo pega en gemini.google.com (o en el cuaderno/Gem que toque),
   copia la respuesta completa y la guarda como
   `inbox/AAAA-MM-DD-HHMM-<tema>-respuesta.txt`. Avisa por Telegram: «trae el
   inbox».
3. **El LAB verifica y cierra**
   `python3 tools/puente_gemini.py archivar <fichero> --valor 4 --nota "..."`
   → mueve el fichero a `procesados/` y añade la línea al registro. La
   respuesta **no se usa** hasta pasar el gate de veracidad: toda cifra que
   venga de Gemini web se contrasta contra datos reales del lab antes de
   incorporarla (skill `gate-veracidad`).

## Frontera de datos — qué NO se pega

- Credenciales, claves, tokens: **nunca**.
- Datos de terceros (entorno/familia) sin necesidad: **nunca**.
- Sesiones o logs completos: no; solo el extracto mínimo.
- Todo lo que la ficha marque como `[NO PEGAR]` se queda fuera.

## Registro y medida

`registro-puente.md` anota cada ida y vuelta (fecha, tema, herramienta, valor
1-5, alternativa local, nota). Es el instrumento de medida que alimenta el
registro semanal `04-operations/registro-uso-gemini.md`, que a su vez sostiene
la revisión mensual de `DEC-GAIPRO-001`.
