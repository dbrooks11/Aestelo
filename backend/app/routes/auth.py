import random
from argon2 import PasswordHasher
from app.db.models import (AuthUser)
from litestar import Response, post, Request, status_codes,get
from litestar.exceptions import (
    HTTPException,
    NotAuthorizedException,
    InternalServerException
)
from sqlalchemy.sql.functions import now
from litestar.controller import Controller
from app.settings import settings
from app.schemas.auth import LoginRequestSchema, SignupRequestSchema, AuthServiceSignupSchema
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.services.auth import provide_auth_service, AuthService
from litestar.di import Provide
from litestar.middleware.csrf import generate_csrf_token

ph = PasswordHasher()

class AuthController(Controller):
    path = "/auth"
    dependencies = {'auth_service': Provide(provide_auth_service)}

    @post('/signup', opt={'csrf_none': True})
    async def signup(self, 
                     data: SignupRequestSchema, 
                     auth_service: AuthService
                     ) -> Response:

        exist = await auth_service.exists(email = data.email)

        if exist:
            raise HTTPException(detail='Email already exists', status_code=409)
        
        count: int = 0
        exist_username: bool = False
        username: str = ''
        while count < 3:
            username = f'user{random.randint(1, 999999999999999999999999)}'
            exist_username = await auth_service.exists(username=username)

            if exist_username:
                count += 1
            else:
                break
        
        if exist_username:
            raise InternalServerException(detail='Failed to create an account. Please try again.')
            
        data_dict = data.model_dump()
        data_dict['username'] = username
        
        await auth_service.create_account(data=AuthServiceSignupSchema.model_validate(data_dict))
        return Response(content='Account created successfully')
    

    @post('/login', opt={'csrf_none': True})
    async def login(self, 
                    data: LoginRequestSchema, 
                    db_session: AsyncSession, 
                    request: Request
                    ) -> dict[str, str | None]:
        account = await db_session.execute(select(AuthUser.id, AuthUser.password_hash).where(
            (AuthUser.email == data.email) | 
            (AuthUser.username == data.username))
        )
        row = account.first()
        if not row:
            raise NotAuthorizedException()
        
        id, password_hash = row
        if not all([id, password_hash]):
            ph.verify('dummy_hash_string', data.password)
            raise NotAuthorizedException()

        id = str(id)
        ph.verify(password_hash, data.password)

        update_fields: dict[str, str | now] = {
            'last_signed_in': func.now()
        }

        if ph.check_needs_rehash(password_hash):
            update_fields['password_hash'] = ph.hash(data.password)
        
        await db_session.execute(update(AuthUser).where(
                (AuthUser.email == data.email) | 
                (AuthUser.username == data.username)
            ).values(**update_fields))

        request.set_session({'user_id': id})
        session_id = request.get_session_id()
        return {'session': session_id}

    @post('/sign-out')
    async def signout(self, request: Request) -> Response:
        request.clear_session()
        return Response('Sign out successful')

    @get('/csrf', opt={'set_session_none': True, 'session_auth_none': True})
    async def get_csrf(self) -> str:
        token: str = generate_csrf_token(secret=settings.app.SECRET_KEY)
        return token