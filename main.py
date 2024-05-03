from pymongo import MongoClient
from bson.code import Code
from datetime import datetime

import pymongo
import json
# Se connecter à la base de données MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ma_base_de_donnees"]
collection = db["films"]

# Charger les données depuis le fichier JSON
with open("data/films.json") as f:
    data = json.load(f)

# Insérer les données dans la collection MongoDB
if not collection.find_one({"_id": data["_id"]}):
    # Insérer les données dans la collection MongoDB
    collection.insert_one(data)
    print("Film inséré avec succès.")
else:
    print("Le film avec cet ID existe déjà dans la collection. Aucune insertion n'a été effectuée.")
    
    
    
    
    

collectionCinema = db["cinemas"]

# Charger les données depuis le fichier JSON
with open("data/cinemas.json") as f:
    data = json.load(f)

# Insérer les données dans la collectionCinema MongoDB
if not collectionCinema.find_one({"_id": data["_id"]}):
    # Insérer les données dans la collectionCinema MongoDB
    collectionCinema.insert_one(data)
    print("Cinema inséré avec succès.")
else:
    print("Le film avec cet ID existe déjà dans la collectionCinema. Aucune insertion n'a été effectuée.")

# Appel de la fonction pour afficher les films par date


    

def afficher_menu():
    print("\n-----------------------------------------------------------------")
    print("|                         Projet                                |")
    print("|                 Selectionné votre option:                     |")
    print("-----------------------------------------------------------------")
    print("|                                                               |")
    print("| 0.   Suppression des collections                              |")
    print("|                                                               |")
    print("| 1.   Actualité du mois                                        |")
    print("| 2.   Top 3 des films                                          |")
    print("| 3.   Liste des films par cinemas et nombre d'entrée           |")
    print("| 4.   Commentaires                                             |")
    print("| 5.   Cinema près de chez vous                                 |")
    print("| 6.   Notes selon le type de film                              |")
    print("| 7.   Vos acteurs                                              |")
    print("| 8.   Insertion de données                                     |")
    print("|                                                               |")
    print("| 9.   Exit                                                     |")
    print("-----------------------------------------------------------------")
#________________________________________________ Choix 0 _______________________________________________________________________________________   
def supprimer_contenu_films():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    collection = db["films"]
    collectionCinemas = db["cinemas"]

    try:
        # Supprimer tous les documents de la collection
        result = collection.delete_many({})
        print(f"{result.deleted_count} documents ont été supprimés de la collection 'films'.")
        resultCinema = collectionCinemas.delete_many({})
        print(f"{resultCinema.deleted_count} documents ont été supprimés de la collection 'cinemas'.")
    except Exception as e:
        print("Une erreur est survenue lors de la suppression du contenu de la collection 'films' :", e)
        print("Une erreur est survenue lors de la suppression du contenu de la collection 'cinemas' :", e)
#________________________________________________ Choix 1 _______________________________________________________________________________________

def actu_du_mois():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    collection = db["films"]

    # Faire une requête pour récupérer les films avec la date de sortie correspondante
    films = collection.find({"date_sortie.annee": "2024", "date_sortie.mois": "05"})

    # Afficher les films
    print(f"\nListe des films sortis ce mois :")
    for film in films:
        print(film["titre"])


#________________________________________________ Choix 2 _______________________________________________________________________________________
def top_3_films_mieux_notes():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    collection = db["films"]

    # Faire une requête pour trouver les 10 films les mieux notés
    top_films = collection.find().sort("note_moyenne", -1).limit(3)

    # Afficher les 10 films les mieux notés
    print("Les 3 films les mieux notés :")
    for film in top_films:
        print(film["titre"], "-", "Note moyenne:", film["note_moyenne"])
#________________________________________________ Choix 3 _______________________________________________________________________________________
def afficher_noms_cinemas():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    cinemas_collection = db["cinemas"]
    films_collection = db["films"]  # Ajout pour récupérer les films liés à chaque cinéma

    # Récupérer tous les documents de la collection "cinemas"
    cinemas = cinemas_collection.find()

    # Afficher les noms des cinémas et les films liés à chaque cinéma
    for cinema in cinemas:
        print(f"\n{cinema['nom']}, \nVille : {cinema['adresse']['ville']}")
        
        # Récupérer les films liés à ce cinéma
        films = films_collection.find({'cinema_id': cinema['_id']})
        if films:
            print("Films :")
            for film in films:
                print(f"- {film['titre']}")
        else:
            print("Aucun film trouvé pour ce cinéma.")





#________________________________________________ Choix 4 _______________________________________________________________________________________
def afficher_films_par_titre():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    films_collection = db["films"]
    # Demander le nom du film à l'utilisateur
    titre = input("Entrez le titre du film : ")
    try:
        # Construire la requête d'agrégation
        pipeline = [
            {"$match": {"titre": titre}},
            {"$group": {"_id": "$titre", "total_entrees": {"$sum": "$nombre_entrees"}}}
        ]

        # Exécuter la requête d'agrégation
        result = list(films_collection.aggregate(pipeline))

        # Afficher le total d'entrées pour les films ayant le même titre
        if result:
            print(f"Total des entrées pour les films avec le titre '{titre}' : {result[0]['total_entrees']}")
        else:
            print(f"Aucun film trouvé avec le titre '{titre}'.")
    except Exception as e:
        print("Une erreur est survenue lors de la recherche des films :", e)



#________________________________________________ Choix 5 _______________________________________________________________________________________

def calculer_et_mettre_a_jour_notes_moyennes():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["nom_de_votre_base_de_donnees"]
    films_collection = db["films"]

    # Parcourir tous les films
    for film in films_collection.find():
        commentaires = film.get("commentaires", [])
        if commentaires:
            # Calculer la moyenne des notes dans les commentaires
            moyenne_notes = sum(commentaire["note"] for commentaire in commentaires) / len(commentaires)
            # Mettre à jour le champ "note_moyenne" pour ce film
            films_collection.update_one({"_id": film["_id"]}, {"$set": {"note_moyenne": moyenne_notes}})
            print(f"Moyenne des notes mise à jour pour '{film['titre']}': {moyenne_notes}")
        else:
            # Si aucun commentaire, mettre la note moyenne à 0
            films_collection.update_one({"_id": film["_id"]}, {"$set": {"note_moyenne": 0}})
            print(f"Aucun commentaire trouvé pour '{film['titre']}', la note moyenne est mise à 0.")
def afficher_moyenne_titre_commentaires_films():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]  
    films_collection = db["films"]  

    # Récupérer tous les documents de la collection "films"
    films = films_collection.find()

    # Afficher le titre, la moyenne et les commentaires de chaque film
    for film in films:
        print(f"Titre : {film['titre']}")
        if 'note_moyenne' in film:
            print(f"Moyenne : {film['note_moyenne']}")
        else:
            print("Moyenne : Non disponible")
        
        commentaires = film.get('commentaires', [])
        if commentaires:
            print("Commentaires :")
            for commentaire in commentaires:
                print(f"- {commentaire['contenu']} ({commentaire['note']})")
        else:
            print("Aucun commentaire.")
        print()


def ajouter_commentaire():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    films_collection = db["films"]

    # Demander le titre du film à l'utilisateur
    titre_film = input("Entrez le titre du film : ")

    # Rechercher le film par son titre
    film = films_collection.find_one({"titre": titre_film})

    if film:
        # Demander à l'utilisateur s'il souhaite ajouter un commentaire
        reponse = input("Voulez-vous ajouter un commentaire pour ce film ? (oui/non) : ")

        if reponse.lower() == "oui":
            # Demander le contenu du commentaire à l'utilisateur
            texte_commentaire = input("Entrez le contenu du commentaire : ")

            # Demander la note du commentaire à l'utilisateur
            note_commentaire = int(input("Entrez la note du commentaire (sur 5) : "))

            # Ajouter le commentaire au film
            commentaire = {
                "contenu": texte_commentaire,
                "note": note_commentaire
            }
            films_collection.update_one({"_id": film["_id"]}, {"$push": {"commentaires": commentaire}})
            print("Commentaire ajouté avec succès.")
        elif reponse.lower() == "non":
            print("Ajout de commentaire annulé.")
        else:
            print("Réponse non valide. Veuillez répondre 'oui' ou 'non'.")
    else:
        print("Film non trouvé.")
#________________________________________________ Choix 6 _______________________________________________________________________________________


def afficher_villes_cinemas():
    # Se connecter à la base de données MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    cinemas_collection = db["cinemas"]

    # Récupérer toutes les villes des cinémas
    villes = cinemas_collection.distinct("adresse.ville")

    # Afficher toutes les villes
    print("Villes ayant un cinéma :")
    for ville in villes:
        print(ville)

    # Demander à l'utilisateur d'entrer le nom de la ville de son choix
    ville_choisie = input("Entrez le nom de la ville de votre choix : ")

    # Afficher les cinémas de la ville choisie
    cinemas_ville = cinemas_collection.find({"adresse.ville": ville_choisie})

    print(f"Cinémas à {ville_choisie} :")
    for cinema in cinemas_ville:
        print(f"Nom : {cinema['nom']}")




#________________________________________________ Choix 7 _______________________________________________________________________________________
def calculer_moyenne_notes_par_categorie():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    films_collection = db["films"]

    try:
        # Construire la requête d'agrégation
        pipeline = [
            {"$group": {"_id": "$type", "moyenne_notes": {"$avg": "$note_moyenne"}}}
        ]

        # Exécuter la requête d'agrégation
        result = list(films_collection.aggregate(pipeline))

        # Afficher la moyenne des notes par catégorie de film
        if result:
            print("Moyenne des notes par catégorie de film :")
            for categorie in result:
                print(f"{categorie['_id']} : {categorie['moyenne_notes']}")
        else:
            print("Aucun film trouvé.")
    except Exception as e:
        print("Une erreur est survenue lors du calcul de la moyenne des notes par catégorie :", e)


#________________________________________________ Choix 8 _______________________________________________________________________________________

def afficher_liste_acteurs():
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]
    films_collection = db["films"]

    # Récupérer la liste des acteurs
    acteurs = set()
    films = films_collection.find()
    for film in films:
        acteurs.update(film.get("acteurs", []))

    # Afficher la liste des acteurs
    print("Liste des acteurs :\n")
    for idx, acteur in enumerate(acteurs, 1):
        print(f"{idx}. {acteur}")

    # Demander à l'utilisateur de choisir un acteur
    choix_acteur = input("\nEntrez le numéro de l'acteur pour voir ses films : ")

    # Vérifier si l'entrée est un nombre valide
    if choix_acteur.isdigit():
        idx_acteur = int(choix_acteur) - 1
        if 0 <= idx_acteur < len(acteurs):
            acteur_selectionne = list(acteurs)[idx_acteur]
            rechercher_films_par_acteur(acteur_selectionne)
        else:
            print("Numéro d'acteur invalide.")
    else:
        print("Veuillez entrer un numéro valide.")

def rechercher_films_par_acteur(nom_acteur):
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]

    films_collection = db["films"]
    # Rechercher les films dans lesquels l'acteur joue
    films = films_collection.find({"acteurs": {"$in": [nom_acteur]}})

    if films:
        print(f"Informations sur les films avec {nom_acteur} :\n")
        for film in films:
            print(f"Titre : {film['titre']}")
            print(f"Année de sortie : {film['date_sortie']}")
            print(f"Acteurs : {', '.join(film['acteurs'])}")
            print(f"Réalisateur(s) : {', '.join(film['realisateurs'])}\n")

    else:
        print(f"Aucun film trouvé pour l'acteur {nom_acteur}.")




#________________________________________________ Choix 9 _______________________________________________________________________________________

def ajouter_film(film_data):
    # Connect to the MongoDB database

    try:
    # Insérer les données des films dans la collection
        collection.insert_many([film_data, film_data1, film_data2, film_data3])
    except pymongo.errors.DuplicateKeyError:
        # If the _id already exists, update the existing document
        collection.update_one({"_id": film_data["_id"]}, {"$set": film_data}, upsert=True)
        print(f"Film avec l'ID {film_data['_id']} mis à jour.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du film : {e}")

# Example film data
film_data = {
    "_id": "filmID1",
    "titre": "Nouveau film",
    "type": "Action",
    "date_sortie": { "jour": "08", "mois": "11", "annee": "2024" },
    "realisateurs": ["Réalisateur 1", "Réalisateur 2"],
    "acteurs": ["Acteur 1", "Acteur 2"],
    "duree_minutes": 120,
    "langue_originale": "Français",
    "limite_age": 12,
    "seances": [
        {
            "date_heure": "2024-02-19T18:00:00Z",
            "salles": [{ "salle_id": 1, "capacite": 170 }],
            "prix": {"etudiant": 8, "senior": 10, "enfant": 6, "adulte": 12},
        }
    ],
    "nombre_entrees": 50,
    "note_moyenne": 5,
    "nombre_votes": 10,
    "cinema_id": "ID3Cine",
    "commentaire":[
    {
      "auteur": "Nom Utilisateur 8",
      "date": "2024-05-08",
      "contenu": "Je m'attendais à mieux.",
      "note": 2
    }]

}
film_data1 = {
    "_id": "filmID2",
    "titre": "Toto et le parc",
    "type": "Jeunesse",
    "date_sortie": { "jour": "08", "mois": "11", "annee": "2024" },
    "realisateurs": ["Réalisateur 1", "Réalisateur 2"],
    "acteurs": ["Marion Cotillard", "Gérard Depardieu"],
    "duree_minutes": 120,
    "langue_originale": "Français",
    "limite_age": 12,
    "seances": [
        {
            "date_heure": "2024-02-19T18:00:00Z",
            "salles": [{ "salle_id": 1, "capacite": 170 }],
        }
    ],
    "nombre_entrees": 8502,
    "note_moyenne": 4,
    "nombre_votes": 200,
    "cinema_id": "ID2Cine",
    "commentaire":[
    {
      "auteur": "Nom Utilisateur 10",
      "date": "2024-05-10",
      "contenu": "Je me suis ennuyé du début à la fin.",
      "note": 1
    },
    {
      "auteur": "Nom Utilisateur 11",
      "date": "2024-05-11",
      "contenu": "À voir absolument !",
      "note": 5
    }]

}
film_data2 = {
    "_id": "filmID3",
    "titre": "Nouveau film",
    "type": "Action",
    "date_sortie": { "jour": "08", "mois": "11", "annee": "2024" },
    "realisateurs": ["Réalisateur 1", "Réalisateur 2"],
    "acteurs": ["Marion Cotillard", "Omar Sy"],
    "duree_minutes": 120,
    "langue_originale": "Français",
    "limite_age": 12,
    "seances": [
        {
            "date_heure": "2024-02-19T18:00:00Z",
            "salles": [{ "salle_id": 1, "capacite": 170 }],
        }
    ],
    "nombre_entrees": 0,
    "note_moyenne": 4,
    "nombre_votes": 0,
    "commentaires": [
    {
      "auteur": "Nom Utilisateur 1",
      "date": "2024-05-01",
      "contenu": "Ce film était incroyable !",
      "note": 5
    },
    {
      "auteur": "Nom Utilisateur 2",
      "date": "2024-05-02",
      "contenu": "Je n'ai pas aimé ce film.",
      "note": 2
    },
    {
      "auteur": "Nom Utilisateur 3",
      "date": "2024-05-03",
      "contenu": "Une performance d'acteur exceptionnelle.",
      "note": 4
    }
  ]

}
film_data3 = {
    "_id": "filmID4",
    "titre": "Les animaux fantastique",
    "type": "Fantastique",
    "date_sortie": { "jour": "08", "mois": "11", "annee": "2024" },
    "realisateurs": ["Réalisateur 1", "Réalisateur 2"],
    "acteurs": ["Eddie Redmayne", "Johnny Deep"],
    "duree_minutes": 120,
    "langue_originale": "Français",
    "seances": [
        {
            "date_heure": "2024-02-19T18:00:00Z",
            "salles": [{ "salle_id": 1, "capacite": 170 }],
        }
    ],
    "nombre_entrees": 10536,
    "note_moyenne": 4,
    "nombre_votes": 502,
    "cinema_id": "ID4Cine",
    "commentaires": [
    {
      "auteur": "Nom Utilisateur 6",
      "date": "2024-05-06",
      "contenu": "Ce film m'a vraiment touché.",
      "note": 4
    },
    {
      "auteur": "Nom Utilisateur 7",
      "date": "2024-05-07",
      "contenu": "Pas mal, mais prévisible.",
      "note": 3
    }
  ]

}
film_data3 = {
    "_id": "filmID5",
    "titre": "Scary Movie",
    "type": "Horreur",
    "date_sortie": { "jour": "08", "mois": "11", "annee": "2024" },
    "realisateurs": ["Réalisateur 1", "Réalisateur 2"],
    "acteurs": ["Anna Faris", "Shawn Wayans"],
    "duree_minutes": 120,
    "langue_originale": "Français",
    "limite_age": 16,
    "seances": [
        {
            "date_heure": "2024-02-19T18:00:00Z",
            "salles": [{ "salle_id": 1, "capacite": 170 }],
        }
    ],
    "nombre_entrees": 296,
    "note_moyenne": 3,
    "nombre_votes": 26,
    "cinema_id": "ID1Cine",
    "commentaires": [
    {
      "auteur": "Nom Utilisateur 4",
      "date": "2024-05-04",
      "contenu": "Une histoire captivante !",
      "note": 4
    },
    {
      "auteur": "Nom Utilisateur 5",
      "date": "2024-05-05",
      "contenu": "Les effets spéciaux étaient impressionnants.",
      "note": 5
    }
  ]

}

def afficher_info_film(film_data):
    print("Informations du film:")
    print(f"Titre: {film_data.get('titre')}")
    print(f"Type: {film_data.get('type')}")
    print(f"Réalisateur(s): {', '.join(film_data.get('realisateurs', []))}")
    print(f"Acteur(s): {', '.join(film_data.get('acteurs', []))}")
    print(f"Durée (minutes): {film_data.get('duree_minutes')}")
    print(f"Langue originale: {film_data.get('langue_originale')}")
    print(f"Limite d'âge: {film_data.get('limite_age')}")
    print("Séances:")
    for seance in film_data.get('seances', []):
        print(f"  Date et heure: {seance.get('date_heure')}")
        print(f"  Salle ID: {seance.get('salle_id')}")
        print("  Prix:")
        prix = seance.get('prix', {})
        for categorie, valeur in prix.items():
            print(f"    {categorie}: {valeur}")
    print(f"Nombre d'entrées: {film_data.get('nombre_entrees')}")
    print(f"Note moyenne: {film_data.get('note_moyenne')}")
    print(f"Nombre de votes: {film_data.get('nombre_votes')}")
    
    
#------------------------------------------------------------------------------------------------
def creer_nouveau_cinema(cinema_data_list):
    # Se connecter à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ma_base_de_donnees"]  # Remplacez "ma_base_de_donnees" par le nom de votre base de données
    collection = db["cinemas"]  # Remplacez "cinemas" par le nom de votre collection de cinémas

    try:
        # Insérer les données des cinémas dans la collection
        result = collection.insert_many(cinema_data_list)
        print(f"{len(result.inserted_ids)} cinémas ont été créés avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création des cinémas : {e}")

# Liste des données de cinéma

# Appel de la fonction pour créer les cinémas

#creer_nouveau_cinema(cinema_data_list)
# Exemple de données de cinéma
cinema_data = {
    "_id": "ID1Cine",
    "nom": "Pathé Montparnasse",
    "adresse": {
        "ville": "Paris",
        "code_postal": "75014",
        "numero_rue": 123
    },
    "tarifs": {
        "etudiant": 6,
        "senior": 9,
        "enfant": 6,
        "adulte": 10
    },
    "options": {
        "vente_popcorn": True,
        "vente_bonbons": False
    }
}

cinema_data2 = {
    "_id": "ID2Cine",
    "nom": "UGC Ciné Cité La Défense",
    "adresse": {
        "ville": "Puteaux",
        "code_postal": "92800",
        "numero_rue": 15
    },
    "tarifs": {
        "etudiant": 7,
        "senior": 10,
        "enfant": 6,
        "adulte": 12
    },
    "options": {
        "vente_popcorn": True,
        "vente_bonbons": True
    }
}

cinema_data3 = {
    "_id": "ID3Cine",
    "nom": "Gaumont Opéra",
    "adresse": {
        "ville": "Paris",
        "code_postal": "75009",
        "numero_rue": 2
    },
    "tarifs": {
        "etudiant": 8,
        "senior": 11,
        "enfant": 7,
        "adulte": 13
    },
    "options": {
        "vente_popcorn": True,
        "vente_bonbons": True
    }
}

cinema_data4 = {
    "_id": "ID4Cine",
    "nom": "Pathé Belle Épine",
    "adresse": {
        "ville": "Thiais",
        "code_postal": "94320",
        "numero_rue": 2
    },
    "tarifs": {
        "etudiant": 6,
        "senior": 9,
        "enfant": 6,
        "adulte": 11
    },
    "options": {
        "vente_popcorn": True,
        "vente_bonbons": False
    }
}


def main():
    # Charger les données des cinémas à partir des fichiers JSON
    # Afficher le menu
    afficher_menu()
    # Gestion du choix de l'utilisateur
    exit_choice = None  # Initialisation de la variable exit_choice

    while exit_choice != 10:  # Sortie de la boucle lorsque exit_choice est égal à 11
        
        choice = int(input("\nEnter votre choix: "))
        # Vérification si le choix est valide
        
        if choice == 0:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                      Suppression des collections                    |")
            print("------------------------------------------------------------------------\n")
            supprimer_contenu_films()
        elif choice == 1:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                        Actualité du mois                             |")
            print("------------------------------------------------------------------------\n")
            actu_du_mois()
        elif choice == 2:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                        Le top 3 des films les                        |")
            print("|                             mieux notés                              |")
            print("------------------------------------------------------------------------\n")
            top_3_films_mieux_notes()
        elif choice == 3:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                      Liste des films par cinemas                     |")
            print("------------------------------------------------------------------------\n")
            afficher_noms_cinemas()
            print("\n------------------------------------------------------------------------")
            print("|                      Nombre d'entrée pour un film                    |")
            print("------------------------------------------------------------------------\n")
            afficher_films_par_titre()
            afficher_menu()
        elif choice == 4:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                                Commentaires                          |")
            print("------------------------------------------------------------------------\n")
            calculer_et_mettre_a_jour_notes_moyennes()
            afficher_moyenne_titre_commentaires_films()
            ajouter_commentaire()
            calculer_et_mettre_a_jour_notes_moyennes()
            afficher_moyenne_titre_commentaires_films()
        elif choice == 5:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                     Cinema près de chez vous                         |")
            print("------------------------------------------------------------------------\n")
            afficher_villes_cinemas()
        elif choice == 6:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                      Notes selon le type de film                     |")
            print("------------------------------------------------------------------------\n")
            calculer_moyenne_notes_par_categorie()
        elif choice == 7:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                            Vos acteurs                               |")
            print("------------------------------------------------------------------------\n")
            afficher_liste_acteurs()
        elif choice == 8:
            afficher_menu()
            print("\n------------------------------------------------------------------------")
            print("|                            Insertion de Films                        |")
            print("------------------------------------------------------------------------\n")
            ajouter_film(film_data)
            afficher_info_film(film_data)
            print("\n------------------------------------------------------------------------")
            print("|                            Insertion de Cinemas                      |")
            print("------------------------------------------------------------------------\n")
            cinemas_data_list = [cinema_data, cinema_data2, cinema_data3, cinema_data4]
            creer_nouveau_cinema(cinemas_data_list)
        elif choice == 9:
            print("Exiting...")
            return  




if __name__ == "__main__":
    main()