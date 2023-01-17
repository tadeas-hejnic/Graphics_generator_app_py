"""Module for all constants using in this app"""

from pathlib import Path


"""BASIC CONSTANTS"""
# ----- my team -----
MY_TEAM = "TJ Sokol Úvaly"

# ---- my leagues -----
MY_LEAGUES = [
    "2-liga-mladsi-dorostenci-zapad",
    "1-liga-starsi-dorostenci",
    "2-liga-muzi-jvc",
    "stredoceska-spolecna-regionalni-liga-muzu"
]

LEAGUE_NAMES_DICT = {
    "2. liga mladší dorostenci - západ" : "2. liga mladší dorostenci",
    "1. liga starší dorostenci" : "1. liga starší dorostenci",
    "2. liga muži JVČ" : "2. liga muži JVČ",
    "Středočeská společná regionální liga mužů" : "společná region. liga mužů"
}

# ----- base url -----
BASE_URL = "https://is.handball.cz"

# ----- image sizes -----
STORIES_SIZE = (1080, 1920)
RESULT_SIZE = (1080, 1350)
RESULT_PHOTO_WIDTH = 1300
INVITE_SIZE = (1080, 1920, 4)
RECTANGLE_SIZE = (39, 292, 4)

# ----- fonts -----
DIN_FONT = r"./Fonts/DIN Condensed Bold.ttf"
REMOVER_FONT = r"./Fonts/Remover.ttf"

# ----- my colors -----
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
MY_WHITE = (247, 247, 247, 255)
DARK_RED = (187, 39, 27)
MY_BLACK = (0, 0, 0)
LIGHT_BLACK = (6, 6, 6, 255)
YELLOW = (255, 189, 30, 255)


"""STORIES CONSTANTS"""
# ----- stories path to elements -----
UNDER_LOGO_PATH = Path("../", "Elements/", "Stories/", "under_logo.png")
VS_PATH = Path("../", "Elements/", "Stories/", "vs.png")
TMP_IMG_PATH = Path("../", "Pictures/", "tmp.png")
HOME_LOGO_PATH = Path("../", "Elements/", "Logos/", "homeTeam.png")
GUEST_LOGO_PATH = Path("../", "Elements/", "Logos/", "guestTeam.png")
LOGO_PATH_STR = "../" + "Elements/" + "Logos/"
STORIES_SAVE_PATH_STR = "../" + "Pictures/"

# ----- paths to elements (other stories) -----
BLACK_BG_PATH = Path("../", "Elements/", "Stories/", "black_element.png")
RED_MID_PATH = Path("../", "Elements/", "Stories/", "red_element.png")
X_ELEMENT_PATH = Path("../", "Elements/", "Stories/", "x_element.png")
TMP_STORIES_PATH = Path("../", "Pictures/", "tmp_stories.png")
BG_STORIES_PATH = Path("../", "Elements/", "Photos/", "bg.png")
MID_TEXT_COME = Path("../", "Elements/", "Text/", "come.png")
MID_TEXT_SUNDAY = Path("../", "Elements/", "Text/", "league_sunday.png")
MID_TEXT_SATURDAY = Path("../", "Elements/", "Text/", "league_saturday.png")

# ----- places of elements (other stories) -----
BLACK_BG_PLACE = (0, 0)
RED_MID_PLACE = (764, 0)
X_ELEMENT_PLACE = (1742, 323)
MID_TEXT_PLACE = (781, 0)


"""RESULT CONSTANTS (not used)"""
# ----- paths to elements -----
MASK_PATH = Path("../", "Elements/", "Result/", "mask.png")
TMP_RES_PATH = Path("../", "Pictures/", "tmp_result.png")
RESULT_PHOTO_PATH = Path("../", "Elements/", "Result/", "photo.png")

# ----- places of elements -----
HOME_LOGO_RESULT_PLACE = (832, 176)
GUEST_LOGO_RESULT_PLACE = (832, 985)


"""INVITE CONSTANTS"""
# ----- invite paths -----
TMP_INVITE_PATH = Path("../", "Pictures", "invite_tmp.png")
WEB_BANNER_PATH = Path("../", "Pictures", "web.png")

# ----- database paths -----
PLAYER_DATABASE_PATH = Path("../", "Database", "database.json")
LAST_USED_DATABASE_PATH = Path("../", "Database", "last_used.json")
TEST_PLAYER_DATABASE_PATH = Path("../", "Database", "test_database.json")
TEST_LAST_USED_DATABASE_PATH = Path("../", "Database", "test_last_used.json")


"""GUI CONSTANTS"""
EXC_TEXT_COLOR = "red"
ISSUE_WITH_LOGO_COLOR = "green"
IMPORT_FILE_COLOR = "green"

# ----- places ----
HOME_LOGO_PLACE = (510, 128)
GUEST_LOGO_PLACE = (735, -407)


"""FINAL IMAGES"""
FINAL_IMG_FOLDER = "../" + "Final_images/"
INVITE_DONE_PATH = Path(FINAL_IMG_FOLDER, "invite.png")
WEB_DONE_PATH = Path(FINAL_IMG_FOLDER, "web.png")
FIRST_STORY_DONE_PATH = Path(FINAL_IMG_FOLDER, "s1.png")
LAST_STORY_DONE_PATH = Path(FINAL_IMG_FOLDER, "s_last.png")
STORY_DONE_PATH = [
    Path(FINAL_IMG_FOLDER, "s2.png"),
    Path(FINAL_IMG_FOLDER, "s3.png"),
    Path(FINAL_IMG_FOLDER, "s4.png"),
    Path(FINAL_IMG_FOLDER, "s5.png"),
    Path(FINAL_IMG_FOLDER, "s6.png"),
]

MUST_EXIST_FILES = [
    Path(FINAL_IMG_FOLDER),
    PLAYER_DATABASE_PATH,
    BLACK_BG_PATH,
    RED_MID_PATH,
    X_ELEMENT_PATH,
    BG_STORIES_PATH,
    MID_TEXT_COME,
    MID_TEXT_SUNDAY,
    MID_TEXT_SATURDAY,
    Path(LOGO_PATH_STR),
    UNDER_LOGO_PATH,
    VS_PATH,
    Path("." + DIN_FONT),
    Path("." + REMOVER_FONT)
]

# ####################################

# ----- OFFLINE API DATA -----
OFFLINE_DATA = [{
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent Plzeň',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T11:00:00Z',
    'competitionName': '2. liga muži JVČ',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    },
]

"""
,
    {
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent Plzeň',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T13:00:00Z',
    'competitionName': '1. liga starší dorostenci',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    }
    {
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent Plzeň',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T15:00:00Z',
    'competitionName': '1. liga starší dorostenci',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    },
{
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent Plzeň',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T17:00:00Z',
    'competitionName': '1. liga starší dorostenci',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    },
    {
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent Plzeň',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T17:00:00Z',
    'competitionName': '1. liga starší dorostenci',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    }
"""

OFFLINE_DATA_1 = [{
    'homeTeamName': 'TJ Sokol Úvaly',
    'guestTeamName': 'Talent plzen',
    'homeTeamScore': 0, 'guestTeamScore': 0,
    'matchStart': '2022-12-11T13:00:00Z',
    'competitionName': '1. liga starší dorostenci',
    'sportFieldName': 'hala Úvaly',
    'homeTeamClubPhotoUrl': '/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.png',
    'guestTeamClubPhotoUrl': '/storage/v2/public-storage/0f589af8-bd4b-44ad-b139-db92f8b38bb1/96.gif'
    }
]
