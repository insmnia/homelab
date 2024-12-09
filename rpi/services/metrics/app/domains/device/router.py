from fastapi import APIRouter, Query, status

from app.core.settings import get_settings
from app.core.fastapi.dependencies import DeviceServiceDependency
from app.domains.device.schemas import DeviceCreatePayload, DeviceRegisterResponsePayload, DeviceResponsePayload
from app.domains.device.service import Device

router = APIRouter()
settings = get_settings()


@router.post(
    "",
    response_model=DeviceRegisterResponsePayload,
    responses={
        status.HTTP_200_OK: {
            "model": DeviceRegisterResponsePayload,
            "description": (
                "Device response. If device is already registered, the device obj is returned. "
                "This is done to prevent multiple HTTP requests from device side and do "
                "registration as-fast-as-possible"
            ),
        }
    },
)
async def register_device(
    device_service: DeviceServiceDependency, payload: DeviceCreatePayload
) -> DeviceRegisterResponsePayload:
    device = await device_service.create(Device.CreateData(**payload.model_dump(mode="json")))
    return DeviceRegisterResponsePayload.model_construct(
        **device,
        broker_ip=settings.BROKER_CONFIGURATION.host,
        broker_port=settings.BROKER_CONFIGURATION.port,
        metrics_topic_name=f"{settings.BROKER_CONFIGURATION.metrics_topic_name}/{device['id']}",
    )


@router.get("", response_model=list[DeviceResponsePayload])
async def list_devices(
    device_service: DeviceServiceDependency,
    page: int = Query(default=1),
    page_size: int = Query(default=settings.BASE_PAGE_SIZE),
) -> list[Device.RetrieveData]:
    devices = await device_service.list(page, page_size)
    return devices
