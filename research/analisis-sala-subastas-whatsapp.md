---
title: "Análisis — Sala de subastas por WhatsApp: viabilidad (16-ago-2026)"
type: research
---

# Análisis — Sala de subastas por WhatsApp: viabilidad (16-ago-2026)

**Fuente:** investigación web (web_search + GitHub API)
**VERACIDAD:** [ALCANCE INTERNO]

## La pregunta: ¿se puede montar/gestionar una sala de subastas por WhatsApp?

### Veredicto corto
**SÍ se puede, pero el canal natural es Telegram, no WhatsApp.** WhatsApp sirve
para AVISAR de subastas (notificaciones), no para el mecanismo de puja en vivo.
Razones verificadas abajo.

## 1. WhatsApp — la vía oficial (Business API) es cara y rígida

- **WhatsApp Business API (WABA)** [VERIFICADO — fuentes múltiples, 2026]: es la
  interfaz oficial de Meta para mensajería empresarial automatizada. Requisitos:
  Business Portfolio + número dedicado + **BSP certificado** (Business Solution
  Provider) + **aprobación de plantillas de mensajes**.
- **BSP**: 360dialog y Twilio son los más conocidos [NO VERIFICADO — el subagente
  no los confirmó; son proveedores ampliamente citados pero no verificados hoy].
- **Coste**: modelo de pago por conversación (sesión de 24h), NO por mensaje
  suelto — coste por cada puja/aviso [ALCANCE INTERNO — coste exacto no
  verificado hoy; depende del BSP y región].
- **⚠️ Regla 2026 [VERIFICADO — Runia/blog sobre cambios 2026]**: Meta actualizó
  los términos: **los chatbots deben realizar tareas de negocio específicas, no
  ser conversadores generales**. Una "sala de subastas" con pujas libres en
  lenguaje natural choca con el modelo de plantillas aprobadas (cada plantilla
  se aprueba; la puja libre no es una plantilla fija).
- **Conclusión WhatsApp**: viable para NOTIFICACIONES (aviso "nueva puja",
  "subasta termina en 1h") con plantillas aprobadas; NO adecuado para el
  mecanismo de puja abierta en vivo (fricción de aprobación, coste por
  conversación, regla anti-chat-general).

## 2. Telegram — el canal natural (API de bots abierta y gratis)

- API de bots **abierta, gratuita y sin aprobación de plantillas** — mensajes
  libres, grupos, inline. [VERIFICADO — conocimiento de dominio del lab: Hermes
  ya usa bots/API de Telegram; la documentación oficial lo confirma]
- **Bots de subasta open source existentes** (verificados vía GitHub API 16-ago):

| Repo | ⭐ | Lenguaje | Licencia | Último push | Estado |
|---|---|---|---|---|---|
| qellyka/telegram-auction-bot | 8 | Python | MIT | **2025-06-06** | 🟢 ACTIVO |
| ribbon-finance/telegram-auction-bot | 5 | TypeScript | Sin lic | 2022-02 | 🟡 Viejo |
| guglielmino/astone-bot | 7 | HTML | MIT | 2019-11 | 🔴 Abandonado |
| skswhwo/AuctionBot | 0 | Ruby | Sin lic | 2016-10 | 🔴 Muerto |

- **qellyka/telegram-auction-bot** [VERIFICADO]: Python, MIT, push 2025 —
  plataforma para crear subastas y listar artículos (enfocado a gifts de
  Telegram pero usable para otros). Es la BASE viable más cercana.

## 3. Alternativa propia (si se quiere control total)

- **Bot de Telegram propio** con python-telegram-bot o aiogram: pujas, cierre
  automático, registro de ganadores — todo local (encaja con el lab).
  [ALCANCE INTERNO — es la vía que usaría el lab]
- **Bot de WhatsApp no oficial** (whatsapp-web.js): funciona pero **riesgo de
  baneo del número** por violar ToS de Meta. [ALCANCE INTERNO — riesgo conocido]

## 4. Comparativa para el caso

| Criterio | WhatsApp (Business API) | Telegram (bot) |
|---|---|---|
| Coste | Por conversación + BSP | **Gratis** |
| Aprobación | Plantillas aprobadas | **Ninguna** |
| Puja libre en vivo | ❌ Choca con regla 2026 | ✅ Natural |
| Notificaciones | ✅ Bueno | ✅ Bueno |
| Open source | ❌ API cerrada | ✅ 4 repos |
| Riesgo de baneo | Bajo (oficial) | Nulo (oficial) |

## Recomendación final
1. **Canal principal: Telegram** — bot propio (o base qellyka/telegram-auction-bot
   si encaja) con pujas, cierre automático y registro. Encaja con local-first
   del lab.
2. **WhatsApp solo como avisos** (si se quiere): Business API con 2-3 plantillas
   aprobadas (nueva puja, cierre, recordatorio) vía BSP.
3. **No** usar whatsapp-web.js (baneo) para el mecanismo de puja.

**Nota de proceso:** la delegación previa (deleg_f631cd85, toolsets=['web']) dio
un informe pobre (2 llamadas API, sin verificar nada). La verificación real se
hizo después con web_search + GitHub API — lección: los self-reports de
subagentes NO son hechos; verificar siempre.
