# schemas/auth_schema.py
from app.extensions import ma
from marshmallow import ValidationError, fields, validate, validates, validates_schema
from models.auth import AuthUser

min_password_length = 8
max_password_length = 64

min_username_length = 1
max_username_length = 30
    
class AuthUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthUser
    
    name = fields.Str()

    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=min_username_length, max=max_username_length, error= f"Username must be between {min_username_length} and {max_username_length} characters")
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
    
    @validates("name")
    def name_field(self, value, **kwargs):
        if value:
            raise ValidationError("Invalid Input(b)")
        
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