---
title: "Análisis reel AlgoInsight — 15 Design Patterns (11-ago-2026)"
type: research
---

# Análisis reel Instagram — AlgoInsight: 15 Design Patterns que debes saber
**VERACIDAD:** [VERIFICADO]

- Fecha: 2026-08-11
- Fuente: https://www.instagram.com/reel/Db3OnefhDlr/ (cuenta algoinsight, algoinsight.io)
- Tipo: reel animado (DSA & System Design)
- Método: descarga mp4 (CDN, firma completa) + ffmpeg frames + GLM 4.6V local (4 frames
  analizados: f_01, f_04, f_07, f_11) + caption completo verificado.
- Transcripción persistente: no aplica (reel sin texto descargable; contenido en research).
- Clasificación KAP: **Confirma** (nombres y trade-offs de patrones ya conocidos) +
  material accionable para documentar la arquitectura del lab (ai-architecture).

## OBS (contenido del reel)

Título: "Most engineers already use design patterns. They just don't know the
names — which means they can't search for the trade-offs."

LOS 15 PATRONES, clasificados (no alfabético — por rol):

CREATING (crear objetos)
1. Singleton — una instancia, compartida
2. Factory Method — crear sin nombrar la clase
3. Builder — ensamblar paso a paso

COMPOSING (componer objetos)
4. Adapter — puente entre interfaces incompatibles
5. Decorator — envolver para añadir comportamiento
6. Facade — una puerta a un subsistema
7. Proxy — ponerse delante y controlar el acceso
8. Composite — tratar hoja y árbol por igual

COORDINATING (coordinar comportamiento)
9. Observer — avisar a todos ante un cambio
10. Strategy — cambiar el algoritmo en runtime
11. Command — una petición como objeto
12. Iterator — recorrer sin exponer internals
13. State — comportarse según el estado actual
14. Template Method — esqueleto, la subclase rellena
15. Chain of Responsibility — pasar la petición hasta que alguien la maneja

TRES COSAS QUE VALE LA PENA SABER (el valor real del reel):
1. SINGLETON está en todas las listas y es el más peligroso: es estado mutable
   global disfrazado de clase. Los tests se vuelven dependientes del orden, las
   dependencias se esconden de los constructores, y es cuello de botella bajo
   concurrencia. La mayoría de usos quieren en realidad "una instancia
   gestionada por el contenedor" — inyección de dependencias con lifetime
   explícito y el objeto aún intercambiable en test.
2. STRATEGY y STATE son IDÉNTICOS en el diagrama de clases y significan lo
   contrario. Ambos delegan en un objeto intercambiable. La diferencia es quién
   decide: con Strategy el CALLER elige y las estrategias no se conocen entre
   sí; con State el OBJETO transiciona y los estados saben cuál viene después.
   "Si tus strategies eligen su propio sucesor, has escrito una máquina de
   estados."
3. DECORATOR, PROXY y ADAPTER todos envuelven un objeto — solo la INTENCIÓN los
   separa. Decorator AÑADE comportamiento (misma interfaz). Proxy CONTROLA el
   acceso (lazy load, cache, permisos, misma interfaz). Adapter CAMBIA la
   interfaz para que cosas incompatibles puedan hablar.

Frase final: "El punto no es usar más patrones. Es que 'necesitamos un Facade
aquí' termina una discusión que 'deberíamos envolver esto de alguna forma' no
puede." + "a pattern is a name for a shape you keep drawing" (confirmado por GLM
en todos los frames).

## HYP (mapeo al lab)

1. SINGLETON/estado global → revisar los scripts del lab (monitor Flask app.py,
   bolsa_scan.py, gateway) en busca de estado mutable global que haga tests
   order-dependent o esconda dependencias. El lab ya tiene skills de refactor
   seguro (refactor-seguro, simplify-code) — esta es una lente concreta para
   auditar.
2. STRATEGY vs STATE → el ai-router del lab (cloud-local routing) es un
   Strategy clásico: el CALLER elige modelo/proveedor por tarea. El pipeline de
   observabilidad (observabilidad-pipeline) es un Observer. Nombrarlos así en
   ai-architecture facilita buscar trade-offs (ej: si algún día el router
   encadena modelos que se eligen solos, sería State, no Strategy).
3. DECORATOR/PROXY/ADAPTER → el lab ya usa wrappers (ej: LM Studio como adapter
   de API OpenAI-compatible; monitor como proxy de telemetría). Nombrar la
   intención de cada wrapper evita "envolver esto de alguna forma".
4. TEMPLATE METHOD → el flujo OBS→HYP→DEC del lab (LPA) es un esqueleto con
   pasos fijos que cada experimento rellena — es un Template Method de facto.
   Documentarlo así en gobernanza-conocimiento ayuda a comparar experimentos.
5. El reel no aporta patrones NUEVOS al lab (todos conocidos), pero aporta
   VOCABULARIO para la arquitectura: nombrar lo que ya hacemos para poder buscar
   los trade-offs. Encaja con la skill ai-architecture (gobernanza de
   arquitectura) y gobernanza-conocimiento.

## DEC

- VALIDA el lab (no gap nuevo): el lab ya tiene ai-architecture, refactor-seguro
  y gobernanza-conocimiento; este reel refuerza el valor de NOMBRAR patrones.
- Accionable (bajo esfuerzo): añadir a ai-architecture la clasificación
  CREATING/COMPOSING/COORDINATING y los 3 matices (Singleton peligroso,
  Strategy vs State, Decorator/Proxy/Adapter) como vocabulario de referencia
  para describir los subsistemas del lab.
- Pendiente opcional: auditar scripts con lente anti-Singleton (estado global)
  cuando se toque el monitor o el scanner.

## Registro

- Backlog 2026-08-06: entrada añadida (veredicto: valida + vocabulario).
- Frames descargados en /tmp (limpiados tras análisis).
