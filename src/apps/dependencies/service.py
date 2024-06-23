from typing import Callable
from src.commons.services.base import BaseService


def get_service(service_type: type[BaseService]) -> Callable[[], BaseService]:
    def _get_service() -> BaseService:
        return service_type()

    return _get_service
