from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import Final, Literal, ClassVar

import structlog
from litestar.data_extractors import RequestExtractorField, ResponseExtractorField
from litestar.utils.module_loader import module_to_os_path
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.__metadata__ import __version__ as current_version

ENV_FILE = 'backend/.env'
ENV_ENCODING = 'utf-8'
DEFAULT_MODULE_NAME = "app"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    ECHO: bool = False
    """Enable SQLAlchemy engine logs."""
    ECHO_POOL: bool = False
    """Enable SQLAlchemy connection pool logs."""
    POOL_DISABLED: bool = False
    """Disable SQLAlchemy pool configuration."""
    POOL_MAX_OVERFLOW: int = 10
    """Max overflow for SQLAlchemy connection pool"""
    POOL_SIZE: int = 10
    """Pool size for SQLAlchemy connection pool"""
    POOL_TIMEOUT: int = 30
    """Time in seconds for timing connections out of the connection pool."""
    POOL_RECYCLE: int = 300
    """Amount of time to wait before recycling connections."""
    POOL_PRE_PING: bool = True
    """Optionally ping database before fetching a session from the connection pool."""
    POSTGRES_USER: str = ""
    """User/username for the postgres"""
    POSTGRES_DB: str = ""
    """Database name for postgres"""
    POSTGRES_PASSWORD: str = ""
    """Database password for postgres"""
    POSTGRES_PORT: int = 5432
    """Database port"""
    POSTGRES_HOST: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """SQLAlchemy Database URL."""
        url = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url
    


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='SERVER_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    """Server configurations."""
    APP_LOC: str = "app.main:app"
    """Path to app executable or factory."""
    HOST: str = "0.0.0.0"
    """Server network host."""
    PORT: int = 8000
    """Server port."""
    KEEPALIVE: int = 65
    """Seconds to hold connections open (65 is > AWS lb idle timeout)."""
    RELOAD: bool = False
    """Turn on hot reloading."""



class SaqSettings(BaseSettings):
    """SAQ (Simple Async Queue) configuration using Redis as broker."""
    model_config = SettingsConfigDict(
        env_prefix='SAQ_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    PROCESSES: int = 1
    """The number of worker processes to start.

    Default is set to 1.
    """
    CONCURRENCY: int = 10
    """The number of concurrent jobs allowed to execute per worker process.

    Default is set to 10.
    """
    WEB_ENABLED: bool = True
    """If true, the worker admin UI is hosted on worker startup."""
    USE_SERVER_LIFESPAN: bool = True
    """Auto start and stop `saq` processes when starting the Litestar application."""

    



class EmailSettings(BaseSettings):
    """Email configuration.

    Set EMAIL_BACKEND to:
    - "console" (default) - prints emails to stdout (development)
    - "memory" - stores in memory (testing)
    - "smtp" - sends via SMTP server
    - "resend" - sends via Resend API (production)
    """
    model_config = SettingsConfigDict(
        env_prefix='EMAIL_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )
    

    BACKEND: str = "console"
    """Email backend: console, memory, smtp, resend."""
    FROM_EMAIL: str = "noreply@localhost"
    """Default from email address."""
    FROM_NAME: str = "Litestar App"
    """Default from name."""

    
    # SMTP settings (only used when BACKEND="smtp")
    SMTP_HOST: str = "localhost"
    """SMTP server hostname."""
    SMTP_PORT: int = 587
    """SMTP server port."""
    SMTP_USER: str = ""
    """SMTP username."""
    SMTP_PASSWORD: str = ""
    """SMTP password."""
    USE_TLS: bool = True
    """Use TLS for SMTP connection."""
    USE_SSL: bool = False
    """Use SSL for SMTP connection."""
    TIMEOUT: int = 30
    """SMTP connection timeout in seconds."""
    RESEND_API_KEY: str = ""
    """Resend API key for production email sending."""




class AppSettings(BaseSettings):
    """Application configuration"""
    model_config = SettingsConfigDict(
        env_prefix='APP_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    ENV: str = "development"
    """Application Environment"""
    DEBUG: bool = True
    """Enables Debug (Disable for production)"""
    NAME: str = ""
    """Application name."""
    VERSION: str = f"v{current_version}"
    """Current application"""
    CONTACT_NAME: str = "Admin"
    """Application contact name"""
    CONTACT_EMAIL: str = "admin@localhost"
    """Application contact email"""
    CLIENT_URL: str = "http://localhost:8000"
    """The frontend base URL"""
    CPU_COUNT: int = 0
    """Number of CPUs"""
    SSD_TIMP_DIR: str = ""
    """Directory specifying where background task should process media"""
    RUN_DEBUG: bool = True
    """Run `Litestar` with `debug=True`."""
    SECRET_KEY: str = ""
    """Application secret key."""
    CSRF_COOKIE_SECURE: bool = False
    """Use secure csrf cookie (set to True in production with HTTPS)"""
    CSRF_COOKIE_SAMESITE: Literal['lax', 'strict', 'none'] = 'none'
    """Sets samesite attribute for the csrf cookie"""
    SESSION_SECRET_KEY: str = "random-string"
    """session secret key"""
    SESSION_SAMESITE: Literal['lax', 'strict', 'none'] = 'none'
    """Sets samesite attribute for session cookies"""
    SESSION_SECURE: bool = False
    """Use secure cookies (set to True in production with HTTPS)"""
    ALLOWED_CORS_ORIGINS: list[str] = ["*"]
    """Allowed CORS Origins"""
    ENABLE_INSTRUMENTATION: bool = False
    """Enable OpenTelemetry instrumentation"""
    GOOGLE_OAUTH2_CLIENT_ID: str = ""
    """Google Client ID"""
    GOOGLE_OAUTH2_CLIENT_SECRET: str = ""
    """Google Client Secret"""
    

class BrokerSettings(BaseSettings):
    """Broker configuration"""
    model_config = SettingsConfigDict(
        env_prefix='BROKER_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    REDIS: str = "redis://localhost:6379/0"
    """Redis URL for broker."""


class ObjectStorageSettings(BaseSettings):
    """Object Storage configuration for cloudflare"""
    model_config = SettingsConfigDict(
        env_prefix='OBJS_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    ACCESS_KEY_ID: str = ""
    """Access key"""
    SECRET_ACCESS_KEY: str = ""
    """Secret access key"""
    ENDPOINT: str = ""
    """S3 Endpoint"""
    ENDPOINT_EU: str = ""
    """S3 Endpoint (EU)"""

    #Public bucket
    BUCKET_NAME: str = ""
    """Name of object bucket serving files"""
    PUBLIC_URL: str = ""
    """Public url that exposes the bucket to the internet."""
    SUB_DOMAIN: str = ""
    """Sub domain the bucket has set"""

    #Private bucket
    PRIVATE_BUCKET_NAME: str = ""
    """Name of private object bucket """


class CloudFlareSettings(BaseSettings):
    """Object Storage configuration for cloudflare"""
    model_config = SettingsConfigDict(
        env_prefix='CF_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    #CLOUDFLARE
    TURNSTILE_SITE_KEY: str = ""
    """Cloudflare's turnstile key for bot protection"""
    R2_ACCOUNT_ID: str = ""
    """Account ID for Cloudflare R2"""

class LogSettings(BaseSettings):
    """Logger configuration"""
    model_config = SettingsConfigDict(
        env_prefix='LOG_',
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Regex to exclude paths from logging. Default: Doesnt exclude any"""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Include 'body' of compressed responses in log output."""
    LEVEL: int = 30
    """Stdlib log levels.

    Only emit logs at this level, or higher.
    """
    OBFUSCATE_COOKIES: set[str] = {"XSRF-TOKEN"}
    """Request cookie keys to obfuscate."""
    OBFUSCATE_HEADERS: set[str] = {"Authorization", "X-API-KEY", "X-XSRF-TOKEN"}
    """Request header keys to obfuscate."""
    REQUEST_FIELDS: list[RequestExtractorField] = ["path","method","query","path_params"]
    """Attributes of the [Request][litestar.connection.request.Request] to be
    logged."""
    RESPONSE_FIELDS: list[ResponseExtractorField] = ["status_code"]
    """Attributes of the [Response][litestar.response.Response] to be
    logged."""
    SAQ_LEVEL: int =  50
    """Level to log SAQ logs."""
    SQLALCHEMY_LEVEL: int = 30
    """Level to log SQLAlchemy logs."""
    ASGI_ACCESS_LEVEL: int = 30
    """Level to log uvicorn access logs."""
    ASGI_ERROR_LEVEL: int = 30
    """Level to log uvicorn error logs."""


class MiscSettings(BaseSettings):
    """Miscellanous configuration"""
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding=ENV_ENCODING,
        extra='ignore'
    )

    MAX_CONCURRENT_IMAGES: int = 4
    """Max amount asyncio semaphorge allows at a time"""


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    """App settings"""
    db: DatabaseSettings = DatabaseSettings()
    """Database settings"""
    server: ServerSettings = ServerSettings()
    """Server settings"""
    saq: SaqSettings = SaqSettings()
    """SAQ Background workers"""
    log: LogSettings = LogSettings()
    """Logging"""
    email: EmailSettings = EmailSettings()
    """Email configuration"""
    storage: ObjectStorageSettings = ObjectStorageSettings()
    """General object configuration"""
    broker: BrokerSettings = BrokerSettings()
    """Broker settings (e.g. Redis)"""
    misc: MiscSettings = MiscSettings()
    """Misc settings"""
    logger: ClassVar = structlog.get_logger()
    """Struct logger"""

    

settings = Settings()