from exstensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)


#TODO: Stuff to do/link to user
#socials
#allow messages from -put in user settings
#circles - for users to be together
#post privacy settings (might go in post.py)
#content_filter_mode
#referal code

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'schema': 'auth'} 
    removed_user_id = Column(BigInteger, ForeignKey('removed_user'), nullable=True)
    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'))
    account_locked_until = Column(DateTime)
    is_business_account = Column(Boolean, default=False)
    password_hash = Column(String(255), nullable=False)

    user_info = relationship('UserInfo', backref= 'user', lazy=True)
    user_profile = relationship('UserProfile', backref= 'user', lazy=True)
    user_settings = relationship('UserSettings', backref= 'user', lazy=True)
    user_subscription = relationship('UserSubscription', backref= 'user', lazy=True)
    post = relationship('Post', backref='user', lazy=True)
    post_media = relationship('PostMedia', backref='user', lazy=True)
    visit = relationship('Visit', backref='user', lazy=True)
    visit_media = relationship('VisitMedia', backref='user', lazy=True)


    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined
        }
       
    
class UserInfo(db.Model):
    __tablename__ = "user_info"
    __table_args__ = {'schema': 'public'} 
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    user_info_id = Column(BigInteger, primary_key=True)
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
            'user_info_id': self.user_info_id,
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
        
    
class UserProfile(db.Model):
    __tablename__ = "user_profile"
    __table_args__ = {'schema': 'public'} 
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    profile_id = Column(BigInteger, primary_key=True)
    profile_pic = Column(String())
    bio = Column(String(250))

    instagram = Column(Text)
    is_verified_instagram = Column(Boolean, default=False)

    facebook =Column(Text)
    is_verified_facebook = Column(Boolean, default=False)

    twitter_x= Column(Text)
    is_verified_twitter_x = Column(Boolean, default=False)

    tiktok = Column(Text)
    is_verified_tiktok = Column(Boolean, default=False)

    profile_image = Column(String())
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    show_online_status = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
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
            'show_online_status': self.show_online_status
    }
    


class UserSettings(db.Model):
    __tablename__ = "user_settings"
    __table_args__ = {'schema': 'public'} 
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    user_settings_id = Column(BigInteger, primary_key=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    location_sharing = Column(Boolean, default=False)
    data_usage_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean , default=False)
    theme_preference = Column(Boolean, default=True) #True = Dawn mode, False = Twilight Mode (light mode or dark mode)

    def to_dict(self):
        return {
            'id': self.id,
            'user_settings_id': self.user_settings_id,
            'email_notifications': self.email_notifications,
            'push_notifications': self.push_notifications,
            'location_sharing': self.location_sharing,
            'data_usage_consent': self.data_usage_consent,
            'marketing_consent': self.marketing_consent,
            'theme_preference': self.theme_preference
    }
    


class UserSubscription(db.Model):
    __tablename__ = "user_subscription"
    __table_args__ = {'schema': 'public'} 
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    subscription_id = Column(BigInteger, primary_key=True)
    tier = Column(String(8), default='free') #free, premium, business
    price = Column(Integer)
    started_at= Column(DateTime)
    expires_at = Column(DateTime)
    auto_renew = Column(Boolean, default=False)
    payment_method_id = Column(BigInteger, primary_key=True)
    billing_cycle = Column(Boolean, default=True)  #True = monthly, False = yearly
    trial_used = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'tier': self.tier,
            'price': self.price,
            'started_at': self.started_at,
            'expires_at': self.expires_at,
            'auto_renew': self.auto_renew,
            'payment_method_id': self.payment_method_id,
            'billing_cycle': self.billing_cycle,
            'trial_used': self.trial_used
    }


class RemovedUser(db.Model):
    __tablename__ = "removed_user"
    __table_args__ = {'schema': 'private'} 
    id = relationship('User', backref='removed_user', lazy=True)
    removed_user_id = Column(BigInteger, primary_key=True)
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'))
    account_locked_until = Column(DateTime)
    is_business_account = Column(Boolean, default=False)
    password_hash = Column(String(255), nullable=False)