from datetime import datetime

from pydantic import BaseModel, UUID4

from src.commons.constants.enum import USER_ROLES


class TokenBase(BaseModel):
    exp: datetime
    iat: datetime


class TokenUser(BaseModel):
    id: str
    full_name: str
    email: str
    role: str


class SignInRequest(BaseModel):
    email: str
    password: str
