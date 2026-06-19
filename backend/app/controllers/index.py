from litestar import get
from app.settings import settings
from litestar.controller import Controller


class IndexController(Controller):
    path='/'

    @get(opt={'access_none': True})
    async def app_health_check(self) -> dict[str, str]:
        return {
            "status": "healthy",
            "message": "Aestelo API is running",
            "env": settings.app.ENV,
        }