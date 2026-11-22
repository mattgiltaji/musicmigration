import libopensonic
import os


def main() -> None:

    # load Excel file

    try:
        conn = connect_navidrome()

        # loop over Excel file
        # figure out the song id
        # if unsure, write the ids we have, log the failure, and move to the next
        song_id = get_song_id(conn, "Self Esteem", "311", "Self Esteem")

        # we've identified the song, log IDs and the original playcount
        # loop playcount times, hitting scrobble based on the last played date

        #song = conn.get_song(songid)
        #print(song.title)
        #conn.scrobble(songid)
    finally:
        print("disconnecting from navidrome")
        conn.cleanup()


def connect_navidrome() -> libopensonic.Connection:
    """
    Connects to a navidrome instance and returns the connection
    :return: libopensonic.Connection
    """
    navidrome_url = os.getenv("NAVIDROME_URL", "https://missing.navidrome.url")
    navidrome_user = os.getenv("NAVIDROME_USER", "missing_username")
    navidrome_pass = os.getenv("NAVIDROME_PASS", "missing_password")
    navidrome_port = int(os.getenv("NAVIDROME_PORT", 443))
    print(f"connecting to navidrome at {navidrome_url} on port {navidrome_port} with username {navidrome_user}.")
    return libopensonic.Connection(navidrome_url, navidrome_user, navidrome_pass, port=navidrome_port)


def get_song_id(conn, title, artist, album) -> str:
    """
    Search navidrome for a song ID based on the song's title, artist, and album

    :param conn: navidrome connection
    :param title: song title
    :param artist: song's artist
    :param album: song's album
    :return: song id
    """
    # Search the song title alone, maybe we'll get lucky
    results = conn.search2(title)
    if len(results.song) == 1:
        print(f"title {title} was unique!")
        return results.song[0].id

    if not len(results.song):
        print(f"title {title} had no matches")
        # throw an error here for better catching?
        return ""

    print(f"title {title} had multiple matches, continuing to further checks")
    # loop over results, see if artist and album will differentiate
    potential_songs = []
    for song in results.song:
        if song.artist == artist and song.album == album:
            potential_songs.append(song)

    if len(potential_songs) == 1:
        print(f"title {title} with artist {artist} and album {album} was unique!")
        return potential_songs[0].id
    if not len(potential_songs):
        print(f"title {title} with artist {artist} and album {album} did not match, find it manually")
    else:
        print(f"title {title} with artist {artist} and album {album} had multiple matches, find it manually")
    return ""