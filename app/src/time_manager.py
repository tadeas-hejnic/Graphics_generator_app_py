"""
Module for opereting with time.
"""
from datetime import datetime


def to_time(my_string):
    """Returns number of minutes to given time (just in one day)

    Args:
        my_string (str): Time in this type of format: "2023-02-12T13:00:00Z".

    Returns:
        int: Number of minutes.
    """

    hour = int(my_string[11]) * 10 + int(my_string[12])
    minute = int(my_string[14]) * 10 + int(my_string[15])
    return hour*60 + minute


def to_date(my_string):
    """Makes a date object from given string.

    Args:
        my_string (str): Time in this type of format: "2023-02-12T13:00:00Z".

    Returns:
        datetime: In this format: "%Y-%m-%d".
    """

    date_string = my_string[:10]
    return datetime.strptime(date_string, "%Y-%m-%d")


def date_without_nulls(date_str, max_len = 6):
    """Deletes unnecessary nulls from date string and cuts the date string.

    Args:
        date_str (str): Time in this type of format: "DD.MM.YYYY".
        max_len (int): Max length of the output time. Default is 6.

    Returns:
        str: Date without starting nulls.
    """

    output = str()
    for i in range(max_len):
        if i+1 == max_len:
            output += date_str[i:i+1]
            break
        if date_str[i] != "0" or date_str[i + 1] == "." or (i and date_str[i - 1] != "."):
            output += date_str[i]

    return output


def day_date_time(date_str):
    """Creates string in format DAY DD.MM. TIME.

    Args:
        date_str (str): Time in this type of format: "2023-02-12T13:00:00Z".

    Returns:
        str: String in right format.
    """

    day = get_czech_day(date_str)
    date = get_date(date_str)
    time = my_time_zone(date_str[11:16])
    return day + " " + date_without_nulls(date) + " " + time


def get_czech_day(date_str):
    """Decides which day of the week it is.

    Args:
        date_str (str): Time in this type of format: "2023-02-12T13:00:00Z".

    Returns:
        str: The name of the day.
    """

    name_of_days = [
        "pondělí",
        "úterý",
        "středa",
        "čtvrtek",
        "pátek",
        "sobota",
        "neděle"
    ]
    date = to_date(date_str)
    return name_of_days[date.weekday()]


def get_date(date_str):
    """Convert date into a format: "%d.%m.%Y".

    Args:
        date_str (str): Time in this type of format: "2023-02-12T13:00:00Z".

    Returns:
        str: Date in right format.
    """

    return to_date(date_str).strftime("%d.%m.%Y")

def my_time_zone(time_str):
    """Convert time to the right time zone.
    Adds one to hours. Can not convert the whole date.

    Args:
        date_str (str): Time in this type of format: "13:00".

    Raises:
        ValueError: If the change of time zone will change also the day. 

    Returns:
        str: Time in right time zone.
"""

    hours = int(time_str[:2])
    if hours >= 23:
        raise ValueError

    return str(hours + 1) + time_str[2:]
