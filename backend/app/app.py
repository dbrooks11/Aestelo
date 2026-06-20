import app.models
from app.config import config
from app.plugins import plugins
from app.controllers import all_controllers
from app.middleware import middlewares
from app.settings import settings
from pydantic import BaseModel
from litestar import Litestar
from app.middleware.sessions import session_auth
from litestar.stores.redis import RedisStore
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape


def serialize_wkb(value: WKBElement) -> str:
    return to_shape(value).wkt


MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

app = Litestar(
    stores={
        "sessions": RedisStore.with_client(
            url=settings.broker.REDIS, namespace="LITESTAR_SESSION"
        )
    },
    cors_config=config.cors_config,
    csrf_config=config.csrf_config,
    openapi_config=config.openapi_config,
    allowed_hosts=config.allowed_host_config,
    route_handlers=all_controllers,
    middleware=middlewares,
    request_max_body_size=MAX_CONTENT_LENGTH,
    on_app_init=[session_auth.on_app_init],
    plugins=[
        plugins.sqlalchemy,
        plugins.email,
        plugins.problem_details,
        plugins.structlog,
        plugins.saq,
    ],
    type_encoders={
        BaseModel: lambda m: m.model_dump(by_alias=True, exclude_none=True),
        WKBElement: serialize_wkb,
    },
    debug=False,
)
