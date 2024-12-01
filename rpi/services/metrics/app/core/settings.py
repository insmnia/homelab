from functools import cached_property, lru_cache
import logging
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from app.core.network_utils import SELF_IP


class DeviceConfigurationSettings(BaseModel):
    device_wifi_ap_pattern: str = ""
    device_wifi_pwd: str = ""
    host_wifi_ssid: str = ""
    host_wifi_pwd: str = ""
    device_http_server_ip: str = "192.168.1.1"
    device_http_server_port: int = 80
    device_configuration_resource: str = "configure"
    device_response_timeout_sec: int = 30

    wifi_ssid_header_name: str = "XXX-HL-WIFI-SSID"
    wifi_pwd_header_name: str = "XXX-HL-WIFI-PWD"
    api_key_header_name: str = "XXX-HL-API-KEY"
    register_url_header_name: str = "XXX-HL-REGISTER-URL"

    @cached_property
    def device_config_endpoint(self) -> str:
        return f"http://{self.device_http_server_ip}:{self.device_http_server_port}/{self.device_configuration_resource}"

class MessageBrokerSettings(BaseModel):
    host: str = SELF_IP
    port: int = 1883
    metrics_topic_name: str = "metrics"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HL_",
        env_nested_delimiter="__",
        extra="ignore",
        populate_by_name=True,
    )
    VERSION: str = "0.0.0"
    DEBUG: bool = False
    PORT: int = 9999
    SCHEME: Literal['http', 'https'] = "http"
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "CRITICAL"] = "INFO"

    POSTGRES_DSN: str = ""
    BASE_PAGE_SIZE: int = 10
    DEVICE_CONFIGURATION: DeviceConfigurationSettings = DeviceConfigurationSettings()
    BROKER_CONFIGURATION: MessageBrokerSettings = MessageBrokerSettings()

    @property
    def log_level_int(self) -> int:
        return logging._nameToLevel[self.LOG_LEVEL]


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")
