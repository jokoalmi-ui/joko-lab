INSERT INTO uso_diario (perfume_id, fecha, clima_temp, clima_desc, animo, ocasion, nota_personal, created_at)
VALUES (1032, '2026-11-16', 15.6,
        'ventana 08-18: 14,3-16,9 C sens, media 15,6; dia 12,9-20,2 C; lluvia 13%',
        'otro', 'diario',
        'ficha del día (víspera, entrega 15-11 10:00) · pronóstico open-meteo 15-11 11:35 UTC+2 · Tuttle Tiziana Terenzi, templado 15,6 C banda estrecha, 3 sprays · fondo klein variante _d70 (cuerpo 2,56:1 tapón 2,92:1 fondo L 139,1) · [VAL: sin respuesta aun | ventana 08-18]',
        datetime('now'));
SELECT id, perfume_id, fecha, clima_temp, substr(nota_personal,1,80) FROM uso_diario WHERE fecha='2026-11-16';
