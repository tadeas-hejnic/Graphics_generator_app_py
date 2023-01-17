import pytest
from src.logo_manager import logoManager


@pytest.mark.parametrize(
    "endpoint, team",
    [
    ("/storage/v2/public-storage/793da09b-218f-4b8a-9e25-051b34728783/218.gif", "homeTeam"),
    ("/storage/v2/club-storage/3537d433-c8c7-4676-9814-5359a05a90c8/logo_handballBEZCZECH.gif", "guestTeam"),
    ("/storage/v2/club-storage/d1552a17-59d1-4a92-9c8f-de64db8820be/logo.hazena.uvaly.1000px.jpg", "homeTeam")
    ])
def test_download_raise_type_error(endpoint, team):
    lm = logoManager()
    with pytest.raises(TypeError):
        lm.download(endpoint, team)
