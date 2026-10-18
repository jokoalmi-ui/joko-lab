---
title: "IFRA ↔ batches — qué batches valen más en la comunidad (18-ago-2026)"
type: research
---

# IFRA ↔ Batches: Qué batches valen más (18-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]
Parfum-Forum, batchcode.org, Trade Perfumes, Première Peau, scenthoarders)

## Contexto regulatorio (los hitos que crean "vintages")

| Hito | Fecha | Efecto |
|---|---|---|
| EU 2003 | 2003 | 26 alérgenos obligatorios en etiquetas |
| IFRA 40º Enmienda | 2006 | Restricciones cuantitativas al oakmoss |
| IFRA 43º Enmienda | 2008/09 | Restricciones SEVERAS a oakmoss/tree moss → "la industria cambió para siempre" |
| EU 2023/1545 | 2023 | 26 → 81 alérgenos |
| **Aplicación EU 2023/1545** | **productos nuevos: julio 2026 (¡YA!)** · stock existente: julio 2028 | **OLA DE REFORMULACIONES EN CURSO** |

## Cómo valora la comunidad

1. Decodifica batch → fecha (CheckFresh, CheckCosmetic, batchcode.org, Parfumo)
2. Compara con los hitos IFRA → identifica pre/post reformulación
3. Pre-reformulación cotiza premium en reventa (Trade Perfumes: "pre-reformulation
   bottles, verifiable through their batch codes, regularly command premiums")
4. Se siguen como vintages de vino (caso Thierry Mugler Angel — coleccionistas
   rastrean batch codes por época)

## Casos del lab (Argos y Kilian) — lo verificado HOY

### Triumph of Bacchus (Argos)
- **OJO: hay DOS fragancias** — EDP (lanzada 2019) y Extrait (lanzada 2020). La
  confusión red vs yellow juice mezcla ambas.
- Comunidad: el **batch antiguo es más armónico, afrutado y menos sintético**
  (Parfum-Forum, usuario con ambos: "Der alte Batch ist viel harmonischer,
  fruchtiger und weniger synthetisch... der neue ist eine Katastrophe")
- Usuario Fragrantica (30ml): "nueva versión reformulada (jugo amarillo) — la
  performance es muy débil, la han matado"
- Reddit (r/Fragrances): sospecha de que quitaron el tinte (dye) → reformulación,
  o "crear deseo de batches antiguos artificialmente"
- Argos responde oficialmente: "el color del EDP puede variar naturalmente de
  batch a batch — característica de ingredientes artesanales"
- **Conclusión: el batch ROJIZO (original, ~2019-2021) es el valorado; el
  AMARILLO (nuevo) es el débil.**

### Intoxicated (Kilian)
- Kilian tiene decodificador propio: batchcode.org/kilian/
- Estudio previo del lab (13-ago): "batches nuevos ya no tienen la longevidad
  del 2019" → batch 2019 = el valorado

## Estado de la BD perfume-ia (verificado 18-ago)

```sql
perfumes: lote TEXT, batch_code TEXT, idx_perfumes_batch (EXISTE pero VACÍO)
decants: tabla SEPARADA (200 registros) — NO pueden tener batch_code
```
- **⚠️ RESTRICCIÓN REAL (usuario, 18-ago): solo puede saber el batch de lo
  que tiene en BOTELLA física. Los DECANTS (200 en BD) no tienen batch.**
- Estructura de la BD: `perfumes` = 320 botellas (potencialmente con batch) ·
  `decants` = 200 (sin batch por diseño). La distinción ya está en la BD.
- **0 de 320 botellas tienen batch_code rellenado** — todo está por hacer.
- **Adonis Awakens (Argos, 2022)**: botella, sin lote ni batch_code
- **Fall of Phaeton (Argos, 2024)**: botella, sin lote ni batch_code
- **Triumph of Bacchus EDP (Argos, 2019)**: botella, sin lote ni batch_code ← el caso clave
- **Angels' Share (Kilian, 2020)**: botella, sin lote ni batch_code
- **Black Phantom (Kilian, 2017)**: botella, sin lote ni batch_code
- **Intoxicated (Kilian)**: NI SIQUIERA ESTÁ en la BD (es el caso sospechoso del estudio)

## Acción pendiente (requiere el usuario en físico — SOLO BOTELLAS)

1. Mirar las botellas físicas (código grabado/estampado en la base del frasco o en la caja)
2. Anotar batch_code SOLO de las que tiene en botella: Triumph of Bacchus EDP,
   Angels' Share, Black Phantom (y cualquier otra botella de la colección)
3. Añadir Intoxicated a la BD (si lo tiene en botella)
4. Decodificar cada código (batchcode.org / checkfresh / parfumo) → fecha
5. Comparar con hitos IFRA → etiquetar pre/post reformulación
6. **Los 200 decants quedan EXCLUIDOS por diseño** (no se puede saber su batch)

## Futurible vinculado (backlog 18-ago)
Tabla `hitos_ifra` + decodificador en perfume-ia → etiquetar cada botella
pre-2006 / pre-2008 / post-2026. Timing óptimo AHORA (EU 2023/1545 activa
desde julio 2026).
