from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.apps.dependencies.database import get_repository
from src.apps.dependencies.service import get_service
from src.apps.users.user_repository import UsersRepository
from src.apps.users.user_schema import CreateUserRequest, UserResponse
from src.commons.configs.config import BaseSettings, get_app_settings
from src.commons.middlewares.exception import ERROR_RESPONSES
from src.commons.models.user_model import User
from src.commons.services.service_result import ServiceResult, handle_result

from .auth_schema import SignInRequest
from .auth_service import AuthService

router = APIRouter()


@router.post(
    path="/signup",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:signup",
)
async def signup_user(
    *,
    payload: CreateUserRequest,
    auth_service: AuthService = Depends(get_service(AuthService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: BaseSettings = Depends(get_app_settings),
) -> ServiceResult:
    """
    Signup new users.
    """
    result = await auth_service.signup_user(
        payload=payload, users_repo=users_repo, settings=settings
    )

    return await handle_result(result)


@router.post(
    path="/signin",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:signin",
)
async def signin_user(
    *,
    payload: SignInRequest,
    auth_service: AuthService = Depends(get_service(AuthService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: BaseSettings = Depends(get_app_settings),
) -> ServiceResult:
    """
    Create new users.
    """
    result = await auth_service.signin_user(
        payload=payload,
        users_repo=users_repo,
        settings=settings,
    )

    return await handle_result(result)
