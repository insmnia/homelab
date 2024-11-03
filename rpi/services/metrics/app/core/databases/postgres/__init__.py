from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.core.settings import get_settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger


settings = get_settings()
postgres_engine = create_async_engine(url=settings.POSTGRES_DSN, echo=False)
AsyncPostgresSession = async_sessionmaker(
    postgres_engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgresSession() as _session:
        try:
            yield _session
        except Exception as e:
            logger.error(f"Error on database session: {e}")
            await _session.rollback()
            raise e
        finally:
            await _session.close()


@asynccontextmanager
async def tx_session_factory() -> AsyncGenerator[AsyncSession, None]:
    """Transactional session"""
    async with AsyncPostgresSession() as _session:
        try:
            async with _session.begin():
                yield _session
                await _session.commit()
        except Exception as e:
            logger.error(f"[TX Session Rollback] Error on database session: {e}")
            await _session.rollback()
            raise e
        finally:
            await _session.close()
