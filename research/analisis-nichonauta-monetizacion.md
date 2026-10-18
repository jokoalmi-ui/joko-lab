---
title: "Análisis — Nichonauta: vídeos de MONETIZACIÓN (20-ago-2026)"
type: research
---

# Análisis — Nichonauta: vídeos de MONETIZACIÓN (20-ago-2026)

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** canal Nichonauta (YouTube) — 3 vídeos de monetización revisados
**Método:** transcripciones VTT en español descargadas y verificadas
**Veracidad:** [VERIFICADO] — contenido de las transcripciones reales

---

## 1. "Crear una Web con IA — Cómo Monetizar con Google AdSense" (sZcqEGhxSh0)
**Invitado: Juan Baladés** (no Nichonauta) — 386K chars

### Contenido
- Flujo completo para monetizar una web con AdSense: crear web con IA →
  tráfico → revisión de AdSense → aprobación → umbral de pago → verificación
  bancaria → cobros mensuales (día 21)
- Umbral de pago: ~1,200 MXN (~$60) en México (antes ~$100)
- Énfasis: no basta aprobar el sitio; hay que llegar al umbral mínimo
- Web con IA + AdSense como fuente de ingresos pasiva

### Aplicabilidad al LAB
| Criterio | Valor |
|---|---|
| Necesidad real | 🔴 BAJA — el lab no tiene web pública ni producto que monetizar |
| Coste | Bajo (dominio + hosting) |
| Encaje local-first | 🟡 Parcial (la web sería pública/cloud) |
| Señal | **El futurible "embudo/landing" ya anotado** — este vídeo lo alimenta |
| Timing | ⚠️ Requiere tráfico — sin producto ni audiencia, no es accionable |

**Veredicto**: NO aplicable hoy. Es un modelo de ingresos por publicidad que
requiere tráfico web sostenido — el plan de ingresos del lab va por LinkedIn
(marca de empleo) y producto, no por AdSense. Queda como referencia para el
futurible "embudo/landing" (cuando haya producto, AdSense es una opción más,
no la principal).

## 2. "FREE Domain — Best Options 2026" (gC8siCVqh8I) — 16K chars

### Contenido
- dot.tk (dominios .tk gratis) YA NO funciona; Freenom tampoco
- Recomendación: empezar con **subdominios gratuitos** o comprar un .com
  (~$10/año)
- Nada de "dominio gratis completo" fiable en 2026

### Aplicabilidad al LAB
- El lab NO expone servicios al exterior (todo localhost, verificado 17-ago)
- La señal del futurible NGINX/Caddy es "exponer servicios" — este vídeo
  confirma que un dominio gratis no es la vía; un .com barato sí

**Veredicto**: NO aplicable hoy (misma señal que NGINX: exponer servicios).
Dato útil: no perder tiempo con dominios gratis, ir directo a .com (~10 €/año)
cuando toque.

## 3. "FREE VPS and Hosting — Google Cloud sin pagar" (OAh9phGdmNo) — 36K chars

### Contenido
- Google Cloud: instancia **e2-micro gratis** (1 máquina no interrumpible/mes,
  regiones US) + $300 de créditos de prueba iniciales
- Alternativas mencionadas: Oracle, IBM, Azure, Amazon, Alibaba
- Requiere tarjeta; los recursos del nivel gratuito NO se cobran de los
  créditos de prueba

### Aplicabilidad al LAB
- El lab es **local-first**: los datos y modelos viven en casa (A2000,
  SSD, Ollama, LM Studio). Un VPS cloud gratis serviría solo para exponer
  algo público (landing, demo, servicio) sin coste
- e2-micro = 2 vCPU compartidas + 1 GB RAM → suficiente para una landing
  estática o un proxy ligero; NO para LLMs

**Veredicto**: NO aplicable hoy, pero es la pieza de infraestructura más
interesante de las 3 PARA EL FUTURO: si el lab hace una landing/embudo
(futurible), un e2-micro gratis de Google Cloud sirve sin coste. Ojo:
tarjeta obligatoria + región US + vigilar que no se cobren recursos fuera
del free tier.

---

## CONCLUSIÓN GLOBAL (honesta)

**Ninguno de los 3 es aplicable HOY.** El lab no tiene: producto web,
tráfico, ni necesidad de exponer servicios. Los 3 alimentan futuribles
YA anotados:

| Vídeo | Futurible que alimenta | Señal |
|---|---|---|
| AdSense | Embudo/landing propia | Producto del lab listo + audiencia |
| Dominio gratis | NGINX/Caddy / exposición | Exponer servicios (dato: .com ~10 €, no gratis) |
| VPS gratis | Embudo/landing | Landing creada → e2-micro de Google Cloud (0 €) |

**Nota positiva**: el canal Nichonauta SÍ tiene visión parecida a la del lab
(IA local, modelos pequeños, iteración) — pero sus vídeos de monetización
son de su contexto (web + AdSense), no del nuestro (local-first + LinkedIn).
La señal real para el lab sigue siendo: **primero producto, luego
distribución**.
