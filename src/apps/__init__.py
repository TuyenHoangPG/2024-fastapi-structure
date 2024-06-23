from fastapi import APIRouter
from .auth import auth_controller as auth
from .users import user_controller as users


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
