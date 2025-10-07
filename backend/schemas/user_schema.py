# schemas/user.py
from app import ma
from models.user import UserProfile, UserInfo, UserRole, UserSettings, UserSubscription
from marshmallow import validates, ValidationError, fields, validate
from datetime import datetime

class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        load_instance = True
        include_fk = True
        exclude = ('is_banned', 'banned_at', 'banned_by', 'banned_reason','num_reports_made','num_reports')  # Hide ban info from users

    id = fields.UUID(dump_only=True)
    profile_created_at = fields.DateTime(dump_only=True)
    follower_count = fields.Int(dump_only=True)
    following_count = fields.Int(dump_only=True)
    post_count = fields.Int(dump_only=True)
    visit_count = fields.Int(dump_only=True)
    
    username = fields.Str(required=True,validate=[validate.Length(min=1, max=50),validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers, and underscores')])
    bio = fields.Str(validate=validate.Length(max=150))
    profile_image= fields.Str(validate=validate.URL())
    instagram= fields.Str(validate=validate.URL())
    facebook= fields.Str(validate=validate.URL())
    tiktok= fields.Str(validate=validate.URL())
    twitter_x= fields.Str(validate=validate.URL())


class UserInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserInfo
        load_instance = True
        include_fk = True
    
    # System-managed
    user_profile_id = fields.UUID(dump_only=True)
    age = fields.Int(dump_only=True)
    first_name = fields.Str(validate=[validate.Length(max=30), validate.Regexp(r"^[a-zA-Z\s'-]+$",error="Name can only contain letters, spaces, apostrophe, and hyphen")])
    last_name = fields.Str(validate=[validate.Length(max=30), validate.Regexp(r"^[a-zA-Z\s'-]+$",error="Name can only contain letters, spaces, apostrophe, and hyphen")])
    email = fields.Email(required=False, validate=validate.Length(max=150))
    phone_number = fields.Str(validate=[validate.Length(max=15), validate.Regexp(r'^[0-9]+$', error='Phone number can only contain numbers')])
    date_of_birth = fields.DateTime()
    gender = fields.Str(
        validate=validate.OneOf([
            'Male', 'Female', 'Non-binary', 
            'Prefer not to say', 'Not specified', 'Other'
        ])
    )
    height_ft = fields.Int(validate=[(validate.Range(min=0,max=10))])
    height_in = fields.Int(validate=[(validate.Range(min=0, max=11))])

    @validates('first_name')
    def validate_first_name(self, value):
        if not value or value.strip() == '':
            return value
        
        apostrophe_count = value.count("'")
        hyphen_count = value.count("-")
        space_count = value.count(' ')

        if apostrophe_count > 1:
            raise ValidationError("Name can only contain one apostrophe")
        if hyphen_count > 1:
            raise ValidationError("Name can only contain one hyphen")
        if space_count > 2:
            raise ValidationError("Name can only contain a few spaces")
        
        if value.startswith(("'", '-')) or value.endswith(("'", '-')):
            raise ValidationError("Name cannot start or end with apostrophe or hyphen")
        
        return value.strip()
    
    @validates('last_name')
    def validate_last_name(self, value):
        if not value or value.strip() == '':
            return value
        
        apostrophe_count = value.count("'")
        hyphen_count = value.count("-")
        space_count = value.count(' ')
        
        if apostrophe_count > 1:
            raise ValidationError("Name can only contain one apostrophe")
        if hyphen_count > 1:
            raise ValidationError("Name can only contain one hyphen")
        if space_count > 3:
            raise ValidationError("Name can only contain a few spaces")
        if value.startswith(("'", '-')) or value.endswith(("'", '-')):
            raise ValidationError("Name cannot start or end with apostrophe or hyphen")
        
        return value.strip()

    @validates('date_of_birth')
    def validate_dob(self, value):
        if value and value > datetime.now():
            raise ValidationError("Date of birth cannot be in the future")
        min_age_date = datetime.now().replace(year=datetime.now().year - 13)
        if value and value > min_age_date:
            raise ValidationError("You must be at least 13 years old")
        return value
   
class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        load_instance = True
        include_fk = True

    user_profile_id = fields.UUID(dump_only=True)
    is_admin = fields.Bool(dump_only=True)
    is_moderator = fields.Bool(dump_only=True)
    is_owner = fields.Bool(dump_only=True)
    granted_at = fields.DateTime(dump_only=True)
    granted_by = fields.UUID(dump_only=True)


class UserSettingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSettings
        load_instance = True
        include_fk = True
    
    user_profile_id = fields.UUID(dump_only=True)
    langauge_preference = fields.Str(validate=validate.OneOf(['english']))


class UserSubscriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSubscription
        load_instance = True
        include_fk = True
 
    user_profile_id = fields.UUID(dump_only=True)
    tier = fields.Str(dump_only=True)
    price = fields.Float(dump_only=True)
    started_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(dump_only=True)
    payment_method_id = fields.UUID(dump_only=True)
    trial_used = fields.Bool(dump_only=True)
    
    auto_renew = fields.Bool()
    billing_cycle = fields.Str(validate=validate.OneOf(['monthly', 'yearly']))
