from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime, Boolean, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *
#todo: create rating model
#todo: create filter models

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



class Post(db.Model):
    __tablename__ = "post"
    __table_args__ = {'schema': post_schema} 
    
    user_profile_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'),nullable=False, index=True)
    post_id = Column(BigInteger, primary_key=True)
    
    name = Column(String(100))
    refined_location = Column(Float, nullable=False)
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String(200))
    total_num_of_images = Column(Integer)

    #total_visits = Column(Integer, default=0)  #* Might add total visits to a post
    average_rating = Column(Float, default=0.0)
    total_num_of_ratings = Column(Integer, default=0)
    last_rated_at = Column(DateTime, default=datetime.now(timezone.utc))

    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    trending_score = Column(Integer, default=0) #will be used to calculate a score for trending post to keep track of which post is trending
    tags = Column(ARRAY(String)) #different from hastags, can put tags on post like ('graffiti', 'red', 'streetwear','dark')

    #* Color pallete willl be added later
    # color_pallette = Column(String())
    accessibility = Column(Boolean, default=False) #is it accessible to people who are handicapped. True = yes, False = no
    num_of_edits = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False) #is the post deleted by user_profile
    deleted_at = Column(DateTime)
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters, admin, etc (does NOT mean deleted by user_profile)
    removed_at = Column(DateTime)
    
    
    post_media_id = relationship('PostMedia', backref='post', lazy=True)
    visit_id = relationship('Visit', backref='post', lazy=True)
    rating = relationship('Rating', backref='post', lazy=True)


    def to_dict(self):
        return {
            "user_profile_id": self.user_profile_id,
            "post_id": self.post_id,
            "date_posted": self.date_posted,
            "description": self.description,
            "total_num_of_photos": self.total_num_of_photos,
            "average_rating": self.average_rating,
            "total_num_of_ratings": self.total_num_of_ratings,
            "last_rated_at": self.last_rated_at,
            "save_count": self.save_count,
            "share_count": self.share_count,
            "trending_score": self.trending_score,
            "accessibility": self.accessibility,
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



class PostMedia(db.Model):
    __tablename__ = "post_media"
    __table_args__ = {'schema': post_media_schema} 

    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'), index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(f'{user_profile_schema}.user_profile.id'), index=True)

    location = relationship('Location', backref='post_media', lazy=True)
    post_media_id =Column(BigInteger, primary_key=True)

    thumbnail_url = Column(Text)
    thumb_media_type = Column(String(15), default = 'image')

    media_url = Column(Text)
    media_type = Column(String(15), default = 'image') #stores what type of media is uploaed, image, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)

    is_primary = Column(Boolean,default=False) #Sets the primary pic in front
    

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "uploaded_by": self.uploaded_by,
            "location_id": self.location_id,
            "post_media_id": self.post_media_id,
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





