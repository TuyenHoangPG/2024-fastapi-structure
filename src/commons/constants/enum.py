from enum import Enum


class ENV_TYPE(Enum):
    PROD: str = "prod"
    UAT: str = "uat"
    QA: str = "qa"
    DEV: str = "dev"


class USER_ROLES(Enum):
    ADMIN: str = "ADMIN"
    SUPER_ADMIN: str = "SUPER_ADMIN"
    USER: str = "USER"


class USER_STATUS(Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
