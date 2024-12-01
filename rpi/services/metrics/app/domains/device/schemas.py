from typing import Annotated
from pydantic import BaseModel, Field, IPvAnyAddress

from app.core.base_schema import BaseSchemaModel


class DeviceCreatePayload(BaseModel):
    mac: Annotated[str, Field(max_length=17)]
    ip: IPvAnyAddress

    name: Annotated[str | None, Field(max_length=50)]
    description: Annotated[str | None, Field(max_length=255)] = None

class DeviceResponsePayload(BaseSchemaModel, DeviceCreatePayload):
    ...

class DeviceRegisterResponsePayload(DeviceResponsePayload):
    broker_ip: str
    broker_port: int
    metrics_topic_name: str
