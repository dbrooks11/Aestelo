from exstensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, 
                        String, DateTime, Boolean, Integer)
from sqlalchemy.dialects.postgresql import UUID
import uuid



class AuthUser(db.Model):

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(30), unique=True)
    email = Column(String(150), unique=True, nullable=False)
    password_encrypted = Column(String(255), nullable=False)

    email_confirmed = Column(Boolean, default=False)
    email_confirmed_at = Column(DateTime)
    email_change_sent_at = Column(DateTime)  #for email sending

    password_change_sent_at = Column(DateTime) #for email sending
    password_confirmed_at = Column(DateTime)
    last_sign_in_at = Column(DateTime)

    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)



    user_profile = relationship("UserProfile", backref='auth_user')
    

