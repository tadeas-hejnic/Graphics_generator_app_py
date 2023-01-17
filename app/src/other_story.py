"""
Module for making first and last stories.
"""
import numpy as np
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from src.time_manager import get_date, date_without_nulls, get_czech_day
from src.image_edit import add_element_to_img, black_and_white
from src.constants import (
    BLACK_BG_PLACE,
    RED_MID_PLACE,
    X_ELEMENT_PLACE,
    BLACK_BG_PATH,
    RED_MID_PATH,
    X_ELEMENT_PATH,
    DIN_FONT,
    MID_TEXT_COME,
    MID_TEXT_SUNDAY,
    MID_TEXT_SATURDAY,
    MID_TEXT_PLACE
)


class OtherStory:
    """Class for creating "other" stories with text.
    If plain is true, no text is added.

    Attributes:
        base (np.array): Stories base image that is changed trough the whole process.
        save_path (pathlib.Path): File path to save.
        gui (DialogWindow): Dialog window in main GUI page.
        bg_image (PIL.Image): Background image.
        mid_text (np.array): Pre-created image with text.
        date (str): Start of the match.
    """
    def __init__(self, save_name, gui, data = None, plain = False):
        self.base = np.zeros((1920, 1080, 4), dtype=np.uint8)
        self.gui = gui
        self.save_path = Path("../", "Final_images/", save_name + ".png")

        if self.gui.import_file("Import background image. (1080x1920), .png",
            Path("../", "Elements/", "Photos/", save_name + "_bg.png")):
            self.bg_image = None
        else:
            self.bg_image = np.array(Image.open(
                Path("../", "Elements/", "Photos/", save_name + "_bg.png")))

        self.mid_text = None
        self.date = None
        if not plain and data:
            if get_czech_day(data[0]["matchStart"]) == "neděle":
                self.mid_text = np.array(Image.open(MID_TEXT_SUNDAY))
            elif get_czech_day(data[0]["matchStart"]) == "sobota":
                self.mid_text = np.array(Image.open(MID_TEXT_SATURDAY))
            else:
                self.gui.print_exception("Can't add text. (Unexpected day)")
            self.date = data[0]["matchStart"]
        elif not plain:
            self.mid_text = np.array(Image.open(MID_TEXT_COME))

    def other_story(self):
        """Main method that directs the process of creating story.
        """

        if self.bg_image is not None:
            self.base = black_and_white(self.bg_image)
            if self.base.shape[2] != 4:
                new = np.zeros((1920, 1080, 4), dtype=np.uint8)
                new[ :, :, :3] = self.base
                new[ :, :, 3] = 255
                self.base = new 
        self.add_elements()
        if self.mid_text is not None:
            self.add_mid_text()
        if self.date is not None:
            self.add_date()
        self.save()

    def save(self):
        """Saves self.base to given self.save_path.
        """

        img = Image.fromarray(self.base)
        img.save(self.save_path)

    def add_elements(self):
        """Adds pre-created elements to base image.
        """

        self.base = add_element_to_img(self.base, np.array(Image.open(BLACK_BG_PATH)), BLACK_BG_PLACE)
        self.base = add_element_to_img(self.base, np.array(Image.open(RED_MID_PATH)), RED_MID_PLACE)
        self.base = add_element_to_img(self.base, np.array(Image.open(X_ELEMENT_PATH)), X_ELEMENT_PLACE)

    def add_date(self):
        """Adds date to base image.
        """

        img = Image.fromarray(self.base)
        date = date_without_nulls(get_date(self.date), 10)

        fnt = ImageFont.truetype(font=DIN_FONT, size=114)
        d = ImageDraw.Draw(img)
        d.text((1080/2, 1281), date, font=fnt, fill=(255, 255, 255, 255), anchor="ms")

        self.base = np.array(img)

    def add_mid_text(self):
        """Adds text to the middle of the base image.
        """

        self.base = add_element_to_img(self.base, self.mid_text, MID_TEXT_PLACE)
