from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime, Boolean, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
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
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'),nullable=False)
    post_id = Column(BigInteger, primary_key=True)

    post_media_id = relationship('PostMedia', backref='post', lazy=True)
    visit_id = relationship('Visit', backref='post', lazy=True)
    rating = relationship('Rating', backref='post', lazy=True)
    
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String(200), default='', nullable=False)
    total_num_of_photos = Column(Integer)

    #total_visits = Column(Integer, default=0)  #* Might add total visits to a post
    average_rating = Column(Float, default=0.0)
    total_num_of_ratings = Column(Float, default=0.0)
    last_rated_at = Column(DateTime, default=datetime.now(timezone.utc))

    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    trending_score = Column(Integer, default=0) #will be used to calculate a score for trending post to keep track of which post is trending

    accessibility = Column(Boolean, default=False) #is it accessible to people who are handicapped. True = yes, False = no

    is_deleted = Column(Boolean, default=False) #is the post deleted by user
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters (does NOT mean deleted by user)
    

    def to_dict(self):
        return {
            'id': self.user_id,
            'post_id': self.post_id,
            'date_posted': self.date_posted,
            'description': self.description,
            'total_num_of_photos': self.total_num_of_photos,
            'average_rating': self.average_rating,
            'total_num_of_ratings': self.total_num_of_ratings,
            'last_rated_at': self.last_rated_at,
            'save_count': self.save_count,
            'share_count': self.share_count,
            'trending_score': self.trending_score,
            'accessibility': self.accessibility,
            'is_deleted': self.is_deleted,
            'num_reports': self.num_reports,
            'is_removed': self.is_removed
        }


class PostMedia(db.Model):
    __tablename__ = "post_media"
    __table_args__ = {'schema': post_media_schema} 

    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'))

    location_id = Column(BigInteger, ForeignKey(f'{location_schema}.location.location_id'))
    post_media_id =Column(BigInteger, primary_key=True)

    media_url = Column(Text)
    media_type = Column(String(15), default = 'image') #stores what type of media is uploaed, image, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)

    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    verified_status = Column(String(8), default='pending') #Will either be pending, verified, or rejected to verify each image
    is_primary = Column(Boolean,default=False) #Sets the primary pic in front
    

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'uploaded_by': self.uploaded_by,
            # The 'location_id' relationship is omitted as it is a related object collection, not a direct column value.
            'post_media_id': self.post_media_id,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'width': self.width,
            'height': self.height,
            'upload_date': self.upload_date,
            'verified_status': self.verified_status,
            'is_primary': self.is_primary
    }


class Rating(db.Model):
    __tablename__ = "rating"
    __table_args__ = {'schema': rating_schema} 
    rating_id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'), nullable=False)
    rating_choice = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'rating_id': self.rating_id,
            'rating_choice': self.rating_choice,
            'created_at': self.created_at,
            'post_id': self.post_id
    }



#The post under a locations posts
class Visit(db.Model):
    __tablename__ = "visit"
    __table_args__ = {'schema': visit_schema} 
    visit_id = Column(BigInteger, primary_key=True)
    
    post_id = Column(BigInteger, ForeignKey(f'{post_schema}.post.post_id'), nullable=False)
    user_id = Column(UUID(as_uuid=True),  ForeignKey(f'{user_schema}.user.id'), nullable=False)
    location_id = relationship('Location', backref='post', lazy=True)
    
    song_id = Column(Text)
    song_artist = Column(Text)
    song_name = Column(Text)
    caption = Column(String(250))
    hashtags = Column(ARRAY(String))
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    like_count = Column(BigInteger, default=0)
    share_count = Column(Integer, default=0)

    num_of_edits = Column(Integer, default=0) # user can edit their vistit only 3 times (caption, image, hashtag, song, etc)
    is_deleted = Column(Boolean, default=False) #is the visit deleted by user
    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=False) #removed due to moderaters (does NOT mean deleted by user)

    def to_dict(self):
        return {
            'visit_id': self.visit_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            # 'location_id' is a relationship and is omitted for simple serialization.
            'song_id': self.song_id,
            'song_artist': self.song_artist,
            'song_name': self.song_name,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'date_posted': self.date_posted,
            'like_count': self.like_count,
            'share_count': self.share_count,
            'num_of_edits': self.num_of_edits,
            'is_deleted': self.is_deleted,
            'num_reports': self.num_reports,
            'is_removed': self.is_removed
    }


class VisitMedia(db.Model):
    __tablename__ = "visit_media"
    __table_args__ = {'schema': visit_media_schema} 
    visit_id = Column(BigInteger, ForeignKey(f'{visit_schema}.visit.visit_id'), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'), nullable=False)

    location_id = Column(BigInteger, ForeignKey(f'{location_schema}.location.location_id'))
    visit_media_id =Column(BigInteger, primary_key=True)
    media_url = Column(Text)
    media_type = Column(String(15), default = 'image') #stores what type of media is uploaed, image, video, 360 video, etc
    width =  Column(Integer)
    height = Column(Integer)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    verified_status = Column(String(8), default='pending') #Will either be pending, verified, or rejected to verify each image
    is_primary = Column(Boolean, default=False) #Sets the primary pic in front
    
    def to_dict(self):
        return {
            'visit_id': self.visit_id,
            'uploaded_by': self.uploaded_by,
            # 'location_id' is a relationship and is omitted for simple serialization.
            'visit_media_id': self.visit_media_id,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'width': self.width,
            'height': self.height,
            'upload_date': self.upload_date,
            'verified_status': self.verified_status,
            'is_primary': self.is_primary
    }



class RemovedPost(db.Model):
    __tablename__ = "removed_post"
    __table_args__ = {'schema': removed_post_schema} 
    removed_post_id = Column(BigInteger, primary_key=True)
    posted_by = Column(String(50), nullable= False)

    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String(200), default='', nullable=False)
    total_num_of_photos = Column(Integer)

    average_rating = Column(Float, default=0.0)
    total_num_of_ratings = Column(Float, default=0.0)
    last_rated_at = Column(DateTime, default=datetime.now(timezone.utc))

    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    trending_score = Column(Integer, default=0) #will be used to calculate a score for trending post to keep track of which post is trending

    accessibility = Column(Boolean, default=False) #is it accessible to people who are handicapped. True = yes, False = no

    num_reports = Column(Integer, default=0)
    is_removed = Column(Boolean, default=True)
    location_id = Column(BigInteger)

    removed_at = Column(DateTime, default=datetime.now(timezone.utc))
    removed_by = Column(String(15))  # 'user', 'admin', 'moderator'
    removal_reason = Column(String(255))
    recoverable_until = Column(DateTime)


   

    def to_dict(self):
        return {
            'removed_post_id': self.removed_post_id,
            'posted_by': self.posted_by,
            'date_posted': self.date_posted,
            'description': self.description,
            'total_num_of_photos': self.total_num_of_photos,
            'average_rating': self.average_rating,
            'total_num_of_ratings': self.total_num_of_ratings,
            'last_rated_at': self.last_rated_at,
            'save_count': self.save_count,
            'share_count': self.share_count,
            'trending_score': self.trending_score,
            'num_reports': self.num_reports,
            'is_removed': self.is_removed,
            'location_id': self.location_id,
            'removed_at': self.removed_at,
            'removed_by': self.removed_by,
            'removal_reason': self.removal_reason,
            'recoverable_until': self.recoverable_until
        }
 