INSERT INTO uso_diario (perfume_id, fecha, clima_temp, clima_desc, animo, ocasion, nota_personal, created_at)
VALUES (1003, '2026-10-30', 15.8, 'ventana 08-18: 11,5-18,5 C sens, media 15,8; dia 11,2-19,3 C; lluvia 0%', 'tranquilo', 'diario', '[VAL: sin respuesta aun | ventana 08-18] ficha del dia: Apex (Roja Parfums) — chipre verde; banda templado, amplitud media 8,4 C; dosis 3 sprays; puerta 17/17; vis tapon 2,80:1 cuerpo 4,05:1 fondo L 104,4', datetime('now'));
SELECT id, perfume_id, fecha, clima_temp, animo, ocasion, substr(nota_personal,1,70) FROM uso_diario WHERE fecha='2026-10-30';
