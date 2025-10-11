from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime, Boolean, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *





#The post under a locations posts
class Visit(db.Model):
    __tablename__ = "visit"
    __table_args__ = {'schema': visit_schema} 
    visit_id = Column(BigInteger, primary_key=True)
    
    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'), nullable=False, index=True)
    user_profile_id = Column(UUID(as_uuid=True),  ForeignKey(f'{user_profile_schema}.user_profile.id'), nullable=False, index=True)
    location_id = relationship('Location', backref='post', lazy=True)
    
    spotify_track_id = Column(String(50), ForeignKey(f'{spotify_track_schema}.spotify_track.spotify_track_id'))
    caption = Column(String(250))
    hashtags = Column(ARRAY(String))
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    like_count = Column(BigInteger, default=0)
    share_count = Column(Integer, default=0)

    num_of_edits = Column(Integer, default=0) # user_profile can edit their vistit only 3 times (caption, image, hashtag, song, etc)
    is_deleted = Column(Boolean, default=False) #is the post deleted by user_profile
    deleted_at = Column(DateTime)
    deleted_by = Column(UUID(as_uuid=True))
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters, admin, etc (does NOT mean deleted by user_profile)

    spotify_track = relationship('SpotifyTrack', backref='visit', lazy=True)

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "post_id": self.post_id,
            "user_profile_id": self.user_profile_id,
            "location_id": self.location_id,
            "song_id": self.song_id,
            "song_artist": self.song_artist,
            "song_name": self.song_name,
            "caption": self.caption,
            "hashtags": self.hashtags,
            "date_posted": self.date_posted,
            "like_count": self.like_count,
            "share_count": self.share_count,
            "num_of_edits": self.num_of_edits,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at,
            "num_reports": self.num_reports,
            "is_removed": self.is_removed
        }
    
    @classmethod
    def active(cls):
        return cls.query.filter_by(is_deleted = False, is_removed = False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class VisitMedia(db.Model):
    __tablename__ = "visit_media"
    __table_args__ = {'schema': visit_media_schema} 
    visit_id = Column(BigInteger, ForeignKey(f'{visit_schema}.visit.visit_id'), nullable=False, index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'), nullable=False, index=True)
    location_id = Column(BigInteger, ForeignKey(f'{location_schema}.location.location_id'), index=True)

    visit_media_id =Column(BigInteger, primary_key=True)
    media_url = Column(Text)
    media_type = Column(String(15), default = 'image') #stores what type of media is uploaed, image, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    verified_status = Column(String(10), default='pending') #Will either be pending, verified, or rejected to verify each image
    is_primary = Column(Boolean, default=False) #Sets the primary pic in front
    
    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "uploaded_by": self.uploaded_by,
            "location_id": self.location_id,
            "visit_media_id": self.visit_media_id,
            "media_url": self.media_url,
            "media_type": self.media_type,
            "width": self.width,
            "height": self.height,
            "upload_date": self.upload_date,
            "verified_status": self.verified_status,
            "is_primary": self.is_primary
        }
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    
#* Visits can get likes but not ratings.Only post can have star ratings
# class VisitLike(db.Model):
#     pass


#     def save(self):
#         db.session.add(self)
#         db.session.commit()