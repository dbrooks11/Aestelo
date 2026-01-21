from exstensions import db
from models.user import UserProfile
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime, Boolean, ARRAY
from geoalchemy2 import Geography
from sqlalchemy.orm import relationship, ColumnProperty
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app

'''
# Rating fields
average_rating
total_ratings
rating_count
created_at
last_rated_at

# Filter fields  
category
has_photos
visit_count
save_count
'''

class Spot(db.Model):
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserProfile.id), nullable=False, index=True)
    
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    coordinates = Column(Geography(geometry_type='POINT', srid=4326, spatial_index=True))
    date_posted = Column(DateTime(timezone=True), index=True)
    description = Column(Text)
    total_num_of_photos = Column(Integer)

    visit_count = Column(Integer, default=0) 
    average_rating = Column(Float, default=0.0)
    total_num_of_ratings = Column(Integer, default=0)
    last_rated_at = Column(DateTime(timezone=True))

    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    trending_score = ColumnProperty((4 * share_count)+(2*save_count)+((1 * average_rating ) + (1.5 * total_num_of_ratings))) #will be used to calculate a score for trending spot to keep track of which spot is trending
    hashtags = Column(ARRAY(String)) 

    #* Color pallete will be added later
    # color_pallette = Column(String())
    accessibility = Column(Boolean, default=False) 
    num_of_edits = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False) #is the spot deleted by user_profile
    deleted_at = Column(DateTime(timezone=True))
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters, admin, etc (does NOT mean deleted by user_profile)
    removed_at = Column(DateTime(timezone=True))
    status = Column(Text, default='processing')
    
    
    spot_media = relationship('SpotMedia', backref='spot', cascade='all, delete-orphan')
    visit = relationship('Visit', backref='spot', cascade='all, delete-orphan')
    rating = relationship('Rating', backref='spot', cascade='all, delete-orphan')

    @classmethod
    def active(cls):
        return cls.query.filter_by(is_deleted = False, is_removed = False)

    def save(self):
        db.session.add(self)
        db.session.commit()



class SpotMedia(db.Model):
    spot_id = Column(BigInteger, ForeignKey(Spot.id), index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(UserProfile.id), index=True)

    id =Column(BigInteger, primary_key=True)
    sort_order = Column(BigInteger)

    photo_path = Column(Text)
    photo_type = Column(Text, default = 'photo') #stores what type of media is uploaed, photo, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def photo_path_url(self):
        if not self.photo_path:
            return None
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{self.photo_path}"
        return public_url





