from datetime import datetime, UTC

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from app.core import DatabaseEntityId
from app.core.databases.postgres import Base
from sqlalchemy import BigInteger, DateTime, Integer


def datetime_default_factory() -> datetime:
    return datetime.now().astimezone(tz=UTC)


class BaseSQLModel(Base):
    __abstract__ = True

    id: Mapped[DatabaseEntityId] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_default_factory, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime_default_factory,
        onupdate=datetime_default_factory,
        nullable=False,
    )
