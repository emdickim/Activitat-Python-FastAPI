# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

NOM_FITXER = "alumnes.json"
llista_alumnes = [{}]
id_actual = 1

# Model per rebre un alumne via POST
class DataNaixement(BaseModel):
    dia: int
    mes: int
    any: int

class Alumne(BaseModel):
    nom: str
    cognom: str
    data: DataNaixement
    email: str
    feina: bool
    curs: str

# Carregar alumnes des del fitxer
def carregar():
    global llista_alumnes, id_actual
    try:
        with open(NOM_FITXER, "r", encoding="utf-8") as f:
            llista_alumnes.clear()
            llista_alumnes.extend(json.load(f))
            if llista_alumnes:
                id_actual = max(a["id"] for a in llista_alumnes) + 1
    except:
        llista_alumnes.clear()

def desar():
    with open(NOM_FITXER, "w", encoding="utf-8") as f:
        json.dump(llista_alumnes, f, indent=4)

# Cridem la càrrega inicial
carregar()

@app.get("/")
def inici():
    return "Institut TIC de Barcelona"

@app.get("/alumnes/")
def total_alumnes():
    return {"total": len(llista_alumnes)}

@app.get("/id/{numero}")
def get_alumne(numero: int):
    for alumne in llista_alumnes:
        if alumne["id"] == numero:
            return alumne
    return "Alumne no trobat"

@app.delete("/del/{numero}")
def eliminar_alumne(numero: int):
    for i, alumne in enumerate(llista_alumnes):
        if alumne["id"] == numero:
            del llista_alumnes[i]
            desar()
            return {"msg": "Alumne eliminat"}
    return "Alumne no trobat"

@app.post("/alumne/")
def afegir_alumne(alumne: Alumne):
    global id_actual
    alumne_dict = alumne.dict()
    alumne_dict["id"] = id_actual
    id_actual += 1
    llista_alumnes.append(alumne_dict)
    desar()
    return {"msg": "Alumne afegit", "id": alumne_dict["id"]}
