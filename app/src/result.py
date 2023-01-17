# The graphic style for results will be changed.

"""
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from src.logoManager import logoManager
from src.api import (
    weekend_result
)
from src.constants import (
    RESULT_SIZE,
    RESULT_PHOTO_WIDTH,
    RESULT_PHOTO_PATH,
    MASK_PATH,
    MY_WHITE,
    BLACK,
    DARK_RED,
    TMP_RES_PATH,
    HOME_LOGO_PATH,
    GUEST_LOGO_PATH,
    DIN_FONT,
    REMOVER_FONT,
    MY_TEAM,
    HOME_LOGO_RESULT_PLACE,
    GUEST_LOGO_RESULT_PLACE
)


def add_element_to_img(base, element, place):
    for i in range(element.shape[0]):
        for j in range(element.shape[1]):
            alpha = (element[i, j, 3] / 255 )
            base[place[0] + i, place[1] + j, :] = (
                                    (element[i, j, :] * alpha)
                                     + (base[place[0]+i, place[1]+j, :] * (1 - alpha))
                                )
    return base


def resize_photo(path):
    photo = Image.open(path)
    width = RESULT_PHOTO_WIDTH
    height = int(photo.height / photo.width * RESULT_PHOTO_WIDTH)
    resized_photo = photo.resize((width, height))
    resized_photo.save(path)


def make_bg(color):
    tmp = np.zeros((RESULT_SIZE[0], RESULT_SIZE[1], 4), dtype=np.uint8)
    tmp[ :, :, :] += np.array([247, 247, 247, 255], dtype=np.uint8)
    return tmp


def mask_image(mask, photo):
    print(photo.shape)
    print(mask.shape)
    new_img = np.zeros((photo.shape[0], photo.shape[1], 4), dtype=np.uint8)
    new_img[ :, :, :3] = photo
    new_img[:, :, 3] = mask[:photo.shape[0], :photo.shape[1], 3]
    return new_img


def black_and_white(photo):
    for i in range(photo.shape[0]):
        for j in range(photo.shape[1]):
            r, g, b = photo[ i, j, 0], photo[ i, j, 1], photo[ i, j, 2]
            # make one gray_scale value (*1.5 = add brightness)
            value = (r * 0.114 + g * 0.587 + r * 0.299) * 1.5
            photo[ i, j, :3] = np.clip(value, 0, 255)


def make_base(winner):
    # TODO - how to choose photo
    bg = make_bg(MY_WHITE)
    resize_photo(RESULT_PHOTO_PATH)
    photo = mask_image(
                np.array(Image.open(MASK_PATH)),
                np.array(Image.open(RESULT_PHOTO_PATH))
                )
    print(photo.shape, "bg:", bg.shape)
    if not winner:
        black_and_white(photo)
    bg = add_element_to_img(bg, photo, (0, 0))
    return bg


def add_logos(base, match_info):
    print("Adding logos...")
    l = logoManager()
    l.download(match_info["homeTeamClubPhotoUrl"], "homeTeam")
    l.download(match_info["guestTeamClubPhotoUrl"], "guestTeam")

    try:
        home_logo = l.resize(HOME_LOGO_PATH, (210, 210), match_info["homeTeamName"])
        add_element_to_img(base, home_logo, HOME_LOGO_RESULT_PLACE)
    except ImportError as exc:
        print(exc, "(Home team logo)")
        print("Download logo with better resolution and save it as ", 
            "\"", match_info["homeTeamName"], "\"", " to /Pictures", sep="")
        print("Then run the app again.")
        ask_for_logo_search(match_info["homeTeamName"])

    try:
        guest_logo = l.resize(GUEST_LOGO_PATH, (210, 210), match_info["guestTeamName"])
        add_element_to_img(base, guest_logo, GUEST_LOGO_RESULT_PLACE)
    except ImportError as exc:
        print(exc, "(Guest team logo)")
        print("Download logo with better resolution and save it as ", 
            "\"", match_info["guestTeamName"], "\"", " to /Pictures", sep="")
        print("Then run the app again.")
        ask_for_logo_search(match_info["guestTeamName"])

    img = Image.fromarray(base)
    img.save(TMP_RES_PATH)


def add_score(home, guest):
    img = Image.open(TMP_RES_PATH)
    text = str(home) + ":" + str(guest)
    fnt = ImageFont.truetype(font=REMOVER_FONT, size=179)

    d = ImageDraw.Draw(img)

    d.text((1350//2, 980), text, font=fnt, fill=DARK_RED, anchor="ms")

    img.save(TMP_RES_PATH)


def add_league(league_name):
    img = Image.open(TMP_RES_PATH)
    text = league_name.upper()
    fnt = ImageFont.truetype(font=DIN_FONT, size=46)

    d = ImageDraw.Draw(img)

    d.text((1350//2, 1049), text, font=fnt, fill=BLACK, anchor="ms")

    img.save(TMP_RES_PATH)


def add_info(match_info):
    add_league(match_info["competitionName"])
    add_score(match_info["homeTeamScore"], match_info["guestTeamScore"])


def is_winner(match):
    if MY_TEAM in match["homeTeamName"]:
        if match["homeTeamScore"] >= match["guestTeamScore"]:
            return True
        else:
            return False
    else:
        if match["guestTeamScore"] >= match["homeTeamScore"]:
            return True
        else:
            return False


def make_result():
    # --------------------------
    print("Getting data from API...")
    todo = weekend_result()
    base = make_base(is_winner(todo[1]))
    # --------------------------
    add_logos(base, todo[1])
    print(todo[1])
    add_info(todo[1])
    print("Job is done.")


# make_result()


res = weekend_result()

for match in res:
    print(match["homeTeamName"], match["homeTeamScore"], ":", match["guestTeamScore"], match["guestTeamName"])
"""
