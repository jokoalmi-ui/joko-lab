"""Índice del pack: única fuente de verdad de qué piezas existen.
La portada se construye desde aquí y gen.py comprueba que no falte ni sobre ninguna."""

PIEZAS = [
    ("00_portada", 1527, "Portada e índice",
     "Qué se entrega, para quién y con qué cifras. La primera hoja del pack."),
    ("01_pagina_creadora", 1920, "Página de la creadora",
     "Su página con código, enlace con seguimiento, selección y condiciones de pago."),
    ("02_sistema_atribucion", 1350, "Sistema de atribución",
     "El circuito completo: cupón, enlace, pedido y comisión. Incluye lo que NO se puede medir."),
    ("03_anuncio_a", 1350, "Anuncio A · producto",
     "Gancho de producto, 4:5 para feed. Enseña el decant y el precio de entrada."),
    ("04_anuncio_b", 1350, "Anuncio B · selección",
     "Gancho de descubrimiento: las tres fragancias y para quién es cada una."),
    ("05_anuncio_c", 1350, "Anuncio C · prueba social",
     "Reseñas y valoración reales de la tienda. Para audiencias frías."),
    ("06_story_9x16", 1920, "Story 9:16",
     "Versión vertical con zonas seguras marcadas y sticker de código."),
    ("07_brief_campana", 1527, "Brief de campaña",
     "Objetivo, mensajes, qué no decir, calendario de 4 semanas y quién aprueba."),
    ("08_informe_mensual", 1920, "Informe mensual",
     "Pedidos por semana, productos y lectura de los datos. Lo que justifica renovar."),
    ("09_panel_seguimiento", 1350, "Panel de seguimiento",
     "Las tres creadoras, su comisión y el retorno. La tabla que se revisa cada mes."),
]
TOTAL = len(PIEZAS)
