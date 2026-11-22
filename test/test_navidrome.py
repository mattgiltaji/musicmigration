# run with 'uv run --env-file local.env pytest'
# or for coverage 'uv run --env-file local.env coverage run -m pytest' then 'uv run coverage report -m'
import pytest
import os
from musicmigration import navidrome


@pytest.fixture
def navi():
    url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
    user = os.getenv("NAVIDROME_USER", "missing_username")
    password = os.getenv("NAVIDROME_PASS", "missing_password")
    with navidrome.Navidrome(url, user, password) as navi:
        yield navi

class TestNavidrome:
    def test_connect_works_with_rando_urls(self):
        navi = navidrome.Navidrome("https://google.com", "username", "password")
        navi.connect()

    def test_context_manager_works(self):
        with navidrome.Navidrome("https://google.com", "username", "password", 443):
            pass

    def test_get_unique_song_id_works(self, navi):
        expected = "3jiXfwp63oU0n2WYhHEgxd"
        actual = navi.get_song_id("Antigravity", "STARSET", "Transmissions")
        assert expected == actual

    def test_get_nonsense_song_id_returns_empty(self, navi):
        expected = ""
        actual = navi.get_song_id("aw43985123045bz", "artist", "album")
        assert expected == actual

    def test_get_song_id_nonsense_artist_returns_empty(self, navi):
        expected = ""
        actual = navi.get_song_id("Hurt", "ez1234567", "Hurt")
        assert expected == actual

    def test_get_song_id_same_tile_multi_albums_works(self, navi):
        expected = "6tmtPWqaZeEVAFxc2OOP9z"
        actual = navi.get_song_id("21st Century (Digital Boy)", "Bad Religion", "All Ages")
        assert expected == actual

    @pytest.skip
    def test_get_song_id_same_tile_same_album_returns_empty(self, navi):
        # this is a spurious pass, we might need to seed some test data for this use case
        expected = ""
        actual = navi.get_song_id("Amaranth", "Nightwish", "Dark Passion Play (special edition)")
        assert expected == actual