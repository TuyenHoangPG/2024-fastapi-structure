from datetime import UTC, datetime, timedelta

from fastapi.encoders import jsonable_encoder
from jwt import decode, encode
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.apps.users.user_repository import UsersRepository
from src.apps.users.user_schema import CreateUserRequest, UserAuthResponse, UserResponse
from src.commons.configs.config import BaseSettings
from src.commons.constants.enum import USER_STATUS
from src.commons.constants.message import ERROR_MESSAGE
from src.commons.middlewares.exception import response_4xx
from src.commons.models.user_model import User
from src.commons.services.base import BaseService
from src.commons.services.service_result import return_service

from .auth_schema import SignInRequest, TokenBase, TokenUser

ALGORITHM = "HS256"


class AuthService(BaseService):
    def create_token(
        self,
        content: dict[str, str],
        settings: BaseSettings,
    ):
        to_encode = content.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=settings.jwt_expire_min)
        to_encode.update(TokenBase(exp=expire, iat=now).model_dump())
        encoded_jwt = encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    def create_token_for_user(self, user: User, settings: BaseSettings) -> str:
        token_user = TokenUser(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            role=user.role,
        ).model_dump()
        access_token = self.create_token(content=token_user, settings=settings)
        return access_token

    def get_user_from_token(
        self,
        token: str,
        settings: BaseSettings,
    ) -> TokenUser:
        try:
            decoded_user = decode(token, settings.secret_key, algorithms=ALGORITHM)
            return TokenUser(**decoded_user)

        except Exception as decode_error:
            raise ValueError(ERROR_MESSAGE.INVALID_TOKEN) from decode_error

    @return_service
    async def signup_user(
        self,
        payload: CreateUserRequest,
        users_repo: UsersRepository,
        settings: BaseSettings,
    ) -> UserResponse:
        duplicate_user = await users_repo.get_user_by_email(email=payload.email)

        if duplicate_user:
            return response_4xx(
                status_code=HTTP_400_BAD_REQUEST,
                context={"reason": ERROR_MESSAGE.EMAIL_EXISTED},
            )

        created_user = await users_repo.create_new_user(user_data=payload)
        access_token = self.create_token_for_user(user=created_user, settings=settings)

        user_response = UserAuthResponse.model_validate(created_user)
        user_response.token = access_token

        return dict(
            status_code=HTTP_201_CREATED,
            content={
                "data": jsonable_encoder(user_response),
            },
        )

    @return_service
    async def signin_user(
        self,
        payload: SignInRequest,
        users_repo: UsersRepository,
        settings: BaseSettings,
    ) -> UserResponse:
        user = await users_repo.get_user_by_email(email=payload.email)

        if not user:
            return response_4xx(
                status_code=HTTP_400_BAD_REQUEST,
                context={"reason": ERROR_MESSAGE.INVALID_EMAIL_OR_PASSWORD},
            )

        validation_password = await users_repo.get_user_password_validation(
            user=user, password=payload.password
        )
        if not validation_password:
            return response_4xx(
                status_code=HTTP_400_BAD_REQUEST,
                context={"reason": ERROR_MESSAGE.INVALID_EMAIL_OR_PASSWORD},
            )

        if user.status == USER_STATUS.INACTIVE:
            return response_4xx(
                status_code=HTTP_400_BAD_REQUEST,
                context={"reason": ERROR_MESSAGE.USER_NOT_ACTIVE},
            )

        access_token = self.create_token_for_user(user=user, settings=settings)
        user_data_with_auth = UserAuthResponse.model_validate(user)
        user_data_with_auth.token = access_token

        return dict(
            status_code=HTTP_200_OK,
            content={
                "data": jsonable_encoder(user_data_with_auth),
            },
        )
