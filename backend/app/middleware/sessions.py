
from litestar.middleware.session.server_side import ServerSideSessionBackend, ServerSideSessionConfig
from litestar.security.session_auth import SessionAuth
from litestar.connection import ASGIConnection
from app.settings import settings
from dataclasses import dataclass
from litestar.exceptions import NotAuthorizedException


auth_paths: dict[str, str] = {
    'login': '/login',
    'signup': '/signup',
    'schema': '/schema',
    'saq': '/saq',
    'refresh': '/refresh'
}

@dataclass
class User:
    id: str

async def retrieve_user_handler(session: dict, connection: ASGIConnection) -> User:

    user_id: str | None = session.get('user_id', None)
    if not user_id:
        raise NotAuthorizedException()
    
    return User(id=user_id)



server_session = ServerSideSessionConfig(
    session_id_bytes=64,
    renew_on_access=False,
    max_age= 14515200, #6 months (in seconds)
    secure=settings.app.SESSION_SECURE, #TODO: set to true for prod
    samesite=settings.app.SESSION_SAMESITE,
    exclude_opt_key='set_session_none'
)


session_auth = SessionAuth[User, ServerSideSessionBackend](
    session_backend_config=server_session,
    retrieve_user_handler=retrieve_user_handler,
    exclude_opt_key='session_auth_none',
    exclude=[auth_paths['login'], auth_paths['signup']],
)