from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from sqlalchemy import MetaData
from celery import Celery, Task
from flask import Flask

convention = {
    "ix": 'ix_%(column_0_name)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata_db = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata_db)
ma = Marshmallow()
jwt = JWTManager()
mg = Migrate()
celery = Celery()

# TODO: use redis for rate limit storage
limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "10000 per hour"],
    storage_uri="memory://", #This URI is only meant for testing/development and 
                            #should be replaced with an appropriate storage of your choice before moving to production.
    )

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app