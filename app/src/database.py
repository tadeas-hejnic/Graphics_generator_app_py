"""
Module for my intern database for players
"""

import json
import random
from pathlib import Path
from src.constants import (
    PLAYER_DATABASE_PATH,
    LAST_USED_DATABASE_PATH
)
"""
from constants import (
    PLAYER_DATABASE_PATH,
    LAST_USED_DATABASE_PATH
)
"""


def make_dict(str_players):
    """Helper function just for me to make the default dictionary from rosters.

    Args:
        str_players (list(tuple(str, str))): First in tuple is the name of category,
            second one is roster where players are divided by ", ".

    Returns:
        Str: dictionary in string, keys are category names and values are dictionaries
            where keys are names and values are by default everywhere False.
    """

    output = []
    output.append("{ {")

    for category in str_players:
        output.append("\"" + category[0] + "\" : { ")
        players = category[1].split(", ")
        for p in players:
            player_str = "\"" + p + "\"" + " : " + "False, "
            output.append(player_str)
        output.append("}, ")

    output.append("} }")
    return "".join(output)


class InviteDatabase:
    """Database for recording who has been already on invite.

    Attributes:
        database (dict(dict)): Keys are categories, values 
            are dictionaries where keys are names and values are bools.
        gui (DialogWindow): Dialog window in main GUI page.
    """
    def __init__(self, save_path = PLAYER_DATABASE_PATH, last_used_path = LAST_USED_DATABASE_PATH,
                 data = None, gui = None):
        self.database_path = save_path
        self.last_used_path = last_used_path
        self.database = dict()
        if data is None:
            with open(PLAYER_DATABASE_PATH, "r", encoding='utf-8') as load_file:
                data = load_file.read()
                self.database = json.loads(data)
                # self.database = json.load(load_file)
        else:
            self.database = data

        self.gui = gui

    def save(self):
        """Saves the database in .json format.
        """

        with open(self.database_path, "w", encoding='utf-8') as save_file:
            json.dump(self.database, save_file)

    def get(self, teams):
        """Randomly choose players of given teams.

        Args:
            teams (list): From these teams are chosen the players.
        """

        list_of_players = []
        for team in teams:
            while True:
                name, boolean = random.choice(list(self.database[team].items()))
                path = Path("../", "Elements/", "Players/", team + "/", name + ".png")
                if team == "b_tym":
                    path = Path("../", "Elements/", "Players/", "a_tym/", name + ".png") 
                if not boolean and path.is_file() and self.not_duplicate((team, name), list_of_players):
                    break
            list_of_players.append((team, name))

        self.save_last_used(list_of_players)
        return list_of_players

    def update(self, team_name = None):
        """Set value to True for given teams and names.

        Args:
            team_name (dict): Key is a team and value is the name of the player.
        """

        if not team_name:
            with open(LAST_USED_DATABASE_PATH, "r", encoding='utf-8') as load_file:
                team_name = json.load(load_file)

        for team, player in team_name.items():
            self.database[team][player] = True
            if "a_tym" == team and player in self.database["b_tym"]:
                self.database["b_tym"][player] = True
            elif "b_tym" == team and player in self.database["a_tym"]:
                self.database["a_tym"][player] = True

        if self.gui:
            self.gui.print_text("Database was updated.")
        self.save()

    def reset(self, team = None):
        """Set all players to False

        Args:
            team (str): Name of the team that is reset. No given team means: reset all teams.
        """

        if team is None:
            for roster in self.database.keys():
                for player in self.database[roster].keys():
                    self.database[roster][player] = False
        else:
            for player in self.database[team].keys():
                self.database[team][player] = False
        if self.gui:
            self.gui.print_text("Database was reset.")
        self.save()

    def save_last_used(self, list_of_players):
        """Saves the list of players to last used database.

        Args:
            list_of_players (list(tuple)): List of players to be saved.
                Tuple consist of team and player name.
        """

        new_dict = {}
        for team, name in list_of_players:
            new_dict[team] = name

        with open(self.last_used_path, "w", encoding='utf-8') as save_file:
            json.dump(new_dict, save_file)

    def not_duplicate(self, name_team, list_of_players):
        """Checks if in the player is already in the list.

        Args:
            name_team (tuple): Team and player name.
            list_of_players (list(tuple)): List of players to be saved.
                Tuple consist of team and player name.

        Returns:
            bool : True if there is no duplicate. Otherwise False.
        """

        if list_of_players == []:
            return True
        if name_team[1] == "a_tym" or name_team[1] == "b_tym":
            for name, _ in list_of_players:
                if name == name_team[0]:
                    return False
            return True

        return not name_team in list_of_players

"""
inpu = [("mladsi_dorost", "Garay Jaroslav, Handl Jan, Hájek Lukáš, Holčák Václav, Horák Martin, Horčičák Daniel, Charouzd Richard, Kroc Tomáš, Petráň František, Pičman David, Pitkevič Aleksandr, Planý Adam, Planý David, Rusek Jakub, Šubrt Richard, Taussig Samuel, Tischer Lukáš, Turek Roman, Valach Filip, Vejvar Lukáš, Voříšek Lukáš, Vrbata František, Zelený Pavel"),
        ("starsi_dorost", "Carboch Michal, Havel Jakub, Jeřábek Vojtěch, Jura Matyáš, Krista Jan, Pektor Patrik, Roubal Jakub, Slavík Vojtěch, Špaček Jaroslav, Trapek Matěj, Vácha Vojtěch, Viktora Jan, Vilimovský Michael"),
        ("a_tym", "Benešovský Michal, Bossanyi Daniel, Cenigr Jan, Francl Pavel, Hájek Michal, Hejnic Tadeáš, Koula Vojtěch, Kroupa Bohdan, Kubec Jiří, Kundrata Petr, Kürti Oliver, Najman Matouš, Polák Michal, Seidl Radek, Slavík Jakub, Šubrt Tomáš, Taitl Václav, Všetečka Dominik"),
        ("b_tym", "Hájek Michal, Koula Vojtěch, Kroupa Bohdan, Kubec Jiří, Kürti Oliver, Polák Michal, Slavík Jakub, Šubrt Tomáš, Taitl Václav, Vintrych Marek, Všetečka Dominik")
]

i = InviteDatabase(data = make_dict(inpu))
i.save()
"""
