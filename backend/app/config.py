import uuid
from app.settings import settings

from litestar.config.allowed_hosts import AllowedHostsConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.logging.config import (
    StructLoggingConfig
)
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.openapi.config import OpenAPIConfig
from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    AlembicAsyncConfig,
    async_autocommit_before_send_handler
)
from advanced_alchemy.extensions.litestar.plugins import (
    SQLAlchemyAsyncConfig,
    EngineConfig
)
from litestar.plugins.structlog import StructlogConfig
from litestar_email import EmailConfig, ResendConfig, SMTPConfig
from litestar_saq import SAQConfig, QueueConfig
from app.tasks.worker import startup, shutdown, before_process, after_process
from app.tasks.profile import process_profile_media
from app.tasks.media import process_post_pipeline
from litestar.openapi.plugins import ScalarRenderPlugin


class Config:
    @property
    def openapi_config(self) -> OpenAPIConfig:
        return OpenAPIConfig(
        title=settings.app.NAME,
        version=settings.app.VERSION,
        render_plugins=[
            ScalarRenderPlugin(
                options={
                    "persistAuth": True,
                    'withCredentials': True,
                }
            )
        ],
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
            allowed_hosts=["localhost:8000", "10.150.176.90:8000", "testserver.local"]
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
            alembic_config=AlembicAsyncConfig(compare_type=True)
        )

    @property
    def csrf_config(self) -> CSRFConfig:
        """Get CSRF configuration.

        Returns:
            The CSRF configuration.
        """
        return CSRFConfig(
            secret=settings.app.SECRET_KEY,
            header_name='x-csrf-token',
            cookie_secure=settings.app.CSRF_COOKIE_SECURE,
            cookie_samesite=settings.app.CSRF_COOKIE_SAMESITE,
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
                    tasks=[process_post_pipeline],
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

        return StructlogConfig(
            middleware_logging_config=LoggingMiddlewareConfig(
                response_cookies_to_obfuscate={'csrftoken', 'access_token', 'refresh_token'},
                response_headers_to_obfuscate={'cookie', 'x-csrftoken'},
                request_cookies_to_obfuscate={'csrftoken', 'access_token', 'refresh_token'},
                request_headers_to_obfuscate={'cookie', 'x-csrftoken'},
                request_log_fields=('path', 'method', 'content_type', 'headers', 'query', 'path_params', 'body'),
                response_log_fields=("status_code", "headers", "body"),
                exclude=['/saq']
            ),
            structlog_logging_config=StructLoggingConfig(
                log_exceptions='always',
                disable_stack_trace={404, ValueError}
            )
        )


config = Config()