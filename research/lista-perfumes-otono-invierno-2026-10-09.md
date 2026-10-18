# Botellas de otoño e invierno — lista para el cambio de caja

Generada: **viernes 09-10-2026 23:30 CEST** · Fuente: `~/perfume-ia/data/coleccion.db` (md5 `f1d21c8382e9893ef163f4bdee6ad408`), leída en solo lectura.

## Método (de dónde sale cada fila)
- Universo: perfumes con `posee` = botella o ambos (**botellas físicas**, no decants ni agotados).
- Temporada: columna `estaciones_norm` de la tabla derivada `rango_termico`, que normaliza el campo `temporada` de la BD (valores compuestos tipo «otoño-invierno» incluidos).
- Orden dentro de cada bloque: **índice térmico** de `rango_termico` (derivado de la columna `sensaciones`, −1 fresco … +1 cálido) de más invernal a menos.

## Límites declarados (leer antes de usar la lista)
1. **La temporada la declara la BD, no está validada.** `rango_termico` es un dato declarado: su propia cabecera mide `r = −0,062` sobre 72 usos con temperatura, es decir **no predice** a qué temperatura se usa un perfume. Vale como punto de partida, no como verdad.
2. **Solo 50 de las 139 tienen pirámide de notas** cargada (180 de 298 botellas en toda la BD). Donde no hay notas, la única fuente es la etiqueta declarada.
3. **40 discordancias**: perfumes declarados otoño/invierno con índice térmico negativo (perfil marcado como fresco). Listadas al final — son candidatas a revisar en la BD, no a descartar de la lista.

## Bloque A — Invierno declarado (91 botellas: 6 «invierno» + 85 «otoño,invierno»)

- **Cocoa Morado** — French Avenue (ix +0.70)
- **Vanille Impériale** — Houbigant (ix +0.70)
- **Halwa Kiss** — Ojar (EDP · ix +0.70)
- **Flaming Red** — Santi Burgas (ix +0.68)
- **Tobacco Honey** — Guerlain (ix +0.65)
- **Ambra Gadir** — Darkbeat (ix +0.62)
- **Journey Man** — Amouage (ix +0.62)
- **Dominus** — Memoize (ix +0.62)
- **Ambre Khandjar** — Une Nuit Nomade (ix +0.60)
- **Cacao²** — Maison Tahité (ix +0.60)
- **Encens Cuivre** — Ojar (EDP · ix +0.60)
- **Sugardaddy** — Fugazzi (ix +0.60)
- **Arabian Nights** — My Geisha (ix +0.57)
- **Cuir-Curcuma** — Affinessence (ix +0.57)
- **Interlude Man** — Amouage (Oriental · ix +0.57 · 10h · estela enorme)  · notas: Bergamota/salida,Sándalo/fondo,Pachulí/fondo,Ámbar/fondo,Oud/fondo,Incienso/fondo,Cuero/fondo,Orégano/salida,Pimienta/salida,Opopónaco/corazon,Ládano/
- **Versace pour Homme Oud Noir** — Versace (ix +0.57)
- **Al Bashiq** — Nabeel (ix +0.57)
- **Oud Rouge Intense** — Fragrance Du Bois (ix +0.56)
- **Musc Ravageur** — Editions de Parfums Frédéric Malle (EDP · ix +0.55)
- **Firma 1** — FIRMA (Oriental · ix +0.55 · 10h · estela enorme)  · notas: Jazmín/corazon,Vetiver/fondo,Manzana/salida,Cereza/salida,Miel/corazon
- **La couche du diable** — Serge Lutens (ix +0.54)
- **Infinity** — Montale (ix +0.53)
- **Patchouli** — Ajmal (ix +0.53)
- **Oud** — Javier Fernández (ix +0.52)
- **Oud** — My Geisha (EDP · ix +0.52)
- **Oud Al'Andalus** — Darkbeat (ix +0.52)
- **Dark Note** — Darkbeat (ix +0.50)
- **Kismet Magic** — Maison Alhambra (EDP · Floral · ix +0.50 · 7h · estela moderada)  · notas: Rosa/corazon,Vainilla/fondo,Almizcle/fondo,Frambuesa/corazon
- **Oud Satin Mood (Eau de Parfum)** — Maison Francis Kurkdjian (Oriental · ix +0.50 · 8h · estela intensa)  · notas: Rosa/corazon,Violeta/corazon,Vainilla/fondo,Cedro/fondo,Ámbar/fondo,Oud/fondo,Fresa/?,Benjuí/fondo,Caramelo/fondo
- **Le Gemme - Orom** — Bvlgari (EDP · Oriental · ix +0.49 · 12h · estela enorme)  · notas: Oud/fondo,Vainilla Bourbon/salida,Benjuí de Siam/corazon
- **Ruby N Vanilla Oud** — EBK (ix +0.48)
- **Singular Oud** — Urban Scents (ix +0.47)
- **Oud de Burgas** — Santi Burgas (ix +0.46)
- **L'Myrrhe** — Darkbeat (ix +0.45)
- **2. Nawab of Oudh Intensivo** — Ormonde Jayne (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Alhambra Oud** — Ramón Monegal (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Carved Oud (Extrait de Parfum)** — Thameen (EDP · Amaderada · ix +0.42 · 7h · estela moderada · usos 6 (ult. 2026-07-17))  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Oud Aquilaria** — Omanluxury (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Oud Wood (Eau de Parfum)** — Tom Ford (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Oud for Greatness (Eau de Parfum)** — Initio (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Shaghaf Oud Royale** — Swiss Arabian (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **Woud & Mood Absolute** — Unique'e Luxury (EDP · Amaderada · ix +0.42 · 7h · estela moderada)  · notas: Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo
- **4. Montabaco Intensivo** — Ormonde Jayne (EDP · Cuero · ix +0.42 · 7h · estela moderada)  · notas: Cedro/fondo,Pachulí/fondo,Cuero/fondo,Tabaco/fondo
- **Bogoss Vibrant Leather** — Zara (EDP · Cuero · ix +0.42 · 7h · estela moderada · usos 4 (ult. 2026-07-19))  · notas: Cedro/fondo,Pachulí/fondo,Cuero/fondo,Tabaco/fondo
- **Tabaco Blanco** — The Lab (EDP · Cuero · ix +0.42 · 7h · estela moderada)  · notas: Cedro/fondo,Pachulí/fondo,Cuero/fondo,Tabaco/fondo
- **Amber Chocolat** — The Lab (EDP · Oriental · ix +0.39 · 7h · estela moderada)  · notas: Vainilla/fondo,Ámbar/fondo,Incienso/fondo,Almizcle/fondo
- **Clandestine Rendez-vous** — Les Sœurs de Noé (ix +0.38)
- **Majnoon** — Azman (ix +0.35)
- **Divine Vanille** — Essential Parfums (EDP · Gourmand · ix +0.34 · 8h · estela moderada)  · notas: Canela/corazon,Incienso/fondo,Pimienta Negra/salida,Salvia/corazon
- **Promise / ??????? (Parfum)** — Editions de Parfums Frédéric Malle (Parfum · Oriental · ix +0.28 · 14h · estela enorme)  · notas: Pimienta rosa/salida,Romero/salida,Manzana/salida,Clavo/corazon,Azafrán/salida
- **Opus XIV - Royal Tobacco** — Amouage (EDP · Oriental · ix +0.25 · 14h · estela enorme)  · notas: Pimienta rosa/salida,Canela/corazon,Sándalo/fondo,Pachulí/fondo,Ámbar/fondo,Oud/fondo,Tabaco/fondo,Labdanum/corazon,Olíbano/corazon,Tabaco Rubio/fondo
- **Triumph of Bacchus (Eau de Parfum)** — Argos (EDP · Oriental · ix +0.24 · 10h · estela intensa)  · notas: Pimienta rosa/salida,Jazmín/corazon,Vainilla/fondo,Sándalo/fondo,Pachulí/fondo,Ámbar/fondo,Almizcle/fondo,Tabaco/fondo,Vetiver/fondo,Haba Tonka/fondo,
- **Dior Homme (2005)** — Dior (EDT · Floral · ix +0.21 · 8h · estela moderada · usos 3 (ult. 2026-07-20))  · notas: Bergamota/salida,Lavanda/salida,Iris/corazon,Pachulí/fondo,Ámbar/fondo,Cuero/fondo,Cardamomo/salida,Salvia/corazon,Cacao/corazon,Vetiver Tahití/fondo
- **Ambre Tabac (Eau de Parfum)** — Daniel Josier (EDP · Oriental · ix +0.19 · 10h · estela intensa)  · notas: Bergamota/salida,Incienso/fondo
- **Boss Bottled Elixir** — Hugo Boss (EDP · Oriental · ix +0.16 · 10h · estela intensa)  · notas: Cedro/fondo,Pachulí/fondo,Incienso/fondo,Vetiver/fondo,Cardamomo/salida,Labdanum/corazon
- **Jubilation XXV Man** — Amouage (EDP · Oriental · ix +0.15 · 12h · estela enorme)  · notas: Naranja/salida,Canela/corazon,Cedro/fondo,Pachulí/fondo,Ámbar/fondo,Oud/fondo,Romero/salida,Labdanum/corazon,Laurel/salida,Zarzamora/salida,Davana/sal
- **Lavish** — Boadicea the Victorious (EDP · Oriental · ix +0.15 · 9h · estela intensa · usos 1 (ult. 2026-08-04))  · notas: Bergamota/salida,Limón/salida,Naranja/salida,Rosa/corazon,Cedro/fondo,Almizcle/fondo,Nuez Moscada/corazon
- **Tabac Nomade** — Houbigant (EDP · Cuero · ix +0.14 · 10h · estela intensa)  · notas: Bergamota/salida,Pimienta rosa/salida,Rosa/corazon,Vainilla/fondo,Cuero/fondo,Tabaco/fondo,Haba Tonka/fondo,Azafrán/salida
- **X for Men** — Clive Christian (EDP · Oriental · ix +0.14 · 10h · estela intensa)  · notas: Bergamota/salida,Jazmín/corazon,Iris/corazon,Canela/corazon,Vainilla/fondo,Cedro/fondo,Ámbar/fondo,Vetiver/fondo,Labdanum/corazon,Styrax/fondo,Ruibarb
- **Oud Or** — Houbigant (EDP · Oriental · ix +0.12 · 11h · estela intensa)  · notas: Rosa/corazon,Geranio/corazon,Vainilla/fondo,Cedro/fondo,Pachulí/fondo,Oud/fondo,Frambuesa/corazon,Cashmere Wood/fondo,Labdanum/corazon,Azafrán/salida,
- **Fall of Phaeton** — Argos (EDP · Cuero · ix +0.10 · 11h · estela enorme)  · notas: Bergamota/salida,Limón/salida,Lavanda/salida,Pimienta rosa/salida,Vainilla/fondo,Oud/fondo,Cuero/fondo,Almizcle/fondo,Cardamomo/salida,Jengibre/salida
- **Bois Mystique (Eau de Parfum)** — Houbigant (EDP · Amaderada · ix +0.06 · 9h · estela moderada · usos 1 (ult. 2026-09-08))  · notas: Bergamota/salida,Incienso/fondo,Jengibre/salida,Davana/salida,Papiro/corazon
- **Winter Palace** — Memo Paris (EDP · Cuero · ix +0.06 · 7h · estela moderada)  · notas: Vainilla/fondo,Labdanum/corazon,Benzoin/fondo,Bergamot/salida,Mate/corazon,Lemon/salida,Clove/salida,Red Tea/corazon,Orange Blossom/corazon
- **Le Gemme - Kobraa** — Bvlgari (EDP · Oriental · ix +0.05 · 10h · estela intensa)  · notas: Geranio/corazon,Oud/fondo,Cuero/fondo,Almizcle/fondo,Olíbano/corazon,Azafrán/salida
- **Alexandria II (Parfum)** — Xerjoff (EDP · Oriental · ix +0.04 · 7h · estela moderada · usos 1 (ult. 2026-09-13))  · notas: Lavanda/salida,Vainilla/fondo,Sándalo/fondo,Cedro/fondo,Ámbar/fondo,Almizcle/fondo,Cinnamon/salida,Agarwood (Oud)/salida,Rose/corazon,Apple/corazon,Li
- **Bois Imperial** — Essential Parfums (EDP · Amaderada · ix +0.04 · 7h · estela moderada · usos 5 (ult. 2026-10-07))  · notas: Pachulí/fondo,Vetiver/fondo,Albahaca tailandesa/salida,Pimienta Timut/salida,Akigalawood/corazon,Ambroxan/fondo
- **Bois Impérial (Eau de Parfum)** — Essential Parfums (EDP · Amaderada · ix +0.04 · 7h · estela moderada)  · notas: Pachulí/fondo,Vetiver/fondo,Albahaca tailandesa/salida,Pimienta Timut/salida,Akigalawood/corazon,Ambroxan/fondo
- **Encre Noire (Eau de Toilette)** — Lalique (EDP · Amaderada · ix +0.04 · 7h · estela moderada)  · notas: Bergamota/salida,Cedro/fondo,Almizcle/fondo
- **Encre Noire Sport** — Lalique (EDP · Amaderada · ix +0.04 · 7h · estela moderada)  · notas: Bergamota/salida,Cedro/fondo,Almizcle/fondo
- **Encre Noire à L'Extrême** — Lalique (EDP · Amaderada · ix +0.04 · 7h · estela moderada)  · notas: Bergamota/salida,Cedro/fondo,Almizcle/fondo
- **L'Homme Intense** — Prada (EDP · Oriental · ix +0.04 · 7h · estela moderada)  · notas: Iris/corazon,Sándalo/fondo,Pachulí/fondo,Ámbar/fondo,Leather/corazon,Tonka Bean/fondo
- **Naxos** — Xerjoff (EDP · Oriental · ix +0.04 · 7h · estela moderada · usos 1 (ult. 2026-10-08))  · notas: Lavanda/salida,Vainilla/fondo,Cinnamon/salida,Jasmine Sambac/corazon,Bergamot/salida,Tonka Bean/fondo,Lemon/salida,Cashmeran/corazon,Honey/salida,Toba
- **Renaissance** — Xerjoff (EDP · Oriental · ix +0.04 · 7h · estela moderada)  · notas: Pachulí/fondo,Ámbar/fondo,Almizcle/fondo,Petitgrain/salida,Rose/corazon,Virginia Cedar/salida,Bergamot/salida,Mint/salida,Lily-of-the-Valley/corazon,A
- **Torino21** — Xerjoff (EDP · Oriental · ix +0.04 · 7h · estela moderada)  · notas: Lavanda/salida,Almizcle/fondo,Lemon/salida,Mint/salida,Jasmine/corazon,Black Currant/corazon,Thyme/salida,Rosemary/salida,Basil/corazon,Lemon Verbena/
- **By the Fireplace** — Maison Margiela (EDP · Amaderada · ix +0.03 · 7h · estela moderada)  · notas: Naranja/salida,Pimienta rosa/salida,Vainilla/fondo,Pachulí/fondo,Ámbar/fondo,Clavo/corazon,Castaña/fondo
- **Hammam** — Régalien (ix -0.03)
- **D600** — Carner (EDP · Amaderada · ix -0.07 · 8h · estela moderada · usos 1 (ult. 2026-09-23))  · notas: Bergamota/salida,Pomelo/salida,Jazmín/corazon,Iris/corazon,Vainilla/fondo,Cedro/fondo,Vetiver/fondo,Cardamomo/salida,Pimienta negra/salida
- **Nakht** — Thauy (ix -0.07)
- **B683 (Extrait de Parfum)** — Marc-Antoine Barrois (Parfum · Oriental · ix -0.10 · 8h · estela intensa · usos 1 (ult. 2026-09-09))  · notas: Violeta/corazon,Vainilla/fondo,Sándalo/fondo,Pachulí/fondo,Oud/fondo,Cuero/fondo,Pimienta Negra/salida,Manzana/salida,Azafrán/salida,Comino/salida
- **Terra** — Rayhaan (ix -0.25)
- **Sheikh** — My Geisha (EDP · ix -0.33)
- **Paramour** — Omanluxury (ix -0.38)
- **Antidote** — Régalien (ix -0.40)
- **Rehab** — My Geisha (EDP · ix -0.40)
- **Agape Special** — Thauy (ix -0.45)
- **Scoville** — Obvious (ix -0.47)
- **Lucius** — Fragrance Du Bois (ix -0.50)
- **Victrix** — Profumum Roma (ix -0.50)
- **Foreplay** — My Geisha (EDP · ix -0.55)
- **Nayssabour** — Loumari (ix -0.57)
- **Brun** — V Canto (ix -0.57)

## Bloque B — Otoño solo (48 botellas)

- **La Tacita de Café** — Day Three Fragrances (ix +0.70)
- **Fuego Futuro** — Thomas De Monaco (ix +0.66)
- **Battito d'Ali** — Profumum Roma (ix +0.62)
- **Hypnotizing Fire** — The Harmonist (EDP · ix +0.62)
- **Instant Crush** — Mancera (ix +0.62)
- **Sundowner** — Tauer Perfumes (ix +0.62)
- **Au Coeur du Désert** — Tauer Perfumes (ix +0.62)
- **Blamage** — Nasomatto (EDP · ix +0.62)
- **Star for Men** — Mauboussin (ix +0.62)
- **Spice Leather** — Darkbeat (ix +0.57)
- **Wood Whisper** — Ojar (EDP · ix +0.57)
- **Silky Woods Elixir** — Goldfield & Banks (ix +0.57)
- **Raw Gold** — Thomas De Monaco (EDP · ix +0.57)
- **French Lover / Bois d'Orage** — Editions de Parfums Frédéric Malle (ix +0.55)
- **Infusion Velours** — Ojar (EDP · ix +0.54)
- **Whisky Nobile** — Farmacia SS. Annunziata (ix +0.50)
- **Black Tie** — Celine (EDP · ix +0.44)
- **Raw Gold** — Thomas De Monaco (EDP · ix +0.36)
- **Green Leather** — Daniel Josier (EDP · Cuero · ix +0.33 · 9h · estela intensa)  · notas: Jazmín/corazon,Ámbar/fondo,Incienso/fondo,Cuero/fondo,Frambuesa/corazon,Tomillo/corazon,Azafrán/salida,Gamuza/fondo
- **Musk** — My Geisha (ix +0.28)
- **Quattro Pizzi** — Casamorati (EDP · Oriental · ix +0.21 · 9h · estela intensa)  · notas: Pimienta rosa/salida,Tabaco/fondo,Haba Tonka/fondo,Ron/corazon,Davana/salida,Cilantro/salida,Tuberosa/corazon,Coco/corazon,Henoo/fondo
- **CH Men Africa** — Carolina Herrera (EDT · Amaderada · ix +0.13 · 7h · estela moderada)  · notas: Mandarina/salida,Pimienta rosa/salida,Cedro/fondo,Cashmere Wood/fondo,Jengibre/salida,Café/fondo,Salvia Azul/corazon
- **Cannabis** — My Geisha (EDP · ix +0.12)
- **Crush On Me** — Unique'e Luxury (ix +0.03)
- **Cherry on Top** — Joterc (ix -0.05)
- **Epoque** — Botanicae Expressions (ix -0.05)
- **Octubre** — Bravanariz (ix -0.10)
- **Somnia 517** — Maison Noir (ix -0.12)
- **Ambre des Abysses** — Houbigant (EDP · Oriental · ix -0.13 · 9h · estela moderada)  · notas: Bergamota/salida,Menta/salida,Flor de Azahar/salida
- **Oud Rain Tropical Storm** — Renier Perfumes (ix -0.20)
- **Aquila Absolute** — Electimuss (ix -0.35)
- **Zen'gi** — Unique'e Luxury (ix -0.40)
- **Hangover Meditation** — Emil Élise (ix -0.42)
- **Vision** — Morph (ix -0.42)
- **Delox** — Tiziana Terenzi (EDP · ix -0.42)
- **Vicebomb** — Simone Andreoli (ix -0.45)
- **Goudh** — Fugazzi (ix -0.47)
- **Zek** — Necalli (ix -0.47)
- **Limited 71 - 2022 Edition** — Widian (ix -0.48)
- **Book** — Commodity (ix -0.50)
- **Highlands** — Botanicae Expressions (ix -0.50)
- **Tramonte** — Botanicae Expressions (ix -0.50)
- **Lira** — Casamorati (EDP · ix -0.53)
- **GoldFawn** — Perroy (ix -0.55)
- **Anniversary** — Farmacia SS. Annunziata (ix -0.60)
- **Otimo** — pernoire (ix -0.60)
- **London** — Widian (EDP · ix -0.68)
- **Valentino Uomo Born In Roma Coral Fantasy** — Valentino (ix -0.72)

## Bloque C — Mixtos con primavera (10 botellas, para entretiempo)

- **Town & Country** — Clive Christian (EDP · Aromática · ix +0.14 · 8h · estela moderada)  · notas: Bergamota/salida,Limón/salida,Sándalo/fondo,Cedro/fondo,Pachulí/fondo,Ámbar/fondo,Cardamomo/salida,Salvia/corazon,Olíbano/corazon,Baya de Enebro/salid
- **195 a.C.** — Agatho (EDP · Amaderada · ix +0.10 · 9h · estela intensa · usos 1 (ult. 2026-07-20))  · notas: Bergamota/salida,Limón/salida,Jazmín/corazon,Cedro/fondo,Pachulí/fondo,Incienso/fondo,Cuero/fondo,Cashmere Wood/fondo,Cardamomo/salida,Higo/corazon,Ho
- **Imperial** — Boadicea the Victorious (EDP · Amaderada · ix -0.06 · 10h · estela intensa)  · notas: Lavanda/salida,Rosa/corazon,Geranio/corazon,Palo de Rosa/salida,Abedul/salida,Angélica/salida,Fresia/corazon
- **Fauno** — Agatho (EDP · Aromática · ix -0.07 · 8h · estela moderada · usos 2 (ult. 2026-10-01))  · notas: Bergamota/salida,Naranja/salida,Iris/corazon,Cedro/fondo,Almizcle/fondo,Salvia/corazon,Manzana/salida,Tomillo/corazon
- **Etruscan Water** — Francesca Bianchi (Chipre · ix -0.23)  · notas: Neroli/corazon,Coco/corazon,Notas verdes/salida,Cítricos/salida
- **V: Amber Fougere** — Clive Christian (EDP · Fougère · ix -0.26 · 7h · estela moderada)  · notas: Bergamota/salida,Lavanda/salida,Pimienta rosa/salida,Cedro/fondo,Almizcle/fondo
- **Apex (Eau de Parfum)** — Roja Parfums (EDP · Chipre · ix -0.28 · 7h · estela moderada)  · notas: Pachulí/fondo,Leather/corazon,Mandarin/salida,Bergamot/salida,Orange/salida,Oakmoss/fondo,Lemon/salida,Pineapple/salida,Jasmine/corazon,Cypress/salida
- **Chypre Toscano** — Unique'e Luxury (EDP · Chipre · ix -0.28 · 7h · estela moderada)  · notas: Bergamota/salida,Cedro/fondo,Pachulí/fondo,Musgo de roble/fondo,Almizcle/fondo
- **Elysium pour Homme (Parfum)** — Roja Parfums (EDP · Chipre · ix -0.28 · 7h · estela moderada · usos 3 (ult. 2026-08-25))  · notas: Vainilla/fondo,Almizcle/fondo,Labdanum/corazon,Benzoin/fondo,Galbanum/fondo,Pink Pepper/salida,Rose/corazon,Leather/corazon,Apple/corazon,Lemon/salida
- **Fougère Royale (2010) (Eau de Parfum)** — Houbigant (EDP · Fougère · ix -0.31 · 8h · estela moderada · usos 2 (ult. 2026-09-19))  · notas: Bergamota/salida,Lavanda/salida,Manzanilla/salida

## Anexo 1 — Discordancias a revisar (40)

Declarado otoño/invierno, pero el índice térmico los deja del lado fresco. O la etiqueta de temporada o las `sensaciones` están mal en la BD.

- Valentino Uomo Born In Roma Coral Fantasy — Valentino · declarado: otoño · ix -0.72 · sensaciones: ["fresco", "citrico", "marino", "ligero"]
- London — Widian · declarado: otoño · ix -0.68 · sensaciones: ["fresco", "mineral", "marino", "ligero"]
- Anniversary — Farmacia SS. Annunziata · declarado: otoño · ix -0.60 · sensaciones: ["citrico", "fresco", "mineral"]
- Otimo — pernoire · declarado: otoño · ix -0.60 · sensaciones: ["fresco", "citrico", "mineral"]
- Brun — V Canto · declarado: otoño-invierno · ix -0.57 · sensaciones: ["fresco", "mineral", "citrico", "ligero"]
- Nayssabour — Loumari · declarado: otoño-invierno · ix -0.57 · sensaciones: ["citrico", "marino", "vibrante"]
- Foreplay — My Geisha · declarado: otoño-invierno · ix -0.55 · sensaciones: ["fresco", "citrico", "verde", "ligero"]
- GoldFawn — Perroy · declarado: otoño · ix -0.55 · sensaciones: ["fresco", "verde", "citrico", "ligero"]
- Lira — Casamorati · declarado: otoño · ix -0.53 · sensaciones: ["citrico", "fresco", "verde", "mineral"]
- Lucius — Fragrance Du Bois · declarado: otoño-invierno · ix -0.50 · sensaciones: ["fresco", "citrico", "mineral", "ligero", "brillante"]
- Victrix — Profumum Roma · declarado: otoño-invierno · ix -0.50 · sensaciones: ["citrico", "fresco", "brillante", "mineral", "ligero"]
- Book — Commodity · declarado: otoño · ix -0.50 · sensaciones: ["fresco", "citrico", "mineral", "brillante"]
- Highlands — Botanicae Expressions · declarado: otoño · ix -0.50 · sensaciones: ["fresco", "mineral", "verde", "ligero"]
- Tramonte — Botanicae Expressions · declarado: otoño · ix -0.50 · sensaciones: ["fresco", "mineral", "verde", "ligero"]
- Limited 71 - 2022 Edition — Widian · declarado: otoño · ix -0.48 · sensaciones: ["fresco", "mineral", "citrico", "ligero", "vibrante"]
- Scoville — Obvious · declarado: invierno · ix -0.47 · sensaciones: ["citrico", "fresco", "mineral", "vibrante"]
- Goudh — Fugazzi · declarado: otoño · ix -0.47 · sensaciones: ["fresco", "citrico", "verde", "brillante"]
- Zek — Necalli · declarado: otoño · ix -0.47 · sensaciones: ["citrico", "marino", "vibrante", "limpio"]
- Agape Special — Thauy · declarado: otoño-invierno · ix -0.45 · sensaciones: ["fresco", "verde", "ligero", "brillante"]
- Vicebomb — Simone Andreoli · declarado: otoño · ix -0.45 · sensaciones: ["fresco", "mineral", "vibrante", "ligero"]
- Vision — Morph · declarado: otoño · ix -0.42 · sensaciones: ["fresco", "verde", "mineral", "brillante"]
- Delox — Tiziana Terenzi · declarado: otoño · ix -0.42 · sensaciones: ["fresco", "verde", "brillante", "mineral"]
- Hangover Meditation — Emil Élise · declarado: otoño · ix -0.42 · sensaciones: ["citrico", "fresco", "mineral", "limpio", "vibrante"]
- Antidote — Régalien · declarado: otoño-invierno · ix -0.40 · sensaciones: ["fresco", "mineral", "vibrante", "ligero", "limpio"]
- Rehab — My Geisha · declarado: otoño-invierno · ix -0.40 · sensaciones: ["fresco", "mineral", "ligero", "vibrante", "limpio"]
- Zen'gi — Unique'e Luxury · declarado: otoño · ix -0.40 · sensaciones: ["fresco", "mineral", "ligero", "vibrante", "limpio"]
- Paramour — Omanluxury · declarado: otoño-invierno · ix -0.38 · sensaciones: ["fresco", "marino", "amaderado", "vibrante"]
- Aquila Absolute — Electimuss · declarado: otoño · ix -0.35 · sensaciones: ["citrico", "fresco", "mineral", "amaderado"]
- Sheikh — My Geisha · declarado: otoño-invierno · ix -0.33 · sensaciones: ["citrico", "marino", "amaderado", "vibrante"]
- Terra — Rayhaan · declarado: invierno · ix -0.25 · sensaciones: ["terroso", "mineral", "verde", "fresco"]
- Oud Rain Tropical Storm — Renier Perfumes · declarado: otoño · ix -0.20 · sensaciones: ["resinoso", "fresco", "mineral"]
- Ambre des Abysses — Houbigant · declarado: otoño · ix -0.13 · sensaciones: ["penetrante", "brillante", "calido", "mineral", "energico", "exotico", "citrico", "marino
- Somnia 517 — Maison Noir · declarado: otoño · ix -0.12 · sensaciones: ["fresco", "mineral", "amaderado", "envolvente"]
- B683 (Extrait de Parfum) — Marc-Antoine Barrois · declarado: otono,invierno · ix -0.10 · sensaciones: ["citrico", "floral", "dulce", "verde", "ambarado", "frutal", "marino"]
- Octubre — Bravanariz · declarado: otoño · ix -0.10 · sensaciones: ["citrico", "frutal", "amaderado", "vibrante"]
- D600 — Carner · declarado: otoño-invierno · ix -0.07 · sensaciones: ["amaderado", "mineral", "fresco", "especiado"]
- Nakht — Thauy · declarado: otoño-invierno · ix -0.07 · sensaciones: ["amaderado", "especiado", "mineral", "fresco"]
- Cherry on Top — Joterc · declarado: otoño · ix -0.05 · sensaciones: ["dulce", "brillante", "frutal", "ligero"]
- Epoque — Botanicae Expressions · declarado: otoño · ix -0.05 · sensaciones: ["fresco", "mineral", "amaderado", "dulce"]
- Hammam — Régalien · declarado: otoño-invierno · ix -0.03 · sensaciones: ["fresco", "mineral", "ahumado", "especiado"]

## Anexo 2 — Huecos de datos vistos de paso
- `familia_olfativa` vacía en 89 de las 139 filas; `longevidad_horas` y `estela` vacías en casi todas (solo las traen las fichas de los últimos meses).
- `estado_botella` está vacío en las 298 botellas (no permite apartar vacías).
- md5 de la BD en el momento de generar: `f1d21c8382e9893ef163f4bdee6ad408` (repetir la consulta con otra copia puede dar filas distintas).
