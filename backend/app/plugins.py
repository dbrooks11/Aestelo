from app.config import config
from litestar.plugins.problem_details import ProblemDetailsPlugin
from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyInitPlugin
from litestar.plugins.structlog import StructlogPlugin
from litestar_email import EmailPlugin
from litestar_saq import SAQPlugin


class Plugins:
    sqlalchemy = SQLAlchemyInitPlugin(config=config.sqlalchemy_config)
    structlog = StructlogPlugin(config=config.structlog_config)
    problem_details = ProblemDetailsPlugin()
    email = EmailPlugin(config=config.email_config)
    saq = SAQPlugin(config=config.saq_config())


plugins = Plugins()
