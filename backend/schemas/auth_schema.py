# schemas/auth_schema.py
from exstensions import ma, db
from models.auth import AuthUser
from marshmallow import validates,validates_schema, ValidationError, fields, validate
from sqlalchemy import exists
from datetime import datetime


min_password_length = 8
max_password_length = 64
    
class AuthUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthUser

    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True,validate=[validate.Length(min=1, max=50),validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers, and underscores')])
    email = fields.Email(required=True, validate=[(validate.Length(min=5, max=150), validate.Email)])
    password = fields.String(required=True, validate=[validate.Length(min=min_password_length,max=max_password_length, error = f"Password must be between {min_password_length} and {max_password_length} characters")], load_only=True)
    confirm_password = fields.String(required=False, validate=[validate.Length(min=min_password_length,max=max_password_length, error = f"Confirmed Password must be between {min_password_length} and {max_password_length} characters")], load_only=True)


    @validates('username')
    def validate_username(self, value, **kwargs):
        existing_user = db.session.query(exists().where(AuthUser.username == value)).scalar()
        
        if existing_user:
            raise ValidationError('Username already exists')
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        if value.contains(' '):
            raise ValidationError('Password cannot contain spaces')
        
    
    @validates_schema
    def validate_passwords(self,data,**kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match", field_name= 'confirm_password')
        

email_pass_confirm_pass = AuthUserSchema(only = ('email', 'password', 'confirm_password'))
username_pass_only = AuthUserSchema(only=('username','password'))
email_pass_only = AuthUserSchema(only=('email', 'password'))