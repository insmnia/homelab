import pytest

from app.core.settings import DeviceConfigurationSettings
from app.tasks.device_discovery_task import DeviceDiscoveryTask
from unittest.mock import patch
from pytest_httpx import HTTPXMock


class MockSettings:
    SCHEME = "https"
    PORT = 9999
    DEVICE_CONFIGURATION = DeviceConfigurationSettings(
        device_wifi_ap_pattern="AP_PATTERN",
        device_wifi_pwd="some_password",  # noqa: S106
        wifi_ssid_header_name="X-Wifi-SSID",
        wifi_pwd_header_name="X-Wifi-Password",  # noqa: S106
        api_key_header_name="X-API-Key",
        register_url_header_name="X-Register-URL",
        device_configuration_resource="http://example.com/config",
        host_wifi_ssid="HOST_SSID",
        host_wifi_pwd="HOST_PASSWORD",  # noqa: S106
        device_response_timeout_sec=5,
        api_registration_resource="register",
    )


@pytest.fixture
def mock_settings() -> MockSettings:
    return MockSettings()


@pytest.fixture
def task(mock_settings: MockSettings):
    return DeviceDiscoveryTask(mock_settings)


@pytest.mark.asyncio
async def test_get_new_device_wifi_ssid(task: DeviceDiscoveryTask):
    # act & assert
    with patch("asyncio.create_subprocess_shell") as mock_subprocess:
        mock_subprocess.return_value.communicate.return_value = (b"SSID\nAP_PATTERN_SSID\n", b"")
        ssid = await task._get_new_device_wifi_ssid()
        assert ssid == "AP_PATTERN_SSID"


@pytest.mark.asyncio
async def test_get_new_device_wifi_ssid_no_output(task: DeviceDiscoveryTask):
    # act & assert
    with patch("asyncio.create_subprocess_shell") as mock_subprocess:
        mock_subprocess.return_value.communicate.return_value = (b"", b"Error message")
        ssid = await task._get_new_device_wifi_ssid()
        assert ssid is None


@pytest.mark.asyncio
async def test_send_wifi_configuration(task: DeviceDiscoveryTask, mock_settings: MockSettings, httpx_mock: HTTPXMock):
    # arrange
    httpx_mock.add_response(
        url=mock_settings.DEVICE_CONFIGURATION.device_config_endpoint,
        method="POST",
        status_code=200,
        json={"message": "Success"},
    )
    # act
    await task._send_wifi_configuration()


@pytest.mark.asyncio
async def test_wifi_send_configuration_error(task: DeviceDiscoveryTask, mock_settings: MockSettings, httpx_mock: HTTPXMock):
    # arrange
    httpx_mock.add_response(
        url=mock_settings.DEVICE_CONFIGURATION.device_config_endpoint,
        method="POST",
        status_code=504,
    )
    await task._send_wifi_configuration()


@pytest.mark.asyncio
async def test_full_flow(task: DeviceDiscoveryTask, mock_settings: MockSettings, httpx_mock: HTTPXMock):
    # arrange
    httpx_mock.add_response(
        url=mock_settings.DEVICE_CONFIGURATION.device_config_endpoint,
        method="POST",
        status_code=200,
        json={"message": "Success"},
    )

    # act & assert
    with patch("asyncio.create_subprocess_shell") as mock_subprocess:
        mock_subprocess.return_value.communicate.return_value = (b"SSID\nAP_PATTERN_SSID\n", b"")
        await task()
