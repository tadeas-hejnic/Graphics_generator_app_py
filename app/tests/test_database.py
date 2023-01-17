import pytest
import json
from src.database import InviteDatabase
from src.constants import (
    TEST_PLAYER_DATABASE_PATH,
    TEST_LAST_USED_DATABASE_PATH
)


@pytest.fixture
def default_db():
    data = {'team1': {'player1': False, 'player2': False}, 
            'team2': {'player3': False, 'player4': False}}
    return InviteDatabase(TEST_PLAYER_DATABASE_PATH, TEST_LAST_USED_DATABASE_PATH, data)


@pytest.fixture
def load_db():
    return InviteDatabase(TEST_PLAYER_DATABASE_PATH, TEST_LAST_USED_DATABASE_PATH)


def test_InviteDatabase_init_1():
    db = InviteDatabase(TEST_PLAYER_DATABASE_PATH, TEST_LAST_USED_DATABASE_PATH)
    assert isinstance(db.database, dict)
    assert db.gui is None


@pytest.mark.parametrize(
    "data",
    [
    {'team1': {'player1': False, 'player2': False}, 
     'team2': {'player3': False, 'player4': False}},
    {'team1': {'player1': True, 'player2': False}, 
     'team2': {'player3': False, 'player4': False}},
    {},
    ])
def test_InviteDatabase_init_2(data):
    db = InviteDatabase(TEST_PLAYER_DATABASE_PATH, TEST_LAST_USED_DATABASE_PATH, data)
    assert isinstance(db.database, dict)
    assert db.database == data
    assert db.gui is None


def test_InviteDatabase_get(load_db):
    """Test if InviteDatabase.get() returns correct players.
    """

    players = load_db.get(["a_tym", "b_tym"])
    assert isinstance(players, list)
    assert len(players) == 2
    assert players[0][0] in ["a_tym", "b_tym"]
    assert players[1][0] in ["a_tym", "b_tym"]
    assert players[0][1] in load_db.database[players[0][0]].keys()
    assert players[1][1] in load_db.database[players[1][0]].keys()
    players = load_db.get(["a_tym"])
    assert len(players) == 1
    assert players[0][0] == "a_tym"
    assert players[0][1] in load_db.database[players[0][0]].keys()


@pytest.mark.parametrize(
    "data, team_name",
    [
    ({"team1": {"player1": False, "player2": False}, 
     "team2": {"player3": False, "player4": False}}, {"team1" : "player1"}),
    ({"team1": {"player1": True, "player2": False}, 
     "team2": {"player3": False, "player4": False}}, {"team1" : "player1", "team1" : "player2"}),
    ({"team1": {"player1": True, "player2": False}, 
     "team2": {"player3": False, "player4": False}}, {"team2" : "player4"}),
    ])
def test_InviteDatabase_update(data, team_name):
    """Test if InviteDatabase.update() updates the database correctly.
    """

    db = InviteDatabase(TEST_PLAYER_DATABASE_PATH, TEST_LAST_USED_DATABASE_PATH, data)
    assert db.database == data
    for team, player in team_name.items():
        data[team][player] = True

    db.update(team_name)
    assert db.database == data
