---
title: "Análisis — Infografía: Top 15 System Design Patterns (abhi_techhub)"
type: research
---

# Análisis — Infografía: Top 15 System Design Patterns (abhi_techhub)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://www.instagram.com/p/DbdLpnlE3XI/ — abhi_techhub (Abhishek, verificado)
**Método:** Descarga de carrusel (10 slides CDN) + análisis GLM 4.6V local
**Imágenes:** /tmp/infografia_abhi/slide_01..10.jpg

---

## PARTE 1 — Contenido (¿aprovechable para el lab?)

### Qué es
Infografía de entrevistas: **"Top 15 Must-Know System Design Patterns"** — 15
patrones de diseño de sistemas, cada uno en su slide, formato consistente.

### Los 15 patrones (índice slide 1)
1. Load Balancer
2. Caching
3. Database Replication
4. Database Sharding
5. Message Queue
6. Event-Driven Architecture
7. API Gateway
8. Circuit Breaker
9. CQRS
10. Saga Pattern
11. Rate Limiting
12. Distributed Lock
13. Service Discovery
14. CDN
15. Final Cheat Sheet

### Formato de cada slide (consistente)
- Título del patrón (ej. "9. CQRS — Comando Query Responsabilidad Segregación")
- **¿Por qué usar X?** — motivo
- **¿Cómo funciona?** — flujo
- **Tabla de diferencias** (cuando aplica)
- **Casos de uso**
- **Beneficios**
- **Diagrama con cajas y flechas** (usuarios → Internet → Load Balancer → Servidores)
- **Consejo de entrevista** (ej. "menciona AWS ELB, Nginx o HAProxy")

### 🔗 Aplicación al lab

| Elemento | ¿Aprovechable? | Cómo |
|---|---|---|
| **Formato por patrón** (por qué/cómo/tabla/casos/beneficios) | ✅ **SÍ — es el mismo formato WHEN/TEMPLATE/PITFALLS** que ya anotamos para los KOs del lab | Refuerza la plantilla KO propuesta |
| **Consejo de entrevista** | 🟡 Para Joseba (máster/meta empleo) | Patrón de entrevistas de system design |
| **Diagramas caja-flecha** | ✅ **SÍ — el lab ya puede hacerlos** (HTML/CSS/SVG → PNG) | Ver Parte 2 |
| **Los 15 patrones como conocimiento** | 🟡 Conocimiento general de system design — relevante para SkillBridge/master, no para el stack actual | Referencia |
| **Patrón "Cheat Sheet" final** | ✅ Idea para el lab | Un resumen visual de los KOs |

**Veredicto contenido:** el formato de infografía es lo más valioso (refuerza el
formato KO del lab), no los patrones en sí (conocimiento estándar de system design).

---

## PARTE 2 — ¿Cómo se hace este tipo de infografía con el lab?

### ✅ Lo que el lab YA tiene (verificado 04-ago: infografía L2)

| Capacidad | Estado | Evidencia |
|---|---|---|
| **HTML/CSS/SVG** | ✅ | research/infografias/l2-loop-engineering.html |
| **Chrome headless → PNG** | ✅ | `google-chrome --headless --screenshot=... --window-size=1200,900` |
| **Verificación visual con GLM** | ✅ | GLM 4.6V lee el PNG y confirma legibilidad |
| **Skill infografia-html** | 🟡 Ofrecida, sin confirmar | Puede estandarizarse |

### 📐 El flujo para replicar este formato

```
1. Datos del patrón (YAML/MD del lab — ej. KO con WHEN/TEMPLATE/PITFALLS)
        ↓
2. Plantilla HTML (por qué/cómo/tabla/casos/beneficios — secciones fijas)
        ↓
3. CSS/SVG: cajas + flechas + iconos (diagrama de flujo del patrón)
        ↓
4. Chrome headless → PNG (1200×900 o 1080×1350 estilo IG)
        ↓
5. Verificación visual con GLM (¿legible? ¿sin cortes?)
        ↓
6. Publicar/guardar (RAG, informe, Telegram)
```

### ⚠️ Lo que FALTARÍA para igualar la calidad

| Carencia | Solución | Esfuerzo |
|---|---|---|
| **Iconos profesionales** | Iconos SVG inline (feather/lucide) o emojis — el lab ya usa emojis | Bajo |
| **Paleta de color consistente** | CSS variables + plantilla única (dark/light) | Bajo |
| **Tipografía estilo "póster"** | Google Fonts (Inter/Space Grotesk) en el HTML | Bajo |
| **Tablas comparativas** | HTML table + CSS (ya viable) | Bajo |
| **Diagramas caja-flecha automáticos** | SVG manual por patrón (el lab los hace a mano) | Medio |
| **Automatización desde datos** | Script que genere el HTML desde el YAML del KO | Medio — el siguiente paso |
| **Estilo "manuscrito/póster" de IG** | Simplemente no es el estilo del lab — el lab haría estilo técnico limpio | N/A (elección) |

### 🎯 Conclusión sobre replicabilidad

**El lab puede hacer este tipo de infografía HOY** — la capacidad está validada
(HTML/CSS/SVG → Chrome headless → PNG → verificación GLM). Lo que falta es:

1. **Estandarizar la plantilla** (secciones fijas: por qué/cómo/tabla/casos/beneficios)
2. **Crear la skill `infografia-html`** como procedimiento reutilizable
3. **Opcional: script que genere el HTML desde el YAML de un KO**

**La diferencia real con estas infografías de IG:** ellos usan diseño manual
cuidado (iconos, paleta, póster). El lab produce infografías **técnicas limpias**
más que "virales de Instagram" — que es lo que corresponde al contexto del lab.

---

## Resumen

- **Contenido:** formato de infografía por patrón (por qué/cómo/tabla/casos/beneficios)
  = refuerza el formato KO del lab. Los 15 patrones en sí = referencia de system design.
- **Replicabilidad:** el lab PUEDE hacer esto (capacidad validada 04-ago). Falta:
  plantilla estándar + skill infografia-html + (opcional) generación desde YAML.
