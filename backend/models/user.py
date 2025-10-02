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
    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'))
    account_locked_until = Column(DateTime)
    password_hash = Column(String(255), nullable=False)

    user_info = relationship('UserInfo', backref= 'user', lazy=True)

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        user = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined
        }
        return user
    
class UserInfo(db.Model):
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
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        user_info = {
            'age': self.age,
            'gender': self.gender,
            'height_ft': self.height_ft,
            'height_in': self.height_in
        }
        return user_info
    
class UserProfile(db.Model):
    profile_id = Column(BigInteger, primary_key=True)
    bio = Column(String(250))
    profile_image = Column(String())
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    show_online_status = Column(Boolean, default=False)
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)


class UserSettings(db.Model):
    user_settings_id = Column(BigInteger, primary_key=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    location_sharing = Column(Boolean, default=False)
    data_usage_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean , default=False)
    theme_preference = Column(Boolean, default=True) #True = Dawn mode, False = Twilight Mode (light mode or dark mode)
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)


class UserSubscription(db.Model):
    subscription_id = Column(BigInteger, primary_key=True)
    tier = Column(String(8), default='free') #free, premium, business
    started_at= Column(DateTime)
    expires_at = Column(DateTime)
    auto_renew = Column(Boolean, default=False)
    payment_method_id = Column(BigInteger, primary_key=True)
    billing_cycle = Column(Boolean, default=True)  #True = monthly, False = yearly
    trial_used = Column(Boolean, default=False)
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

