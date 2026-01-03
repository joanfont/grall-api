from abc import ABCMeta, abstractmethod
from datetime import date
import json


from grall.encoder import SongEncoder, SongDecoder
from grall.models import Song
from grall.cache import connection

class SongRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_by_date(self, playlist_id: str, day: date) -> Song:
        pass

    @abstractmethod
    def set_by_date(self, playlist_id: str, day: date, song: Song, ttl: int=None): 
        pass
    
    def get_daily_songs(self, playlist_id: str) -> list[Song]:
        pass

class RedisSongRepository(SongRepository):

    SEPARATOR = ':'
    DAILY_SONGS_PREFIX = ['daily', 'song']

    def __init__(self, redis_client=None):
        self._redis_client = redis_client or connection
    
    def get_by_date(self, playlist_id: str, day: date) -> Song:
        key = self._build_daily_key(playlist_id, day)
        song_str = connection.get(key)
        if song_str is None:
            return None
        
        return self._unserialize_song(song_str)
        
    def set_by_date(self, playlist_id: str, day: date, song: Song, ttl: int=None):
        key = self._build_daily_key(playlist_id, day)
        song_str = self._serialize_song(song)
        connection.set(key, song_str, ex=ttl)
    
    def get_daily_songs(self, playlist_id: str) -> list[Song]:
        daily_songs_key = self.SEPARATOR.join(self.DAILY_SONGS_PREFIX)
        keys = self._redis_client.keys(f'{daily_songs_key}*')
        return list(map(self._get_by_key, keys))

    def _get_by_key(self, key: str) -> Song:
        song = connection.get(key)
        if not song:
            return None
        
        return self._unserialize_song(song)

    def _serialize_song(self, song: Song) -> str:
        return json.dumps(song, cls=SongEncoder)
    
    def _unserialize_song(self, song: str) -> Song:
        return json.loads(song, cls=SongDecoder)
    
    def _build_daily_key(self, playlist_id: str, day: date) -> str:
        day_str = day.isoformat()
        return self.SEPARATOR.join(self.DAILY_SONGS_PREFIX + [playlist_id, day.isoformat()])
