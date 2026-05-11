from celery import Celery, Task
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix_%(table_name)s_%(all_column_names)s',
    'uq': 'uq_%(table_name)s_%(all_column_names)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}
metadata_db = MetaData(
    naming_convention=convention
)

db = SQLAlchemy(metadata=metadata_db)
ma = Marshmallow()
jwt = JWTManager()
mg = Migrate()
celery = Celery()

if os.getenv('FLASK_ENV') == 'development':
    limiter = Limiter(
        get_remote_address,
        default_limits=["1000 per hour", "30 per minute"],
        storage_uri="memory://"
    )
else:
    limiter = Limiter(
        get_remote_address,
        default_limits=["1000 per hour", "30 per minute"],
        storage_uri=os.environ.get("REDIS"),
        strategy="fixed-window"  
    )

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config, namespace="CELERY")
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app