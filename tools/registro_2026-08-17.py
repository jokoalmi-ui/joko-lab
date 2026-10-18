#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registro diario EXP-002 - 2026-08-17 (no_operar)."""
import json, io, os

BASE = "/home/jokoalmi/joko-lab/lpa/experiments/bolsa"
LEDGER = os.path.join(BASE, "ledger-operaciones.jsonl")
ESTADO = os.path.join(BASE, "estado-juego.json")

entrada = {
    "tipo": "no_operar",
    "fecha": "2026-08-17T22:35:00+02:00",
    "motivo": "guardarrail contexto externo (9o dia de mercado consecutivo): crisis de Ormuz sigue activa SIN acuerdo: 'US-Iran peace talks stall, Hormuz shipping slows' (NDTV Profit 17-ago-2026); Brent sube HOY ~88-91 USD/Bbl (TradingEconomics 17-ago-2026: 90.83 +2,61% hoy y +36,38% interanual; univest.in 17-ago-2026: 89.20, intraday high 89.40; regionalert.com 17-ago-2026: 88.72, +5% semanal por ataques a buques ADNOC y refinería de Aramco; straits.live 17-ago-2026: estrecho efectivamente cerrado al comercio, 1 barco el 09-ago vs ~73/día normal). Candidatas L del scan (datos = ultimo cierre disponible en API, viernes 08/14; la barra del lunes aun no publicada a las 22:31): WDC (508.80, DD -31,82%, rec +17,15%) con rally del sector memoria (tradingkey 17-ago-2026: abre +4,03%; Benzinga 17-ago-2026: optimismo memoria/almacenamiento, +2% premarket) pero recovery 17,15% << 50% = acaba de salir del valle, buy the dip, no mitad de subida; MRVL (222.02, DD -29,84%, rec +35,88%) - SUBE +7,5% intraday hoy a 238.72 (ts2.tech 17-ago-2026), demanda por interconnect y outlook FY27 al alza (Yahoo Finance 17-ago-2026), pero recovery <50% y earnings binarios Q2 FY27 el 27-ago-2026 (en 10 dias; opciones implican swing 14% segun TipRanks 14-ago-2026) + Investor Day 06-oct-2026; MCHP (79.17, DD -22,92%, rec +10,93%) con reiteracion Overweight Cantor Fitzgerald (MarketBeat 17-ago-2026) y guidance Q2 revenue 1.59-1.62B (MarketScreener 17-ago-2026) PERO el COO Richard Simoncic DIMITE efectivo HOY 17-ago-2026 (management change = incertidumbre, SEC filing) y recovery <50%. Ninguna pasa el filtro de upside (rec>=50% + margen al max>=20%). FACTOR AGOSTO (leccion 3): liquidez baja, Dani no tiene mucho dinero en bolsa en agosto. Contexto externo malo y sin mejora + filtro de upside no cumplido + earnings binario MRVL en 10 dias + management change MCHP: NO abrir posiciones nuevas",
    "candidatas_ignoradas": ["WDC", "MRVL", "MCHP"],
    "capital_virtual_eur": 1000.0,
    "fuente_contexto": "NDTV Profit 17-ago-2026 (Hormuz shipping slows, no peace deal); TradingEconomics Brent 17-ago-2026 (90.83, +36,38% interanual); univest.in 17-ago-2026 (Brent 89.20); regionalert.com 17-ago-2026 (Brent 88.72, attacks ADNOC/Aramco); straits.live 17-ago-2026 (Hormuz closed, 1 ship); ts2.tech 17-ago-2026 (MRVL +7,5% a 238.72); Yahoo Finance 17-ago-2026 (MRVL interconnect demand, FY27 outlook); TipRanks/CNN 14-ago-2026 (MRVL options imply 14% swing Q2 earnings); tradingkey.com 17-ago-2026 (WDC +4,03% open); Benzinga 17-ago-2026 (WDC memory optimism); MarketBeat 17-ago-2026 (MCHP Cantor Overweight reiterado); MarketScreener 17-ago-2026 (MCHP Q2 revenue guide 1.59-1.62B); Stockopedia/SEC 17-ago-2026 (MCHP COO Simoncic resigns); nasdaq.com/api snapshot 2026-08-17 (ultimo cierre disponible 08/14)"
}

with io.open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
print("LEDGER OK")

with io.open(ESTADO, "r", encoding="utf-8") as f:
    estado = json.load(f)

decision = {
    "fecha": "2026-08-17T22:35:00+02:00",
    "decision": "no_operar",
    "motivo": "guardarrail contexto externo (9o dia de mercado consecutivo): Ormuz activo sin acuerdo (NDTV Profit 17-ago-2026), Brent 88-91 subiendo hoy +36,38% interanual (TradingEconomics 17-ago-2026; univest; regionalert; straits.live). Candidatas L: WDC (508.80, rec 17,15%), MRVL (222.02, rec 35,88%, earnings Q2 FY27 27-ago-2026 en 10 dias), MCHP (79.17, rec 10,93%, COO dimite hoy). Ninguna pasa filtro de upside (rec>=50%). FACTOR AGOSTO: liquidez baja. NO abrir posiciones nuevas",
    "candidatas_ignoradas": ["WDC", "MRVL", "MCHP"]
}
estado.setdefault("decisiones", []).append(decision)

with io.open(ESTADO, "w", encoding="utf-8") as f:
    json.dump(estado, f, ensure_ascii=False, indent=2)
print("ESTADO OK, decisiones:", len(estado["decisiones"]))
