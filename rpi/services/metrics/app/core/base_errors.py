from typing import Any

from app.core.settings import get_settings

settings = get_settings()


class NotFound(Exception):
    entity: str

    def __init__(self, *_: list, **kwargs: dict[str, Any]) -> None:
        if settings.DEBUG:
            for k, v in kwargs.items():
                kwargs[k] = str(v)
            super().__init__(f"{self.entity} is not found with given attributes: {kwargs}")
        else:
            super().__init__(f"{self.entity} is not found")


class AlreadyExists(Exception):
    entity: str

    def __init__(self, *_: list, **kwargs: dict[str, Any]) -> None:
        if settings.DEBUG:
            for k, v in kwargs.items():
                kwargs[k] = str(v)
            super().__init__(f"Such {self.entity} already exists with given attributes: {kwargs}")
        else:
            super().__init__(f"Such {self.entity} already exists")
