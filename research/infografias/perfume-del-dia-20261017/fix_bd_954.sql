-- Correcciones BD 954 (Encre Noire) · 2026-10-17 · backup: coleccion.db.BACKUP.20261017_ficha
UPDATE perfumes SET concentracion='EDT', updated_at=datetime('now')
 WHERE id=954 AND concentracion='EDP';

INSERT INTO notas (nombre, tipo) SELECT 'Acetato de vetiverilo','salida'
 WHERE NOT EXISTS (SELECT 1 FROM notas WHERE nombre='Acetato de vetiverilo');
INSERT INTO notas (nombre, tipo) SELECT 'Vetiver de Haití','corazon'
 WHERE NOT EXISTS (SELECT 1 FROM notas WHERE nombre='Vetiver de Haití');
INSERT INTO notas (nombre, tipo) SELECT 'Vetiver de Bourbon','corazon'
 WHERE NOT EXISTS (SELECT 1 FROM notas WHERE nombre='Vetiver de Bourbon');
INSERT INTO notas (nombre, tipo) SELECT 'Madera de cachemira','fondo'
 WHERE NOT EXISTS (SELECT 1 FROM notas WHERE nombre='Madera de cachemira');

INSERT INTO perfume_notas (perfume_id, nota_id, intensidad)
SELECT 954, n.id, 3 FROM notas n
 WHERE n.nombre IN ('Ciprés','Acetato de vetiverilo','Vetiver de Haití','Vetiver de Bourbon','Madera de cachemira','Almizcle')
   AND NOT EXISTS (SELECT 1 FROM perfume_notas pn WHERE pn.perfume_id=954 AND pn.nota_id=n.id);

UPDATE uso_diario
   SET nota_personal = replace(nota_personal,
       'BD corregida: concentracion EDP->EDT y notas placeholder->piramide oficial (backup previo)',
       'BD id 954 corregida: concentracion EDP->EDT y 5 notas de la piramide oficial anadidas (habia 3, dos de ellas no oficiales) · backup coleccion.db.BACKUP.20261017_ficha')
 WHERE fecha='2026-10-17' AND perfume_id=954;
