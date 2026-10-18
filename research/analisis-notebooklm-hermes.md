---
title: "Análisis — Vídeo: NotebookLM (Gemini Notebook) + Hermes (Rodolfo Carrasco)"
type: research
---

# Análisis — Vídeo: NotebookLM (Gemini Notebook) + Hermes (Rodolfo Carrasco)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 09-ago-2026
**Fuente:** https://youtu.be/aA_OfLKe700 — Rodolfo Carrasco (Kerkcour System, agencia IA)
**Tema:** La nueva actualización de NotebookLM → "Gemini Notebook" + cómo conectarlo con Hermes

---

## Qué trae la actualización

| Característica | Detalle |
|---|---|
| **Nuevo nombre** | NotebookLM → **Gemini Notebook** |
| **Fuentes** | PDF, Word, web, vídeos YouTube, audios, hojas de cálculo — hasta 50/cuaderno (gratis) |
| **Plan gratis** | 100 cuadernos, 50 fuentes/cuaderno, 50 preguntas/día, 3 audios/día |
| **Servidor por cuaderno** | Solo en planes Pro/Ultra (el "servidor" de Google por cuaderno) |
| **Clave** | Responde SOLO con las fuentes incrustadas — cita, y si no sabe, lo dice (no alucina) |

## La conexión con Hermes (lo interesante)

**Problema:** Gemini Notebook no tiene "manos" — no abre carpetas, no escribe archivos, no manda correos.

**Solución del vídeo:** conectar NotebookLM con Hermes vía CLI:
- `notebook login` (auth con cuenta de Google)
- `notebook chat` (verifica autenticación)
- `notebook create` (crea cuaderno)
- Skill en la carpeta de Hermes para que el agente use NotebookLM como herramienta

**Caso de uso demostrado:** preparar reunión con cliente nuevo
1. Hermes crea cuaderno "reunión reformas del mar" en NotebookLM
2. Mete 3 archivos (web, LinkedIn, notas de llamada)
3. Hermes consulta NotebookLM → nota técnica del negocio del cliente
4. Hermes busca más fuentes en internet por su cuenta → guion completo de reunión

---

## 🔗 Aplicación al LAB

### El lab YA tiene esto cubierto (y mejor)

| NotebookLM | Lab |
|---|---|
| Responde con fuentes incrustadas | ✅ **RAG local (BGE-M3 + LanceDB)** — mismo principio, local y privado |
| No alucina (dice si no sabe) | ✅ Evidencia de fuentes en el RAG |
| 50 fuentes/cuaderno | ✅ Ilimitado en el vault |
| Servidor en la nube (pago) | ✅ Local (A2000) |
| Citas a fuentes | ✅ RAG devuelve paths |

### Lo ÚNICO que aporta

**Conexión Hermes ↔ NotebookLM como herramienta externa** — pero el lab no la necesita:
- El RAG del lab ya hace lo mismo (búsqueda en el vault) sin depender de la nube de Google
- NotebookLM añadiría dependencia de cuenta Google + límites de 50 preguntas/día

### Para el TFM/Founderz
- El caso de uso (preparar reunión con cliente) es buen **material de presentación**
- Demuestra el patrón "agente + herramienta de investigación con fuentes"

## Veredicto honesto

**El vídeo valida el diseño del RAG del lab** (responder con fuentes, no alucinar)
pero **no aporta nada accionable** — NotebookLM es una alternativa en la nube a lo
que el lab ya tiene local, con más límites. No se implementa nada.

**Si algún día se quiere NotebookLM** (ej. para TFM con fuentes Google), la
conexión vía CLI/skill es el camino — pero es opcional y añade dependencia cloud.

## Nota

Canal: Rodolfo Carrasco (Kerkcour System) — promociona mentorías/WhatsApp.
El kit de instalación se entrega vía grupo de WhatsApp (no es de acceso abierto).
