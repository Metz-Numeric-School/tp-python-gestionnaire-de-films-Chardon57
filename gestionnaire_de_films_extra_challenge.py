import csv
import os
import json
import inquirer, rich
from inquirer.themes import GreenPassion
from rich.console import Console
from rich.table import Table

ERROR_MESSAGE_INVALID = "Erreur : entrée invalide."
ERROR_MESSAGE_NOT_EXISTS = "Erreur : Fichier inexistant ou pas encore créé"
ERROR_MESSAGE_EMPTY = "Erreur : La liste de films est vide !"
ERROR_MESSAGE_NOT_FOUND = "Erreur : entrée introuvable."
FILE_NAME = "movies.csv"
JSON_FILE_NAME = "movies.json"
FIELD_NAMES = ["title","release_year","genre","is_seen"]

def get_csv_datas(path: str) -> list:
    """Extrait les données du fichier CSV et renvoie une liste de dictionnaires. Reçoit
    le chemin du fichier CSV en paramètre"""
    data = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)
    return data

def write_csv_datas(path: str, rows: list):
    """Ecrit dans le fichier les données passées en entrée (*datas*) sous forme de liste.
    Reçoit également le chemin du fichier CSV en paramètre."""
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames= FIELD_NAMES)
        writer.writeheader()
        writer.writerows(rows)

def list_movies(path: str):
    """Affiche le contenu de la collection de films (fichier CSV). REçoit le chemin
    du fichier en paramètre. Si le fichier n'existe pas, affiche un message d'erreur."""
    film_list = get_csv_datas(path)
    if len(film_list) > 0:
        table = Table(title="Liste des films")

        table.add_column("Titre", justify="center", style="white")
        table.add_column("Année", justify="center", style="white")
        table.add_column("Genre", justify="center", style="white")
        table.add_column("Visionné", justify="center", style="white")
        
        for i, film in enumerate(film_list):
    
            table.add_row(
                f"{film["title"]}",
                f"{film["release_year"]}",
                f"{film["genre"]}",
                f"{"Oui" if film["is_seen"] == "True" else "Non"}"
            )

        console = Console()
        console.print(table)

    else:
        print(ERROR_MESSAGE_EMPTY)

def add_movie(path: str):
    """Permet d'ajouter un film à la liste des films. Si le fichier est absent il 
    sera créé, sinon la nouvelle entrée sera ajoutée. Reçoit en paramètre le chemin 
    du fichier à modifier"""
    film_list = get_csv_datas(path)
    title = input("Entrez le titre du film à ajouter : ").lower().strip()
    while True:
        release_year = input(f"En quelle année \"{title.capitalize()}\" est sorti ? ")
        if release_year.isdigit() and int(release_year) > 1000:
            release_year = int(release_year)
            break
        print(ERROR_MESSAGE_INVALID)
    genre = input(f"Quel est le genre de \"{title.capitalize()} ({release_year})\" ? ").lower().strip()
    is_seen = input(f"Avez vous visionné \"{title.capitalize()} ({release_year})\" (o/n) ? ") == "o"
    new_entry = {
        "title": title,
        "release_year": release_year,
        "genre": genre,
        "is_seen": is_seen
    }
    film_list.append(new_entry)
    write_csv_datas(path, film_list)
    print("Entrée ajoutée.\n")

def search_movie(path: str, search_prompt:str) -> dict | None:
    """Recherche un film dans la liste à partir de sont titre. Reçoit en paramètre
    le chemin du fichier CSV et le titre du film. renvoie les données du film trouvé
    sous forme de dictionnaire, sinon renvoie *None*"""
    film_list = get_csv_datas(path)
    if len(film_list) > 0:
        for film in film_list:
            if film["title"] == search_prompt.lower().strip():
                return film
    return None

def display_search_result(path: str):
    """Affiche le résultat de la recherche d'un film. Si le film n'est pas
    trouvé, affiche un message d'erreur adapté"""
    search_pattern = input("Quel film recherchez vous : ")
    result = search_movie(path, search_pattern)
    if result is None:
        print(ERROR_MESSAGE_NOT_FOUND)
    else:
        print(f"Titre : {result["title"]}\nAnnée : {result["release_year"]}\nGenre : {result["genre"]}\nVisionné : {"Oui" if result["is_seen"] == "True" else "Non"}")

def delete_movie(path: str):
    """Recherche le film demandé puis le supprime de la liste des films
    avant d'écraser le CSV avec le nouveau contenu. **Le fichier CSV précédent
    est remplacé !**"""
    movie_to_del = input("Quel film voulez vous supprimer ? ")
    film_list = get_csv_datas(path)
    
    del_entry = search_movie(path, movie_to_del)
    
    if del_entry is None:
        print(ERROR_MESSAGE_NOT_FOUND)
    
    film_list.remove(del_entry)
    write_csv_datas(path, film_list)
    

def mark_movie_as_seen(path: str):
    """Recherche le film demandé puis modifie la clé *is_seen* en la passant
    de *False* à *True*"""
    seen_movie = input("Quel film avez vous regardé ? ")
    film_list = get_csv_datas(path)
    if len(film_list) > 0:
        for film in film_list:
            if film["title"] == seen_movie.lower().strip():
               film["is_seen"] = True
               write_csv_datas(path, film_list)
               break
        print(ERROR_MESSAGE_NOT_FOUND)
    print(ERROR_MESSAGE_EMPTY)
        
def export_json(csv_path: str, json_path: str):
    film_list = get_csv_datas(csv_path)
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(film_list, json_file, ensure_ascii= False, indent= 2)

def save_stats_in_json(csv_path: str, json_path: str):
    film_list = get_csv_datas(csv_path)
    nb_film = len(film_list)
    nb_viewed = 0
    nb_not_viewed = 0
    genre_list = []
    for film in film_list:
        genre_list.append(film["genre"])
        if film["is_seen"] == "True":
            nb_viewed += 1
        else:
            nb_not_viewed += 1
    single_genres = set(genre_list)
    genre_count =[]
    for unique_genre in single_genres:
        genre_score = genre_list.count(unique_genre)
        genre_count.append({"genre": unique_genre, "score": genre_score})

    def get_score(item: dict) -> int:
        return item["score"]

    sorted_genres = sorted(genre_count, key=get_score, reverse=True)
    json_stats = {
        "total_film_number": nb_film,
        "nb_viewed_films": nb_viewed,
        "nb_not_viewed": nb_not_viewed,
        "top_genres": sorted_genres[0:3]
    }
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_stats, json_file, ensure_ascii= False, indent= 2)


def menu():
    """Affiche le menu principal et exécute les demandes de l'utilisateur."""
    print("Bienvenue dans le gestionnaire de films\n")
    while True:
        options = [
            inquirer.List(
                name="menu",
                message="",
                choices=[
                    ("Ajouter un film", "ajouter"),
                    ("Afficher la liste des films", "liste"),
                    ("Rechercher un film", "rechercher"),
                    ("Supprimer un film", "supprimer"),
                    ("Marquer un film comme vu", "marquer"),
                    ("Quitter", "sortir")
                ]
            )
        ]

        action_choice = inquirer.prompt(options, theme=GreenPassion())

        match action_choice["menu"]:
            case "ajouter":
                add_movie(FILE_NAME)
                export_json(FILE_NAME, JSON_FILE_NAME)
                save_stats_in_json(FILE_NAME, JSON_FILE_NAME)
            case "liste":
                list_movies(FILE_NAME)
            case "rechercher":
                display_search_result(FILE_NAME)
            case "supprimer":
                delete_movie(FILE_NAME)
                export_json(FILE_NAME, JSON_FILE_NAME)
                save_stats_in_json(FILE_NAME, JSON_FILE_NAME)
            case "marquer":
                mark_movie_as_seen(FILE_NAME)
                export_json(FILE_NAME, JSON_FILE_NAME)
                save_stats_in_json(FILE_NAME, JSON_FILE_NAME)
            case "sortir":
                exit()
            case _:
                print(ERROR_MESSAGE_INVALID)
                # print(f"'menu' returned : {action_choice["menu"]}")
        

if __name__ == "__main__":
    menu()