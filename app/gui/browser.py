"""
Module for gui using web browser.

"""

import webbrowser
from unidecode import unidecode


def search_for_logo(team_name):
    """This function opens browser and search for logo of given team.

    Args:
        team_name (Str): Name of the team.
    """
    url = "https://www.google.com/search?q=" + unidecode(team_name) + " logo png"
    webbrowser.open_new(url)
