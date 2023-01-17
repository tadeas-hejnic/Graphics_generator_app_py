import pytest
import json
from src.invite import Invite
from src.constants import (
    LIGHT_BLACK
)

@pytest.fixture
def invite():
    return Invite(gui = None, data = None)


@pytest.mark.parametrize(
    "list1, list2, equal",
    [
    ([(1, 3), (3, 4), (6, 9)], [(1, 3), (3, 4), (6, 9)], True),
    ([(1, 3), (3, 4), (6, 9)], [(3, 4), (1, 3), (6, 9)], False),
    ([("name", "address"), (True, True), (4, 2)], [("name", "address"), (True, True), (4, 2)], True),
    ([("name", "address"), (False, False), (4, 2)], [("name", "address"), (True, True), (4, 2)], False),
    ([("str0", "str1", "str2"), ("str3", "str4", "str5")], [("str0", "str1", "str2"), ("str3", "str4", "str5")], True),
    ([("str0", "str1", "str2"), ("str3", "str4", "str5")], [(3, 4), (1, 3), (6, 9)], False),
    ([(1)], [(1)], True),
    ([(1)], [(0)], False)
    ])
def test_isequal(list1, list2, equal):
    i = Invite(gui = None, data = None)
    assert i.isequal(list1, list2) == equal


def test_make_bg(invite):
    invite.make_bg()

    for i in range(invite.base.shape[0]):
        for j in range(invite.base.shape[1]):
            assert tuple(invite.base[ i, j, :]) == LIGHT_BLACK
