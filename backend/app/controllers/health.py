from litestar.controller import Controller
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from litestar import get
from litestar.exceptions import ServiceUnavailableException
from litestar import Response
from litestar.di import NamedDependency

class HealthCheckController(Controller):
    path='/healthz'
    include_in_schema=False
    
    @get()
    async def health(self) -> Response[str]:
        """
        Verifies the app is healthy
        """
        return Response('Litestar backend application is healthy')

    @get('/db')
    async def health_db(self, db_session: NamedDependency[AsyncSession]) -> Response[str]:
        """
        Verifies the app can reach the Database
        """
        try:
            await db_session.execute(select(1))
            return Response('Database is healthy')
        except Exception as e:
            raise ServiceUnavailableException('Database is unhealthy') from e        

    

        