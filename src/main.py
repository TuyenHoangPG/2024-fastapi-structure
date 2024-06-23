from pathlib import Path

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.staticfiles import StaticFiles

from .apps import api_router

from .commons.configs.config import get_app_settings
from .commons.middlewares.events import (
    create_start_app_handler,
    create_stop_app_handler,
)
from .commons.configs.logging import CustomizeLogger
from .commons.middlewares.exception import AppExceptionCase, app_exception_handler
from .commons.middlewares.validation import (
    http_exception_handler,
    request_validation_exception_handler,
)

config_path = Path(__file__).with_name("logging_conf.json")
settings = get_app_settings()


def create_app() -> FastAPI:
    app = FastAPI(**settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(CorrelationIdMiddleware)
    app.logger = CustomizeLogger.make_logger(config_path)
    app.include_router(api_router, prefix=settings.api_prefix)
    app.mount("/static", StaticFiles(directory="src/static"))

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI custom",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"{settings.openapi_prefix}/static/swagger-ui-bundle.js",
            swagger_css_url=f"{settings.openapi_prefix}/static/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=f"{settings.openapi_prefix}/static/redoc.standalone.js",
        )

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    app.add_event_handler("startup", create_start_app_handler(app, settings))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    return app


app = create_app()
