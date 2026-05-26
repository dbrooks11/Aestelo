import logging

import uuid
import structlog
from app.settings import settings
from litestar.config.allowed_hosts import AllowedHostsConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.exceptions import NotAuthorizedException, PermissionDeniedException
from litestar.logging.config import (
    LoggingConfig,
    StructLoggingConfig,
    default_logger_factory,
)
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.openapi.config import OpenAPIConfig
from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    async_autocommit_before_send_handler,
    EngineConfig,
    AlembicAsyncConfig
)
from litestar.plugins.structlog import StructlogConfig
from litestar_email import EmailConfig, ResendConfig, SMTPConfig
from litestar_saq import SAQConfig, QueueConfig
from app.tasks.worker_config_processes import startup, shutdown, before_process, after_process
from app.tasks.profile_tasks import process_profile_media
from app.tasks.post_media_task import process_post_media

class Config:
    @property
    def openapi_config(self) -> OpenAPIConfig:
        return OpenAPIConfig(
            title=settings.app.NAME,
            version=settings.app.VERSION
        )

    @property
    def cors_config(self) -> CORSConfig:
        """Get CORS configuration.

        Returns:
            The CORS configuration.
        """
        return CORSConfig(
            allow_credentials=True,
            allow_methods=["GET", "POST", "PATCH", "DELETE"],
            allow_headers=["Content-Type", "x-csrf-token"],
            allow_origins=settings.app.ALLOWED_CORS_ORIGINS,
            allow_origin_regex=r"http://localhost(:\d+)?$"
        )

    @property
    def allowed_host_config(self) -> AllowedHostsConfig:
        """Get allowed host configuration.

        Returns:
            The allowed host configuration.
        """
        return AllowedHostsConfig(
            allowed_hosts=["localhost"]
        )

    @property
    def sqlalchemy_config(self) -> SQLAlchemyAsyncConfig:
        """Get SQLAlchemy configuration. This desciption also contains the convention 
        for manually settings certain arguments.

        Returns:
            The SQLAlchemy configuration.
        
        db_convention = {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
        """
        return SQLAlchemyAsyncConfig(
            connection_string=settings.db.DATABASE_URL,
            session_config=AsyncSessionConfig(expire_on_commit=False),
            before_send_handler=async_autocommit_before_send_handler,
            engine_config=EngineConfig(
                pool_size=settings.db.POOL_SIZE,
                max_overflow=settings.db.POOL_MAX_OVERFLOW,
                pool_timeout=settings.db.POOL_TIMEOUT,
                pool_recycle=settings.db.POOL_RECYCLE,
                pool_pre_ping=settings.db.POOL_PRE_PING,
                echo=settings.db.ECHO,
                echo_pool=settings.db.ECHO_POOL
            ),
            create_all=True,
            alembic_config=AlembicAsyncConfig(
                script_location=settings.db.MIGRATION_PATH,
                version_table_name=settings.db.MIGRATION_DDL_VERSION_TABLE,
                script_config=settings.db.MIGRATION_CONFIG
            )
        )

    @property
    def csrf_config(self) -> CSRFConfig:
        """Get CSRF configuration.

        Returns:
            The CSRF configuration.
        """
        return CSRFConfig(
            secret=settings.app.SECRET_KEY,
            cookie_secure=settings.app.JWT_COOKIE_SECURE,
            cookie_samesite=settings.app.JWT_COOKIE_SAMESITE,
            exclude_from_csrf_key='csrf_none'
        )
    
    
    def saq_config(self) -> SAQConfig:
        """Get SAQ configuration.

        Returns:
            The SAQ configuration.
        """
        return SAQConfig(
            web_enabled=settings.saq.WEB_ENABLED,
            worker_processes=settings.saq.PROCESSES,
            use_server_lifespan=settings.saq.USE_SERVER_LIFESPAN,
            queue_configs=[
                QueueConfig(
                    name="default",
                    id=f'default_worker_{uuid.uuid4()}',
                    dsn=settings.broker.REDIS,
                    tasks=[],
                    concurrency=settings.saq.CONCURRENCY,
                    startup=startup,
                    shutdown=shutdown,
                    before_process=before_process,
                    after_process=after_process
                ),
                QueueConfig(
                    name="profile_processing",
                    id=f'profile_worker_{uuid.uuid4()}',
                    dsn=settings.broker.REDIS,
                    tasks=[process_profile_media],
                    concurrency=settings.saq.CONCURRENCY,
                    startup=startup,
                    shutdown=shutdown,
                    before_process=before_process,
                    after_process=after_process
                ),
                QueueConfig(
                    name="media_processing",
                    id=f'media_worker_{uuid.uuid4()}',
                    dsn=settings.broker.REDIS,
                    tasks=[process_post_media],
                    concurrency=settings.saq.CONCURRENCY,
                    startup=startup,
                    shutdown=shutdown,
                    before_process=before_process,
                    after_process=after_process
                )
            ],
        )

    @property
    def email_config(self) -> EmailConfig: 
        """Return EmailConfig for the litestar-email plugin.

        As of litestar-email v0.3.0, the backend parameter accepts either
        string ("smtp", "resend").

        Returns:
            The email configuration.
        """
        backend: str | SMTPConfig | ResendConfig = settings.email.BACKEND
        if settings.email.BACKEND == "smtp":
            backend = SMTPConfig(
                host=settings.email.SMTP_HOST,
                port=settings.email.SMTP_PORT,
                username=settings.email.SMTP_USER,
                password=settings.email.SMTP_PASSWORD,
                use_tls=settings.email.USE_TLS,
                use_ssl=settings.email.USE_SSL,
                timeout=settings.email.TIMEOUT,
            )
        elif settings.email.BACKEND == "resend":
            backend = ResendConfig(api_key=settings.email.RESEND_API_KEY)
        return EmailConfig(
            backend=backend,
            from_email=settings.email.FROM_EMAIL,
            from_name=settings.email.FROM_NAME,
        )

    @property
    def structlog_config(self) -> StructlogConfig:
        """Get log configuration

        Returns:
            The log configuration
        """
        from app.lib import log as log_conf

        return StructlogConfig(
            enable_middleware_logging=False,
            structlog_logging_config=StructLoggingConfig(
                log_exceptions="always",
                processors=log_conf.structlog_processors(as_json=not log_conf.is_tty()),
                logger_factory=default_logger_factory(as_json=not log_conf.is_tty()),
                disable_stack_trace={404, 401, 403, NotAuthorizedException, PermissionDeniedException},
                standard_lib_logging_config=LoggingConfig(
                    log_exceptions="always",
                    disable_stack_trace={404, 401, 403, NotAuthorizedException, PermissionDeniedException},
                    root={"level": logging.getLevelName(settings.log.LEVEL), "handlers": ["queue_listener"]},
                    formatters={
                        "standard": {
                            "()": structlog.stdlib.ProcessorFormatter,
                            "processors": log_conf.stdlib_logger_processors(as_json=not log_conf.is_tty()),
                        },
                    },
                    loggers={
                        "saq": {
                            "propagate": False,
                            "level": settings.log.SAQ_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                        "sqlalchemy.engine": {
                            "propagate": False,
                            "level": settings.log.SQLALCHEMY_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                        "sqlalchemy.pool": {
                            "propagate": False,
                            "level": settings.log.SQLALCHEMY_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                        "opentelemetry.sdk.metrics._internal": {
                            "propagate": False,
                            "level": 40,
                            "handlers": ["queue_listener"],
                        },
                        "httpx": {
                            "propagate": False,
                            "level": max(settings.log.LEVEL, logging.WARNING),
                            "handlers": ["queue_listener"],
                        },
                        "httpcore": {
                            "propagate": False,
                            "level": max(settings.log.LEVEL, logging.WARNING),
                            "handlers": ["queue_listener"],
                        },
                        "_granian": {
                            "propagate": False,
                            "level": settings.log.ASGI_ERROR_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                        "granian.server": {
                            "propagate": False,
                            "level": settings.log.ASGI_ERROR_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                        "granian.access": {
                            "propagate": False,
                            "level": settings.log.ASGI_ACCESS_LEVEL,
                            "handlers": ["queue_listener"],
                        },
                    },
                ),
            ),
            middleware_logging_config=LoggingMiddlewareConfig(
                request_log_fields=settings.log.REQUEST_FIELDS,
                response_log_fields=settings.log.RESPONSE_FIELDS,
            ),
        )


config = Config()