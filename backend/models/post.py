from exstensions import db
from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
#todo: Create post model
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
    post_id = Column(BigInteger, primary_key=True)
    posted_by = Column(String(50), nullable= False)
    date_posted = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String(200), default='', nullable=False)

    rating = relationship('Rating', backref='post', lazy=True)


class Rating(db.Model):
    rating_id = Column(BigInteger, primary_key=True)
    post_id = Column(BigInteger, ForeignKey('post.post_id'), nullable=False)
    average_rating = Column(Float)
    total_rating = Column(Float, default=0.0)
    rating_choice = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_rated_at = Column(DateTime, default=datetime.now(timezone.utc))