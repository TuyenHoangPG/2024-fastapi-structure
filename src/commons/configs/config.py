import logging
import os
import sys
from functools import lru_cache
from typing import Any, Dict, List, Tuple, Type

from loguru import logger
from pydantic import PostgresDsn, SecretStr

from src.commons.constants.enum import ENV_TYPE

from .logging import InterceptHandler

from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv(filename=f'.env.{os.getenv("APP_ENV")}')
load_dotenv(env_file)


class BaseSettings:
    app_env: ENV_TYPE = ENV_TYPE.DEV
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI example application"
    version: str = "0.0.0"

    database_url: PostgresDsn = f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}"
    max_connection_count: int = 10
    min_connection_count: int = 10

    jwt_token_type = "Bearer"
    secret_key: SecretStr = os.getenv("SECRET_KEY")

    api_prefix: str = "/api"

    jwt_expire_min: int = 15

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    s3_access_key: SecretStr = os.getenv("S3_ACCESS_KEY")
    s3_secret_key: SecretStr = os.getenv("S3_SECRET_KEY")
    s3_region: SecretStr = os.getenv("S3_REGION")
    s3_bucket_name: SecretStr = os.getenv("S3_BUCKET_NAME")

    email_user: str = os.getenv("EMAIL_USER")
    email_password: SecretStr = os.getenv("EMAIL_PASSWORD")
    email_from: str = os.getenv("EMAIL_FROM")
    email_host: str = os.getenv("EMAIL_HOST")
    email_port: int = os.getenv("EMAIL_PORT")

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])


class DevSettings(BaseSettings):
    debug: bool = True
    title: str = "Dev FastAPI example application"
    logging_level: int = logging.DEBUG


class QASettings(BaseSettings):
    debug: bool = True
    title: str = "QA FastAPI example application"
    logging_level: int = logging.DEBUG
    max_connection_count: int = 5
    min_connection_count: int = 5
    jwt_expire_min: int = 60


class UATSettings(BaseSettings):
    debug: bool = False
    title: str = "UAT FastAPI example application"
    logging_level: int = logging.DEBUG
    max_connection_count: int = 5
    min_connection_count: int = 5
    jwt_expire_min: int = 60


class ProdSettings(BaseSettings):
    debug: bool = False
    title: str = "FastAPI example application"
    logging_level: int = logging.INFO
    jwt_expire_min: int = 60


environments: Dict[str, Type[BaseSettings]] = {
    "dev": DevSettings,
    "qa": QASettings,
    "uat": UATSettings,
    "prod": ProdSettings,
}


@lru_cache
def get_app_settings() -> BaseSettings:
    app_env = os.getenv("APP_ENV")
    config = environments[app_env]

    return config()
