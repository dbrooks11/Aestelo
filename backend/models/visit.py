from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Text, DateTime, Boolean, ARRAY, func
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
    date_posted = Column(DateTime(timezone=True), server_default=func.now())
    like_count = Column(BigInteger, default=0)
    share_count = Column(Integer, default=0)

    total_num_of_photos = Column(Integer)

    num_of_edits = Column(Integer, default=0) # user_profile can edit their vistit only 3 times (caption, photo, hashtag, song, etc)
    is_deleted = Column(Boolean, default=False) #is the spot deleted by user_profile
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(UUID(as_uuid=True))
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters, admin, etc (does NOT mean deleted by user_profile)
    removed_at = Column(DateTime(timezone=True))
    removed_by = Column(UUID)

    status = Column(String(), default='processing')

    visit_media = relationship('VisitMedia', backref='visit', cascade='all, delete-orphan')
    
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
    photo_type = Column(String(15), default = 'photo') 
    width =  Column(Integer)
    height = Column(Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()
