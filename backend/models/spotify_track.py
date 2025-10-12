from app import db
from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from datetime import datetime, timezone

class SpotifyTrack(db.Model):
    __tablename__ = "spotify_track"
    __table_args__ = {'schema': 'public'}

    spotify_track_id = Column(String(50), primary_key=True)  # Spotify's ID (URI)
    
    # Track info
    track_name = Column(String(200), nullable=False)
    artist_name = Column(String(200), nullable=False)
    album_name = Column(String(200))
    
    # URLs
    album_art_url = Column(String(500))  # Album cover image
    preview_url = Column(String(500))    # 30s preview MP3
    spotify_url = Column(String(200))    # spotify:track:xxx or https://open.spotify.com/track/xxx
    
    # Metadata
    duration_ms = Column(BigInteger)        # Track length in milliseconds
    duration_formatted = Column(String(10))
    release_date = Column(String(20))   
    times_used = Column(Integer, default=0)

    def to_dict(self):
        return {
            'spotify_track_id': self.spotify_track_id,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'album_name': self.album_name,
            'album_art_url': self.album_art_url,
            'preview_url': self.preview_url,
            'spotify_url': self.spotify_url,
            'duration_ms': self.duration_ms,
            'duration_formatted':self.duration_formatted,
            'release_date': self.release_date,
            'times_used': self.times_used
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        