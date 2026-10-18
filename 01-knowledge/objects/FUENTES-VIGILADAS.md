# FUENTES-VIGILADAS

Registro de fuentes externas (sitios y directorios) que el lab decide vigilar, con la
superficie a consultar, el filtro y la **tasa de señal medida**. La receta de cómo evaluar
un sitio externo está en la skill `triaje-contenido-externo`
(`references/evaluar-fuente-o-directorio.md`); **aquí solo el estado**.

Norma de entrada: una fuente entra solo con números medidos (cadencia, señal/ruido) y con
**OK explícito del usuario**. Vigilar es leer: no autoriza a citar sus cifras ni a publicar
nada desde aquí.

## Registro

| Fuente | Superficie principal | Filtro | Señal medida | Decisión |
|---|---|---|---|---|
| aiidelist.com | `sitemap.xml` + índice del blog | hermes\|nous\|opencode\|mcp\|pricing\|limit\|quota\|open-weights\|gguf\|local\|jev\|laya | 4/33 (12%) estricto · 11/33 (33%) amplio | vigilar filtrado (24-sep-2026) |

## aiidelist.com — ficha de la fuente (24-sep-2026)

- Qué es: directorio «AI IDE List» (se leyeron 237 y luego 251 fichas: **fechar toda cifra**).
  Cubre Nous Research, OpenCode, OpenRouter, Hugging Face.
- **Superficie principal: `sitemap.xml`** (299 URLs con `lastmod`) y el índice del blog.
- **El RSS `updates.xml` NO vale como única superficie**: 33 items entre el 26-ago y el
  18-sep-2026, solo categorías `news` (6) y `guide` (27), y **no contenía el artículo de
  LAYA** ni el clúster Apple de los días 23-24. Es una ventana incompleta y retrasada.
- El sitemap también es parcial: publica solo 12 URLs `/ide/` (frente a ~250 fichas) y no
  incluye `/jev`, que sí existe.
- Reparto medido sobre 208 URLs sin traducción: agentes comerciales 63 (30%) · visión 25 ·
  precios/cuotas 13 · Apple 11 · OpenCode/Pi/Aider/Cline 6 · MCP/plugins/skills 6 ·
  navegador y scraping 6 · **local/open-weights/GGUF/Ollama/LM Studio 3** ·
  **Hermes/Nous 1** · decisión/JEV/Laya 1 · **n8n 0**.
- Cadencia: ráfagas, no goteo (semanas ISO: 2,1,3,7,9,10,·,3,5,6,27,56,10,12,57). ~30% del
  sitio son traducciones zh/ja/ko del mismo contenido: es escalado SEO, no redacción nueva.
- Límite medido: **~1 de cada 8 piezas es aplicable a este stack**, y **0** sobre el núcleo
  local (Ollama, LM Studio, GGUF, CUDA, RAG, n8n). Sus latencias son de otra máquina y sus
  artículos no citan fuentes.

## Reglas de uso

1. Se consulta el **sitemap o el índice del blog**, no solo el RSS, y se aplica el filtro de
   palabras clave. Esperar ráfagas: la media semanal engaña.
2. Las cifras del sitio (nº de fichas, precios, latencias) **no entran como dato del lab**:
   se fechan, se miden dos veces si deciden, y se contrastan en fuente primaria.
3. La pieza concreta hallada se registra como **caso puntual fechado**, con aviso si es de un
   tercero o de un port no oficial; nunca como muestra representativa de la casa.
4. Vigilar no se automatiza (cron, script o suscripción) sin OK explícito del usuario.
5. Si la fuente deja de cumplir (señal medida por debajo o datos falsos contrastados), se
   anota aquí la baja con fecha; RULE-017 se aplica a canales de contenido y RULE-013/015 a
   todo dato.
