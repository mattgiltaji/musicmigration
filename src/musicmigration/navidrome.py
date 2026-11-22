import libopensonic
from types import TracebackType

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
            self.conn = self.connect()

        # Search the song title alone, maybe we'll get lucky
        results = self.conn.search2(title)

        if results.song is None:
            print(f"title {title} had no matches")
            return ""

        if len(results.song) == 1:
            print(f"title {title} was unique!")
            return results.song[0].id

        print(f"title {title} had multiple matches, continuing to further checks")
        # loop over results, see if artist and album will differentiate
        potential_songs = []
        for song in results.song:
            if song.artist == artist and song.album == album and song.title == title:
                potential_songs.append(song)

        if len(potential_songs) == 1:
            print(f"title {title} with artist {artist} and album {album} was unique!")
            return potential_songs[0].id
        if not len(potential_songs):
            print(f"title {title} with artist {artist} and album {album} did not match, find it manually")
        else:
            ids = [song.id for song in potential_songs]
            print(f"title {title} with artist {artist} and album {album} had multiple matches {ids}, find it manually")
        return ""