from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime)


class User(db.Model):
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'),nullable= False)
    password_hash = Column(String(255), nullable=False)

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        user = ({
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined
        })
        return user