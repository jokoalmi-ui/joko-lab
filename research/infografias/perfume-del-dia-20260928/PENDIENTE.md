# PENDIENTE — ficha del día 28-09-2026 (Loewe 7 Plata)

## Hecho y verificado
- Investigación del día: Loewe 7 Plata (clima ventana 08-18: 21,7 / media 26,3 / 29,0 °C; 2 sprays).
- `perfume_del_dia_v5_7plata.html` (17/17 campos, FALTA 0, veredicto ENVIAR con 2 avisos).
- `7plata_figura.png`, `7plata_pack.png`, `qr_fragrantica.png`.
- Render de prueba: 1080x1350, dos pasadas con el mismo sha256, scrollHeight 1350, pie 1340.

## Falta (bloqueado por GPU colgada)
- `7plata_fondo.png` (SDXL) → render final `ficha_perfume_del_dia_20260928_7plata.png` → envío al canal.

## Cómo se retoma solo
- `continuar_ficha.sh` (esta carpeta) hace todo: espera la GPU, arranca comfyui, genera el fondo,
  para comfyui, renderiza, pasa la puerta y envía a telegram:-1003968087263.
- Lo lanza al arrancar el PC la unidad de usuario `ficha-7plata-postboot.service` (enabled).
- Registro: `post_reboot.log`. Si el envío sale bien, escribe `ficha_enviada.ok` (idempotente).
- Si falla, avisa por Telegram al DM con el motivo.
- Prueba en seco sin GPU ni envío: `FICHA_DRY=1 bash continuar_ficha.sh`.
- Para desactivar la unidad: `systemctl --user disable ficha-7plata-postboot.service`.

## Después de enviarla
- Insertar en `uso_diario` de `coleccion.db` (requiere OK del usuario).
- Girar la sección del foco: siguiente decisión pendiente = publicar L4 y anotar `fecha_publicacion`.
