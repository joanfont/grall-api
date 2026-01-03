from datetime import date
import random

from grall.config import config
from grall.models import Song
from grall.repository import SongRepository, RedisSongRepository
from grall.spotify import SpotifyClient, CachedSpotipyClient
from grall.utils import Calendar


class GetSongOfDay:

    def __init__(self, 
        song_repository: SongRepository=None, 
        spotify_client: SpotifyClient=None, 
        calendar: Calendar=None,
        song_rotation_days: int=None
    ):
        self._song_repository = song_repository or RedisSongRepository()
        self._spotify_client = spotify_client or CachedSpotipyClient()
        self._calendar = calendar or Calendar()
        self._song_rotation_days = song_rotation_days or config.SONG_ROTATION_DAYS

    def execute(self, playlist_id: str, day: date) -> Song:
        today_saved_song = self._song_repository.get_by_date(playlist_id, day)
        if today_saved_song is not None:
            return today_saved_song
        
        all_songs = self._spotify_client.get_playlist_songs(playlist_id)
        played_songs = self._song_repository.get_daily_songs(playlist_id)

        eligible_songs = self._get_eligible_songs(all_songs, played_songs)
        song = random.choice(eligible_songs)

        song_rotation_seconds = self._song_rotation_days * 24 * 60 * 60
        self._song_repository.set_by_date(playlist_id, day, song, ttl=song_rotation_seconds)

        return song
    
    def _get_eligible_songs(self, all_songs: list[Song], played_songs: list[Song]) -> list[Song]:
        played_song_ids = set(map(lambda s: s.id, played_songs))
        return list(filter(lambda s: s.id not in played_song_ids, all_songs))
    



class GetSongs:

    def __init__(self, spotify_client: SpotifyClient=None):
        self._spotify_client = spotify_client or CachedSpotipyClient()

    def execute(self, playlist_id: str) -> list[Song]:
        return self._spotify_client.get_playlist_songs(playlist_id)