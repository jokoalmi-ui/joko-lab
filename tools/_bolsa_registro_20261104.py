import json, io

BASE = '/home/jokoalmi/joko-lab/lpa/experiments/bolsa'

nuevo = {
 "fecha": "2026-11-04",
 "hora": "22:35",
 "decision": "no_operar",
 "tipo": "no_operar",
 "ticker": None,
 "precio_usd": None,
 "precio_entrada_usd": None,
 "precio_salida_usd": None,
 "retorno_pct_usd": None,
 "retorno_pct_eur": None,
 "capital_virtual_eur": 1000.0,
 "posiciones_abiertas": [],
 "fx_usd_eur": 0.893426,
 "horizonte": None,
 "candidatas_L": [],
 "descartados": [
  {"ticker": "UAA", "precio_usd": 5.77, "var_dia_pct": 8.15, "patron": "ascendente",
   "rec_rango_pct": 65.0, "drawdown_pct": -9.84, "upside_max_3m_pct": 10.91,
   "motivo": "CRUZA el gatillo del 35% de rango (ayer 34,03% en 5,335) y deja de ser L-swing: con 5,77 el rango ya es 65,0% y el DD solo -9,84% -> el upside al maximo de 3m (6,40) cae a +10,91%, por debajo del 20% exigido. Ademas presenta el Q2 FY27 el 06-nov a las 06:55 ET (evento binario a 3 horas de la apertura siguiente). Doble no: demasiado tarde + evento binario."},
  {"ticker": "WDC", "precio_usd": 323.83, "var_dia_pct": -6.80, "patron": "descendente",
   "rec_rango_pct": -4.0, "drawdown_pct": -39.59,
   "motivo": "PERDIDO el valle de 30 dias 332,00 (cierra 323,83): REC_RANGO negativo (-4,0%), patron descendente. El selloff de memoria/disco por el resultado electoral y la guia cauta de Kioxia (02-nov) deshace el L. Solo vuelve a watchlist si reconstruye un valle nuevo."},
  {"ticker": "MRVL", "precio_usd": 159.8, "var_dia_pct": -7.08, "patron": "descendente",
   "rec_rango_pct": -10.04, "drawdown_pct": -44.32,
   "motivo": "Rompe tambien su valle de 30 dias (171,41) al cerrar en 159,80: -44,32% desde el maximo de 3m y REC_RANGO -10,04%. Causa: la compra de Lumentum todo en acciones (dilucion ~50% del share count; BofA rebaja a Neutral y PT 225 desde 400, CNBC 03-nov) + castigo extra del sector data-center tras la victoria democratica. Un patron L no sobrevive a un evento de dilucion (2a confirmacion tras el 29-oct)."}
 ],
 "guardarrail_externo": "ACTIVO (12a sesion): Brent 103,60 USD (cierre 03-nov, minimo de 4 semanas) y sin reapertura de Ormuz. Entre el 29 y el 30-oct, al menos 4 petroleros alcanzados por proyectiles y minas lapa (Windward; ultimo uso con exito de minas lapa en la region en 2019) y el buque Louise 1 con dos cargas en el casco a 25 mn de Khasab; EEUU ataco la isla de Qeshm (02-03 nov); la OMI no recomienda a ningun buque usar el estrecho (Dominguez, 02-nov). Transitos en octubre: 750 observados/asumidos (749 en septiembre, maximo desde julio), con VLCC bajando a 156 desde 184 y Bab al-Mandeb saudita a 21 desde 52. Negociacion del 'plan de dos dias' en Doha sin acuerdo. Ninguno de los tres criterios de levantamiento se cumple.",
 "motivo": "58a pasada, 0 operaciones. CANDIDATAS_L: NINGUNA por primera vez desde el 01-sep: el universo del juego (semis/memoria/data-center) se ha ido a descendente o lateral mientras el indice sube. Sesion de dos velocidades tras las midterms del 03-nov (victoria democratica en ambas camaras): Dow +2,8% (~1.400 pts), S&P 500 +1,7%, Nasdaq +2,0% con Apple y Microsoft en maximos historicos, pero el hardware de IA y la memoria se venden con fuerza por el compromiso democratico de endurecer la construccion de data centers: SNDK -9%, COHR -7%, STX -6,9%, WDC -6,8%, MU -5,7%, LITE -10%, MRVL -7,1%. En el universo: NVDA -3,2% (200,13; descendente), GOOGL descendente, PLTR descendente, FSLY descendente; unicos ascendentes V (436,67), REGN (930,67), CCL (31,32), MSFT (555,80) y NKE (40,48, en lista EVITAR), ninguno con patron L. UAA es el caso del dia: cruzo el gatillo del 35% de rango que llevaba 5 sesiones acechando, pero lo hizo un dia antes de su propio print y con el upside ya en +10,91%, de modo que el umbral se cumplio cuando la operacion ya no era valida por dos vias independientes. Racing: 0 posiciones, 1.000 EUR virtuales intactos; nada que autocorregir (0 operaciones cerradas).",
 "fuente_datos": "nasdaq.com/api (sin key): snapshot 2026-11-04T22:31:55 (tools/bolsa_scan.py); cierre oficial del dia via /api/quote/{ticker}/info (secondaryData 'Closed at ... 4:00 PM ET') en los 14 tickers; /api/quote/{ticker}/historical con lag de un dia (ultimo punto 11/03/2026); VSCO fuera por serie insuficiente; FX open.er-api.com 04-nov-2026 00:02 UTC (0,893426 USD/EUR)",
 "fuente_contexto": "Yahoo Finance 04-nov-2026 (midterms: victoria democratica en ambas camaras, Dow +2,8%/1.478 pts, S&P +1,7%, Nasdaq +2%, Apple y Microsoft en maximos); Schwab 04-nov-2026 (reapertura tras la victoria democratica); TradingEconomics 04-nov-2026 (futuros y CFD, S&P 7.545 el 04-nov); Yahoo/247wallst 04-nov-2026 ('Lumentum Sinks 10% With Marvell as Blue Wave Hits Data-Center Stocks'); 247wallst 04-nov-2026 ('SanDisk Retreats 9%, Micron and Western Digital Fall 7% as Election and Memory Price Worries Weigh'); CNBC 03-nov-2026 (BofA rebaja MRVL a Neutral, PT 225 desde 400, dilucion ~50%); oilandgasmiddleeast 04-nov-2026 y SPA 03-nov-2026 (Brent 103,60, minimo de 4 semanas; minas lapa 29-30 oct; 750 transitos en octubre; OMI); grafa 04-nov-2026 (Brent 103,60, WTI 95,98; Vortexa octubre 17,1 Mb/d); Yahoo Finance 04-nov-2026 (UAA Q2 FY27 el 06-nov 08:30 ET / 06:55 ET release; estimaciones -0,01 USD y 1,23 mM)",
 "fuentes": [
  "https://api.nasdaq.com/api/quote/UAA/info?assetclass=stocks",
  "https://api.nasdaq.com/api/quote/UAA/historical?assetclass=stocks",
  "https://finance.yahoo.com/markets/stocks/articles/lumentum-sinks-10-marvell-blue-190635208.html",
  "https://247wallst.com/investing/2026/11/04/sandisk-slides-5-micron-and-western-digital-fall-3-as-election-and-memory-price-worries-weigh/",
  "https://www.cnbc.com/2026/11/03/acquisition-marvell-lumentum-acquisition-bofa-downgrade.html",
  "https://www.oilandgasmiddleeast.com/news/brent-hits-4-week-low-on-iran-talks",
  "https://open.er-api.com/v6/latest/USD"
 ]
}

with open(BASE + '/ledger-operaciones.jsonl', 'a') as f:
    f.write(json.dumps(nuevo, ensure_ascii=False) + '\n')

est = json.load(open(BASE + '/estado-juego.json'))

est['decisiones'].append({
 "fecha": "2026-11-04T22:35:00+01:00",
 "decision": "no_operar",
 "motivo": "58a pasada, 0 operaciones, CANDIDATAS_L NINGUNA. Dos velocidades tras las midterms: indices en verde (Dow +2,8%, Nasdaq +2,0%, Apple y Microsoft en maximos) y hardware de IA/memoria en rojo (SNDK -9%, MRVL -7,1%, WDC -6,8%, MU -5,7%) por el compromiso democratico de endurecer la construccion de data centers + la guia cauta de Kioxia. Efecto en el juego: WDC pierde el valle 332,00 (323,83) y MRVL el suyo (171,41 -> 159,80, dilucion del deal con Lumentum): el universo entero queda descendente/lateral/ascendente sin ningun L. UAA cruzo el gatillo del 35% de rango (5,77; REC_RANGO 65,0%) pero un dia antes de su Q2 FY27 y con upside al maximo de 3m reducido a +10,91% (<20%): doble motivo independiente de no entrada. Guardarrail externo activo (12a sesion): Brent 103,60, minas lapa en 4 petroleros el 29-30 oct, ataque de EEUU a Qeshm, OMI desaconsejando el transito y plan de dos dias en Doha sin acuerdo. Capital 1.000 EUR intactos.",
 "candidatas_ignoradas": ["UAA", "WDC", "MRVL"]
})

est['aprendizajes'].append({
 "fecha": "2026-11-04",
 "tema": "un evento politico puede mover el indice al alza y el universo del juego a la baja al mismo tiempo; y un gatillo cruzado la vispera del print no es un gatillo",
 "detalle": "(1) SECTOR vs INDICE: la victoria democratica en ambas camaras (midterms 03-nov) subio el Dow +2,8% (~1.400 pts), el S&P +1,7% y el Nasdaq +2,0% con Apple y Microsoft en maximos historicos, mientras el hardware de IA y la memoria caian por el compromiso de endurecer la construccion de data centers: SNDK -9%, LITE -10%, COHR -7%, STX -6,9%, WDC -6,8%, MU -5,7%, MRVL -7,1%. Leccion: 'el mercado sube' no dice nada del universo que vigila el juego; el guardarrail externo y el filtro de patron miran el ticker y su sector, no el indice. Fue el primer dia desde el 01-sep con CERO candidatas L (todo descendente, lateral o ascendente sin L). (2) GATILLO EN VISPERA DE PRINT: UAA llevaba 5 sesiones acercandose al 35% de rango (34,03% el 03-nov en 5,335) y lo cruzo el 04-nov cerrando en 5,77 (+8,15%); pero el mismo movimiento la saco de L-swing (ascendente, DD -9,84%) y dejo el upside al maximo de 3m en +10,91% (<20% exigido), con el Q2 FY27 al dia siguiente (06-nov, 06:55 ET). Es la 4a 'fuga por arriba' del experimento (tras FSLY 21 y 23-sep y el propio UAA) y la primera que se produce justo antes de su evento binario: el umbral se cumplio cuando la operacion ya era invalida por dos vias independientes. (3) UN L NO SOBREVIVE A UN EVENTO DE DILUCION: MRVL cierra 159,80 (-7,1%), por debajo de su valle de 30 dias 171,41, con -44,32% desde el maximo de 3m y REC_RANGO -10,04%, por la compra de Lumentum todo en acciones (dilucion ~50% del share count; BofA a Neutral con PT 225 desde 400) mas el castigo del sector data-center. Segunda confirmacion de la leccion del 29-oct: comprobar rumores de M&A/ampliaciones antes de dar por valido un L. (4) DISCIPLINA DE FUENTES: aparecio un articulo (businessday.ng) afirmando Brent a 72 USD y un MoU de Ormuz firmado 'desde el 18-jun'; contradice a todas las fuentes del dia (SPA, Oil & Gas Middle East, Grafa: Brent 103,60) y al propio scan, asi que se descarto como material obsoleto/erroneo en lugar de usarlo para levantar el guardarrail. (5) El informe semanal de bolsa de Dani del lunes 03-nov sigue sin localizar (23a pasada); la referencia de contexto del curso continua siendo la leccion 5 del 07-sep.",
 "fuente": "nasdaq.com/api snapshot 2026-11-04T22:31:55; Yahoo Finance/Schwab/247wallst 04-nov-2026; CNBC 03-nov-2026; SPA y Oil & Gas Middle East 03-04-nov-2026; open.er-api.com 04-nov-2026"
})

json.dump(est, open(BASE + '/estado-juego.json', 'w'), ensure_ascii=False, indent=2)
print('ok: ledger +1 linea, estado-juego con', len(est['decisiones']), 'decisiones y', len(est['aprendizajes']), 'aprendizajes')
