from pymongo import MongoClient
from pymongo import MongoClient, InsertOne
import json

#Établir la connexion locale à la base de données
client = MongoClient('localhost', 27017)

#Accès direct à la base de données
db = client['ma_base_de_donnees']

#Création d'une collection
collection = db['cinemas']
def inserer_cinemas(cinemas):
    # Connexion à la base de données
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ma_base_de_donnees']
    collection = db['cinemas']

    # Préparation des opérations d'insertion
    operations = [InsertOne(cinema) for cinema in cinemas]

    # Exécution des opérations d'insertion
    try:
        result = collection.bulk_write(operations)
        print(f"{result.inserted_count} cinémas insérés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des cinémas : {e}")

def charger_donnees_json(fichier):
    with open(fichier, 'r') as f:
        donnees = json.load(f)
    return donnees

def affiche_cinemas ():
    nb_document = db.cinemas.count_documents({})
    print("nb_document :",nb_document)

def recherche_cinemas_150place(ville):
    result = db.cinemas.find({
    "adresse.ville": ville,
    "salles.capacite": {"$gt": 150}
    } )
    return list(result)

# Charger les données des cinémas à partir des fichiers JSON
cinema1_data = charger_donnees_json('data/cinema.json')
cinema2_data = charger_donnees_json('data/cinema2.json')
cinemas_data = charger_donnees_json("data/cinemas.json")
# Rassembler les données des cinémas dans une liste
cinemas_a_inserer = [cinemas_data]

# Appel de la fonction pour insérer les cinémas
#inserer_cinemas(cinemas_a_inserer)
inserer_cinemas(cinemas_a_inserer)
affiche_cinemas()
print (recherche_cinemas_150place("Paris"))