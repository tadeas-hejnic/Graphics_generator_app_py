import pytest
from src.api import (
    login,
    get_matches,
    only_relevant
)


def test_login():
    assert isinstance(login(), dict)


MY_LEAGUES = [
    "2-liga-mladsi-dorostenci-zapad",
    "1-liga-starsi-dorostenci",
    "2-liga-muzi-jvc",
    "stredoceska-spolecna-regionalni-liga-muzu"
]


@pytest.mark.parametrize(
    "league",
    [
    "2-liga-mladsi-dorostenci-zapad",
    "1-liga-starsi-dorostenci",
    "2-liga-muzi-jvc",
    "stredoceska-spolecna-regionalni-liga-muzu"
    ])
def test_get_matches_correct_leagues(league):
    result = get_matches(league)
    assert isinstance(result, list)
    for match in result:
        assert isinstance(match, dict)


@pytest.mark.parametrize(
    "league",
    [
    "1-liga-mladsi-dorostenci",
    "2-liga-starsi-dorostenci-cechy",
    "1-liga-muzi"
    ])
def test_get_matches_incorrect_leagues(league):
    assert get_matches(league) == None


@pytest.mark.parametrize(
    "league",
    [
    "2-liga-mladsi-dorostenci-zapad",
    "1-liga-starsi-dorostenci",
    "2-liga-muzi-jvc",
    "stredoceska-spolecna-regionalni-liga-muzu"
    ])
def test_only_relevant_correct_leagues(league):
    result = only_relevant(get_matches(league))

    assert isinstance(result, list)
    for match in result:
        assert len(match) == 9


@pytest.mark.parametrize(
    "league",
    [
    "1-liga-mladsi-dorostenci",
    "2-liga-starsi-dorostenci-cechy",
    "1-liga-muzi"
    ])
def test_only_relevant_incorrect_leagues(league):
    assert only_relevant(get_matches(league)) == None
