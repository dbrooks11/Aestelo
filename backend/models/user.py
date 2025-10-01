from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime)


class User(db.Model):
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150),unique=True, nullable=False)
    date_joined = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    last_login = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S'),)
    password_hash = Column(String(255), nullable=False)

    user_info = relationship('user_info', backref= 'user', lazy=True)

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        user = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined
        }
        return user
    
class UserInfo(db.Model):
    user_info_id = Column(BigInteger, primary_key=True)
    age = Column(Integer, default=0)
    gender = Column(String(10), default= 'Not specified')
    height_ft = Column(Integer, default=0)
    height_in = Column(Integer, default=0)

    def to_dict(self):
        user_info = {
            'age': self.age,
            'gender': self.gender,
            'height_ft': self.height_ft,
            'height_in': self.height_in
        }
        return user_info