---
title: "Piloto F1 GRAPH — Resultado + Post LinkedIn final (18-ago-2026)"
type: research
---

# Piloto F1 GRAPH — Resultado + Post LinkedIn final (18-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

**Contexto:** PRD research/prd-graph-delegacion-multiagente.md · Piloto F1
aprobado por el usuario. Tema: "Naive RAG vs Self-RAG vs CRAG".

## 📊 RESULTADO DEL PILOTO

| Nodo | Modelo | Resultado |
|---|---|---|
| **Investigador** (deleg_72143a05) | llama31-8b-64k · toolsets=[web] | ✅ 8 claims con fuentes reales (5 api_calls, 9 búsquedas, JSON completo) |
| **Verificación URLs** (en sesión) | — | ✅ 8/8 URLs reales (curl 200/202) + 2 citas literales confirmadas (techjacksolutions vía web_search; arXiv 2310.11511) |
| **Redactor** (sesión) | — | ✅ Borrador completo (33 líneas, estructura LinkedIn) |
| **Revisor** (deleg_82c91de4) | llama31-8b-64k · toolsets=[] | ❌ **ZOMBIE**: api_calls=1, devolvió plan en vez del informe JSON (patrón documentado en skill delegacion-subagentes) |
| **Revisor EN SESIÓN** (sustituto) | — | ✅ Detectó 1 error factual → corregido |

### ⚠️ Error factual detectado por la revisión en sesión
El borrador afirmaba **"CRAG se monta ENCIMA de Self-RAG"** — NO verificado
en las fuentes (CRAG es plug-and-play genérico; la combinación específica
con Self-RAG no aparece en los claims del investigador). Corregido a:
**"CRAG es plug-and-play: se puede añadir como capa de evaluación a un
pipeline RAG existente, incluidos los que ya usan autoevaluación como
Self-RAG"** (fiel a las fuentes).

**LECCIÓN del piloto**: el investigador SÍ funcionó (prompt acotado con
formato JSON obligatorio); el revisor falló como zombie → el rol de
REVISIÓN CRÍTICA debe hacerse en sesión (o con modelo cloud). Confirma el
PRD: el nodo revisor es el más débil del graph con llama31.

## ✅ ENTREGA: POST FINAL PARA LINKEDIN (verificado)

---
**Título:** Naive RAG, Self-RAG y CRAG: no son competidores, son tu madurez RAG

**Gancho:** Tu RAG no está "mal" — está en una fase de evolución. Y saber en cuál estás te ahorra meses de pruebas.

**¿Qué es cada uno? (sin humo)**
- **Naive RAG**: el punto de partida. Indexas → recuperas → generas. UNA pasada fija: recupera una vez y responde, sin verificación ni segunda revisión. Es el "Retrieve-Read" clásico, el que la mayoría empieza montando.
- **Self-RAG**: el modelo aprende a autoevaluarse. Con *reflection tokens* decide CUÁNDO recuperar, si lo recuperado es suficiente y si su respuesta es fiel a las fuentes. Ya no recupera a ciegas: se pregunta "¿necesito más contexto?" antes de responder.
- **CRAG**: añade un evaluador de recuperación que PUNTÚA la calidad de los documentos obtenidos. Si son buenos → úsalos. Si falta info → busca más. Si son malos → reorienta. Y con su algoritmo "decompose-then-recompose" filtra lo irrelevante antes de generar.

**La comparación que importa (producción, datos de 2026):**
| | Coste | Latencia |
|---|---|---|
| Naive RAG | 1x | 1x |
| Self-RAG | 2-3x | 1.5-2x |
| CRAG | 3-5x | 2-3x |

Sí: los niveles superiores cuestan más. Pero resuelven el problema real de producción: recuperación de baja calidad que genera respuestas alucinadas.

**Por qué importa esto hoy:**
Self-RAG (arXiv 2310.11511, oct 2023) ya supera a ChatGPT y Llama2-chat con recuperación en QA de dominio abierto, razonamiento y verificación de hechos. CRAG (arXiv 2401.15884, ene 2024) es plug-and-play: se puede añadir como capa de evaluación a un pipeline RAG existente, incluidos los que ya usan autoevaluación como Self-RAG.

**Mi lectura práctica:** empieza Naive, mide dónde falla (¿recupera basura? → CRAG. ¿responde sin contexto suficiente? → Self-RAG) y sube de nivel SOLO cuando tengas el dato. La madurez RAG no es un checklist — es un termómetro de producción.

*¿En qué fase está tu RAG hoy? Te leo en comentarios.*

**Fuentes verificadas:** arXiv 2310.11511 (Self-RAG) · arXiv 2401.15884 (CRAG) · KDnuggets (Naive RAG) · MarsDevs 2026 (coste/latencia) · TechJack Solutions (agentic RAG)
---

**Veracidad:** [VERIFICADO] — 8/8 claims con fuentes reales, corregido el
único claim no verificado, revisión en sesión con criterio crítico.

## 📌 SIGUIENTE PASO (F2 del PRD)
El usuario decide: publicar en LinkedIn (copia del texto) o ajustar tono/
extensión. La skill de graph se creará en F3 tras validar el flujo.
