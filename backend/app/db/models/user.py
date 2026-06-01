from typing import TYPE_CHECKING, Optional
import uuid
from advanced_alchemy.extensions.litestar import base
from app.settings import settings

if TYPE_CHECKING:
    from models import (
        AuthUser,
        Collection,
        Follow,
        Likes,
        Rating,
        Report,
        Spot,
        Visit,
    )
from app.db.enum_schemas import (
    LanguagePreferenceEnum,
    UserGenderEnum,
    UserRoleEnum,
    UserSubscriptionBillCycleEnum,
    UserSubscriptionTierEnum,
)
from sqlalchemy import (
    UUID,
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    String,
    Enum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from advanced_alchemy.types import DateTimeUTC
from app.lib.validation import validate


class UserProfile(base.UUIDAuditBase):
    __tablename__ = 'user_profile'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('auth_user.id', ondelete='CASCADE'), primary_key=True)
    avatar: Mapped[Optional[str]] = mapped_column(Text)
    banner: Mapped[Optional[str]] = mapped_column(Text)
    bio: Mapped[Optional[str]] = mapped_column(String(validate.MAX_PROFILE_BIO_LENGTH))

    spot_count: Mapped[int] = mapped_column(Integer, default=0)
    visit_count: Mapped[int] = mapped_column(Integer, default=0)
    follower_count: Mapped[int] = mapped_column(BigInteger, default=0)
    following_count: Mapped[int] = mapped_column(BigInteger, default=0)

    # Account Status
    is_private: Mapped[bool] = mapped_column(default=False)
    show_online_status: Mapped[bool] = mapped_column(default=False)
    is_business_account: Mapped[bool] = mapped_column(default=False)
    is_prem_account: Mapped[bool] = mapped_column(default=False)

    # Banning & Moderation
    is_banned: Mapped[bool] = mapped_column(default=False)
    banned_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    banned_reason: Mapped[Optional[str]] = mapped_column(Text)
    banned_by: Mapped[Optional[uuid.UUID]] = mapped_column(default=None)

    # Soft Deletion & Reports
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)

    auth: Mapped['AuthUser'] = relationship(back_populates='profile', lazy='joined')
    info: Mapped["UserInfo"] = relationship(back_populates="profile", lazy='joined')
    settings: Mapped["UserSettings"] = relationship(back_populates="profile", lazy='joined')
    role: Mapped["UserRole"] = relationship(back_populates="profile", lazy='joined')
    subscription: Mapped["UserSubscription"] = relationship(back_populates="profile", lazy='joined')
    spot: Mapped[list["Spot"]] = relationship(back_populates="profile", lazy='selectin')
    visit: Mapped[list["Visit"]] = relationship(back_populates="profile", lazy='selectin')
    rating: Mapped[list["Rating"]] = relationship(back_populates="profile", lazy='selectin')
    report: Mapped[list["Report"]] = relationship(back_populates="profile")
    collection: Mapped[list["Collection"]] = relationship(back_populates="profile", lazy='selectin')
    follower: Mapped[list["Follow"]] = relationship(foreign_keys="Follow.follower_id", back_populates="follower", lazy='selectin')
    following: Mapped[list["Follow"]] = relationship(foreign_keys="Follow.following_id", back_populates="following", lazy='selectin')
    likes: Mapped[list["Likes"]] = relationship(back_populates='profile', lazy='selectin')
    
    @hybrid_property
    def avatar_url(self) -> str | None:
        if self.avatar:
            return f"https://{settings.storage.SUB_DOMAIN}/{self.avatar}"
        return None

    @hybrid_property
    def banner_url(self) -> str | None:
        if self.banner:
            return f"https://{settings.storage.SUB_DOMAIN}/{self.banner}"
        return None
    
class UserInfo(base.DefaultBase):
    __tablename__ = 'user_info'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)

    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)

    date_of_birth: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    age: Mapped[int] = mapped_column(Integer, default=0)
    gender: Mapped[UserGenderEnum] = mapped_column(Enum(UserGenderEnum), default=UserGenderEnum.NOT_SPECIFIED)
    
    height_ft: Mapped[int] = mapped_column(Integer, default=0)
    height_in: Mapped[int] = mapped_column(Integer, default=0)

    state: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)

    profile: Mapped["UserProfile"] = relationship(back_populates="info", lazy='joined')

class UserRole(base.DefaultBase):
    __tablename__ = 'user_role'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    granted_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    granted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))

    profile: Mapped["UserProfile"] = relationship(back_populates="role", lazy='joined')

class UserSettings(base.DefaultBase):
    __tablename__ = 'user_settings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)
    language_preference: Mapped[Optional[LanguagePreferenceEnum]] = mapped_column(Enum(LanguagePreferenceEnum), default=LanguagePreferenceEnum.ENGLISH)
    email_notifications: Mapped[bool] = mapped_column(default=False)
    push_notifications: Mapped[bool] = mapped_column(default=False)
    location_sharing: Mapped[bool] = mapped_column(default=False)
    data_usage_consent: Mapped[bool] = mapped_column(default=False)
    marketing_consent: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["UserProfile"] = relationship(back_populates="settings", lazy='joined')
    
class UserSubscription(base.DefaultBase):
    __tablename__ = 'user_subscription'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)
    tier: Mapped[UserSubscriptionTierEnum] = mapped_column(Enum(UserSubscriptionTierEnum), default=UserSubscriptionTierEnum.FREE)
    price: Mapped[float] = mapped_column(Float, default=0.00)
    started_at: Mapped[DateTime] = mapped_column(DateTimeUTC, server_default=func.now())
    expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTimeUTC)
    auto_renew: Mapped[bool] = mapped_column(default=False)
    payment_method_id: Mapped[Optional[uuid.UUID]] = mapped_column() 
    billing_cycle: Mapped[UserSubscriptionBillCycleEnum] = mapped_column(Enum(UserSubscriptionBillCycleEnum), default=UserSubscriptionBillCycleEnum.MONTHLY)
    trial_used: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["UserProfile"] = relationship(back_populates="subscription", lazy='joined')