from pydantic import BaseModel, ConfigDict, EmailStr, UUID4

from src.commons.constants.enum import USER_ROLES


class CreateUserRequest(BaseModel):
    full_name: str
    password: str
    email: EmailStr


class UpdateUserRequest(BaseModel):
    full_name: str


class UsersFilters(BaseModel):
    skip: int | None = 0
    limit: int | None = 100


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID4
    email: str
    full_name: str
    role: USER_ROLES
    status: str


class UserAuthResponse(UserResponse):
    token: str | None = None
