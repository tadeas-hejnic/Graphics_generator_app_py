"""
Module for making match stories.
"""
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from src.logo_manager import logoManager
from src.image_edit import add_element_to_img
from src.time_manager import (
    get_czech_day,
    get_date,
    my_time_zone,
    date_without_nulls
)
from src.constants import (
    UNDER_LOGO_PATH,
    VS_PATH,
    HOME_LOGO_PATH,
    GUEST_LOGO_PATH,
    HOME_LOGO_PLACE,
    GUEST_LOGO_PLACE,
    DIN_FONT,
    WHITE,
    DARK_RED,
    MY_BLACK,
    LEAGUE_NAMES_DICT,
    STORY_DONE_PATH
)


class Story:
    """Class for creating "match" stories.

    Attributes:
        base (np.array): Stories base image that is changed trough the whole process.
        num (int): Order number of the story.
        save_path (pathlib.Path): File path to save.
        gui (DialogWindow): Dialog window in main GUI page.
        bg_image (PIL.Image): Background image.
        data (dict): Data of the match related to this story.
    """
    def __init__(self, number, data, gui, bg_img = "bg.png"):
        self.base = np.zeros((1920, 1080, 4), dtype=np.uint8)
        self.num = number
        self.save_path = STORY_DONE_PATH[self.num]
        self.gui = gui
        self.bg_image = Image.open(Path("../", "Elements/", "Photos/", bg_img))
        self.data = data

    def story(self):
        """Main method that directs the process of creating story.
        """

        self.gui.print_text("Creating Background...")
        self.make_background()
        self.add_under_logo()
        self.add_vs()
        self.gui.print_text("Adding logos...")
        self.add_logos()
        self.gui.print_text("Adding match info...")
        self.add_info()
        self.gui.print_text("Saving...")
        self.save()

    def save(self):
        """Saves self.base to given self.save_path.
        """

        img = Image.fromarray(self.base)
        img.save(self.save_path)

    def make_background(self):
        """Combines background image with color to create background.
        """

        bg_photo = np.array(self.bg_image)
        red = np.zeros((self.bg_image.height, self.bg_image.width, 4))
        red[:, :, :3] += self.get_color()

        self.base[ :, :, :3] = (bg_photo[ :, :, :3] * 0.15 + red[ :, :, :3] * 0.85).astype(np.uint8)
        self.base[ :, :, 3] = 255

    def add_under_logo(self):
        """Adds two elements under logo to base image.
        """

        element = np.array(Image.open(UNDER_LOGO_PATH))
        self.base = add_element_to_img(self.base, element, (384, 0))

        rotate_element = np.rot90(element, 2)
        self.base = add_element_to_img(self.base, rotate_element, (512, -783))

    def add_vs(self):
        """Adds pre-created "vs" text to base image.
        """

        self.base = add_element_to_img(self.base, np.array(Image.open(VS_PATH)), (688, 444))

    def add_info(self):
        """Directs the process of adding informative text to base image.
        """

        self.add_league(self.data["competitionName"])
        self.add_time(self.data["matchStart"])
        self.add_date(self.data["matchStart"])
        self.add_place()

    def add_league(self, league_name):
        """Adds league name to base image using PIL ImageDraw.

        Args:
            league_name (str): Name of the league.
        """

        img = Image.fromarray(self.base)
        text = LEAGUE_NAMES_DICT[league_name].upper()

        fnt = ImageFont.truetype(font=DIN_FONT, size=94)
        d = ImageDraw.Draw(img)
        d.text((1080/2, 228), text, font=fnt, fill=WHITE, anchor="ms")

        self.base = np.array(img)

    def add_time(self, time_str):
        """Adds match start to base image using PIL ImageDraw.

        Args:
            time_str (str): Time in this type of format: "2023-02-12T13:00:00Z".
        """

        img = Image.fromarray(self.base)
        time = my_time_zone(time_str[11:16])

        fnt = ImageFont.truetype(font=DIN_FONT, size=315)
        d = ImageDraw.Draw(img)

        # ":" baseline is to low - must print divided
        d.text((274, 1242), time[:2], font=fnt, fill=(255, 255, 255, 255), anchor="lt")
        d.text((274+234, 1325), time[2], font=fnt, fill=(255, 255, 255, 255), anchor="lt")
        d.text((1080-279, 1242), time[3:], font=fnt, fill=(255, 255, 255, 255), anchor="rt")

        self.base = np.array(img)

    def add_date(self, date):
        """Adds date of the match start to base image using PIL ImageDraw.

        Args:
            time_str (str): Time in this type of format: "2023-02-12T13:00:00Z".
        """

        img = Image.fromarray(self.base)
        date = (get_czech_day(date) + " " + date_without_nulls(get_date(date), 10)).upper()

        fnt = ImageFont.truetype(font=DIN_FONT, size=94)
        d = ImageDraw.Draw(img)
        d.text((1080/2, 1627), date, font=fnt, fill=(255, 255, 255, 255), anchor="ms")

        self.base = np.array(img)

    def add_place(self, place = "sportovní hala, Úvaly"):
        """Adds date of the match start to base image using PIL ImageDraw.

        Args:
            place (str): Place where the match is played. Default is "sportovní hala, Úvaly".
        """

        img = Image.fromarray(self.base)
        place = place.upper()

        fnt = ImageFont.truetype(font=DIN_FONT, size=94)
        d = ImageDraw.Draw(img)
        d.text((1080/2, 1739), place, font=fnt, fill=(255, 255, 255, 255), anchor="ms")

        self.base = np.array(img)

    def add_logos(self):
        """Adds both logos using logoManager module.
        Communicates with user if issue with logo is occurred.
        """

        l = logoManager()
        l.delete_prev()
        try:
            continue_flag = False
            l.download(self.data["homeTeamClubPhotoUrl"], "homeTeam")
            home_logo = l.resize(HOME_LOGO_PATH, (300, 300))
        except TypeError:
            self.gui.print_exception("Wrong data type. (Home team logo " + self.data["homeTeamName"] + " )")
            continue_flag = self.gui.issue_with_logo(
                "Download and import logo in .png.",
                self.data["homeTeamName"],
                HOME_LOGO_PATH)
            if not continue_flag:
                home_logo = l.resize(HOME_LOGO_PATH, (285, 285), False)
        except ValueError:
            self.gui.print_exception("Low resolution. (Home team logo " + self.data["homeTeamName"] + " )")
            if not self.gui.yes_no("Do you want to use the low resolution logo?"):
                continue_flag = self.gui.issue_with_logo("Download and import logo in .png.",
                    self.data["homeTeamName"],
                    HOME_LOGO_PATH)
            if not continue_flag:
                home_logo = l.resize(HOME_LOGO_PATH, (285, 285), False)

        if not continue_flag:
            self.base = add_element_to_img(self.base, home_logo, HOME_LOGO_PLACE)

        try:
            continue_flag = False
            l.download(self.data["guestTeamClubPhotoUrl"], "guestTeam")
            guest_logo = l.resize(GUEST_LOGO_PATH, (285, 285))
        except TypeError:
            self.gui.print_exception("Wrong data type. (Guest team logo - " + self.data["guestTeamName"] + " )")
            continue_flag = self.gui.issue_with_logo(
                "Download and import logo in .png.",
                self.data["guestTeamName"],
                GUEST_LOGO_PATH)
            if not continue_flag:
                guest_logo = l.resize(GUEST_LOGO_PATH, (285, 285), False)
        except ValueError:
            self.gui.print_exception("Low resolution. (Guest team logo - " + self.data["guestTeamName"] + " )")
            if not self.gui.yes_no("Do you want to use the low resolution logo?"):
                continue_flag = self.gui.issue_with_logo("Download and import logo in .png.",
                    self.data["guestTeamName"],
                    GUEST_LOGO_PATH)
            if not continue_flag:
                guest_logo = l.resize(GUEST_LOGO_PATH, (285, 285), False)

        if not continue_flag:
            self.base = add_element_to_img(self.base, guest_logo, GUEST_LOGO_PLACE)

    def get_color(self):
        """Choose color depending on order number.

        Returns:
            tuple: Color from constants.
        """

        if self.num % 2 == 0:
            return DARK_RED
        return MY_BLACK
