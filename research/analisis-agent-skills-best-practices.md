---
title: "Análisis — 5 Best Practices para Agent Skills (vídeo YT, 12-ago-2026)"
type: research
---

# Análisis — 5 Best Practices para Agent Skills (vídeo YT, 12-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 12-ago-2026 (08:00 CEST)
**Fuente:** https://youtu.be/qYNs80FKIVc — vídeo de desarrollo (transcripción completa)
**Tema:** Cómo construir bien las agent skills (procedimientos para agentes IA).
Formato: skill.md (YAML frontmatter + markdown) en una carpeta, con references/ y scripts/.
Estandar abierto: agentskills.io.

---

## Las 5 Best Practices (con los datos del vídeo)

### 1. LA DESCRIPCIÓN ES EL GATILLO
- El agente solo ve name + description de cada skill al arrancar (no puede leer
  las 100 skills sin llenar el contexto).
- La descripción debe decir QUÉ hace Y CUÁNDO usarla ("genera el informe mensual
  de compliance, usado cuando pidan el informe o el filing mensual").
- ⚠️ Los modelos tienden a UNDER-trigger (no usar skills que deberían) → la
  descripción debe ser un poco "vendedora" (oversell), no tímida.
- Límites agentskills.io: name ≤64 chars, description ≤1024 chars.

### 2. CONSTRUIR DESDE EXPERTICIA REAL (no dejar que el LLM la escriba)
- Si el LLM escribe la skill sola → "generic mush" ("maneja errores
  apropiadamente, valida inputs" — cosas que el modelo ya sabe).
- La skill debe contener TU forma específica de hacer un trabajo concreto.
- Dos vías: (a) caminar la tarea a mano una vez y anotar qué funcionó (incluyendo
  correcciones); (b) sintetizar desde artefactos reales (informes, runbooks,
  PR reviews).
- Simon Willison: "keep the domain expertise and let the agent do the routine part"
  → TÚ pones la expertise, el modelo pone la mecanografía.
- **El mayor valor del cuerpo de la skill: GOTCHAS** — hechos específicos del
  entorno que desafían suposiciones razonables. Cada corrección manual = un gotcha.
  "Si no lo escribes, harás la misma corrección la semana que viene."

### 3. GASTAR CONTEXTO CON SABIDURÍA (cuerpo <500 líneas / ~5K tokens)
- Cuando el agente SELECCIONA una skill, lee el cuerpo → ese contexto compite
  con todo lo demás.
- Solo escribir lo que el modelo NO sabría por sí mismo (no "qué es un PDF").
- Si el cuerpo excede ~500 líneas → mover detalles a `references/` (progressive
  disclosure: el agente solo abre los archivos cuando los necesita).
- **Matiz (el vídeo lo muestra): 2 y 3 parecen opuestos (más detalle vs más
  lean) — la solución es: detalle en references/ (bajo demanda), cuerpo lean.**

### 4. USAR SCRIPTS DETERMINISTAS para pasos frágiles
- "Match how prescriptive you are to how fragile the step is":
  paso flexible → instrucciones; paso frágil → CÓDIGO (scripts/).
- El script no entra en contexto (ahorra tokens) y no improvisa (más fiable).
- Ser explícito sobre la intención: "RUN este script" vs "lee esto como
  referencia" — no dejar que el modelo lo adivine.
- Caso real del vídeo: informe con sumas que no cuadraban → se convirtió el
  cálculo en un script determinista → "toda esa clase de bug desaparece".
- "A test only catches what you already thought to check. The answer is: for
  the parts that have to be right, take the guess out of the loop."
- Pasar de probabilístico (agente improvisando) a determinista (lógica dura).

### 5. VETAR UNA SKILL ANTES DE EJECUTARLA (seguridad)
- Una skill puede contener scripts ejecutables con acceso a: sistema de archivos
  local, API keys.
- ⚠️ **DATO CLAVE: auditoría 2026 de ~4.000 skills públicas: >35% tenían algún
  fallo de seguridad, 13% algo crítico (prompt injection o malware).**
- Tratar una skill como cualquier dependencia: leer qué hace y a qué accede
  ANTES de ejecutarla. El estándar abierto NO garantiza seguridad.

### Resumen del vídeo
Una buena skill: se gatilla (1) + construida con expertise real (2) + lean (3)
+ scripts deterministas donde la improvisación sería peligrosa/inconsistente (4)
+ vetada antes de ejecutar (5).

---

## 🎯 Aplicación al LAB — VALIDACIÓN MASIVA DE LAS SKILLS DE HERMES

### El lab YA cumple las 5 (y el vídeo lo confirma)

| Best Practice | Lab (Hermes skills) |
|---|---|
| **1. Descripción = gatillo** | ✅ Hermes usa name+description para el skill matching; las skills del lab tienen descripciones con "use when..." |
| **2. Expertise real** | ✅ Las skills del lab son 100% de experiencia real (pitfalls de sesiones, correcciones documentadas) |
| **3. Contexto sabio / progressive disclosure** | ✅ **El lab YA usa references/** (historial-completo, detalle por tema) — mismo patrón exacto del vídeo |
| **4. Scripts deterministas** | ✅ **El lab lo hace extensivamente**: scripts/ en skills (fetch_transcript.py, analizar-carrusel-rapido.py, verify-monitor-health.py), crons no_agent (deterministas), watchdog |
| **5. Vetar antes de ejecutar** | ⚠️ **El punto donde el lab puede mejorar** — ver abajo |

### El matiz de las 5 vs el estado del lab

**Fortalezas confirmadas:**
- El patrón references/ del lab = progressive disclosure del vídeo (práctica 3)
- Los crons no_agent con scripts = "quitar la conjetura del loop" (práctica 4)
- Los pitfalls en las skills = "cada corrección manual es un gotcha" (práctica 2)

**⚠️ Gap real (práctica 5 — seguridad):**
- El lab descarga/usa skills del ecosistema (ej: las de la tienda de skills de
  Hermes, skills de la comunidad). La auditoría dice 35% con fallos y 13% crítico.
- **Mejora: auditar las skills instaladas de terceros** (leer qué hacen, a qué
  acceden) antes de usarlas. El lab no tiene un proceso formal de veting.

**⚠️ Matiz interesante (práctica 3 vs 2):** el lab tiene skills MUY largas
(perfume-ia 96K chars, lm-studio 12K, biohacking-cerebral largo) — el vídeo
recomienda <5K tokens de cuerpo y mover el detalle a references/. El lab ya lo
hizo con lm-studio (compactado 86K→12K) y local-rag (92K→14K) — pero perfume-ia
sigue siendo enorme. **Futurible: compactar perfume-ia como se hizo con lm-studio.**

### Futuribles
1. 🟢 **Auditar skills de terceros** (práctica 5): proceso de veting antes de
   usar skills de la comunidad (35% con fallos, 13% crítico según auditoría 2026).
2. 🟡 **Compactar perfume-ia** (96K chars → ~12K con references/) — mismo patrón
   que lm-studio/local-rag (práctica 3).

## Conclusión
Vídeo de altísima relevancia: **valida el diseño de skills del lab en 4 de 5
prácticas** (el lab ya hace progressive disclosure, scripts deterministas y
gotchas). Aporta 2 futuribles: auditoría de seguridad de skills de terceros
(práctica 5 — el gap real) y compactación de perfume-ia (práctica 3).

## Nota técnica
- Transcripción en inglés (sin versión es)
- Formato skill.md del vídeo = el mismo de Hermes (YAML frontmatter + markdown)
