import libopensonic
from types import TracebackType
from datetime import datetime

class Navidrome:
    def __init__(self, url:str, username:str, password:str, port=443):
        self.url = url
        self.username = username
        self.password = password
        self.port = port
        self.conn = None

    def __enter__(self):
        self.conn = self.connect()
        return self

    def __exit__(
            self,
            type_: type[BaseException] | None,
            value: BaseException | None,
            traceback: TracebackType | None,
    ) -> bool | None:
        # fancy annotation from https://stackoverflow.com/questions/58808055/what-are-the-python-builtin-exit-argument-types
        self.close()

    def connect(self) -> libopensonic.Connection:
        """
        Connects to a navidrome instance and returns the connection
        :return: libopensonic.Connection
        """
        return libopensonic.Connection(self.url, self.username, self.password, port=self.port)

    def close(self):
        """
        Closes the connection to the navidrome instance
        :return:
        """
        self.conn.cleanup()
        self.conn = None


    def get_song_id(self, title, artist, album) -> str:
        """
        Search navidrome for a song ID based on the song's title, artist, and album

        :param title: song title
        :param artist: song's artist
        :param album: song's album
        :return: song id
        """
        if self.conn is None:
            raise RuntimeError(f"called get_song_id() without connecting to navidrome")

        # Search the song title alone, maybe we'll get lucky
        results = self.conn.search2(title)

        if results.song is None:
            raise NoTitleMatchError(f"title '{title}' had no matches")

        if len(results.song) == 1:
            print(f"title {title} was unique!")
            return results.song[0].id

        print(f"title {title} had multiple matches, continuing to further checks")
        # loop over results, see if artist and album will differentiate
        potential_songs = []
        for song in results.song:
            if artist in song.artist and album in song.album and title in song.title:
                potential_songs.append(song)

        if len(potential_songs) == 1:
            print(f"title '{title}' with artist '{artist}' and album '{album}' was unique!")
            return potential_songs[0].id
        if not len(potential_songs):
            raise NoComboMatchError(f"title '{title}' by '{artist}' on '{album}' did not match")
        else:
            ids = [song.id for song in potential_songs]
            raise MultiMatchError(f"title '{title}' by '{artist}' on '{album}' had multiple matches {ids}")

    def super_scrobble(self, song_id, count, date):
        """
        Repeatedly scrobbles a song to bump its play count up.

        Note that this will add 'count' to its play count, not replace the play count with count.

        Some accidental re-run protections:
            For larger counts (over 20), error if the song's play count is already higher than count

        :param song_id: song id to scrobble
        :param count: the number of times to scrobble
        :param date: the date to scrobble (will become last played date on a song that has not been played yet)
        :return:
        """
        if self.conn is None:
            raise RuntimeError(f"called super_scrobble() without connecting to navidrome")

        song = self.conn.get_song(song_id)
        current_count = song.play_count
        if not current_count:
            current_count = 0
        if current_count >= count > 20:
            raise AlreadySuperScrobbledError(f"song '{song.title}' already has more than {count} plays")

        timestamp = datetime.strptime(date, "%m/%d/%Y")
        unix_timestamp = int(timestamp.timestamp())
        print(f"super scrobbling {song.title} {count} times")

        scrobbles = 0
        while scrobbles < count:
            scrobbles += 1
            response = self.conn.scrobble(song_id, listen_time=unix_timestamp)
            if not response:
                raise RuntimeError(f"Scrobble {scrobbles} of {count} for id {song_id} failed, check navidrome logs")


class NoTitleMatchError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class NoComboMatchError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class MultiMatchError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class AlreadySuperScrobbledError(ValueError):
    def __init__(self, message):
        super().__init__(message)