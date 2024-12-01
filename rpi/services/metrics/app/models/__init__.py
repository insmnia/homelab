from sqlalchemy.schema import MetaData

from app.domains.device.models import DeviceSQLModel


def _merge_metadata(*original_metadata: list[MetaData]) -> MetaData:
    merged = MetaData()

    for m in original_metadata:
        for table in m.tables.values():
            table.to_metadata(merged)

    return merged


combined_metadata = _merge_metadata(DeviceSQLModel.metadata)
