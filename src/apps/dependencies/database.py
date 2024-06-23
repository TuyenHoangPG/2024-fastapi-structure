from collections.abc import AsyncGenerator, Callable
import logging

from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.commons.constants.message import ERROR_MESSAGE
from src.commons.database.repositories.base import BaseRepository
from src.commons.middlewares.exception import AppExceptionCase


logger = logging.getLogger(__name__)


def db_error_handler(func) -> callable:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DBAPIError as e:
            db_error_context = e.orig.__context__.__str__()
            logger.error("db_error_context: %s", db_error_context)
            raise AppExceptionCase(
                context={"reason": ERROR_MESSAGE.SERVER_ERROR, "code": e.code},
                status_code=500,
            )

    return wrapper


def _get_db_session(request: Request) -> AsyncSession:
    return request.app.state.pool


async def _get_connection_from_session(
    pool: AsyncSession = Depends(_get_db_session),
) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session:
        yield session


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        session: AsyncSession = Depends(_get_connection_from_session),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo
