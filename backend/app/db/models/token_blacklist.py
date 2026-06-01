from advanced_alchemy.extensions.litestar import base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class TokenBlackList(base.BigIntAuditBase):
    __tablename__ = 'token_black_list'
    
    jti: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    def __repr__(self):
        return f"<Token {self.jti}>"
    