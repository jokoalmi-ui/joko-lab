---
title: "Análisis — codedsoul_05: System Design (22-ago-2026)"
type: research
---

# Análisis — codedsoul_05: System Design (22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/codedsoul_05/ (5 posts analizados 22-ago)
**Método:** captions extraídos con browser (solo lectura, sin aplicar cambios)

## Resumen de los 5 posts

### ⭐ VALOR ALTO 1: "BookMyShow Coldplay — race condition" (20-ago)
**Problema**: 2M usuarios quieren 5K asientos; dos usuarios ven "A1 libre" a la vez y ambos pagan → double booking (race condition).
**Solución real (BookMyShow)**:
1. **Queue** a las 12:00 — no dejar 2M golpear la DB a la vez; cola tipo teatro ("tu número es 2.345, espera 2 min"), solo 10K dentro del booking hall
2. **Redis lock** al hacer clic: `SET seat_A1 your_id NX EX 300` — lockea el asiento 5 min solo si nadie más lo tiene; si falla → rojo
3. **Pago**: éxito → DB BOOKED para siempre; fallo/timeout → lock liberado
4. **Seguridad en DB**: `UNIQUE(show_id, seat_id)` — la DB misma impide doble reserva

**Lección**: Junior = check-then-book (double booking). Senior = lock-then-book + queue.
**Para el lab**: patrón de concurrencia correcto; aplicable si EXP-002 (bolsa) o crons concurrentes comparten recursos. Sin acción hoy.

### ⭐ VALOR ALTO 2: "WhatsApp Stories sin cron — lazy delete" (20-ago)
**Problema**: borrar stories caducadas con cron (`DELETE WHERE expires_at < NOW()`) con 50B filas → lockea la DB y muere.
**Solución real (Instagram/WhatsApp)**:
1. **EXPIRY ON READ (lazy delete)**: no borrar, ocultar — `SELECT ... WHERE expires_at > NOW()`; si caducó, la query no devuelve nada. Cero jobs. + partial index `WHERE expires_at > NOW()`
2. **TTL en storage (write side)**: Cassandra/Dynamo/Scylla TTL nativo (86400s) · S3 lifecycle rule · Redis `EXPIRE 86400`
3. **Limpieza de disco sin cron**: tablas time-partitioned (`stories_2026_08_20`) + `DROP TABLE` (DROP es instantáneo, DELETE es lento) · compaction de Cassandra
4. **Por qué NO cron**: DELETE 500M filas = txn larga, locks, replica lag, WAL bloat, OOM

**Regla**: no borres para expirar — haz lo caducado invisible en lectura y deja que el storage TTL limpie en escritura.
**Para el lab**: conexión con el RAG/indexer (LanceDB crece; fragmentos obsoletos podrían necesitar patrón lazy en vez de limpieza cron). **PENDIENTE débil — evaluar limpieza del RAG**.

### VALOR MEDIO: "C is foundation" (21-ago, 46 likes)
C no está viejo: Python/Java/JS usan C por dentro; OS/DB/smart devices en C; control de memoria (stack vs heap) + punteros. **Material LinkedIn** (memoria/VRAM análoga).

### VALOR MUY BAJO ×2: "Java Handwritten Notes" y "Computer Architecture Notes" (21-ago)
Engagement bait puro ("Comment JAVA/ARCH for notes"). Sin contenido técnico en caption.

## Conclusión
2 posts de VALOR ALTO (system design: concurrencia + lazy delete) → pendiente débil para el lab
(limpieza del RAG con patrón lazy). 3 posts descartables (bait). Ninguno aplicado al lab.
