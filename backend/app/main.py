import app.db.models
from app.config import config
from app.lib.jwt import jwt_cookie_access, jwt_cookie_refresh
from app.plugins import plugins
from app.routes import all_controllers
from app.settings import settings
from app.middleware import middlewares
from pydantic import BaseModel
from litestar import Litestar


app = Litestar(
    cors_config=config.cors_config,
    csrf_config=config.csrf_config,
    openapi_config=config.openapi_config,
    allowed_hosts=config.allowed_host_config,
    route_handlers=all_controllers,
    middleware=middlewares,
    on_app_init=[jwt_cookie_access.on_app_init],
    plugins=[
        plugins.sqlalchemy,
        plugins.email,
        plugins.problem_details,
        plugins.structlog,
    ],
    type_encoders={BaseModel: lambda m: m.model_dump(by_alias=True, exclude_none=True)},
    debug=settings.app.DEBUG,
)



