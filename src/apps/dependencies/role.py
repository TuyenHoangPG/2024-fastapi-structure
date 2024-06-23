from typing import Callable, List

from fastapi import Depends, HTTPException

from src.apps.dependencies.auth import get_current_user
from src.commons.constants.enum import USER_ROLES
from src.commons.constants.message import ERROR_MESSAGE
from src.commons.models.user_model import User
from starlette.status import HTTP_403_FORBIDDEN


def is_valid_role(
    *,
    list_role: List[USER_ROLES],
) -> Callable:
    def check_role(current_user: User = Depends(get_current_user)):
        if current_user.role not in list_role:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=ERROR_MESSAGE.FORBIDDEN,
            )

    return check_role
