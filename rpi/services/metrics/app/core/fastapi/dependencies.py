from typing import Annotated

from fastapi import Depends
from app.domains.device.repository import DeviceSQLRepository
from app.domains.device.service import DeviceService


DeviceSQLRepositoryDependency = Annotated[DeviceSQLRepository, Depends(lambda: DeviceSQLRepository())]


def get_device_service(
    device_sql_repository: DeviceSQLRepositoryDependency,
) -> DeviceService:
    return DeviceService(device_sql_repository=device_sql_repository)


DeviceServiceDependency = Annotated[DeviceService, Depends(get_device_service)]
