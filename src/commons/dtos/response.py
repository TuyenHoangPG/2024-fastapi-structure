from typing import Any

from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    app_exception: str = ""
    context: dict[str, Any] | None = {"reason": ""}


class ApiResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    message: str = ""
    data: BaseModel
    detail: dict[str, Any] | None = {}
