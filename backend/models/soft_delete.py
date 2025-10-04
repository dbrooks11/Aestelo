from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *





class RemovedUser(db.Model):
    __tablename__ = "removed_user"
    __table_args__ = {'schema': removed_user_schema} 

    removed_user_id = Column(BigInteger, primary_key=True)
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'))
    account_locked_until = Column(DateTime)
    is_business_account = Column(Boolean, default=False)
    password_hash = Column(String(255), nullable=False)

    removed_at = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'))
    removed_by = Column(String(50))  # 'self', 'admin', etc.
    removal_reason = Column(String(255))
    recoverable_until = Column(DateTime)  # Auto-delete after 30 days




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
 

   
class RemovedVisit(db.Model):
    __tablename__ = "removed_visit"
    __table_args__ = {'schema': removed_visit_schema} 
    removed_visit_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'), nullable=False)
    
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

    removed_at = Column(DateTime, default=datetime.now(timezone.utc))
    removed_by = Column(String(15))  # 'user', 'admin', 'moderator'
    removal_reason = Column(String(255))
    recoverable_until = Column(DateTime)


    def to_dict(self):
        return {
            'removed_visit_id': self.removed_visit_id,
            'visit_id': self.visit_id,
            'user_id': self.user_id,
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
            'is_removed': self.is_removed,
            'removed_at': self.removed_at,
            'removed_by': self.removed_by,
            'removal_reason': self.removal_reason,
            'recoverable_until': self.recoverable_until
    }

