from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.types import Boolean

from app.models.base_sql import BaseSQLModel, datetime_default_factory


class DeviceSQLModel(BaseSQLModel):
    __tablename__ = "device"
    mac: Mapped[str] = mapped_column(String(17))
    ip: Mapped[str] = mapped_column(String(15))

    name: Mapped[str | None]
    description: Mapped[str | None]
    is_online: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_default_factory, nullable=False)

    __table_args__ = (UniqueConstraint("mac", "ip", name="mac_ip_uc"),)
