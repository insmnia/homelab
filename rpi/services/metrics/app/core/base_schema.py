from datetime import datetime
from pydantic import BaseModel

from app.core import DatabaseEntityId


class BaseSchemaModel(BaseModel):
    id: DatabaseEntityId
    created_at: datetime
    updated_at: datetime | None = None
