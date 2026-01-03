from decouple import config as decouple_config

class Config:

    @property
    def SPOTIFY_CLIENT_ID(self):
        return decouple_config('SPOTIFY_CLIENT_ID')

    @property
    def SPOTIFY_CLIENT_SECRET(self):
        return decouple_config('SPOTIFY_CLIENT_SECRET')

    @property
    def REDIS_HOST(self):
        return decouple_config('REDIS_HOST')
    
    @property
    def REDIS_PORT(self):
        return decouple_config('REDIS_PORT', cast=int)
    
    @property
    def SPOTIFY_DEFAULT_PLAYLIST_ID(self):
        return decouple_config('SPOTIFY_DEFAULT_PLAYLIST_ID')
    
    @property
    def SONG_ROTATION_DAYS(self):
        return decouple_config('SONG_ROTATION_DAYS', default=None, cast=int)


config = Config()
