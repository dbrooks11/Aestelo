import random
import uuid
import jwt
from argon2 import PasswordHasher
from app.db.models import (AuthUser, TokenBlackList)
from app.middleware.jwt import jwt_cookie_access, jwt_cookie_refresh
from litestar import Response, post, Request, status_codes
from litestar.exceptions import (
    HTTPException,
    NotAuthorizedException,
    InternalServerException
)
from sqlalchemy.sql.functions import now
from litestar.controller import Controller
from app.settings import settings
from app.schemas.auth import LoginRequestSchema, SignupRequestSchema, AuthServiceSignupSchema
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.params import Body
from litestar.enums import RequestEncodingType
from typing import Annotated
from app.db.models.services.auth import provide_auth_service, AuthService
from litestar.di import Provide

ph = PasswordHasher()

class AuthController(Controller):
    path = "/auth"
    dependencies = {'auth_service': Provide(provide_auth_service)}

    @post('/signup', opt={'csrf_none': True, 'access_none': True, 'refresh_none': True})
    async def signup(self, 
                     data: Annotated[SignupRequestSchema, Body(media_type=RequestEncodingType.MULTI_PART)], 
                     auth_service: AuthService) -> Response:

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
    

    @post('/login', status_code=status_codes.HTTP_200_OK, opt={'csrf_none': True, 'access_none': True, 'refresh_none': True})
    async def login(self, data: Annotated[LoginRequestSchema, Body(media_type=RequestEncodingType.MULTI_PART)], db_session: AsyncSession) -> Response:
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

        response_access = jwt_cookie_access.login(
            identifier=id,
            token_unique_jwt_id=str(uuid.uuid4()),
            response_body={"message": "Login Successful"}
        )

        response_refresh = jwt_cookie_refresh.login(
            token_unique_jwt_id=str(uuid.uuid4()),
            identifier=id,
        )

        for cookie in response_refresh.cookies:
            response_access.cookies.append(cookie)

        return response_access


    @post('/logout')
    async def logout(self, request: Request,  db_session: AsyncSession) -> Response:
        response: Response = Response('Logged out successfully')
        cookies = request.cookies
        revoked_tokens: list[dict[str, str]] = []
        for name, token in cookies.items():
            if name in ['access_token', 'refresh_token']:
                payload = jwt.decode(token, settings.app.JWT_SECRET_KEY, algorithms=['HS256'])
                revoked_tokens.append({'jti': payload.get('jti', '')})
                response.delete_cookie(name)

        await db_session.execute(insert(TokenBlackList).values(revoked_tokens))
        return response


    @post('/refresh', middleware=[jwt_cookie_refresh.middleware])                                           
    async def refresh(self, request: Request) -> Response:
        user_id = request.user.id
        response = jwt_cookie_access.login(
            identifier=user_id,
            token_unique_jwt_id=str(uuid.uuid4),
            response_body={'message': 'Refresh successful'}
        )
        return response