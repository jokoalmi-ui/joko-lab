import json, shutil, os, datetime

BASE = "/home/jokoalmi/joko-lab/lpa/experiments/bolsa"
EST = os.path.join(BASE, "estado-juego.json")
LED = os.path.join(BASE, "ledger-operaciones.jsonl")
SNAP = os.path.join(BASE, "snapshots/2026-10-13.json")

# --- comprobaciones fail-closed con la salida real del scan de hoy ---
d = json.load(open(SNAP))
res = d["resultados"]
assert d["fecha"].startswith("2026-10-13"), d["fecha"]
assert res["UAA"]["live_date"] == "10/13/2026", res["UAA"]
assert res["UAA"]["patron_live"] == "L-swing"
assert res["UAA"]["recovery_live_pct"] == 14.52, res["UAA"]["recovery_live_pct"]
assert res["UAA"]["drawdown_live_pct"] == -34.19, res["UAA"]["drawdown_live_pct"]
assert "live_close" not in res["MCHP"], res["MCHP"]
assert d["errores"] == {"VSCO": "serie insuficiente"}, d["errores"]

fx = 0.895156  # open.er-api.com, time_last_update_utc 2026-10-12T23:57:31Z

MOTIVO = (
 "guardarrail contexto externo (42a entrada no_operar del juego; 41 previas del 06-ago al 12-oct) + "
 "la unica candidata L no pasa el filtro conjunto del juego. DATOS: snapshot 2026-10-13T22:30:30 con "
 "CIERRE OFICIAL DEL DIA 10/13/2026 en los 13 tickers con dato (campo live_close de "
 "/api/quote/{ticker}/info, secondaryData 'Closed at ... 4:00 PM ET'); MCHP es el UNICO ticker SIN CIERRE "
 "EN VIVO en esta pasada (hueco del instrumento ya visto de madrugada, aqui en horario de tarde: se usa su "
 "ultimo cierre de serie, 73,83 del 10/12) y la serie /historical sigue publicando con un dia de retraso "
 "(su ultimo punto en los 14 tickers es el 10/12/2026: 20a confirmacion del lag del API). Cierres oficiales "
 "del 13-oct y variacion sobre el cierre del 12-oct: NVDA 228,52 (+0,97%); V 396,11 (+1,75%, nuevo maximo de "
 "3 meses); GOOGL 353,78 (+0,30%); MSFT 543,45 (+0,43%); AAPL 341,27 (+0,09%); CCL 26,73 (+0,94%); "
 "WDC 380,71 (-1,61%); MRVL 268,73 (+1,08%); REGN 753,12 (-1,27%); PLTR 208,67 (-0,16%); FSLY 27,09 "
 "(+2,50%); UAA 4,89 (-0,91%); NKE 35,34 (-0,01%). VSCO fuera por serie insuficiente. FX del dia: "
 "1 USD = 0,895156 EUR (EUR/USD ~1,117; open.er-api.com, actualizado 12-oct-2026 23:57 UTC). "
 "CANDIDATA_L con el cierre de hoy (1): UAA 4,89 USD, patron_live 'L-swing', DD -34,19% desde el maximo de "
 "3 meses (7,43), REC 14,52% desde el valle de 30 dias (4,27) - PASA el margen al maximo (34,19% >= 20%) "
 "pero FALLA la recovery (14,52% << 50%): 13a confirmacion de que los dos filtros del juego son CONJUNTOS y "
 "no intercambiables; sigue pegada al valle = buy the dip, prohibido por el metodo ('no entras en el caballo "
 "caido, entras en el que ya remonta'); su variacion reciente (~10-15%) es banda, no swing (umbral de Dani). "
 "NOTICIAS DE LA CANDIDATA (contexto, no senal): la lectura del dia sobre UAA es que el suelo se esta "
 "defendiendo, no que haya remontada: Baird (Jonathan Komp) RETIRO su 'Bearish Fresh Pick' el 13-oct "
 "reiterando Neutral con precio objetivo 5,50 USD y el argumento de que 'el riesgo/beneficio se ve mas "
 "equilibrado' tras el -9% desde mediados de septiembre, con Frasers en ~4% del capital total y valoracion "
 "<10x EV/EBITDA sobre estimaciones deprimidas, aunque mantiene riesgo sobre la proyeccion del segundo "
 "semestre fiscal (streetinsider.com, 13-oct-2026). Frasers Group mantiene el 8,78% de la Clase A (16,6 M "
 "acciones, filing del 01-oct; WSJ 07-oct-2026) sin intencion declarada y sin OPA posible (Kevin Plank "
 "controla ~65% del voto; Yahoo Finance 13-oct-2026 recuerda que el fundador sigue siendo el accionista "
 "mayoritario). Evento binario propio CONFIRMADO dentro del horizonte de swing: resultados del Q2 FY27 el "
 "05-nov-2026 (stockanalysis.com, 'Est. Earnings Nov 5, 2026'; tambien trendmatrix.com), con la compania "
 "guiando caida de ventas mid-single-digit para FY2027 y un short interest de ~37% del float que amplifica "
 "el movimiento (Perplexity Finance, 13-oct-2026). Dispersion de consenso alta y util como filtro: PT medio "
 "de ~6,27 USD en 33 analistas (trendmatrix.com, +27% desde el cierre) frente a los 5,50 USD de Baird "
 "(+12,5%) -> el filtro Akamai (margen >= 20% al objetivo) NO es concluyente con esta dispersion. "
 "CONTEXTO EXTERNO: GUARDARRAIL ACTIVO. Sesion del martes 13-oct marcada por (a) el arranque de la temporada "
 "de resultados del Q3 con la gran banca: JPMorgan batio en beneficios (EPS 5,57 vs 5,90 esperado) y en "
 "ingresos (50,91 mM vs 51,22 mM) pero elevo la guia de margen de intereses netos a 106,2 mM (por encima de "
 "los 105,4 mM esperados) y subio ~1,2%; Goldman Sachs batió con ingresos de 18,68 mM frente a 16,71 mM "
 "esperados (acciones +1,4%); Wells Fargo mixto; el S&P 500 se mantuvo cerca de su maximo historico con "
 "subidas de menos del 0,1% y el Nasdaq 100 cayo ~0,3-0,6% (CNBC, WSJ live coverage, Bloomberg via "
 "theedgesingapore.com y AP via ktbs.com, 13-oct-2026); (b) segundo dia de selloff de semis/memoria: los "
 "fabricantes de componentes de disco duro fueron los mas castigados (Seagate hasta -7,9% y Western Digital "
 "-5,5% a las 9:56 ET) tras una caida nocturna en Corea del Sur (Bloomberg via theedgesingapore.com 13-oct; "
 "CNBC 13-oct: 'steep overnight decline in South Korea that put pressure on memory names'); (c) el petroleo "
 "cedio tras tres sesiones de subidas: Brent ~105,20 USD (-1,3/-1,4%) despues de que el IRGC irani "
 "reclamara (sin nombrar buque ni confirmacion independiente) un tercer superpetrolero golpeado en Ormuz, "
 "con el mercado tratando los ataques como coste de flete y no como barriles perdidos (Trading Economics/AP "
 "via tradesprophet.com y gate.com, 13-oct-2026); (d) el registro real de ataques sigue siendo extremo: "
 "UKMTO contabiliza al menos 12 petroleros atacados en y alrededor de Ormuz en la ultima semana y seis "
 "ataques en un solo dia (domingo 11-oct: cinco petroleros y un portacontenedores; MT Valthera confirmado "
 "por India y MT Petro Dolphin en Sohar con dos marineros indios desaparecidos) - 'unprecedented during the "
 "current conflict' (The National 13-oct-2026; World Ports Organization 13-oct-2026); (e) macro: el IPC de "
 "septiembre de EEUU llega manana miercoles 14-oct a las 8:30 ET (consenso 3,6-3,7% general, desde el 3,4%; "
 "Libro Beige el mismo dia), PPI y ventas minoristas el 15-oct y FOMC el 27-28-oct; el 10 anos de EEUU "
 "sigue en maximos desde 2002 (>5,23%) y la Fed mantiene la opcion de otra subida antes de fin de ano "
 "(actas del 07-oct). Los tres criterios explicitos de levantamiento del guardarrail (reapertura CONFIRMADA "
 "de Ormuz, levantamiento del bloqueo naval o acuerdo firmado) siguen SIN cumplirse. RAZONAMIENTO "
 "OBS->HYP->DEC: OBS = una sola candidata L (UAA) y sigue pegada al valle (REC 14,52% frente al 50% "
 "exigido) con el margen al maximo bien cubierto, mientras el contexto externo mantiene la semana mas "
 "intensa de ataques a buques del conflicto (12 en siete dias) y la temporada de resultados arranca con "
 "selloff de semis/memoria pese a la banca solida. HYP = el cuello de botella estructural sigue siendo el "
 "umbral REC>=50% (43 pasadas, 0 operaciones desde el 06-ago) y el guardarrail no tiene ventana de salida: "
 "ninguna de las dos condiciones de entrada puede cumplirse hoy. DEC = no_operar (0 operaciones, 1.000 EUR "
 "virtuales intactos), con UAA en VIGILAR. PENDIENTE: el informe semanal de bolsa de Dani (lunes 12-oct y "
 "lunes 05-oct) sigue SIN poder comprobarse - 16a pasada consecutiva: el puerto CDP 9222 (Chrome normal con "
 "sesion de Skool) devuelve http_code 404 a /json/version a las 22:30 CEST y el 9224 es chrome-lab sin "
 "sesion de Skool - y tampoco aparece en busqueda web; la referencia de contexto del curso sigue siendo la "
 "leccion 5 del 07-sep-2026."
)

APRENDIZAJE = (
 "Regla 'intradia != cierre' medida HOY en el sector disco duro + hueco del instrumento de cierre en vivo "
 "(MCHP). (1) Los titulares de la manana del 13-oct daban un selloff fuerte de memoria/disco: Seagate hasta "
 "-7,9% y Western Digital -5,5% a las 9:56 ET (Bloomberg via theedgesingapore.com), con la caida nocturna "
 "de Corea del Sur como detonante (CNBC) -> el CIERRE OFICIAL del dia (/quote/info) dejo WDC en 380,71 USD, "
 "solo -1,61% sobre el cierre del 12-oct: quien hubiera decidido con el dato intradia habria descrito un "
 "desplome del sector que al cierre no existia, exactamente el mismo patron ya medido el 28-sep (WDC -4% "
 "intradia -> -0,78% al cierre). Refuerza que la decision oficial se toma SOLO con el cierre del dia y que "
 "las cifras intradia son tesis provisionales. (2) Hueco nuevo del instrumento: MCHP fue el UNICO ticker del "
 "universo sin cierre en vivo en la pasada de las 22:30 (sin live_close/live_date en el snapshot; se usa su "
 "ultimo punto de serie, 73,83 del 10/12). Hasta ahora el fallo de secondaryData se habia visto SOLO en la "
 "franja de madrugada (pasada de recuperacion del 09-oct a las 07:19, con el mercado cerrado): este es el "
 "primer caso en horario de tarde, cuando el fix del 18-sep deberia funcionar siempre. No afecto a la "
 "decision (MCHP estaba lateral, DD -14,41% y REC 6,09% con los datos de serie, muy lejos del filtro), pero "
 "queda anotado porque cualquier candidata que caiga en ese hueco se decidiria con datos de un dia antes. "
 "(3) 20a confirmacion del lag del API Nasdaq (04, 08, 09, 14, 15, 16, 17, 18, 21, 23, 24, 25, 28, 29, 30-sep "
 "y 02, 05, 06, 07, 09, 12 y 13-oct; la serie solo publica hasta el 10/12/2026 a las 22:30 CEST). "
 "(4) Catalizador corporativo que se 'desactiva' en lugar de activarse: Baird RETIRO su 'Bearish Fresh Pick' "
 "sobre UAA el 13-oct (Neutral, PT 5,50 USD) por 'riesgo/beneficio mas equilibrado' tras el -9% del ultimo "
 "mes - es la validacion de un SUELO, no de una remontada: el lab mantiene el no_operar porque lo que exige "
 "el metodo es media subida recorrida (REC>=50%), no un suelo defendido por los analistas."
)

# --- backup (RULE-007/008: .bak-YYYYMMDD en la misma carpeta) ---
shutil.copy2(EST, EST + ".bak-20261013")
shutil.copy2(LED, LED + ".bak-20261013")

# --- estado-juego.json ---
e = json.load(open(EST))
assert e["capital_virtual_eur"] == 1000.0
e["decisiones"].append({
    "fecha": "2026-10-13T22:35:00+02:00",
    "decision": "no_operar",
    "candidatas_ignoradas": ["UAA"],
    "motivo": MOTIVO,
    "capital_virtual_eur": 1000.0,
    "posiciones_abiertas": [],
    "fx_usd_eur_13oct": "1 USD = 0,895156 EUR (EUR/USD ~1,117; open.er-api.com, actualizado 12-oct-2026 23:57 UTC); sin impacto operativo: 0 posiciones abiertas",
    "fuente_datos": "nasdaq.com/api (sin key): snapshot 2026-10-13T22:30:30 generado por bolsa_scan.py; /historical con ultimo punto publicado 10/12/2026 (lag) + /api/quote/{ticker}/info secondaryData = cierre OFICIAL del 10/13/2026 en 13 tickers (MCHP sin secondaryData). VSCO descartado por serie insuficiente",
    "fuente_contexto": "CNBC 13-oct-2026 (arranque de resultados de banca, caida nocturna de Corea del Sur, futuros); WSJ live coverage 13-oct-2026 ('Stock Market Today: bank earnings'); Bloomberg via theedgesingapore.com 13-oct-2026 ('S&P 500 holds firm as banks report earnings, chipmakers slump': Seagate hasta -7,9%, WDC -5,5% a las 9:56 ET); AP via ktbs.com 13-oct-2026 (JPMorgan EPS 5,57 vs 5,90, NII 106,2 mM; Goldman +1,4%); The National 13-oct-2026 ('Strait of Hormuz attacks surge': al menos 12 petroleros atacados en la semana); World Ports Organization 13-oct-2026 (UKMTO: seis ataques el 11-oct, MT Valthera, MT Petro Dolphin con dos marineros indios desaparecidos); Trades Prophet y Gate News 13-oct-2026 (Brent ~105,20 USD -1,3/-1,4%, reclamacion no verificada del IRGC de un tercer superpetrolero, CPI EEUU 14-oct 8:30 ET consenso 3,6-3,7%); streetinsider.com 13-oct-2026 (Baird retira el Bearish Fresh Pick de UAA: Neutral, PT 5,50 USD); WSJ 07-oct y Yahoo Finance 13-oct-2026 (Frasers 8,78% = 16,6 M acciones Clase A del filing del 01-oct; Plank ~65% del voto); stockanalysis.com y trendmatrix.com 13-oct-2026 (resultados UAA el 05-nov-2026; PT medio ~6,27 USD en 33 analistas); Perplexity Finance 13-oct-2026 (short interest UAA ~37% del float); open.er-api.com 13-oct-2026 (FX USD/EUR 0,895156)",
})
e["aprendizajes"].append({
    "fecha": "2026-10-13T22:35:00+02:00",
    "tema": "intradia != cierre medido en disco duro (WDC -5,5% a las 9:56 ET -> -1,61% al cierre) + primer hueco del cierre en vivo en horario de tarde (MCHP) + 13a confirmacion del filtro conjunto (43 pasadas, 0 operaciones)",
    "detalle": APRENDIZAJE,
})
e["ultima_actualizacion"] = "2026-10-13T22:35:00+02:00"
tmp = EST + ".tmp"
json.dump(e, open(tmp, "w"), ensure_ascii=False, indent=2)
os.replace(tmp, EST)

# --- ledger ---
line = {
    "tipo": "no_operar",
    "fecha": "2026-10-13T22:35:00+02:00",
    "motivo": MOTIVO,
    "candidatas_ignoradas": ["UAA"],
    "capital_virtual_eur": 1000.0,
    "posiciones_abiertas": [],
    "fx_usd_eur_13oct": "1 USD = 0,895156 EUR (EUR/USD ~1,117; open.er-api.com, actualizado 12-oct-2026 23:57 UTC); sin impacto operativo: 0 posiciones abiertas",
    "fuente_datos": "nasdaq.com/api (sin key): /historical (ultimo punto 10/12/2026 = lag) + /api/quote/{ticker}/info (secondaryData = cierre oficial del 10/13/2026 en 13 tickers; MCHP sin dato en vivo) + snapshot 2026-10-13.json de bolsa_scan.py (22:30:30). Candidata L: UAA (4,89; DD -34,19%; REC 14,52%; max 3m 7,43; valle 30d 4,27 = FALLA la recovery)",
    "fuente_contexto": "CNBC 13-oct-2026; WSJ live coverage 13-oct-2026; Bloomberg via theedgesingapore.com 13-oct-2026 (chips/HDD: Seagate -7,9%, WDC -5,5% intradia); AP via ktbs.com 13-oct-2026 (banca Q3); The National 13-oct-2026 y World Ports Organization 13-oct-2026 (UKMTO: 12 petroleros atacados en la semana, seis ataques el 11-oct); Trades Prophet / Gate News 13-oct-2026 (Brent ~105,20 USD; CPI 14-oct); streetinsider.com 13-oct-2026 (Baird retira Bearish Fresh Pick de UAA, PT 5,50 USD); stockanalysis.com y trendmatrix.com (resultados UAA 05-nov-2026); open.er-api.com (FX 0,895156)",
}
with open(LED, "a") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")

print("OK estado-juego.json decisiones:", len(e["decisiones"]), "aprendizajes:", len(e["aprendizajes"]))
print("ultima_actualizacion:", e["ultima_actualizacion"])
