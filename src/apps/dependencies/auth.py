from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
)

from src.apps.auth.auth_service import AuthService
from src.apps.dependencies.database import get_repository
from src.apps.dependencies.service import get_service
from src.apps.users.user_repository import UsersRepository
from src.commons.configs.config import BaseSettings, get_app_settings
from src.commons.constants.message import ERROR_MESSAGE
from src.commons.models.user_model import User


class CustomAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException as auth_exc:
            raise HTTPException(
                status_code=auth_exc.status_code,
                detail=ERROR_MESSAGE.UNAUTHORIZED,
            )


def _get_auth_from_header(
    api_key: str = Security(CustomAPIKeyHeader(name="Authorization")),
    settings: BaseSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGE.INVALID_TOKEN,
        )

    if token_prefix != settings.jwt_token_type:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=ERROR_MESSAGE.INVALID_TOKEN_TYPE
        )

    return token


async def get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_auth_from_header),
    settings: BaseSettings = Depends(get_app_settings),
    auth_service: AuthService = Depends(get_service(AuthService)),
) -> User:
    try:
        token_user = auth_service.get_user_from_token(token=token, settings=settings)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGE.INVALID_TOKEN,
        )

    try:
        user = await users_repo.get_user_by_email(email=token_user.email)

        if user is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGE.INVALID_TOKEN,
            )
        else:
            return user

    except ValueError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGE.INVALID_TOKEN,
        )
