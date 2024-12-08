from app.core.logging import setup_logging
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
    setup_logging(loglevel=settings.log_level_int)

    app.include_router(api_router)
    # exception handlers
    app = setup_exception_handlers(app)

    return app


app = create_app()
