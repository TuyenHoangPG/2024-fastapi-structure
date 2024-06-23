import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import BaseSettings

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI, settings: BaseSettings) -> None:
    logger.info("Connecting to database...")

    engine = create_async_engine(
        url=str(settings.database_url),
        pool_size=settings.max_connection_count,
        max_overflow=0,
        echo=True,
        future=True,
    )
    async_session_factory = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True
    )
    app.state.pool = async_session_factory

    logger.info("Connected to database.")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing database connection...")

    app.state.pool.close_all()

    logger.info("Database connection closed.")
