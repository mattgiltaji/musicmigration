import os
import types

import pandas as pd
from types import SimpleNamespace

from . import navidrome, excel

def main() -> None:
    args = MusicMigration.parse_env()
    MusicMigration.migrate(args.navidrome_url, args.navidrome_user, args.navidrome_pass, args.navidrome_port,
                           args.excel_input, args.excel_output)

class MusicMigration:
    @staticmethod
    def parse_env() -> SimpleNamespace:
        args = types.SimpleNamespace()
        args.navidrome_url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
        args.navidrome_user = os.getenv("NAVIDROME_USER", "missing_username")
        args.navidrome_pass = os.getenv("NAVIDROME_PASS", "missing_password")
        args.navidrome_port = int(os.getenv("NAVIDROME_PORT", 443))
        args.excel_input = os.getenv("INPUT_FILE", "./data/input.xlsx")
        args.excel_output = os.getenv("OUTPUT_FILE", "./data/output.xlsx")
        return args

    @staticmethod
    def migrate(navidrome_url, navidrome_user, navidrome_pass, navidrome_port, excel_input, excel_output):
        with (
            navidrome.Navidrome(navidrome_url, navidrome_user, navidrome_pass, navidrome_port) as navi,
            excel.Excel(excel_input, excel_output) as ex,
        ):

            # loop over Excel file
            for row in ex.df.itertuples():
                if pd.isnull(row.song_id):
                    try:
                        song_id = navi.get_song_id(row.song, row.artist, row.album)
                        ex.df.at[row.Index, "song_id"] = song_id
                    except ValueError as err:
                        ex.df.at[row.Index, "notes"] = str(err)
                        continue
                else:
                    song_id = row.song_id

                try:
                    navi.super_scrobble(song_id, int(row.playcount), row.last_played)
                except (RuntimeError, ValueError) as err:
                    ex.df.at[row.Index, "notes"] = str(err)
                    continue
                ex.df.at[row.Index, "notes"] = "Successfully increased playcount"