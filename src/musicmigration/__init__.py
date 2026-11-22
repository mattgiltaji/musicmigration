import os


from . import navidrome

def main() -> None:

    # load Excel file
    navidrome_url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
    navidrome_user = os.getenv("NAVIDROME_USER", "missing_username")
    navidrome_pass = os.getenv("NAVIDROME_PASS", "missing_password")
    navidrome_port = int(os.getenv("NAVIDROME_PORT", 443))
    with navidrome.Navidrome(navidrome_url, navidrome_user, navidrome_pass, navidrome_port) as navi:

        # loop over Excel file
        # figure out the song id
        # if unsure, write the ids we have, log the failure, and move to the next
        song_id = navi.get_song_id("Self Esteem", "311", "Self Esteem")
        print(song_id)

        # we've identified the song, log IDs and the original playcount
        # loop playcount times, hitting scrobble based on the last played date

        #song = conn.get_song(songid)
        #print(song.title)
        #conn.scrobble(songid)


