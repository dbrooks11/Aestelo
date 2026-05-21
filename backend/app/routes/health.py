from litestar.controller import Controller
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from litestar import get
from litestar.exceptions import InternalServerException



class HealthCheckController(Controller):
    path='/health'

    @get(opt={'access_none':True})
    async def health_check(self, db_session: AsyncSession) -> None:
        """
        Verifies the app can reach the Database and Redis Cloud.
        """

        db_health = await db_session.execute(select(1))

        if not db_health:
            raise InternalServerException()
