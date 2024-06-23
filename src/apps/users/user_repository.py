from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncConnection

from src.apps.dependencies.database import db_error_handler
from src.commons.constants.enum import USER_ROLES, USER_STATUS
from src.commons.database.repositories.base import BaseRepository
from src.commons.models.user_model import User

from .user_schema import CreateUserRequest, UpdateUserRequest


class UsersRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection) -> None:
        super().__init__(conn)

    async def get_user_password_validation(self, *, user: User, password: str) -> bool:
        user_password_checked = user.check_password(password=password)
        return user_password_checked

    @db_error_handler
    async def get_user_by_id(self, *, user_id: int) -> User:
        query = (
            select(User)
            .where(and_(User.id == user_id, User.status == USER_STATUS.ACTIVE))
            .limit(1)
        )

        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()

        return result.User if result is not None else result

    @db_error_handler
    async def get_user_by_email(self, *, email: str) -> User:
        query = (
            select(User)
            .where(and_(User.email == email, User.status == USER_STATUS.ACTIVE))
            .limit(1)
        )

        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()

        return result.User if result is not None else result

    @db_error_handler
    async def get_filtered_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        query = select(User).offset(skip).limit(limit)

        raw_results = await self.connection.execute(query)
        results = raw_results.scalars().all()
        return results

    @db_error_handler
    async def create_new_user(self, *, user_data: CreateUserRequest) -> User:
        created_user = User(**user_data.model_dump(exclude_none=True))
        created_user.salt, created_user.password = User.hash_password(
            password=user_data.password
        )
        created_user.role = USER_ROLES.USER
        self.connection.add(created_user)
        await self.connection.commit()
        await self.connection.refresh(created_user)
        return created_user

    @db_error_handler
    async def update_user(self, *, id: str, user_data: UpdateUserRequest) -> User:
        user = await self.get_user_by_id(user_id=id)
        user.full_name = user_data.full_name

        self.connection.add(user)
        await self.connection.commit()
        await self.connection.refresh(user)
        return user

    @db_error_handler
    async def delete_user(self, *, id: str) -> User:
        user = await self.get_user_by_id(user_id=id)
        user.status = USER_STATUS.INACTIVE

        self.connection.add(user)
        await self.connection.commit()
        await self.connection.refresh(user)
        return user
