from app.core.logging import hyperlogger
from app.core.settings import get_settings
from fastapi import FastAPI
from app.api.routes import api_router
from app.core.fastapi.http_exceptions import setup_exception_handlers

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Horekih homelab service",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        debug=settings.DEBUG,
        version=settings.VERSION,
    )
    app.logger = hyperlogger

    app.include_router(api_router)
    # exception handlers
    setup_exception_handlers(app)

    return app


app = create_app()
