from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *
#TODO: Stuff to do/link to user
#socials
#allow messages from -put in user settings
#circles - for users to be together
#post privacy settings (might go in post.py)
#content_filter_mode
#referal code




class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'schema': user_schema} 
    #removed_user_id = Column(UUID(as_uuid=True), ForeignKey(f'{private}.removed_user.removed_user_id'), nullable=True)
    id = Column(UUID(as_uuid=True), primary_key=True)

    username = Column(String(50), unique=True, nullable=False)
    profile_image = Column(Text)
    bio = Column(String(250))

    instagram = Column(Text)
    is_verified_instagram = Column(Boolean, default=False)

    facebook =Column(Text)
    is_verified_facebook = Column(Boolean, default=False)

    twitter_x= Column(Text)
    is_verified_twitter_x = Column(Boolean, default=False)

    tiktok = Column(Text)
    is_verified_tiktok = Column(Boolean, default=False)

    
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    show_online_status = Column(Boolean, default=False)
    is_business_account = Column(Boolean, default=False)

    
    user_info = relationship('UserInfo', backref='user', lazy=True)
    user_settings = relationship('UserSettings', backref= 'user', lazy=True)
    user_subscription = relationship('UserSubscription', backref= 'user', lazy=True)
    post = relationship('Post', backref='user', lazy=True)
    post_media = relationship('PostMedia', backref='user', lazy=True)
    visit = relationship('Visit', backref='user', lazy=True)
    visit_media = relationship('VisitMedia', backref='user', lazy=True)
    rating = relationship('Rating', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'instagram': self.instagram,
            'is_verified_instagram': self.is_verified_instagram,
            'facebook': self.facebook,
            'is_verified_facebook': self.is_verified_facebook,
            'twitter_x': self.twitter_x,
            'is_verified_twitter_x': self.is_verified_twitter_x,
            'tiktok': self.tiktok,
            'is_verified_tiktok': self.is_verified_tiktok,
            'profile_image': self.profile_image,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'is_private': self.is_private,
            'show_online_status': self.show_online_status,
            'is_business_account': self.is_business_account
    }
       
    
class UserInfo(db.Model):
    __tablename__ = "user_info"
    __table_args__ = {'schema': user_info_schema} 
    id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'),primary_key=True, nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(30))
    date_of_birth = Column(DateTime)
    age = Column(Integer, default=0)
    gender = Column(String(10), default= 'Not specified')
    height_ft = Column(Integer, default=0)
    height_in = Column(Integer, default=0)
    secondary_email = Column(String(150),unique=True)
    preferred_language = Column(String(20))
    state = Column(String(20))
    city = Column(String(25))
    

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'age': self.age,
            'gender': self.gender,
            'height_ft': self.height_ft,
            'height_in': self.height_in,
            'secondary_email': self.secondary_email,
            'preferred_language': self.preferred_language,
            'state': self.state,
            'city': self.city
    }


class UserRole(db.Model):
    __tablename__ = "user_role"
    __table_args__ = {'schema': user_role_schema}
    id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'), primary_key=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_moderator = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)
    granted_at = Column(DateTime, default=datetime.now(timezone.utc))
    granted_by = Column(UUID(as_uuid=True), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'is_admin': self.is_admin,
            'is_moderator': self.is_moderator,
            'is_owner': self.is_owner,
            'granted_at': self.granted_at,
            'granted_by':self.granted_by
        }
        


class UserSettings(db.Model):
    __tablename__ = "user_settings"
    __table_args__ = {'schema': user_settings_schema} 
    id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'), primary_key=True, nullable=False)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    location_sharing = Column(Boolean, default=False)
    data_usage_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean , default=False)
    theme_preference = Column(Boolean, default=True) #True = Dawn mode, False = Twilight Mode (light mode or dark mode)

    def to_dict(self):
        return {
            'id': self.id,
            'email_notifications': self.email_notifications,
            'push_notifications': self.push_notifications,
            'location_sharing': self.location_sharing,
            'data_usage_consent': self.data_usage_consent,
            'marketing_consent': self.marketing_consent,
            'theme_preference': self.theme_preference
    }
    


class UserSubscription(db.Model):
    __tablename__ = "user_subscription"
    __table_args__ = {'schema': user_subscription_schema} 
    id = Column(UUID(as_uuid=True), ForeignKey(f'{user_schema}.user.id'),primary_key=True, nullable=False)
    tier = Column(String(8), default='free') #free, premium, business
    price = Column(Integer)
    started_at= Column(DateTime)
    expires_at = Column(DateTime)
    auto_renew = Column(Boolean, default=False)
    payment_method_id = Column(UUID(as_uuid=True), nullable=True) 
    billing_cycle = Column(String(10), default='monthly')  #monthly or yearly
    trial_used = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tier': self.tier,
            'price': self.price,
            'started_at': self.started_at,
            'expires_at': self.expires_at,
            'auto_renew': self.auto_renew,
            'payment_method_id': self.payment_method_id,
            'billing_cycle': self.billing_cycle,
            'trial_used': self.trial_used
    }


