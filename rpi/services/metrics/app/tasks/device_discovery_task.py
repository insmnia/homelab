from app.core.logging import LoggerMixin
from app.core.network_utils import SELF_IP
from app.scheduler import broker
import asyncio
import subprocess
import httpx
from app.core.settings import get_settings

settings = get_settings()



class DeviceDiscoveryTask(LoggerMixin):
    async def _get_new_device_wifi_ssid(self) -> str | None:
        proc = await asyncio.create_subprocess_shell(
            "nmcli --fields SSID dev wifi",
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stderr:
            self.logger.error(stderr.decode())
            return None

        ssids = stdout.decode().split("\n")[1:]  # amend SSID header
        for ssid in ssids:
            if settings.DEVICE_CONFIGURATION.device_wifi_ap_pattern in ssid:
                return ssid

    async def _connect_to_ssid(self, ssid: str, pwd: str) -> None:
        proc = await asyncio.create_subprocess_shell(
            f"nmcli dev wifi connect {ssid} password '{pwd}'",
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if stdout and (out := stdout.decode()):
            self.logger.info(out)

        if stderr and (err := stderr.decode()):
            self.logger.error(err)

    async def _send_wifi_configuration(self) -> None:
        headers = {
            settings.DEVICE_CONFIGURATION.wifi_ssid_header_name: settings.DEVICE_CONFIGURATION.host_wifi_ssid,
            settings.DEVICE_CONFIGURATION.wifi_pwd_header_name: settings.DEVICE_CONFIGURATION.host_wifi_pwd,
            settings.DEVICE_CONFIGURATION.api_key_header_name: "lkfjsdklfj",
            settings.DEVICE_CONFIGURATION.register_url_header_name: f"{settings.SCHEME}://{SELF_IP}:{settings.PORT}/{settings.DEVICE_CONFIGURATION.api_registration_resource}",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    settings.DEVICE_CONFIGURATION.device_config_endpoint,
                    headers=headers,
                    timeout=settings.DEVICE_CONFIGURATION.device_response_timeout_sec,
                )
                self.logger.info(f"Got response from device: [{response.status_code}]{response.text}")
            except httpx.ReadTimeout:
                self.logger.exception(
                    "Timeouted waiting for response from device. "
                    "Sometimes it's an error, sometimes not. Please online devices"
                )
            except httpx.ConnectError:
                self.logger.exception("")

    async def __call__(self) -> None:
        new_device_wifi_ssid = await self._get_new_device_wifi_ssid()
        if not new_device_wifi_ssid:
            self.logger.info("Didn't find any devices on wifi network")
            return

        await self._connect_to_ssid(new_device_wifi_ssid, settings.DEVICE_CONFIGURATION.device_wifi_pwd)
        await self._send_wifi_configuration()
        await self._connect_to_ssid(  # connect back to host WiFi
            settings.DEVICE_CONFIGURATION.host_wifi_ssid,
            settings.DEVICE_CONFIGURATION.host_wifi_pwd,
        )


task = DeviceDiscoveryTask()


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def discover_devices() -> None:
    await task()


if __name__ == "__main__":
    asyncio.run(task())
