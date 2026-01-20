from exstensions import db
from sqlalchemy import (Column, BigInteger, 
                        String, DateTime, func)

class TokenBlackList(db.Model):
    id = Column(BigInteger, primary_key=True)
    jti = Column(String(64), nullable=False, index=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()