#!/usr/bin/env python3
"""consolidar-medicion.py — une la medicion cruda + la repeticion del 2,6B y
recalcula los veredictos con el valor CORRECTO de la cuenta (360,00 EUR).

Ojo: en la 1a pasada el script llevaba un esperado erroneo (370) -> los campos
"acierto" de CALCULAR en el JSON crudo estan mal. Aqui se recalculan desde la
salida literal de cada modelo. El crudo no se reescribe.
"""
import json, pathlib

lec = pathlib.Path(__file__).parent
crudo = json.load(open(lec / "medicion-tamano-20260918.json", encoding="utf-8"))
rep = json.load(open(lec / "medicion-tamano-2,6b-repeticion.json", encoding="utf-8"))

def veredicto_calc(salida):
    """Acierto si el unico numero devuelto es 360 (con o sin decimales)."""
    s = (salida or "").strip().replace("€", "").replace(" ", "")
    s = s.rstrip(".").replace(",00", "").replace(".00", "")
    return s in ("360",)

TABLA = {
    "2,6B": {"clasificar": "5/5", "extraer": "FALLO", "calcular": "OK",
             "nota_extraer": "no llega a responder: agota el presupuesto razonando (2 pasadas)",
             "s_clas": 18.2, "s_extrae": 31.6, "s_calc": 6.5,
             "modelo": "lfm2.5-2.6b"},
    "8B": {"clasificar": "5/5", "extraer": "OK", "calcular": "FALLO",
           "nota_extraer": "responde el importe en 0,3 s",
           "s_clas": 13.8, "s_extrae": 0.3, "s_calc": 0.2,
           "modelo": "granite-4.1-8b"},
    "35B": {"clasificar": "5/5", "extraer": "OK", "calcular": "OK",
            "nota_extraer": "responde el importe en 48,8 s",
            "s_clas": 119.6, "s_extrae": 48.8, "s_calc": 49.1,
            "modelo": "qwen3.6-35b-a3b-mtp"},
}

# comprobacion: recalcular desde las salidas guardadas
comprobacion = {}
for fila in crudo["modelos"]:
    t = fila["tamano"]
    comprobacion[t] = {
        "clasificar": f"{fila['clasificar']['aciertos']}/5",
        "extraer": "OK" if fila["extraer"]["acierto"] else "FALLO",
        "calcular": "OK" if veredicto_calc(fila["calcular"]["salida"]) else "FALLO",
        "calcular_salida": fila["calcular"]["salida"][:40],
    }
comprobacion["2,6B"]["extraer"] = "FALLO"  # tambien en la repeticion con 1600 tokens
comprobacion["2,6B"]["calcular"] = "OK" if veredicto_calc(rep["calcular"]["salida"]) else "FALLO"

coincide = all(comprobacion[t][k] == TABLA[t][k] for t in TABLA for k in ("clasificar", "extraer", "calcular"))

con = {
    "tema": "Leccion 0-B: cuanto importa el tamano del modelo en 3 usos tipicos",
    "fecha": crudo["fecha"],
    "api": crudo["api"],
    "diseno": {
        "modelos": {t: TABLA[t]["modelo"] for t in TABLA},
        "tareas": ["clasificar 5 resenas (POSITIVA/NEGATIVA)",
                   "extraer el importe del transporte de una factura (12,00)",
                   "calcular el total: 4 x 89,50 - 10,00 + 12,00 = 360,00"],
        "control": "mismo prompt y temperatura 0 para los tres",
    },
    "tabla": TABLA,
    "recalculo_desde_salidas_crudas": comprobacion,
    "coincide_con_tabla": coincide,
    "correccion_metodologica": [
        "El esperado de la cuenta estaba mal en la 1a pasada (370); el valor correcto es 360,00. Verificado a mano: 4x89,50=358; 358-10=348; 348+12=360.",
        "Por eso el JSON crudo marca 'calcular: no' en los tres: los veredictos de aqui salen de recalcular sobre la salida literal.",
        "El 2,6B necesito una 2a pasada con 1600 tokens (la 1a acabo en finish_reason=length); con ese presupuesto sigue sin entregar el importe.",
    ],
    "hallazgo_operativo": ("Con el VLM glm-4.6v-flash residente en LM Studio, los modelos 8B y 35B no cargaban "
                           "(llama-server exited before becoming healthy, exitCode=1). Tras 'lms unload' cargaron los dos."),
    "ficheros_crudos": ["medicion-tamano-20260918.json", "medicion-tamano-2,6b-repeticion.json",
                        "medicion-tamano-parcial.json"],
}
out = lec / "medicion-tamano-consolidado.json"
out.write_text(json.dumps(con, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"coincide_con_tabla: {coincide}")
print(f"{'tamano':>6s} | clasificar | extraer              | calcular | segundos")
for t in ("2,6B", "8B", "35B"):
    f = TABLA[t]
    print(f"{t:>6s} | {f['clasificar']:>10s} | {f['extraer']:>7s} {f['nota_extraer'][:26]:26s} | "
          f"{f['calcular']:>8s} | {f['s_clas']}+{f['s_extrae']}+{f['s_calc']} = "
          f"{round(f['s_clas']+f['s_extrae']+f['s_calc'],1)}s")
print("JSON:", out)
