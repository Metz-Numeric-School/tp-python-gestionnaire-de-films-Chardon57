import os
import re
import sys
from pprint import pprint
from inquirer.themes import GreenPassion

sys.path.append(os.path.realpath("."))
import inquirer  # noqa


def phone_validation(answers, current):
    if not re.match(r"\+?\d[\d ]+\d", current):
        raise inquirer.errors.ValidationError("", reason="I don't like your phone number!")

    return True


# questions = [
#     inquirer.Text("name", message="What's your name?"),
#     inquirer.Text("surname", message="What's your surname, {name}?"),
#     inquirer.Text(
#         "phone",
#         message="What's your phone number",
#         validate=phone_validation,
#     ),
# ]

# questions = [
#             inquirer.List(
#                 name="menu",
#                 message="",
#                 choices=[
#                     ("Ajouter un film", "ajouter"),
#                     ("Afficher la liste des films", "liste"),
#                     ("Rechercher un film", "rechercher"),
#                     ("Supprimer un film", "supprimer"),
#                     ("Marquer un film comme vu", "marquer"),
#                     ("Quitter", "sortir")
#                 ]
#             )
#         ]

# title = input("Entrez le titre du film à ajouter : ")
# while True:
#     release_year = input(f"En quelle année \"{title.capitalize()}\" est sorti ? ")
#     if release_year.isdigit() and int(release_year) > 1000:
#         release_year = int(release_year)
#         break
#     print("erreur")
# genre = input(f"Quel est le genre de \"{title.capitalize()} ({release_year})\" ? ").lower().strip()
# is_seen = input(f"Avez vous visionné \"{title.capitalize()} ({release_year})\" (o/n) ? ") == "o"
# new_entry = {
#     "title": title,
#     "release_year": release_year,
#     "genre": genre,
#     "is_seen": is_seen
# }

def year_validation(answers, current):
    if not current.isdigit() or int(current) < 1000:
         raise inquirer.errors.ValidationError("", reason="Entrez une année valide")

    return True

questions = [
    inquirer.Text("title", message="Entrez le titre du film"),
    inquirer.Text(
        "release_year",
        message="En quelle année \"{title}\" est sorti ? ",
        validate=year_validation,
    ),
    inquirer.Text("genre", message="Quel est le genre de \"{title}\" ? "),
    inquirer.List(name="is_seen",
                  message="Avez vous visionné \"{title}\" ? ",
                  choices=["Oui","Non"],
                  default="Non"
            )
    ]


answers = inquirer.prompt(questions, theme=GreenPassion())

# new_entry = {
#     "title": answers["title"],
#     "release_year": answers["release_year"],
#     "genre": answers["genre"],
#     "is_seen": answers["is_seen"]
# }

print(answers)
# pprint(new_entry)
# inquirer.prompt(q, theme=GreenPassion())