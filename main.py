# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Nom del fitxer on es desaran les dades dels alumnes
NOM_FITXER = "alumnes.json"
# Llista que contindrà els alumnes
llista_alumnes = [{}]
# Identificador únic per a cada alumne
id_actual = 1

# Model per representar la data de naixement
class DataNaixement(BaseModel):
    dia: int
    mes: int
    any: int

# Model per representar un alumne
class Alumne(BaseModel):
    nom: str
    cognom: str
    data: DataNaixement
    email: str
    feina: bool
    curs: str

# Funció per carregar els alumnes des d’un fitxer JSON
def carregar():
    global llista_alumnes, id_actual
    try:
        with open(NOM_FITXER, "r", encoding="utf-8") as f:
            llista_alumnes.clear()
            llista_alumnes.extend(json.load(f))
            if llista_alumnes:
                # Assignar el següent id basant-se en l’últim alumne
                id_actual = max(a["id"] for a in llista_alumnes) + 1
    except:
        # Si el fitxer no existeix o hi ha error, es neteja la llista
        llista_alumnes.clear()

# Funció per desar els alumnes en un fitxer JSON
def desar():
    with open(NOM_FITXER, "w", encoding="utf-8") as f:
        json.dump(llista_alumnes, f, indent=4)

# Carreguem les dades dels alumnes quan s’inicia el servidor
carregar()

# Ruta principal per comprovar que el servidor funciona
@app.get("/")
def inici():
    return "Institut TIC de Barcelona"

# Ruta per obtenir el nombre total d’alumnes
@app.get("/alumnes/")
def total_alumnes():
    return {"total": len(llista_alumnes)}

# Ruta per obtenir un alumne pel seu id
@app.get("/id/{numero}")
def get_alumne(numero: int):
    for alumne in llista_alumnes:
        if alumne["id"] == numero:
            return alumne
    return "Alumne no trobat"

# Ruta per eliminar un alumne pel seu id
@app.delete("/del/{numero}")
def eliminar_alumne(numero: int):
    for i, alumne in enumerate(llista_alumnes):
        if alumne["id"] == numero:
            del llista_alumnes[i]
            desar()
            return {"msg": "Alumne eliminat"}
    return "Alumne no trobat"

# Ruta per afegir un nou alumne
@app.post("/alumne/")
def afegir_alumne(alumne: Alumne):
    global id_actual
    alumne_dict = alumne.dict()
    alumne_dict["id"] = id_actual
    id_actual += 1
    llista_alumnes.append(alumne_dict)
    desar()
    return {"msg": "Alumne afegit", "id": alumne_dict["id"]}
