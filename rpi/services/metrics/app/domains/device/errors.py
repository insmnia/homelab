from app.core.base_errors import AlreadyExists


class DeviceAlreadyExistsError(AlreadyExists):
    entity = "Device"
