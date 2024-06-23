import logging

from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from src.commons.constants.message import ERROR_MESSAGE
from src.commons.middlewares.exception import response_4xx
from src.commons.models.user_model import User
from src.commons.services.base import BaseService
from src.commons.services.service_result import ServiceResult, return_service

from .user_repository import UsersRepository
from .user_schema import UpdateUserRequest, UserResponse, UsersFilters

logger = logging.getLogger(__name__)


class UsersService(BaseService):
    @return_service
    async def get_user_by_id(
        self,
        user_id: str,
        users_repo: UsersRepository,
    ) -> ServiceResult:
        user = await users_repo.get_user_by_id(user_id=user_id)
        if not user:
            return response_4xx(
                status_code=HTTP_404_NOT_FOUND,
                context={"reason": ERROR_MESSAGE.USER_NOT_FOUND},
            )

        return dict(
            status_code=HTTP_200_OK,
            content={
                "data": jsonable_encoder(UserResponse.model_validate(user)),
            },
        )

    @return_service
    async def get_current_user(
        self,
        user: User,
    ) -> ServiceResult:
        return dict(
            status_code=HTTP_200_OK,
            content={
                "data": jsonable_encoder(UserResponse.model_validate(user)),
            },
        )

    def get_users_filters(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> UsersFilters:
        return UsersFilters(
            skip=skip,
            limit=limit,
        )

    @return_service
    async def update_user(
        self,
        user_id: str,
        payload: UpdateUserRequest,
        users_repo: UsersRepository,
    ) -> UserResponse:
        updated_user = await users_repo.update_user(id=user_id, user_data=payload)

        return dict(
            status_code=HTTP_200_OK,
            content={
                "data": jsonable_encoder(UserResponse.model_validate(updated_user)),
            },
        )

    @return_service
    async def delete_user(
        self,
        user_id: str,
        users_repo: UsersRepository,
    ) -> ServiceResult:
        deleted_user = await users_repo.delete_user(id=user_id)

        return dict(
            status_code=HTTP_200_OK,
            content={
                "data": jsonable_encoder(UserResponse.model_validate(deleted_user)),
            },
        )
