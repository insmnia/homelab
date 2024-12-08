from datetime import datetime
from typing import TypedDict

from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.base_sql_repository import UniqueKeyDuplicateError
from app.domains.device.repository import DeviceFilter, DeviceSQLRepository


class Device:
    class CreateData(TypedDict):
        mac: str
        ip: str
        name: str | None
        description: str | None

    class RetrieveData(CreateData, TypedDict):
        id: int
        created_at: datetime
        updated_at: datetime


class DeviceService:
    def __init__(
        self,
        device_sql_repository: DeviceSQLRepository,
        *,
        sql_db_session: AsyncSession | None = None,
    ) -> None:
        self._device_sql_repo = device_sql_repository
        self._sql_db_session = sql_db_session

    def set_sql_db_session(self, sql_db_session: AsyncSession | None = None) -> None:
        self._sql_db_session = sql_db_session

    async def create(self, input_data: Device.CreateData) -> Device.RetrieveData:
        try:
            db_model = await self._device_sql_repo.create(data=input_data, session=self._sql_db_session)
        except UniqueKeyDuplicateError:
            # device already exists, need to send broker settings anyway for device to start operating
            db_model = await self._device_sql_repo.list(DeviceFilter(name=input_data['name']), page_size=1)
            db_model = db_model[0]

        return Device.RetrieveData(**db_model.__dict__)

    async def list(self, page: int, page_size: int) -> list[Device.RetrieveData]:
        devices = await self._device_sql_repo.list(page=page, page_size=page_size)
        return [Device.RetrieveData(**d.__dict__) for d in devices]
