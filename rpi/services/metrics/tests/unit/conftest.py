from typing import AsyncIterator, Iterator
from fastapi import FastAPI
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker
from app.core.fastapi.dependencies import get_device_service
from app.core.fastapi.http_exceptions import setup_exception_handlers
from app.domains.device.repository import DeviceSQLRepository
from app.domains.device.service import DeviceService
from app.models import combined_metadata
from unittest.mock import MagicMock, patch
import pytest_asyncio
from app.api.routes import api_router
from fastapi.testclient import TestClient

engine = create_async_engine("sqlite+aiosqlite:///:memory:")
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
sc_session = scoped_session(async_session)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncIterator[AsyncSession]:
    """Create a new database session for a test."""
    async with engine.begin() as connection:
        await connection.run_sync(combined_metadata.drop_all)
        await connection.run_sync(combined_metadata.create_all)

        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(autouse=True)
def mock_session_factory(db_session: AsyncSession):
    with patch("app.core.base_sql_repository.session_factory", return_value=db_session):
        yield


# ------ DEVICE ------


@pytest.fixture
def device_repository() -> DeviceSQLRepository:
    return DeviceSQLRepository()


@pytest.fixture
def device_service(device_repository: DeviceSQLRepository, db_session: AsyncSession) -> DeviceService:
    return DeviceService(
        device_sql_repository=device_repository,
        sql_db_session=db_session,
    )


# ------ FASTAPI ------


@pytest.fixture
def app(device_service: DeviceService) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app = setup_exception_handlers(app)
    app.dependency_overrides[get_device_service] = lambda: device_service
    return app


@pytest.fixture
def test_client(app: FastAPI) -> Iterator[TestClient]:
    with patch("app.core.settings.get_self_ip", return_value="192.168.1.1"):
        client = TestClient(app=app, base_url="http://testserver/api")
        yield client


@pytest.fixture(autouse=True)
def mock_subprocess() -> Iterator[MagicMock]:
    with patch("subprocess.check_output") as mock:
        yield mock
