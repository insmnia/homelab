from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
)
from loguru import logger

from app.core.errors.base import AlreadyExists, NotFound


async def any_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled exception occured: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content="Internal server error occured, please contact support if error persists",
    )


async def not_found_exception_handler(_: Request, exc: NotFound) -> JSONResponse:
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=str(exc))


async def conflict_exception_handler(_: Request, exc: AlreadyExists) -> JSONResponse:
    return JSONResponse(status_code=HTTP_409_CONFLICT, content=str(exc))


def setup_exception_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(Exception, any_exception_handler)
    app.add_exception_handler(NotFound, not_found_exception_handler)
    app.add_exception_handler(AlreadyExists, conflict_exception_handler)
    return app
