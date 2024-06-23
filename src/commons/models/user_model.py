from sqlalchemy import Column, Enum, String

from ..constants.enum import USER_ROLES, USER_STATUS
from ..utils.password import generate_salt, get_password_hash, verify_password
from .base_model import CustomBaseModel


class User(CustomBaseModel):
    __tablename__ = "users"

    email = Column(String(255), nullable=False, unique=True)
    full_name = Column(
        String(255),
        nullable=False,
    )
    salt = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(
        Enum(USER_ROLES),
        nullable=False,
        default=USER_ROLES.USER,
    )
    status = Column(
        Enum(USER_STATUS),
        nullable=False,
        default=USER_STATUS.ACTIVE,
    )

    def __repr__(self):
        return f"<User email={self.email}, role={self.role}>"

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.password)

    @classmethod
    def hash_password(cls, password: str) -> tuple[str, str]:
        salt = generate_salt()
        return salt, get_password_hash(salt + password)
