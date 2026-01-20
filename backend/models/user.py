from exstensions import db
from flask import current_app
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean, func)
from sqlalchemy.dialects.postgresql import UUID
#TODO: Stuff to do/link to user_profile
#socials
#allow messages from -put in user_profile settings
#circles - for users to be together
#spot privacy settings (might go in spot.py)
#content_filter_mode
#referal code




class UserProfile(db.Model):
    
    id = Column(UUID(as_uuid=True), ForeignKey('auth_user.id'), primary_key=True)
    music_track_id = Column(Text, ForeignKey('music_track.id'))

    username = Column(Text)
    profile_photo = Column(Text)
    profile_banner = Column(Text)
    bio = Column(Text)

    instagram = Column(Text)
    is_verified_instagram = Column(Boolean, default=False)

    facebook =Column(Text)
    is_verified_facebook = Column(Boolean, default=False)

    twitter_x= Column(Text)
    is_verified_twitter_x = Column(Boolean, default=False)

    tiktok = Column(Text)
    is_verified_tiktok = Column(Boolean, default=False)

    spot_count = Column(Integer, default=0)
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
    deleted_at = Column(DateTime(timezone=True))

    num_reports_made = Column(Integer, default=0)
    num_reports = Column(Integer, default=0)

    profile_created_at = Column(DateTime, server_default=func.now())


    user_info = relationship('UserInfo', uselist=False ,backref='user_profile')
    user_settings = relationship('UserSettings', uselist=False ,backref= 'user_profile')
    user_role = relationship('UserRole', uselist=False, backref='user_profile')
    user_subscription = relationship('UserSubscription', uselist=False ,backref= 'user_profile')
    spot = relationship('Spot', backref='user_profile')
    spot_media = relationship('SpotMedia', backref='user_profile')
    visit = relationship('Visit', backref='user_profile')
    visit_media = relationship('VisitMedia', backref='user_profile')
    rating = relationship('Rating', backref='user_profile')
    report = relationship('Report', backref='user_profile')
    follower = relationship('Follow',primaryjoin='UserProfile.id == Follow.follower_id',backref='follower')
    following = relationship('Follow',primaryjoin='UserProfile.id == Follow.following_id',backref='following')
    
    
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
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{self.profile_photo}"
        return public_url
    

    @property
    def profile_banner_url(self):
        if not self.profile_banner:
            return None
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{self.profile_banner}"
        return public_url
        
    
class UserInfo(db.Model):

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profile.id'),primary_key=True)
    first_name = Column(Text) #limit to 30
    last_name = Column(Text) #limit to 30
    email = Column(Text) #limit to 150 chars when checking
    date_of_birth = Column(DateTime(timezone=True))
    age = Column(Integer, default=0)
    gender = Column(Text, default= 'Not specified')
    height_ft = Column(Integer, default=0)
    height_in = Column(Integer, default=0)
    
    state = Column(Text)
    city = Column(Text)
    

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
    granted_at = Column(DateTime(timezone=True))
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
    language_preference = Column(Text)
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
    tier = Column(Text, default='free') #free, premium, business
    price = Column(Float, default=0.00)
    started_at= Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    auto_renew = Column(Boolean, default=False)
    payment_method_id = Column(UUID(as_uuid=True)) 
    billing_cycle = Column(Text, default='monthly')  #monthly or yearly
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


