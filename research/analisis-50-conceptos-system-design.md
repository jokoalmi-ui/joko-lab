---
title: "Análisis — Guía 50 Conceptos de System Design (Code Era)"
type: research
---

# Análisis — Guía 50 Conceptos de System Design (Code Era)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://www.instagram.com/p/DbA_4TqliX0/ — codeera.tech (Code Era)
**Método:** Descarga carrusel (8 slides CDN) + análisis GLM 4.6V local
**Imágenes:** /tmp/codeera/slide_01..08.jpg

---

## Qué es

**Infografía educativa: los 50 conceptos clave de System Design** — organizada
como lista numerada (1-50) con definiciones, diagramas y "Why important?" en
cada concepto. Estilo: guía de entrevistas de system design.

## Estructura por slides (según GLM)

| Slides | Contenido |
|---|---|
| 1 | Conceptos 1-10: qué es SD, escalado v/h, load balancer, requisitos funcionales/no funcionales, monolito vs microservicios, tolerancia a fallos |
| 2 | Conceptos 11-19: SQL vs NoSQL, índices (B-tree), replicación maestro-esclavo, sharding, ACID/BASE, teorema CAP, consistencia eventual |
| 3 | Performance/caching: caché, cache aside, write through/back, CDN, rate limiting (leaky bucket), colas, Kafka vs RabbitMQ, idempotencia |
| 4 | Sistemas distribuidos 31-39: consistent hashing, liderazgo, lock, retry, saga, long polling vs WebSockets |
| 5 | Problemas de diseño 41-49: URL shortener, API gateway, etc. con diagramas de flujo |
| 6 | Patrones avanzados: Gossip, relojes vectoriales, contadores distribuidos, clave idempotente |
| 7 | Sharding, cache invalidation, CDN edge, replicación lag |
| 8 | Conceptos 20-23: failover, quorum, persistencia poliglota, CDC |

## 🔗 Aplicación al LAB

| Concepto | Conexión al lab |
|---|---|
| **Observabilidad/monitoring** (implícito) | Coherente con F4 telemetría |
| **Rate limiting / idempotencia** | Patrones aplicables a los cron del lab (evitar duplicados) |
| **CAP / consistencia eventual** | El file bus multi-sesión = consistencia eventual (sin locks fuertes) |
| **Saga pattern** | Patrón para pipelines multi-paso del lab |
| **Cache aside / write through** | El lab usa caché de embeddings (reranker CPU) — patrón cache aside |
| **Formato "Why important?"** | Mismo patrón WHEN de los KOs del lab |
| **Los 50 conceptos** | Material de referencia para entrevistas (máster/empleo) |

## Veredicto

**Guía de referencia** de system design bien hecha (50 conceptos con diagramas).
Para el lab: refuerza patrones ya usados (cache aside, consistencia eventual del
file bus) y el formato "Why important?" (idéntico a los KOs). Los 50 conceptos
son material de estudio para entrevistas, no conocimiento nuevo para el stack.

**Nota:** el alt de la imagen decía "planta de edificio, calendario" — engañoso;
el contenido real es la guía de system design (lección aprendida de nuevo: no
fiarse del alt).
