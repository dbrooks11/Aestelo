from models import AuthUser, UserProfile, UserInfo, UserRole, UserSettings, UserSubscription, Collection

class DatabaseService:
    @staticmethod
    def create_user_with_stack(session, email: str, username: str, password_encrypted: str):

        auth_user = AuthUser(email=email, username=username, password_encrypted=password_encrypted)
        profile = UserProfile(username=username)

        auth_user.user_profile = profile 
        profile.user_info = UserInfo(email=email)
        profile.user_settings = UserSettings()
        profile.user_role = UserRole()
        profile.user_subscription = UserSubscription()
        
        profile.collection.append(
            Collection(name='Default', is_default=True)
        )

        session.add(auth_user)
        session.commit()
