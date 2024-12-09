import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.device.service import Device, DeviceService
import secrets

from tests.unit.device.conftest import DeviceFactory


@pytest.mark.asyncio
async def test_service_register_device(device_service: DeviceService) -> None:
    # arrange
    device_name = secrets.token_hex(3)

    new_device = Device.CreateData(
        mac="0:0:0:0:0", ip="192.168.1.1", name=device_name, description=f"test device with name {device_name}"
    )

    # act
    created_device = await device_service.create(new_device)

    # assert
    assert created_device["id"] is not None
    assert created_device["name"] == device_name


@pytest.mark.asyncio
@pytest.mark.skip(reason="Some issue with session rollback. Investigate later...")
async def test_service_register_duplicate(device_service: DeviceService, db_session: AsyncSession) -> None:
    # arrange
    device = await DeviceFactory.create()

    new_device = Device.CreateData(
        mac=device.mac,
        ip=device.ip,
        name=device.name,
    )

    # act
    created_device = await device_service.create(new_device)

    # assert
    assert created_device["id"] is not None
    assert created_device["name"] == device.name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "devices_amount, page_size, expected",
    [
        (1, 1, 1),
        (5, 3, 3),
        (2, 5, 2),
    ],
)
async def test_service_list_devices(devices_amount: int, page_size: int, expected: int, device_service: DeviceService) -> None:
    # arrange
    await DeviceFactory.create_batch(devices_amount)

    # act
    devices = await device_service.list(page=1, page_size=page_size)

    # assert
    assert len(devices) == expected
