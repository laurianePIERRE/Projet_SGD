from pymongo import MongoClient, InsertOne
from datetime import datetime
import json

# Établir la connexion globale à la base de données
client = MongoClient('localhost', 27017)
db = client['ma_base_de_donnees']
cinemas_collection = db['cinemas']
films_collection = db['films']

def charger_donnees_json(fichier):
    with open(fichier, 'r') as f:
        donnees = json.load(f)
    return donnees

def inserer_cinemas(cinemas):
    operations = [InsertOne(cinema) for cinema in cinemas]
    try:
        result = cinemas_collection.bulk_write(operations)
        print(f"{result.inserted_count} cinémas insérés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des cinémas : {e}")

def inserer_films(films):
    operations = [InsertOne(film) for film in films]
    try:
        result = films_collection.bulk_write(operations)
        print(f"{result.inserted_count} films insérés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des films : {e}")

def calculer_ajout_moyenne_note():
    films = films_collection.find()
    for film in films:
        commentaires = film.get('commentaires', [])
        if commentaires:
            somme_des_notes = sum([commentaire['note'] for commentaire in commentaires])
            nombre_de_notes = len(commentaires)
            note_moyenne = somme_des_notes / nombre_de_notes if nombre_de_notes > 0 else 0
            films_collection.update_one({'_id': film['_id']}, {'$set': {'note_moyenne': note_moyenne}})
            print(f"Moyenne ajoutée pour {film['titre']}: {note_moyenne}")
        else:
            print(f"Aucun commentaire trouvé pour {film['titre']}.")

def affiche_cinemas():
    nb_document = cinemas_collection.count_documents({})
    print("Nombre de documents dans 'cinemas':", nb_document)

def affiche_films():
    films = list(films_collection.find())
    for film in films :

        print("Documents dans 'films':", films)

def recherche_cinemas_150place(ville):
    result = cinemas_collection.find({
        "adresse.ville": ville,
        "salles.capacite": {"$gt": 150}
    })
    return list(result)

def recherche_des_film_sorti_apres_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    result = films_collection.find({"date_sortie": {"$gt": date_obj}})
    return list(result)
def supprimer_tous_les_films():
    # Supprimer tous les documents de la collection 'films'
    result = films_collection.delete_many({})
    print(f"{result.deleted_count} films ont été supprimés.")

def recherche_de_commentaire(nom_utilisateur):
    result = films_collection.find({"commentaires.auteur.email": nom_utilisateur })

    return list(result)

def bon_fim_action():
    result = films_collection.find({"categories": "Action", "note_moyenne": {"$gt": 4.0}})
    result = list(result)
    print ("result :",result)
    noms_des_films = [film["titre"] for film in result]
    print ("Voici les films des films d'action avec une note moyenne supérieure à 4 ", noms_des_films)
# Charger les données des cinémas à partir des fichiers JSON
cinema1_data = charger_donnees_json('data/cinema.json')
cinema2_data = charger_donnees_json('data/cinema2.json')
cinemas_data = charger_donnees_json("data/cinemas.json")
# Rassembler les données des cinémas dans une liste
cinemas_a_inserer = [cinemas_data]

# Appel de la fonction pour insérer les cinémas
#inserer_cinemas(cinemas_a_inserer)
#inserer_cinemas(cinemas_a_inserer)
affiche_cinemas()
print (recherche_cinemas_150place("Paris"))

films = charger_donnees_json("data/film.json")
supprimer_tous_les_films()
inserer_films(films)
calculer_ajout_moyenne_note()
affiche_films()
print (recherche_des_film_sorti_apres_date("2023-01-01"))
print("comm")
print(recherche_de_commentaire("john@example.com"))
print(bon_fim_action())