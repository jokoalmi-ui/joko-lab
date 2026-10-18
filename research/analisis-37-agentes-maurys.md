---
title: "Análisis — Equipo de 37 Agentes IA (maurys_alvarez_, 15-ago-2026)"
type: research
---

# Análisis — Equipo de 37 Agentes IA (maurys_alvarez_, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcByMArjN7L/ (carrusel 10 slides, img_index 5)
**Autor:** maurys_alvarez_ (mismo autor de "Sistema Operativo de IA" analizado 12-ago)
**Método:** 10/10 slides descargadas del CDN + GLM-4.6V-Flash local (prompt directo)

---

## Contenido del carrusel

**Título:** "Así manejo mi equipo de 37 agentes de IA" — evolución del concepto
"Sistema Operativo de IA" (12-ago) ahora con equipo multiagente por departamentos.

| Slide | Contenido |
|---|---|
| 1 | 37 agentes, un solo mando, cero caos: Piensa → Delega → Ejecuta (roles: Conductor, Paperclip, Fables, Hermes) |
| 2 | Agente **Conductor**: recibe instrucción, divide por departamentos (Ventas, Marketing, Finanzas, Legal, Operaciones, Soporte, Análisis), supervisa |
| 3 | Corre en **Claude Code Headless** (sin interfaz, suscripción actual, continuidad) |
| 4 | **Paperclip**: repo open source multiagente para escalar |
| 5 | **Fables**: agente director que instruye (traduce tareas en órdenes), dirige jefes de departamento, alinea contexto, verifica avance |
| 6 | **Hermes = capa de acción** con GLM 5.2: PIDE → ACCIONA → ENTREGA (Acciones, Herramientas, Ejecución, Flujo) |
| 7 | "El Cerebro evita alucinaciones": **Núcleo de Conocimiento** (memoria central: empresas, socios, empleados, documentos) → guardar, contextualizar, responder con precisión |
| 8 | "Mi sistema corre TODO local" (control, privacidad, estabilidad, escalar) |
| 9 | **Tailscale** lo lleva a todos lados (acceso remoto seguro, MacBook, sistema base 24/7) |
| 10 | CTA: "comenta BUILD" → repo premium (marketing/leads) |

---

## Veredicto

### ✅ VALIDA el lab (tercera validación del mismo autor, ahora con detalle de implementación)

| Idea del carrusel | Equivalente REAL en el lab |
|---|---|
| Agente Conductor que divide por departamentos | **Hermes** + skills por dominio (perfume, café, bolsa, biohacking, founderz...) |
| Memoria central que evita alucinaciones (slide 7) | **RAG LanceDB (19.894 filas) + SVP + evidence_contract** — exactamente la capa 1-2 del control anti-alucinación |
| Todo local | **Local-first** del lab (LM Studio + R1 + GLM + BGE-M3) |
| Hermes como capa de acción | **El lab USA Hermes Agent** (Nous) como orquestador — validación externa de la herramienta |
| Paperclip open source multiagente | El lab decidió **no-multi-agente** (topología no aporta; 22 frameworks analizados 09-ago) |
| Tailscale acceso remoto | Futurible menor (el lab no opera remoto hoy) |
| Claude Code Headless | Equivalente: OpenCode/Aider workers (ya instalados) |

### 🚫 NADA accionable nuevo

- Es el **mismo concepto del 12-ago** ("Sistema Operativo de IA") con más detalle
  de la implementación del autor — no aporta técnica nueva al lab
- El lab ya cubre los 4 bloques del sistema (Conductor=Hermes, Memoria=RAG,
  Local=local-first, Agentes=workers) con datos reales
- Slide 10 = **marketing puro** (repo premium a cambio de comentario "BUILD")
  — mismo patrón comercial que detectamos en briascoi (vende curso)

### 📌 ÚNICO matiz aprovechable (menor)

- **Hermes como "capa de acción" con VLM (GLM)**: el autor usa la MISMA
  arquitectura que el lab (orquestador + modelo de visión local + acciones).
  Sirve como **validación externa para LinkedIn Lab / TFM** ("el patrón que
  usamos es el que otros venden como sistema operativo de IA").
- **Tailscale**: si algún día el usuario quiere operar el lab fuera de casa,
  es la vía de acceso remoto segura (futurible, no urgente).

---

## Registro

- Guardado: research/analisis-37-agentes-maurys.md
- Veredicto: **VALIDA (3ª del autor) + nada accionable + material TFM/LinkedIn**
- Relacionado: research/analisis-sistema-operativo-ia.md (12-ago)
