from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from app.settings import settings
from app.db.models import  TokenBlackList
from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTCookieAuth, Token
from sqlalchemy import select
from app.config import config

auth_paths: dict[str, str] = {
    'login': '/login',
    'signup': '/signup',
    'schema': '/schema',
    'saq': '/saq',
    'refresh': '/refresh'
}


@dataclass
class CookieUser:
    """Minimal user object for authenticated requests."""
    id: str


async def retrieve_user_handler(token: Token,  connection: ASGIConnection[Any, Any, Any, Any]) -> CookieUser | None:
    """
    Create user from JWT claims - NO DATABASE QUERY.
    The token already contains the user ID.
    """
    if not token.sub:
        return None
    
    return CookieUser(id=token.sub)

async def revoked_token_hander(token: Token, connection: ASGIConnection[Any, Any, Any, Any]) -> bool:
    """
    Check if token is revoked - Database Query via Token Black List 
    The token is considered revoked (True) if it exist in the database. Otherwise, false.
    """
    if token:
        jti = token.jti
        session = config.sqlalchemy_config.create_session_maker()  
        async with session() as session:
            exist = await session.scalar(select(1).where(TokenBlackList.jti == jti))
        return exist is not None


jwt_cookie_access = JWTCookieAuth[CookieUser](
    key='access_token',
    token_secret=settings.app.JWT_SECRET_KEY,
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_hander,
    default_token_expiration=timedelta(seconds=settings.app.JWT_ACCESS_TOKEN_EXPIRES),
    secure=settings.app.JWT_COOKIE_SECURE,
    samesite=settings.app.JWT_COOKIE_SAMESITE,
    exclude=[auth_paths['refresh'], auth_paths['schema'], auth_paths['saq']], #TODO: remove schema and saq paths
    exclude_opt_key='access_none'
)


jwt_cookie_refresh = JWTCookieAuth[CookieUser](
    key='refresh_token',
    token_secret=settings.app.JWT_SECRET_KEY,
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_hander,
    default_token_expiration=timedelta(seconds=settings.app.JWT_REFRESH_TOKEN_EXPIRES),
    secure=settings.app.JWT_COOKIE_SECURE,
    samesite=settings.app.JWT_COOKIE_SAMESITE,
    exclude_opt_key='refresh_none'
)

