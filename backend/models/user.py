from exstensions import db
from flask import current_app
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
#TODO: Stuff to do/link to user_profile
#socials
#allow messages from -put in user_profile settings
#circles - for users to be together
#post privacy settings (might go in post.py)
#content_filter_mode
#referal code




class UserProfile(db.Model):
    
    id = Column(UUID(as_uuid=True), ForeignKey('auth_user.id'), primary_key=True)
    banner_theme = Column(String(30))

    music_track_id = Column(String(50), ForeignKey('music_track.id'))

    username = Column(String(30))
    profile_photo = Column(Text)
    profile_banner = Column(Text)
    bio = Column(String(250))

    instagram = Column(Text)
    is_verified_instagram = Column(Boolean, default=False)

    facebook =Column(Text)
    is_verified_facebook = Column(Boolean, default=False)

    twitter_x= Column(Text)
    is_verified_twitter_x = Column(Boolean, default=False)

    tiktok = Column(Text)
    is_verified_tiktok = Column(Boolean, default=False)

    post_count = Column(Integer, default=0)
    visit_count = Column(Integer, default=0)
    
    follower_count = Column(BigInteger, default=0)
    following_count = Column(BigInteger, default=0)

    is_private = Column(Boolean, default=False)
    show_online_status = Column(Boolean, default=False)
    is_business_account = Column(Boolean, default=False)
    is_prem_account = Column(Boolean, default=False)

    is_banned = Column(Boolean, default=False)
    banned_at = Column(DateTime)
    banned_reason = Column(String(255))
    banned_by = Column(UUID(as_uuid=True))

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

    num_reports_made = Column(Integer, default=0)
    num_reports = Column(Integer, default=0)

    profile_created_at = Column(DateTime, default=datetime.now(timezone.utc))


    user_info = relationship('UserInfo', uselist=False ,backref='user_profile')
    user_settings = relationship('UserSettings', uselist=False ,backref= 'user_profile')
    user_role = relationship('UserRole', uselist=False, backref='user_profile')
    user_subscription = relationship('UserSubscription', uselist=False ,backref= 'user_profile')
    post = relationship('Post', backref='user_profile')
    post_media = relationship('PostMedia', backref='user_profile')
    visit = relationship('Visit', backref='user_profile')
    visit_media = relationship('VisitMedia', backref='user_profile')
    rating = relationship('Rating', backref='user_profile')
    report = relationship('Report', backref='user_profile')
    follower = relationship('Follow',primaryjoin='UserProfile.id == Follow.follower_id',backref='follower')
    following = relationship('Follow',primaryjoin='UserProfile.id == Follow.following_id',backref='following')
    

    def to_dict(self):
        return {
            'id': str(self.user_id),
            'banner_theme': self.banner_theme,
            'music_track_id':self.music_track_id,
            'username': self.username,
            'profile_photo': self.profile_photo,
            'bio': self.bio,
            'instagram': self.instagram,
            'is_verified_instagram': self.is_verified_instagram,
            'facebook': self.facebook,
            'is_verified_facebook': self.is_verified_facebook,
            'twitter_x': self.twitter_x,
            'is_verified_twitter_x': self.is_verified_twitter_x,
            'tiktok': self.tiktok,
            'is_verified_tiktok': self.is_verified_tiktok,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'is_private': self.is_private,
            'show_online_status': self.show_online_status,
            'is_business_account': self.is_business_account,
            'is_banned': self.is_banned,
            'banned_at': self.banned_at,
            'banned_reason': self.banned_reason,
            'num_reports_made': self.num_reports_made,
            'num_reports': self.num_reports,
            'profile_created_at':self.profile_created_at
        }
    def to_dict_public(self):
        return{
            'banner_theme': self.banner_theme,
            'username': self.username,
            'profile_photo': self.profile_photo,
            'bio': self.bio,
            'instagram': self.instagram,
            'facebook': self.facebook,
            'twitter_x': self.twitter_x,
            'tiktok': self.tiktok,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'show_online_status': self.show_online_status,
        }
    def to_dict_private(self):
        return{
            'banner_theme': self.banner_theme,
            'username': self.username,
            'profile_photo': self.profile_photo,
        }
    
    @classmethod
    def active(cls):
        return cls.query.filter_by(is_banned = False, is_deleted = False)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def profile_photo_url(self):
        if not self.profile_photo:
            return None
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{current_app.config['R2_BUCKET_NAME']}/{self.profile_photo}"
        return public_url
    

    @property
    def profile_banner_url(self):
        if not self.profile_banner:
            return None
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{current_app.config['R2_BUCKET_NAME']}/{self.profile_banner}"
        return public_url
        
    
class UserInfo(db.Model):

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'),primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(150))
    date_of_birth = Column(DateTime)
    age = Column(Integer, default=0)
    gender = Column(String(15), default= 'Not specified')
    height_ft = Column(Integer, default=0)
    height_in = Column(Integer, default=0)
    
    state = Column(String(20))
    city = Column(String(25))
    

    def to_dict(self):
        return {
            'user_profile_id': str(self.user_profile_id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'age': self.age,
            'gender': self.gender,
            'height_ft': self.height_ft,
            'height_in': self.height_in,
            'state': self.state,
            'city': self.city
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

class UserRole(db.Model):

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    is_admin = Column(Boolean, default=False)
    is_moderator = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)
    granted_at = Column(DateTime)
    granted_by = Column(UUID(as_uuid=True))

    def to_dict(self):
        return {
            'user_profile_id': str(self.user_profile_id),
            'is_admin': self.is_admin,
            'is_moderator': self.is_moderator,
            'is_owner': self.is_owner,
            'granted_at': self.granted_at,
            'granted_by':self.granted_by
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        


class UserSettings(db.Model):

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    language_preference = Column(String(50))
    email_notifications = Column(Boolean, default=False)
    push_notifications = Column(Boolean, default=False)
    location_sharing = Column(Boolean, default=False)
    data_usage_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean , default=False)
    theme_preference = Column(Boolean, default=True) #True = Dawn mode, False = Twilight Mode (light mode or dark mode)

    def to_dict(self):
        return {
            'user_profile_id': str(self.user_profile_id),
            'email_notifications': self.email_notifications,
            'push_notifications': self.push_notifications,
            'location_sharing': self.location_sharing,
            'data_usage_consent': self.data_usage_consent,
            'marketing_consent': self.marketing_consent,
            'theme_preference': self.theme_preference
    }

    def save(self):
        db.session.add(self)
        db.session.commit()
    


class UserSubscription(db.Model):

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    tier = Column(String(10), default='free') #free, premium, business
    price = Column(Float, default=0.00)
    started_at= Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    auto_renew = Column(Boolean, default=False)
    payment_method_id = Column(UUID(as_uuid=True)) 
    billing_cycle = Column(String(10), default='monthly')  #monthly or yearly
    trial_used = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'user_profile_id': str(self.user_profile_id),
            'tier': self.tier,
            'price': self.price,
            'started_at': self.started_at,
            'expires_at': self.expires_at,
            'auto_renew': self.auto_renew,
            'payment_method_id': self.payment_method_id,
            'billing_cycle': self.billing_cycle,
            'trial_used': self.trial_used
    }

    def save(self):
        db.session.add(self)
        db.session.commit()


