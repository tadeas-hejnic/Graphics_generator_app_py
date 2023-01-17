import pytest
from datetime import datetime
from src.time_manager import (
    to_time,
    date_without_nulls,
    get_czech_day,
    day_date_time,
    my_time_zone
)


@pytest.mark.parametrize(
    "time, expected",
    [
    ("2021-02-12T00:30:00Z", 30),
    ("2020-02-12T12:00:00Z", 720),
    ("1923-02-12T23:59:00Z", 1439),
    ("2023-02-12T09:00:00Z", 540),
    ("2021-04-12T10:05:00Z", 605),
    ("2023-02-02T00:01:00Z", 1),
    ])
def test_to_time(time, expected):
    assert to_time(time) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
    ("12.02.2002", "12.2.2002"),
    ("02.03.2012", "2.3.2012"),
    ("10.10.2000", "10.10.2000"),
    ("03.01.2011", "3.1.2011"),
    ("20.02.2020", "20.2.2020"),
    ])
def test_date_without_nulls(date, expected):
    assert date_without_nulls(date) == expected[:-4]
    assert date_without_nulls(date, 10) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
    ("2021-02-12T00:30:00Z", "pátek"),
    ("2020-02-12T12:00:00Z", "středa"),
    ("1923-02-12T22:00:00Z", "pondělí"),
    ("2023-02-12T09:00:00Z", "neděle"),
    ("2021-04-12T10:05:00Z", "pondělí"),
    ("2023-02-02T00:01:00Z", "čtvrtek"),
    ])
def test_get_czech_day(date, expected):
    assert get_czech_day(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
    ("2021-02-12T00:30:00Z", "pátek 12.2. 1:30"),
    ("2020-02-12T12:00:00Z", "středa 12.2. 13:00"),
    ("1923-02-12T22:00:00Z", "pondělí 12.2. 23:00"),
    ("2023-02-12T09:00:00Z", "neděle 12.2. 10:00"),
    ("2021-04-12T10:05:00Z", "pondělí 12.4. 11:05"),
    ("2023-02-02T00:01:00Z", "čtvrtek 2.2. 1:01"),
    ])
def test_day_date_time(date, expected):
    assert day_date_time(date) == expected


@pytest.mark.parametrize(
    "time, expected",
    [
    ("00:30", "1:30"),
    ("12:00", "13:00"),
    ("22:59", "23:59"),
    ("09:00", "10:00"),
    ("10:05", "11:05"),
    ("00:01", "1:01"),
    ])
def test_my_time_zone(time, expected):
    assert my_time_zone(time) == expected


@pytest.mark.parametrize(
    "time",
    [
    ("23:30"),
    ("23:00"),
    ("23:59")
    ])
def test_my_time_zone_exception(time):
    with pytest.raises(ValueError):
        my_time_zone(time)
