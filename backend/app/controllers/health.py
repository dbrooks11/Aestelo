from litestar import Response, get
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.exceptions import ServiceUnavailableException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HealthCheckController(Controller):
    path = "/healthz"
    include_in_schema = False

    @get()
    async def health(self) -> Response[str]:
        """
        Verifies the app is healthy
        """
        return Response("Litestar backend application is healthy")

    @get("/db")
    async def health_db(
        self, db_session: NamedDependency[AsyncSession]
    ) -> Response[str]:
        """
        Verifies the app can reach the Database
        """
        try:
            await db_session.execute(select(1))
            return Response("Database is healthy")
        except Exception as e:
            raise ServiceUnavailableException("Database is unhealthy") from e
