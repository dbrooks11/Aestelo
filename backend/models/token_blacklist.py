from exstensions import db
from datetime import datetime, timezone
from sqlalchemy import (Column, BigInteger, 
                        String, DateTime)
from .schema_types import *

class TokenBlackList(db.Model):
    __tablename__: 'token_blacklist'
    __table_args__ = {'schema': token_blacklist_schema} 

    id = Column(BigInteger, primary_key=True)
    jti = Column(String(64), nullable=False)
    create_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()