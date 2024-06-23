from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.orm import declarative_base, declared_attr

from ..utils.datetime import utc_now


class CustomBaseModel:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __name__: str

    id = Column(UUID(), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


CustomBaseModel = declarative_base(cls=CustomBaseModel)
