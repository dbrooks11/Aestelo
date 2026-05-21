from app.routes.auth import AuthController
from app.routes.health import HealthCheckController
from app.routes.index import IndexController
from app.routes.profile import ProfileController

all_controllers = [
    AuthController,
    HealthCheckController,
    IndexController,
    ProfileController,
]