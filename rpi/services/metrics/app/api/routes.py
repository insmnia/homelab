from fastapi import APIRouter, Request
from datetime import datetime, UTC
from app.core.logging import hyperlogger
from sqlalchemy import text

from app.core.databases.postgres import postgres_engine

api_router = APIRouter(prefix="/api")
start_time = datetime.now(UTC).isoformat()


async def __check_db() -> bool:
    try:
        async with postgres_engine.connect() as conn:
            await conn.execute(text("SELECT * FROM user"))
        return True
    except Exception as e:
        hyperlogger.debug(e)
        return False


@api_router.get("/health")
async def healthcheck(request: Request) -> dict[str, str]:
    db_ok = await __check_db()
    return {
        "api status": "running",
        "start_time": start_time,
        "database status": "running" if db_ok else "unavailable",
    }
