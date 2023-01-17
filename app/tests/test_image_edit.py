import pytest
import numpy as np
from src.image_edit import (
    add_element_to_img,
    make_shadow,
    black_and_white,
    unicode_text
)


def test_add_element_to_img():
    base = np.zeros((10, 10, 4), dtype=np.uint8)
    element = np.ones((5, 5, 4), dtype=np.uint8) * 255

    result = add_element_to_img(base, element)

    assert (result[:5, :5] == 255).all()
    assert (result[5:, :] == 0).all()


def test_make_shadow():
    base = np.zeros((100, 100, 4), dtype=np.uint8)
    element = np.ones((20, 20, 4), dtype=np.uint8) * 255
    base[20:40, 20:40, :] = element

    # checks if pixels around the element has aplha channel equal to zero
    for i in range(element.shape[0] + 10):
        for j in range(element.shape[1] + 10):
            if i < 5 or j < 5 or i > 24 or j > 24:
                assert base[i + 15, j + 15, 3] == 0

    result = make_shadow(base)

    assert result.shape == (100, 100, 4)
    # checks if there is a shadow around the element -> aplha channel is not equal to zero
    for i in range(element.shape[0] + 10):
        for j in range(element.shape[1] + 10):
            assert result[i + 15, j + 15, 3] != 0


def test_black_and_white():
    red = np.ones((5, 5), dtype=np.uint8) * 255
    alpha = np.ones((5, 5), dtype=np.uint8) * 255
    base = np.zeros((10, 10, 4), dtype=np.uint8)
    base[:5, :5, 0] = red
    base[:5, :5, 3] = alpha

    result = black_and_white(base, 1)

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            # grayscale has every color layer same value
            assert result[i, j, 0] == result[i, j, 1] == result[i, j, 2]
            # check if alpha is unchanged
            if i < 5 and j < 5:
                assert result[i, j, 3] == 255
            else:
                assert result[i, j, 3] == 0


@pytest.mark.parametrize(
    "text, expected",
    [
    ("neděle", "nedele"),
    ("Tomáš", "Tomás"),
    ("úterý", "úterý"),
    ("středa", "streda"),
    ("Tohle je testovací věta!", "Tohle je testovací veta!")
    ])
def test_unicode_text(text, expected):
    assert unicode_text(text) == expected
