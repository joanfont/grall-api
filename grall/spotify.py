from abc import ABCMeta, abstractmethod
from urllib.parse import urlparse, parse_qs

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from grall.cache import remember
from grall.config import config
from grall.encoder import SongEncoder, SongDecoder
from grall.models import Song
from grall.factories import SongFactory


class SpotifyClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_playlist_songs(self, playlist_id: str) -> list[Song]:
        pass


class SpotipyClient(SpotifyClient):

    def __init__(self, client=None, song_factory=None):
        self._client = client or spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID, 
                client_secret=config.SPOTIFY_CLIENT_SECRET
            )
        )
        
        self._song_factory = song_factory or SongFactory()
    
    def get_playlist_songs(self, playlist_id: str) -> list[Song]:
        songs = self._do_get_playlist_songs(playlist_id, offset=None)
        return list(filter(lambda s: s.preview is not None, songs))
    
    def _do_get_playlist_songs(self, playlist_id, offset=None) -> list[Song]:
        response = self._client.playlist_tracks(playlist_id, fields='items.track,next', offset=offset)
        
        tracks = list(map(self._song_factory.from_spotify, response['items']))

        if response['next']:
            parsed_next_url = urlparse(response['next'])
            parsed_next_qs = dict(parse_qs(parsed_next_url.query))
            tracks.extend(
                self._do_get_playlist_songs(playlist_id, offset=parsed_next_qs['offset'])
            )
        
        return tracks


class CachedSpotipyClient(SpotipyClient):

        @remember('songs', 86400, SongEncoder, SongDecoder)
        def get_playlist_songs(self, playlist_id) -> list[Song]:
            return super().get_playlist_songs(playlist_id)
