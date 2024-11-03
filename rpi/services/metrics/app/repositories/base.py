from typing import Any, Generic, Optional, TypeAlias, TypeVar
from uuid import UUID

import sqlalchemy as sa

from app.core.databases.postgres import session_factory
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession

from models.base import BaseDBModel
from app.core.settings import get_settings


T = TypeVar("T", bound=BaseDBModel)
Q = TypeVar("Q", sa.Select, sa.Update, sa.Delete)
M: TypeAlias = dict[str, Any]
settings = get_settings()


class DBFilter(BaseModel, Generic[T]):
    def apply(self, table: T, q: Q) -> Q:
        return q


F = TypeVar("F", bound=DBFilter[Any])


class BaseRepository(Generic[T, F]):
    Table: T

    async def create(self, data: M, session: Optional[AsyncSession] = None) -> T:
        instance = self.Table(**data)

        if not session:
            async with session_factory() as new_session:
                new_session.add(instance)
                await new_session.commit()
                await new_session.refresh(instance)
        else:
            session.add(instance)
            await session.flush()
        return instance

    async def update(
        self, id: UUID, data: M, session: Optional[AsyncSession] = None
    ) -> None:
        data.pop("id", None)
        q = sa.update(self.Table).where(self.Table.id == id).values(**data)

        if not session:
            async with session_factory() as new_session:
                await new_session.execute(q)
                await new_session.commit()
        else:
            await session.execute(q)
            await session.flush()

    async def get(self, id: UUID, db_filter: Optional[F] = None) -> T | None:
        async with session_factory() as session:
            q = sa.select(self.Table).where(self.Table.id == id)
            q = db_filter.apply(self.Table, q) if db_filter else q

            result = (await session.execute(q)).scalars().first()
            return result

    async def exists(self, db_filter: Optional[F] = None) -> bool:
        async with session_factory() as session:
            q = sa.exists(self.Table).select()
            q = db_filter.apply(self.Table, q) if db_filter else q

            result = await session.scalar(q)
            return result

    async def list(
        self,
        db_filter: Optional[F] = None,
        page_size: int = settings.api_configuration.DEFAULT_PAGE_SIZE,
        page: int = 0,
    ) -> list[T]:
        async with session_factory() as session:
            q = sa.select(self.Table)
            q = db_filter.apply(self.Table, q) if db_filter else q

            if page_size:
                q = q.limit(page_size)
            if page:
                q = q.offset((page - 1) * page_size)

            result = (await session.execute(q)).scalars().all()
            return result

    async def delete(
        self, db_filter: Optional[F] = None, session: Optional[AsyncSession] = None
    ) -> None:
        q = sa.delete(self.Table)
        q = db_filter.apply(self.Table, q) if db_filter else q
        if not session:
            async with session_factory() as new_session:
                await new_session.execute(q)
                await new_session.commit()
        else:
            await session.execute(q)
