"""
Module for filters, image edits, ...
"""

import numpy as np
from PIL import Image, ImageFilter
from src.constants import (
    LIGHT_BLACK,
)


letters_with_hook = {
    "č" : "c",
    "ď" : "ď",
    "ě" : "e",
    "ň" : "n",
    "ř" : "r",
    "š" : "s",
    "ť" : "t",
    "ž" : "z",
    "ů" : "u"
}


def add_element_to_img(base, element, place = (0, 0)):
    """Adds element to image on given position.
    Images must be in RGBA format.

    Args:
        base (np.array): Base image.
        element (np.array): Element.
        place (tuple): Place where the element will "start".

    Returns:
        np.array: Image with added element.
    """

    assert element.shape[2] == 4
    assert base.shape[2] == 4

    for i in range(element.shape[0]):
        for j in range(element.shape[1]):
            alpha = (element[i, j, 3] / 255)
            if (place[0] + i >= base.shape[0]) or (place[1] + j >= base.shape[1]):
                break
            base[place[0] + i, place[1] + j, :3] = (
                                    (element[i, j, :3] * alpha)
                                     + (base[place[0]+i, place[1]+j, :3] * (1 - alpha))
                                )
            base[place[0] + i, place[1] + j, 3] = max(base[place[0] + i, place[1] + j, 3], element[i, j, 3])

    return base


def make_shadow(element):
    """Adds shadow/black glow behind the element.

    Args:
        element (np.array): Base image.

    Returns:
        np.array: Image with back shadow.
    """

    shade = np.zeros(element.shape, dtype=np.uint8)
    for i in range(element.shape[0]):
        for j in range(element.shape[1]):
            if element[i, j, 3] != 0:
                shade[i, j, :] = LIGHT_BLACK

    img = Image.fromarray(shade)
    shade_img = img.filter(ImageFilter.GaussianBlur(radius = 20))

    base = np.array(shade_img)

    element_with_shade = add_element_to_img(base, element)

    return element_with_shade


def add_gradient(image):
    """Adds gradient on the bottom part of image.

    Args:
        image (np.array): Base image.

    Returns:
        np.array: Image with bottom gradient.
    """

    black = np.zeros(image.shape, dtype=np.uint8)
    black[ -170:, :, :] = LIGHT_BLACK

    img = Image.fromarray(black)
    gradint_img = img.filter(ImageFilter.GaussianBlur(radius = 30))
    return add_element_to_img(image, np.array(gradint_img))


def get_resized_array(image_path, to_size):
    """Resized an image and converts to an array.

    Args:
        image_path (pathlib.Path): Image that is resized.
        to_size (tuple): New size of the image.

    Returns:
        np.array: Resized image in array.
    """

    img = Image.open(image_path)
    resized = img.resize(to_size)
    return np.array(resized)


def black_and_white(image, brightness = 1.5):
    """Converts image to black and white.

    Args:
        image (np.array): Base image.
        brightness (float): Default is 1.5.

    Returns:
        np.array: Image in black and white but in RGBA format.
    """

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r, g, b = image[ i, j, 0], image[ i, j, 1], image[ i, j, 2]
            # make one gray_scale value (*1.5 = add brightness)
            value = (r * 0.114 + g * 0.587 + b * 0.299) * brightness
            image[ i, j, :3] = np.clip(value, 0, 255)
    return image

def unicode_text(text):
    """Removes hooks from letters.

    Args:
        text (str): Base text.

    Returns:
        str: Text with letters without hooks.
    """

    new_text = []
    for x in text:
        if x in letters_with_hook.keys():
            new_text.append(letters_with_hook[x])
        else:
            new_text.append(x)
    return "".join(new_text)
