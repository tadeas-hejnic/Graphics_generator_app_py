"""Module for class downloading logos from API server."""

import requests
import numpy as np
import os
from PIL import Image
from src import api
from src.image_edit import add_element_to_img
from src.constants import (
    BASE_URL,
    LOGO_PATH_STR,
    HOME_LOGO_PATH,
    GUEST_LOGO_PATH
)


class logoManager:
    """Class for downloading logos and editing logos.
    Communicates with GUI DialogWindow.

    Attributes:
        header (dict): Api login token.
    """
    def __init__(self):
        self.header = api.login()

    def download(self, endpoint, team):
        """Downloads logo from given endpoint.
        Saves it to logo directory.

        Args:
            endpoint (str): URL endpoint of logo.
            team (str): Name of save file. ("homeTeam" or "guestTeam")

        Raises:
            TypeError: If the downloaded logo is not in .png format.
        """

        if ".png" not in endpoint:
            raise TypeError
        url = BASE_URL + endpoint
        result = requests.get(url, headers=self.header, timeout=10).content
        with open(LOGO_PATH_STR + team + ".png", 'wb') as handler:
            handler.write(result)

    def delete_prev(self):
        """Deletes logos from logo directory.
        """

        try:
            os.remove(HOME_LOGO_PATH)
        except FileNotFoundError:
            pass
        try:
            os.remove(GUEST_LOGO_PATH)
        except FileNotFoundError:
            pass

    def resize(self, path, new_size, resolution_check = True):
        """Resizes given image.

        Args:
            path (pathlib.Path): File path of the image.
            new_size (tuple): Resolution of new image.
            resolution_check (bool): If resolution check should be made. Default is False.

        Raises:
            ValueError: If resolution of given image is lower than new resolution.

        Returns:
            np.array: Resized logo in array.
        """

        logo = Image.open(path)

        if (resolution_check
            and
            (logo.width < new_size[0] or logo.height < new_size[1])):
            if logo is None:
                raise ValueError

        if logo.width > logo.height:
            width = new_size[0]
            height = int(logo.height / logo.width * new_size[0])
        else:
            height = new_size[1]
            width = int(logo.width / logo.height * new_size[1])

        logo_resized = logo.resize((width, height))

        start_i = (new_size[0] - logo_resized.height) // 2
        start_j = (new_size[1] - logo_resized.width) // 2
        small_logo = np.zeros((new_size[0], new_size[1], 4), dtype=np.uint8)
        return add_element_to_img(small_logo, np.array(logo_resized), (start_i, start_j))
