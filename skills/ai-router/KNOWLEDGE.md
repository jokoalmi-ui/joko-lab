# ai-router — Conocimiento

## Proveedores disponibles

| Proveedor | Tipo | URL / Endpoint | Estado |
|---|---|---|---|---|
| DeepSeek | Externo (API) | deepseek-v4-flash | Principal activo |
| Ollama | Local | http://localhost:11434/v1 | Docker, GPU habilitada |
| Gemini | Externo (API) | API de Google | Pendiente configurar |
| LM Studio | Local (opcional, API) | http://localhost:1234/v1 | API activa, 5 modelos VLM disponibles |
| LM Studio (visión local) | Local (alternativa a Gemini) | http://localhost:1234/v1 | Alternativa local para tareas multimodales |

## Modelos disponibles en LM Studio (2026-07-07)

| Modelo | Tipo | Cuantización | Contexto | Notas |
|---|---|---|---|---|
| `google/gemma-4-e4b` | VLM (visión+lenguaje) | Q4_K_M | 131k | ~4B parámetros, candidato a visión local |
| `google/gemma-4-12b` | VLM | Q4_K_M | 262k | 12B, justo para RTX A2000 12GB |
| `google/gemma-4-12b-qat` | VLM | Q4_0 | 262k | 12B con QAT, versión optimizada |
| `qwen/qwen3.5-9b` | VLM | Q4_K_M | 262k | 9B, buena relación tamaño/calidad |
| `glm-4.6v-flash` | VLM | Q4_K_M | 131k | Modelo flash ligero |
| `text-embedding-nomic-embed-text-v1.5` | Embeddings | Q4_K_M | 2k | Para RAG / búsqueda semántica |

> **Nota:** Los modelos en LM Studio aparecen como `not-loaded`. Hay que cargarlos manualmente desde la interfaz de LM Studio antes de poder usarlos. La VRAM disponible (~10.9 GB) permite cargar modelos de hasta ~9B en Q4_K_M. Los de 12B podrían no caber completos.

## Criterios de enrutamiento detallados

### 1. Privacidad

Regla: si la tarea contiene información personal, financiera, credenciales, datos de clientes o cualquier dato sensible → **Ollama siempre**.

No se negocia: aunque la tarea sea compleja, se prioriza la privacidad. Si el modelo local no puede resolverla, se informa al usuario en lugar de enviarla a un proveedor externo.

### 2. Razonamiento complejo

Regla: si la tarea requiere análisis profundo, múltiples pasos lógicos, depuración de código, o comprensión de contexto largo → **DeepSeek** (v4-flash).

Indicadores: "explica por qué", "compara estas opciones", "encuentra el error en", "diseña una solución para".

### 3. Multimodal

Regla: si la tarea incluye imágenes, PDFs escaneados, gráficos, diagramas o audio → **Gemini**.

Nota: si Gemini no está configurado, se informa al usuario y se sugiere configurarlo. No se intenta procesar imágenes con modelos que no soporten visión.

### 4. Recursos del sistema (memoria)

Regla: si la VRAM libre es menor a 4 GB o la RAM disponible es menor a 8 GB → **modelo ligero local**.

Rango de VRAM y modelo sugerido:

| VRAM libre | Modelo sugerido | Ejemplo |
|---|---|---|
| > 6 GB | Modelo completo (7B-8B) | qwen2.5:7b, llama3.1:8b, llama31-8b-64k |
| 2 - 6 GB | Modelo mediano (3B-4B) | phi4-mini, qwen2.5:3b |
| < 2 GB | Modelo ligero (1B) | llama3.2:1b, tinyllama, qwen2.5:0.5b |

> **Nota:** En tu equipo (RTX A2000 12 GB) con ~10.9 GB libres, entras en la categoría > 6 GB. Los modelos 7B-8B cargan sin problema.

Comando para medir VRAM libre:

```bash
nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits
```

### 5. Consultas rápidas

Regla: si la tarea es una pregunta simple, una transformación de texto breve, o un formato rápido → **modelo ligero local**.

Indicadores: "traduce", "resume", "formatea", "corrige", "convierte", preguntas de una línea.

## Árbol de decisión

```
¿Contiene datos privados?
├── Sí → Ollama (local). ¿No puede resolverlo? → Informar al usuario.
└── No → ¿Tiene imágenes/PDFs?
    ├── Sí → ¿LM Studio con modelo VLM cargado?
    │   ├── Sí → LM Studio (visión local, datos no salen del equipo)
    │   └── No → Gemini (API externa, si configurado) / Informar si no.
    └── No → ¿Requiere razonamiento complejo?
        ├── Sí → DeepSeek V4 Flash (cloud, $0.00023/consulta)
        └── No → ¿VRAM < 2 GB o RAM < 4 GB?
            ├── Sí → Modelo ligero local
            └── No → Modelo local completo (~7B-8B, rápido, sin coste)
```

> **Nota de coste:** DeepSeek V4 Flash cuesta $0.077/M input + $0.154/M output (~$0.00023 por consulta tipica). Es 13x mas barato que Gemini 2.5 Flash. No hay franja cara ni barata — DeepSeek es el cloud por defecto permanente. El unico motivo para forzar local es privacidad de datos, no coste.

## Tareas típicas por proveedor

| Tarea | Proveedor | Motivo |
|---|---|---|
| Diagnóstico del sistema | Ollama (llama31-8b-64k) | Más rápido (1.9s), buena calidad, local |
| Depuración de Docker/n8n | DeepSeek | Razonamiento, contexto largo |
| Análisis de privacidad | Ollama (cualquier modelo) | Datos sensibles nunca salen |
| Procesar factura/PDF con imagen | LM Studio (gemma-4-e4b o similar) si cargado, si no Gemini | Visión local sin enviar datos fuera |
| Traducción rápida | Ollama (llama31-8b-64k) | 1.9s de respuesta, sin coste |
| Diseño de workflow complejo | DeepSeek | Razonamiento estructurado |
| Chat casual | Ollama (llama31-8b-64k) | 1.9s, sin coste, calidad aceptable |
| Resumir documento grande | DeepSeek o llama31-8b-64k | Ambos con 64k de contexto |
| Consulta simple de una línea | Ollama (llama31-8b-64k) | 1.9s, la opción más rápida |

> **Nota de rendimiento (testeado el 2026-07-07):** `llama31-8b-64k` respondió en 1.92s frente a 15.87s (qwen2.5:7b) y 18.32s (llama3.1:8b) para consultas simples. Es el modelo local recomendado por defecto para tareas rápidas.

## Test de razonamiento (2026-07-07)

Se comparó DeepSeek (v4-flash) vs llama31-8b-64k para un script bash con lógica condicional y temporización.

**Resultado:**

| Criterio | DeepSeek | llama31-8b-64k |
|---|---|---|
| Tiempo | ~2-3s | 5.23s |
| Script funcional | ✅ Sí, completo y correcto | ❌ No, errores de lógica |
| Claridad | Alta | Baja |

**Conclusión:** Para razonamiento complejo, DeepSeek es claramente superior. El modelo local sirve para consultas rápidas y diagnósticos, pero no para lógica elaborada.

## Test de visión local (2026-07-07)

Se probó `google/gemma-4-e4b` en LM Studio con una foto real (persona en playa con pala y cubo).

**Resultado:**

| Aspecto | Valor |
|---|---|
| Modelo | google/gemma-4-e4b (~4B, Q4_K_M) |
| Plataforma | LM Studio (localhost:1234) |
| VRAM usada | ~4-5 GB (estimado) |
| Consulta simple texto | 0.25s - 0.58s |
| Visión (imagen real) | ✅ Descripción correcta: "Un niño jugando en la arena de la playa con su pala y cubo" |
| Tiempo visión | ~2-5s (estimado) |

**Conclusión:** gemma-4-e4b es viable como alternativa local a Gemini para tareas multimodales. Es más rápido que cualquier modelo de Ollama y procesa imágenes sin enviar datos fuera del equipo. Queda pendiente probar con PDFs escaneados y documentos más complejos.

## Árbol de decisión actualizado
