from fastapi import APIRouter, Request
from datetime import datetime, UTC

from app.core.databases.postgres import check_db
from app.domains.device.router import router as device_router

api_router = APIRouter(prefix="/api")
api_router.include_router(device_router, prefix="/devices", tags=["Devices"])
start_time = datetime.now(UTC).isoformat()


@api_router.get("/health")
async def healthcheck(request: Request) -> dict[str, str]:
    db_ok = await check_db()
    return {
        "api status": "running",
        "start_time": start_time,
        "database status": "running" if db_ok else "unavailable",
    }
