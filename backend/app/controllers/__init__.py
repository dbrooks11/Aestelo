from app.controllers.auth import AuthController
from app.controllers.health import HealthCheckController
from app.controllers.index import IndexController
from app.controllers.s3 import ObjectStorageController
from app.controllers.spot import SpotController
from app.controllers.user import UserController

all_controllers = [
    AuthController,
    HealthCheckController,
    IndexController,
    UserController,
    ObjectStorageController,
    SpotController,
]
