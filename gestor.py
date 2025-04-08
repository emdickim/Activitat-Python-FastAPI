# gestor.py
import os
import json

# Fitxer on guardarem els alumnes
NOM_FITXER = "alumnes.json"
llista_alumnes = []
id_actual = 1  # ID autoincremental

### Funcions ##################################################

def carregar_dades():
    global llista_alumnes, id_actual
    try:
        with open(NOM_FITXER, 'r', encoding='utf-8') as f:
            llista_alumnes = json.load(f)
            # Busquem el següent ID disponible
            if llista_alumnes:
                id_actual = max(alumne["id"] for alumne in llista_alumnes) + 1
    except:
        llista_alumnes = []

def desar_dades():
    with open(NOM_FITXER, 'w', encoding='utf-8') as f:
        json.dump(llista_alumnes, f, indent=4)

def mostrar_alumnes():
    for alumne in llista_alumnes:
        print(f"{alumne['id']} - {alumne['nom']} {alumne['cognom']}")

def afegir_alumne():
    global id_actual
    nom = input("Nom: ")
    cognom = input("Cognom: ")
    dia = int(input("Dia naixement: "))
    mes = int(input("Mes naixement: "))
    any = int(input("Any naixement: "))
    email = input("Email: ")
    feina = input("Treballa? (s/n): ").lower() == "s"
    curs = input("Curs: ")

    alumne = {
        "id": id_actual,
        "nom": nom,
        "cognom": cognom,
        "data": {"dia": dia, "mes": mes, "any": any},
        "email": email,
        "feina": feina,
        "curs": curs
    }
    llista_alumnes.append(alumne)
    id_actual += 1
    print("Alumne afegit correctament!")

def veure_alumne():
    id_buscat = int(input("ID de l'alumne: "))
    for alumne in llista_alumnes:
        if alumne["id"] == id_buscat:
            print(json.dumps(alumne, indent=4))
            return
    print("Alumne no trobat.")

def esborrar_alumne():
    id_buscat = int(input("ID de l'alumne a esborrar: "))
    for i, alumne in enumerate(llista_alumnes):
        if alumne["id"] == id_buscat:
            del llista_alumnes[i]
            print("Alumne eliminat correctament.")
            return
    print("No s'ha trobat l'alumne.")

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Gestió d'Alumnes - Institut TIC BCN")
    print("1. Mostrar alumnes")
    print("2. Afegir alumne")
    print("3. Veure alumne")
    print("4. Esborrar alumne")
    print("5. Desar fitxer")
    print("6. Llegir fitxer")
    print("0. Sortir")
    return input("Tria una opció: ")

### Programa principal #########################################
carregar_dades()

while True:
    match menu():
        case "1":
            mostrar_alumnes(); input("Prem ENTER per continuar...")
        case "2":
            afegir_alumne(); input("Prem ENTER per continuar...")
        case "3":
            veure_alumne(); input("Prem ENTER per continuar...")
        case "4":
            esborrar_alumne(); input("Prem ENTER per continuar...")
        case "5":
            desar_dades(); input("Fitxer desat. Prem ENTER per continuar...")
        case "6":
            carregar_dades(); input("Fitxer carregat. Prem ENTER per continuar...")
        case "0":
            print("Adeu!")
            break
        case _:
            print("Opció no vàlida.")
