from app.extensions  import db
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship


class MusicTrack(db.Model):

    id = Column(String(50), primary_key=True)  # music's ID (URI)
    
    # Track info
    track_name = Column(String(200), nullable=False)
    artist_name = Column(String(200), nullable=False)
    album_name = Column(String(200))
    
    # URLs
    album_art_url = Column(String(500))  # Album cover image
    preview_url = Column(String(500))    # 30s preview MP3
    music_url = Column(String(200))    # music:track:xxx or https://open.music.com/track/xxx
    
    # Metadata
    duration_ms = Column(BigInteger)        # Track length in milliseconds
    duration_formatted = Column(String(10))
    release_date = Column(String(20))   
    times_used = Column(Integer, default=0)

    visit = relationship('Visit', backref='music_track')
    user_profile = relationship('UserProfile', backref='music_track')


    def save(self):
        db.session.add(self)
        db.session.commit()
        