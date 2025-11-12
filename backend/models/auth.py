from exstensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, 
                        String, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *



class AuthUser(db.Model):
    __tablename__: "auth_user"
    __table_args__ = {'schema': auth_user_schema} 

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(150), unique=True, nullable=False)
    password_encrypted = Column(String(255), unique=True, nullable=False)

    email_confirmed = Column(Boolean, default=False)
    email_confirmed_at = Column(DateTime)
    email_change_sent_at = Column(DateTime)  #for email sending

    password_change_sent_at = Column(DateTime) #for email sending
    password_confirmed_at = Column(DateTime)
    last_sign_in_at = Column(DateTime)



    user_profile = relationship("UserProfile", backref='auth_user', lazy=True)
    

