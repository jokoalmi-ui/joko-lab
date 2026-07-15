# Cinco ideas que NO implementar en Joko Lab durante el próximo año

---

## 1. Dashboard web unificado (Grafana + Prometheus)

**Qué sería:** Un panel web tipo Grafana que centralice métricas de todos los servicios: CPU, RAM, VRAM, estado de contenedores, latencia de modelos, logs centralizados.

**Por qué NO:**

- Ya tenemos múltiples dashboards: `nvidia-smi` para GPU, `docker ps` para contenedores, el monitor Flask de LM Studio, y los logs individuales de cada servicio.
- El problema real no es "no tenemos métricas", es "no sabemos interpretar lo que ya tenemos".
- Prometheus + Grafana añaden su propio stack: recolector, base de datos time-series, configuración de alertas. Eso requiere mantenimiento continuo.
- **No reduce trabajo futuro significativamente** porque el tiempo que ahorrarías mirando un panel lo gastas manteniendo el panel.
- **No mejora el conocimiento del sistema** — las métricas ya están disponibles con comandos simples.
- **No mejora la capacidad de operar autónomamente** — un panel no diagnostica ni repara.

Criterio Joko Lab: no aporta ninguno de los tres beneficios. Rechazada.

---

## 2. Replicar flujos de n8n en scripts Python

**Qué sería:** Migrar flujos de n8n a scripts Python o Node.js "para tener más control" o "para eliminar dependencia de n8n".

**Por qué NO:**

- n8n es una herramienta consolidada, con UI, scheduling, logging, manejo de errores, credenciales, y ejecución visual. Replicar eso en scripts es reinventar la rueda mal.
- Cada flujo migrado sería un proyecto de scripting independiente, sin interfaz, sin logging estructurado, sin scheduler nativo.
- **No reduce trabajo futuro** — al contrario, multiplica el mantenimiento.
- **No mejora el conocimiento del sistema** — ya sabes usar n8n.
- **No mejora la capacidad de operar autónomamente** — tus flujos ya se ejecutan solos en n8n.

Excepción: si algún día n8n se vuelve inestable o bloquea la evolución del laboratorio, se reconsidera. Pero no es el caso actual.

Criterio Joko Lab: va contra el principio 4 (soluciones simples y mantenibles). Rechazada.

---

## 3. Servicio de auto-aprendizaje continuo (fine-tuning local automático)

**Qué sería:** Un pipeline que coja conversaciones del laboratorio, las limpie, y haga fine-tuning de un modelo local periódicamente para mejorar respuestas.

**Por qué NO:**

- El fine-tuning local con una RTX A2000 de 12 GB es posible pero lento. Un fine-tuning completo puede llevar horas o días.
- El dataset de conversaciones del laboratorio es pequeño y ruidoso. No hay garantía de que mejore el modelo.
- El pipeline requeriría: recolección, limpieza, formateo, validación, ejecución de fine-tuning, evaluación. Eso es un proyecto grande en sí mismo.
- Hardware actual: 12 GB VRAM. Un fine-tuning de un modelo de 7B ya consume prácticamente toda la VRAM, dejando sin servicio a Ollama y LM Studio durante horas.
- **No reduce trabajo futuro** — el overhead de gestionar el pipeline supera cualquier beneficio hipotético.
- **No mejora el conocimiento del sistema** — el laboratorio no necesita un modelo personalizado para funcionar.

Criterio Joko Lab: viola el principio 1 (comprender antes de actuar) — no sabemos si el fine-tuning aporta valor real. Rechazada.

---

## 4. Sistema de backups automáticos a la nube (AWS S3, Backblaze, etc.)

**Qué sería:** Un cron que suba backups de n8n, configuraciones, y datos críticos a un proveedor cloud.

**Por qué NO:**

- Ya tienes backups locales en `/mnt/ssd_ia_datos/backups`.
- Añadir cloud introduce:
  - Dependencia de un proveedor externo.
  - Coste recurrente (aunque pequeño).
  - Latencia en subida de backups grandes (varios GB).
  - Credenciales que gestionar.
  - Complejidad extra en scripts de backup.
- El riesgo real no es perder datos por desastre físico, es perder datos por error humano (borrar algo, romper configuración). Un backup local en un disco separado ya cubre ese caso.
- **No reduce trabajo futuro** — añade mantenimiento.
- **No mejora el conocimiento del sistema** — ya sabes hacer backups.
- **No mejora la capacidad de operar autónomamente** — los backups locales ya son automáticos.

Excepción: si algún día los datos del laboratorio crecen al punto de ser irremplazables y el disco SSD es el único punto de fallo, se reconsidera. Pero no es el caso actual.

Criterio Joko Lab: viola el principio 4 (priorizar soluciones simples). El backup local es más simple y suficiente. Rechazada.

---

## 5. Reescritura completa de la documentación en formato libro/PDF

**Qué sería:** Convertir toda la documentación del laboratorio (HERMES.md, READMEs de skills, docs/decisiones/) a un libro estructurado en PDF o HTML estático.

**Por qué NO:**

- La documentación actual ya está en markdown, versionada, buscable, y listada en el orden de consulta.
- Un PDF se desactualiza en cuanto modificas un archivo. Para mantenerlo sincronizado, necesitas un pipeline de build automático (más mantenimiento).
- No hay evidencia de que el formato actual sea insuficiente. El problema no es la presentación, es el contenido.
- **No reduce trabajo futuro** — el PDF se desactualiza y genera trabajo de sincronización.
- **No mejora el conocimiento del sistema** — el conocimiento ya está en markdown.
- **No mejora la capacidad de operar autónomamente** — la documentación markdown ya es consultable desde terminal.

Criterio Joko Lab: viola el principio 4 (priorizar soluciones simples) y el principio 1 (comprender antes de actuar) — no sabemos si el formato actual es un problema real. Rechazada.

---

## Resumen

| # | Idea | Motivo principal | Principio violado |
|---|------|------------------|-------------------|
| 1 | Dashboard web (Grafana) | Ya tienes métricas accesibles, añade un stack entero | No aporta los 3 beneficios |
| 2 | Replicar n8n en scripts | n8n ya funciona, reinventar es más trabajo | Principio 4 (simplicidad) |
| 3 | Fine-tuning automático | Consume VRAM sin valor probado, overhead enorme | Principio 1 (comprender) |
| 4 | Backups a la nube | Añade complejidad sin necesidad real | Principio 4 (simplicidad) |
| 5 | Documentación en PDF | Se desactualiza, no mejora nada existente | Principios 1 y 4 |

Todas fallan el filtro de la filosofía operativa del laboratorio: ninguna reduce trabajo futuro, aumenta el conocimiento del sistema, o mejora la capacidad de operar autónomamente de forma significativa.
