from dataclasses import dataclass, asdict

@dataclass
class Song:
    id: str
    name: str
    album: str
    artist: str
    preview: str

    def as_dict(self) -> dict:
        return asdict(self)
