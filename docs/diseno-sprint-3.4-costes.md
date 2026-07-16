================================================================================
       SPRINT 3.4 — DISEÑO AJUSTADO (post-objeciones)
       2026-07-16
================================================================================

1. VERIFICACIÓN DE ENDPOINTS REALES (contra API con curl)
2. MODO ESTIMACIÓN — LOG DE ADVERTENCIA
3. CALIBRACIÓN DE TOKENS/SESIÓN CON DATOS REALES
4. DISEÑO FINAL

================================================================================
1. VERIFICACIÓN DE ENDPOINTS REALES
================================================================================

DeepSeek:
  Endpoint:   GET https://api.deepseek.com/user/balance
  Header:     Authorization: Bearer $DEEPSEEK_KEY
  Respuesta:  {"is_available":true,
                "balance_infos":[{"currency":"USD",
                                  "total_balance":"16.86",
                                  "granted_balance":"0.00",
                                  "topped_up_balance":"16.86"}]}
  Modo:       API DIRECTA — saldo real disponible
  Limitación: No hay endpoint de uso histórico (/user/usage, /dashboard/billing
              no existen o devuelven vacío). Solo saldo actual.

Gemini:
  Endpoint:   No existe endpoint de billing con API key simple.
              Google Cloud billing API requiere proyecto GCP facturado,
              no está disponible vía API key de Gemini.
  Modo:       SÓLO ESTIMACIÓN

================================================================================
2. MODO ESTIMACIÓN — LOG DE ADVERTENCIA
================================================================================

Cuando la fuente no sea "api_directa":

  En state-manager.py (check_cost):
    - Log: "⚠️  <proveedor>: coste estimado — no hay API de billing disponible"
    - state.json: "fuente": "estimacion"

  En apply-decision.sh (ya existente):
    - No necesita cambios — no toca costes.

  En el informe ejecutivo:
    - Si "fuente" = "estimacion", mostrar: "*coste estimado, no real"

================================================================================
3. CALIBRACIÓN DE TOKENS/SESIÓN CON DATOS REALES
================================================================================

Datos reales del sistema (verificados):
  - Sesiones Hermes totales:      12 (desde 13 julio)
  - Sesiones por día:             ~4
  - Tamaño medio por sesión:      ~400 KB
  - Equivalente bruto:            ~100K tokens/sesión (4 bytes/token)
  - Estimación realista (tool calls
    inflan el tamaño en 2-3x):   ~30-50K tokens de API/sesión

Default propuesto: 40K tokens/sesión
  - Se recalibra tras 7 días comparando con diferencia de saldo real
    de DeepSeek (único que tiene API directa).

Ejemplo de calibración:
  Día 1: saldo = 16.86 USD
  Día 7: saldo = 16.50 USD
  Diferencia real = 0.36 USD en 7 días
  Estimación (40K * 4 sesiones/día * 7 días * $0.50/M) = 0.56 USD
  Factor de corrección = 0.36 / 0.56 = 0.64
  → Ajustar default a 40K * 0.64 = ~25K tokens/sesión

Sin este paso, el default se queda como "40K hasta tener dato real".

================================================================================
4. DISEÑO FINAL (state-manager.py)
================================================================================

Nuevo método en _collect_fast():

def check_cost():
    costes = {}

    # --- DeepSeek: API directa ---
    saldo = None
    try:
        key = read_secret("deepseek.key")
        r = requests.get("https://api.deepseek.com/user/balance",
                         headers={"Authorization": f"Bearer {key}"},
                         timeout=10)
        if r.status_code == 200:
            data = r.json()
            saldo = float(data["balance_infos"][0]["total_balance"])
            fuente = "api_directa"
        else:
            fuente = "estimacion"
            log("⚠️  DeepSeek: /user/balance devolvió HTTP {r.status_code}")
    except Exception as e:
        fuente = "estimacion"
        log(f"⚠️  DeepSeek: error al consultar balance — {e}")

    # --- Gemini: solo estimación ---
    fuente_gemini = "estimacion"
    log("⚠️  Gemini: coste estimado — no hay API de billing disponible")

    # --- Estimación basada en actividad ---
    tokens_por_sesion = TOKENS_POR_SESION  # 40000, recalibrable
    sesiones_hoy = contar_sesiones_hoy()   # lee sessions dir
    coste_estimado_deepseek = sesiones_hoy * tokens_por_sesion * PRECIO_DEEPSEEK
    coste_estimado_gemini = sesiones_hoy * tokens_por_sesion * PRECIO_GEMINI

    costes["deepseek"] = {
        "saldo_actual_usd": saldo,          # null si no disponible
        "fuente": fuente,
        "gasto_diario_estimado_usd": coste_estimado_deepseek,
        "ultima_actualizacion": now()
    }
    costes["gemini"] = {
        "saldo_actual_usd": None,
        "fuente": "estimacion",
        "gasto_diario_estimado_usd": coste_estimado_gemini,
        "ultima_actualizacion": now()
    }

    return costes

Constantes nuevas:
  TOKENS_POR_SESION = 40000     # recalibrar tras 7 días
  PRECIO_DEEPSEEK   = 0.50e-6   # $/token (deepseek-v4-flash)
  PRECIO_GEMINI_IN  = 0.25e-6   # $/token input
  PRECIO_GEMINI_OUT = 1.50e-6   # $/token output
  PRECIO_GEMINI_MEDIA = 0.75e-6 # media ponderada 3:1

Salida en state.json (nuevo):
  "costes": {
    "deepseek": {
      "saldo_actual_usd": 16.86,
      "fuente": "api_directa",
      "gasto_diario_estimado_usd": 0.08,
      "ultima_actualizacion": "2026-07-16T08:00:00"
    },
    "gemini": {
      "saldo_actual_usd": null,
      "fuente": "estimacion",
      "gasto_diario_estimado_usd": 0.04,
      "ultima_actualizacion": "2026-07-16T08:00:00"
    },
    "total_diario_estimado_usd": 0.12,
    "total_mensual_estimado_usd": 3.60,
    "nota": "Gemini es estimado — solo DeepSeek tiene API de billing"
  }

================================================================================
LO QUE NO CAMBIA
================================================================================

- config.yaml — no se toca
- horario.yaml — no se toca
- decision_engine.py — no se toca
- apply-decision.sh — no se toca
- Ninguna política, capability o contrato
- Ningún test existente

================================================================================
Validación POST-IMPLEMENTACIÓN
================================================================================

1. Ejecutar state-manager manualmente una vez
2. Verificar que state.json contiene el bloque "costes"
3. Confirmar que deepseek.fuente = "api_directa" y saldo ≈ 16.84
4. Confirmar que gemini.fuente = "estimacion"
5. Log debe mostrar "⚠️ Gemini: coste estimado"
6. A los 7 días: comparar diferencia de saldo real con estimación acumulada
   y recalibrar TOKENS_POR_SESION si difiere >20%

================================================================================
📌 REGLA ADICIONAL: DETECCIÓN DE RECARGA MANUAL
================================================================================

Si la diferencia de saldo entre dos lecturas consecutivas es POSITIVA
(el saldo subió en vez de bajar), NO se interpreta como "gasto negativo".

En su lugar:
  - state.json: "gasto_diario_estimado_usd": null, "recarga_detectada": true
  - Log: "⚠️ DeepSeek: saldo subió de X a Y — recarga manual detectada.
         Gasto diario no computable este período."
  - El saldo anterior se conserva como referencia para el próximo ciclo.

Sin esta regla, una recarga de $17 daría "gasto_diario_estimado_usd": -17.00
en state.json, que es un dato absurdo sin validación.

================================================================================
📌 NOTA: RELEVANCIA DE GLM TRAS EL CÁLCULO DE COSTE REAL
================================================================================

Con el default de 13K tokens/sesión y ~4 sesiones/día:

  Gasto DeepSeek (15h/día):   ~$0.046/día
  Gasto Gemini (9h/día):      ~$0.039/día
  Total estimado:             ~$0.085/día (~$31/año)

Si GLM (gratuito) sustituyera a Gemini en su franja, el ahorro sería de
~$0.039/día, que es el ~46% del gasto total en cloud. Proporcionalmente
es relevante, aunque en términos absolutos sean ~$14/año.

Esto NO decide la integración de GLM (sigue pendiente la prueba de
calidad). Pero da contexto real de cuánto pesa la decisión: no es
"céntimos sueltos", es casi la mitad del gasto cloud.
