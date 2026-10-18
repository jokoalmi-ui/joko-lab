#!/usr/bin/env python3
"""Registro EXP-002 - pasada 2026-08-13 22:35: decision no_operar."""
import json

ESTADO = "/home/jokoalmi/joko-lab/lpa/experiments/bolsa/estado-juego.json"
LEDGER = "/home/jokoalmi/joko-lab/lpa/experiments/bolsa/ledger-operaciones.jsonl"

motivo = (
    "guardarrail contexto externo (7o dia de mercado consecutivo): crisis de Ormuz activa y EN EXPANSION. "
    "Los Houthis entraron en la guerra de Iran: ataques diarios en Yemen y Arabia Saudi (CSIS 13-ago-2026); "
    "derrame de petroleo masivo en Ormuz, Iran culpa a los stakeholders, IEA advierte de -4% de suministro global "
    "(Benzinga 13-ago-2026); Iran cerro de nuevo el estrecho y Trump afirma tener control (Alex Jones Live 13-ago-2026). "
    "Brent 87.92 USD/Bbl -1,19% hoy pero +31,53% interanual (TradingEconomics 13-ago-2026); Bloomberg Opinion 13-ago-2026: "
    "el mercado no grita escasez (<90 USD) por reservas estrategicas y oleoductos de bypass, pero el conflicto sigue "
    "impredecible. Candidatas L del scan: MRVL (cierre 217.08, DD -31,40%, recovery +32,85%) - upgrade Zacks Rank #2 Buy "
    "(Yahoo Finance 13-ago-2026) y noticia de rating (Seeking Alpha 13-ago-2026, 12:30 ET), PT promedio 271.33 (TipRanks), "
    "portafolio AI memory FMS (04-ago), pero NO pasa el filtro de upside (recovery 32,85% < 50%) y tiene earnings binarios "
    "Q2 FY27 el 27-ago-2026 (en 14 dias) + Investor Day 06-oct-2026; MCHP (cierre 79.44, DD -22,66%, recovery +11,31%) con "
    "beat Q1 FY27 del 06-ago (EPS 0.76 vs 0.70, revenue 1.485B +38% YoY +13,2% secuencial, ir.microchip.com; MarketBeat) y "
    "dividendo 0.455 ex 24-ago-2026, tampoco pasa el filtro (recovery <50%). FACTOR AGOSTO (leccion 3): baja liquidez "
    "estacional, Dani no tiene mucho dinero en bolsa en agosto. Contexto externo malo y ampliandose + filtro de upside no "
    "cumplido + earnings binario proximo: NO abrir posiciones nuevas"
)

fuente_contexto = (
    "CSIS 13-ago-2026 (Houthis enter Iran war); Benzinga 13-ago-2026 (oil spill Hormuz, IEA -4% supply); "
    "Alex Jones Live 13-ago-2026 (Iran closed Hormuz again); TradingEconomics Brent 13-ago-2026 (87.92, +31,53% interanual); "
    "Bloomberg Opinion 13-ago-2026 (Hormuz not closed, <90 USD); Yahoo Finance 13-ago-2026 (MRVL Zacks Rank #2 Buy); "
    "Seeking Alpha 13-ago-2026 (MRVL rating upgrade); TipRanks (MRVL PT promedio 271.33); "
    "ir.microchip.com 06-ago-2026 (MCHP Q1 FY27 beat); MarketBeat (MCHP EPS 0.76 vs 0.70); "
    "nasdaq.com/api snapshot 2026-08-13"
)

decision = {
    "fecha": "2026-08-13T22:35:00+02:00",
    "decision": "no_operar",
    "motivo": motivo,
    "candidatas_ignoradas": ["MRVL", "MCHP"],
}

with open(ESTADO, encoding="utf-8") as f:
    estado = json.load(f)
estado["decisiones"].append(decision)
with open(ESTADO, "w", encoding="utf-8") as f:
    json.dump(estado, f, indent=2, ensure_ascii=False)
    f.write("\n")

entry = {
    "tipo": "no_operar",
    "fecha": decision["fecha"],
    "motivo": motivo,
    "candidatas_ignoradas": decision["candidatas_ignoradas"],
    "capital_virtual_eur": 1000.0,
    "fuente_contexto": fuente_contexto,
}
with open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print("OK: estado-juego.json actualizado + ledger append")
