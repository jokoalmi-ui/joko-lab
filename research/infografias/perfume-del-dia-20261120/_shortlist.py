import json, sqlite3
p = "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20261120/candidatos.json"
d = json.load(open(p))
el = d["elegibles"]
# dia fresco 14.8 -> amaderado / especiado suave; banda frio o medio aceptables
cand = [x for x in el if x["banda"] in ("frio", "medio")]
cand.sort(key=lambda x: (x["compat"], -(x["dias_desde_uso"] if x["dias_desde_uso"] is not None else 9999)))
con = sqlite3.connect("/home/jokoalmi/perfume-ia/data/coleccion.db")
con.row_factory = sqlite3.Row
print(f"{'id':>5} {'compat':>6} {'banda':>5} {'idx':>6} {'dias':>5}  nombre / casa  [posee|decant]  sens")
for x in cand:
    det = con.execute("SELECT sensaciones, estela, longevidad_horas, concentracion FROM perfumes WHERE id=?", (x["id"],)).fetchone()
    print(f"{x['id']:>5} {x['compat']:>6} {str(x['banda']):>5} {x['indice']:>6.2f} {str(x['dias_desde_uso']):>5}  {x['nombre']} / {x['casa']}  [{x['posee']}|{x['decant']}]  {det['sensaciones'] if det else ''} | estela={det['estela'] if det else ''} long={det['longevidad_horas'] if det else ''} conc={det['concentracion'] if det else ''}")
print("total frio/medio elegibles:", len(cand))
