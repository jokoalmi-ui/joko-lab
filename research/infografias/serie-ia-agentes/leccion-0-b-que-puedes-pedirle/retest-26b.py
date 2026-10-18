#!/usr/bin/env python3
"""retest-26b.py — repite las 3 tareas del 2,6B con presupuesto de tokens suficiente.
En la 1a pasada su 'extraer' acabo con finish_reason=length (gasto todo el
presupuesto en el razonamiento antes de escribir la respuesta), no por fallo
de capacidad. Se repite con 1600 tokens para comparar en igualdad de condiciones.
"""
import json, pathlib, datetime, importlib.util, sys

lec = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("m", lec / "medicion-tamano.py")
sys.argv = ["x"]
src = (lec / "medicion-tamano.py").read_text(encoding="utf-8").split("res = {")[0]
ns = {}
exec(compile(src, "medicion-tamano.py", "exec"), ns)

llama, etiquetas, igual = ns["llama"], ns["etiquetas"], ns["igual"]
RESENAS, ESPERADO_CLAS = ns["RESENAS"], ns["ESPERADO_CLAS"]
PROMPT_CLAS, PROMPT_EXTRAE, PROMPT_CALCULA = ns["PROMPT_CLAS"], ns["PROMPT_EXTRAE"], ns["PROMPT_CALCULA"]
ESPERADO_EXTRAE, ESPERADO_CALCULA = ns["ESPERADO_EXTRAE"], ns["ESPERADO_CALCULA"]

out = {"modelo": "lfm2.5-2.6b", "tamano": "2,6B", "motivo": "repeticion con presupuesto de tokens suficiente",
       "max_tokens": {"clas": 900, "extrae": 1600, "calc": 1600}, "fecha": datetime.date.today().isoformat()}

txt, dt, fr, rz = llama("lfm2.5-2.6b", PROMPT_CLAS, 900)
ets = etiquetas(txt)
ac = sum(1 for e, x in zip(ESPERADO_CLAS, ets) if e == x)
out["clasificar"] = {"aciertos": ac, "n": 5, "segundos": dt, "finish_reason": fr, "salida": txt[:900]}
print(f"clasificar {ac}/5 en {dt}s (fin={fr})", flush=True)

txt2, dt2, fr2, rz2 = llama("lfm2.5-2.6b", PROMPT_EXTRAE, 1600)
out["extraer"] = {"acierto": igual(txt2, ESPERADO_EXTRAE), "segundos": dt2, "finish_reason": fr2,
                  "salida": txt2[:900], "razonamiento": rz2[:400]}
print(f"extraer {'OK' if out['extraer']['acierto'] else 'FALLO'} en {dt2}s (fin={fr2}) -> {txt2[:120]!r}", flush=True)

txt3, dt3, fr3, rz3 = llama("lfm2.5-2.6b", PROMPT_CALCULA, 1600)
out["calcular"] = {"acierto": igual(txt3, ESPERADO_CALCULA), "segundos": dt3, "finish_reason": fr3,
                   "salida": txt3[:900], "razonamiento": rz3[:400]}
print(f"calcular {'OK' if out['calcular']['acierto'] else 'FALLO'} en {dt3}s (fin={fr3}) -> {txt3[:120]!r}", flush=True)

out["segundos_total"] = round(dt + dt2 + dt3, 1)
p = lec / "medicion-tamano-2,6b-repeticion.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("JSON:", p)
