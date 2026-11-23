import os
import pandas as pd

from . import navidrome, excel

def main() -> None:

    # load Excel file
    navidrome_url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
    navidrome_user = os.getenv("NAVIDROME_USER", "missing_username")
    navidrome_pass = os.getenv("NAVIDROME_PASS", "missing_password")
    navidrome_port = int(os.getenv("NAVIDROME_PORT", 443))
    excel_input = "./data/input.xlsx"
    excel_output = "./data/output.xlsx"
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
            else:
                song_id = row.song_id

            print(f"song id: {song_id} for row: {row}")
            # we've identified the song, log IDs and the original playcount
            # loop playcount times, hitting scrobble based on the last played date

        #song = conn.get_song(songid)
        #print(song.title)
        #conn.scrobble(songid)


