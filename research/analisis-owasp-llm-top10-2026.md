---
title: "Análisis — OWASP LLM Top 10 2026 (IBM Technology / Security Intelligence)"
type: research
---

# Análisis — OWASP LLM Top 10 2026 (IBM Technology / Security Intelligence)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/auS34nm9VAc (IBM Technology / Security Intelligence
podcast — panel de expertos)
**Método:** transcripción VTT EN descargada (284 KB → 91.7K chars limpios)
**Veracidad:** [VERIFICADO] — transcripción real, secciones extraídas

---

## QUÉ ES

Panel de expertos de IBM sobre el **OWASP LLM Top 10 2026** (lista de los 10
mayores riesgos de seguridad en aplicaciones con LLM, actualización del
OWASP Top 10 for LLM Applications).

## RANKING CLAVE 2026 (confirmado en la transcripción)

| Posición | Riesgo | Cambio |
|---|---|---|
| **1** | **Prompt Injection** | = (sigue nº 1, sin sorpresa) |
| **2** | **Sensitive Information Disclosure** | = (igual que la versión anterior) |
| **3** | **Excessive Agency** (agencia excesiva) | ⬆️ **SUBIO 3 PUESTOS** (de la 6ª a la 3ª) |

## PUNTOS CLAVE DEL PANEL

1. **Prompt Injection sigue #1** — era previsible, pero el panel destaca que
   el riesgo de **agentes con permisos excesivos** saltó al top 3: "failing
   to rein in our own models can be a big problem" (no contener nuestros
   propios modelos es un gran problema).

2. **Excessive Agency = el gran salto** — subió 3 posiciones, lo que sugiere
   "un nuevo aprecio por las formas en que no controlar nuestros modelos
   puede ser un gran problema".

3. **Uso recomendado del Top 10** — NO como checklist de compliance, sino
   como **tabletop/ejercicio de mesa**: "si uno de estos ataques ocurriera
   mañana, ¿podrías detectarlo? ¿Podrías contenerlo? ¿Podrías reconstruir
   qué hizo realmente la IA durante el ataque?"

4. **Supply chain** — la visibilidad de dependencias es valiosa: el
   componente vulnerable puede estar "3 o 4 capas de profundidad en algo que
   nunca instalaste conscientemente". Cadenas de suministro de software
   increíblemente profundas.

5. **Lenguaje común para defensores** — el Top 10 da a los defensores un
   vocabulario común para el riesgo de IA (aunque no hay que tratarlo como
   checklist de compliance).

## CONEXIÓN CON EL LAB

| Riesgo OWASP | Estado en el lab |
|---|---|
| Prompt Injection | ⚠️ Gate de veracidad + least-privilege-lab (R1-R5) cubren parcialmente; MCP lab-db es SOLO LECTURA (bien) |
| Excessive Agency | ✅ **Cubierto por diseño**: least-privilege-lab (toolsets mínimos, delegation), no_agent en crons, MCP solo lectura, `enabled_toolsets` mínimos |
| Sensitive Info | ⚠️ Credenciales [REDACTED] en .env, no reproducir valores — política vigente |
| Supply Chain | ⚠️ fastmcp 1.0 tenía 14 avisos OSV (monitorizar); auditado en skill lm-studio |

**Veredicto**: el lab YA implementa la mitigación del riesgo #3 (excessive
agency) mediante least-privilege-lab — buena señal de que la arquitectura
sigue las mejores prácticas OWASP 2026. El tabletop (detectar/contener/
reconstruir) es un ejercicio que no está formalizado.

## FUTURIBLE

- **Ejercicio tabletop de seguridad IA** (detectar/contener/reconstruir ante
  un ataque simulado al lab: prompt injection en n8n, agente con permisos
  excesivos, exfiltración de datos) — señal: antes de exponer servicios del
  lab al exterior (NGINX/Caddy futurible) o al crear bots con Bot Mode
  (0.21.0). Coste bajo (1 sesión), valor alto.

## Nota de proceso
- Transcripción: /tmp/vid_owasp.en.vtt (temporal)
- El 429 inicial en español se resolvió con subtítulos EN
