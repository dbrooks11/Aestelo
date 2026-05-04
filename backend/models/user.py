import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from extensions import db

if TYPE_CHECKING:
    from models import (
        AuthUser,
        Collection,
        Follow,
        Rating,
        Report,
        Spot,
        SpotMedia,
        Visit,
        VisitMedia,
        Likes
    )
from flask import current_app
from sqlalchemy import (
    UUID,
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

#TODO: Stuff to do/link to user_profile
#socials
#allow messages from -put in user_profile settings
#circles - for users to be together
#spot privacy settings (might go in spot.py)
#content_filter_mode
#referal code




class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    music_track_id: Mapped[Optional[str]] = mapped_column(Text, ForeignKey('music_track.id'))

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('auth_user.id'), primary_key=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    profile_photo: Mapped[Optional[str]] = mapped_column(Text)
    profile_banner: Mapped[Optional[str]] = mapped_column(Text)
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Social Media
    instagram: Mapped[Optional[str]] = mapped_column(Text)
    is_verified_instagram: Mapped[bool] = mapped_column(default=False)

    facebook: Mapped[Optional[str]] = mapped_column(Text)
    is_verified_facebook: Mapped[bool] = mapped_column(default=False)

    twitter_x: Mapped[Optional[str]] = mapped_column(Text)
    is_verified_twitter_x: Mapped[bool] = mapped_column(default=False)

    tiktok: Mapped[Optional[str]] = mapped_column(Text)
    is_verified_tiktok: Mapped[bool] = mapped_column(default=False)

    # Counters
    spot_count: Mapped[int] = mapped_column(default=0)
    visit_count: Mapped[int] = mapped_column(default=0)
    follower_count: Mapped[int] = mapped_column(BigInteger, default=0)
    following_count: Mapped[int] = mapped_column(BigInteger, default=0)

    # Account Status
    is_private: Mapped[bool] = mapped_column(default=False)
    show_online_status: Mapped[bool] = mapped_column(default=False)
    is_business_account: Mapped[bool] = mapped_column(default=False)
    is_prem_account: Mapped[bool] = mapped_column(default=False)

    # Banning & Moderation
    is_banned: Mapped[bool] = mapped_column(default=False)
    banned_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    banned_reason: Mapped[Optional[str]] = mapped_column(Text)
    banned_by: Mapped[Optional[uuid.UUID]] = mapped_column(default=None)

    # Soft Deletion & Reports
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    num_reports_made: Mapped[int] = mapped_column(default=0)
    num_reports: Mapped[int] = mapped_column(default=0)

    # Timestamps
    profile_created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    auth: Mapped['AuthUser'] = relationship('AuthUser', back_populates='user_profile')
    user_info: Mapped["UserInfo"] = relationship("UserInfo", uselist=False, back_populates="user_profile")
    user_settings: Mapped["UserSettings"] = relationship("UserSettings", uselist=False, back_populates="user_profile")
    user_role: Mapped["UserRole"] = relationship("UserRole", uselist=False, back_populates="user_profile")
    user_subscription: Mapped["UserSubscription"] = relationship("UserSubscription", uselist=False, back_populates="user_profile")
    spot: Mapped[list["Spot"]] = relationship("Spot", back_populates="user_profile")
    spot_media: Mapped[list["SpotMedia"]] = relationship("SpotMedia", back_populates="user_profile")
    visit: Mapped[list["Visit"]] = relationship("Visit", back_populates="user_profile")
    visit_media: Mapped[list["VisitMedia"]] = relationship("VisitMedia", back_populates="user_profile")
    rating: Mapped[list["Rating"]] = relationship("Rating", back_populates="user_profile")
    report: Mapped[list["Report"]] = relationship("Report", back_populates="user_profile")
    collection: Mapped[list["Collection"]] = relationship("Collection", back_populates="user_profile")
    follower: Mapped[list["Follow"]] = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    following: Mapped[list["Follow"]] = relationship("Follow", foreign_keys="Follow.following_id", back_populates="following")
    likes: Mapped[list["Likes"]] = relationship("Likes", back_populates='user_profile')
    
    @classmethod
    def active(cls):
        return cls.query.filter_by(is_banned = False, is_deleted = False)
    
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
    __tablename__ = 'user_info'
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)

    # Name & Email
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)

    # Personal Details
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    age: Mapped[int] = mapped_column(Integer, default=0)
    gender: Mapped[str] = mapped_column(Text, default='Not specified')
    
    # Physical attributes
    height_ft: Mapped[int] = mapped_column(Integer, default=0)
    height_in: Mapped[int] = mapped_column(Integer, default=0)

    # Location
    state: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)

    user_profile: Mapped["UserProfile"] = relationship(UserProfile, back_populates="user_info")

class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_moderator: Mapped[bool] = mapped_column(default=False)
    is_owner: Mapped[bool] = mapped_column(default=False)
    granted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    granted_by: Mapped[Optional[uuid.UUID]] = mapped_column()

    user_profile: Mapped["UserProfile"] = relationship(UserProfile, back_populates="user_role")
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    language_preference: Mapped[Optional[str]] = mapped_column(Text)
    email_notifications: Mapped[bool] = mapped_column(default=False)
    push_notifications: Mapped[bool] = mapped_column(default=False)
    location_sharing: Mapped[bool] = mapped_column(default=False)
    data_usage_consent: Mapped[bool] = mapped_column(default=False)
    marketing_consent: Mapped[bool] = mapped_column(default=False)
    theme_preference: Mapped[bool] = mapped_column(default=True)

    user_profile: Mapped["UserProfile"] = relationship(UserProfile, back_populates="user_settings")
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id'), primary_key=True)
    tier: Mapped[str] = mapped_column(Text, default='free')
    price: Mapped[float] = mapped_column(Float, default=0.00)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    auto_renew: Mapped[bool] = mapped_column(default=False)
    payment_method_id: Mapped[Optional[uuid.UUID]] = mapped_column() 
    billing_cycle: Mapped[str] = mapped_column(Text, default='monthly')
    trial_used: Mapped[bool] = mapped_column(default=False)

    user_profile: Mapped["UserProfile"] = relationship(UserProfile, back_populates="user_subscription")

    def save(self):
        db.session.add(self)
        db.session.commit()