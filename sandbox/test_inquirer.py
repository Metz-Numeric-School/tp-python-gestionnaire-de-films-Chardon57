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

questions = [
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

answers = inquirer.prompt(questions, theme=GreenPassion())

pprint(answers["menu"])
# inquirer.prompt(q, theme=GreenPassion())