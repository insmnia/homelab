from datetime import datetime, UTC
import uuid

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from app.core import DatabaseEntityId
from app.core.databases.postgres import Base
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.schema import MetaData


def datetime_default_factory() -> datetime:
    return datetime.now().astimezone(tz=UTC)


class BaseDBModel(Base):
    __abstract__ = True

    id: Mapped[DatabaseEntityId] = mapped_column(
        BigInteger,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime_default_factory, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime_default_factory,
        onupdate=datetime_default_factory,
        nullable=False,
    )


def _merge_metadata(*original_metadata: list[MetaData]) -> MetaData:
    merged = MetaData()

    for m in original_metadata:
        for table in m.tables.values():
            table.to_metadata(merged)

    return merged


combined_metadata = _merge_metadata()
