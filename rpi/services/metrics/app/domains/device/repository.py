from app.core.base_sql_repository import Q, BaseSQLRepository, DBFilter
from app.domains.device.models import DeviceSQLModel


class DeviceFilter(DBFilter):
    name: str | None = None

    def apply(self, table: DeviceSQLModel, q: Q) -> Q:
        if self.name is not None:
            q = q.where(table.name == self.name)
        return super().apply(table, q)


class DeviceSQLRepository(BaseSQLRepository[DeviceSQLModel, DeviceFilter]):
    Table = DeviceSQLModel
