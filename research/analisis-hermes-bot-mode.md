---
title: "Análisis — Vídeo \"Hermes Bot Mode: Create Your Own AI Employee Team\" (19-ago-2026)"
type: research
---

# Análisis — Vídeo "Hermes Bot Mode: Create Your Own AI Employee Team" (19-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/lI0WMeTEwYQ (Codedigipt)
**Método:** transcripción VTT en inglés descargada y verificada (23.534 chars limpios)
**Veracidad:** [VERIFICADO] — técnica extraída de la transcripción real

---

## QUÉ ES (extraído de la transcripción)

**Hermes Bot Mode = función nativa de Hermes Desktop 0.20.3+** para crear
múltiples BOTS (agentes con rol) que se comunican entre sí.

### Cómo funciona
1. **Pestaña "Bots"** en Hermes Desktop (junto a la sesión normal)
2. Crear bots con: emoji, nombre, descripción, **system prompt** (identidad,
   responsabilidades, niveles de severidad), capability
3. Los bots se comunican **@mencionando** a otros bots (ej. `hi @backend-dev`)
4. El bot receptor recibe el mensaje **con todo el contexto de su rol** y responde
5. Es un **equipo de IA**: AI Researcher → Code Reviewer → Backend Dev, etc.

### Detalles técnicos verificados
- Versión mínima: **0.20.3** (el autor insiste en actualizar)
- **Requisito para comunicación entre bots**: gateway activo
  (`hermes gateway status`; si no corre → `hermes gateway install`)
- Se puede pedir a ChatGPT/otro LLM que genere el system prompt del bot
- Modelos gratuitos incluidos en desktop (HoI 3, Laguna S 2.1, Step 3.7 flash
  — nombres de la transcripción, no verificados contra la doc oficial)

### Comparación con alternativas (según el autor)
- **Gorgon bot (Otto?)**: misma feature pero PAGADA (suscripción)
- **Hermes Bot Mode**: **gratis**

---

## 🎯 CONEXIÓN CON EL LAB — CRÍTICA

**El lab YA construyó esto como procedimiento manual** (PRD graph de
delegación multi-agente, 18-ago, F0-F4 + skill graph-lab + piloto F1):
Coordinador → Investigador → verificación URLs → Redacción → Revisor.

**PERO con una limitación verificada:** la delegación con modelo local
(llama31-8b) falló 4/5 veces → investigación SIEMPRE en sesión (regla
definitiva documentada en graph-lab).

**Bot Mode haría esto de forma NATIVA:** cada bot = un agente con rol propio
y system prompt persistente, comunicándose con @menciones — sin necesitar
delegate_task ni subagentes frágiles.

### Estado real del lab vs requisito
| Requisito | En el lab | Dato real |
|---|---|---|
| Hermes ≥ 0.20.3 | ⚠️ **NO — estamos en 0.17.0** | `/handoff` roto, esperando 0.21.0 (~20-23-ago) |
| Gateway | ✅ Activo | Telegram conectado (este canal) |
| Uso de bots | ⏸️ Futurible | Cuando se actualice Hermes |

---

## 📌 VEREDICTO

**FUTURIBLE PRIORITARIO — no implementable hoy:**
- **Señal de activación:** actualización de Hermes a ≥ 0.20.3 (revisar el
  23-ago con la 0.21.0) + primera tarea que justifique un equipo de bots
- **Encaje:** ALTO — el lab ya tiene el PRD del graph y las lecciones
  (revisor en sesión, prompts JSON cerrados); Bot Mode los haría nativos
- **Riesgo:** bajo (gratis, local-first); validar qué modelos puede usar
  (los gratuitos de desktop o los locales del lab: GLM/R1)

**Regla DataStreak:** know-how (cómo crear bots) → a skill cuando se
implemente; la herramienta (Bot Mode) llega con la actualización.

**Nota:** el autor menciona ChatGPT para generar system prompts — el lab
puede hacerlo con sus propios modelos (GLM-4.6v) o con la skill de
prompt-engineering existente.

---

**Backlog:** entrada añadida con backup (RULE-008)
