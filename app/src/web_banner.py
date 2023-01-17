"""Module for class that converts classic invite image to wide web banner"""

import numpy as np
from PIL import Image
# from src.api import league_sunday
from src.image_edit import (
    add_element_to_img
)
from src.constants import (
    LIGHT_BLACK,
    WEB_DONE_PATH,
)

class WebBanner:
    """Class for creating web banner from classic invite image.

    Attributes:
        image (Image): Base image.
        num_of_matches (int): Number of matches in invite.
        gui (DialogWindow): Dialog window in main GUI page.
        banner_size (tuple): Default size of np.array.
    """
    banner_size = (600, 1567, 4)
    def __init__(self, matches, image, gui):
        self.image = image
        self.num_of_matches = len(matches)
        self.gui = gui

    def make_banner(self):
        """
        if self.num_of_matches == 4:
            self.image = Image.open(TMP_INVITE_PATH)
            self.crop()
            self.move_to_center()
            # self.add_info()
        else:
        """
        self.move_to_center()
        self.image.save(WEB_DONE_PATH)
        return self.image

    def move_to_center(self):
        """Creates base of banner size and place the image to center.
        """

        background = np.zeros(self.banner_size, dtype=np.uint8)
        background[ :, :, :] = LIGHT_BLACK
        self.image = self.resize()

        center = (0, (self.image.width - self.banner_size[0]) // 2)
        self.image = Image.fromarray(add_element_to_img(background, np.array(self.image), center))

    def resize(self):
        """Resizes the invite image to fit in new resolution.

        Returns:
            Image: Resized image.
        """

        height = self.banner_size[0]
        width = int(self.image.width / self.image.height * self.banner_size[0])

        return self.image.resize((width, height))

    def crop(self):
        """Not used method for now.
        """

        cropped = np.zeros((1320, 1080, 4), dtype=np.uint8)
        cropped = np.array(self.image)[600:, :, :]
        self.image = Image.fromarray(cropped)
        raise NotImplementedError

    def add_info(self):
        """Not used method for now.
        """

        raise NotImplementedError
