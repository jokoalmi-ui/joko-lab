---
title: "Análisis — Ya no busco aplicaciones, ahora las creo con IA (hdeleon.net, 15-ago-2026)"
type: research
---

# Análisis — Ya no busco aplicaciones, ahora las creo con IA (hdeleon.net, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/6ZcEEoF9jQQ (12 min, hdeleon.net)
**Transcripción:** completa (es, 401 líneas)
**Fecha:** 2026-08-15 10:45 CEST (verificado con date)

---

## Qué propone el vídeo

**Idea:** crear **aplicaciones personales** (solo para ti, sin publicar, sin
servidor, sin pagar hosting) con IA en **minutos** — y descartarlas si no te
gustan.

**El caso práctico:** app de gastos mensuales en el móvil, construida con
Ionic + Angular + IA.

### El flujo (lo valioso)

1. **Archivo de instrucciones (AGENTS.md/CLAUDE.md del proyecto)** — se genera
   al crear el proyecto con la arquitectura, tecnologías (Ionic, Angular,
   standalone, Bootstrap, tabs) y reglas (código en inglés, validación de
   respuesta "listo, precioso" para confirmar que carga el contexto). Así no
   hay que repetir nada en cada prompt.
2. **Modo plan con modelo ROBUSTO** (ej. Sol) → genera el plan de construcción
   (quitar tabs de ejemplo, persistencia con servicio JSON, borrado lógico,
   navegación solo gastos/categorías, moneda local).
3. **Construcción con modelo BARATO** ("pedorrón" — el autor) → ejecuta el
   plan ya definido. *"El plan ya le va a dar los pasos."*
4. **Verificación humana del código** — el autor revisa los puntos de
   no-determinismo (IDs, validaciones, borrado lógico) para asegurarse de que
   la IA hizo lo que esperaba. *"A mí me gusta seguir leyendo el código... y
   ver si hay una incoherencia o algo no determinista."*
5. Persistencia local con Capacitor Preferences (JSON), sin SQLite (no hace
   falta para algo pequeño), validaciones separadas en métodos, lógica de
   negocio encapsulada en servicios (buena práctica Angular).

### Marketing
- Cursos en Metal Code (15% descuento con cupón), curso de "programación
  asistida con IA".

---

## Veredicto para el lab

### ✅ VALIDA 3 patrones que el lab YA usa (nada nuevo, pero confirmación)

| Patrón del vídeo | Equivalente en el lab |
|---|---|
| **Modo plan (modelo robusto) → construcción (modelo barato)** | **Router del lab**: R1-14B para razonamiento/plan, modelo rápido para ejecutar; el router decide local/cloud según la tarea |
| **Archivo de instrucciones del proyecto** (no repetir contexto) | **Skills + GUIA-JOKO-LAB.md + file bus del lab** — el contexto vive en archivos, no en cada prompt |
| **Verificación humana del código generado** (buscar no-determinismo) | **Gates del lab** (SVP, evidence F4, KVC, KCR) + suite 205 OK — verificar lo que el agente hizo, nunca fiarse |

### 🚫 NO accionable directamente

- El lab no necesita crear apps Ionic/Angular (su "aplicación" es el propio
  lab: scripts + servicios + crons)
- Es un caso de uso distinto (desarrollo móvil personal), no un gap del lab

### ⭐ La perla (idea aplicable)

**"Modelo robusto en modo plan → modelo barato en construcción"** es el
patrón de **token budgeting** que el lab ya sigue — pero el vídeo lo lleva al
extremo: **ni siquiera usa modelos de frontera para construir** (solo para
planificar). Confirma la dirección del lab: el coste no está en el modelo de
ejecución, está en el razonamiento/contexto (99% del coste DeepSeek =
contexto, según el análisis del lab).

**Futurible (menor):** si algún día el lab necesita una UI/web app, Ionic +
IA es el camino validado (corre en web/escritorio/móvil con un solo código).

### 📌 Nota honesta

- Vídeo divulgativo con fuerte componente de marketing (curso)
- El flujo real es sólido: la app funciona, el autor muestra el resultado
  (gastos, categorías, total del mes)
- Canal **hdeleon.net** — nivel medio (desarrollo web + IA aplicada), para
  la lista de referencia como canal menor

---

## Registro

- Guardado: research/analisis-apps-personales-ia-hdeleon.md
- Veredicto: **VALIDA 3 patrones del lab (plan→construcción, instrucciones en
  archivo, verificación humana) — NO accionable (caso móvil/Ionic); perla:
  modelo robusto solo para planear, barato para construir; canal menor de
  referencia**
- Relacionado: llm-router.sh, token budgeting (coste DeepSeek), gates SVP/F4
