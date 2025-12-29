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
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=30),
            validate.Regexp(r'^(?!.*\.$)(?!^\.)[a-z0-9._]+$', error='Username can only contain letters, numbers, periods, and underscores')
    ])
    email = fields.Email(
        required=True, 
        validate=[
            validate.Length(min=5, max=150)
    ])
    password = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=min_password_length,max=max_password_length, 
                            error = f"Password must be between {min_password_length} and {max_password_length} characters")], 
                            load_only=True
                    )
    confirm_password = fields.Str(
        required=False, 
        validate=[validate.Length(min=min_password_length,max=max_password_length, 
                                  error = f"Confirmed Password must be between {min_password_length} and {max_password_length} characters")], 
                                  load_only=True
                    )

    
    @validates('password')
    def validate_password(self, value, **kwargs):
        if ' ' in value:
            raise ValidationError('Password cannot contain spaces')
        
    
    @validates_schema
    def validate_passwords(self,data,**kwargs):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match", field_name='confirm_password')
        

email_pass_confirm_pass = AuthUserSchema(only = ('email', 'password', 'confirm_password'))
username_pass_only = AuthUserSchema(only=('username','password'))
email_pass_only = AuthUserSchema(only=('email', 'password'))