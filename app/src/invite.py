"""Module for class that creates the main invite graphics."""

import numpy as np
import random
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from src.api import league_sunday
from src.image_edit import (
    add_element_to_img,
    make_shadow,
    add_gradient,
    get_resized_array,
    unicode_text
)
from src.database import InviteDatabase
from src.time_manager import day_date_time
from src.constants import (
    LIGHT_BLACK,
    MY_WHITE,
    DARK_RED,
    YELLOW,
    INVITE_SIZE,
    REMOVER_FONT,
    DIN_FONT,
    INVITE_DONE_PATH,
    TMP_INVITE_PATH,
)


# invite constants

HOME_TEAMS = {
    "2. liga mladší dorostenci - západ" : "mladsi_dorost",
    "1. liga starší dorostenci" : "starsi_dorost",
    "2. liga muži JVČ" : "a_tym",
    "Středočeská společná regionální liga mužů" : "b_tym",
}

SIZES = {
    1 : {
        "players_insert_list" : [0, 4, 1, 3, 2],
        "start_home_teams" : (704, 653),
        "start_guest_teams" : (954, 926),
        "start_players" : 0,
        "start_rectangle" : (811, 776),
        "start_date" : (960, 840),
        "home_text_size" : (610, 139),
        "rectangle_size" : (49, 367, 4),
        "guest_text_size" : 130,
        "date_text_size" : 41,
        "space_between" : 0,
    },
    2 : {
        "players_insert_list" : [0, 2, 1],
        "start_home_teams" : (240, 175),
        "start_guest_teams" : (420, 410),
        "start_players" : 600,
        "start_rectangle" : (320, 279),
        "start_date" : (419, 343),
        "home_text_size" : (487, 111),
        "rectangle_size" : (39, 292, 4),
        "guest_text_size" : 104,
        "date_text_size" : 32,
        "space_between" : 315,
    },
    3 : {
        "players_insert_list" : [0, 2, 1],
        "start_home_teams" : (106, 175),
        "start_guest_teams" : (420, 281),
        "start_players" : 600,
        "start_rectangle" : (192, 274),
        "start_date" : (419, 216),
        "home_text_size" : (487, 111),
        "rectangle_size" : (39, 292, 4),
        "guest_text_size" : 104,
        "date_text_size" : 30,
        "space_between" : 315,
    },
    4 : {
        "players_insert_list" : [0, 2, 1],
        "start_home_teams" : (36, 175),
        "start_guest_teams" : (410, 194),
        "start_players" : 600,
        "start_rectangle" : (111, 289),
        "start_date" : (419, 132),
        "home_text_size" : (438, 100),
        "rectangle_size" : (36, 268, 4),
        "guest_text_size" : 97,
        "date_text_size" : 30,
        "space_between" : 263,
    }
}


class Invite:
    """Class for creating invite graphics.

    Attributes:
        gui (DialogWindow): Dialog window in main GUI page.
        matches (list(dict)): List of matches data.
        num_of_matches (int): Number of matches in invite.
        base (np.array): Invite image that is changed trough the whole process.
        database (InviteDatabase): Keys are categories, values
            are dictionaries where keys are names and values are bools.
        SIZES (dict): Dictionary of constants depending on num_of_matches.
    """
    def __init__(self, gui, data = None):
        self.gui = gui
        self.matches = data
        if data is None:
            self.matches = league_sunday()
        self.num_of_matches = len(self.matches)
        self.base = np.zeros(INVITE_SIZE, dtype=np.uint8)
        self.database = InviteDatabase()
        self.SIZES = SIZES[self.num_of_matches]

    def invite(self):
        """Main method that directs the process of creating invite.

        Returns:
            PIL.Image: Done invite image.
        """

        self.gui.print_text("Creating background...")
        self.make_bg()
        self.gui.print_text("Adding players...")
        self.add_players()
        if self.num_of_matches == 4:
            self.save(TMP_INVITE_PATH)
        self.gui.print_text("Adding home teams...")
        self.add_home_teams()
        self.gui.print_text("Adding guest teams...")
        self.add_guest_teams()
        self.add_rectangles()
        self.gui.print_text("Adding dates...")
        self.add_date()
        self.gui.print_text("Saving...")
        self.save()
        return Image.fromarray(self.base)

    def save(self, path = INVITE_DONE_PATH):
        """Saves self.base to given path.

        Args:
            path (pathlib.Path): File path to save. Default is INVITE_DONE_PATH.
        """

        img = Image.fromarray(self.base)
        img.save(path)

    def make_bg(self):
        """Creates LIGHT_BLACK background.
        """

        self.base[ :, :, :] += np.array(LIGHT_BLACK, dtype=np.uint8)

    def add_players(self):
        """Adds right amount of players to base image.
        """

        categories = []
        for match in self.matches:
            categories.append(HOME_TEAMS[match["competitionName"]])
        categories = self.complete_players(categories, "starsi_dorost")

        category_names = self.choose_players(categories)

        players = []
        for category, name in category_names:
            players.append(
                np.array(
                    (Image.open(Path("../", "Elements/", "Players/", category + "/", name + ".png")))
                ))

        for i in self.SIZES["players_insert_list"]:
            shadow = make_shadow(players[i])
            player = add_gradient(shadow)
            self.base = add_element_to_img(self.base, player, (0, self.SIZES["start_players"] + i*300))

    def add_home_teams(self):
        """Adds pre-created texts of home teams to base image.
        """

        for i in range(self.num_of_matches):
            file_name = HOME_TEAMS[(self.matches[i]["competitionName"])] + ".png"
            path = Path("../Elements/Text/", file_name)
            text = get_resized_array(path, self.SIZES["home_text_size"])
            add_element_to_img(
                self.base, text,
                (self.SIZES["start_home_teams"][0] + i*self.SIZES["space_between"],
                self.SIZES["start_home_teams"][1])
            )

    def add_guest_teams(self):
        """Adds names of guest teams to base image.
        """

        img = Image.fromarray(self.base)
        fnt = ImageFont.truetype(font=REMOVER_FONT, size=self.SIZES["guest_text_size"])
        d = ImageDraw.Draw(img)
        text = [match["guestTeamName"] for match in self.matches]
        for i in range(self.num_of_matches):
            if len(text[i]) > 15:
                self.gui.print_exception("Name of the guest team is to long.\n(" + text[i] + ")")
                text[i] = self.gui.entry_new_text("Entry shorter name: ")
            new_text = unicode_text(text[i])
            if new_text != text[i]:
                self.gui.print_exception("\"" + text[i] + "\" can be written wrong.")
            d.text((self.SIZES["start_guest_teams"][0],
                    self.SIZES["start_guest_teams"][1] + (i * self.SIZES["space_between"])),
                    new_text.lower(), font=fnt, fill=YELLOW, anchor="mm")

        self.base = np.array(img)

    def add_rectangles(self):
        """Creates red rectangles and adds them to base image.
        """

        rectangle = np.zeros(self.SIZES["rectangle_size"], dtype=np.uint8)
        rectangle[ :, :, :3] = DARK_RED
        rectangle[ :, :, 3] = 255
        for i in range(self.num_of_matches):
            self.base = add_element_to_img(
                self.base, rectangle,
                (self.SIZES["start_rectangle"][0] + i*self.SIZES["space_between"], self.SIZES["start_rectangle"][1]))

    def add_date(self):
        """Adds date texts over red rectangles.
        """

        img = Image.fromarray(self.base)
        fnt = ImageFont.truetype(font=DIN_FONT, size=self.SIZES["date_text_size"])
        d = ImageDraw.Draw(img)
        for i in range(self.num_of_matches):
            date = day_date_time(self.matches[i]["matchStart"]).upper()
            d.text((self.SIZES["start_date"][0],
                   self.SIZES["start_date"][1] + (i * self.SIZES["space_between"])), date, font=fnt, fill=MY_WHITE, anchor="mm")

        self.base = np.array(img)

    def choose_players(self, categories):
        """Helper method for choosing players and their order in graphics.
        Communicates with user via dialog window.

        Args:
            categories (list(str)): List of categories that play some match.

        Returns:
            list(str): List of chosen players in chosen order.
        """

        while True:
            category_names = self.database.get(categories)
            # Convert the list of tuples to a string
            choice = "\n".join(f"{x[0]}:\t{x[1]}," for x in category_names)
            if self.gui.yes_no("\nUse these players?\n" + choice):
                break

        while True:
            order = "\n".join(f"{x[0]}:\t{x[1]}," for x in category_names)
            if self.gui.yes_no("\nUse in this order?\n" + order):
                break
            prev = category_names.copy()
            while self.isequal(prev, category_names):
                random.shuffle(category_names)

        return category_names

    def complete_players(self, categories, to_remove = "b_tym"):
        """Helper method for choosing players.
        Removes or adds a player depending on num_of_matches.

        Args:
            categories (list(str)): List of categories that play some match.
            to_remove (str): Category that is removed if necessary. Default is "b_tym".

        Returns:
            list(str): Complete list of players.
        """

        if self.num_of_matches == 4:
            categories.remove(to_remove)
        elif self.num_of_matches == 2:
            if self.gui.yes_no("\nTwo players from team:", categories[0], categories[1]):
                categories.append(categories[0])
            else:
                categories.append(categories[1])
        elif self.num_of_matches == 1:
            while len(categories) < 5:
                categories.append(categories[0])

        return categories

    def isequal(self, x_list, y_list):
        """Helper method comparing two lists of tuples.

        Args:
            x_list (list(tuple)): List of tuples to compare.
            y_list (list(tuple)): List of tuples to compare.

        Returns:
            bool: True if equal, otherwise False.
        """

        if len(x_list) != len(y_list):
            return False
        for x, y in zip(x_list, y_list):
            if x != y:
                return False
        return True
