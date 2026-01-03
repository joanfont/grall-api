from json import JSONEncoder, JSONDecoder

from grall.models import Song

class SongEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Song):
            return obj.as_dict()

        return super().default(obj)


class SongDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        return Song(dct['id'],dct['name'], dct['album'], dct['artist'], dct['preview'])
