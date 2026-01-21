from sqlalchemy import event
from sqlalchemy.orm import object_session
from models.auth import AuthUser
from models.user import UserProfile, UserInfo, UserRole, UserSettings, UserSubscription
from models.collection import Collection

@event.listens_for(AuthUser, 'after_insert')
def create_entire_user_stack(mapper, connection, target):
    """
    Runs after a new AuthUser is inserted.
    """
    session = object_session(target)
    user_id = target.id
    user_email = target.email
    user_username = target.username

    profile = UserProfile(id=user_id, username=user_username)
    
    info = UserInfo(user_id=user_id, email=user_email)
    settings = UserSettings(user_id=user_id)
    role = UserRole(user_id=user_id)
    sub = UserSubscription(user_id=user_id)
    
    default_collection = Collection(
        user_id=user_id,
        name='Default',
        is_default=True
    )

    session.add_all([profile, info, settings, role, sub, default_collection])