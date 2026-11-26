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

@pytest.fixture
def sample_song_id():
    # safe to scrobble and such
    return "6TuhFkipm48hScmJwIAaKR"

@pytest.fixture
def many_plays_song_id():
    # safe to scrobble and such
    return "5SIkkSbiynLChzFkYQ6zCg"

class TestNavidrome:
    def test_connect_works_with_rando_urls(self):
        navi = navidrome.Navidrome("https://google.com", "username", "password")
        navi.connect()

    def test_context_manager_works(self):
        with navidrome.Navidrome("https://google.com", "username", "password", 443):
            pass

    def test_get_song_without_init_fails(self):
        navi = navidrome.Navidrome("https://google.com", "username", "password")
        with pytest.raises(RuntimeError):
            navi.get_song_id("Test", "Test", "Test")

    def test_get_unique_song_id_works(self, navi):
        expected = "3jiXfwp63oU0n2WYhHEgxd"
        actual = navi.get_song_id("Antigravity", "STARSET", "Transmissions")
        assert expected == actual

    def test_get_nonsense_song_id_errors(self, navi):
        with pytest.raises(navidrome.NoTitleMatchError):
            navi.get_song_id("aw43985123045bz", "artist", "album")

    def test_get_song_id_nonsense_artist_errors(self, navi):
        with pytest.raises(navidrome.NoComboMatchError):
            navi.get_song_id("Hurt", "ez1234567", "Hurt")

    def test_get_song_id_same_tile_multi_albums_works(self, navi):
        expected = "6tmtPWqaZeEVAFxc2OOP9z"
        actual = navi.get_song_id("21st Century (Digital Boy)", "Bad Religion", "All Ages")
        assert expected == actual

    @pytest.mark.parametrize("test_input, expected", [
        ("Apostrophe Can’`'‛t", "apostrophe can''''t"),
        ("normalize ﬃ", "normalize ffi"),
        ("CaSe FoLdInG sTrAße", "case folding strasse"),
    ])
    def test_standardized_works(self, test_input, expected):
        actual = navidrome.Navidrome.standardized(test_input)
        assert expected == actual

    def test_multi_match_errors(self, navi):
        # this is a spurious pass, we might need to seed some test data for this use case
        with pytest.raises(navidrome.MultiMatchError):
            navi.get_song_id("Sample 5", "Test Artist", "Test Album")

    def test_super_scrobble_without_init_fails(self, sample_song_id):
        navi = navidrome.Navidrome("https://google.com", "username", "password")
        with pytest.raises(RuntimeError):
            navi.super_scrobble(sample_song_id, 1, "1/1/2021")

    def test_super_scrobble_errors_on_high_current_playcount(self, navi, many_plays_song_id):
        with pytest.raises(navidrome.AlreadySuperScrobbledError):
            navi.super_scrobble(many_plays_song_id, 21, "1/1/2021")

    def test_super_scrobble_works_on_low_count_high_playcount(self, navi, many_plays_song_id):
        iterations = 3
        current = navi.conn.get_song(many_plays_song_id).play_count
        expected = current + iterations
        navi.super_scrobble(many_plays_song_id, iterations, "1/1/2021")
        actual = navi.conn.get_song(many_plays_song_id).play_count
        assert expected == actual
