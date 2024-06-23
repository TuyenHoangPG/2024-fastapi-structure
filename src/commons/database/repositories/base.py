from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Base Repository for all repositories."""

    def __init__(self, conn: AsyncSession) -> None:
        self._conn = conn

    @property
    def connection(self) -> AsyncSession:
        return self._conn
