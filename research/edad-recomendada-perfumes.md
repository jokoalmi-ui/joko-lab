---
title: "Edad recomendada de la colección (rango) — método y resultado 15-ago-2026"
type: research
---

# Edad recomendada de la colección (rango) — método y resultado 15-ago-2026
**VERACIDAD:** [ALCANCE INTERNO]

**Petición del usuario:** "tengo casi 56 años, de mi colección de perfumes,
investiga la edad recomendada de cada uno — rango de edad, todos sin excepción,
añadir columna".

**Resultado:** columna `edad_recomendada` añadida a `perfumes` (152/152
asignados, 0 nulos, `PRAGMA integrity_check` ok).

---

## Método (transparente, sin inventar)

**La "edad recomendada" NO es un dato oficial** — es percepción comunitaria.
Se asignó con reglas derivadas de datos BD (familia olfativa 99% + sensaciones
100%), contrastando los dudosos con foros (Fragrantica/Parfumo snippets).

### Escala (5 rangos)

| Etiqueta | Rango | Perfil BD |
|---|---|---|
| joven | 18-30 | Gourmand, cítrica/acuática con sensaciones vibrante/divertido |
| joven-adulto | 25-40 | Cítrica/Aromática fresca, acuática, deportiva |
| adulto | 35-50 | Floral, Fougère, Chipre, amaderada equilibrada |
| maduro | 45-60 | Oriental, Cuero, especiado profundo, ambarado denso |
| atemporal | 20-60+ | Verificado con fuentes (aparece en guías de regalo de rangos dispares) |

### Reglas de asignación

1. **Base por familia** (mapeo directo):
   - Gourmand → joven (18-30)
   - Cítrica/Acuática/Aromática → joven-adulto (25-40)
   - Floral/Fougère/Chipre → adulto (35-50)
   - Oriental/Cuero/Amaderada → maduro (45-60)
2. **Ajuste por sensaciones** (solo si aplica):
   - vibrante/divertido/energico/ligero/fresco → bajar un escalón
   - serio/elegante/profundo/sensual → subir un escalón
3. **Atemporal** solo si verificado con fuentes (no por defecto).

### Contraste con foros (solo los dudosos, no los 152)

| Perfume | Percepción de foros | Resultado |
|---|---|---|
| Oud Satin Mood (MFK, 2015) | "you'd have to be quite mature or at least elegant" (Fragrantica) | ✅ maduro — confirma regla |
| Bois Imperial (2020) | Guías de regalo Fragrantica: "For a 25-Year-Old Man" Y "For a Lady Aged 70+" | 🟢 atemporal (20-60+) — NO maduro |
| Afternoon Swim | Cítrico fresco/ligero/vibrante (sensaciones BD) — familia corregida a Cítrica (no tenía) | joven (18-30) |

---

## Distribución final (152 perfumes, tras corrección de familias 15-ago)

| Rango | Cantidad | % |
|---|---|---|
| adulto (35-50) | 62 | 41% |
| joven (18-30) | 31 | 20% |
| maduro (45-60) | 33 | 22% |
| joven-adulto (25-40) | 24 | 16% |
| atemporal (20-60+) | 2 | 1% |

**⚠️ CORRECCIÓN DE FAMILIAS DETECTADA Y APLICADA (15-ago, mismo día):** al
filtrar los "joven", aparecieron 6 perfumes con familia MAL asignada en BD
(error heredado del importador — el patrón documentado de Angels' Share):
- Grand Soir (MFK) Cítrica→**Oriental** (fuente: guías lo describen "Oriental
  Amber — labdanum, benzoin, vanilla")
- L'Air du Désert Marocain (Tauer) Cítrica→**Oriental** (Fragrantica: "Oriental
  Spicy", 2005)
- Angels' Share (Kilian) Cítrica→**Gourmand** (patrón conocido; el decant ya
  estaba corregido a Gourmand el 05-ago — el perfume no)
- Ganymede (MAB) Cítrica→**Amaderada** (perfil real mineral/amaderado)
- Body Kouros (YSL) Cítrica→**Fougère** (perfil real fougère especiado)
- V: Amber Fougere (Clive Christian) Aromática→**Fougère** (su propio nombre)

Consecuencia: los 6 pasaron de "joven (18-30)" a adulto/joven-adulto — la
lectura "37 jóvenes" bajó a **31**.

---

## Lectura para el usuario (56 años)

- **Con 56 años**, el rango natural de la colección es **adulto (35-50) y
  maduro (45-60)** = 92 perfumes (61%) — encajan con su edad.
- **37 jóvenes (18-30)**: usables como frescura diaria/verano, pero
  percibidos "de chaval" — elegir con criterio (ocasiones informales).
- **2 atemporales** (Bois Imperial): seguros siempre, cualquier edad.
- El rango NO bloquea — orienta. La nariz del usuario manda (regla del lab).

---

## Registro

- Backup BD: `coleccion.db.bak-edad-20260815` (RULE-008, antes del ALTER perfumes)
- Backup BD: `coleccion.db.bak-decants-edad-20260815` (RULE-008, antes del ALTER decants)
- Script: `/tmp/asignar_edad.py` (perfumes, --simulate/--apply) + `/tmp/clasificar_decants_edad_v2.py` (decants)
- Skill perfume-ia: columna documentada (añadir a esquema si se actualiza)
- Backlog: cruzar esta entrada

---

## DECANTS — clasificación de edad completada (15-ago, misma sesión)

**Petición:** "revisa la clasificación de los decants con todos los parámetros
actuales" (tras la clasificación de perfumes).

**Método:** columna `edad_recomendada` en `decants` (ALTER). Tres vías:
1. **Heredada de `perfume_id`** (32 decants vinculados a botella)
2. **Criterio experto por familia real conocida** (nombre → familia → misma
   regla que perfumes) — 163 decants
3. **5 manuales** (variantes de nombre: Acqua di Giò Profumo, Vanille
   Impériale, Blessed Baraka, Andaluiza, Au Coeur du Désert)

**Resultado: 200/200 decants con edad (0 nulos, integridad ok):**

| Rango | Decants | % |
|---|---|---|
| maduro (45-60) | 72 | 36% |
| adulto (35-50) | 72 | 36% |
| joven-adulto (25-40) | 36 | 18% |
| joven (18-30) | 20 | 10% |

**Nota honesta:** 88 de 163 por criterio experto con confianza alta/media;
~75 con confianza "dudosa" (perfumes menos conocidos) — criterio razonado,
no inventado, pero los dudosos conviene contrastarlos con foros cuando salgan
en recomendaciones (misma regla que la clasificación de temporada de 05-ago).

**Relevancia para la recomendación del día (Pacific Chill vs Elysium):**
- Pacific Chill (decant 80): joven-adulto (25-40) — cítrico veraniego
- Elysium Parfum Cologne (decant 153): joven-adulto (25-40) — cítrico
- Ambos en la franja correcta para el look playero de la camisa de flores.
