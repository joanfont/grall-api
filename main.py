from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from grall.config import config
from grall.services import GetSongOfDay, GetSongs
from grall.utils import Calendar


app = FastAPI(title="Grall", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/tracks')
async def tracks(playlist: str=None):
    playlist_id = playlist or config.SPOTIFY_DEFAULT_PLAYLIST_ID
    get_songs = GetSongs()
    songs = get_songs.execute(playlist_id)

    return JSONResponse(list(map(lambda s: s.as_dict(), songs)))


@app.get('/today')
async def today(playlist: str = None, day: date = None):
    playlist_id = playlist or config.SPOTIFY_DEFAULT_PLAYLIST_ID
    day = day or Calendar().today()
    get_today_song = GetSongOfDay()
    song = get_today_song.execute(playlist_id, day)
    
    return JSONResponse(song.as_dict())
