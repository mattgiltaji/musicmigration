# run with 'uv run --env-file local.env pytest'
# or for coverage 'uv run --env-file local.env coverage run -m pytest' then 'uv run coverage report -m'
import os
import types
from types import SimpleNamespace
from musicmigration import MusicMigration, excel


class TestMain:
    def test_parse_default_env(self, monkeypatch):
        expected = types.SimpleNamespace()
        expected.navidrome_url = "https://missing.navidrome.url"
        expected.navidrome_user = "missing_username"
        expected.navidrome_pass = "missing_password"
        expected.navidrome_port = 443
        expected.excel_input = "./data/input.xlsx"
        expected.excel_output = "./data/output.xlsx"
        monkeypatch.delenv("NAVIDROME_USER", raising=False)
        monkeypatch.delenv("NAVIDROME_PASS", raising=False)
        monkeypatch.delenv("NAVIDROME_URL", raising=False)
        monkeypatch.delenv("NAVIDROME_PORT", raising=False)
        monkeypatch.delenv("INPUT_FILE", raising=False)
        monkeypatch.delenv("OUTPUT_FILE", raising=False)

        actual = MusicMigration.parse_env()
        assert expected == actual

    def test_parse_env_correctly(self, monkeypatch):
        expected = types.SimpleNamespace()
        expected.navidrome_url = "test url"
        expected.navidrome_user = "test user"
        expected.navidrome_pass = "test password"
        expected.navidrome_port = 1234
        expected.excel_input = "./data/lol.xlsx"
        expected.excel_output = "./data/lmao.xlsx"
        monkeypatch.setenv("NAVIDROME_USER", expected.navidrome_user)
        monkeypatch.setenv("NAVIDROME_PASS", expected.navidrome_pass)
        monkeypatch.setenv("NAVIDROME_URL", expected.navidrome_url)
        monkeypatch.setenv("NAVIDROME_PORT", str(expected.navidrome_port))
        monkeypatch.setenv("INPUT_FILE", expected.excel_input)
        monkeypatch.setenv("OUTPUT_FILE", expected.excel_output)

        actual = MusicMigration.parse_env()
        assert expected == actual


    def test_main_happy_path(self, tmpdir):
        url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
        user = os.getenv("NAVIDROME_USER", "missing_username")
        password = os.getenv("NAVIDROME_PASS", "missing_password")
        in_file = "./test/data/input.xlsx"
        out_file = tmpdir.join("done.xlsx")
        expected = excel.Excel("./test/data/expected.xlsx")
        expected.read()
        MusicMigration.migrate(url, user, password, 443, in_file, out_file)
        actual = excel.Excel(out_file)
        actual.read()
        assert actual.df.equals(expected.df)
