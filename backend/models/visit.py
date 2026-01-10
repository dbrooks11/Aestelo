from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Text, DateTime, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography





#The spot under a locations spots
class Visit(db.Model):
    id = Column(BigInteger, primary_key=True)
    
    spot_id = Column(BigInteger, ForeignKey('spot.id'), nullable=False)
    user_profile_id = Column(UUID(as_uuid=True),  ForeignKey('user_profile.id'), nullable=False)
    
    coordinates = Column(Geography(geometry_type='POINT', srid=4326, spatial_index=True))

    music_track_id = Column(String(50), ForeignKey('music_track.id'), nullable=True)
    caption = Column(String(200))
    hashtags = Column(ARRAY(String))
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    like_count = Column(BigInteger, default=0)
    share_count = Column(Integer, default=0)

    total_num_of_photos = Column(Integer)

    num_of_edits = Column(Integer, default=0) # user_profile can edit their vistit only 3 times (caption, photo, hashtag, song, etc)
    is_deleted = Column(Boolean, default=False) #is the spot deleted by user_profile
    deleted_at = Column(DateTime)
    deleted_by = Column(UUID(as_uuid=True))
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters, admin, etc (does NOT mean deleted by user_profile)
    removed_at = Column(DateTime)
    removed_by = Column(UUID)

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "spot_id": self.spot_id,
            "user_profile_id": self.user_profile_id,
            'music_track_id':self.music_track_id,
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
    visit_id = Column(BigInteger, ForeignKey('visit.id'), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), nullable=False)

    id =Column(BigInteger, primary_key=True)
    sort_order = Column(Integer)

    photo_path = Column(Text)
    photo_type = Column(String(15), default = 'photo') #stores what type of media is uploaed, photo, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()
