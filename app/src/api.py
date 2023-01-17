"""
Functions for communication with API server.
Call league_sunday() to get a list of dictionaries with relevant data to each match played on the next League Sunday.
Call weekend_result() to get a list of dictionaries with relevant data to each match played last week.
"""

import requests
import json
from datetime import (
    datetime,
    timedelta
)
from src.time_manager import (
    to_date,
    to_time
)
from src.constants import (
    MY_TEAM,
    MY_LEAGUES
)
"""
from time_manager import (
    to_date,
    to_time
)
from constants import (
    MY_TEAM,
    MY_LEAGUES
)
"""

# API endpoints
# /api/partner/competitions/{competitionSlug}/my-matches
# /api/partner/competitions/{competitionSlug}/teams (unused)
# /api/partner/competitions


def login():
    """Manages the login to API server.

    Returns:
        dict : Authorization token.
    """

    itemdto = {
        "userName": "jakub.ransdorf@hazena-uvaly.cz",
        "password":"APIhu44",
    }
    login_token = requests.post("https://is.handball.cz/api/partner/login", json=itemdto, timeout=10)
    token = json.loads(login_token.text)
    return {"Authorization": "Bearer " + token["access_token"]}


def get_matches(league):
    """Finds all matches of given league.

    Parameters:
            league (str): Name of the league.

    Returns:
        list : List of matches (dict).
    """

    header = login()
    url = "https://is.handball.cz/api/partner/competitions/" + league + "/my-matches"
    result = requests.get(url, headers=header, timeout=10)
    if result.status_code != 200:
        print("API CONNECT FAIL")
        return None

    return json.loads(result.text)


def get_leagues():
    """Returns all leagues playing my_team.

    Returns:
        list : List of leagues.
    """

    header = login()
    url = "https://is.handball.cz/api/partner/competitions/"
    result = requests.get(url, headers=header, timeout=10)
    if result.status_code != 200:
        print("API CONNECT FAIL")
        return None

    return json.loads(result.text)


def played(data):
    """Filters data and eturns match, played up to seven days ago.

    Returns:
        dict : Dictionary with API data.
    """

    today = datetime.today()
    for match in data:
        if MY_TEAM in match["homeTeamName"] or MY_TEAM in match["guestTeamName"]:
            match_start_date = to_date(match["matchStart"])
            if today + timedelta(days=7) > match_start_date > today:
                return match
    return None


def plays_this_week(data):
    """Gets API data of some league.
    Returns home match of my_team playing in 15 days

    Returns:
        dict : Dictionary with API data.
    """

    today = datetime.today()
    for match in data:
        if MY_TEAM in match["homeTeamName"]:
            match_start_date = to_date(match["matchStart"])
            if today + timedelta(days=15) > match_start_date > today:
                return match
    return None


def only_relevant(data):
    """Removes all irrevelant data from .json dictionary

    Parameters:
        data (dict): Huge dictionary.

    Returns:
        dict : New dictionary only with relevant keys.
    """

    if not data:
        return None

    new_data = []
    for match in data:
        tmp = {
            "homeTeamName" : match["homeTeamName"],
            "guestTeamName" : match["guestTeamName"],
            "homeTeamScore" : match["homeTeamScore"],
            "guestTeamScore" : match["guestTeamScore"],
            "matchStart" : match["matchStart"],
            "competitionName" : match["competitionName"],
            "sportFieldName" : match["sportFieldName"],
            "homeTeamClubPhotoUrl" : match["homeTeamClubPhotoUrl"],
            "guestTeamClubPhotoUrl" : match["guestTeamClubPhotoUrl"],
            }
        new_data.append(tmp)
    return new_data


def league_sunday():
    """Gets data about all macthes and sorts it by match start.

    Returns:
        list (dict) : Each dictionary in list is one match playes my team as "home team".
    """

    schedule = []
    for league in MY_LEAGUES:
        matches = plays_this_week(get_matches(league))
        if matches is not None:
            schedule.append(matches)

    schedule = only_relevant(schedule)
    schedule.sort(key=lambda d: to_time(d["matchStart"]))
    return schedule

"""
def weekend_result():
    # Returns list of match dictionaries played up to 7 days ago
    results = []
    for league in MY_LEAGUES:
        match = played(get_matches(league))
        if match is not None:
            results.append(match)

    return only_relevant(results)
"""
