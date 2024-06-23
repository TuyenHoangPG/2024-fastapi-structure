from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src.apps.dependencies.auth import get_current_user
from src.apps.dependencies.database import get_repository
from src.apps.dependencies.role import is_valid_role
from src.apps.dependencies.service import get_service
from src.apps.users.user_repository import UsersRepository
from src.commons.constants.enum import USER_ROLES
from src.commons.models.user_model import User


from .user_schema import UpdateUserRequest, UserResponse
from .user_service import UsersService
from src.commons.middlewares.exception import ERROR_RESPONSES
from src.commons.services.service_result import handle_result

router = APIRouter()


@router.get(
    "/me",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:get-current-user",
)
async def get_current_user_info(
    *,
    user: User = Depends(get_current_user),
    user_service: UsersService = Depends(get_service(UsersService)),
) -> UserResponse:
    result = await user_service.get_current_user(user=user)

    return await handle_result(result)


@router.get(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:info-by-id",
)
async def read_user_by_id(
    *,
    user: User = Depends(get_current_user),
    is_valid_role=Depends(
        is_valid_role(list_role=[USER_ROLES.ADMIN, USER_ROLES.SUPER_ADMIN])
    ),
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_id: str,
) -> UserResponse:
    result = await users_service.get_user_by_id(user_id=user_id, users_repo=users_repo)

    return await handle_result(result)


@router.patch(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:patch-by-id",
)
async def update_user(
    *,
    user: User = Depends(get_current_user),
    is_valid_role=Depends(
        is_valid_role(list_role=[USER_ROLES.ADMIN, USER_ROLES.SUPER_ADMIN])
    ),
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    payload: UpdateUserRequest,
    user_id: str,
) -> UserResponse:
    result = await users_service.update_user(
        user_id=user_id, payload=payload, users_repo=users_repo
    )
    return await handle_result(result)


@router.delete(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:delete-by-id",
)
async def delete_user(
    *,
    user: User = Depends(get_current_user),
    is_valid_role=Depends(
        is_valid_role(list_role=[USER_ROLES.ADMIN, USER_ROLES.SUPER_ADMIN])
    ),
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_id: str,
) -> UserResponse:
    result = await users_service.delete_user(user_id=user_id, users_repo=users_repo)
    return await handle_result(result)
