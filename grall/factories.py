from grall.models import Song

class SongFactory:

    def from_spotify(self, data): 
        track = data['track']
        return Song(
            id=track['id'],
            name=track['name'],
            album=track['album']['name'],
            artist=track['artists'][0]['name'],
            preview=track['preview_url']
        )
