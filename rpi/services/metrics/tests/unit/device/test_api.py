from ipaddress import IPv4Address
from fastapi.testclient import TestClient
import pytest
from app.domains.device.schemas import DeviceCreatePayload
from tests.unit.device.conftest import DeviceFactory


@pytest.mark.asyncio
async def test_register_device(test_client: TestClient):
    # arrange
    new_device_data = DeviceCreatePayload(mac="00:11:22:33:44:55", ip=IPv4Address("192.168.1.1"), name="test1").model_dump(
        mode="json"
    )

    # act
    response = test_client.post("/devices", json=new_device_data)

    # assert
    assert response.status_code == 200  # noqa: PLR2004
    response_data = response.json()
    assert "id" in response_data
    assert response_data["mac"] == new_device_data["mac"]
    assert response_data["ip"] == new_device_data["ip"]
    assert "broker_ip" in response_data
    assert "broker_port" in response_data
    assert "metrics_topic_name" in response_data


@pytest.mark.asyncio
async def test_list_devices(test_client: TestClient):
    # arrange
    device = await DeviceFactory.create()

    # act
    response = test_client.get("/devices")

    # assert
    assert response.status_code == 200  # noqa: PLR2004
    response_data = response.json()
    assert "id" in response_data[0]
    assert response_data[0]["name"] == device.name
